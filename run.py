import subprocess
import sys
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

def run(script):
    print(f"\n▶ Executing: {script}")
    subprocess.run([sys.executable, str(ROOT / script)], check=True)

def set_morphology(mode):
    path = ROOT / "data/parameters.json"
    with open(path, "r") as f:
        data = json.load(f)
    data["VI_experimental_sweep_parameters"]["morphology_mode"] = mode
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
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

if __name__ == "__main__":
    main()