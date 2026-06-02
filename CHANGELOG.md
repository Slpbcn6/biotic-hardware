# Changelog

## [1.1.0] - 2026-06-02

### Added
- Deterministic benchmarking pipeline in `run.py`
- Morphology switching system via `data/parameters.json`
- Dual-layer data architecture:
  - Scalar CSV contract (benchmark outputs)
  - Tensor NPZ layer (latent state preservation)
- Automated visualization pipeline via `plot_sensitivity.py`

### Changed
- Refactored `node_coupling.py` into a unidirectional computation pipeline:
  Morphology → Geometry → Array Factor → Coherence → Q_effective → Merit_scaled
- Centralized experimental configuration in `parameters.json`
- Improved separation between computation layer and output layer

### Removed
- Legacy unified output file `simulation_results.csv`

### Notes
- Version 1.1 defines a deterministic and reproducible benchmarking system
- The system is strictly computational and does not modify underlying model equations