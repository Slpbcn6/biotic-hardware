import csv
import os

import matplotlib.pyplot as plt
import numpy as np


COLORS = {
    "fractal":   "#2196F3",
    "botanical": "#4CAF50",
    "random":    "#FF5722",
}

METRICS = ["Merit_Scaled", "Coherence_Ratio", "Peak_AF"]
PAIRS   = ["Fractal vs Botanical", "Fractal vs Random", "Botanical vs Random"]


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


def plot_sensitivity_curves(ax, df, pf, cf, msf, db, pb, cb, msb,
                            has_random, dr, cr, msr):
    ax.plot(df, norm(msf), label="Fractal - Merit Scaled",
            linewidth=2, color=COLORS["fractal"])
    ax.plot(df, norm(cf),  label="Fractal - Coherence",
            linestyle="--", color=COLORS["fractal"], alpha=0.6)

    ax.plot(db, norm(msb), label="Botanical - Merit Scaled",
            linewidth=2, color=COLORS["botanical"])
    ax.plot(db, norm(cb),  label="Botanical - Coherence",
            linestyle="--", color=COLORS["botanical"], alpha=0.6)

    if has_random:
        ax.plot(dr, norm(msr), label="Random Control - Merit Scaled",
                linewidth=2, color=COLORS["random"])
        ax.plot(dr, norm(cr),  label="Random Control - Coherence",
                linestyle="--", color=COLORS["random"], alpha=0.6)

    ax.set_xlabel("Distance (m)", fontsize=10)
    ax.set_ylabel("Normalized value", fontsize=10)
    ax.set_title(
        "Morphological Sensitivity Benchmark v1.2 — Bio-Inspired vs. Random Control",
        fontsize=11,
    )
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9)


def plot_stat_heatmaps(ax_p, ax_d, p_matrix, d_matrix, sig_matrix):
    short_metrics = ["Merit\nScaled", "Coherence\nRatio", "Peak\nAF"]
    short_pairs   = ["Frac vs\nBot", "Frac vs\nRand", "Bot vs\nRand"]

    masked_p = np.where(np.isnan(p_matrix), 1.0, p_matrix)
    im1 = ax_p.imshow(masked_p, cmap="RdYlGn_r", vmin=0, vmax=0.1, aspect="auto")
    ax_p.set_xticks(range(len(PAIRS)))
    ax_p.set_xticklabels(short_pairs, fontsize=8)
    ax_p.set_yticks(range(len(METRICS)))
    ax_p.set_yticklabels(short_metrics, fontsize=8)
    ax_p.set_title("p-value  (green = significant, threshold 0.05)", fontsize=9)
    for i in range(len(METRICS)):
        for j in range(len(PAIRS)):
            val = p_matrix[i, j]
            if np.isnan(val):
                label = "n/a"
            else:
                sig = "*" if sig_matrix[i][j] == "yes" else ""
                label = f"{val:.4f}{sig}"
            txt_color = "white" if (not np.isnan(val) and val < 0.01) else "black"
            ax_p.text(j, i, label, ha="center", va="center",
                      fontsize=8, color=txt_color, fontweight="bold")
    plt.colorbar(im1, ax=ax_p, fraction=0.046, pad=0.04)

    d_max = max(float(np.nanmax(d_matrix)) if not np.all(np.isnan(d_matrix)) else 1.0, 1.0)
    masked_d = np.where(np.isnan(d_matrix), 0.0, d_matrix)
    im2 = ax_d.imshow(masked_d, cmap="Blues", vmin=0, vmax=d_max, aspect="auto")
    ax_d.set_xticks(range(len(PAIRS)))
    ax_d.set_xticklabels(short_pairs, fontsize=8)
    ax_d.set_yticks(range(len(METRICS)))
    ax_d.set_yticklabels(short_metrics, fontsize=8)
    ax_d.set_title("|Cohen's d|  (dark blue = large effect > 0.8)", fontsize=9)
    for i in range(len(METRICS)):
        for j in range(len(PAIRS)):
            val = d_matrix[i, j]
            label = "n/a" if np.isnan(val) else f"{val:.2f}"
            txt_color = "white" if (not np.isnan(val) and val > d_max * 0.6) else "black"
            ax_d.text(j, i, label, ha="center", va="center",
                      fontsize=8, color=txt_color, fontweight="bold")
    plt.colorbar(im2, ax=ax_d, fraction=0.046, pad=0.04)


def plot():
    f_path    = "data/simulation_results_fractal.csv"
    b_path    = "data/simulation_results_botanical.csv"
    r_path    = "data/simulation_results_random.csv"
    stat_path = "data/statistical_summary.csv"

    if not os.path.exists(f_path) or not os.path.exists(b_path):
        print("[plot_sensitivity] Missing benchmark datasets — aborting.")
        return

    df, pf, cf, mf, qf, msf = load_mode_data(f_path)
    db, pb, cb, mb, qb, msb = load_mode_data(b_path)

    has_random = os.path.exists(r_path)
    dr = cr = msr = None
    if has_random:
        dr, pr, cr, mr, qr, msr = load_mode_data(r_path)

    has_stats = os.path.exists(stat_path)
    p_matrix, d_matrix, sig_matrix = load_statistical_summary(stat_path)

    if has_stats and not np.all(np.isnan(p_matrix)):
        fig = plt.figure(figsize=(16, 10))
        gs  = fig.add_gridspec(2, 2, height_ratios=[1.6, 1], hspace=0.42, wspace=0.35)

        ax_curves = fig.add_subplot(gs[0, :])
        ax_p      = fig.add_subplot(gs[1, 0])
        ax_d      = fig.add_subplot(gs[1, 1])

        plot_sensitivity_curves(ax_curves, df, pf, cf, msf,
                                db, pb, cb, msb, has_random, dr, cr, msr)
        plot_stat_heatmaps(ax_p, ax_d, p_matrix, d_matrix, sig_matrix)

        fig.suptitle(
            "Biotic Hardware Synthesis v1.2 — Morphological Benchmark & Statistical Validation",
            fontsize=13, fontweight="bold", y=0.98,
        )
    else:
        fig, ax_curves = plt.subplots(figsize=(14, 6))
        plot_sensitivity_curves(ax_curves, df, pf, cf, msf,
                                db, pb, cb, msb, has_random, dr, cr, msr)

    os.makedirs("data", exist_ok=True)
    plt.savefig("data/sensitivity_analysis.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[plot_sensitivity] Plot saved: data/sensitivity_analysis.png")


if __name__ == "__main__":
    plot()
