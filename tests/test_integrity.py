import pandas as pd
import subprocess
import sys
from pathlib import Path
import shutil
import tempfile
import numpy as np

ROOT = Path(__file__).parent.parent


def test_morphological_divergence():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        essential_files = [
            "run.py",
            "data/parameters.json",
            "data/node_resonance.py",
            "data/node_coupling.py",
            "data/plot_sensitivity.py",
            "data/input_generator.py",
        ]

        for src in essential_files:
            dest = tmp_path / src
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / src, dest)

        result = subprocess.run(
            [sys.executable, "run.py"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, result.stderr

        f = tmp_path / "data/simulation_results_fractal.csv"
        b = tmp_path / "data/simulation_results_botanical.csv"

        assert f.exists()
        assert b.exists()

        df_f = pd.read_csv(f)
        df_b = pd.read_csv(b)

        metric = "Merit_Scaled"

        assert metric in df_f.columns
        assert metric in df_b.columns

        mf = df_f[metric].mean()
        mb = df_b[metric].mean()

        rel_diff = abs(mf - mb) / (abs(mf) + 1e-12)
        assert rel_diff > 0.001

        corr = np.corrcoef(df_f[metric], df_b[metric])[0, 1]
        assert corr < 0.999