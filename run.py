import subprocess
import sys
import json
<<<<<<< HEAD
=======
import shutil
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f
from pathlib import Path

ROOT = Path(__file__).parent

def run(script):
<<<<<<< HEAD
    print(f"Executing: {script}")
=======
    print(f"\n▶ Executing: {script}")
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f
    subprocess.run([sys.executable, str(ROOT / script)], check=True)

def set_morphology(mode):
    path = ROOT / "data/parameters.json"
    with open(path, "r") as f:
        data = json.load(f)
    data["VI_experimental_sweep_parameters"]["morphology_mode"] = mode
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def set_morphology(mode):
    path = ROOT / "data/parameters.json"

    with open(path, "r") as f:
        data = json.load(f)

    data["VI_experimental_sweep_parameters"]["morphology_mode"] = mode

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def run_coupling(mode, output_file, tensor_file):
    set_morphology(mode)

    import data.node_coupling as coupling
    coupling.run_sweep(output_file, tensor_file)


def main():
<<<<<<< HEAD
    print("===================================================")
    print("DETERMINISTIC COMPARATIVE MORPHOLOGICAL PIPELINE v1.1")
    print("===================================================")

    run("data/node_resonance.py")

    run_coupling(
        "fractal",
        "data/simulation_results_fractal.csv",
        "data/af_tensors_fractal.npz"
    )

    run_coupling(
        "botanical",
        "data/simulation_results_botanical.csv",
        "data/af_tensors_botanical.npz"
    )

    run("data/plot_sensitivity.py")

    print("===================================================")
    print("BENCHMARK COMPLETE: SUCCESSFUL EXECUTION")
    print("===================================================")

=======
    print("\n===================================================")
    print(" DETERMINISTIC COMPARATIVE MORPHOLOGICAL PIPELINE v1.1")
    print("===================================================")
    
    print("\n[1/4] Running node resonance baseline calculation...")
    run("data/node_resonance.py")
    
    print("\n[2/4] Executing Sweep for FRACTAL morphology...")
    set_morphology("fractal")
    run("data/node_coupling.py")
    shutil.copy(ROOT / "data/simulation_results.csv", ROOT / "data/simulation_results_fractal.csv")
    
    print("\n[3/4] Executing Sweep for BOTANICAL morphology...")
    set_morphology("botanical")
    run("data/node_coupling.py")
    shutil.copy(ROOT / "data/simulation_results.csv", ROOT / "data/simulation_results_botanical.csv")
    
    print("\n[4/4] Generating comparative visualization metrics...")
    run("data/plot_sensitivity.py")
    
    print("\n===================================================")
    print(" BENCHMARK COMPLETE: SUCCESSFUL EXECUTION")
    print("===================================================")
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f

if __name__ == "__main__":
    main()