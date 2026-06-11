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

ESSENTIAL_FILES = [
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
    "data/parametric_sweep.py",
    "data/stats_utils.py", 
]


def _copy_essential(tmp_path):
    for src in ESSENTIAL_FILES:
        dest = tmp_path / src
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / src, dest)


def test_morphological_divergence():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        _copy_essential(tmp_path)

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
        robustness_csv = tmp_path / "outputs/robustness_matrix.csv"

        assert stat_csv.exists(), "statistical_summary.csv missing"
        assert multi_csv.exists(), "multi_seed_summary.csv missing"
        assert summary_json.exists(), "exploration_summary.json missing"
        assert robustness_csv.exists(), "robustness_matrix.csv missing"

        out_png = tmp_path / "outputs/sensitivity_analysis.png"
        data_png = tmp_path / "data/sensitivity_analysis.png"
        assert out_png.exists(), "sensitivity_analysis.png missing in outputs/"
        assert data_png.exists(), "sensitivity_analysis.png missing in data/"

        for mode in MORPHOLOGY_MODES:
            npz_path = tmp_path / f"outputs/af_tensors_{mode}.npz"
            assert npz_path.exists(), f"{mode} NPZ missing"
            # Corrección: Uso de contexto 'with' para cerrar el descriptor de archivo
            with np.load(npz_path) as npz_data:
                assert "distance" in npz_data, f"{mode} NPZ missing 'distance' key"
                assert "af" in npz_data, f"{mode} NPZ missing 'af' key"
                assert npz_data["af"].shape == (30, 200), (
                    f"{mode} NPZ 'af' shape expected (30, 200), got {npz_data['af'].shape}"
                )

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
        assert summary["pipeline_version"] == "1.2.2"
        assert set(summary["morphologies"]) == set(MORPHOLOGY_MODES)

        exp_cfg = summary["experimental_configuration"]
        assert "noise_botanical" in exp_cfg, "noise_botanical missing from experimental_configuration"
        assert exp_cfg["noise_botanical"] == 0.15

        deriv = summary["parameter_derivation"]
        assert deriv["f_target_hz"] == 12.5
        assert deriv["f_check_hz"] == 12.5
        assert 1.5e-4 <= deriv["C_derived_F"] <= 1.7e-4

        df_rob = pd.read_csv(robustness_csv)
        required_rob_cols = [
            "k0_base", "beta_loss_factor", "Q_individual",
            "p_botanical_vs_random", "d_botanical_vs_random", "finding_holds",
        ]
        for col in required_rob_cols:
            assert col in df_rob.columns, f"Missing column in robustness_matrix: {col}"
        assert len(df_rob) == 48, (
            f"Expected 48 rows (4 k0 x 3 beta x 4 Q), got {len(df_rob)}"
        )
        n_holds = df_rob["finding_holds"].sum()
        assert n_holds / 48 >= 0.5, (
            f"Botanical separation holds in <50% of grid ({n_holds}/48)"
        )


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


def test_determinism():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        _copy_essential(tmp_path)

        def _run():
            out_dir = tmp_path / "outputs"
            if out_dir.exists():
                shutil.rmtree(out_dir)
            r = subprocess.run(
                [sys.executable, "run.py"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
            )
            assert r.returncode == 0, r.stderr

        _run()
        first = {}
        for mode in MORPHOLOGY_MODES:
            f = tmp_path / f"outputs/simulation_results_{mode}.csv"
            first[mode] = f.read_text()
        first_stat = (tmp_path / "outputs/statistical_summary.csv").read_text()
        first_rob = (tmp_path / "outputs/robustness_matrix.csv").read_text()

        _run()
        for mode in MORPHOLOGY_MODES:
            f = tmp_path / f"outputs/simulation_results_{mode}.csv"
            assert f.read_text() == first[mode], (
                f"Non-deterministic simulation output: {mode}"
            )
        assert (tmp_path / "outputs/statistical_summary.csv").read_text() == first_stat, (
            "Non-deterministic statistical_summary.csv"
        )
        assert (tmp_path / "outputs/robustness_matrix.csv").read_text() == first_rob, (
            "Non-deterministic robustness_matrix.csv"
        )