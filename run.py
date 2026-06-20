import contextlib
import csv
import io
import json
import subprocess
import sys
import threading
import time
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


def _step(n, label, func):
    title = f"[{n}/{TOTAL_STEPS}] {label}"
    print()
    if not sys.__stdout__.isatty():
        print(title)
        return func()

    stop = threading.Event()

    def _animate():
        frames = (" .", " ..", " ...")
        i = 0
        while not stop.is_set():
            sys.__stdout__.write("\r" + title + frames[i % len(frames)] + "   ")
            sys.__stdout__.flush()
            time.sleep(0.4)
            i += 1

    buffer = io.StringIO()
    spinner = threading.Thread(target=_animate, daemon=True)
    spinner.start()
    try:
        with contextlib.redirect_stdout(buffer):
            result = func()
    finally:
        stop.set()
        spinner.join()
        sys.__stdout__.write("\r" + title + "    \n")
        sys.__stdout__.flush()
        captured = buffer.getvalue()
        if captured:
            sys.__stdout__.write(captured)
            sys.__stdout__.flush()
    return result


def run(script):
    print(f"\n[RUN] {script}")
    result = subprocess.run(
        [sys.executable, str(ROOT / script)],
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.returncode != 0:
        if result.stderr:
            print(result.stderr, end="")
        raise subprocess.CalledProcessError(result.returncode, script)


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
        output_file = output_path("curve_separation_summary.csv")

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


def inference_step():
    from data.inference_analysis import run_inference
    records = run_inference()
    return records


def topology_step():
    from data.topology_analysis import run_topology_analysis
    results = run_topology_analysis()
    return results


def write_exploration_summary(multi_seed_results, output_file=None):
    if output_file is None:
        output_file = output_path("exploration_summary.json")

    params = load_parameters()
    seeds = params["VI_experimental_sweep_parameters"]["multi_seed_list"]
    pipeline_version = params["VIII_pipeline"]["version"]

    summary = {
        "pipeline_version": pipeline_version,
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
            "seeds": seeds,
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

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"      Written: {rel(output_file)}")


def main():
    params = load_parameters()
    seeds = params["VI_experimental_sweep_parameters"]["multi_seed_list"]
    pipeline_version = params["VIII_pipeline"]["version"]
    n = len(MORPHOLOGY_MODES)
    total_pairs = n * (n - 1) // 2

    ensure_output_dir()

    print("\n===================================================")
    print(f" DETERMINISTIC COMPARATIVE MORPHOLOGICAL PIPELINE v{pipeline_version}")
    print(f" {n} morphologies | {total_pairs} pairs | N={len(seeds)} seeds ({seeds[0]}–{seeds[-1]})")
    print("===================================================")

    for idx, mode in enumerate(MORPHOLOGY_MODES, start=1):
        _step(idx, f"{mode.upper()} sweep", lambda mode=mode: run_coupling(mode))

    _step(n + 1, f"Curve separation descriptors (Welch t + Cohen d, 3 metrics x {total_pairs} pairs)", compute_statistical_summary)

    multi_seed_results = _step(n + 2, f"Multi-seed analysis (N={len(seeds)} seeds x {n} morphologies)", multi_seed_step)

    print("\n      Writing exploration_summary.json...")
    write_exploration_summary(multi_seed_results)

    _step(n + 3, "Inference analysis (Welch + Holm-Bonferroni + bootstrap CI 95% + power)", inference_step)

    _step(n + 4, "Graph-topology analysis (union k-NN spectra + clustering vs merit, N=10)", topology_step)

    _step(n + 5, "Sensitivity plot (curves + stat heatmaps)", lambda: run("data/plot_sensitivity.py"))

    from data.parametric_sweep import run_parametric_sweep, effective_grids
    k0_grid, beta_grid, q_grid = effective_grids()
    _step(n + 6, f"Parametric robustness sweep ({len(k0_grid)} x {len(beta_grid)} x {len(q_grid)} = {len(k0_grid) * len(beta_grid) * len(q_grid)} grid points)", run_parametric_sweep)

    out_dir = ensure_output_dir()
    artifacts = sorted(
        p for p in out_dir.iterdir() if p.is_file() and p.name != ".gitkeep"
    )
    print("\n  Artifacts written to outputs/:")
    for p in artifacts:
        print(f"    - {p.name}")
    print("    (sensitivity_analysis.png is also copied to data/)")

    print("\n===================================================")
    print(f" BENCHMARK COMPLETE - v{pipeline_version}")
    print(f" {len(artifacts)} artifacts in outputs/ | all steps OK")
    print("===================================================")


if __name__ == "__main__":
    main()