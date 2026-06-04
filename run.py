import subprocess
import sys
import json
from pathlib import Path

ROOT = Path(__file__).parent


def run(script):
    print(f"Executing: {script}")
    subprocess.run([sys.executable, str(ROOT / script)], check=True)


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


if __name__ == "__main__":
    main()