# Overview: Biotic Hardware Synthesis (v1.1)

This repository provides a Python pipeline for simulating abstract coupled network dynamics, executing a deterministic morphological benchmarking sequence, and generating structured numerical outputs.

---

## Pipeline
The system executes a stateful deterministic computational workflow for abstract complex-valued interference modeling over the angular domain across multiple structural inputs by mutating configuration parameters:

1. Parameter initialization and sequential morphology selection (`fractal` / `botanical`) via `data/parameters.json` mutation.
2. Geometric mapping and array factor computation for an array of $N = 64$ nodes under homotetic scaling.
3. Dual-layer data separation (Scalar CSV Benchmarking Contract & Tensor NPZ Research Layer).
4. Parametric sensitivity analysis and visualization.

Run:

```bash
python run.py
```

---

## Data Architecture & Outputs

The pipeline separates computed metrics into two distinct operational layers:

### 1. Scalar Layer (Benchmarking Contract)
- `data/simulation_results_fractal.csv`  
- `data/simulation_results_botanical.csv`  

### 2. Tensor Layer (Research Layer)
- `data/af_tensors_fractal.npz`  
- `data/af_tensors_botanical.npz`  

### 3. Visualization Artifacts
- `data/sensitivity_analysis.png`  

---

## Key Result

![Sensitivity Analysis](./data/sensitivity_analysis.png)

---

## Scope
This system is strictly computational.

It does not model or validate physical systems.

All behavior is confined to an abstract computational simulation space with no physical interpretation.

**Execution State Note:** The orchestrator (`run.py`) manages the benchmark sequentially by mutating `data/parameters.json` between runs. The architecture is stateful; executing `data/node_coupling.py` independently outside of `run.py` will yield results exclusively tied to the last configuration state preserved in the JSON file.

---

## Version
v1.1 introduces the automated Morphological Benchmark Pipeline, the dual-layer data model (CSV/NPZ), and acts as a frozen version for numerical reproducibility.