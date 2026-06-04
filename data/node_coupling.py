import numpy as np
import csv
import json
import os

from data import input_generator

os.makedirs("data", exist_ok=True)

def load_simulation_parameters():
    with open("data/parameters.json", "r") as f:
        return json.load(f)

def compute_array_factor(positions, Q):
    theta = np.linspace(0, 2 * np.pi, 200)
    k0 = 0.004
    k = k0 * (1 + 0.15 * (Q - 0.785))

    base_phases = [0, np.pi/2, np.pi, 3*np.pi/2]
    phases = np.array([base_phases[i % 4] for i in range(len(positions))])

    af = np.zeros_like(theta, dtype=complex)

    for pos, phi in zip(positions, phases):
        spatial = k * (pos[0] * np.cos(theta) + pos[1] * np.sin(theta))
        af += np.exp(1j * (spatial + phi))

    magnitude = np.abs(af)
    peak = np.max(magnitude)
    mean = np.mean(magnitude)
    coherence = peak / (mean + 1e-12)

    return peak, coherence, mean, magnitude

def run_sweep(mode, output_file, tensor_file):
    params = load_simulation_parameters()

    Q0 = float(params["IV_network_performance_metrics"]["individual_q_factor"])
    cfg = params["VI_experimental_sweep_parameters"]

    n_nodes = int(cfg["n_nodes"])
    seed = int(cfg["seed"])
    beta = float(cfg["beta_loss_factor"])

    if mode == "fractal":
        base_nodes = input_generator.generate_fractal_morphology(n_nodes=n_nodes, seed=seed)
        noise = 0.0
    elif mode == "botanical":
        base_nodes = input_generator.generate_botanical_graph(n_nodes=n_nodes, seed=seed)
        noise = 0.15
    else:
        raise ValueError(f"Unknown mode: {mode}")

    rng = np.random.default_rng(seed)

    distances = np.linspace(0.1, 2.0, 30)

    distance_store = []
    mean_store = []
    af_store = []

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Distance", "Peak_AF", "Coherence_Ratio", "Merit_Function", "Q_effective", "Merit_Scaled"])

        for i, d in enumerate(distances):

            perturb = rng.normal(0, noise, base_nodes.shape)
            positions = (base_nodes + perturb) * d

            Q_eff = Q0 * (1 - beta * (i / len(distances)))

            peak, coherence, mean, magnitude = compute_array_factor(positions, Q_eff)

            merit = peak * coherence
            scaled = merit * Q_eff

            writer.writerow([d, peak, coherence, merit, Q_eff, scaled])

            distance_store.append(d)
            mean_store.append(mean)
            af_store.append(magnitude)

    np.savez(output_file.replace(".csv", ".npz"),
             distance=np.array(distance_store),
             mean=np.array(mean_store))

    np.savez(tensor_file,
             distance=np.array(distance_store),
             af=np.array(af_store))