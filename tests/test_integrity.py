import pandas as pd
import subprocess
import sys
import json
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
            "data/__init__.py",
            "data/parameters.json",
            "data/node_resonance.py",
            "data/node_coupling.py",
            "data/plot_sensitivity.py",
            "data/input_generator.py",
            "data/topology_validator.py",
            "data/schumann_reference.py",
            "data/multi_seed_analysis.py",
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

        # --- v1.1 outputs still present ---
        f_csv = tmp_path / "data/simulation_results_fractal.csv"
        b_csv = tmp_path / "data/simulation_results_botanical.csv"
        r_csv = tmp_path / "data/simulation_results_random.csv"

        assert f_csv.exists(), "fractal CSV missing"
        assert b_csv.exists(), "botanical CSV missing"
        assert r_csv.exists(), "random CSV missing"

        df_f = pd.read_csv(f_csv)
        df_b = pd.read_csv(b_csv)

        metric = "Merit_Scaled"
        assert metric in df_f.columns
        assert metric in df_b.columns

        rel_diff = abs(df_f[metric].mean() - df_b[metric].mean()) / (
            abs(df_f[metric].mean()) + 1e-12
        )
        assert rel_diff > 0.001, "Fractal and botanical metrics must diverge"

        corr = np.corrcoef(df_f[metric], df_b[metric])[0, 1]
        assert corr < 0.999, "Fractal and botanical must not be perfectly correlated"

        # --- v1.2 outputs ---
        stat_csv = tmp_path / "data/statistical_summary.csv"
        multi_csv = tmp_path / "data/multi_seed_summary.csv"
        summary_json = tmp_path / "data/exploration_summary.json"

        assert stat_csv.exists(), "statistical_summary.csv missing"
        assert multi_csv.exists(), "multi_seed_summary.csv missing"
        assert summary_json.exists(), "exploration_summary.json missing"

        df_stat = pd.read_csv(stat_csv)
        required_stat_cols = [
            "Metric", "Pair", "t_statistic", "p_value",
            "Significant_p05", "Cohens_d", "Effect_size",
        ]
        for col in required_stat_cols:
            assert col in df_stat.columns, f"Missing column in statistical_summary: {col}"
        assert len(df_stat) == 9, f"Expected 9 rows (3 metrics x 3 pairs), got {len(df_stat)}"

        df_multi = pd.read_csv(multi_csv)
        assert "Morphology" in df_multi.columns
        assert len(df_multi) == 3, "Expected 3 morphology rows in multi_seed_summary"

        with open(summary_json) as fj:
            summary = json.load(fj)
        assert "pipeline_version" in summary
        assert "resonance_baseline" in summary
        assert "multi_seed_analysis" in summary
        assert summary["pipeline_version"] == "1.2.0"