import numpy as np
import csv
import json
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import input_generator

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

def run_sweep():
    params = load_simulation_parameters()
    
    Q0 = float(params["IV_network_performance_metrics"]["individual_q_factor"])
    sweep_cfg = params["VI_experimental_sweep_parameters"]
    
    mode = sweep_cfg["morphology_mode"]
    n_nodes = int(sweep_cfg["n_nodes"])
    seed = int(sweep_cfg["seed"])
    beta = float(sweep_cfg["beta_loss_factor"])
    
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

if __name__ == "__main__":
    run_sweep()