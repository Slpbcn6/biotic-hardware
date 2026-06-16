import csv
import numpy as np
from itertools import combinations
from scipy.stats import ttest_ind

from data.config import load_parameters, output_path, rel
from data.stats_utils import (
    cohens_d,
    holm_correction,
    bootstrap_ci,
    power_from_d,
    near_zero_variance,
)

METRICS = ["Merit_Scaled", "Coherence_Ratio", "Peak_AF"]

VARIANCE_FRACTION = 0.15


def run_inference(raw_file=None, output_file=None):
    if raw_file is None:
        raw_file = output_path("multi_seed_raw.csv")
    if output_file is None:
        output_file = output_path("inference_summary.csv")

    params = load_parameters()
    modes = list(params["VIII_pipeline"]["morphologies"])

    per_seed = {mode: {m: [] for m in METRICS} for mode in modes}

    with open(raw_file) as f:
        for row in csv.DictReader(f):
            mode = row["Morphology"]
            for m in METRICS:
                per_seed[mode][m].append(float(row[m]))

    group_std = {m: {} for m in METRICS}
    reference_std = {}
    degenerate = {m: set() for m in METRICS}
    for metric in METRICS:
        for mode in modes:
            group_std[metric][mode] = float(np.std(per_seed[mode][metric], ddof=1))
        reference_std[metric] = float(np.median(list(group_std[metric].values())))
        for mode in modes:
            if near_zero_variance(
                group_std[metric][mode], reference_std[metric], VARIANCE_FRACTION
            ):
                degenerate[metric].add(mode)

    for metric in METRICS:
        for mode in sorted(degenerate[metric]):
            print(
                f"      WARNING: {mode} has near-zero seed variance for {metric} "
                f"(std={group_std[metric][mode]:.2e} < {VARIANCE_FRACTION:.0%} of "
                f"median {reference_std[metric]:.2e}); multi-seed inference reported as n/a"
            )

    pair_combos = list(combinations(modes, 2))
    records = []
    holm_index = []

    for metric in METRICS:
        for a, b in pair_combos:
            vals_a = per_seed[a][metric]
            vals_b = per_seed[b][metric]
            n = len(vals_a)
            mean_diff = float(np.mean(vals_a)) - float(np.mean(vals_b))
            ci_lower, ci_upper = bootstrap_ci(vals_a, vals_b)

            rec = {
                "Metric": metric,
                "Pair": f"{a.capitalize()} vs {b.capitalize()}",
                "N": n,
                "mean_diff": round(mean_diff, 6),
                "CI_lower": round(ci_lower, 6),
                "CI_upper": round(ci_upper, 6),
                "Cohens_d": "n/a",
                "p_raw": "n/a",
                "p_holm": "n/a",
                "Significant_holm": "n/a",
                "power": "n/a",
            }

            if a in degenerate[metric] or b in degenerate[metric]:
                records.append(rec)
                continue

            _, p_raw = ttest_ind(vals_a, vals_b, equal_var=False)
            d = cohens_d(vals_a, vals_b)
            power = power_from_d(d, n)
            rec["Cohens_d"] = round(d, 4) if not np.isnan(d) else "n/a"
            rec["p_raw"] = round(float(p_raw), 6)
            rec["power"] = round(power, 4) if not np.isnan(power) else "n/a"
            records.append(rec)
            holm_index.append((len(records) - 1, float(p_raw)))

    if holm_index:
        p_holm_list = holm_correction([p for _, p in holm_index])
        for (rec_i, _), ph in zip(holm_index, p_holm_list):
            records[rec_i]["p_holm"] = round(ph, 6)
            records[rec_i]["Significant_holm"] = "yes" if ph < 0.05 else "no"

    fieldnames = [
        "Metric", "Pair", "N", "mean_diff",
        "CI_lower", "CI_upper", "Cohens_d",
        "p_raw", "p_holm", "Significant_holm", "power",
    ]

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    valid_count = len(holm_index)
    sig_count = sum(1 for r in records if r["Significant_holm"] == "yes")
    na_count = sum(1 for r in records if r["Significant_holm"] == "n/a")
    print(
        f"      {sig_count}/{valid_count} valid pairs significant after Holm correction "
        f"({na_count} pairs n/a: near-zero seed variance)"
    )
    print(f"      Written: {rel(output_file)}")

    return records
