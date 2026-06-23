# Biotic Hardware Synthesis: Computational Framework for Morphological Pattern Discrimination via Statistical Inference

<p align="center">
  <a href="https://github.com/Slpbcn6/biotic-hardware/actions/workflows/ci.yml"><img src="https://github.com/Slpbcn6/biotic-hardware/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white" alt="Python 3.12"></a>
  <a href="https://github.com/Slpbcn6/biotic-hardware/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT"></a>
  <a href="https://github.com/Slpbcn6/biotic-hardware/blob/main/CHANGELOG.md"><img src="https://img.shields.io/badge/version-1.4.1-green" alt="Version"></a>
  <a href="https://doi.org/10.5281/zenodo.20590864"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.20590864.svg" alt="DOI"></a>
</p>


![Biotic Hardware Synthesis](assets/readme1-4-1.svg)


> **v1.4.1** is a documentation-only patch over the **v1.4.0** pipeline: it refines wording in this README, `OVERVIEW.md`, and `CITATION.cff`. The code, parameters, and every numerical result are identical to v1.4.0 and were not re-run.

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

This executes the complete computational workflow (17 steps — ten morphology sweeps plus seven analysis stages; see [OVERVIEW.md](./OVERVIEW.md) for the full numbered breakdown):

- Pre-simulation topology validation per sweep (connectivity, node count, degenerate structure detection)
- Distributed Phased Array simulation (phase-based interference superposition) across ten morphologies: fractal, botanical, random control, Fibonacci spiral, Voronoi control, hexagonal lattice, diffusion-limited aggregation (DLA), Gaussian clusters, concentric rings, and reticulate vein growth
- Statistical separation testing: Welch t-test + Cohen's d across 3 metrics and 45 morphology pairs
- Parametric sensitivity analysis and visualization of system response under geometric scaling
- Multi-seed analysis: mean ± std distributions across N=30 seeds (seeds 42–71)
- Multi-seed classical inference: Welch t-test, Cohen's d, bootstrap CI, post-hoc power, and Holm-Bonferroni correction pooled across all valid pairs over N=30 per-seed means; a near-zero-variance guard flags any seed-frozen morphology as n/a (under the geometry-referenced phase rule none are flagged in this release)
- Phase-robustness cross-check: the botanical-vs-control inference recomputed under a continuous centroid-referenced phase and compared against the primary spatial-sector rule, with an agreement flag per pair
- Graph-topology analysis: per-morphology k-nearest-neighbour graphs, spectral descriptors (algebraic connectivity lambda_2, eigenratio R, clustering coefficient), and pre-specified topology-vs-merit correlations with leave-one-out cross-validation
- Parametric robustness sweep: k0 × beta × Q grid (5×5×5 = 125 combinations) swept across all 30 seeds (3750 grid×seed cells), reporting the fraction of cells in which the below-both-stochastic-controls signature holds

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
- `outputs/phase_robustness.csv` (botanical-vs-control inference under the primary spatial-sector phase and the continuous centroid-referenced phase side by side: Cohen's d, Holm-corrected p, and verdict per rule, plus a per-metric flag recording whether the v1.3.0 below-control signature is absent under both)
- `outputs/sensitivity_analysis.png` — sensitivity curves + statistical heatmaps (also written to `data/sensitivity_analysis.png`)
- `outputs/robustness_matrix.csv` (parametric robustness grid: 125 combinations of k0, beta, Q swept across all 30 seeds = 3750 grid×seed cells; records the botanical-vs-random, botanical-vs-fractal, and botanical-vs-voronoi curve-separation ratios and whether the below-both-stochastic-controls signature holds at each cell)

---

## Principal Finding

The benchmark separates two analytical lenses that earlier versions conflated. The single-seed **curve-separation descriptor** (`curve_separation_summary.csv`) compares autocorrelated sweep steps and is descriptive only — its Welch values are not independent-sample tests. The **classical inference** (`inference_summary.csv`) treats each seed's mean as one i.i.d. observation across N=30 seeds (seeds 42–71) and is the statistically valid test.

**v1.4.0 is a methodological-correction release that retracts the central v1.3.0 claim.** v1.3.0 reported that botanical "sits below the high-merit stochastic controls" (Voronoi and reticulate vein growth) on Merit_Scaled and Peak_AF. That result was an artefact of how node phases were assigned. The array factor summed each node with a phase drawn from a fixed four-value sequence indexed by the node's position in the generator's output list (`base_phases[i % 4]`), so the interference pattern — and every metric derived from it — depended on the arbitrary order in which a generator happened to emit its nodes rather than on the morphology's geometry. Re-ordering the same point set changed the result. v1.4.0 removes the confound by assigning each node's phase from its angular sector around the point-set centroid, a geometry-referenced rule that is invariant to node ordering, and cross-checks it against a continuous centroid-referenced phase as an independent robustness rule.

In v1.3.0 three of the ten morphologies — fractal, Fibonacci, and hexagonal — were seed-frozen by construction, with per-seed standard deviation roughly two orders of magnitude below the seed-variable morphologies, so a variance guard reported every pair involving them as n/a. Under the geometry-referenced phase rule that no longer holds: because the phase now depends on each node's position relative to the centroid, the symmetric 0.15 positional noise shifts nodes across sector boundaries and gives even the deterministic generators genuine per-seed variance (Merit_Scaled std ≈ 0.17–0.20). None of the ten fall below the degeneracy threshold this release, so the inference reports 0 pairs as n/a and every comparison is a valid test. A single near-zero-variance authority (`stats_utils.near_zero_variance`, an absolute floor combined with a fraction-of-reference test) still backs both the Cohen's d guard and the seed-frozen detection, so the two can never disagree, and it would flag any genuinely seed-frozen series.

Holm–Bonferroni is applied across **all valid pairs pooled into a single family**, not per metric. With ten morphologies that family is 135 pairs (45 pairs × 3 metrics). Earlier documentation described a per-metric correction; that was incorrect relative to the code, and the per-metric framing would have made botanical-vs-random and botanical-vs-Voronoi appear significant where the pooled correction the pipeline actually applies leaves them non-significant. Under the pre-specified primary (sector) phase rule and this pooled burden the v1.3.0 signature does not reproduce. On Merit_Scaled and Peak_AF, botanical is **statistically indistinguishable from every genuine stochastic control**: botanical vs random d = +0.67 / +0.69 (p_holm = 0.51 / 0.44, n.s.), botanical vs Voronoi d = +0.61 / +0.64 (p_holm = 0.93 / 0.68, n.s.), and botanical vs DLA and botanical vs reticulate are both non-significant. Note the sign: where v1.3.0 reported botanical d = −1.05 below Voronoi, the corrected estimate is d = +0.61 and non-significant — the direction itself does not hold. Botanical's only Holm-significant Merit_Scaled and Peak_AF separations are from the **regular geometric controls** (Gaussian clusters d ≈ +0.93, concentric rings d ≈ +2.16 / +2.20) and from the deterministic-geometry references (fractal, Fibonacci, hexagonal). On Merit_Scaled and Peak_AF, then, botanical separates from ordered or degenerate structure but not from unstructured or stochastic structure — the property earlier versions reported as the headline finding. That metric-scoped statement is not a blanket claim of equivalence: on the coherence ratio botanical does differ robustly from the Voronoi control, as the secondary observation below records. Merit_Scaled is an internal structural indicator within the abstract simulation space, not a physical performance measure.

**Phase-robustness cross-check** (`outputs/phase_robustness.csv`). The botanical-vs-control inference is recomputed under the continuous centroid-referenced phase and compared against the primary sector rule for all three metrics (18 botanical-vs-control comparisons). For the two metrics the v1.3.0 claim concerned — Merit_Scaled and Peak_AF — the below-control signature is **absent under both rules in all 12 comparisons** (six controls × two metrics). The two rules agree on the *sign* of any residual difference but not on its significance or magnitude: on both metrics botanical sits *above* random and Voronoi under each rule — non-significant under the sector rule (d ≈ +0.6–0.7) but significantly above under the continuous rule (botanical vs random d = +0.98 / +1.00, botanical vs Voronoi d = +1.13 / +1.16, p_holm ≈ 0.002–0.015). Neither rule reproduces the v1.3.0 *below*-control direction, so the retraction holds under both. The remaining six comparisons cover Coherence_Ratio, where one difference does survive both rules — see the secondary observation that follows.

**Secondary observation (coherence ratio).** One structural difference does survive on a metric outside the v1.3.0 claim. On Coherence_Ratio — the peak-to-mean concentration of the array factor — botanical sits significantly *below* Voronoi under both phase rules (sector d = −1.12, p_holm = 0.004; continuous d = −1.56, p_holm = 0.00003), and below the concentric-rings control under both rules as well. Because the difference is robust to the phase-assignment rule that this release corrects, it is not an artefact of the confound. It is reported as a genuine but restrained structural observation: within the simulation, botanical produces a less peaked, more distributed coherence profile than the Voronoi control. No performance or physical interpretation is attached to it, and it does not reinstate the retracted Merit_Scaled/Peak_AF claim — that claim concerned different metrics and reverses sign under the same cross-check.

**Topology lens (exploratory).** A graph-topology layer builds k-nearest-neighbour graphs per morphology and tests three pre-specified hypotheses across the ten morphologies — H1 (eigenratio R vs merit), H2 (algebraic connectivity lambda_2 vs merit), H3 (clustering coefficient vs merit) — by Pearson correlation with leave-one-out cross-validation, against a pre-specified threshold of |r| ≥ 0.632. The test is anchored on the pre-specified primary neighbourhood size k = 6, with k = 3, 10, and 15 swept as a robustness check that no relationship is an artefact of a single graph resolution. At the pre-specified primary resolution (k = 6, all N = 10 morphologies connected) the strongest hypothesis, H2, gives r = −0.35 (p ≈ 0.33) — no linear relationship between spectral structure and merit, and none of the three hypotheses crosses the criterion there. A correlation that crosses the bar appears only at the non-primary robustness resolution k = 3, where H2 reaches r = −0.72 (p ≈ 0.028) but rests on only N = 9 morphologies, because one graph disconnects at k = 3 and is dropped. Because k = 3 is a robustness resolution and not the pre-specified test, this is reported as an exploratory observation rather than a confirmed relationship; at the available sample size the simple spectral descriptors do not reliably predict merit, and the framework is provided so the hypothesis can be revisited with a larger morphology set.

**Parametric robustness.** The 125-point k0 × beta × Q parameter grid (5×5×5; `noise_level=0.15` applied identically to all morphologies) is swept across all 30 seeds, giving 3750 grid×seed cells. The v1.3.0 "botanical separates below both stochastic controls (random and Voronoi)" signature holds in only **500 of 3750 cells (13%)** (see `outputs/robustness_matrix.csv`), confirming from a third direction that it is not a robust structural property. The matrix records the botanical-vs-random, botanical-vs-fractal, and botanical-vs-voronoi separation ratios at every cell.

---

## Key Research Points

- **Perspective:** Application of signal processing, wave-interference modeling, and bio-inspired computational design to synthetic morphologies inspired by natural botanical branching structures.
- **Model:** Network-based representation using coupled oscillator systems, with Near-Field Magnetic Induction (NFMI) used strictly as conceptual inspiration for interaction topology design — not as a physical implementation or performance target.
- **Methodology:** Mapping of morphological geometry into abstract electromagnetic network representations for simulation, parameter exploration, and statistical comparison.
- **Validation:** Pre-simulation topology validation rejects degenerate structures before execution. Results are stress-tested across N=30 seeds per morphology, a 3750-cell parametric robustness grid (125 points × 30 seeds), and a two-phase-rule robustness cross-check.

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

Each node's phase is assigned from its angular sector around the point-set centroid: the plane is divided into four equal quadrants and a node receives the base phase of the quadrant its position falls in. This makes the phase a function of geometry, invariant to the order in which a generator emits its nodes. A continuous centroid-referenced phase (the centroid angle mapped directly onto the phase circle) is available as an independent robustness rule.

- Base sequence: **[0°, 90°, 180°, 270°]**, selected by spatial sector rather than by node index

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
- **Formal multi-seed inference** (`outputs/inference_summary.csv`): Welch t-test, Cohen's d, Hedges' g, bootstrap CI, post-hoc power, and Holm-Bonferroni correction pooled across all valid pairs (a single 135-pair family, not per metric) over the N=30 per-seed means, with a variance-collapse guard that marks any seed-frozen morphology as `n/a`. Under the geometry-referenced phase rule no morphology is degenerate, so this release reports 0 pairs as n/a.
- **Phase-robustness cross-check** (`outputs/phase_robustness.csv`): the botanical-vs-control inference recomputed under the continuous centroid-referenced phase and laid alongside the primary sector rule, with a per-metric flag confirming the v1.3.0 Merit_Scaled/Peak_AF below-control signature is absent under both (12 / 12), alongside the secondary coherence-ratio difference that does survive.

Multi-seed analysis runs each morphology through N=30 seeds (seeds 42–71) and reports mean ± std per metric, confirming result stability across random initializations.

---

## Graph Topology Analysis

In addition to the field-coherence metrics, `data/graph_topology.py` reduces each morphology's node geometry to a graph and characterizes its structure independently of the array-factor computation. For each morphology and seed it builds a symmetric k-nearest-neighbour graph, forms the combinatorial Laplacian `L = D − A`, and computes its eigenspectrum with `scipy.linalg.eigh`. From the spectrum it derives the algebraic connectivity (lambda_2, the smallest non-zero eigenvalue), the largest eigenvalue (lambda_max), and the eigenratio `R = lambda_max / lambda_2`, together with the average clustering coefficient and classical descriptors (mean degree, density, characteristic path length). Disconnected graphs (more than one near-zero eigenvalue) are reported as `n/a` for the connectivity-dependent quantities — the module never emits a silent `inf` or `NaN`.

`data/topology_analysis.py` aggregates these per-seed descriptors into `outputs/graph_topology_summary.csv` (one row per morphology × k, averaged over the 30 seeds) and tests three pre-specified hypotheses about whether structure predicts the merit metric across the ten morphologies:

- **H1** — eigenratio R vs Merit_Scaled
- **H2** — algebraic connectivity lambda_2 vs Merit_Scaled
- **H3** — clustering coefficient vs Merit_Scaled

Each hypothesis is evaluated by Pearson correlation with leave-one-out cross-validation at several neighbourhood sizes (k = 3, 6, 10, 15), against a pre-specified threshold of |r| ≥ 0.632, and written to `outputs/topology_correlation.csv` (r, p, LOOCV mean/min/max r, sign stability, threshold flag).

**Result:** at the pre-specified primary resolution (k = 6, all N = 10 morphologies connected) none of the three crosses the criterion; the strongest hypothesis is H2 at r = −0.35 (p ≈ 0.33) — no linear structure-to-merit relationship. A correlation that crosses the |r| ≥ 0.632 / p < 0.05 bar appears only at the non-primary robustness resolution k = 3, where H2 reaches r = −0.72 (p ≈ 0.028) on N = 9 (one graph disconnects at k = 3 and is dropped). Because k = 3 is a robustness resolution and not the pre-specified test, this is reported as an exploratory observation, not a confirmed relationship. At N = 10 morphologies the test is underpowered; the layer is intended to be revisited with a larger morphology set. This is the analytical reason the benchmark was expanded to ten morphologies — to give the topology lens enough distinct structures to be meaningful.

---

## Sensitivity Analysis

A parametric sweep evaluates system response under continuous variation of the global spatial scale d. The visual analysis extracts and normalizes specific variables from the scalar CSV datasets.

The visualization generates a combined figure with four sections:

**Section 1 — Sensitivity curves:** Merit Scaled, Coherence Ratio, and Peak AF across the continuous distance sweep for all ten morphologies, with shaded ±1 SD bands from the per-seed means.

**Section 2 — Seed distribution:** per-morphology box plots of Merit Scaled over the N = 30 independent seeds, with the individual seed values overlaid.

**Section 3 — Topology vs merit:** two scatter panels of algebraic connectivity lambda_2 against mean Merit Scaled across the ten morphologies — the pre-specified primary resolution (k = 6, N = 10; null) and the non-primary robustness resolution that gives the strongest correlation (k = 3, N = 9). Each panel reports its Pearson r, p-value, and the pre-specified |r| ≥ 0.632 / p < 0.05 verdict; the pre-specified primary test is null, and the k = 3 panel crosses the bar only at that non-primary resolution and is flagged as a robustness check (see the topology lens above).

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