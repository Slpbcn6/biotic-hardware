# Overview: Biotic Hardware Synthesis (v1.2.0)

This repository provides a Python pipeline for simulating abstract coupled network dynamics, executing a deterministic morphological benchmarking sequence, and generating structured numerical outputs with full statistical validation.

---

## Pipeline

The system executes a deterministic 7-step computational workflow for abstract complex-valued interference modeling over the angular domain across multiple structural inputs:

1. Node-level resonance baseline and external Schumann resonance comparison (NOAA/GFZ Potsdam reference modes 1–5).
2. Pre-simulation topology validation per sweep — union-find connectivity (BFS), minimum node count, degenerate structure detection. Invalid topologies are rejected before any sweep executes.
3. Fractal morphology sweep: geometry → array factor → coherence → merit.
4. Botanical morphology sweep: same pipeline under branching-graph topology.
5. Random control sweep: uniform random node placement (same N = 64, same seed) as the structural baseline for falsifiable comparison.
6. Parametric sensitivity analysis and visualization across all three morphologies.
7. Statistical separation (Welch t-test + Cohen's d, 3 metrics × 3 pairs) and multi-seed analysis (seeds 42–46 per morphology), producing mean ± std distributions and a machine-readable exploration summary.

Run:

```bash
python run.py
```

---

## Data Architecture & Outputs

The pipeline separates computed metrics into two operational layers and produces additional statistical artifacts.

### Scalar Layer (Benchmarking Contract)

- `data/simulation_results_fractal.csv`
- `data/simulation_results_botanical.csv`
- `data/simulation_results_random.csv`

### Tensor Layer (Research Layer)

- `data/af_tensors_fractal.npz`
- `data/af_tensors_botanical.npz`
- `data/af_tensors_random.npz`

### Statistical Outputs

- `data/statistical_summary.csv` — Welch t-test + Cohen's d across 3 metrics × 3 morphology pairs (9 rows × 7 columns).
- `data/multi_seed_summary.csv` — per-morphology mean ± std across seeds 42–46.
- `data/exploration_summary.json` — machine-readable record of resonance baseline, experimental configuration, and multi-seed results per morphology.

### Visualization Artifacts

- `data/sensitivity_analysis.png` — normalized sensitivity curves + statistical significance heatmaps (p-value and Cohen's d).

---

## Key Result

Principal finding of v1.2: **botanical morphology achieves statistically significant separation from both fractal (p = 0.004, d = −0.843, large effect) and random control (p = 0.005, d = 0.825, large effect) on Merit_Scaled. Fractal morphology does not separate from the random control (p = 1.000, d = −0.020, not significant).**

Multi-seed analysis confirms this finding is structural: botanical Merit_Scaled exhibits seed-dependent variance (std = 0.0106), while fractal is seed-stable (std = 0.0006). The botanical branching model is the primary source of behavioral divergence; geometric structure alone does not differentiate fractal from an unstructured baseline at this configuration.

![Sensitivity Analysis](./data/sensitivity_analysis.png)

---

## Scope

This system is strictly computational. It does not model or validate physical systems. All behavior is confined to an abstract computational simulation space with no physical interpretation.

**Execution State Note:** The orchestrator (`run.py`) manages the benchmark sequentially by injecting morphology modes directly into the coupling solver. Each sweep is independent and side-effect-free; `data/parameters.json` is never mutated at runtime. Executing `data/node_coupling.py` independently outside of `run.py` will use the configuration state defined in the JSON file at that moment.

---

## Version

v1.2.0 introduces pre-simulation topology validation, an external Schumann resonance baseline (NOAA/GFZ Potsdam), formal statistical separation testing (Welch t-test + Cohen's d), multi-seed sensitivity distributions (seeds 42–46), a CI/CD pipeline (`.github/workflows/ci.yml`), and a machine-readable exploration summary (`data/exploration_summary.json`). The standard CC BY 4.0 license replaces the previous non-standard text. All results are reproducible via explicit seed tracking, pinned dependencies, and automated testing.
