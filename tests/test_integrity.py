import os
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
    "data/inference_analysis.py",
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
            env={**os.environ, "PIPELINE_FAST": "1"},
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

        stat_csv       = tmp_path / "outputs/curve_separation_summary.csv"
        multi_csv      = tmp_path / "outputs/multi_seed_summary.csv"
        raw_csv        = tmp_path / "outputs/multi_seed_raw.csv"
        inference_csv  = tmp_path / "outputs/inference_summary.csv"
        summary_json   = tmp_path / "outputs/exploration_summary.json"
        robustness_csv = tmp_path / "outputs/robustness_matrix.csv"

        assert stat_csv.exists(),       "curve_separation_summary.csv missing"
        assert multi_csv.exists(),      "multi_seed_summary.csv missing"
        assert raw_csv.exists(),        "multi_seed_raw.csv missing"
        assert inference_csv.exists(),  "inference_summary.csv missing"
        assert summary_json.exists(),   "exploration_summary.json missing"
        assert robustness_csv.exists(), "robustness_matrix.csv missing"

        out_png  = tmp_path / "outputs/sensitivity_analysis.png"
        data_png = tmp_path / "data/sensitivity_analysis.png"
        assert out_png.exists(),  "sensitivity_analysis.png missing in outputs/"
        assert data_png.exists(), "sensitivity_analysis.png missing in data/"

        for mode in MORPHOLOGY_MODES:
            npz_path = tmp_path / f"outputs/af_tensors_{mode}.npz"
            assert npz_path.exists(), f"{mode} NPZ missing"
            with np.load(npz_path) as npz_data:
                assert "distance" in npz_data, f"{mode} NPZ missing 'distance' key"
                assert "af" in npz_data,       f"{mode} NPZ missing 'af' key"
                assert npz_data["af"].shape == (30, 200), (
                    f"{mode} NPZ 'af' shape expected (30, 200), "
                    f"got {npz_data['af'].shape}"
                )

        df_stat = pd.read_csv(stat_csv)
        required_stat_cols = [
            "Metric", "Pair", "t_statistic", "p_value",
            "Significant_p05", "Cohens_d", "Effect_size",
        ]
        for col in required_stat_cols:
            assert col in df_stat.columns, \
                f"Missing column in curve_separation_summary: {col}"

        n_modes = len(MORPHOLOGY_MODES)
        expected_pairs = n_modes * (n_modes - 1) // 2
        expected_rows  = 3 * expected_pairs
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

        df_raw = pd.read_csv(raw_csv)
        required_raw_cols = ["Morphology", "Seed", "Merit_Scaled", "Coherence_Ratio", "Peak_AF"]
        for col in required_raw_cols:
            assert col in df_raw.columns, f"Missing column in multi_seed_raw: {col}"
        assert len(df_raw) > 0, "multi_seed_raw.csv is empty"

        df_inf = pd.read_csv(inference_csv)
        required_inf_cols = [
            "Metric", "Pair", "N", "mean_diff",
            "CI_lower", "CI_upper", "Cohens_d",
            "p_raw", "p_holm", "Significant_holm", "power",
        ]
        for col in required_inf_cols:
            assert col in df_inf.columns, f"Missing column in inference_summary: {col}"
        assert len(df_inf) == expected_rows, (
            f"Expected {expected_rows} rows in inference_summary, got {len(df_inf)}"
        )

        with open(summary_json) as fj:
            summary = json.load(fj)

        assert "pipeline_version"           in summary
        assert "parameter_derivation"       in summary
        assert "resonance_baseline"         in summary
        assert "experimental_configuration" in summary
        assert "multi_seed_analysis"        in summary
        assert summary["pipeline_version"] == "1.2.4"
        assert set(summary["morphologies"]) == set(MORPHOLOGY_MODES)

        exp_cfg = summary["experimental_configuration"]
        assert "noise_level" in exp_cfg, \
            "noise_level missing from experimental_configuration"
        assert exp_cfg["noise_level"] == 0.15, \
            f"Expected noise_level=0.15, got {exp_cfg['noise_level']}"
        assert "noise_botanical" not in exp_cfg, \
            "Stale key 'noise_botanical' still present in experimental_configuration"

        deriv = summary["parameter_derivation"]
        assert deriv["f_target_hz"] == 12.5
        assert deriv["f_check_hz"]  == 12.5
        assert 1.5e-4 <= deriv["C_derived_F"] <= 1.7e-4

        df_rob = pd.read_csv(robustness_csv)
        required_rob_cols = [
            "k0_base", "beta_loss_factor", "Q_individual",
            "curve_sep_botanical_vs_random", "curve_sep_botanical_vs_fractal",
            "finding_holds",
        ]
        for col in required_rob_cols:
            assert col in df_rob.columns, \
                f"Missing column in robustness_matrix: {col}"

        expected_rob_rows = 8
        assert len(df_rob) == expected_rob_rows, (
            f"Expected {expected_rob_rows} rows in robustness_matrix (subprocess forces "
            f"PIPELINE_FAST=1, a 2x2x2 grid), got {len(df_rob)}"
        )
        n_holds = df_rob["finding_holds"].sum()
        assert n_holds / len(df_rob) >= 0.5, (
            f"Botanical separation holds in <50% of grid ({n_holds}/{len(df_rob)})"
        )


def test_resonance_config_integrity():
    with open(ROOT / "data" / "parameters.json") as f:
        data = json.load(f)

    freq   = data["I_simulation_fixed_parameters"]["frequency_hz"]
    q      = data["IV_network_performance_metrics"]["individual_q_factor"]
    radius = data["VI_experimental_sweep_parameters"]["connection_radius_m"]

    assert isinstance(freq,   (int, float))
    assert isinstance(q,      (int, float))
    assert isinstance(radius, (int, float))

    assert freq   > 0
    assert q      > 0
    assert radius > 0

    assert 0 < q      < 100
    assert 1 < freq   < 1e6
    assert 0 < radius <= 10.0

    assert "morphologies" in data["VIII_pipeline"]
    assert set(data["VIII_pipeline"]["morphologies"]) == set(MORPHOLOGY_MODES)

    sweep_cfg = data["VI_experimental_sweep_parameters"]
    assert "noise_level" in sweep_cfg, \
        "noise_level missing from VI_experimental_sweep_parameters"
    assert isinstance(sweep_cfg["noise_level"], (int, float)), \
        "noise_level must be a number"
    assert sweep_cfg["noise_level"] > 0, \
        "noise_level must be positive"

    assert "multi_seed_list" in sweep_cfg, \
        "multi_seed_list missing from VI_experimental_sweep_parameters"
    assert isinstance(sweep_cfg["multi_seed_list"], list), \
        "multi_seed_list must be a list"
    assert len(sweep_cfg["multi_seed_list"]) >= 2, \
        "multi_seed_list must contain at least 2 seeds"


def test_conceptual_reference_values_are_separated():
    with open(ROOT / "data" / "parameters.json") as f:
        data = json.load(f)

    fixed = data["I_simulation_fixed_parameters"]
    assert "magnetic_permeability_ur" not in fixed, \
        "Unused reference value must not live in active parameter section I"
    assert "resistivity_ohm_m" not in fixed

    ref = data["IX_conceptual_reference_values"]
    assert "magnetic_permeability_ur" in ref
    assert "resistivity_ohm_m"        in ref


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
                env={**os.environ, "PIPELINE_FAST": "1"},
            )
            assert r.returncode == 0, r.stderr

        _run()
        first = {}
        for mode in MORPHOLOGY_MODES:
            f = tmp_path / f"outputs/simulation_results_{mode}.csv"
            first[mode] = f.read_text()
        first_stat     = (tmp_path / "outputs/curve_separation_summary.csv").read_text()
        first_rob      = (tmp_path / "outputs/robustness_matrix.csv").read_text()
        first_raw      = (tmp_path / "outputs/multi_seed_raw.csv").read_text()
        first_inf      = (tmp_path / "outputs/inference_summary.csv").read_text()

        _run()
        for mode in MORPHOLOGY_MODES:
            f = tmp_path / f"outputs/simulation_results_{mode}.csv"
            assert f.read_text() == first[mode], (
                f"Non-deterministic simulation output: {mode}"
            )
        assert (tmp_path / "outputs/curve_separation_summary.csv").read_text() == first_stat, \
            "Non-deterministic curve_separation_summary.csv"
        assert (tmp_path / "outputs/robustness_matrix.csv").read_text() == first_rob, \
            "Non-deterministic robustness_matrix.csv"
        assert (tmp_path / "outputs/multi_seed_raw.csv").read_text() == first_raw, \
            "Non-deterministic multi_seed_raw.csv"
        assert (tmp_path / "outputs/inference_summary.csv").read_text() == first_inf, \
            "Non-deterministic inference_summary.csv"