# Overview: Biotic Hardware Synthesis (v1.3.0)

## What this is

Biotic Hardware Synthesis is a deterministic, single-command Python framework that treats synthetic morphologies inspired by botanical branching patterns and natural plant geometry, plus geometric controls, as structured inputs, maps them into abstract coupled-oscillator and phased-array network models, and measures how their structure affects a set of coherence and merit metrics under continuous geometric scaling.

It is strictly a computational simulation. All electromagnetic vocabulary (resonance, array factor, beamforming, NFMI) is used as an analytical analogy; no physical, biological, or electromagnetic system is modeled, built, or implied.

This project originated from the visual study of botanical iconography in MS 408 (Voynich Manuscript). The manuscript is the historical starting point; the morphological generators and the benchmarking framework are independent of it.

## What it is for

The framework answers one question rigorously: does the geometry of a morphology produce a measurable, statistically separable signature in an abstract network model, and is that signature stable across random seeds? It is built for:

- reproducible morphological benchmarking — ten morphologies, fixed seeds, pinned dependencies, single-command execution;
- formal statistical comparison (Welch t-test + Cohen's d, Hedges' g) instead of visual inspection;
- falsifiability — an unstructured random control plus eight synthetic controls (Fibonacci spiral, Voronoi, hexagonal lattice, DLA, Gaussian clusters, concentric rings, reticulate vein growth) bound the result so structure can be distinguished from noise across ordered, stochastic, and clustered extremes;
- a graph-topology lens that tests, with cross-validation, whether spectral structure predicts the merit metric across the morphology set.

---

## Pipeline

The system executes a deterministic 16-step computational workflow — ten morphology sweeps (steps 1–10) followed by six analysis stages (steps 11–16) — for abstract complex-valued interference modeling over the angular domain across multiple structural inputs. Each morphology sweep runs geometry → pre-simulation topology validation (union-find with path-halving, minimum node count, degenerate-structure rejection) → array factor → coherence → merit, and invalid topologies are rejected before any sweep executes. The Voronoi nodes are the finite Voronoi vertices of a uniform random seed set that fall within the domain bounds; if fewer than the target node count qualify, the remainder is filled with uniform random points, keeping the control a fixed-size, reproducible point set. Three morphologies (fractal, Fibonacci, hexagonal) are seed-frozen by construction; the other seven carry genuine seed variance. The full execution order is:

1. Fractal sweep
2. Botanical sweep
3. Random control sweep
4. Fibonacci spiral sweep
5. Voronoi control sweep
6. Hexagonal lattice sweep
7. Diffusion-limited aggregation (DLA) sweep
8. Gaussian clusters sweep
9. Concentric rings sweep
10. Reticulate vein growth sweep
11. Curve-separation descriptors: Welch t-test + Cohen's d across 3 metrics × 45 morphology pairs on autocorrelated sweep steps (descriptive only).
12. Multi-seed analysis (N=30 seeds, seeds 42–71 per morphology), producing mean ± std distributions and a machine-readable exploration summary.
13. Multi-seed classical inference: `data/inference_analysis.py` runs Welch t-test, Cohen's d, Hedges' g, bootstrap CI, Holm-Bonferroni, and post-hoc power over the N=30 per-seed means. Morphologies with near-zero seed variance (fractal, Fibonacci, hexagonal) are flagged n/a per metric to prevent variance-collapse artefacts. Output: `outputs/inference_summary.csv`.
14. Graph-topology analysis: `data/topology_analysis.py` builds per-morphology k-nearest-neighbour graphs (`data/graph_topology.py`), derives spectral descriptors (algebraic connectivity lambda_2, eigenratio R, clustering coefficient) over the 30 seeds, and tests three pre-specified topology-vs-merit hypotheses across the ten morphologies by Pearson correlation with leave-one-out cross-validation. Outputs: `outputs/graph_topology_summary.csv`, `outputs/topology_correlation.csv`.
15. Parametric sensitivity analysis and visualization across all ten morphologies.
16. Parametric robustness sweep: `data/parametric_sweep.py` runs botanical vs random vs fractal vs Voronoi across a 5×5×5 grid of k0_base × beta_loss_factor × Q_individual (125 combinations), recording the curve-separation ratios at each point. Output: `outputs/robustness_matrix.csv`.

Run:

```bash
python run.py
```

---

## Data Architecture & Outputs

The pipeline separates computed metrics into two operational layers and produces additional statistical artifacts.

All generated artifacts are written to `outputs/` (regenerated on each run); `sensitivity_analysis.png` is additionally written to `data/`.

### Scalar Layer (Benchmarking Contract)

One `outputs/simulation_results_<morphology>.csv` per morphology: `fractal`, `botanical`, `random`, `fibonacci`, `voronoi`, `hexagonal`, `dla`, `clusters`, `concentric`, `reticulate`.

### Tensor Layer (Research Layer)

One `outputs/af_tensors_<morphology>.npz` per morphology, for the same ten morphologies as the scalar layer.

### Statistical Outputs

- `outputs/curve_separation_summary.csv` — Welch t-test + Cohen's d curve-separation descriptors across 3 metrics × 10 morphology pairs on autocorrelated sweep steps (descriptive only, not independent-sample tests).
- `outputs/multi_seed_summary.csv` — per-morphology mean ± std across N=30 seeds (seeds 42–71).
- `outputs/multi_seed_raw.csv` — per-seed means per morphology × metric; raw input to the inference step.
- `outputs/inference_summary.csv` — classical inference over N=30 per-seed means: Welch t-test, Cohen's d, Hedges' g, bootstrap CI, Holm-corrected p, post-hoc power. Pairs involving a seed-frozen morphology are reported as n/a (variance collapse).
- `outputs/graph_topology_summary.csv` — per-morphology spectral and classical graph descriptors averaged over the 30 seeds (lambda_2, eigenratio R, clustering coefficient, mean degree, density, characteristic path length, mean merit), one row per morphology × k.
- `outputs/topology_correlation.csv` — H1/H2/H3 topology-vs-merit Pearson correlations across the ten morphologies, with p-value, leave-one-out cross-validation (mean/min/max r, sign stability), and the pre-specified |r| ≥ 0.632 threshold flag, at each k.
- `outputs/exploration_summary.json` — machine-readable record of experimental configuration and multi-seed results per morphology.
- `outputs/robustness_matrix.csv` — parametric robustness grid: 125 combinations (5×5×5) of k0_base × beta_loss_factor × Q_individual; columns: k0_base, beta_loss_factor, Q_individual, curve_sep_botanical_vs_random, curve_sep_botanical_vs_fractal, curve_sep_botanical_vs_voronoi, finding_holds (botanical separates from both random and Voronoi controls).

### Visualization Artifacts

- `outputs/sensitivity_analysis.png` — combined figure: sensitivity curves (Merit Scaled, Coherence Ratio, Peak AF), the Merit Scaled seed-distribution box plots, two topology-vs-merit scatter panels (primary k=6 and strongest-correlation k=3, both null), and the pairwise |Cohen's d| effect-size matrices. Also committed at `data/sensitivity_analysis.png`.

---

## Key Results

Principal finding: the benchmark distinguishes the descriptive single-seed curve-separation lens from the classical multi-seed inference. In the inference, three morphologies are seed-frozen (fractal, Fibonacci, hexagonal; per-seed std ≈ 0.0005–0.001), so on Merit_Scaled and Peak_AF every pair involving them is reported as **n/a** (24 of 45 pairs per metric; 9 of 45 on Coherence_Ratio, where only fractal collapses) rather than as a spurious large-effect finding. v1.3.0 grows the benchmark from five to ten morphologies, so Holm–Bonferroni now corrects across **21 valid pairs per metric**. Under this heavier burden, botanical still separates with Holm-corrected significance on both Merit_Scaled and Peak_AF: it sits **below the high-merit stochastic controls** — Voronoi (d = −1.05, −1.19) and reticulate vein growth (d = −1.04, −1.22) — and **above the low-merit regular controls** — Gaussian clusters (d = +1.64, +1.66) and concentric rings (d = +1.52, +1.57) — with post-hoc power 0.98–1.0. Botanical is no longer separable from the random control or DLA after the larger correction, so the claim is a robust mid-merit position between ordered and stochastic extremes, not a blanket "below all controls".

Topology finding (exploratory): the three pre-specified topology-vs-merit hypotheses (H1 eigenratio R, H2 algebraic connectivity lambda_2, H3 clustering coefficient) do **not** reach the pre-specified significance criterion (|r| ≥ 0.632 with p < 0.05) at any k. At the pre-specified primary resolution (k = 6, all N = 10 morphologies connected) the strongest, H2, gives r = −0.28 (p ≈ 0.43) — no linear structure-to-merit relationship. Across the robustness sweep (k = 3, 10, 15) the strongest correlation is at k = 3, where H2 reaches r = −0.66, exceeding the |r| bar but still failing significance (p ≈ 0.055, N = 9, one graph disconnects at k = 3). At N = 10 morphologies the spectral descriptors do not linearly predict merit; this is reported honestly as a null, and the graph-topology layer is provided so the hypothesis can be revisited with more morphologies.

Multi-seed analysis explains why the variance guard is required: the seven seed-variable morphologies carry seed-dependent variance while fractal, Fibonacci, and hexagonal are seed-stable. No claim is made about comparisons involving the seed-frozen morphologies. Merit_Scaled is an internal structural indicator within the abstract simulation space, not a physical performance measure.

Robustness finding: botanical's curve separation from the random control holds in **100% of the 125-point k0 × beta × Q grid** (`outputs/robustness_matrix.csv`), well above the 0.10 threshold at every point. The finding is a structural property of botanical morphology, not a configuration artifact.

![Sensitivity Analysis](./data/sensitivity_analysis.png)

---

## Scope

This system is strictly computational. It does not model or validate physical systems. All behavior is confined to an abstract computational simulation space with no physical interpretation.

**Execution State Note:** The orchestrator (`run.py`) manages the benchmark sequentially by injecting morphology modes directly into the coupling solver. Each sweep is independent and side-effect-free; `data/parameters.json` is never mutated at runtime. Executing `data/node_coupling.py` independently outside of `run.py` will use the configuration state defined in the JSON file at that moment.

---

## Version History

v1.3.0 doubles the benchmark from five morphologies to ten — adding a hexagonal lattice (seed-frozen), diffusion-limited aggregation (DLA), Gaussian clusters, concentric rings, and reticulate vein growth — and introduces a graph-topology layer. A new `data/graph_topology.py` builds k-nearest-neighbour graphs and computes spectral descriptors (algebraic connectivity lambda_2, eigenratio R, clustering coefficient) from the Laplacian eigenspectrum, with disconnected graphs reported as n/a rather than silent inf/NaN; `data/topology_analysis.py` aggregates these over the 30 seeds and tests three pre-specified topology-vs-merit hypotheses by Pearson correlation with leave-one-out cross-validation. The expansion more than triples the multiple-comparison burden (21 valid pairs per metric under Holm); the botanical Merit_Scaled and Peak_AF separation survives, now framed as a mid-merit position below the high-merit stochastic controls (Voronoi, reticulate) and above the low-merit regular controls (clusters, concentric). The topology-vs-merit correlations are an exploratory null at N = 10. New outputs: `graph_topology_summary.csv`, `topology_correlation.csv`. The licence changes from CC BY 4.0 to MIT.

v1.2.6 is a hardening and cleanup release with no change to the scientific result. It removes the resonance-baseline scaffolding (`data/node_resonance.py`, `data/schumann_reference.py`, `data/parameter_derivation.py`) and the corresponding Schumann external-comparison and L/C derivation steps, shortening the pipeline from 12 to 10 steps; the simulation never depended on those values. It adds a Hedges' g column (small-sample-corrected effect size) alongside Cohen's d in `inference_summary.csv`, extends the parametric robustness sweep so botanical separation must hold against both stochastic controls (random and Voronoi) at every grid point, externalises `variance_collapse_fraction` to `parameters.json` section VI, and adds focused unit tests for `stats_utils`, `input_generator`, and `topology_validator`.

v1.2.5 externalises `curve_separation_threshold` from a hardcoded literal in `data/parametric_sweep.py` into `data/parameters.json` section VI as the single source of truth; removes the unused `IX_conceptual_reference_values` section from `parameters.json`; moves the `BENCHMARK COMPLETE` banner in `run.py` to after the artifact listing with an artifact count; drops the corresponding integrity test (section IX no longer exists, 3 tests remain); and adds `tests/conftest.py` with an animated dot progress indicator that writes to `sys.stdout` to avoid column corruption on Windows terminals.

v1.2.4 reframes the project documentation in terms of natural botanical branching patterns and geometric structural families. The historical origin of the project (visual study of MS 408 / Voynich Manuscript) is acknowledged in a closing note within each document's introductory section. No code, parameters, tests, or computational results are affected.

v1.2.3 adds a classical multi-seed inference step (`data/inference_analysis.py`: Welch t-test, Cohen's d, bootstrap CI, Holm-Bonferroni, post-hoc power over N=30 per-seed means) together with a variance-collapse guard that flags seed-frozen morphologies (fractal, Fibonacci) as `n/a` instead of reporting their inflated effect sizes as findings; raises the multi-seed count from 5 to 30 seeds (42–71); expands the robustness sweep to a full 5×5×5 = 125-point grid reporting curve-separation ratios; renames `statistical_summary.csv` to `curve_separation_summary.csv` to mark it as a descriptor rather than an independent-sample test; and externalizes the seed list to `parameters.json`. The net effect is that the only surviving statistical claims are botanical separating from the stochastic controls.

v1.2.2 corrects the noise regime from asymmetric (botanical only, σ=0.15; all others σ=0.0) to symmetric (`noise_level=0.15` applied identically to every morphology); externalizes `noise_level` to `parameters.json` section VI as the single source of truth; updates `exploration_summary.json` accordingly; adds parametric robustness analysis (`data/parametric_sweep.py`, 48-point grid, 100% of combinations confirm botanical separation at p<0.05); fixes the Cohen's d NaN artifact (pooled std < 1e-4 → `"n/a"`, |d| > 50 → `"extreme"`); and adds a full-pipeline determinism test. Under symmetric noise, Coherence_Ratio no longer produces extreme Cohen's d values — those were artifacts of near-zero fractal variance under asymmetric conditions.

v1.2.1 extended the morphological benchmark from three to five morphologies, adding two synthetic controls — a Fibonacci spiral (golden-angle 137.508°) and a Voronoi vertex distribution — widening the statistical comparison to 3 metrics × 10 pairs (30 rows). Added closed-form parameter derivation, centralized outputs to `outputs/`, replaced the custom Welch t-test with `scipy.stats.ttest_ind(equal_var=False)`, vectorized the array-factor computation, and added weekly Dependabot monitoring.