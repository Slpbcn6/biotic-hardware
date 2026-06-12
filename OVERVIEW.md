# Overview: Biotic Hardware Synthesis (v1.2.2)

## What this is

Biotic Hardware Synthesis is a deterministic, single-command Python framework that treats synthetic morphologies inspired by the MS 408 / Voynich Manuscript botanical iconography, plus geometric controls, as structured inputs, maps them into abstract coupled-oscillator and phased-array network models, and measures how their structure affects a set of coherence and merit metrics under continuous geometric scaling.

It is strictly a computational simulation. All electromagnetic vocabulary (resonance, array factor, beamforming, NFMI) is used as an analytical analogy; no physical, biological, or electromagnetic system is modeled, built, or implied.

## What it is for

The framework answers one question rigorously: does the geometry of a morphology produce a measurable, statistically separable signature in an abstract network model, and is that signature stable across random seeds? It is built for:

- reproducible morphological benchmarking — five morphologies, fixed seeds, pinned dependencies, single-command execution;
- formal statistical comparison (Welch t-test + Cohen's d) instead of visual inspection;
- falsifiability — an unstructured random control plus two synthetic controls (Fibonacci spiral, Voronoi) bound the result so structure can be distinguished from noise;
- external anchoring — the model's frequency regime is compared against published Schumann resonance modes (NOAA/GFZ Potsdam).

---

## Pipeline

The system executes a deterministic 11-step computational workflow for abstract complex-valued interference modeling over the angular domain across multiple structural inputs:

1. Parameter derivation — closed-form L/C derivation from the target frequency (f_target → L → C → f_check at 12.5 Hz), documenting the resonance configuration without altering the simulation.
2. Node-level resonance baseline and external Schumann resonance comparison (NOAA/GFZ Potsdam reference modes 1–5).
3–7. Five morphology sweeps — fractal, botanical, random control, Fibonacci spiral (golden-angle 137.508°), and Voronoi control. Each sweep runs: geometry → pre-simulation topology validation (union-find with path-halving, minimum node count, degenerate-structure rejection) → array factor → coherence → merit. Invalid topologies are rejected before the sweep executes.
8. Statistical separation: Welch t-test + Cohen's d across 3 metrics × 10 morphology pairs (30 rows).
9. Parametric sensitivity analysis and visualization across all five morphologies.
10. Multi-seed analysis (seeds 42–46 per morphology), producing mean ± std distributions and a machine-readable exploration summary.
11. Parametric robustness sweep: `data/parametric_sweep.py` runs botanical vs random across a 4×3×4 grid of k0_base × beta_loss_factor × Q_individual (48 combinations), recording p and Cohen's d at each point. Output: `outputs/robustness_matrix.csv`.

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
- `outputs/robustness_matrix.csv` — parametric robustness grid: 48 combinations of k0_base × beta_loss_factor × Q_individual; columns: k0_base, beta_loss_factor, Q_individual, p_botanical_vs_random, d_botanical_vs_random, finding_holds.

### Visualization Artifacts

- `outputs/sensitivity_analysis.png` — normalized sensitivity curves + statistical significance heatmaps (p-value and Cohen's d). Also committed at `data/sensitivity_analysis.png`.

---

## Key Results

Principal finding (v1.2.2, symmetric noise): on Merit_Scaled, **9 of 10 morphology pairs separate at p < 0.05; the sole non-significant pair is fractal vs random control (p = 0.484, d = 0.182).** The two synthetic controls bound the metric range — **Voronoi is highest (multi-seed mean 0.0575) and Fibonacci lowest (0.0089), each separating from every other morphology with large effect (|d| > 1.1).** Botanical separates from fractal (p = 0.026, d = −0.593, medium effect) and from random control (p = 0.008, d = 0.714, medium effect). Under the corrected symmetric noise regime (noise_level = 0.15 applied identically to all morphologies), botanical effect sizes are medium rather than large; the separation persists under fair comparison conditions, confirming it is a structural property of botanical morphology rather than an artifact of asymmetric perturbation.

Multi-seed analysis confirms the result is structural: botanical, random, and Voronoi carry seed-dependent variance (std ≈ 0.007–0.012), while fractal and Fibonacci are seed-stable (std ≈ 0.0005–0.0009). Geometric structure alone does not differentiate fractal from an unstructured baseline at this configuration; the measurable separations are driven by botanical branching and by the control vertex distributions. Merit_Scaled is an internal structural indicator within the abstract simulation space, not a physical performance measure.

Robustness finding (v1.2.2, symmetric noise): botanical separation holds at p < 0.05 in **100% of the 48-point k0 × beta × Q grid** (`outputs/robustness_matrix.csv`), with Cohen's d ranging from 0.642 to 0.840 (medium-to-large) across all combinations. The finding is a structural property of botanical morphology, not a configuration artifact.

![Sensitivity Analysis](./data/sensitivity_analysis.png)

---

## Scope

This system is strictly computational. It does not model or validate physical systems. All behavior is confined to an abstract computational simulation space with no physical interpretation.

**Execution State Note:** The orchestrator (`run.py`) manages the benchmark sequentially by injecting morphology modes directly into the coupling solver. Each sweep is independent and side-effect-free; `data/parameters.json` is never mutated at runtime. Executing `data/node_coupling.py` independently outside of `run.py` will use the configuration state defined in the JSON file at that moment.

---

## Version History

v1.2.2 corrects the noise regime from asymmetric (botanical only, σ=0.15; all others σ=0.0) to symmetric (`noise_level=0.15` applied identically to every morphology); externalizes `noise_level` to `parameters.json` section VI as the single source of truth; updates `exploration_summary.json` accordingly; adds parametric robustness analysis (`data/parametric_sweep.py`, 48-point grid, 100% of combinations confirm botanical separation at p<0.05); fixes the Cohen's d NaN artifact (pooled std < 1e-4 → `"n/a"`, |d| > 50 → `"extreme"`); and adds a full-pipeline determinism test. Under symmetric noise, Coherence_Ratio no longer produces extreme Cohen's d values — those were artifacts of near-zero fractal variance under asymmetric conditions.

v1.2.1 extended the morphological benchmark from three to five morphologies, adding two synthetic controls — a Fibonacci spiral (golden-angle 137.508°) and a Voronoi vertex distribution — widening the statistical comparison to 3 metrics × 10 pairs (30 rows). Added closed-form parameter derivation, centralized outputs to `outputs/`, replaced the custom Welch t-test with `scipy.stats.ttest_ind(equal_var=False)`, vectorized the array-factor computation, and added weekly Dependabot monitoring.