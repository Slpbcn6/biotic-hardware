import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def run(script):
    print(f"\n▶ Running {script}")
    subprocess.run([sys.executable, str(ROOT / script)], check=True)


def main():
    print("\n===================================================")
    print(" NORMALIZED SPATIAL SENSITIVITY PIPELINE")
    print("===================================================")

    print("\n[1/2] Executing coupling simulation...")
    run("data/node_coupling.py")

    print("\n[2/2] Generating sensitivity analysis...")
    run("data/plot_sensitivity.py")

    print("\n===================================================")
    print(" SIMULATION COMPLETE")
    print("===================================================")

    print("\nGenerated artifacts:")
    print(" - data/simulation_results.csv")
    print(" - data/sensitivity_analysis.png")

    print("\nSystem status:")
    print(" ✔ Coupling simulation: OK")
    print(" ✔ Sensitivity analysis: OK")
    print(" ✔ Output pipeline: COMPLETE")

    print("\n▶ Biotic Hardware Simulation: SUCCESSFUL EXECUTION")


if __name__ == "__main__":
    main()