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
<<<<<<< HEAD

    if not os.path.exists(f_path) or not os.path.exists(b_path):
        print("Error: Missing benchmark output datasets.")
        return

    df, pf, cf, mf, qf, msf = load_mode_data(f_path)
    db, pb, cb, mb, qb, msb = load_mode_data(b_path)

    plt.figure(figsize=(12, 6))

    plt.plot(df, norm(msf), label="Fractal - Merit Scaled (norm)", color="blue", linewidth=2)
    plt.plot(df, norm(cf), label="Fractal - Coherence (norm)", color="cyan", linestyle="--")

    plt.plot(db, norm(msb), label="Botanical - Merit Scaled (norm)", color="red", linewidth=2)
    plt.plot(db, norm(cb), label="Botanical - Coherence (norm)", color="orange", linestyle="--")

=======
    
    if not os.path.exists(f_path) or not os.path.exists(b_path):
        print("Error: Missing benchmark output datasets.")
        return
        
    df, pf, cf, mf, qf, msf = load_mode_data(f_path)
    db, pb, cb, mb, qb, msb = load_mode_data(b_path)
    
    plt.figure(figsize=(12, 6))
    
    plt.plot(df, norm(msf), label="Fractal - Merit Scaled (norm)", color="blue", linewidth=2)
    plt.plot(df, norm(cf), label="Fractal - Coherence (norm)", color="cyan", linestyle="--")
    
    plt.plot(db, norm(msb), label="Botanical - Merit Scaled (norm)", color="red", linewidth=2)
    plt.plot(db, norm(cb), label="Botanical - Coherence (norm)", color="orange", linestyle="--")
    
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f
    plt.xlabel("Distance")
    plt.ylabel("Normalized Metrics")
    plt.title("Morphology Benchmark: Fractal vs Botanical (v1.1)")
    plt.grid(True)
    plt.legend()
<<<<<<< HEAD

    os.makedirs("data", exist_ok=True)
    plt.savefig("data/sensitivity_analysis.png", dpi=300)
    plt.close()

    print("Comparative plot generated successfully: data/sensitivity_analysis.png")
=======
    
    os.makedirs("data", exist_ok=True)
    plt.savefig("data/sensitivity_analysis.png", dpi=300)
    plt.close()
    print("✔ Comparative plot generated successfully: data/sensitivity_analysis.png")
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f

if __name__ == "__main__":
    plot()