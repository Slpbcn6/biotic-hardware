import numpy as np
import csv
import os
import json

from input_generator import load_morphology

os.makedirs("data", exist_ok=True)


def load_resonance(path="data/resonance_params.json"):
    with open(path, "r") as f:
        return json.load(f)


def compute_array_factor(d, Q, positions):

    theta = np.linspace(0, 2 * np.pi, 200)

    k0 = 0.004
    k = k0 * (1 + 0.15 * (Q - 0.785))

    phases = np.array([0, np.pi / 2, np.pi, 3 * np.pi / 2])

    af = np.zeros_like(theta, dtype=complex)

    for pos, phi in zip(positions, phases):

        spatial = k * (
            pos[0] * np.cos(theta) +
            pos[1] * np.sin(theta)
        )

        af += np.exp(1j * (spatial + phi))

    magnitude = np.abs(af)

    peak = np.max(magnitude)
    mean = np.mean(magnitude)

    coherence = peak / (mean + 1e-12)

    return peak, coherence


def run_sweep(use_generated_morphology=False):

    resonance = load_resonance()
    Q0 = float(resonance["Q_factor"])

    distances = np.linspace(0.1, 2.0, 30)
    d_norm = distances / np.max(distances)

    peaks = []
    coherences = []
    merits = []

    for d in distances:

        if use_generated_morphology:
            base = load_morphology("fractal")

            positions = base[:4].copy()
            positions[:, 0] *= d
            positions[:, 1] *= d

        else:
            positions = np.array([
                [0, 0, 0],
                [d, 0, 0],
                [0, d, 0],
                [d, d, 0]
            ])

        peak, coherence = compute_array_factor(d, Q0, positions)

        merit = peak * coherence

        peaks.append(peak)
        coherences.append(coherence)
        merits.append(merit)

    mean_coh = np.mean(coherences)

    alpha = 0.6
    beta = 0.25

    Q_list = [
        Q0 * (1 + alpha * (c - mean_coh) - beta * dn)
        for c, dn in zip(coherences, d_norm)
    ]

    merit_scaled_list = [
        m * q for m, q in zip(merits, Q_list)
    ]

    output_path = "data/simulation_results.csv"

    with open(output_path, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Distance",
            "Peak_AF",
            "Coherence_Ratio",
            "Merit_Function",
            "Q_effective",
            "Merit_Scaled"
        ])

        for i, d in enumerate(distances):

            writer.writerow([
                d,
                peaks[i],
                coherences[i],
                merits[i],
                Q_list[i],
                merit_scaled_list[i]
            ])


if __name__ == "__main__":
    run_sweep()