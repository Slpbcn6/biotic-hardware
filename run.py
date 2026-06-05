import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

def run(script):
    print(f"\n[RUN] {script}")
    subprocess.run([sys.executable, str(ROOT / script)], check=True)

def set_morphology(mode):
    import json
    path = ROOT / "data/parameters.json"
    with open(path, "r") as f:
        data = json.load(f)

    data["VI_experimental_sweep_parameters"]["morphology_mode"] = mode

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def run_coupling(mode, output_file, tensor_file):
    import data.node_coupling as coupling
    coupling.run_sweep(mode, output_file, tensor_file)

def main():
    print("\n===================================================")
    print(" DETERMINISTIC COMPARATIVE MORPHOLOGICAL PIPELINE v1.1")
    print("===================================================")

    print("\n[1/5] Running node resonance baseline...")
    run("data/node_resonance.py")

    print("\n[2/5] Running FRACTAL sweep...")
    set_morphology("fractal")
    run_coupling(
        "fractal",
        "data/simulation_results_fractal.csv",
        "data/af_tensors_fractal.npz"
    )

    print("\n[3/5] Running BOTANICAL sweep...")
    set_morphology("botanical")
    run_coupling(
        "botanical",
        "data/simulation_results_botanical.csv",
        "data/af_tensors_botanical.npz"
    )

    print("\n[4/5] Running RANDOM CONTROL sweep...")
    set_morphology("random")
    run_coupling(
        "random",
        "data/simulation_results_random.csv",
        "data/af_tensors_random.npz"
    )

    print("\n[5/5] Generating sensitivity plot...")
    run("data/plot_sensitivity.py")

    print("\n===================================================")
    print(" BENCHMARK COMPLETE")
    print("===================================================")

if __name__ == "__main__":
    main()