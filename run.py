import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

def run_script(relative_path):
    script_path = ROOT / relative_path
    
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)
    except FileNotFoundError:
        sys.exit(1)

def main():
    run_script("data/node_resonance.py")
    run_script("data/node_coupling.py")

if __name__ == "__main__":
    main()