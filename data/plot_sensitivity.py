import sys
import csv
import os
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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


def color_for(mode, i):
    return NAMED_COLORS.get(mode, _FALLBACK(i % 10))


METRICS = ["Merit_Scaled", "Coherence_Ratio", "Peak_AF"]
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


def norm(x):
    return (x - x.min()) / (x.max() - x.min() + 1e-12)


def load_statistical_summary(filepath):
    p_matrix   = np.full((len(METRICS), len(PAIRS)), np.nan)
    d_matrix   = np.full((len(METRICS), len(PAIRS)), np.nan)
    sig_matrix = [["" for _ in PAIRS] for _ in METRICS]

    if not os.path.exists(filepath):
        return p_matrix, d_matrix, sig_matrix

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            metric = row["Metric"]
            pair   = row["Pair"]
            if metric not in METRICS or pair not in PAIRS:
                continue
            i = METRICS.index(metric)
            j = PAIRS.index(pair)
            p_matrix[i, j]  = float(row["p_value"])
            d_matrix[i, j]  = abs(float(row["Cohens_d"]))
            sig_matrix[i][j] = row.get("Significant_p05", "")

    return p_matrix, d_matrix, sig_matrix


def plot_sensitivity_curves(ax, mode_data):
    for i, (mode, (d, p, c, mf, q, ms)) in enumerate(mode_data.items()):
        color = color_for(mode, i)
        ax.plot(d, norm(ms), label=f"{mode.capitalize()} - Merit Scaled",
                linewidth=2, color=color)
        ax.plot(d, norm(c),  label=f"{mode.capitalize()} - Coherence",
                linestyle="--", color=color, alpha=0.5)

    ax.set_xlabel("Distance (m)", fontsize=10)
    ax.set_ylabel("Normalized value", fontsize=10)
    ax.set_title(
        f"Morphological Sensitivity Benchmark v1.2.2 - {len(mode_data)} Morphologies",
        fontsize=11,
    )
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, ncol=2)


def plot_stat_heatmaps(ax_p, ax_d, p_matrix, d_matrix, sig_matrix):
    short_metrics = ["Merit\nScaled", "Coherence\nRatio", "Peak\nAF"]
    short_pairs = [
        f"{a[:3]}/{b[:3]}"
        for a, b in combinations(MORPHOLOGY_MODES, 2)
    ]

    masked_p = np.where(np.isnan(p_matrix), 1.0, p_matrix)
    im1 = ax_p.imshow(masked_p, cmap="RdYlGn_r", vmin=0, vmax=0.1, aspect="auto")
    ax_p.set_xticks(range(len(PAIRS)))
    ax_p.set_xticklabels(short_pairs, fontsize=7, rotation=45, ha="right")
    ax_p.set_yticks(range(len(METRICS)))
    ax_p.set_yticklabels(short_metrics, fontsize=8)
    ax_p.set_title("p-value  (green = significant, p < 0.05)", fontsize=9)
    for i in range(len(METRICS)):
        for j in range(len(PAIRS)):
            val = p_matrix[i, j]
            if np.isnan(val):
                label = "n/a"
            else:
                sig = "*" if sig_matrix[i][j] == "yes" else ""
                label = f"{val:.3f}{sig}"
            txt_color = "white" if (not np.isnan(val) and val < 0.01) else "black"
            ax_p.text(j, i, label, ha="center", va="center",
                      fontsize=6, color=txt_color, fontweight="bold")
    plt.colorbar(im1, ax=ax_p, fraction=0.046, pad=0.04)

    d_max = max(float(np.nanmax(d_matrix)) if not np.all(np.isnan(d_matrix)) else 1.0, 1.0)
    masked_d = np.where(np.isnan(d_matrix), 0.0, d_matrix)
    im2 = ax_d.imshow(masked_d, cmap="Blues", vmin=0, vmax=d_max, aspect="auto")
    ax_d.set_xticks(range(len(PAIRS)))
    ax_d.set_xticklabels(short_pairs, fontsize=7, rotation=45, ha="right")
    ax_d.set_yticks(range(len(METRICS)))
    ax_d.set_yticklabels(short_metrics, fontsize=8)
    ax_d.set_title("|Cohen's d|  (dark blue = large effect > 0.8)", fontsize=9)
    for i in range(len(METRICS)):
        for j in range(len(PAIRS)):
            val = d_matrix[i, j]
            label = "n/a" if np.isnan(val) else f"{val:.2f}"
            txt_color = "white" if (not np.isnan(val) and val > d_max * 0.6) else "black"
            ax_d.text(j, i, label, ha="center", va="center",
                      fontsize=6, color=txt_color, fontweight="bold")
    plt.colorbar(im2, ax=ax_d, fraction=0.046, pad=0.04)


def plot():
    mode_data = {}
    for mode in MORPHOLOGY_MODES:
        path = output_path(f"simulation_results_{mode}.csv")
        if not os.path.exists(path):
            print(f"[plot_sensitivity] Missing: {rel(path)} - skipping.")
            continue
        mode_data[mode] = load_mode_data(path)

    if len(mode_data) < 2:
        print("[plot_sensitivity] Need at least 2 morphologies - aborting.")
        return

    stat_path = output_path("statistical_summary.csv")
    p_matrix, d_matrix, sig_matrix = load_statistical_summary(stat_path)
    has_stats = not np.all(np.isnan(p_matrix))

    if has_stats:
        fig = plt.figure(figsize=(20, 11))
        gs  = fig.add_gridspec(2, 2, height_ratios=[1.6, 1], hspace=0.48, wspace=0.38)
        ax_curves = fig.add_subplot(gs[0, :])
        ax_p      = fig.add_subplot(gs[1, 0])
        ax_d      = fig.add_subplot(gs[1, 1])
        plot_sensitivity_curves(ax_curves, mode_data)
        plot_stat_heatmaps(ax_p, ax_d, p_matrix, d_matrix, sig_matrix)
        fig.suptitle(
            "Biotic Hardware Synthesis v1.2.2 - Morphological Benchmark & Statistical Validation",
            fontsize=13, fontweight="bold", y=0.99,
        )
    else:
        fig, ax_curves = plt.subplots(figsize=(14, 6))
        plot_sensitivity_curves(ax_curves, mode_data)

    ensure_output_dir()
    out_png = output_path("sensitivity_analysis.png")
    data_png = data_path("sensitivity_analysis.png")
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.savefig(data_png, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[plot_sensitivity] Plot saved: {rel(out_png)}")
    print(f"[plot_sensitivity] Plot also saved: {rel(data_png)}")


if __name__ == "__main__":
    plot()