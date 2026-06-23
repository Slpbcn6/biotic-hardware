import sys
import csv
import os
import textwrap
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.patches import Rectangle

from data.config import morphologies, load_parameters, ensure_output_dir, output_path, data_path, rel
from data.stats_utils import pearson_r


MORPHOLOGY_MODES = morphologies()
PIPELINE_VERSION = load_parameters()["VIII_pipeline"]["version"]
CORRELATION_THRESHOLD = float(
    load_parameters().get("IX_topology_parameters", {}).get("correlation_threshold", 0.632)
)

NAMED_COLORS = {
    "fractal":    "#2196F3",
    "botanical":  "#4CAF50",
    "random":     "#FF5722",
    "fibonacci":  "#9C27B0",
    "voronoi":    "#FF9800",
    "hexagonal":  "#00BCD4",
    "dla":        "#795548",
    "clusters":   "#E91E63",
    "concentric": "#607D8B",
    "reticulate": "#8BC34A",
}

_FALLBACK = matplotlib.colormaps["tab10"]

plt.rcParams.update({
    "font.family":      "sans-serif",
    "font.sans-serif":  ["DejaVu Sans", "Arial", "Helvetica"],
    "axes.titleweight": "bold",
    "axes.edgecolor":   "#bbbbbb",
    "axes.linewidth":   1.0,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})


def color_for(mode, i):
    return NAMED_COLORS.get(mode, _FALLBACK(i % 10))


METRICS = ["Merit_Scaled", "Coherence_Ratio", "Peak_AF"]
METRIC_LABELS = ["Merit Scaled", "Coherence Ratio", "Peak AF"]

TOPOLOGY_FOCUS_HYP = "H2"
TOPOLOGY_PRIMARY_K = 6
TOPOLOGY_FAVORABLE_K = 3

PAIRS = [
    f"{a.capitalize()} vs {b.capitalize()}"
    for a, b in combinations(MORPHOLOGY_MODES, 2)
]


def load_mode_data(filepath):
    d, p, c, m, q, ms = [], [], [], [], [], []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            d.append(float(r["Distance"]))
            p.append(float(r["Peak_AF"]))
            c.append(float(r["Coherence_Ratio"]))
            m.append(float(r["Merit_Function"]))
            q.append(float(r["Q_effective"]))
            ms.append(float(r["Merit_Scaled"]))
    return (
        np.array(d), np.array(p), np.array(c),
        np.array(m), np.array(q), np.array(ms),
    )


def load_multi_seed_summary(filepath):
    summary = {}
    if not os.path.exists(filepath):
        return summary
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mode = row["Morphology"]
            summary[mode] = {
                "Merit_Scaled":    (float(row["Merit_Mean"]),     float(row["Merit_Std"])),
                "Coherence_Ratio": (float(row["Coherence_Mean"]), float(row["Coherence_Std"])),
                "Peak_AF":         (float(row["PeakAF_Mean"]),    float(row["PeakAF_Std"])),
            }
    return summary


def load_multi_seed_raw(filepath):
    raw = {mode: {"Merit_Scaled": [], "Coherence_Ratio": [], "Peak_AF": []}
           for mode in MORPHOLOGY_MODES}
    if not os.path.exists(filepath):
        return raw
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mode = row["Morphology"]
            if mode in raw:
                raw[mode]["Merit_Scaled"].append(float(row["Merit_Scaled"]))
                raw[mode]["Coherence_Ratio"].append(float(row["Coherence_Ratio"]))
                raw[mode]["Peak_AF"].append(float(row["Peak_AF"]))
    return raw


def load_inference_summary(filepath):
    d_matrix   = np.full((len(METRICS), len(PAIRS)), np.nan)
    sig_matrix = [["" for _ in PAIRS] for _ in METRICS]
    if not os.path.exists(filepath):
        return d_matrix, sig_matrix
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            metric = row["Metric"]
            pair   = row["Pair"]
            if metric not in METRICS or pair not in PAIRS:
                continue
            i = METRICS.index(metric)
            j = PAIRS.index(pair)
            d_val = row["Cohens_d"]
            d_matrix[i, j] = abs(float(d_val)) if d_val not in ("n/a", "") else np.nan
            sig_matrix[i][j] = row.get("Significant_holm", "")
    return d_matrix, sig_matrix


def load_topology_points(filepath, k):
    points = []
    if not os.path.exists(filepath):
        return points
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if int(float(row["k"])) != k:
                    continue
                x = float(row["lambda_2_mean"])
                y = float(row["Merit_Mean"])
                name = row["Morphology"]
            except (ValueError, KeyError, TypeError):
                continue
            if np.isfinite(x) and np.isfinite(y):
                points.append((name, x, y))
    return points


def load_topology_stat(filepath, hypothesis, k):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if row.get("Hypothesis") != hypothesis or int(float(row["k"])) != k:
                    continue
                return {
                    "r":      float(row["r"]),
                    "p":      float(row["p"]),
                    "n":      int(float(row["N"])),
                    "passes": row.get("passes_threshold", "no"),
                }
            except (ValueError, KeyError, TypeError):
                continue
    return None


def load_robustness_fraction(filepath):
    total = 0
    held = 0
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if str(row.get("finding_holds", "")).strip().lower() == "true":
                held += 1
    if total == 0:
        return None
    return held, total


def load_phase_agreement(filepath):
    rows = 0
    absent = 0
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Metric") not in ("Merit_Scaled", "Peak_AF"):
                continue
            rows += 1
            if str(row.get("signature_absent_both", "")).strip().lower() == "true":
                absent += 1
    if rows == 0:
        return None
    return absent, rows


def load_coherence_observation(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get("Metric") == "Coherence_Ratio"
                    and row.get("Pair") == "Botanical vs Voronoi"):
                if (row.get("verdict_sector") == "below"
                        and row.get("verdict_continuous") == "below"):
                    return float(row["Cohens_d_sector"]), float(row["Cohens_d_continuous"])
                return None
    return None


def _curve_values(data_tuple, metric_key):
    if metric_key == "Merit_Scaled":
        return data_tuple[5]
    if metric_key == "Coherence_Ratio":
        return data_tuple[2]
    return data_tuple[1]


def plot_curve_panel(ax, mode_data, seed_summary, metric_key, metric_label, show_legend):
    for i, (mode, data_tuple) in enumerate(mode_data.items()):
        dist   = data_tuple[0]
        values = _curve_values(data_tuple, metric_key)
        color  = color_for(mode, i)

        ax.plot(dist, values, color=color, linewidth=2.4,
                label=mode.capitalize(), zorder=3)

        if mode in seed_summary and metric_key in seed_summary[mode]:
            _, std_val = seed_summary[mode][metric_key]
            lo = np.maximum(values - std_val, 0.0)
            hi = values + std_val
            ax.fill_between(dist, lo, hi, color=color, alpha=0.13, zorder=1)

    ax.set_xlabel("Distance (m)", fontsize=14)
    ax.set_ylabel(metric_label, fontsize=14)
    ax.set_title(metric_label, fontsize=17)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.22, linestyle="--")
    ax.tick_params(labelsize=12)
    if show_legend:
        ax.legend(fontsize=12, framealpha=0.88, loc="upper left")


def plot_boxplots(ax, raw_data):
    data_by_mode = [raw_data[m]["Merit_Scaled"] for m in MORPHOLOGY_MODES]
    labels = [m.capitalize() for m in MORPHOLOGY_MODES]
    colors = [color_for(m, i) for i, m in enumerate(MORPHOLOGY_MODES)]

    bp = ax.boxplot(
        data_by_mode,
        patch_artist=True,
        notch=False,
        showfliers=False,
        medianprops=dict(color="black", linewidth=2.2),
        boxprops=dict(linewidth=1.4),
        whiskerprops=dict(color="#666666", linewidth=1.1),
        capprops=dict(color="#666666", linewidth=1.1),
    )
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.55)

    jitter_rng = np.random.default_rng(42)
    for position, (values, color) in enumerate(zip(data_by_mode, colors), start=1):
        points = np.asarray(values, dtype=float)
        offsets = jitter_rng.uniform(-0.16, 0.16, size=points.shape[0])
        ax.scatter(
            np.full_like(points, position) + offsets,
            points,
            s=22,
            color=color,
            edgecolor="white",
            linewidth=0.5,
            alpha=0.85,
            zorder=3,
        )

    n_seeds = max((len(raw_data[m]["Merit_Scaled"]) for m in MORPHOLOGY_MODES), default=0)
    ax.set_xticklabels(labels, fontsize=11, rotation=35, ha="right")
    ax.set_ylabel("Merit Scaled", fontsize=14)
    ax.set_title(
        f"Merit Scaled — seed distribution\n(N={n_seeds} independent seeds per morphology)",
        fontsize=14,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", alpha=0.22, linestyle="--")
    ax.tick_params(labelsize=12)


def plot_inference_matrices(fig, spec, d_matrix, sig_matrix):
    n      = len(MORPHOLOGY_MODES)
    names  = [m.capitalize() for m in MORPHOLOGY_MODES]
    combos = list(combinations(range(n), 2))

    cubes, flags = [], []
    for mi in range(len(METRICS)):
        mat = np.full((n, n), np.nan)
        sg  = np.zeros((n, n), dtype=bool)
        for k, (ia, ib) in enumerate(combos):
            mat[ib, ia] = d_matrix[mi, k]
            sg[ib, ia]  = sig_matrix[mi][k] == "yes"
        cubes.append(mat)
        flags.append(sg)

    finite = [c[np.isfinite(c)] for c in cubes]
    finite = np.concatenate(finite) if any(v.size for v in finite) else np.array([1.0])
    d_cap  = min(float(np.nanmax(finite)), 5.0)

    cmap = matplotlib.colormaps["YlOrRd"].with_extremes(bad="white")

    inner = spec.subgridspec(3, 3, height_ratios=[0.10, 1.0, 0.06],
                             hspace=0.04, wspace=0.04)

    ax_head = fig.add_subplot(inner[0, :])
    ax_head.axis("off")
    ax_head.text(
        0.5, 0.4,
        "Pairwise effect size  ·  |Cohen's d|  ·  lower triangle per metric",
        ha="center", va="center", fontsize=18, fontweight="bold",
    )

    im = None
    for j in range(len(METRICS)):
        ax  = fig.add_subplot(inner[1, j])
        mat = cubes[j]
        sg  = flags[j]
        masked = np.ma.masked_invalid(mat)
        im = ax.imshow(masked, cmap=cmap, vmin=0, vmax=d_cap, aspect="auto")

        ax.set_title(METRIC_LABELS[j], fontsize=15, fontweight="bold", pad=10)
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels(names, fontsize=9.5, rotation=45, ha="right")
        ax.set_yticklabels(names if j == 0 else [], fontsize=9.5)
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
        ax.grid(which="minor", color="white", linewidth=2)

        for ia, ib in combos:
            val  = mat[ib, ia]
            star = "*" if sg[ib, ia] else ""
            if np.isnan(val):
                ax.add_patch(Rectangle((ia - 0.5, ib - 0.5), 1, 1,
                                       facecolor="#eeeeee", edgecolor="white",
                                       linewidth=2, zorder=2))
                ax.text(ia, ib, "–", ha="center", va="center",
                        fontsize=9, color="#bbbbbb", zorder=3)
            else:
                col = "white" if val > d_cap * 0.6 else "#222222"
                ax.text(ia, ib, f"{val:.2f}{star}", ha="center", va="center",
                        fontsize=8, color=col, fontweight="bold", zorder=3)

    cax = fig.add_subplot(inner[2, :])
    cb  = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_label(
        "|Cohen's d|     ( * = significant after Holm–Bonferroni   ·   – = n/a, seed-frozen pair )",
        fontsize=12,
    )
    cb.ax.tick_params(labelsize=11)
    for threshold, lbl in [(0.2, "small"), (0.5, "medium"), (0.8, "large")]:
        if threshold <= d_cap:
            cb.ax.axvline(threshold, color="black", linewidth=0.9,
                          linestyle="--", alpha=0.5)
            cb.ax.text(threshold / d_cap, 1.6, lbl, transform=cb.ax.transAxes,
                       ha="center", va="bottom", fontsize=10, color="#555555")


def plot_topology_scatter(ax, points, stat, k, role_label):
    if not points:
        ax.axis("off")
        ax.text(0.5, 0.5, "topology data unavailable",
                ha="center", va="center", fontsize=12, color="#888888")
        return

    plotted  = {p[0] for p in points}
    excluded = [m for m in MORPHOLOGY_MODES if m not in plotted]

    xs = np.array([p[1] for p in points])
    ys = np.array([p[2] for p in points])

    if len(xs) >= 2:
        slope, intercept = np.polyfit(xs, ys, 1)
        xline = np.linspace(xs.min(), xs.max(), 100)
        ax.plot(xline, slope * xline + intercept, linestyle="--",
                color="#888888", linewidth=1.6, zorder=2)

    for name, x, y in points:
        ax.scatter(x, y, s=150, color=NAMED_COLORS.get(name, "#888888"),
                   edgecolor="white", linewidth=1.4, zorder=3)
    ax.margins(x=0.10, y=0.12)

    ax.set_xlabel(r"Algebraic connectivity  $\lambda_2$", fontsize=14)
    ax.set_ylabel("Merit Scaled (mean)", fontsize=14)
    ax.set_title(f"Topology vs merit  ·  {role_label}  (k={k})",
                 fontsize=13.5, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.22, linestyle="--")
    ax.tick_params(labelsize=12)

    if len(xs) >= 3:
        r, p = pearson_r(xs, ys)
        n = len(xs)
        passes = abs(r) >= CORRELATION_THRESHOLD and p < 0.05
        if passes:
            verdict = "significant"
        elif abs(r) >= CORRELATION_THRESHOLD:
            verdict = "exceeds |r| threshold but not significant"
        else:
            verdict = "not significant"
        if stat is not None and (abs(stat["r"] - r) > 0.01 or stat["n"] != n):
            print("[plot_sensitivity] WARNING: topology_correlation.csv "
                  f"(r={stat['r']:.3f}, N={stat['n']}) diverges from the plotted "
                  f"points (r={r:.3f}, N={n}); showing values recomputed from the "
                  "plotted points.")
        txt = (f"Pearson r = {r:.2f}    p = {p:.3f}    (N = {n})\n"
               f"{verdict}\n"
               f"threshold |r| ≥ {CORRELATION_THRESHOLD:.3f} and p < 0.05")
        if excluded:
            names = ", ".join(m.capitalize() for m in excluded)
            txt += f"\n{names} excluded: graph disconnected at k={k}"
        ax.text(0.97, 0.97, txt, transform=ax.transAxes, ha="right", va="top",
                fontsize=8.5, color="#222222", linespacing=1.4,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#f5f5f5",
                          edgecolor="#cccccc"))


def place_matched_legend(fig, ref_ax, legend_ax, handles, labels):
    fig.canvas.draw()
    fig.set_layout_engine("none")
    renderer = fig.canvas.get_renderer()
    ref = ref_ax.get_position()
    anchor = legend_ax.get_position()
    target_h = ref.height
    top_y = ref.y1
    x0 = anchor.x0

    def draw_legend(label_spacing):
        leg = fig.legend(
            handles, labels, loc="upper left",
            bbox_to_anchor=(x0, top_y), bbox_transform=fig.transFigure,
            ncol=1, fontsize=12, frameon=True, framealpha=0.9,
            handlelength=1.6, handletextpad=0.6, labelspacing=label_spacing,
            borderpad=0.9, title="Morphologies", title_fontsize=13,
        )
        fig.canvas.draw()
        height = leg.get_window_extent(renderer).height / fig.bbox.height
        return leg, height

    leg_low, h_low = draw_legend(0.4)
    leg_low.remove()
    leg_high, h_high = draw_legend(2.8)
    leg_high.remove()
    if abs(h_high - h_low) < 1e-9:
        label_spacing = 0.9
    else:
        label_spacing = 0.4 + (target_h - h_low) * (2.8 - 0.4) / (h_high - h_low)
    label_spacing = max(0.2, min(label_spacing, 6.0))
    draw_legend(label_spacing)


def plot():
    mode_data = {}
    for mode in MORPHOLOGY_MODES:
        path = output_path(f"simulation_results_{mode}.csv")
        if not os.path.exists(path):
            print(f"[plot_sensitivity] Missing: {rel(path)} — skipping.")
            continue
        mode_data[mode] = load_mode_data(path)

    if len(mode_data) < 2:
        print("[plot_sensitivity] Need at least 2 morphologies — aborting.")
        return

    seed_summary = load_multi_seed_summary(output_path("multi_seed_summary.csv"))
    raw_data     = load_multi_seed_raw(output_path("multi_seed_raw.csv"))
    d_matrix, sig_matrix = load_inference_summary(output_path("inference_summary.csv"))
    topo_summary_path = output_path("graph_topology_summary.csv")
    topo_corr_path    = output_path("topology_correlation.csv")
    topo_points_primary = load_topology_points(topo_summary_path, TOPOLOGY_PRIMARY_K)
    topo_points_fav     = load_topology_points(topo_summary_path, TOPOLOGY_FAVORABLE_K)
    topo_stat_primary   = load_topology_stat(topo_corr_path, TOPOLOGY_FOCUS_HYP, TOPOLOGY_PRIMARY_K)
    topo_stat_fav       = load_topology_stat(topo_corr_path, TOPOLOGY_FOCUS_HYP, TOPOLOGY_FAVORABLE_K)
    robustness_fraction = load_robustness_fraction(output_path("robustness_matrix.csv"))
    phase_agreement     = load_phase_agreement(output_path("phase_robustness.csv"))
    coherence_obs       = load_coherence_observation(output_path("phase_robustness.csv"))
    has_inference = not np.all(np.isnan(d_matrix))
    has_raw       = any(len(raw_data[m]["Merit_Scaled"]) > 0 for m in MORPHOLOGY_MODES)

    full = has_inference and has_raw

    if full:
        fig = plt.figure(figsize=(16, 21.0), layout="constrained")
        outer = fig.add_gridspec(4, 1, height_ratios=[5.5, 3.0, 3.6, 6.8])
    else:
        fig = plt.figure(figsize=(16, 5.0), layout="constrained")
        outer = fig.add_gridspec(1, 1, height_ratios=[4.2])
    fig.get_layout_engine().set(h_pad=0.09, w_pad=0.03, hspace=0.07, wspace=0.06)

    gs_curves = outer[0].subgridspec(1, 4, width_ratios=[0.5, 1, 1, 1], wspace=0.14)
    ax_legend    = fig.add_subplot(gs_curves[0, 0])
    ax_legend.axis("off")
    ax_merit     = fig.add_subplot(gs_curves[0, 1])
    ax_coherence = fig.add_subplot(gs_curves[0, 2])
    ax_peak      = fig.add_subplot(gs_curves[0, 3])
    for ax, key, label in [
        (ax_merit,     "Merit_Scaled",    "Merit Scaled"),
        (ax_coherence, "Coherence_Ratio", "Coherence Ratio"),
        (ax_peak,      "Peak_AF",         "Peak AF"),
    ]:
        plot_curve_panel(ax, mode_data, seed_summary, key, label, False)

    legend_handles, legend_labels = ax_merit.get_legend_handles_labels()

    if full:
        ax_box = fig.add_subplot(outer[1])
        plot_boxplots(ax_box, raw_data)

        gs_topo = outer[2].subgridspec(1, 2, wspace=0.16)
        ax_topo_primary = fig.add_subplot(gs_topo[0, 0])
        plot_topology_scatter(ax_topo_primary, topo_points_primary, topo_stat_primary,
                              TOPOLOGY_PRIMARY_K, "primary resolution")
        ax_topo_fav = fig.add_subplot(gs_topo[0, 1])
        plot_topology_scatter(ax_topo_fav, topo_points_fav, topo_stat_fav,
                              TOPOLOGY_FAVORABLE_K, "robustness check")

        plot_inference_matrices(fig, outer[3], d_matrix, sig_matrix)

    footer_parts = [
        "Single representative run (seed 42); shaded bands ±1 SD of per-seed means across "
        "N=30 seeds · Welch t-test with Holm-Bonferroni pooled across all valid pairs (single family) · "
        "spatial-sector phase assignment (primary rule)."
    ]
    if robustness_fraction is not None:
        held, total = robustness_fraction
        pct = 100.0 * held / total
        footer_parts.append(
            f"The v1.3 separation holds in only {held}/{total} ({pct:.0f}%) of grid×seed cells."
        )
    if phase_agreement is not None:
        absent, rows = phase_agreement
        footer_parts.append(
            f"Spatial-sector and continuous phase rules agree the original signature is absent "
            f"in {absent}/{rows} botanical-vs-control comparisons."
        )
    if coherence_obs is not None:
        d_sec, d_cont = coherence_obs
        footer_parts.append(
            f"On the coherence ratio (secondary metric) botanical sits below Voronoi under "
            f"both rules (d = {d_sec:.2f} / {d_cont:.2f})."
        )

    footer = textwrap.fill(" ".join(footer_parts), width=165)
    fig.supxlabel(footer, fontsize=12, color="#666666")

    fig.suptitle(
        f"Biotic Hardware Synthesis  ·  Morphological Benchmark  ·  v{PIPELINE_VERSION}\n"
        "Methodological correction — the v1.3 botanical signature\n"
        "does not survive a centroid-referenced phase assignment",
        fontsize=21, fontweight="bold",
    )

    place_matched_legend(fig, ax_merit, ax_legend, legend_handles, legend_labels)

    ensure_output_dir()
    out_png  = output_path("sensitivity_analysis.png")
    data_png = data_path("sensitivity_analysis.png")
    plt.savefig(out_png,  dpi=150, bbox_inches="tight")
    plt.savefig(data_png, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[plot_sensitivity] Plot saved: {rel(out_png)}")
    print(f"[plot_sensitivity] Plot also saved: {rel(data_png)}")


if __name__ == "__main__":
    plot()