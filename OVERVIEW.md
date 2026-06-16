# Overview: Biotic Hardware Synthesis (v1.2.5)

## What this is

Biotic Hardware Synthesis is a deterministic, single-command Python framework that treats synthetic morphologies inspired by botanical branching patterns and natural plant geometry, plus geometric controls, as structured inputs, maps them into abstract coupled-oscillator and phased-array network models, and measures how their structure affects a set of coherence and merit metrics under continuous geometric scaling.

It is strictly a computational simulation. All electromagnetic vocabulary (resonance, array factor, beamforming, NFMI) is used as an analytical analogy; no physical, biological, or electromagnetic system is modeled, built, or implied.

This project originated from the visual study of botanical iconography in MS 408 (Voynich Manuscript). The manuscript is the historical starting point; the morphological generators and the benchmarking framework are independent of it.

## What it is for

The framework answers one question rigorously: does the geometry of a morphology produce a measurable, statistically separable signature in an abstract network model, and is that signature stable across random seeds? It is built for:

- reproducible morphological benchmarking — five morphologies, fixed seeds, pinned dependencies, single-command execution;
- formal statistical comparison (Welch t-test + Cohen's d) instead of visual inspection;
- falsifiability — an unstructured random control plus two synthetic controls (Fibonacci spiral, Voronoi) bound the result so structure can be distinguished from noise;
- external anchoring — the model's frequency regime is compared against published Schumann resonance modes (NOAA/GFZ Potsdam).

---

## Pipeline

The system executes a deterministic 12-step computational workflow for abstract complex-valued interference modeling over the angular domain across multiple structural inputs:

1. Parameter derivation — closed-form L/C derivation from the target frequency (f_target → L → C → f_check at 12.5 Hz), documenting the resonance configuration without altering the simulation.
2. Node-level resonance baseline and external Schumann resonance comparison (NOAA/GFZ Potsdam reference modes 1–5).
3. Fractal morphology sweep — geometry → pre-simulation topology validation (union-find with path-halving, minimum node count, degenerate-structure rejection) → array factor → coherence → merit.
4. Botanical morphology sweep — same pipeline as step 3.
5. Random control morphology sweep — same pipeline as step 3.
6. Fibonacci spiral morphology sweep (golden-angle 137.508°) — same pipeline as step 3.
7. Voronoi control morphology sweep — same pipeline as step 3. Invalid topologies are rejected before any sweep executes.
8. Curve-separation descriptors: Welch t-test + Cohen's d across 3 metrics × 10 morphology pairs on autocorrelated sweep steps (descriptive only — 30 rows).
9. Parametric sensitivity analysis and visualization across all five morphologies.
10. Multi-seed analysis (N=30 seeds, seeds 42–71 per morphology), producing mean ± std distributions and a machine-readable exploration summary.
11. Multi-seed classical inference: `data/inference_analysis.py` runs Welch t-test, Cohen's d, bootstrap CI, Holm-Bonferroni, and post-hoc power over the N=30 per-seed means. Morphologies with near-zero seed variance (fractal, Fibonacci) are flagged n/a to prevent variance-collapse artefacts. Output: `outputs/inference_summary.csv`.
12. Parametric robustness sweep: `data/parametric_sweep.py` runs botanical vs random vs fractal across a 5×5×5 grid of k0_base × beta_loss_factor × Q_individual (125 combinations), recording the curve-separation ratios at each point. Output: `outputs/robustness_matrix.csv`.

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
- `outputs/curve_separation_summary.csv` — Welch t-test + Cohen's d curve-separation descriptors across 3 metrics × 10 morphology pairs on autocorrelated sweep steps (descriptive only, not independent-sample tests).
- `outputs/multi_seed_summary.csv` — per-morphology mean ± std across N=30 seeds (seeds 42–71).
- `outputs/multi_seed_raw.csv` — per-seed means per morphology × metric; raw input to the inference step.
- `outputs/inference_summary.csv` — classical inference over N=30 per-seed means: Welch t-test, Cohen's d, bootstrap CI, Holm-corrected p, post-hoc power. Pairs involving a seed-frozen morphology are reported as n/a (variance collapse).
- `outputs/exploration_summary.json` — machine-readable record of parameter derivation, resonance baseline, experimental configuration, and multi-seed results per morphology.
- `outputs/robustness_matrix.csv` — parametric robustness grid: 125 combinations (5×5×5) of k0_base × beta_loss_factor × Q_individual; columns: k0_base, beta_loss_factor, Q_individual, curve_sep_botanical_vs_random, curve_sep_botanical_vs_fractal, finding_holds.

### Visualization Artifacts

- `outputs/sensitivity_analysis.png` — normalized sensitivity curves + statistical significance heatmaps (p-value and Cohen's d). Also committed at `data/sensitivity_analysis.png`.

---

## Key Results

Principal finding (v1.2.3): v1.2.3 distinguishes the descriptive single-seed curve-separation lens from the classical multi-seed inference. In the inference, fractal and Fibonacci are seed-frozen (per-seed std ≈ 0.0005), so every pair involving them is reported as **n/a** (18 of 30 pairs) rather than as a spurious large-effect finding. Of the 12 statistically valid pairs, **4 survive Holm–Bonferroni correction, all of them botanical separating from a stochastic control**: vs random and vs Voronoi on Merit_Scaled (d = −0.79, −1.05) and on Peak_AF (d = −0.86, −1.19), with post-hoc power 0.85–0.99. Botanical sits consistently below both stochastic controls.

Multi-seed analysis explains why the guard is required: botanical, random, and Voronoi carry seed-dependent variance (std ≈ 0.012–0.020), while fractal and Fibonacci are seed-stable (std ≈ 0.0005–0.0009). No claim is made about comparisons involving the seed-frozen morphologies. Merit_Scaled is an internal structural indicator within the abstract simulation space, not a physical performance measure.

Robustness finding (v1.2.3): botanical's curve separation from the random control holds in **100% of the 125-point k0 × beta × Q grid** (`outputs/robustness_matrix.csv`), with the botanical-vs-random separation ratio between 0.45 and 0.49 at every point. The finding is a structural property of botanical morphology, not a configuration artifact.

![Sensitivity Analysis](./data/sensitivity_analysis.png)

---

## Scope

This system is strictly computational. It does not model or validate physical systems. All behavior is confined to an abstract computational simulation space with no physical interpretation.

**Execution State Note:** The orchestrator (`run.py`) manages the benchmark sequentially by injecting morphology modes directly into the coupling solver. Each sweep is independent and side-effect-free; `data/parameters.json` is never mutated at runtime. Executing `data/node_coupling.py` independently outside of `run.py` will use the configuration state defined in the JSON file at that moment.

---

## Version History

v1.2.5 externalises `curve_separation_threshold` from a hardcoded literal in `data/parametric_sweep.py` into `data/parameters.json` section VI as the single source of truth; removes the unused `IX_conceptual_reference_values` section from `parameters.json`; moves the `BENCHMARK COMPLETE` banner in `run.py` to after the artifact listing with an artifact count; drops the corresponding integrity test (section IX no longer exists, 3 tests remain); and adds `tests/conftest.py` with an animated dot progress indicator that writes to `sys.stdout` to avoid  column corruption on Windows terminals.

v1.2.4 reframes the project documentation in terms of natural botanical branching patterns and geometric structural families. The historical origin of the project (visual study of MS 408 / Voynich Manuscript) is acknowledged in a closing note within each document's introductory section. No code, parameters, tests, or computational results are affected.

v1.2.3 adds a classical multi-seed inference step (`data/inference_analysis.py`: Welch t-test, Cohen's d, bootstrap CI, Holm-Bonferroni, post-hoc power over N=30 per-seed means) together with a variance-collapse guard that flags seed-frozen morphologies (fractal, Fibonacci) as `n/a` instead of reporting their inflated effect sizes as findings; raises the multi-seed count from 5 to 30 seeds (42–71); expands the robustness sweep to a full 5×5×5 = 125-point grid reporting curve-separation ratios; renames `statistical_summary.csv` to `curve_separation_summary.csv` to mark it as a descriptor rather than an independent-sample test; and externalizes the seed list to `parameters.json`. The net effect is that the only surviving statistical claims are botanical separating from the stochastic controls.

v1.2.2 corrects the noise regime from asymmetric (botanical only, σ=0.15; all others σ=0.0) to symmetric (`noise_level=0.15` applied identically to every morphology); externalizes `noise_level` to `parameters.json` section VI as the single source of truth; updates `exploration_summary.json` accordingly; adds parametric robustness analysis (`data/parametric_sweep.py`, 48-point grid, 100% of combinations confirm botanical separation at p<0.05); fixes the Cohen's d NaN artifact (pooled std < 1e-4 → `"n/a"`, |d| > 50 → `"extreme"`); and adds a full-pipeline determinism test. Under symmetric noise, Coherence_Ratio no longer produces extreme Cohen's d values — those were artifacts of near-zero fractal variance under asymmetric conditions.

v1.2.1 extended the morphological benchmark from three to five morphologies, adding two synthetic controls — a Fibonacci spiral (golden-angle 137.508°) and a Voronoi vertex distribution — widening the statistical comparison to 3 metrics × 10 pairs (30 rows). Added closed-form parameter derivation, centralized outputs to `outputs/`, replaced the custom Welch t-test with `scipy.stats.ttest_ind(equal_var=False)`, vectorized the array-factor computation, and added weekly Dependabot monitoring.