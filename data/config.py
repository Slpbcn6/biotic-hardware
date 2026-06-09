"""Single source of truth for paths and pipeline morphologies.

All generated artifacts are written under OUTPUT_DIR (outputs/). The sensitivity
plot is additionally written into DATA_DIR (data/).

The morphology list is read from parameters.json (VIII_pipeline.morphologies)
so that run.py, multi_seed_analysis.py, plot_sensitivity.py and the tests never
hardcode their own divergent copies.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
PARAMETERS_PATH = DATA_DIR / "parameters.json"


def load_parameters():
    with open(PARAMETERS_PATH, "r") as f:
        return json.load(f)


def morphologies():
    return list(load_parameters()["VIII_pipeline"]["morphologies"])


def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def output_path(name):
    return str(OUTPUT_DIR / name)


def data_path(name):
    return str(DATA_DIR / name)


def rel(path):
    """Display helper: format a path relative to the repo root as a POSIX
    string (e.g. 'outputs/foo.json'), so console logs never leak absolute
    machine-specific paths. Falls back to the bare filename if the path is
    outside the repo root."""
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(path).name