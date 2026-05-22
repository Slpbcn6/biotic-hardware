import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def run(script):
    print(f"\n▶ Running {script}")
    subprocess.run([sys.executable, str(ROOT / script)], check=True)


def main():
    print("\n===================================================")
    print(" HIERARCHICAL SPATIAL SENSITIVITY PIPELINE")
    print("===================================================")

    print("\n[1/3] Executing node resonance model...")
    run("data/node_resonance.py")

    print("\n[2/3] Executing coupling simulation...")
    run("data/node_coupling.py")

    print("\n[3/3] Generating sensitivity analysis...")
    run("data/plot_sensitivity.py")

    print("\n===================================================")
    print(" SIMULATION COMPLETE")
    print("===================================================")

    print("\nGenerated artifacts:")
    print(" - data/resonance_params.json")
    print(" - data/simulation_results.csv")
    print(" - data/sensitivity_analysis.png")

    print("\nSystem status:")
    print(" ✔ Node resonance model: OK")
    print(" ✔ Coupling simulation: OK")
    print(" ✔ Sensitivity analysis: OK")
    print(" ✔ Hierarchical pipeline: COMPLETE")

    print("\n▶ Biotic Hardware Simulation: SUCCESSFUL EXECUTION")


if __name__ == "__main__":
    main()