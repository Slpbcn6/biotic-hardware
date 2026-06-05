# Overview: Biotic Hardware Synthesis (v1.1.2)

This repository provides a Python pipeline for simulating abstract coupled network dynamics, executing a deterministic morphological benchmarking sequence, and generating structured numerical outputs.

---

## Pipeline

The system executes a deterministic computational workflow for abstract complex-valued interference modeling over the angular domain across multiple structural inputs:

1. Parameter initialization and sequential morphology selection (`fractal` / `botanical` / `random`) injected directly into the coupling solver.
2. Geometric mapping and array factor computation for an array of N = 64 nodes under homotetic scaling.
3. Dual-layer data separation (Scalar CSV Benchmarking Contract & Tensor NPZ Research Layer).
4. Random control sweep: uniform random node placement (same N, same seed) as structural baseline.
5. Parametric sensitivity analysis and visualization across all three morphologies.

Run:

```bash
python run.py
```

---

## Data Architecture & Outputs

The pipeline separates computed metrics into two distinct operational layers:

### Scalar Layer (Benchmarking Contract)

- `data/simulation_results_fractal.csv`
- `data/simulation_results_botanical.csv`
- `data/simulation_results_random.csv`

### Tensor Layer (Research Layer)

- `data/af_tensors_fractal.npz`
- `data/af_tensors_botanical.npz`
- `data/af_tensors_random.npz`

### Visualization Artifacts

- `data/sensitivity_analysis.png`

---

## Key Result

The system produces consistent morphological divergence between fractal and botanical configurations under identical parameter constraints, and measures separation of both bio-inspired morphologies against a uniform random control (same N = 64, same seed, equivalent spatial extent).

![Sensitivity Analysis](./data/sensitivity_analysis.png)

Fractal and Random Control exhibit near-identical Merit Scaled trajectories, smooth, linear, and stable across the full distance range. Botanical diverges significantly, showing high variance in both Coherence and Merit. At this configuration, geometric structure does not differentiate Fractal from an unstructured baseline; the Botanical branching model is the primary source of behavioral divergence.

---

## Scope

This system is strictly computational.

It does not model or validate physical systems.

All behavior is confined to an abstract computational simulation space with no physical interpretation.

**Execution State Note:** The orchestrator (`run.py`) manages the benchmark sequentially by injecting morphology modes directly into the coupling solver. Each sweep is independent and side-effect-free; `data/parameters.json` is never mutated at runtime. Executing `data/node_coupling.py` independently outside of `run.py` will use the configuration state defined in the JSON file at that moment.

---

## Version

v1.1.2 introduces the automated Morphological Benchmark Pipeline, the dual-layer data model (CSV/NPZ), and acts as a frozen version for numerical reproducibility. The random control morphology (`generate_random_control`) is added as a structural baseline enabling falsifiable comparison between bio-inspired and unstructured topologies.