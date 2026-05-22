import numpy as np
import matplotlib.pyplot as plt
import csv


def load_data():

    with open("data/simulation_results.csv", "r") as f:
        reader = csv.DictReader(f)

        d, p, c, m = [], [], [], []
        q, m_scaled = [], []

        fieldnames = reader.fieldnames

        has_q = "Q_effective" in fieldnames
        has_scaled = "Merit_Scaled" in fieldnames

        for r in reader:
            d.append(float(r["Distance"]))
            p.append(float(r["Peak_AF"]))
            c.append(float(r["Coherence_Ratio"]))
            m.append(float(r["Merit_Function"]))

            if has_q:
                q.append(float(r["Q_effective"]))
            if has_scaled:
                m_scaled.append(float(r["Merit_Scaled"]))

    return d, p, c, m, q, m_scaled, has_q, has_scaled


def norm(x):
    x = np.array(x)
    return (x - x.min()) / (x.max() - x.min() + 1e-12)


def plot():

    d, p, c, m, q, m_scaled, has_q, has_scaled = load_data()

    x = norm(d)

    p = norm(p)
    c = norm(c)
    m = norm(m)

    print("Generating sensitivity visualization...")

    plt.figure(figsize=(10, 5))

    plt.plot(x, p, label="Peak_AF (norm)", linewidth=2)
    plt.plot(x, c, label="Coherence (norm)", linewidth=2)
    plt.plot(x, m, label="Merit (norm)", linewidth=2)

    if has_scaled:
        m_scaled = norm(m_scaled)
        plt.plot(x, m_scaled, label="Merit_Scaled (norm)", linewidth=2)

    if has_q:
        q = norm(q)
        plt.plot(x, q, "--", label="Q_effective (norm)", linewidth=2)

    plt.xlabel("Normalized Distance")
    plt.ylabel("Normalized Response")
    plt.grid(True, linestyle="--", alpha=0.4)

    plt.title("Coupled System Response (fully normalized)")

    plt.legend()

    plt.tight_layout()

    out = "data/sensitivity_analysis.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")

    print("Visualization complete")
    print(f"Saved → {out}")

    plt.show()


if __name__ == "__main__":
    plot()