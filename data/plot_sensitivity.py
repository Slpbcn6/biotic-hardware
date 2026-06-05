import numpy as np
import matplotlib.pyplot as plt
import csv
import os

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

    return np.array(d), np.array(p), np.array(c), np.array(m), np.array(q), np.array(ms)

def norm(x):
    return (x - x.min()) / (x.max() - x.min() + 1e-12)

def plot():
    f_path = "data/simulation_results_fractal.csv"
    b_path = "data/simulation_results_botanical.csv"
    r_path = "data/simulation_results_random.csv"

    if not os.path.exists(f_path) or not os.path.exists(b_path):
        print("Missing benchmark datasets")
        return

    df, pf, cf, mf, qf, msf = load_mode_data(f_path)
    db, pb, cb, mb, qb, msb = load_mode_data(b_path)

    has_random = os.path.exists(r_path)
    if has_random:
        dr, pr, cr, mr, qr, msr = load_mode_data(r_path)

    plt.figure(figsize=(14, 6))

    plt.plot(df, norm(msf), label="Fractal — Merit Scaled", linewidth=2, color="#2196F3")
    plt.plot(df, norm(cf),  label="Fractal — Coherence",    linestyle="--", color="#2196F3", alpha=0.6)

    plt.plot(db, norm(msb), label="Botanical — Merit Scaled", linewidth=2, color="#4CAF50")
    plt.plot(db, norm(cb),  label="Botanical — Coherence",    linestyle="--", color="#4CAF50", alpha=0.6)

    if has_random:
        plt.plot(dr, norm(msr), label="Random Control — Merit Scaled", linewidth=2, color="#FF5722")
        plt.plot(dr, norm(cr),  label="Random Control — Coherence",    linestyle="--", color="#FF5722", alpha=0.6)

    plt.xlabel("Distance")
    plt.ylabel("Normalized Metrics")
    plt.title("Morphological Sensitivity Benchmark v1.1 — Bio-Inspired vs. Random Control")
    plt.grid(True, alpha=0.3)
    plt.legend()

    os.makedirs("data", exist_ok=True)
    plt.savefig("data/sensitivity_analysis.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("Plot generated: data/sensitivity_analysis.png")

if __name__ == "__main__":
    plot()