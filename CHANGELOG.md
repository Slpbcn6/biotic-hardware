# Changelog

## [1.2.6] - 2026-06-17

This is a hardening and cleanup release. No scientific result changes: the principal finding (botanical separating from both stochastic controls) is identical to v1.2.5. The release removes the resonance-baseline scaffolding that the simulation never consumed, adds a small-sample-corrected effect size and a second stochastic control to the robustness criterion, externalizes the last hardcoded statistical constant, and expands unit-test coverage.

### Removed

- **`data/parameter_derivation.py`, `data/node_resonance.py`, `data/schumann_reference.py`** (deleted): the analytic L/C derivation, the stored RLC resonance baseline, and the external Schumann mode comparison (NOAA/GFZ Potsdam, modes 1-5). These produced reference values (`f ≈ 12.5 Hz`, `f_res ≈ 12.99 Hz`, deviation 9.13% from mode 2) that were never inputs to the morphological benchmark; the coupling solver and statistics never read them. The pipeline drops from 12 to 10 steps.
- **`outputs/resonance_params.json`**: no longer produced (the modules that wrote it are gone).
- **`data/parameters.json`**: removed the fixed-parameter sections tied to the resonance derivation (target frequency, stored RLC). Section VI now also carries `variance_collapse_fraction` (see Changed).

### Added

- **`data/inference_analysis.py`**: `Hedges_g` column in `inference_summary.csv` — Cohen's d corrected by the small-sample factor `1 - 3 / (4 * df - 1)`, reported alongside Cohen's d for every valid pair.
- **`data/parametric_sweep.py`**: a Voronoi stochastic control generator and a `curve_sep_botanical_vs_voronoi` column in `robustness_matrix.csv`. `finding_holds` now requires botanical to separate from **both** the random and the Voronoi controls (each `abs(separation) >= curve_separation_threshold`) at every grid point, hardening the robustness claim against a second independent stochastic baseline.
- **`data/parameters.json` (section VI)**: `variance_collapse_fraction: 0.15` — externalizes the variance-collapse guard threshold that was previously a hardcoded constant in `inference_analysis.py`.
- **`tests/test_stats_utils.py`, `tests/test_input_generator.py`, `tests/test_topology_validator.py`** (new): focused unit tests for the effect-size and Holm/bootstrap/power helpers, the five morphology generators, and the union-find topology validator.
- **`results/`** (new): reference results from the maintainer's run — the deterministic CSV/JSON outputs behind the reported findings, committed so reviewers can read the numbers without running the pipeline and forks can diff their own `outputs/` against them; see `results/README.md`.

### Changed

- **`run.py`**: pipeline reduced to 10 steps (resonance derivation and Schumann comparison steps removed); `TOTAL_STEPS` and the step loop adjusted accordingly; `exploration_summary.json` now records experimental configuration and multi-seed results only (no parameter-derivation or resonance-baseline blocks), written with `ensure_ascii=False`.
- **`tests/test_integrity.py`**: `ESSENTIAL_FILES` trimmed to the surviving modules; asserts the `Hedges_g` and `curve_sep_botanical_vs_voronoi` columns and version `1.2.6`; the resonance-config integrity test is replaced by a config integrity test that no longer references the removed frequency parameter.
- **`README.md`, `OVERVIEW.md`, `docs/Morpho-Topological Framework and Parameter Space.md`, `notebook/demo.ipynb`, `CITATION.cff`**: updated to v1.2.6; the resonance/Schumann sections are removed or reclassified as conceptual reference only; Hedges' g and the Voronoi robustness control are documented.


## [1.2.5] - 2026-06-16

### Changed

- **`data/parameters.json`**: removed unused `IX_conceptual_reference_values` section (was never read by any module); added `curve_separation_threshold: 0.10` to section VI as single source of truth for the parametric sweep threshold.
- **`data/parametric_sweep.py`**: threshold read from `parameters.json` via `.get("curve_separation_threshold", 0.10)` instead of a hardcoded literal; log message now reflects the configured value dynamically.
- **`run.py`**: `BENCHMARK COMPLETE` banner moved to after the artifact listing, with artifact count (`N artifacts in outputs/ | all steps OK`).
- **`tests/test_integrity.py`**: removed `test_conceptual_reference_values_are_separated` (section IX no longer exists); 3 tests remain.

### Added

- **`tests/conftest.py`** (new): animated dot progress indicator for `pytest -v`; writes directly to `sys.stdout` to avoid corrupting pytest's column tracker and prevent `[NN%]` from wrapping to a new line on Windows terminals.


## [1.2.4] - 2026-06-16

### Changed

- **Documentation reframing:** the morphological taxonomy is now presented in terms of natural botanical branching patterns and geometric structural families, rather than with MS 408 as the primary analytical reference. The manuscript is acknowledged as the historical origin of the project in a closing note within each document's introductory section. No code, parameters, tests, or computational results are affected.
- **`assets/` header diagram (SVG):** updated to v1.2.4; revised tagline to botanical framing ("Does botanical branching produce a measurable topological signature?"); panel 03 retitled from "Matrix Map" to "Significance" with explicit Holm–Bonferroni framing and n/a count (18/30); panel 04 retitled from "Robustness" to "Inference" with per-metric effect sizes and power.


## [1.2.3] - 2026-06-14

### Fixed

- **Variance-collapse guard in multi-seed inference** (`data/inference_analysis.py`): the fractal and Fibonacci morphologies are seed-frozen (their generators ignore the seed), so their per-seed standard deviation is ~0.0005 — roughly two orders of magnitude below the seed-variable morphologies. Cohen's d divides by the pooled standard deviation, so any multi-seed comparison involving a seed-frozen morphology produced spurious, astronomically large effect sizes (|d| up to ~26) and false "significance". v1.2.3 detects this: for each metric, a morphology whose per-seed std is below `VARIANCE_FRACTION` (0.15) of the median per-morphology std is treated as degenerate. Every pair involving a degenerate morphology is written to `inference_summary.csv` as `n/a` (Cohen's d, p, power all `n/a`), a console WARNING is printed, and Holm-Bonferroni correction is applied only across the statistically valid pairs. This removes the variance-collapse artefacts that v1.2.2 reported as findings.
- **Parametric robustness sweep schema** (`data/parametric_sweep.py`): the previous implementation decided `finding_holds` from a Welch t-test p-value computed on 30 autocorrelated sweep steps, which is not a valid significance test. The p-value column has been removed entirely. `finding_holds = True` now means the botanical-vs-random curve-separation ratio `(mean(botanical) - mean(random)) / |mean(random)| >= 0.10`. The grid is expanded to the full 5x5x5 = 125 combinations.
- **`data/multi_seed_analysis.py`**: standard deviation now computed with `ddof=1` (sample std), correcting the previous population std (`ddof=0`).
- **`run.py`**: `pipeline_version` and `seeds` read from `parameters.json` (`VIII_pipeline.version`, `VI_experimental_sweep_parameters.multi_seed_list`) instead of being hardcoded; the stale `SEEDS` import from `multi_seed_analysis.py` is removed. The pipeline header version string and seed range are now dynamic.

### Added

- **`data/inference_analysis.py`** (new module): classical statistical inference over N=30 i.i.d. per-seed means. For each metric x morphology pair: Welch t-test, Cohen's d, bootstrap CI (95%, N=10000 iterations, seed=0), post-hoc power (non-central t). The variance-collapse guard (see Fixed) flags degenerate morphologies as `n/a`; Holm-Bonferroni correction runs across the valid pairs only. Output: `outputs/inference_summary.csv` (columns: Metric, Pair, N, mean_diff, CI_lower, CI_upper, Cohens_d, p_raw, p_holm, Significant_holm, power).
- **`data/stats_utils.py`**: four new functions — `holm_correction(p_values)` (manual Holm-Bonferroni), `bootstrap_ci(a, b, n_bootstrap, ci, seed)` (percentile bootstrap on the mean difference), `power_from_d(d, n, alpha)` (post-hoc power via scipy non-central t), and `near_zero_variance(group_std, reference_std, fraction)` (returns True when a group's std falls below `fraction x reference_std`, the test that drives the variance-collapse guard).
- **`data/parameters.json` (section VI)**: `multi_seed_list` — 30 consecutive seeds [42-71], single source of truth for the seed sequence.
- **`outputs/multi_seed_raw.csv`** (new output): per-seed means for every morphology x metric (columns: Morphology, Seed, Merit_Scaled, Coherence_Ratio, Peak_AF). The raw material consumed by `inference_analysis.py`.
- **`outputs/inference_summary.csv`** (new output): full inference results with the variance-collapse guard, Holm correction, and bootstrap CI.
- **`run.py`**: pipeline extended from 11 to 12 steps. Step 11 is the inference analysis; the parametric robustness sweep moves to step 12.
- **`tests/test_integrity.py`**: assertions for `multi_seed_raw.csv` and `inference_summary.csv`; `robustness_matrix.csv` assertions updated for the new `curve_sep_botanical_vs_random` / `curve_sep_botanical_vs_fractal` columns and the 125-point grid (8 in `PIPELINE_FAST`); version assertion `"1.2.3"`.
- **`.github/workflows/ci.yml`**: `PIPELINE_FAST: "1"` added to the test step.

### Changed

- **`outputs/statistical_summary.csv` -> `outputs/curve_separation_summary.csv`**: renamed to make explicit that these Welch values operate on autocorrelated sweep steps and are curve-separation descriptors, not independent-sample tests.
- **`data/multi_seed_analysis.py`**: seeds read from `parameters.json`; `PIPELINE_FAST=1` uses the first 2 seeds; results dict includes a `"values"` key (per-seed means); `multi_seed_raw.csv` written alongside `multi_seed_summary.csv`.
- **`data/parametric_sweep.py`**: full 5x5x5 = 125 grid (`PIPELINE_FAST=1` uses 2x2x2 = 8); CSV columns are `k0_base, beta_loss_factor, Q_individual, curve_sep_botanical_vs_random, curve_sep_botanical_vs_fractal, finding_holds`. The former p-value / Cohen's d columns are removed.
- **`data/plot_sensitivity.py`**: reads `curve_separation_summary.csv`; titles bumped to v1.2.3.
- **`data/parameters.json`**: `source_document` note and `VIII_pipeline.version` bumped to v1.2.3.
- **`CITATION.cff`**: version 1.2.3, date-released 2026-06-14.

### Scientific results (v1.2.3 - N=30 seeds, seeds 42-71)

**Inference (N=30 per-seed means, Welch t-test, Holm-Bonferroni over valid pairs):**

Of the 30 metric x pair combinations, 18 involve a seed-frozen morphology (fractal or
Fibonacci) and are reported as **n/a** (variance collapse). Of the 12 statistically valid
pairs, **4 are significant after Holm correction** — and all four are botanical separating
from a stochastic control, on Merit_Scaled and Peak_AF:

| Metric | Pair | mean diff | CI 95% | Cohen's d | p_holm | sig | power |
|---|---|---|---|---|---|---|---|
| Merit_Scaled | Botanical vs Random | -0.0096 | [-0.0156, -0.0037] | -0.788 | 0.031 | yes | 0.851 |
| Merit_Scaled | Botanical vs Voronoi | -0.0172 | [-0.0252, -0.0093] | -1.053 | 0.002 | yes | 0.980 |
| Merit_Scaled | Random vs Voronoi | -0.0076 | [-0.0159, +0.0006] | -0.456 | 0.584 | no | 0.412 |
| Coherence_Ratio | Botanical vs Random | -0.0012 | [-0.0530, +0.0517] | -0.012 | 1.000 | no | 0.050 |
| Coherence_Ratio | Botanical vs Fibonacci | +0.0143 | [-0.0174, +0.0459] | 0.228 | 1.000 | no | 0.140 |
| Coherence_Ratio | Botanical vs Voronoi | +0.0348 | [-0.0206, +0.0895] | 0.309 | 1.000 | no | 0.218 |
| Coherence_Ratio | Random vs Fibonacci | +0.0155 | [-0.0318, +0.0575] | 0.170 | 1.000 | no | 0.099 |
| Coherence_Ratio | Random vs Voronoi | +0.0360 | [-0.0283, +0.0993] | 0.275 | 1.000 | no | 0.183 |
| Coherence_Ratio | Fibonacci vs Voronoi | +0.0204 | [-0.0276, +0.0702] | 0.206 | 1.000 | no | 0.123 |
| Peak_AF | Botanical vs Random | -0.0099 | [-0.0155, -0.0042] | -0.861 | 0.015 | yes | 0.906 |
| Peak_AF | Botanical vs Voronoi | -0.0191 | [-0.0270, -0.0112] | -1.186 | <0.001 | yes | 0.995 |
| Peak_AF | Random vs Voronoi | -0.0091 | [-0.0171, -0.0011] | -0.569 | 0.261 | no | 0.582 |

The remaining 18 pairs (every pair containing fractal or Fibonacci) are `n/a`: their
per-seed variance is too small for a meaningful standardized effect size. Botanical sits
consistently below both stochastic controls (random, Voronoi); no claim is made about the
seed-frozen morphologies.

**Multi-seed means (N=30 seeds, seeds 42-71):**

| Morphology | Merit mean | Merit std | Coherence mean | Coherence std | Peak_AF mean | Peak_AF std |
|---|---|---|---|---|---|---|
| fractal | 0.0221 | 0.0005 | 1.1131 | 0.0104 | 0.0295 | 0.0007 |
| botanical | 0.0274 | 0.0119 | 1.4321 | 0.0821 | 0.0282 | 0.0116 |
| random | 0.0371 | 0.0125 | 1.4333 | 0.1250 | 0.0382 | 0.0115 |
| fibonacci | 0.0091 | 0.0008 | 1.4178 | 0.0340 | 0.0095 | 0.0009 |
| voronoi | 0.0446 | 0.0198 | 1.3973 | 0.1360 | 0.0473 | 0.0195 |

Fractal and Fibonacci are seed-stable (Merit std ~0.0005-0.0008); botanical, random, and
Voronoi are seed-sensitive (std ~0.012-0.020). This is exactly why the variance-collapse
guard is required for the inference step.

**Parametric robustness (curve_sep_botanical_vs_random >= 0.10):**

125/125 grid points hold (100%). The botanical-vs-random separation ratio ranges
0.4527-0.4937 across the full 5x5x5 k0 x beta x Q grid; the botanical-vs-fractal ratio
ranges 0.3387-0.3648. The separation of botanical from the random control is a structural
property of botanical morphology, robust across the entire parameter grid.


## [1.2.2] - 2026-06-11

### Fixed

- **Symmetric noise regime** (`data/node_coupling.py`, `data/parametric_sweep.py`): the previous implementation applied Gaussian perturbation (σ=0.15) exclusively to the `botanical` morphology while all other morphologies ran with `noise=0.0`. This asymmetry biased every comparison involving botanical. The parameter has been renamed `noise_level` and is now applied identically to every morphology at every sweep step. No conditional branch on mode remains in the codebase.
- `data/parameters.json`: `noise_botanical` removed; `noise_level: 0.15` added to section VI with a note documenting its symmetric application. `parameters.json` is now the single source of truth for this value.
- `data/parametric_sweep.py`: internal variable renamed from `noise_botanical` to `noise_level` for consistency with `node_coupling.py` and `parameters.json`.
- `run.py` (`write_exploration_summary`): `experimental_configuration` block now logs `noise_level` instead of `noise_botanical`.
- `run.py`: import of `K0_GRID`, `BETA_GRID`, `Q_GRID` moved before the step label that references them to prevent `UnboundLocalError`.
- `tests/test_integrity.py`: assertion updated to check for `noise_level` in `experimental_configuration`; additional negative assertion verifies that the stale key `noise_botanical` is no longer present. `test_resonance_config_integrity` now asserts `noise_level` is present and positive in section VI.

### Added

- `data/parametric_sweep.py`: parametric robustness sweep across a 4×3×4 grid of `k0_base` [0.002, 0.004, 0.006, 0.008] × `beta_loss_factor` [0.1, 0.25, 0.4] × `Q_individual` [0.5, 0.8, 1.5, 3.0] (48 combinations). For each combination, runs botanical vs random, computes Welch t-test + Cohen's d on Merit_Scaled, and records whether botanical separation holds at p < 0.05. Output: `outputs/robustness_matrix.csv`.
- `tests/test_integrity.py`: `test_determinism()` — runs the full pipeline twice from identical state and asserts all simulation CSVs, statistical summary, and robustness matrix are bit-for-bit identical across runs.

### Changed

- `data/node_coupling.py`: reads `noise_level` from `parameters.json` section VI (defaults to 0.15 if key absent); applies it to all morphologies unconditionally.
- `run.py`: version string `v1.2.2`; pipeline extends to 11 steps with the parametric robustness sweep as step 11.
- `CITATION.cff`: version bumped to 1.2.2, date-released 2026-06-11.

### Scientific results (post symmetric-noise fix — seed 42, N=64)

**Merit_Scaled:**

| Pair | p | Cohen's d | Effect |
|---|---|---|---|
| Fractal vs Botanical | 0.0259 | −0.593 | medium |
| Fractal vs Random | 0.4837 | 0.182 | n.s. |
| Fractal vs Fibonacci | <0.001 | 1.505 | large |
| Fractal vs Voronoi | <0.001 | −1.752 | large |
| Botanical vs Random | 0.0078 | 0.714 | medium |
| Botanical vs Fibonacci | <0.001 | 1.750 | large |
| Botanical vs Voronoi | <0.001 | −1.373 | large |
| Random vs Fibonacci | <0.001 | 1.139 | large |
| Random vs Voronoi | <0.001 | −1.809 | large |
| Fibonacci vs Voronoi | <0.001 | −2.322 | large |

9 of 10 pairs significant; only Fractal vs Random non-significant (p=0.484, d=0.182).
Botanical vs Fractal: medium effect (d=−0.593, down from large d=−0.843 under asymmetric
noise). Botanical vs Random: medium effect (d=0.714, down from large d=0.825). The
reduction in effect size is expected: the previous advantage was partly an artifact of
unperturbed comparison morphologies. The separation persists under fair conditions.

**Parametric robustness (48/48, 100%):** botanical separation from random holds at p<0.05
across all 48 combinations of the k0 × beta × Q grid. Cohen's d range: 0.6421–0.8398
(all medium-to-large). p range: 0.0020–0.0160. The finding is a structural property of
botanical morphology, not a configuration artifact.

**Coherence_Ratio:** 8 of 10 pairs significant. Two pairs are not significant under
symmetric noise: Botanical vs Fibonacci (p=0.324, d=0.258, small) and Random vs Voronoi
(p=0.177, d=0.354, small). Of the 8 significant pairs, all carry large effect sizes
(max |d|=8.926, Fractal vs Voronoi). No extreme values remain — the previously reported
|d|=1398.713 was an artifact of near-zero within-group variance in fractal under
asymmetric noise (fractal ran with noise=0.0). Under symmetric noise all morphologies
carry comparable variance and all effect sizes are interpretable.

**Multi-seed (seeds 42–46):**

| Morphology | Merit mean | Merit std | Coherence mean | Coherence std |
|---|---|---|---|---|
| fractal | 0.0222 | 0.0005 | 1.1051 | 0.0076 |
| botanical | 0.0285 | 0.0106 | 1.4175 | 0.1058 |
| random | 0.0327 | 0.0073 | 1.5188 | 0.0266 |
| fibonacci | 0.0089 | 0.0009 | 1.4292 | 0.0320 |
| voronoi | 0.0575 | 0.0119 | 1.4101 | 0.1398 |

Voronoi highest (0.0575), Fibonacci lowest (0.0089). Fractal and Fibonacci seed-stable
(std ≈ 0.0005–0.0009); botanical, random, and Voronoi seed-sensitive (std ≈ 0.007–0.012).

---

## [1.2.1] - 2026-06-09

### Added

- `data/input_generator.py`: two control morphologies - `generate_fibonacci_spiral()` (golden-angle 137.508 deg) and `generate_voronoi_control()` (scipy Voronoi vertex sampling).
- `data/config.py`: centralized output paths and the morphology list (read from `parameters.json`).
- `data/parameter_derivation.py`: auditable L/C derivation documenting the f_target -> L -> C -> f_res chain (12.5 Hz); documentation only, does not alter the simulation.
- `.github/dependabot.yml`: weekly Dependabot monitoring for `pip` and `github-actions`.
- `data/parameters.json`: `VIII_pipeline` metadata (version + morphologies) and an `IX_conceptual_reference_values` section.

### Changed

- Output layout: all generated artifacts now write to `outputs/` instead of `data/`; `sensitivity_analysis.png` is also written to `data/`.
- Morphology list and statistical pairs are derived dynamically; removed the duplicated `MORPHOLOGY_MODES` literals and the hardcoded `/7` step counter.
- `run.py`: statistical summary now runs before the sensitivity plot, restoring the full 3-panel figure; pairs generated via `itertools.combinations`; custom `_welch_t()` replaced by `scipy.stats.ttest_ind(equal_var=False)`.
- `data/node_coupling.py`: vectorized `compute_array_factor()`; topology validation moved into `run_sweep()` (reads `connection_radius_m`); removed the redundant `simulation_results_*.npz` write.
- `data/parameters.json`: removed dead `morphology_mode`; added `connection_radius_m`; moved the unused `magnetic_permeability_ur` and `resistivity_ohm_m` out of section I into `IX_conceptual_reference_values`.
- `data/schumann_reference.py`: removed a latent `np` reference (numpy was never imported).
- `tests/test_integrity.py`: updated for the `outputs/` layout and v1.2.1 pipeline metadata.
- `requirements.txt`: added `scipy`; pinned `pytest`.
- `.github/workflows/ci.yml`: pinned actions to commit SHAs; removed the duplicate standalone pipeline run.
- `LICENSE`: replaced 15-line summary with official CC BY 4.0 legalcode — GitHub now recognizes license automatically.

### Scientific results

- Merit_Scaled (seed 42, N=64): 9 of 10 pairs significant; only Fractal vs Random not significant (p=0.938, d=-0.020). Botanical vs Fractal p=0.002, d=-0.843 (large); Botanical vs Random p=0.002, d=0.825 (large). Voronoi and Fibonacci each separate from every other morphology with large effect (|d|>1.4).
- Coherence_Ratio: all 10 pairs statistically significant with large effect sizes.
- Peak_AF: 9 of 10 pairs significant; only Fractal vs Botanical not significant (p=0.457, d=-0.194). Botanical vs Random p=0.001, d=0.913 (large); Fractal vs Random p=0.005, d=0.764 (medium).
- Multi-seed (seeds 42-46): Voronoi highest Merit_Scaled (mean 0.0567, std 0.0117) and Fibonacci lowest (0.0070, std 0.0006); botanical and random seed-sensitive (std ~0.008-0.011), fractal and fibonacci seed-stable (std ~0.0006).
- Scope: `Merit_Scaled` is an internal structural indicator within the abstract simulation space, not a physical performance metric; figures describe this metric only, not general properties of the geometries.

## [1.2.0] - 2026-06-08

### Added

- `data/topology_validator.py`: pre-simulation morphology validation with union-find with path-halving, minimum node count, degenerate structure detection, and maximum nearest-neighbor distance reporting. Invalid topologies are rejected before any sweep executes.
- `data/schumann_reference.py`: external ELF baseline comparison against published Schumann resonance modes (NOAA/GFZ Potsdam). Simulated 12.9949 Hz positioned at   9.13% deviation from mode 2 (14.30 Hz). Cites Schumann 1952, Williams 1992, Nickolaenko & Hayakawa 2002.
- `data/multi_seed_analysis.py`: multi-seed sensitivity analysis across seeds [42–46] per morphology — transforms single-point results into mean +/- std distributions.
- `data/exploration_summary.json` (pipeline output): machine-readable record of resonance baseline, experimental configuration, and multi-seed results per morphology.  Satisfies roadmap exploration_summary.json contract.
- `data/statistical_summary.csv` (pipeline output): Welch t-test + Cohen d across 3 metrics (Merit_Scaled, Coherence_Ratio, Peak_AF) × 3 morphology pairs = 9 rows.
- `data/multi_seed_summary.csv` (pipeline output): per-morphology mean +/- std across 5 seeds for all three metrics.
- `.github/workflows/ci.yml`: CI pipeline executing full run.py + pytest on every push.

### Changed

- `run.py`: pipeline extended from 5 to 7 steps — topology validation per sweep, Schumann comparison after resonance baseline, statistical summary (3 metrics) and multi-seed analysis as terminal steps. All file reads use proper context managers.
- `data/node_coupling.py`: `run_sweep()` accepts optional `seed_override` parameter - backward-compatible, enables multi-seed execution without modifying parameters.json.
- `tests/test_integrity.py`: updated essential_files list to include all v1.2 modules; added assertions validating statistical_summary.csv (9 rows, 7 columns), multi_seed_summary.csv (3 rows), and exploration_summary.json schema.

### Scientific results

- Merit_Scaled: Botanical vs Fractal p=0.004, d=-0.843 (large); Botanical vs Random p=0.005, d=0.825 (large); Fractal vs Random p=1.000, d=-0.020 (not significant).
- Coherence_Ratio: all three pairs statistically significant with large effect sizes.
- Peak_AF: Botanical vs Random p=0.002, d=0.913 (large); Fractal vs Random p=0.009, d=0.764 (medium); Fractal vs Botanical not significant (p=0.913).
- Multi-seed confirms botanical Merit variance is structural (std 0.0106) vs fractal stability (std 0.0006). Fractal morphology does not separate from random control on Merit_Scaled — principal finding of v1.2.

## [1.1.2] - 2026-06-05

### Changed

- Fixed double-encoded author field in `data/parameters.json`  
- Moved hardcoded array factor constants (`k0_base`, `k_modulation_coeff`, `q_reference`) from `node_coupling.py` to `parameters.json` (section `VII_array_factor_parameters`)  
- Added `if __name__ == "__main__":` guard to `node_resonance.py` — module now importable without side effects  
- Removed `set_morphology()` from `run.py` — pipeline no longer mutates `parameters.json` during execution  
- Added per-sweep summary output to `run.py` (Peak AF, Coherence, Merit Scaled at max distance)  
- Fixed em dash rendering in `plot_sensitivity.py` labels (Windows matplotlib compatibility)  
- Pinned dependency versions in `requirements.txt`  
- Added cell `id` fields to `notebook/demo.ipynb` (nbformat 5.1.4+ compliance)  

---

## [1.1.1] - 2026-06-04

### Added

- `generate_random_control(n_nodes, seed)` in `data/input_generator.py`: uniform random node placement within equivalent spatial bounds as bio-inspired morphologies  
- Random control execution step in `run.py` (pipeline extends from 4 to 5 steps)  
- Random control outputs: `data/simulation_results_random.csv`, `data/af_tensors_random.npz`  
- Three-morphology comparison in `data/plot_sensitivity.py` (fractal / botanical / random control)  
- Interactive three-way comparison and statistical separation metrics in `notebook/demo.ipynb`  

### Purpose

Establishes a falsifiable structural baseline: bio-inspired morphologies (fractal, botanical) are now evaluated against an unstructured random topology of identical node count and seed. This constitutes the minimum control baseline required for comparative morphological analysis.

---

## [1.1.0] - 2026-06-02

### Added

- Deterministic benchmarking pipeline in `run.py`  
- Morphology switching system via `data/parameters.json`  
- Dual-layer data architecture:
  - Scalar CSV contract (benchmark outputs)
  - Tensor NPZ layer (latent state preservation)  
- Automated visualization pipeline via `plot_sensitivity.py`  

### Changed

- Refactored `node_coupling.py` into a deterministic morphology-conditioned pipeline:  
  Morphology → Geometry → Array Factor → Coherence → Q_effective → Merit_scaled  
- Centralized experimental configuration in `parameters.json`  
- Improved separation between computation layer and output layer  

### Removed

- Legacy unified output file `simulation_results.csv`  

### Notes

- Version 1.1 defines a deterministic and reproducible benchmarking system  
- The system preserves core resonance equations while enabling deterministic morphological variation in spatial configuration  
- The system is strictly computational and does not modify underlying model equations  
- The system remains fully deterministic; the introduction of the random control does not alter simulation equations or internal model behavior