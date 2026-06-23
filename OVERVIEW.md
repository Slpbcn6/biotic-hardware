# Overview: Biotic Hardware Synthesis (v1.4.1)

*v1.4.1 is a documentation-only patch over the v1.4.0 pipeline: it refines wording in this overview, the README, and the citation metadata. The pipeline, parameters, and all numerical results are identical to v1.4.0 and were not re-run.*

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

The system executes a deterministic 17-step computational workflow — ten morphology sweeps (steps 1–10) followed by seven analysis stages (steps 11–17) — for abstract complex-valued interference modeling over the angular domain across multiple structural inputs. Each morphology sweep runs geometry → pre-simulation topology validation (union-find with path-halving, minimum node count, degenerate-structure rejection) → array factor → coherence → merit, and invalid topologies are rejected before any sweep executes. Each node's phase is assigned from its angular sector around the point-set centroid, a geometry-referenced rule that is invariant to the order in which a generator emits its nodes. The Voronoi nodes are the finite Voronoi vertices of a uniform random seed set that fall within the domain bounds; if fewer than the target node count qualify, the remainder is filled with uniform random points, keeping the control a fixed-size, reproducible point set. Under the geometry-referenced phase rule all ten morphologies carry genuine per-seed variance, because the positional noise shifts nodes across sector boundaries even for the deterministic generators (fractal, Fibonacci, hexagonal). The full execution order is:

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
13. Multi-seed classical inference: `data/inference_analysis.py` runs Welch t-test, Cohen's d, Hedges' g, bootstrap CI, post-hoc power, and Holm-Bonferroni correction pooled across all valid pairs (a single 135-pair family) over the N=30 per-seed means. A near-zero-variance guard flags any seed-frozen morphology as n/a; under the geometry-referenced phase rule none are degenerate, so 0 pairs are n/a this release. Output: `outputs/inference_summary.csv`.
14. Phase-robustness cross-check: `data/phase_robustness.py` recomputes the botanical-vs-control inference under a continuous centroid-referenced phase and compares it against the primary spatial-sector rule, flagging, per metric, whether the v1.3.0 below-control signature is absent under both. Output: `outputs/phase_robustness.csv`.
15. Graph-topology analysis: `data/topology_analysis.py` builds per-morphology k-nearest-neighbour graphs (`data/graph_topology.py`), derives spectral descriptors (algebraic connectivity lambda_2, eigenratio R, clustering coefficient) over the 30 seeds, and tests three pre-specified topology-vs-merit hypotheses across the ten morphologies by Pearson correlation with leave-one-out cross-validation. Outputs: `outputs/graph_topology_summary.csv`, `outputs/topology_correlation.csv`.
16. Parametric sensitivity analysis and visualization across all ten morphologies.
17. Parametric robustness sweep: `data/parametric_sweep.py` runs botanical vs random vs fractal vs Voronoi across a 5×5×5 grid of k0_base × beta_loss_factor × Q_individual (125 combinations) swept over all 30 seeds (3750 grid×seed cells), recording the curve-separation ratios and the below-both-stochastic-controls flag at each cell. Output: `outputs/robustness_matrix.csv`.

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

- `outputs/curve_separation_summary.csv` — Welch t-test + Cohen's d curve-separation descriptors across 3 metrics × 45 morphology pairs on autocorrelated sweep steps (descriptive only, not independent-sample tests).
- `outputs/multi_seed_summary.csv` — per-morphology mean ± std across N=30 seeds (seeds 42–71).
- `outputs/multi_seed_raw.csv` — per-seed means per morphology × metric; raw input to the inference step.
- `outputs/inference_summary.csv` — classical inference over N=30 per-seed means: Welch t-test, Cohen's d, Hedges' g, bootstrap CI, Holm-corrected p (pooled across all valid pairs), post-hoc power. Any seed-frozen morphology would be reported as n/a (variance collapse); under the geometry-referenced phase rule none are, so 0 pairs are n/a.
- `outputs/phase_robustness.csv` — the botanical-vs-control inference under the primary spatial-sector phase and the continuous centroid-referenced phase side by side (Cohen's d, Holm-corrected p, verdict per rule), with a per-metric flag recording whether the v1.3.0 below-control signature is absent under both.
- `outputs/graph_topology_summary.csv` — per-morphology spectral and classical graph descriptors averaged over the 30 seeds (lambda_2, eigenratio R, clustering coefficient, mean degree, density, characteristic path length, mean merit), one row per morphology × k.
- `outputs/topology_correlation.csv` — H1/H2/H3 topology-vs-merit Pearson correlations across the ten morphologies, with p-value, leave-one-out cross-validation (mean/min/max r, sign stability), and the pre-specified |r| ≥ 0.632 threshold flag, at each k.
- `outputs/exploration_summary.json` — machine-readable record of experimental configuration and multi-seed results per morphology.
- `outputs/robustness_matrix.csv` — parametric robustness grid: 125 combinations (5×5×5) of k0_base × beta_loss_factor × Q_individual swept across all 30 seeds (3750 grid×seed cells); columns: k0_base, beta_loss_factor, Q_individual, seed, curve_sep_botanical_vs_random, curve_sep_botanical_vs_fractal, curve_sep_botanical_vs_voronoi, finding_holds (botanical separates below both the random and Voronoi controls at that cell). The below-both signature holds in 500 of 3750 cells (13%).

### Visualization Artifacts

- `outputs/sensitivity_analysis.png` — combined figure: sensitivity curves (Merit Scaled, Coherence Ratio, Peak AF), the Merit Scaled seed-distribution box plots, two topology-vs-merit scatter panels (the pre-specified primary k=6, null, and the non-primary robustness resolution k=3 that crosses the bar only there), and the pairwise |Cohen's d| effect-size matrices. Also committed at `data/sensitivity_analysis.png`.

---

## Key Results

Principal finding (methodological correction): v1.4.0 retracts the central v1.3.0 claim. v1.3.0 assigned each node's phase from a fixed four-value sequence indexed by the node's position in the generator output (`base_phases[i % 4]`), so the array factor — and every metric derived from it — depended on the arbitrary order a generator emitted its nodes rather than on geometry. v1.4.0 assigns phase from each node's angular sector around the point-set centroid, a geometry-referenced rule, and cross-checks it against a continuous centroid-referenced phase. Under the corrected, pre-specified primary (sector) rule, with Holm–Bonferroni pooled across **all valid pairs in a single family** (135 pairs = 45 × 3 metrics, not per metric), botanical is **statistically indistinguishable from every genuine stochastic control** on Merit_Scaled and Peak_AF: vs random d = +0.67 / +0.69 (p_holm = 0.51 / 0.44, n.s.), vs Voronoi d = +0.61 / +0.64 (p_holm = 0.93 / 0.68, n.s.), and vs DLA and reticulate both n.s. Where v1.3.0 reported botanical d = −1.05 below Voronoi, the corrected estimate is d = +0.61 and non-significant — the direction itself does not hold. Botanical's only Holm-significant Merit_Scaled and Peak_AF separations are from the **regular geometric controls** (Gaussian clusters d ≈ +0.93, concentric rings d ≈ +2.16 / +2.20) and the deterministic references (fractal, Fibonacci, hexagonal): on these two metrics it separates from ordered or degenerate structure but not from unstructured or stochastic structure — though on the coherence ratio it does differ robustly from Voronoi (secondary observation below).

Phase-robustness cross-check: the inference is recomputed under the continuous phase for all three metrics (18 comparisons). For Merit_Scaled and Peak_AF — the metrics the v1.3.0 claim concerned — the below-control signature is **absent under both** the sector and the continuous phase rules in all 12 comparisons; the two rules agree on the *sign* of any residual difference but differ in its significance and magnitude — both place botanical *above* random and Voronoi, non-significant under the sector rule (d ≈ +0.6–0.7) but significantly above under the continuous rule (d ≈ +0.98–1.16, p_holm ≈ 0.002–0.015) — and neither reproduces the v1.3.0 *below*-control direction. On Coherence_Ratio, however, botanical sits robustly *below* Voronoi under both rules (sector d = −1.12, continuous d = −1.56) and below the concentric control as well — a secondary structural observation, not a performance claim and not a revival of the retracted Merit_Scaled/Peak_AF finding, which concerned different metrics and reverses sign under the same cross-check.

Variance note: in v1.3.0 fractal, Fibonacci, and hexagonal were seed-frozen and every pair involving them was reported as n/a. Under the geometry-referenced phase rule the positional noise shifts nodes across sector boundaries, so even these deterministic generators acquire genuine per-seed variance (Merit_Scaled std ≈ 0.17–0.20); none fall below the degeneracy threshold and this release reports 0 pairs as n/a. A single near-zero-variance authority (`stats_utils.near_zero_variance`) backs both the Cohen's d guard and the seed-frozen detection and would still flag any genuinely seed-frozen series. Merit_Scaled is an internal structural indicator within the abstract simulation space, not a physical performance measure.

Topology finding (exploratory): at the pre-specified primary resolution (k = 6, all N = 10 morphologies connected) none of the three hypotheses (H1 eigenratio R, H2 algebraic connectivity lambda_2, H3 clustering coefficient) crosses the pre-specified criterion (|r| ≥ 0.632 with p < 0.05); the strongest, H2, gives r = −0.35 (p ≈ 0.33). A correlation that crosses the bar appears only at the non-primary robustness resolution k = 3, where H2 reaches r = −0.72 (p ≈ 0.028) on N = 9 (one graph disconnects at k = 3 and is dropped). Because k = 3 is a robustness resolution and not the pre-specified test, it is reported as an exploratory observation, not a confirmed relationship; the layer is provided so the hypothesis can be revisited with more morphologies.

Robustness finding: across the 125-point k0 × beta × Q grid swept over all 30 seeds (3750 grid×seed cells; `outputs/robustness_matrix.csv`), the v1.3.0 "botanical below both stochastic controls (random and Voronoi)" signature holds in only **500 of 3750 cells (13%)**, confirming from a third direction that it is not a robust structural property.

![Sensitivity Analysis](./data/sensitivity_analysis.png)

---

## Scope

This system is strictly computational. It does not model or validate physical systems. All behavior is confined to an abstract computational simulation space with no physical interpretation.

**Execution State Note:** The orchestrator (`run.py`) manages the benchmark sequentially by injecting morphology modes directly into the coupling solver. Each sweep is independent and side-effect-free; `data/parameters.json` is never mutated at runtime. Executing `data/node_coupling.py` independently outside of `run.py` will use the configuration state defined in the JSON file at that moment.

---

## Version History

v1.4.0 is a methodological-correction / honest-null release that retracts the central v1.3.0 finding. The node phase was previously assigned from a fixed four-value sequence indexed by each node's position in the generator output (`base_phases[i % 4]`), so the array factor depended on the arbitrary order a generator emitted its nodes rather than on geometry; re-ordering the same point set changed the result. v1.4.0 assigns phase from each node's angular sector around the point-set centroid (a geometry-referenced rule, invariant to node ordering) and adds a continuous centroid-referenced phase as an independent robustness rule (`data/phase_robustness.py` → `outputs/phase_robustness.csv`). Under the corrected rule the v1.3.0 signature collapses: with Holm–Bonferroni pooled across all 135 valid pairs (the per-metric framing of earlier docs was incorrect relative to the code), botanical is statistically indistinguishable from every genuine stochastic control (random, Voronoi, DLA, reticulate) on Merit_Scaled and Peak_AF, separating only from the regular and deterministic controls; the "below Voronoi" claim reverses sign and loses significance. Both phase rules agree the Merit_Scaled/Peak_AF below-control signature is absent (12 / 12); on the coherence ratio, by contrast, botanical sits robustly below Voronoi under both rules (a restrained secondary observation, not a performance claim). The parametric robustness sweep — now run across all 30 seeds (3750 grid×seed cells) — holds the retracted signature in only 500 cells (13%). The variance guard is unified into a single near-zero-variance authority in `stats_utils.py`; under the geometry-referenced phase the formerly seed-frozen morphologies acquire genuine per-seed variance, so 0 pairs are n/a this release. The topology layer is reframed: the pre-specified primary test (k = 6) is null (H2 r = −0.35), and the k = 3 crossing (r = −0.72, p = 0.028, N = 9) is reported as a non-primary exploratory robustness observation. The pipeline grows from 16 to 17 steps with the phase-robustness check. No claim in this release was pre-registered; all are pre-specified.

v1.3.0 doubles the benchmark from five morphologies to ten — adding a hexagonal lattice (seed-frozen), diffusion-limited aggregation (DLA), Gaussian clusters, concentric rings, and reticulate vein growth — and introduces a graph-topology layer. A new `data/graph_topology.py` builds k-nearest-neighbour graphs and computes spectral descriptors (algebraic connectivity lambda_2, eigenratio R, clustering coefficient) from the Laplacian eigenspectrum, with disconnected graphs reported as n/a rather than silent inf/NaN; `data/topology_analysis.py` aggregates these over the 30 seeds and tests three pre-specified topology-vs-merit hypotheses by Pearson correlation with leave-one-out cross-validation. The expansion more than triples the multiple-comparison burden (21 valid pairs per metric under Holm); the botanical Merit_Scaled and Peak_AF separation survives, now framed as a mid-merit position below the high-merit stochastic controls (Voronoi, reticulate) and above the low-merit regular controls (clusters, concentric). The topology-vs-merit correlations are an exploratory null at N = 10. New outputs: `graph_topology_summary.csv`, `topology_correlation.csv`. The licence changes from CC BY 4.0 to MIT.

v1.2.6 is a hardening and cleanup release with no change to the scientific result. It removes the resonance-baseline scaffolding (`data/node_resonance.py`, `data/schumann_reference.py`, `data/parameter_derivation.py`) and the corresponding Schumann external-comparison and L/C derivation steps, shortening the pipeline from 12 to 10 steps; the simulation never depended on those values. It adds a Hedges' g column (small-sample-corrected effect size) alongside Cohen's d in `inference_summary.csv`, extends the parametric robustness sweep so botanical separation must hold against both stochastic controls (random and Voronoi) at every grid point, externalises `variance_collapse_fraction` to `parameters.json` section VI, and adds focused unit tests for `stats_utils`, `input_generator`, and `topology_validator`.

v1.2.5 externalises `curve_separation_threshold` from a hardcoded literal in `data/parametric_sweep.py` into `data/parameters.json` section VI as the single source of truth; removes the unused `IX_conceptual_reference_values` section from `parameters.json`; moves the `BENCHMARK COMPLETE` banner in `run.py` to after the artifact listing with an artifact count; drops the corresponding integrity test (section IX no longer exists, 3 tests remain); and adds `tests/conftest.py` with an animated dot progress indicator that writes to `sys.stdout` to avoid column corruption on Windows terminals.

v1.2.4 reframes the project documentation in terms of natural botanical branching patterns and geometric structural families. The historical origin of the project (visual study of MS 408 / Voynich Manuscript) is acknowledged in a closing note within each document's introductory section. No code, parameters, tests, or computational results are affected.

v1.2.3 adds a classical multi-seed inference step (`data/inference_analysis.py`: Welch t-test, Cohen's d, bootstrap CI, Holm-Bonferroni, post-hoc power over N=30 per-seed means) together with a variance-collapse guard that flags seed-frozen morphologies (fractal, Fibonacci) as `n/a` instead of reporting their inflated effect sizes as findings; raises the multi-seed count from 5 to 30 seeds (42–71); expands the robustness sweep to a full 5×5×5 = 125-point grid reporting curve-separation ratios; renames `statistical_summary.csv` to `curve_separation_summary.csv` to mark it as a descriptor rather than an independent-sample test; and externalizes the seed list to `parameters.json`. The net effect is that the only surviving statistical claims are botanical separating from the stochastic controls.

v1.2.2 corrects the noise regime from asymmetric (botanical only, σ=0.15; all others σ=0.0) to symmetric (`noise_level=0.15` applied identically to every morphology); externalizes `noise_level` to `parameters.json` section VI as the single source of truth; updates `exploration_summary.json` accordingly; adds parametric robustness analysis (`data/parametric_sweep.py`, 48-point grid, 100% of combinations confirm botanical separation at p<0.05); fixes the Cohen's d NaN artifact (pooled std < 1e-4 → `"n/a"`, |d| > 50 → `"extreme"`); and adds a full-pipeline determinism test. Under symmetric noise, Coherence_Ratio no longer produces extreme Cohen's d values — those were artifacts of near-zero fractal variance under asymmetric conditions.

v1.2.1 extended the morphological benchmark from three to five morphologies, adding two synthetic controls — a Fibonacci spiral (golden-angle 137.508°) and a Voronoi vertex distribution — widening the statistical comparison to 3 metrics × 10 pairs (30 rows). Added closed-form parameter derivation, centralized outputs to `outputs/`, replaced the custom Welch t-test with `scipy.stats.ttest_ind(equal_var=False)`, vectorized the array-factor computation, and added weekly Dependabot monitoring.