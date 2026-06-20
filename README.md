# Biotic Hardware Synthesis: Computational Framework for Morphological Pattern Discrimination via Statistical Inference

<p align="center">
  <a href="https://github.com/Slpbcn6/biotic-hardware/actions/workflows/ci.yml"><img src="https://github.com/Slpbcn6/biotic-hardware/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white" alt="Python 3.12"></a>
  <a href="https://github.com/Slpbcn6/biotic-hardware/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT"></a>
  <a href="https://github.com/Slpbcn6/biotic-hardware/blob/main/CHANGELOG.md"><img src="https://img.shields.io/badge/version-1.3.0-green" alt="Version"></a>
  <a href="https://doi.org/10.5281/zenodo.20590864"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.20590864.svg" alt="DOI"></a>
</p>


![Biotic Hardware Synthesis](assets/readme1-3-0.svg)


This repository provides a reproducible computational framework for simulating structured network dynamics inspired by morphological datasets. It implements a full pipeline for parameter-driven simulation of coherence metrics, phase-based interference behavior (complex-valued phasor summation), sensitivity analysis under parametric variation, and formal statistical separation testing — producing numerical outputs, statistical artifacts, and visualization from a single executable workflow.

It operates under an ELF-inspired scalar parameterization using synthetic morphologies as structured inputs for abstract graph-based and lumped-element system modeling. All electromagnetic terminology used throughout (ELF, phased array, array factor, k0, NFMI) is applied in an analogical and computational sense. No physical electromagnetic system is modeled or implied.

It implements a generative computational pipeline in which synthetic morphological structures inspired by plant branching topology and botanical morphological patterns are mapped into simplified wave-interference and oscillator analogues inspired by abstract electromagnetic-style system analogies. These mappings enable the study of structural and dynamical properties within coupled-oscillator and network-based simulation frameworks.

The framework is designed for exploratory modeling, parametric sensitivity analysis, structural experimentation, and morphological comparison with formal statistical validation. It situates these simulations within a computational context where structural consistency is evaluated using numerical wave-interference-inspired mathematical models and lumped-parameter abstractions.

Procedural morphology generators (e.g., fractal and botanical structures) are structurally integrated into the main execution pipeline. These modules drive the deterministic benchmarking sequence via the `run.py` orchestrator, mapping structural inputs to spatial matrices before computing the array factor.

The system is strictly computational and interpretative. It does not represent a physical or biological implementation.

*Historical note:* this project originated from the visual study of botanical iconography in MS 408 (Voynich Manuscript). The manuscript was the starting point for exploring botanical branching as a structural taxonomy; the generators and the benchmarking framework are independent of it.

---

## Requirements

Install dependencies before running the pipeline:

```bash
pip install -r requirements.txt
```

---

## Quick Start

To run the full computational simulation pipeline:

```bash
python run.py
```

This executes the complete computational workflow (16 steps — ten morphology sweeps plus six analysis stages; see [OVERVIEW.md](./OVERVIEW.md) for the full numbered breakdown):

- Pre-simulation topology validation per sweep (connectivity, node count, degenerate structure detection)
- Distributed Phased Array simulation (phase-based interference superposition) across ten morphologies: fractal, botanical, random control, Fibonacci spiral, Voronoi control, hexagonal lattice, diffusion-limited aggregation (DLA), Gaussian clusters, concentric rings, and reticulate vein growth
- Statistical separation testing: Welch t-test + Cohen's d across 3 metrics and 45 morphology pairs
- Parametric sensitivity analysis and visualization of system response under geometric scaling
- Multi-seed analysis: mean ± std distributions across N=30 seeds (seeds 42–71)
- Multi-seed classical inference: Welch t-test, Cohen's d, bootstrap CI, Holm-Bonferroni correction, and post-hoc power over N=30 per-seed means; morphologies with near-zero seed variance are flagged n/a instead of being reported as findings
- Graph-topology analysis: per-morphology k-nearest-neighbour graphs, spectral descriptors (algebraic connectivity lambda_2, eigenratio R, clustering coefficient), and pre-specified topology-vs-merit correlations with leave-one-out cross-validation
- Parametric robustness sweep: k0 × beta × Q grid (5×5×5 = 125 combinations) confirming botanical separation is structural, not a tuning artifact

Outputs (generated artifacts are written to `outputs/`):

- Console logs of simulation results with per-sweep summary metrics
- `outputs/simulation_results_{fractal,botanical,random,fibonacci,voronoi,hexagonal,dla,clusters,concentric,reticulate}.csv` (Scalar Benchmark Contract)
- `outputs/af_tensors_{...}.npz` (Tensor Research Layer, one per morphology)
- `outputs/curve_separation_summary.csv` (curve separation descriptors: Welch t-test + Cohen's d on the autocorrelated sweep steps, 3 metrics × 45 pairs)
- `outputs/multi_seed_summary.csv` (mean ± std per morphology, N=30 seeds (seeds 42–71))
- `outputs/multi_seed_raw.csv` (per-seed means per morphology × metric; raw input consumed by the inference step)
- `outputs/inference_summary.csv` (classical inference: Welch t-test, Cohen's d, Hedges' g, bootstrap CI, Holm-corrected p, post-hoc power; near-zero-variance pairs reported as n/a)
- `outputs/graph_topology_summary.csv` (per-morphology spectral and classical graph descriptors averaged over the 30 seeds, with mean merit)
- `outputs/topology_correlation.csv` (H1/H2/H3 topology-vs-merit Pearson correlations across the ten morphologies, with LOOCV and the pre-specified significance threshold flag, at each k)
- `outputs/exploration_summary.json` (machine-readable experiment record)
- `outputs/sensitivity_analysis.png` — sensitivity curves + statistical heatmaps (also written to `data/sensitivity_analysis.png`)
- `outputs/robustness_matrix.csv` (parametric robustness grid: 125 combinations of k0, beta, Q; records the botanical-vs-random, botanical-vs-fractal, and botanical-vs-voronoi curve-separation ratios and whether the botanical separation holds against both stochastic controls at each point)

---

## Principal Finding

The benchmark separates two analytical lenses that earlier versions conflated. The single-seed **curve-separation descriptor** (`curve_separation_summary.csv`) compares autocorrelated sweep steps and is descriptive only — its Welch values are not independent-sample tests. The **classical inference** (`inference_summary.csv`) treats each seed's mean as one i.i.d. observation across N=30 seeds (seeds 42–71) and is the statistically valid test.

Three of the ten morphologies are seed-frozen by construction — fractal, Fibonacci, and hexagonal — with per-seed standard deviation ≈ 0.0005–0.001, roughly two orders of magnitude below the seed-variable morphologies. Any multi-seed test involving a seed-frozen morphology divides by a near-zero variance and produces spurious, astronomically large effect sizes. A variance-floor guard detects this per metric and reports every such pair as **n/a** (24 of the 45 pairs on Merit_Scaled and Peak_AF; 9 of 45 on Coherence_Ratio, where only fractal collapses) instead of as a finding.

v1.3.0 raises the benchmark from five morphologies to ten, which more than triples the multiple-comparison burden: Holm–Bonferroni now corrects across **21 valid pairs per metric** — each of the three metrics is treated as its own correction family, not pooled into a single 63-test family — instead of the earlier handful. The botanical result survives this heavier burden. On both Merit_Scaled and Peak_AF, botanical separates with Holm-corrected significance from four of the six other seed-variable morphologies, sitting **below the two high-merit stochastic controls** — Voronoi (d = −1.05 on Merit, −1.19 on Peak_AF) and reticulate vein growth (d = −1.04, −1.22) — and **above the two low-merit regular controls** — Gaussian clusters (d = +1.64, +1.66) and concentric rings (d = +1.52, +1.57) — with post-hoc power 0.98–1.0. On the third metric, Coherence_Ratio, botanical separates from none of the controls after Holm correction, so the signature is specific to Merit_Scaled and Peak_AF. Under the larger correction family botanical is no longer separable from the random control or from DLA (both fall below significance after Holm), so v1.3.0 reports botanical's signature as a robust mid-merit position relative to ordered and stochastic extremes rather than a blanket "below all controls" claim. Merit_Scaled is an internal structural indicator within the abstract simulation space, not a physical performance measure.

**Topology lens (exploratory).** A graph-topology layer builds k-nearest-neighbour graphs per morphology and tests three pre-specified hypotheses across the ten morphologies — H1 (eigenratio R vs merit), H2 (algebraic connectivity lambda_2 vs merit), H3 (clustering coefficient vs merit) — by Pearson correlation with leave-one-out cross-validation, against a pre-specified threshold of |r| ≥ 0.632. The test is anchored on the pre-specified primary neighbourhood size k = 6, with k = 3, 10, and 15 swept as a robustness check that no relationship is an artefact of a single graph resolution. **None of the three reaches the pre-specified significance criterion (|r| ≥ 0.632 with p < 0.05) at any k.** At the primary resolution (k = 6, all N = 10 morphologies connected) the strongest hypothesis, H2, gives r = −0.28 (p ≈ 0.43) — no linear relationship between spectral structure and merit. Across the robustness sweep the strongest correlation is at k = 3: there H2 reaches r = −0.66, exceeding the |r| bar, but it still falls short of significance (p ≈ 0.055) and rests on only N = 9 morphologies, because one graph disconnects at k = 3 and is dropped. The 0.632 bar is the critical Pearson r for ten points, and across all k the |r| values range roughly 0.03–0.66. At the available sample size the simple spectral descriptors do not linearly predict merit; this is reported honestly as a null result and the framework is provided so the hypothesis can be revisited with a larger morphology set.

Parametric robustness (symmetric noise): under the symmetric noise regime (`noise_level=0.15` applied identically to all morphologies), botanical's curve separation from the random control holds across **100% of the 125-point k0 × beta × Q parameter grid** (5×5×5; see `outputs/robustness_matrix.csv`), with the botanical-vs-random separation ratio staying well above the 0.10 threshold at every grid point. The matrix also records the botanical-vs-fractal and botanical-vs-voronoi ratios at each point for reference. The persistence under fair comparison conditions confirms the separation is a structural property of botanical morphology, not an artefact of perturbation or parameter tuning.

---

## Key Research Points

- **Perspective:** Application of signal processing, wave-interference modeling, and bio-inspired computational design to synthetic morphologies inspired by natural botanical branching structures.
- **Model:** Network-based representation using coupled oscillator systems, with Near-Field Magnetic Induction (NFMI) used strictly as conceptual inspiration for interaction topology design — not as a physical implementation or performance target.
- **Methodology:** Mapping of morphological geometry into abstract electromagnetic network representations for simulation, parameter exploration, and statistical comparison.
- **Validation:** Pre-simulation topology validation rejects degenerate structures before execution. Results are stress-tested across N=30 seeds per morphology and a 125-point parametric robustness grid.

Simulation baseline: [/data/parameters.json](./data/parameters.json)

---

## Objective

- Investigate whether morphological datasets can be used as structured inputs for generating consistent abstract network representations inspired by electromagnetic system analogies.
- Provide a reproducible computational framework for simulation, sensitivity analysis, and formal statistical comparison.
- Enable systematic comparison of geometric parameterizations under a unified modeling approach, with external baseline anchoring.

---

## Morphological Taxonomy Rationale

The ten morphological types — fractal branching, botanical, random control, Fibonacci spiral, Voronoi, hexagonal lattice, diffusion-limited aggregation (DLA), Gaussian clusters, concentric rings, and reticulate vein growth — are synthetic abstractions of structural patterns observable in nature. Each represents a distinct topology class: deterministic recursive structures, branching plant networks, unstructured spatial distributions, golden-ratio angular distributions, proximity-based tessellations, regular crystalline packing, stochastic dendritic growth, locally dense clumping, radial banding, and anastomosing filament networks. Three of the ten — fractal, Fibonacci, and hexagonal — are seed-frozen by construction (their generators ignore the seed beyond cosmetic jitter) and act as deterministic reference structures; the other seven carry genuine seed-to-seed variance.

The generators produce point-set geometries from mathematical rules. No external dataset is parsed or reproduced.

Alternative morphologies with analogous structural properties are compatible with this framework.

---

## Propagation and Signal Flow (Conceptual Model)

Morphological structures are mapped into abstract network components as follows:

- **Source / Grounding Grid:** Baseline node constraints in the network model.
- **Modulation and Filtering:** Structural symmetries mapped to abstract response modulation within lumped-parameter simulation components.
- **Inductive Coupling:** Geometric branching interpreted as coupling motifs in NFMI-inspired networks.
- **Phase Synchronization:** Radial structures represented as phase-coupled oscillators.
- **Material Layering:** Structural variation mapped to parameter heterogeneity (loss, damping, coupling strength).

These mappings are used strictly for computational simulation. No physical signal propagation is modeled.

---

## Numerical Model: Distributed Phased Array (Beamforming)

The system is extended into a spatial network model: [/data/node_coupling.py](./data/node_coupling.py)

This module computes coherent field superposition using a phased array formulation applied to abstract node graphs. The terminology (array factor, phased array, beamforming) is borrowed from antenna engineering as a computational analogy. No physical antenna array is modeled.

The coupling model includes phenomenological scaling coefficients used to modulate coherence response, spatial sensitivity, and normalized quality-factor behavior across the parametric sweep. These coefficients are heuristic simulation parameters intended for exploratory system dynamics and do not represent experimentally derived electromagnetic constants.

### Spatial Configuration

Nodes are distributed dynamically based on the selected morphology (one of the ten: fractal, botanical, random control, Fibonacci spiral, Voronoi control, hexagonal lattice, DLA, Gaussian clusters, concentric rings, or reticulate vein growth), comprising an array of N = 64 nodes.

**Geometric Treatment:** The transformation is strictly homotetic. The base topology remains fixed while the global scale is modulated continuously by a spacing parameter d from 0.1 to 2.0 meters (`positions = base_nodes * d`).

Phase assignments are applied cyclically across the N-node array to maintain controlled interference periodicity:

- Base sequence: **[0°, 90°, 180°, 270°]**

### Pre-simulation Topology Validation

Before each sweep executes, `data/topology_validator.py` validates the generated morphology using union-find with path-halving, minimum node count, and degenerate structure detection. Invalid topologies raise a `RuntimeError` and halt the pipeline.

### Scaling Parameter k0

The variable `k0_base` is a heuristic spatial scaling coefficient used to modulate the phase contribution of each node in the array factor computation. It is **not** the electromagnetic wave number k₀ = 2πf/c. In any ELF-inspired regime the physical wave number would be many orders of magnitude smaller than the value used here. The discrepancy is intentional: the model operates in an abstract simulation space, not in physical electromagnetic space.

### Data Export Architecture (Dual Layer)

To maintain a clean analytical contract while enabling deep research, the system bifurcates the computed data into two explicit layers:

#### 1. Scalar Output (Benchmarking Contract)

Exported as `outputs/simulation_results_*.csv`. Contains strictly the reduced variables for the analytical pipeline:

- `Distance` (Spatial scaling parameter)
- `Peak_AF` (Maximum amplitude of the Array Factor)
- `Coherence_Ratio` (Peak-to-mean field distribution ratio)
- `Merit_Function` (Base structural performance)
- `Q_effective` (Density-dependent dynamic regularization)
- `Merit_Scaled` (Post-transformation metric)

#### 2. Tensor Output (Research Layer)

Exported as `outputs/af_tensors_*.npz`. Contains the preserved latent state of the system for advanced topological analysis:

- `distance`: Full array of scaling steps.
- `af`: The complete 200-point Array Factor magnitude vector per step.

---

## Statistical Analysis

After all ten sweeps complete, the pipeline executes formal statistical separation testing:

- **Curve-separation descriptor** (`outputs/curve_separation_summary.csv`, 7 columns: Metric, Pair, t_statistic, p_value, Significant_p05, Cohens_d, Effect_size): a Welch t-test + Cohen's d computed over the autocorrelated sweep steps for all 3 metric × 45 pair combinations. This is a descriptive separation measure, not an independent-sample test.
- **Formal multi-seed inference** (`outputs/inference_summary.csv`): Welch t-test, Cohen's d, Hedges' g, bootstrap CI, Holm-Bonferroni and post-hoc power over the N=30 per-seed means, with a variance-collapse guard that marks seed-frozen morphologies (fractal, Fibonacci, hexagonal) as `n/a`.

Multi-seed analysis runs each morphology through N=30 seeds (seeds 42–71) and reports mean ± std per metric, confirming result stability across random initializations.

---

## Graph Topology Analysis

In addition to the field-coherence metrics, `data/graph_topology.py` reduces each morphology's node geometry to a graph and characterizes its structure independently of the array-factor computation. For each morphology and seed it builds a symmetric k-nearest-neighbour graph, forms the combinatorial Laplacian `L = D − A`, and computes its eigenspectrum with `scipy.linalg.eigh`. From the spectrum it derives the algebraic connectivity (lambda_2, the smallest non-zero eigenvalue), the largest eigenvalue (lambda_max), and the eigenratio `R = lambda_max / lambda_2`, together with the average clustering coefficient and classical descriptors (mean degree, density, characteristic path length). Disconnected graphs (more than one near-zero eigenvalue) are reported as `n/a` for the connectivity-dependent quantities — the module never emits a silent `inf` or `NaN`.

`data/topology_analysis.py` aggregates these per-seed descriptors into `outputs/graph_topology_summary.csv` (one row per morphology × k, averaged over the 30 seeds) and tests three pre-specified hypotheses about whether structure predicts the merit metric across the ten morphologies:

- **H1** — eigenratio R vs Merit_Scaled
- **H2** — algebraic connectivity lambda_2 vs Merit_Scaled
- **H3** — clustering coefficient vs Merit_Scaled

Each hypothesis is evaluated by Pearson correlation with leave-one-out cross-validation at several neighbourhood sizes (k = 3, 6, 10, 15), against a pre-specified threshold of |r| ≥ 0.632, and written to `outputs/topology_correlation.csv` (r, p, LOOCV mean/min/max r, sign stability, threshold flag).

**Result:** none of the three reaches the pre-specified criterion (|r| ≥ 0.632 with p < 0.05) at any k. At the pre-specified primary resolution (k = 6, all N = 10 morphologies connected) the strongest hypothesis is H2 at r = −0.28 (p ≈ 0.43) — no linear structure-to-merit relationship. Across the robustness sweep (k = 3, 10, 15) the strongest correlation is at k = 3, where H2 reaches r = −0.66, exceeding the |r| bar but failing significance at p ≈ 0.055 on N = 9 (one graph disconnects at k = 3 and is dropped). At N = 10 morphologies the test is underpowered and the simple spectral descriptors do not linearly predict merit; the layer is reported as an exploratory null and is intended to be revisited with a larger morphology set. This is the analytical reason v1.3.0 expands the benchmark to ten morphologies — to give the topology lens enough distinct structures to be meaningful.

---

## Sensitivity Analysis

A parametric sweep evaluates system response under continuous variation of the global spatial scale d. The visual analysis extracts and normalizes specific variables from the scalar CSV datasets.

The visualization generates a combined figure with four sections:

**Section 1 — Sensitivity curves:** Merit Scaled, Coherence Ratio, and Peak AF across the continuous distance sweep for all ten morphologies, with shaded ±1 SD bands from the per-seed means.

**Section 2 — Seed distribution:** per-morphology box plots of Merit Scaled over the N = 30 independent seeds, with the individual seed values overlaid.

**Section 3 — Topology vs merit:** two scatter panels of algebraic connectivity lambda_2 against mean Merit Scaled across the ten morphologies — the pre-specified primary resolution (k = 6, N = 10) and a robustness-sweep resolution (k = 3, N = 9). Each panel reports its Pearson r, p-value, and the pre-specified |r| ≥ 0.632 / p < 0.05 verdict; both are null (see the topology lens above).

**Section 4 — Pairwise effect size:** |Cohen's d| matrices (lower triangle per metric: Merit Scaled, Coherence Ratio, Peak AF), with colour intensity encoding effect-size magnitude, an asterisk marking pairs that remain significant after Holm–Bonferroni, and seed-frozen pairs shown as n/a.

Output: `outputs/sensitivity_analysis.png` (also written to `data/sensitivity_analysis.png`)

---

## Integration: Theory vs Computational Implementation

This repository implements a computational validation of the coherence and beamforming behavior defined in the theoretical model.

The associated document [Morpho-Topological Framework and Parameter Space.md](./docs/Morpho-Topological%20Framework%20and%20Parameter%20Space.md) defines a theoretical parameter space for the full system model, including structural variables such as permeability coefficients, coupling regimes, and energy-transfer analogues.

The README specifies the implemented computational subset of this space.

The current implementation focuses exclusively on the network synchronization kernel, which evaluates:

- phase coherence
- distributed coupling stability
- emergent beamforming behavior in graph-based oscillator networks

Modules related to energy conversion are treated as architectural specifications within the theoretical parameter space and are not instantiated in the current simulation layer. This separation reflects a layered abstraction model, where:

- the theoretical model defines the full parameterized system space
- the implementation evaluates a restricted subset of dynamical behaviors within that space

The parameter **k** is defined as a schematic spatial scaling factor representing the mapping between normalized geometric space and simulation space. It is not derived from electromagnetic wave propagation constants. Consequently, it is not directly coupled to material parameters such as permeability (μr); both operate as independent parameters within the modeling abstraction.

The implementation uses a small set of derived scaling variables (`k0_base` and the coherence-modulated wave number `k = k0_base · (1 + k_mod_coeff · (Q − q_ref))`) that operate at different stages of the simulation pipeline: base scaling initialization and coherence-modulated scaling. These variables are computational constructs used for numerical stability and do not represent a physically derived parameter hierarchy.

---

## Reproducibility

All simulations are fully deterministic given fixed seeds (default: 42). The pipeline is single-command executable (`python run.py`) with no external API calls or runtime downloads. Generated results are written to `outputs/` and regenerated on each run; the sensitivity figure is also committed at `data/sensitivity_analysis.png` for reference.

Pinned dependency versions are declared in `requirements.txt`. Environment reproducibility is further documented in `CHANGELOG.md`.