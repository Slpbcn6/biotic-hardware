import csv
import numpy as np

from data.config import load_parameters, output_path, rel
from data.graph_topology import compute_topology
from data.input_generator import load_morphology
from data.stats_utils import pearson_r, loocv_pearson


def _read_merit_by_mode(raw_file):
    merit = {}
    seeds = {}
    with open(raw_file) as f:
        for row in csv.DictReader(f):
            mode = row["Morphology"]
            merit.setdefault(mode, []).append(float(row["Merit_Scaled"]))
            seeds.setdefault(mode, []).append(int(row["Seed"]))
    merit_mean = {mode: float(np.mean(vals)) for mode, vals in merit.items()}
    return merit_mean, seeds


def _nanmean(values):
    arr = np.array(values, dtype=float)
    return float(np.nanmean(arr)) if np.any(np.isfinite(arr)) else float("nan")


def _nanstd(values):
    arr = np.array(values, dtype=float)
    return float(np.nanstd(arr, ddof=1)) if np.sum(np.isfinite(arr)) > 1 else float("nan")


def _summarise(records, n_seeds):
    return {
        "n_seeds": n_seeds,
        "lambda_2_mean": _nanmean([r["lambda_2"] for r in records]),
        "lambda_2_std": _nanstd([r["lambda_2"] for r in records]),
        "lambda_max_mean": _nanmean([r["lambda_max"] for r in records]),
        "eigenratio_mean": _nanmean([r["eigenratio"] for r in records]),
        "eigenratio_std": _nanstd([r["eigenratio"] for r in records]),
        "clustering_mean": _nanmean([r["clustering_coefficient"] for r in records]),
        "clustering_std": _nanstd([r["clustering_coefficient"] for r in records]),
        "mean_degree": _nanmean([r["mean_degree"] for r in records]),
        "density": _nanmean([r["density"] for r in records]),
        "char_path_length": _nanmean([r["char_path_length"] for r in records]),
    }


def _topology_by_k(mode, seeds, k_values, n_nodes):
    per_k = {k: [] for k in k_values}
    for seed in seeds:
        nodes = load_morphology(mode=mode, n_nodes=n_nodes, seed=seed)
        for k in k_values:
            per_k[k].append(compute_topology(nodes, k))
    return {k: _summarise(per_k[k], len(seeds)) for k in k_values}


def run_topology_analysis(raw_file=None, summary_file=None, correlation_file=None):
    """Run the graph-topology analysis step of the pipeline.

    For every morphology the union k-NN graph is built at the primary neighbour
    count and at each robustness neighbour count from parameters.json, and the
    Laplacian spectral descriptors, clustering coefficient and basic graph
    statistics are averaged over the same seeds used by the multi-seed sweep.
    The per-morphology means are written to the topology summary. The analysis
    then correlates three topology metrics against scaled merit across the ten
    morphologies (N=10): H1 eigenratio R, H2 algebraic connectivity lambda_2 and
    H3 the clustering coefficient. Each correlation is reported with its Pearson
    r, two-tailed p-value, leave-one-out stability and a pass flag against the
    critical |r| threshold for N=10. Results are exploratory and not
    pre-specified.

    Parameters
    ----------
    raw_file : str or None
        Path to the per-seed multi-seed raw CSV. Defaults to
        outputs/multi_seed_raw.csv.
    summary_file : str or None
        Output path for the per-morphology topology summary CSV. Defaults to
        outputs/graph_topology_summary.csv.
    correlation_file : str or None
        Output path for the topology-vs-merit correlation CSV. Defaults to
        outputs/topology_correlation.csv.

    Returns
    -------
    dict
        Keys: 'summary' (list of per-morphology, per-k records) and
        'correlations' (list of correlation records).
    """
    if raw_file is None:
        raw_file = output_path("multi_seed_raw.csv")
    if summary_file is None:
        summary_file = output_path("graph_topology_summary.csv")
    if correlation_file is None:
        correlation_file = output_path("topology_correlation.csv")

    params = load_parameters()
    modes = list(params["VIII_pipeline"]["morphologies"])
    n_nodes = int(params["VI_experimental_sweep_parameters"]["n_nodes"])
    topo = params["IX_topology_parameters"]
    k_primary = int(topo["k_primary"])
    k_robustness = [int(k) for k in topo["k_robustness"]]
    k_values = [k_primary] + [k for k in k_robustness if k != k_primary]
    threshold = float(topo["correlation_threshold"])

    merit_mean, seeds_by_mode = _read_merit_by_mode(raw_file)

    summary_records = []
    per_k = {k: {} for k in k_values}
    for mode in modes:
        seeds = seeds_by_mode.get(mode, [])
        merit = merit_mean.get(mode, float("nan"))
        stats_by_k = _topology_by_k(mode, seeds, k_values, n_nodes)
        for k in k_values:
            stats = stats_by_k[k]
            record = {"Morphology": mode, "k": k, "Merit_Mean": round(merit, 6)}
            for key, value in stats.items():
                record[key] = round(value, 6) if isinstance(value, float) else value
            summary_records.append(record)
            per_k[k][mode] = {**stats, "merit": merit}

    summary_fields = [
        "Morphology", "k", "n_seeds",
        "lambda_2_mean", "lambda_2_std",
        "lambda_max_mean",
        "eigenratio_mean", "eigenratio_std",
        "clustering_mean", "clustering_std",
        "mean_degree", "density", "char_path_length",
        "Merit_Mean",
    ]
    with open(summary_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary_records)

    hypotheses = [
        ("H1", "eigenratio_R", "eigenratio_mean"),
        ("H2", "algebraic_connectivity_lambda_2", "lambda_2_mean"),
        ("H3", "clustering_coefficient", "clustering_mean"),
    ]

    correlation_records = []
    for k in k_values:
        for label, metric_name, stat_key in hypotheses:
            xs = []
            ys = []
            for mode in modes:
                entry = per_k[k][mode]
                xs.append(entry[stat_key])
                ys.append(entry["merit"])
            xs = np.array(xs, dtype=float)
            ys = np.array(ys, dtype=float)
            mask = np.isfinite(xs) & np.isfinite(ys)
            n_used = int(np.sum(mask))
            r, p = pearson_r(xs[mask], ys[mask])
            loo = loocv_pearson(xs[mask], ys[mask])
            passes = (
                "yes"
                if (not np.isnan(r)) and abs(r) >= threshold and (not np.isnan(p)) and p < 0.05
                else "no"
            )
            correlation_records.append({
                "Hypothesis": label,
                "Metric": metric_name,
                "Target": "Merit_Scaled",
                "k": k,
                "N": n_used,
                "r": round(r, 6) if not np.isnan(r) else "n/a",
                "p": round(p, 6) if not np.isnan(p) else "n/a",
                "threshold_abs_r": threshold,
                "passes_threshold": passes,
                "loocv_mean_r": round(loo["mean"], 6) if not np.isnan(loo["mean"]) else "n/a",
                "loocv_min_r": round(loo["min"], 6) if not np.isnan(loo["min"]) else "n/a",
                "loocv_max_r": round(loo["max"], 6) if not np.isnan(loo["max"]) else "n/a",
                "loocv_sign_stable": "yes" if loo["sign_stable"] else "no",
            })

    correlation_fields = [
        "Hypothesis", "Metric", "Target", "k", "N",
        "r", "p", "threshold_abs_r", "passes_threshold",
        "loocv_mean_r", "loocv_min_r", "loocv_max_r", "loocv_sign_stable",
    ]
    with open(correlation_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=correlation_fields)
        writer.writeheader()
        writer.writerows(correlation_records)

    primary = [c for c in correlation_records if c["k"] == k_primary]
    n_pass = sum(1 for c in primary if c["passes_threshold"] == "yes")
    print(
        f"      Topology correlations at k={k_primary}: {n_pass}/{len(primary)} "
        f"reach |r|>={threshold:.3f} with p<0.05"
    )
    print(f"      Written: {rel(summary_file)}")
    print(f"      Written: {rel(correlation_file)}")

    return {"summary": summary_records, "correlations": correlation_records}
