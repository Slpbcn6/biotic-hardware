import pandas as pd
import subprocess
import sys
import json
from pathlib import Path
import shutil
import tempfile
import numpy as np
from itertools import combinations

ROOT = Path(__file__).parent.parent

with open(ROOT / "data" / "parameters.json") as _f:
    MORPHOLOGY_MODES = json.load(_f)["VIII_pipeline"]["morphologies"]


def test_morphological_divergence():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        essential_files = [
            "run.py",
            "data/__init__.py",
            "data/config.py",
            "data/parameters.json",
            "data/node_resonance.py",
            "data/node_coupling.py",
            "data/plot_sensitivity.py",
            "data/input_generator.py",
            "data/topology_validator.py",
            "data/schumann_reference.py",
            "data/multi_seed_analysis.py",
            "data/parameter_derivation.py",
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

        for mode in MORPHOLOGY_MODES:
            csv_path = tmp_path / f"outputs/simulation_results_{mode}.csv"
            assert csv_path.exists(), f"{mode} CSV missing"

        df_f = pd.read_csv(tmp_path / "outputs/simulation_results_fractal.csv")
        df_b = pd.read_csv(tmp_path / "outputs/simulation_results_botanical.csv")

        metric = "Merit_Scaled"
        assert metric in df_f.columns
        assert metric in df_b.columns

        rel_diff = abs(df_f[metric].mean() - df_b[metric].mean()) / (
            abs(df_f[metric].mean()) + 1e-12
        )
        assert rel_diff > 0.001, "Fractal and botanical metrics must diverge"

        corr = np.corrcoef(df_f[metric], df_b[metric])[0, 1]
        assert corr < 0.999, "Fractal and botanical must not be perfectly correlated"

        stat_csv = tmp_path / "outputs/statistical_summary.csv"
        multi_csv = tmp_path / "outputs/multi_seed_summary.csv"
        summary_json = tmp_path / "outputs/exploration_summary.json"

        assert stat_csv.exists(), "statistical_summary.csv missing"
        assert multi_csv.exists(), "multi_seed_summary.csv missing"
        assert summary_json.exists(), "exploration_summary.json missing"

        out_png = tmp_path / "outputs/sensitivity_analysis.png"
        data_png = tmp_path / "data/sensitivity_analysis.png"
        assert out_png.exists(), "sensitivity_analysis.png missing in outputs/"
        assert data_png.exists(), "sensitivity_analysis.png missing in data/"

        df_stat = pd.read_csv(stat_csv)
        required_stat_cols = [
            "Metric", "Pair", "t_statistic", "p_value",
            "Significant_p05", "Cohens_d", "Effect_size",
        ]
        for col in required_stat_cols:
            assert col in df_stat.columns, f"Missing column in statistical_summary: {col}"

        n_modes = len(MORPHOLOGY_MODES)
        expected_pairs = n_modes * (n_modes - 1) // 2
        expected_rows = 3 * expected_pairs
        assert len(df_stat) == expected_rows, (
            f"Expected {expected_rows} rows (3 metrics x {expected_pairs} pairs), "
            f"got {len(df_stat)}"
        )

        pair_labels = set(df_stat["Pair"].unique())
        for a, b in combinations(MORPHOLOGY_MODES, 2):
            expected_label = f"{a.capitalize()} vs {b.capitalize()}"
            assert expected_label in pair_labels, f"Missing pair: {expected_label}"

        df_multi = pd.read_csv(multi_csv)
        assert "Morphology" in df_multi.columns
        assert len(df_multi) == len(MORPHOLOGY_MODES), (
            f"Expected {len(MORPHOLOGY_MODES)} morphology rows in multi_seed_summary"
        )

        with open(summary_json) as fj:
            summary = json.load(fj)
        assert "pipeline_version" in summary
        assert "parameter_derivation" in summary
        assert "resonance_baseline" in summary
        assert "multi_seed_analysis" in summary
        assert summary["pipeline_version"] == "1.2.1"
        assert set(summary["morphologies"]) == set(MORPHOLOGY_MODES)

        deriv = summary["parameter_derivation"]
        assert deriv["f_target_hz"] == 12.5
        assert deriv["f_check_hz"] == 12.5
        assert 1.5e-4 <= deriv["C_derived_F"] <= 1.7e-4


def test_resonance_config_integrity():
    with open(ROOT / "data" / "parameters.json") as f:
        data = json.load(f)

    freq = data["I_simulation_fixed_parameters"]["frequency_hz"]
    q = data["IV_network_performance_metrics"]["individual_q_factor"]
    radius = data["VI_experimental_sweep_parameters"]["connection_radius_m"]

    assert isinstance(freq, (int, float))
    assert isinstance(q, (int, float))
    assert isinstance(radius, (int, float))

    assert freq > 0
    assert q > 0
    assert radius > 0

    assert 0 < q < 100
    assert 1 < freq < 1e6
    assert 0 < radius <= 10.0

    assert "morphologies" in data["VIII_pipeline"]
    assert set(data["VIII_pipeline"]["morphologies"]) == set(MORPHOLOGY_MODES)


def test_conceptual_reference_values_are_separated():
    with open(ROOT / "data" / "parameters.json") as f:
        data = json.load(f)

    fixed = data["I_simulation_fixed_parameters"]
    assert "magnetic_permeability_ur" not in fixed, (
        "Unused reference value must not live in active parameter section I"
    )
    assert "resistivity_ohm_m" not in fixed

    ref = data["IX_conceptual_reference_values"]
    assert "magnetic_permeability_ur" in ref
    assert "resistivity_ohm_m" in ref