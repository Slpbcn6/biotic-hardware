import numpy as np
import matplotlib.pyplot as plt
import csv
import os

os.makedirs('data', exist_ok=True)

def get_positions(d):
    """
    2D square array geometry.
    Node spacing = d controls physical aperture size.
    """
    return np.array([
        [0.0, 0.0, 0.0],
        [d,   0.0, 0.0],
        [0.0, d,   0.0],
        [d,   d,   0.0]
    ])

def compute_array_factor(positions, phases, theta, wavelength):
    """
    Array Factor with physically meaningful phase propagation:
    AF = sum exp(j (k r·u + φ))
    """
    k = 2 * np.pi / wavelength
    af = np.zeros_like(theta, dtype=complex)

    for pos, phi in zip(positions, phases):
        spatial_term = k * (
            pos[0] * np.cos(theta) +
            pos[1] * np.sin(theta)
        )
        af += np.exp(1j * (spatial_term + phi))

    return np.abs(af) / len(positions)

def extract_metrics(af):
    """
    Coherence metrics of interference structure.
    """
    peak = np.max(af)
    mean = np.mean(af)

    coherence = peak / mean if mean > 0 else 0.0

    return peak, coherence

distances_sweep = [0.1, 0.2, 0.3, 0.4]

phases = [0, np.pi/2, np.pi, 3*np.pi/2]

frequency = 12.5
c = 3e8
wavelength = c / frequency

theta = np.linspace(0, 2*np.pi, 200)

results = []

print("Running physically consistent sensitivity analysis...")

for d in distances_sweep:

    positions = get_positions(d)

    af = compute_array_factor(
        positions,
        phases,
        theta,
        wavelength
    )

    peak, coherence = extract_metrics(af)

    results.append([d, peak, coherence])

    print(f"d={d:.2f} | peak={peak:.4f} | coherence={coherence:.4f}")

with open('data/simulation_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Distance', 'Peak_AF', 'Coherence_Ratio'])
    writer.writerows(results)

print("\nAnalysis complete.")
print("Results saved to data/simulation_results.csv")