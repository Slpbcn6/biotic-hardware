# Changelog

## [1.2.2] - 2026-06-11

### Fixed

- **Symmetric noise regime** (`data/node_coupling.py`, `data/parametric_sweep.py`):
  the previous implementation applied Gaussian perturbation (σ=0.15) exclusively to
  the `botanical` morphology while all other morphologies ran with `noise=0.0`. This
  asymmetry biased every comparison involving botanical. The parameter has been renamed
  `noise_level` and is now applied identically to every morphology at every sweep step.
  No conditional branch on mode remains in the codebase.
- `data/parameters.json`: `noise_botanical` removed; `noise_level: 0.15` added to
  section VI with a note documenting its symmetric application. `parameters.json` is
  now the single source of truth for this value.
- `data/parametric_sweep.py`: internal variable renamed from `noise_botanical` to
  `noise_level` for consistency with `node_coupling.py` and `parameters.json`.
- `run.py` (`write_exploration_summary`): `experimental_configuration` block now logs
  `noise_level` instead of `noise_botanical`.
- `run.py`: import of `K0_GRID`, `BETA_GRID`, `Q_GRID` moved before the step label
  that references them to prevent `UnboundLocalError`.
- `tests/test_integrity.py`: assertion updated to check for `noise_level` in
  `experimental_configuration`; additional negative assertion verifies that the stale
  key `noise_botanical` is no longer present. `test_resonance_config_integrity` now
  asserts `noise_level` is present and positive in section VI.

### Added

- `data/parametric_sweep.py`: parametric robustness sweep across a 4×3×4 grid of
  `k0_base` [0.002, 0.004, 0.006, 0.008] × `beta_loss_factor` [0.1, 0.25, 0.4] ×
  `Q_individual` [0.5, 0.8, 1.5, 3.0] (48 combinations). For each combination, runs
  botanical vs random, computes Welch t-test + Cohen's d on Merit_Scaled, and records
  whether botanical separation holds at p < 0.05. Output: `outputs/robustness_matrix.csv`.
- `tests/test_integrity.py`: `test_determinism()` — runs the full pipeline twice from
  identical state and asserts all simulation CSVs, statistical summary, and robustness
  matrix are bit-for-bit identical across runs.

### Changed

- `data/node_coupling.py`: reads `noise_level` from `parameters.json` section VI
  (defaults to 0.15 if key absent); applies it to all morphologies unconditionally.
- `run.py`: version string `v1.2.2`; pipeline extends to 11 steps with the parametric
  robustness sweep as step 11.
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

- `run.py`: pipeline extended from 5 to 7 steps — topology validation per sweep,
  Schumann comparison after resonance baseline, statistical summary (3 metrics) and
  multi-seed analysis as terminal steps. All file reads use proper context managers.
- `data/node_coupling.py`: `run_sweep()` accepts optional `seed_override` parameter —
  backward-compatible, enables multi-seed execution without modifying parameters.json.
- `tests/test_integrity.py`: updated essential_files list to include all v1.2 modules;
  added assertions validating statistical_summary.csv (9 rows, 7 columns),
  multi_seed_summary.csv (3 rows), and exploration_summary.json schema.

### Scientific results

- Merit_Scaled: Botanical vs Fractal p=0.004, d=-0.843 (large); Botanical vs Random
  p=0.005, d=0.825 (large); Fractal vs Random p=1.000, d=-0.020 (not significant).
- Coherence_Ratio: all three pairs statistically significant with large effect sizes.
- Peak_AF: Botanical vs Random p=0.002, d=0.913 (large); Fractal vs Random p=0.009,
  d=0.764 (medium); Fractal vs Botanical not significant (p=0.913).
- Multi-seed confirms botanical Merit variance is structural (std 0.0106) vs fractal
  stability (std 0.0006). Fractal morphology does not separate from random control
  on Merit_Scaled — principal finding of v1.2.

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