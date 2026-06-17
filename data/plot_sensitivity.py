import sys
import csv
import os
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

from data.config import morphologies, ensure_output_dir, output_path, data_path, rel


MORPHOLOGY_MODES = morphologies()

NAMED_COLORS = {
    "fractal":   "#2196F3",
    "botanical": "#4CAF50",
    "random":    "#FF5722",
    "fibonacci": "#9C27B0",
    "voronoi":   "#FF9800",
}

_FALLBACK = matplotlib.colormaps["tab10"]

plt.rcParams.update({
    "font.family":     "monospace",
    "font.monospace":  ["Courier New", "Courier", "DejaVu Sans Mono"],
    "axes.titleweight": "bold",
})


def color_for(mode, i):
    return NAMED_COLORS.get(mode, _FALLBACK(i % 10))


METRICS = ["Merit_Scaled", "Coherence_Ratio", "Peak_AF"]
METRIC_LABELS = ["Merit Scaled", "Coherence Ratio", "Peak AF"]

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
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_ylabel("Merit Scaled", fontsize=14)
    ax.set_title(
        f"Merit Scaled — seed distribution\n(N={n_seeds} independent seeds per morphology)",
        fontsize=14,
    )
    ax.grid(True, axis="y", alpha=0.22, linestyle="--")
    ax.tick_params(labelsize=12)


def plot_inference_heatmap(ax, d_matrix, sig_matrix):
    short_pairs = [
        f"{a[:3]}/{b[:3]}"
        for a, b in combinations(MORPHOLOGY_MODES, 2)
    ]
    short_metrics = ["Merit\nScaled", "Coherence\nRatio", "Peak\nAF"]

    d_cap     = min(float(np.nanmax(d_matrix)) if not np.all(np.isnan(d_matrix)) else 3.0, 5.0)
    d_display = np.where(np.isnan(d_matrix), 0.0, d_matrix)

    im = ax.imshow(d_display, cmap="YlOrRd", vmin=0, vmax=d_cap, aspect="auto")

    ax.set_xticks(range(len(PAIRS)))
    ax.set_xticklabels(short_pairs, fontsize=12, rotation=45, ha="right")
    ax.set_yticks(range(len(METRICS)))
    ax.set_yticklabels(short_metrics, fontsize=13)
    ax.set_title(
        "Statistical inference — |Cohen's d|   (* = significant after Holm-Bonferroni)\n"
        "Welch t-test on N=30 per-seed means · 30 simultaneous tests corrected",
        fontsize=14,
    )

    for i in range(len(METRICS)):
        for j in range(len(PAIRS)):
            val = d_matrix[i, j]
            sig = " *" if sig_matrix[i][j] == "yes" else ""
            if np.isnan(val):
                label, txt_color = "n/a", "#888888"
            else:
                label     = f"{val:.2f}{sig}"
                txt_color = "white" if val > d_cap * 0.62 else "black"
            ax.text(j, i, label, ha="center", va="center",
                    fontsize=14, color=txt_color, fontweight="bold")

    cbar = plt.colorbar(im, ax=ax, fraction=0.030, pad=0.04)
    cbar.set_label("|Cohen's d|", fontsize=13)
    cbar.ax.yaxis.set_ticks_position("left")
    cbar.ax.yaxis.set_label_position("left")
    cbar.ax.tick_params(labelsize=11)
    for threshold, lbl in [(0.2, "small"), (0.5, "medium"), (0.8, "large")]:
        if threshold <= d_cap:
            frac = threshold / d_cap
            cbar.ax.axhline(y=frac, color="black", linewidth=0.9,
                            linestyle="--", alpha=0.55)
            cbar.ax.text(1.3, frac, lbl, va="center", ha="left", fontsize=10,
                         color="#444444", transform=cbar.ax.transAxes)


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
    has_inference = not np.all(np.isnan(d_matrix))
    has_raw       = any(len(raw_data[m]["Merit_Scaled"]) > 0 for m in MORPHOLOGY_MODES)

    fig = plt.figure(figsize=(22, 13))

    if has_inference and has_raw:
        gs = gridspec.GridSpec(
            2, 3, figure=fig,
            height_ratios=[1.0, 1.0],
            hspace=0.46, wspace=0.26,
        )
        ax_merit     = fig.add_subplot(gs[0, 0])
        ax_coherence = fig.add_subplot(gs[0, 1])
        ax_peak      = fig.add_subplot(gs[0, 2])
        ax_box       = fig.add_subplot(gs[1, 0])
        ax_heatmap   = fig.add_subplot(gs[1, 1:])

        for show_leg, (ax, key, label) in zip(
            [True, False, False],
            [
                (ax_merit,     "Merit_Scaled",    "Merit Scaled"),
                (ax_coherence, "Coherence_Ratio", "Coherence Ratio"),
                (ax_peak,      "Peak_AF",         "Peak AF"),
            ],
        ):
            plot_curve_panel(ax, mode_data, seed_summary, key, label, show_leg)

        plot_boxplots(ax_box, raw_data)
        plot_inference_heatmap(ax_heatmap, d_matrix, sig_matrix)

        fig.text(
            0.5, 0.005,
            "Top row: single representative run (seed 42).  "
            "Shaded bands: ±1 SD of per-seed means across N=30 independent seeds.  "
            "Bottom right: Welch t-test corrected for 30 simultaneous comparisons (Holm-Bonferroni).",
            ha="center", fontsize=11, color="#666666", style="italic",
        )
    else:
        gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.26)
        for idx, (key, label) in enumerate([
            ("Merit_Scaled",    "Merit Scaled"),
            ("Coherence_Ratio", "Coherence Ratio"),
            ("Peak_AF",         "Peak AF"),
        ]):
            ax = fig.add_subplot(gs[0, idx])
            plot_curve_panel(ax, mode_data, seed_summary, key, label, idx == 0)

    fig.suptitle(
        "Biotic Hardware Synthesis  ·  Morphological Benchmark  ·  v1.2.6",
        fontsize=24, fontweight="bold", y=1.02,
    )

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