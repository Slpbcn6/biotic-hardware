import subprocess
import sys
import csv
import json
from math import lgamma, exp
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent


def run(script):
    print(f"\n[RUN] {script}")
    subprocess.run([sys.executable, str(ROOT / script)], check=True)


def run_coupling(mode, output_file, tensor_file):
    import data.node_coupling as coupling
    from data.topology_validator import validate_topology
    from data import input_generator

    with open("data/parameters.json") as f:
        params = json.load(f)
    cfg = params["VI_experimental_sweep_parameters"]
    n_nodes = int(cfg["n_nodes"])
    seed = int(cfg["seed"])

    generators = {
        "fractal":   input_generator.generate_fractal_morphology,
        "botanical": input_generator.generate_botanical_graph,
        "random":    input_generator.generate_random_control,
    }
    nodes = generators[mode](n_nodes=n_nodes, seed=seed)

    valid, report = validate_topology(nodes)
    print(f"      Topology: {report[0]}")
    if not valid:
        raise RuntimeError(f"Topology validation failed for {mode}: {report}")

    coupling.run_sweep(mode, output_file, tensor_file)

    with open(output_file) as f:
        rows = list(csv.DictReader(f))
    last = rows[-1]
    print(
        f"      Peak AF: {float(last['Peak_AF']):.2f} | "
        f"Coherence: {float(last['Coherence_Ratio']):.2f} | "
        f"Merit Scaled: {float(last['Merit_Scaled']):.2f}  "
        f"(d={float(last['Distance']):.1f})"
    )


def _welch_t(a, b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    n1, n2 = len(a), len(b)
    s1, s2 = np.var(a, ddof=1), np.var(b, ddof=1)
    se = np.sqrt(s1 / n1 + s2 / n2 + 1e-14)
    t = (np.mean(a) - np.mean(b)) / se
    df = (s1 / n1 + s2 / n2) ** 2 / (
        (s1 / n1) ** 2 / (n1 - 1) + (s2 / n2) ** 2 / (n2 - 1)
    )
    x = df / (df + t ** 2)

    def beta_inc(a, b, x, steps=800):
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        lbeta = lgamma(a) + lgamma(b) - lgamma(a + b)
        return sum(
            ((i + 0.5) / steps * x) ** (a - 1)
            * (1 - (i + 0.5) / steps * x) ** (b - 1)
            * (x / steps)
            for i in range(steps)
        ) / exp(lbeta)

    p = 2 * beta_inc(df / 2, 0.5, x)
    return float(t), min(float(p), 1.0)


def _cohens_d(a, b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    pooled = np.sqrt(
        (np.std(a, ddof=1) ** 2 + np.std(b, ddof=1) ** 2) / 2 + 1e-14
    )
    return float((np.mean(a) - np.mean(b)) / pooled)


def _col(rows, key):
    return [float(r[key]) for r in rows]


def compute_statistical_summary(output_file="data/statistical_summary.csv"):
    with open("data/simulation_results_fractal.csv") as f:
        df_f = list(csv.DictReader(f))
    with open("data/simulation_results_botanical.csv") as f:
        df_b = list(csv.DictReader(f))
    with open("data/simulation_results_random.csv") as f:
        df_r = list(csv.DictReader(f))

    metrics = ["Merit_Scaled", "Coherence_Ratio", "Peak_AF"]
    pairs = [
        ("Fractal",   df_f, "Botanical", df_b),
        ("Fractal",   df_f, "Random",    df_r),
        ("Botanical", df_b, "Random",    df_r),
    ]

    rows_out = []
    for metric in metrics:
        for n1, d1, n2, d2 in pairs:
            s1, s2 = _col(d1, metric), _col(d2, metric)
            t, p = _welch_t(s1, s2)
            d = _cohens_d(s1, s2)
            sig  = "yes" if p < 0.05 else "no"
            size = "large" if abs(d) > 0.8 else "medium" if abs(d) > 0.5 else "small"
            rows_out.append([
                metric, f"{n1} vs {n2}",
                round(t, 4), round(p, 6),
                sig, round(d, 4), size,
            ])

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Metric", "Pair", "t_statistic", "p_value",
            "Significant_p05", "Cohens_d", "Effect_size",
        ])
        writer.writerows(rows_out)

    print(f"      {'Metric':<18} {'Pair':<28} {'p':>7}  {'d':>7}  {'sig':>4}  effect")
    for row in rows_out:
        print(
            f"      {row[0]:<18} {row[1]:<28} "
            f"{row[3]:>7.4f}  {row[5]:>7.3f}  {row[4]:>4}  {row[6]}"
        )

    return rows_out


def schumann_comparison(f_simulated):
    from data.schumann_reference import schumann_report
    for line in schumann_report(f_simulated):
        print(f"      {line}")


def multi_seed_step():
    from data.multi_seed_analysis import run_multi_seed
    results = run_multi_seed("data/multi_seed_summary.csv")
    for mode, r in results.items():
        m = r["Merit_Scaled"]
        c = r["Coherence_Ratio"]
        print(
            f"      {mode:12s}  "
            f"Merit {m['mean']:.4f} +/- {m['std']:.4f}  |  "
            f"Coherence {c['mean']:.4f} +/- {c['std']:.4f}"
        )
    return results


def write_exploration_summary(resonance_data, multi_seed_results,
                               output_file="data/exploration_summary.json"):
    from data.schumann_reference import nearest_schumann_mode
    from data.multi_seed_analysis import SEEDS

    with open("data/parameters.json") as f:
        params = json.load(f)

    f_sim = resonance_data["f_resonance_Hz"]
    nearest_hz, mode_n, deviation_pct = nearest_schumann_mode(f_sim)

    summary = {
        "pipeline_version": "1.2.0",
        "resonance_baseline": {
            "f_simulated_hz": round(f_sim, 4),
            "Q_factor": round(resonance_data["Q_factor"], 4),
            "schumann_nearest_mode_hz": nearest_hz,
            "schumann_mode_index": mode_n,
            "deviation_pct": deviation_pct,
            "reference": "NOAA/GFZ Potsdam (published reference values)",
        },
        "experimental_configuration": {
            "n_nodes": params["VI_experimental_sweep_parameters"]["n_nodes"],
            "reference_seed": params["VI_experimental_sweep_parameters"]["seed"],
            "beta_loss_factor": params["VI_experimental_sweep_parameters"]["beta_loss_factor"],
            "k0_base": params["VII_array_factor_parameters"]["k0_base"],
            "k_modulation_coeff": params["VII_array_factor_parameters"]["k_modulation_coeff"],
            "q_reference": params["VII_array_factor_parameters"]["q_reference"],
        },
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

    print(f"      Written: {output_file}")


def main():
    print("\n===================================================")
    print(" DETERMINISTIC COMPARATIVE MORPHOLOGICAL PIPELINE v1.2")
    print("===================================================")

    print("\n[1/7] Running node resonance baseline...")
    run("data/node_resonance.py")

    print("\n      Schumann resonance external comparison:")
    with open("data/resonance_params.json") as f:
        resonance_data = json.load(f)
    schumann_comparison(resonance_data["f_resonance_Hz"])

    print("\n[2/7] Running FRACTAL sweep...")
    run_coupling(
        "fractal",
        "data/simulation_results_fractal.csv",
        "data/af_tensors_fractal.npz",
    )

    print("\n[3/7] Running BOTANICAL sweep...")
    run_coupling(
        "botanical",
        "data/simulation_results_botanical.csv",
        "data/af_tensors_botanical.npz",
    )

    print("\n[4/7] Running RANDOM CONTROL sweep...")
    run_coupling(
        "random",
        "data/simulation_results_random.csv",
        "data/af_tensors_random.npz",
    )

    print("\n[5/7] Generating sensitivity plot...")
    run("data/plot_sensitivity.py")

    print("\n[6/7] Statistical separation (Welch t-test + Cohen d, 3 metrics)...")
    compute_statistical_summary()

    print("\n[7/7] Multi-seed analysis (seeds 42-46 x 3 morphologies)...")
    multi_seed_results = multi_seed_step()

    print("\n      Writing exploration_summary.json...")
    write_exploration_summary(resonance_data, multi_seed_results)

    print("\n===================================================")
    print(" BENCHMARK COMPLETE — v1.2")
    print("===================================================")
    print("\n  Outputs:")
    print("    data/simulation_results_*.csv")
    print("    data/af_tensors_*.npz")
    print("    data/sensitivity_analysis.png")
    print("    data/statistical_summary.csv")
    print("    data/multi_seed_summary.csv")
    print("    data/exploration_summary.json")


if __name__ == "__main__":
    main()