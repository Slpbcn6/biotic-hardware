import numpy as np
import csv
import os

os.makedirs("data", exist_ok=True)


def compute_array_factor(d):
    """
    Simplified coherent system model.
    Returns peak response and coherence ratio.
    """

    theta = np.linspace(0, 2 * np.pi, 200)

    k = 0.004
    phases = [0, np.pi/2, np.pi, 3*np.pi/2]

    # geometry
    positions = np.array([
        [0, 0, 0],
        [d, 0, 0],
        [0, d, 0],
        [d, d, 0]
    ])

    af = np.zeros_like(theta, dtype=complex)

    for pos, phi in zip(positions, phases):
        spatial = k * (pos[0] * np.cos(theta) + pos[1] * np.sin(theta))
        af += np.exp(1j * (spatial + phi))

    magnitude = np.abs(af)

    peak = np.max(magnitude)
    mean = np.mean(magnitude)

    coherence_ratio = peak / (mean + 1e-12)

    return peak, coherence_ratio


def run_sweep():
    print("Running normalized sensitivity analysis...")

    distances = np.linspace(0.1, 2.0, 30)

    results = []

    for d in distances:
        peak, coherence = compute_array_factor(d)
        d_norm = d / np.max(distances)
        merit = peak * coherence

        print(f"d={d:.2f} | peak={peak:.6f} | coherence={coherence:.6f} | merit={merit:.6e}")

        results.append([d, d_norm, peak, coherence, merit])

    with open("data/simulation_results.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Distance",
            "d_norm",
            "Peak_AF",
            "Coherence_Ratio",
            "Merit_Function"
        ])

        writer.writerows(results)

    print("\nSaved: data/simulation_results.csv")


if __name__ == "__main__":
    run_sweep()