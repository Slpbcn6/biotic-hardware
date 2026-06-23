import os
import csv
import numpy as np
from pathlib import Path

import data.node_coupling as coupling
from data.config import load_parameters, ensure_output_dir, output_path

METRICS = ["Merit_Scaled", "Coherence_Ratio", "Peak_AF"]


def run_multi_seed(output_file=None, raw_output_file=None, phase_rule="sector"):
    ensure_output_dir()
    if output_file is None:
        output_file = output_path("multi_seed_summary.csv")
    if raw_output_file is None:
        raw_output_file = output_path("multi_seed_raw.csv")

    params = load_parameters()
    seeds_all = params["VI_experimental_sweep_parameters"]["multi_seed_list"]
    seeds = seeds_all[:2] if os.environ.get("PIPELINE_FAST") == "1" else seeds_all
    modes = list(params["VIII_pipeline"]["morphologies"])

    results = {}
    raw_rows = []

    for mode in modes:
        mode_data = {m: [] for m in METRICS}

        for i, seed in enumerate(seeds):
            print(f"      [{i + 1}/{len(seeds)}] {mode} — seed {seed}")
            tmp_csv = output_path(f"_tmp_{mode}_{seed}.csv")
            tmp_npz = output_path(f"_tmp_{mode}_{seed}.npz")

            coupling.run_sweep(mode, tmp_csv, tmp_npz, seed_override=seed, phase_rule=phase_rule)

            with open(tmp_csv) as f:
                rows = list(csv.DictReader(f))

            seed_row = {"Morphology": mode, "Seed": seed}
            for metric in METRICS:
                values = [float(r[metric]) for r in rows]
                seed_mean = float(np.mean(values))
                mode_data[metric].append(seed_mean)
                seed_row[metric] = seed_mean

            raw_rows.append(seed_row)
            Path(tmp_csv).unlink(missing_ok=True)
            Path(tmp_npz).unlink(missing_ok=True)

        results[mode] = {
            m: {
                "mean": float(np.mean(mode_data[m])),
                "std": float(np.std(mode_data[m], ddof=1)),
                "values": [float(v) for v in mode_data[m]],
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
                str(seeds),
                round(r["Merit_Scaled"]["mean"], 6),
                round(r["Merit_Scaled"]["std"], 6),
                round(r["Coherence_Ratio"]["mean"], 6),
                round(r["Coherence_Ratio"]["std"], 6),
                round(r["Peak_AF"]["mean"], 6),
                round(r["Peak_AF"]["std"], 6),
            ])

    with open(raw_output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Morphology", "Seed"] + METRICS)
        writer.writeheader()
        for row in raw_rows:
            writer.writerow({
                k: (round(v, 8) if isinstance(v, float) else v)
                for k, v in row.items()
            })

    return results
