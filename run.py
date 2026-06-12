import subprocess
import sys
import csv
import json
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.stats import ttest_ind

from data.config import (
    morphologies,
    load_parameters,
    ensure_output_dir,
    output_path,
    rel,
)
from data.stats_utils import cohens_d

ROOT = Path(__file__).parent

MORPHOLOGY_MODES = morphologies()
TOTAL_STEPS = len(MORPHOLOGY_MODES) + 6


def _step(n, label):
    print(f"\n[{n}/{TOTAL_STEPS}] {label}")


def run(script):
    print(f"\n[RUN] {script}")
    subprocess.run([sys.executable, str(ROOT / script)], check=True)


def run_coupling(mode):
    import data.node_coupling as coupling

    output_file = output_path(f"simulation_results_{mode}.csv")
    tensor_file = output_path(f"af_tensors_{mode}.npz")

    topo_report = coupling.run_sweep(mode, output_file, tensor_file)
    print(f"      Topology: {topo_report}")

    with open(output_file) as f:
        rows = list(csv.DictReader(f))
    last = rows[-1]
    print(
        f"      Peak AF: {float(last['Peak_AF']):.2f} | "
        f"Coherence: {float(last['Coherence_Ratio']):.2f} | "
        f"Merit Scaled: {float(last['Merit_Scaled']):.2f}  "
        f"(d={float(last['Distance']):.1f})"
    )


def _col(rows, key):
    return [float(r[key]) for r in rows]


def compute_statistical_summary(output_file=None):
    if output_file is None:
        output_file = output_path("statistical_summary.csv")

    morphology_data = {}
    for mode in MORPHOLOGY_MODES:
        with open(output_path(f"simulation_results_{mode}.csv")) as f:
            morphology_data[mode] = list(csv.DictReader(f))

    metrics = ["Merit_Scaled", "Coherence_Ratio", "Peak_AF"]
    pair_combos = list(combinations(MORPHOLOGY_MODES, 2))

    rows_out = []
    for metric in metrics:
        for a, b in pair_combos:
            s1 = _col(morphology_data[a], metric)
            s2 = _col(morphology_data[b], metric)
            t, p = ttest_ind(s1, s2, equal_var=False)
            d = cohens_d(s1, s2)
            sig = "yes" if p < 0.05 else "no"
            if np.isnan(d):
                size    = "n/a"
                d_write = "n/a"
            else:
                size = (
                    "extreme" if abs(d) > 50
                    else "large"  if abs(d) > 0.8
                    else "medium" if abs(d) > 0.5
                    else "small"
                )
                d_write = round(d, 4)
            pair_label = f"{a.capitalize()} vs {b.capitalize()}"
            rows_out.append([
                metric, pair_label,
                round(float(t), 4),
                round(float(p), 6),
                sig, d_write, size,
            ])

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Metric", "Pair", "t_statistic", "p_value",
            "Significant_p05", "Cohens_d", "Effect_size",
        ])
        writer.writerows(rows_out)

    print(f"      {'Metric':<18} {'Pair':<32} {'p':>7}  {'d':>7}  {'sig':>4}  effect")
    for row in rows_out:
        d_display = f"{'n/a':>7}" if row[5] == "n/a" else f"{row[5]:>7.3f}"
        print(
            f"      {row[0]:<18} {row[1]:<32} "
            f"{row[3]:>7.4f}  {d_display}  {row[4]:>4}  {row[6]}"
        )

    return rows_out


def schumann_comparison(f_simulated):
    from data.schumann_reference import schumann_report
    for line in schumann_report(f_simulated):
        print(f"      {line}")


def multi_seed_step():
    from data.multi_seed_analysis import run_multi_seed
    results = run_multi_seed(output_path("multi_seed_summary.csv"))
    for mode, r in results.items():
        m = r["Merit_Scaled"]
        c = r["Coherence_Ratio"]
        print(
            f"      {mode:12s}  "
            f"Merit {m['mean']:.4f} +/- {m['std']:.4f}  |  "
            f"Coherence {c['mean']:.4f} +/- {c['std']:.4f}"
        )
    return results


def write_exploration_summary(resonance_data, derivation_data, multi_seed_results,
                               output_file=None):
    from data.schumann_reference import nearest_schumann_mode
    from data.multi_seed_analysis import SEEDS

    if output_file is None:
        output_file = output_path("exploration_summary.json")

    params = load_parameters()

    f_sim = resonance_data["f_resonance_Hz"]
    nearest_hz, mode_n, deviation_pct = nearest_schumann_mode(f_sim)

    summary = {
        "pipeline_version": "1.2.2",
        "parameter_derivation": {
            "f_target_hz":  derivation_data["f_target_hz"],
            "L_H":          derivation_data["L_H"],
            "C_derived_F":  derivation_data["C_F"],
            "f_check_hz":   derivation_data["f_actual_hz"],
        },
        "resonance_baseline": {
            "f_simulated_hz":           round(f_sim, 4),
            "Q_factor":                 round(resonance_data["Q_factor"], 4),
            "schumann_nearest_mode_hz": nearest_hz,
            "schumann_mode_index":      mode_n,
            "deviation_pct":            deviation_pct,
            "reference":                "NOAA/GFZ Potsdam (published reference values)",
        },
        "experimental_configuration": {
            "n_nodes":             params["VI_experimental_sweep_parameters"]["n_nodes"],
            "reference_seed":      params["VI_experimental_sweep_parameters"]["seed"],
            "beta_loss_factor":    params["VI_experimental_sweep_parameters"]["beta_loss_factor"],
            "noise_level":         params["VI_experimental_sweep_parameters"].get("noise_level", 0.15),
            "connection_radius_m": params["VI_experimental_sweep_parameters"]["connection_radius_m"],
            "k0_base":             params["VII_array_factor_parameters"]["k0_base"],
            "k_modulation_coeff":  params["VII_array_factor_parameters"]["k_modulation_coeff"],
            "q_reference":         params["VII_array_factor_parameters"]["q_reference"],
        },
        "morphologies": params["VIII_pipeline"]["morphologies"],
        "multi_seed_analysis": {
            "seeds": SEEDS,
            "morphologies": {
                mode: {
                    metric: {
                        "mean": round(r["mean"], 6),
                        "std":  round(r["std"],  6),
                    }
                    for metric, r in vals.items()
                }
                for mode, vals in multi_seed_results.items()
            },
        },
    }

    with open(output_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"      Written: {rel(output_file)}")


def main():
    n = len(MORPHOLOGY_MODES)
    total_pairs = n * (n - 1) // 2

    ensure_output_dir()

    print("\n===================================================")
    print(" DETERMINISTIC COMPARATIVE MORPHOLOGICAL PIPELINE v1.2.2")
    print(f" {n} morphologies | {total_pairs} pairs | seeds 42-46")
    print("===================================================")

    _step(1, "Parameter derivation (f_target -> L, C)...")
    from data.parameter_derivation import report as derive_report
    derivation_data = derive_report()

    _step(2, "Node resonance baseline (simulation)....")
    run("data/node_resonance.py")
    with open(output_path("resonance_params.json")) as f:
        resonance_data = json.load(f)
    print("\n      Schumann resonance external comparison:")
    schumann_comparison(resonance_data["f_resonance_Hz"])

    for idx, mode in enumerate(MORPHOLOGY_MODES, start=3):
        _step(idx, f"{mode.upper()} sweep...")
        run_coupling(mode)

    _step(n + 3, f"Statistical separation (Welch t-test + Cohen d, 3 metrics x {total_pairs} pairs)...")
    compute_statistical_summary()

    _step(n + 4, "Sensitivity plot (curves + stat heatmaps)...")
    run("data/plot_sensitivity.py")

    _step(n + 5, f"Multi-seed analysis (seeds 42-46 x {n} morphologies)...")
    multi_seed_results = multi_seed_step()

    print("\n      Writing exploration_summary.json...")
    write_exploration_summary(resonance_data, derivation_data, multi_seed_results)

    from data.parametric_sweep import run_parametric_sweep, K0_GRID, BETA_GRID, Q_GRID
    _step(n + 6, f"Parametric robustness sweep (k0 x beta x Q — {len(K0_GRID) * len(BETA_GRID) * len(Q_GRID)} grid points)...")
    run_parametric_sweep()

    print("\n===================================================")
    print(" BENCHMARK COMPLETE - v1.2.2")
    print("===================================================")

    out_dir = ensure_output_dir()
    artifacts = sorted(
        p for p in out_dir.iterdir() if p.is_file() and p.name != ".gitkeep"
    )
    print("\n  Artifacts written to outputs/:")
    for p in artifacts:
        print(f"    - {p.name}")
    print("  (sensitivity_analysis.png is also copied to data/)")


if __name__ == "__main__":
    main()