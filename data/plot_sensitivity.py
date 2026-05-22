import numpy as np
import matplotlib.pyplot as plt
import csv

def load_data():
    d, dn, p, c, m = [], [], [], [], []

    with open("data/simulation_results.csv", "r") as f:
        reader = csv.DictReader(f)

        required = {"Distance", "d_norm", "Peak_AF", "Coherence_Ratio", "Merit_Function"}
        if not required.issubset(reader.fieldnames):
            raise ValueError(f"CSV schema mismatch: {reader.fieldnames}")

        for r in reader:
            d.append(float(r["Distance"]))
            dn.append(float(r["d_norm"]))
            p.append(float(r["Peak_AF"]))
            c.append(float(r["Coherence_Ratio"]))
            m.append(float(r["Merit_Function"]))

    return map(list, zip(*sorted(zip(d, dn, p, c, m))))

def plot():
    d, dn, p, c, m = load_data()

    print("\nGenerating sensitivity visualization...")

    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(dn, p, label="Peak Array Factor", linewidth=2)
    ax1.plot(dn, m, label="Merit Function (P × C)", linewidth=2)

    ax1.set_xlabel("Normalized Spatial Parameter (d / d_max)")
    ax1.set_ylabel("Amplitude Metrics")
    ax1.grid(True, linestyle="--", alpha=0.5)

    ax2 = ax1.twinx()
    ax2.plot(dn, c, color="red", label="Coherence Ratio", linewidth=2)
    ax2.set_ylabel("Coherence Metric")

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(lines + lines2, labels + labels2, loc="best")

    plt.title("Normalized Sensitivity Analysis of Coupled Spatial Network")

    plt.tight_layout()

    output_path = "data/sensitivity_analysis.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    print("\n===================================================")
    print(" VISUALIZATION COMPLETE")
    print("===================================================")

    print(f"Saved figure → {output_path}")
    print("Resolution: 300 DPI")
    print("Layout: tight bbox (publication-ready)")

    plt.show()

if __name__ == "__main__":
    plot()