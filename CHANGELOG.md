# Changelog

## [1.2.0] - 2026-06-08

### Added

- `data/topology_validator.py`: pre-simulation morphology validation with union-find   connectivity check (BFS), minimum node count, degenerate structure detection, and   maximum nearest-neighbor distance reporting. Invalid topologies are rejected before   any sweep executes.
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
- `LICENSE`: replaced non-standard text with official CC BY 4.0 body — GitHub now
  recognizes license automatically.

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