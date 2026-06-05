# Changelog

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