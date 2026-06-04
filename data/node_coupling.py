import numpy as np
import csv
import json
import os
<<<<<<< HEAD
from pathlib import Path

from data import input_generator

os.makedirs("data", exist_ok=True)


=======
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import input_generator

os.makedirs("data", exist_ok=True)

>>>>>>> 095aff2e377e7b34f157569668481023b770e39f
def load_simulation_parameters():
    with open("data/parameters.json", "r") as f:
        return json.load(f)

<<<<<<< HEAD

=======
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f
def compute_array_factor(positions, Q):
    theta = np.linspace(0, 2 * np.pi, 200)
    k0 = 0.004
    k = k0 * (1 + 0.15 * (Q - 0.785))
<<<<<<< HEAD

    base_phases = [0, np.pi / 2, np.pi, 3 * np.pi / 2]
    phases = np.array([base_phases[i % 4] for i in range(len(positions))])

=======
    
    base_phases = [0, np.pi/2, np.pi, 3*np.pi/2]
    phases = np.array([base_phases[i % 4] for i in range(len(positions))])
    
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f
    af = np.zeros_like(theta, dtype=complex)
    for pos, phi in zip(positions, phases):
        spatial = k * (pos[0] * np.cos(theta) + pos[1] * np.sin(theta))
        af += np.exp(1j * (spatial + phi))
    
    magnitude = np.abs(af)
    peak = np.max(magnitude)
    mean = np.mean(magnitude)
    coherence = peak / (mean + 1e-12)
<<<<<<< HEAD

    return peak, coherence, mean, magnitude


def run_sweep(output_file, tensor_file):
    params = load_simulation_parameters()

    Q0 = float(params["IV_network_performance_metrics"]["individual_q_factor"])
    sweep_cfg = params["VI_experimental_sweep_parameters"]

=======
    
    return peak, coherence, mean, magnitude

def run_sweep():
    params = load_simulation_parameters()
    
    Q0 = float(params["IV_network_performance_metrics"]["individual_q_factor"])
    sweep_cfg = params["VI_experimental_sweep_parameters"]
    
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f
    mode = sweep_cfg["morphology_mode"]
    n_nodes = int(sweep_cfg["n_nodes"])
    seed = int(sweep_cfg["seed"])
    beta = float(sweep_cfg["beta_loss_factor"])
<<<<<<< HEAD

    if mode == "fractal":
        base_nodes = input_generator.generate_fractal_morphology(
            n_nodes=n_nodes, seed=seed
        )
        morph_noise = 0.0

    elif mode == "botanical":
        base_nodes = input_generator.generate_botanical_graph(
            n_nodes=n_nodes, seed=seed
        )
        morph_noise = 0.15

    else:
        raise ValueError(f"Unknown morphology mode: {mode}")

    rng = np.random.default_rng(seed)

    distances = np.linspace(0.1, 2.0, 30)
    d_norm = distances / np.max(distances)

    distance_store = []
    mean_store = []
    af_store = []

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Distance",
            "Peak_AF",
            "Coherence_Ratio",
            "Merit_Function",
            "Q_effective",
            "Merit_Scaled"
        ])

        for d, dn in zip(distances, d_norm):

            noise = rng.normal(0, morph_noise, base_nodes.shape)
            positions = (base_nodes + noise) * d

            Q_eff = Q0 * (1 - beta * dn)

            peak, coherence, mean, magnitude = compute_array_factor(
                positions, Q_eff
            )

            merit_base = peak * coherence
            merit_scaled = merit_base * Q_eff

            writer.writerow([
                d,
                peak,
                coherence,
                merit_base,
                Q_eff,
                merit_scaled
            ])

            distance_store.append(d)
            mean_store.append(mean)
            af_store.append(magnitude)

    np.savez(
        output_file.replace(".csv", ".npz"),
        distance=np.array(distance_store),
        mean=np.array(mean_store),
    )

    np.savez(
        tensor_file,
        distance=np.array(distance_store),
        af=np.array(af_store),
    )

=======
    
    if mode == "fractal":
        base_nodes = input_generator.generate_fractal_morphology(n_nodes=n_nodes, seed=seed)
    elif mode == "botanical":
        base_nodes = input_generator.generate_botanical_graph(n_nodes=n_nodes, seed=seed)
    else:
        raise ValueError(f"Unknown morphology mode: {mode}")
    
    distances = np.linspace(0.1, 2.0, 30)
    d_norm = distances / np.max(distances)
    
    distance_store = []
    mean_store = []
    af_store = []
    
    output_path = "data/simulation_results.csv"
    
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Distance", "Peak_AF", "Coherence_Ratio", "Merit_Function", "Q_effective", "Merit_Scaled"])
        
        for d, dn in zip(distances, d_norm):
            positions = base_nodes * d
            Q_eff = Q0 * (1 - beta * dn)
            
            peak, coherence, mean, magnitude = compute_array_factor(positions, Q_eff)
            
            merit_base = peak * coherence
            merit_scaled = merit_base * Q_eff
            
            writer.writerow([d, peak, coherence, merit_base, Q_eff, merit_scaled])
            
            distance_store.append(d)
            mean_store.append(mean)
            af_store.append(magnitude)
            
    np.savez(
        f"data/af_tensors_{mode}.npz",
        distance=np.array(distance_store),
        mean=np.array(mean_store),
        af=np.array(af_store)
    )
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f

if __name__ == "__main__":
    run_sweep(
        "data/simulation_results.csv",
        "data/af_tensors.npz"
    )