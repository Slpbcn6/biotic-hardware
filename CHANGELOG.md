# Changelog

## [1.1.0] - 2026-06-02

### Added
<<<<<<< HEAD

- Deterministic benchmarking pipeline in `run.py`
- Morphology switching system via `data/parameters.json`
- Multi-layer data architecture:
  - Scalar CSV contract (benchmark outputs)
  - Statistical NPZ layer (aggregated metrics)
  - Tensor NPZ layer (array factor field state)
- Automated visualization pipeline via `plot_sensitivity.py`

### Changed

- Refactored `node_coupling.py` into a deterministic morphology-conditioned pipeline:
  Morphology → Geometry → Array Factor → Coherence → Q_effective → Merit_scaled
  + Added dual output export (CSV + NPZ + AF tensors)
=======
- Deterministic benchmarking pipeline in `run.py`
- Morphology switching system via `data/parameters.json`
- Dual-layer data architecture:
  - Scalar CSV contract (benchmark outputs)
  - Tensor NPZ layer (latent state preservation)
- Automated visualization pipeline via `plot_sensitivity.py`

### Changed
- Refactored `node_coupling.py` into a unidirectional computation pipeline:
  Morphology → Geometry → Array Factor → Coherence → Q_effective → Merit_scaled
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f
- Centralized experimental configuration in `parameters.json`
- Improved separation between computation layer and output layer

### Removed
<<<<<<< HEAD

- Legacy unified output file `simulation_results.csv`

### Notes

- Version 1.1 defines a deterministic and reproducible benchmarking system
- The system preserves core resonance equations but allows deterministic morphological variation in spatial configuration
=======
- Legacy unified output file `simulation_results.csv`

### Notes
- Version 1.1 defines a deterministic and reproducible benchmarking system
- The system is strictly computational and does not modify underlying model equations
>>>>>>> 095aff2e377e7b34f157569668481023b770e39f
