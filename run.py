import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def run(script):
    print(f"\nRunning {script}")
    subprocess.run([sys.executable, str(ROOT / script)], check=True)


def main():
    print("\n--- NORMALIZED SPATIAL SENSITIVITY PIPELINE ---")

    run("data/node_coupling.py")
    run("data/plot_sensitivity.py")

    print("\n--- COMPLETE ---")
    print("Outputs:")
    print("- simulation_results.csv")
    print("- sensitivity_analysis.png")


if __name__ == "__main__":
    main()