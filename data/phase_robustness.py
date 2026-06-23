import csv
from pathlib import Path

from data.config import output_path, rel
from data.multi_seed_analysis import run_multi_seed
from data.inference_analysis import run_inference

CONTROLS = ["Random", "Voronoi", "Reticulate", "Dla", "Clusters", "Concentric"]
METRICS = ["Merit_Scaled", "Peak_AF", "Coherence_Ratio"]


def _verdict(d_str, sig_str):
    if d_str == "n/a" or d_str == "":
        return "n/a"
    if sig_str == "yes":
        return "below" if float(d_str) < 0 else "above"
    return "ns"


def _read_summary(path):
    with open(path) as f:
        return {(r["Metric"], r["Pair"]): r for r in csv.DictReader(f)}


def run_phase_robustness(primary_summary=None, output_file=None):
    """Repeat the multi-seed inference under the continuous phase rule and
    compare it pair by pair against the primary sector-phase inference.

    The primary pipeline assigns each node a phase from its angular sector around
    the point-set centroid. This check repeats the entire multi-seed inference
    with the continuous centroid-relative angle instead, an independent
    geometry-driven rule. For every botanical-versus-control pair it
    records whether the v1.3.0 signature (botanical significantly *below* the
    control) is present under each rule, and flags the signature as absent under
    both. Agreement across the two rules is the evidence that the original
    separation was bound to node ordering rather than to geometry.

    Parameters
    ----------
    primary_summary : str or None
        Path to the sector-phase inference_summary.csv. Defaults to the file
        written by the main inference step.
    output_file : str or None
        Path for the comparison CSV. Defaults to outputs/phase_robustness.csv.

    Returns
    -------
    list of dict
        One record per (metric, control) comparison.
    """
    if primary_summary is None:
        primary_summary = output_path("inference_summary.csv")
    if output_file is None:
        output_file = output_path("phase_robustness.csv")

    cont_raw = output_path("phase_robustness_raw_continuous.csv")
    cont_summary = output_path("inference_continuous.csv")
    cont_ms_summary = output_path("multi_seed_summary_continuous.csv")

    run_multi_seed(
        output_file=cont_ms_summary,
        raw_output_file=cont_raw,
        phase_rule="continuous",
    )
    run_inference(raw_file=cont_raw, output_file=cont_summary)

    sector_table = _read_summary(primary_summary)
    cont_table = _read_summary(cont_summary)

    fieldnames = [
        "Metric", "Pair",
        "Cohens_d_sector", "p_holm_sector", "verdict_sector",
        "Cohens_d_continuous", "p_holm_continuous", "verdict_continuous",
        "signature_absent_both",
    ]

    records = []
    for metric in METRICS:
        for ctrl in CONTROLS:
            pair = f"Botanical vs {ctrl}"
            s = sector_table.get((metric, pair), {})
            c = cont_table.get((metric, pair), {})
            v_sector = _verdict(s.get("Cohens_d", "n/a"), s.get("Significant_holm", "n/a"))
            v_cont = _verdict(c.get("Cohens_d", "n/a"), c.get("Significant_holm", "n/a"))
            records.append({
                "Metric": metric,
                "Pair": pair,
                "Cohens_d_sector": s.get("Cohens_d", "n/a"),
                "p_holm_sector": s.get("p_holm", "n/a"),
                "verdict_sector": v_sector,
                "Cohens_d_continuous": c.get("Cohens_d", "n/a"),
                "p_holm_continuous": c.get("p_holm", "n/a"),
                "verdict_continuous": v_cont,
                "signature_absent_both": bool(v_sector != "below" and v_cont != "below"),
            })

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    Path(cont_ms_summary).unlink(missing_ok=True)

    v13 = [r for r in records if r["Metric"] in ("Merit_Scaled", "Peak_AF")]
    v13_absent = sum(1 for r in v13 if r["signature_absent_both"])
    coherence_below = [
        r for r in records
        if r["Metric"] == "Coherence_Ratio"
        and r["verdict_sector"] == "below"
        and r["verdict_continuous"] == "below"
    ]
    print(
        f"      Phase robustness — v1.3.0 signature (Merit_Scaled, Peak_AF): "
        f"absent under both phase rules in {v13_absent}/{len(v13)} "
        f"botanical-vs-control comparisons"
    )
    if coherence_below:
        names = ", ".join(r["Pair"].replace("Botanical vs ", "") for r in coherence_below)
        print(
            f"      Phase robustness — Coherence_Ratio (secondary check): botanical "
            f"sits below under both rules vs {names}"
        )
    print(f"      Written: {rel(output_file)}")

    return records


if __name__ == "__main__":
    run_phase_robustness()
