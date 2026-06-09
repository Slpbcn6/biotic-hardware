# Overview: Biotic Hardware Synthesis (v1.2.1)

## What this is

Biotic Hardware Synthesis is a deterministic, single-command Python framework that treats morphological datasets — the MS 408 / Voynich Manuscript botanical iconography, plus synthetic geometric controls — as structured inputs, maps them into abstract coupled-oscillator and phased-array network models, and measures how their structure affects a set of coherence and merit metrics under continuous geometric scaling.

It is strictly a computational simulation. All electromagnetic vocabulary (resonance, array factor, beamforming, NFMI) is used as an analytical analogy; no physical, biological, or electromagnetic system is modeled, built, or implied.

## What it is for

The framework answers one question rigorously: does the geometry of a morphology produce a measurable, statistically separable signature in an abstract network model, and is that signature stable across random seeds? It is built for:

- reproducible morphological benchmarking — five morphologies, fixed seeds, pinned dependencies, single-command execution;
- formal statistical comparison (Welch t-test + Cohen's d) instead of visual inspection;
- falsifiability — an unstructured random control plus two synthetic controls (Fibonacci spiral, Voronoi) bound the result so structure can be distinguished from noise;
- external anchoring — the model's frequency regime is compared against published Schumann resonance modes (NOAA/GFZ Potsdam).

---

## Pipeline

The system executes a deterministic 10-step computational workflow for abstract complex-valued interference modeling over the angular domain across multiple structural inputs:

1. Parameter derivation — closed-form L/C derivation from the target frequency (f_target → L → C → f_check at 12.5 Hz), documenting the resonance configuration without altering the simulation.
2. Node-level resonance baseline and external Schumann resonance comparison (NOAA/GFZ Potsdam reference modes 1–5).
3–7. Five morphology sweeps — fractal, botanical, random control, Fibonacci spiral (golden-angle 137.508°), and Voronoi control. Each sweep runs: geometry → pre-simulation topology validation (union-find connectivity via BFS, minimum node count, degenerate-structure rejection) → array factor → coherence → merit. Invalid topologies are rejected before the sweep executes.
8. Statistical separation: Welch t-test + Cohen's d across 3 metrics × 10 morphology pairs (30 rows).
9. Parametric sensitivity analysis and visualization across all five morphologies.
10. Multi-seed analysis (seeds 42–46 per morphology), producing mean ± std distributions and a machine-readable exploration summary.

Run:

```bash
python run.py
```

---

## Data Architecture & Outputs

The pipeline separates computed metrics into two operational layers and produces additional statistical artifacts.

All generated artifacts are written to `outputs/` (regenerated on each run); `sensitivity_analysis.png` is additionally written to `data/`.

### Scalar Layer (Benchmarking Contract)

- `outputs/simulation_results_fractal.csv`
- `outputs/simulation_results_botanical.csv`
- `outputs/simulation_results_random.csv`
- `outputs/simulation_results_fibonacci.csv`
- `outputs/simulation_results_voronoi.csv`

### Tensor Layer (Research Layer)

- `outputs/af_tensors_fractal.npz`
- `outputs/af_tensors_botanical.npz`
- `outputs/af_tensors_random.npz`
- `outputs/af_tensors_fibonacci.npz`
- `outputs/af_tensors_voronoi.npz`

### Statistical Outputs

- `outputs/resonance_params.json` — node resonance baseline (simulated f_resonance and Q factor).
- `outputs/statistical_summary.csv` — Welch t-test + Cohen's d across 3 metrics × 10 morphology pairs (30 rows × 7 columns).
- `outputs/multi_seed_summary.csv` — per-morphology mean ± std across seeds 42–46.
- `outputs/exploration_summary.json` — machine-readable record of parameter derivation, resonance baseline, experimental configuration, and multi-seed results per morphology.

### Visualization Artifacts

- `outputs/sensitivity_analysis.png` — normalized sensitivity curves + statistical significance heatmaps (p-value and Cohen's d). Also committed at `data/sensitivity_analysis.png`.

---

## Key Result

Principal finding of v1.2.1: on Merit_Scaled, **9 of 10 morphology pairs separate at p < 0.05; the only non-significant pair is fractal vs random control (p = 0.938, d = −0.020).** The two synthetic controls bound the metric range — **Voronoi is highest (multi-seed mean 0.0567) and Fibonacci lowest (0.0070), each separating from every other morphology with large effect (|d| > 1.4).** Botanical separates from both fractal (p = 0.002, d = −0.843, large effect) and random control (p = 0.002, d = 0.825, large effect).

Multi-seed analysis confirms the result is structural: botanical, random, and Voronoi carry seed-dependent variance (std ≈ 0.008–0.012), while fractal and Fibonacci are seed-stable (std ≈ 0.0006). Geometric structure alone does not differentiate fractal from an unstructured baseline at this configuration; the measurable separations are driven by botanical branching and by the control vertex distributions. Merit_Scaled is an internal structural indicator within the abstract simulation space, not a physical performance measure.

![Sensitivity Analysis](./data/sensitivity_analysis.png)

---

## Scope

This system is strictly computational. It does not model or validate physical systems. All behavior is confined to an abstract computational simulation space with no physical interpretation.

**Execution State Note:** The orchestrator (`run.py`) manages the benchmark sequentially by injecting morphology modes directly into the coupling solver. Each sweep is independent and side-effect-free; `data/parameters.json` is never mutated at runtime. Executing `data/node_coupling.py` independently outside of `run.py` will use the configuration state defined in the JSON file at that moment.

---

## Version

v1.2.1 extends the morphological benchmark from three to five morphologies, adding two synthetic controls — a Fibonacci spiral (golden-angle 137.508°) and a Voronoi vertex distribution — which widen the statistical comparison to 3 metrics × 10 pairs (30 rows). It adds closed-form parameter derivation (`data/parameter_derivation.py`, documenting the f_target → L → C chain), centralizes output paths and the morphology list in `data/config.py`, relocates all generated artifacts to `outputs/` (with `sensitivity_analysis.png` also written to `data/`), replaces the custom Welch t-test with `scipy.stats.ttest_ind(equal_var=False)`, vectorizes the array-factor computation, and adds weekly Dependabot monitoring. All results remain reproducible via explicit seed tracking, pinned dependencies, and automated testing.