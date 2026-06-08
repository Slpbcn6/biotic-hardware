"""
Multi-seed sensitivity analysis — v1.2

Runs each morphology across N seeds to produce mean +/- std distributions
instead of single-point results. Transforms point estimates into statistically
robust distributions enabling falsifiable comparison across morphologies.
"""

import numpy as np
import csv
from pathlib import Path

import data.node_coupling as coupling

SEEDS = [42, 43, 44, 45, 46]
MODES = ["fractal", "botanical", "random"]
METRICS = ["Merit_Scaled", "Coherence_Ratio", "Peak_AF"]


def run_multi_seed(output_file="data/multi_seed_summary.csv"):
    """
    Runs each morphology with each seed in SEEDS.
    Computes mean +/- std per metric across seeds.
    Writes results to output_file.
    Returns results dict.
    """
    results = {}

    for mode in MODES:
        mode_data = {m: [] for m in METRICS}

        for seed in SEEDS:
            tmp_csv = f"data/_tmp_{mode}_{seed}.csv"
            tmp_npz = f"data/_tmp_{mode}_{seed}.npz"

            coupling.run_sweep(mode, tmp_csv, tmp_npz, seed_override=seed)

            with open(tmp_csv) as f:
                rows = list(csv.DictReader(f))

            for metric in METRICS:
                values = [float(r[metric]) for r in rows]
                mode_data[metric].append(float(np.mean(values)))

            Path(tmp_csv).unlink(missing_ok=True)
            Path(tmp_npz).unlink(missing_ok=True)

        results[mode] = {
            m: {
                "mean": float(np.mean(mode_data[m])),
                "std": float(np.std(mode_data[m])),
            }
            for m in METRICS
        }

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Morphology", "Seeds",
            "Merit_Mean", "Merit_Std",
            "Coherence_Mean", "Coherence_Std",
            "PeakAF_Mean", "PeakAF_Std",
        ])
        for mode, r in results.items():
            writer.writerow([
                mode,
                str(SEEDS),
                round(r["Merit_Scaled"]["mean"], 6),
                round(r["Merit_Scaled"]["std"], 6),
                round(r["Coherence_Ratio"]["mean"], 6),
                round(r["Coherence_Ratio"]["std"], 6),
                round(r["Peak_AF"]["mean"], 6),
                round(r["Peak_AF"]["std"], 6),
            ])

    return results