# Biotic Hardware Synthesis: Computational Framework for Morphological Pattern Discrimination via Statistical Inference

<p align="center">
  <a href="https://github.com/Slpbcn6/biotic-hardware/actions/workflows/ci.yml"><img src="https://github.com/Slpbcn6/biotic-hardware/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white" alt="Python 3.12"></a>
  <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey" alt="License: CC BY 4.0"></a>
  <a href="https://github.com/Slpbcn6/biotic-hardware/blob/main/CHANGELOG.md"><img src="https://img.shields.io/badge/version-1.2.5-green" alt="Version"></a>
  <a href="https://doi.org/10.5281/zenodo.20590864"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.20590864.svg" alt="DOI"></a>
</p>


![Biotic Hardware Synthesis](assets/readme1-2-5.svg)


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

This executes the complete computational workflow (12 steps — see [OVERVIEW.md](./OVERVIEW.md) for the full numbered breakdown):

- Parameter derivation: closed-form L/C derivation from the target frequency (f_target → L → C → f_check at 12.5 Hz)
- Node-level resonance baseline and external Schumann resonance comparison (NOAA/GFZ Potsdam, modes 1–5)
- Pre-simulation topology validation per sweep (connectivity, node count, degenerate structure detection)
- Distributed Phased Array simulation (phase-based interference superposition) across five morphologies: fractal, botanical, random control, Fibonacci spiral, and Voronoi control
- Statistical separation testing: Welch t-test + Cohen's d across 3 metrics and 10 morphology pairs
- Parametric sensitivity analysis and visualization of system response under geometric scaling
- Multi-seed analysis: mean ± std distributions across N=30 seeds (seeds 42–71)
- Multi-seed classical inference: Welch t-test, Cohen's d, bootstrap CI, Holm-Bonferroni correction, and post-hoc power over N=30 per-seed means; morphologies with near-zero seed variance are flagged n/a instead of being reported as findings
- Parametric robustness sweep: k0 × beta × Q grid (5×5×5 = 125 combinations) confirming botanical separation is structural, not a tuning artifact

Outputs (generated artifacts are written to `outputs/`):

- Console logs of simulation results with per-sweep summary metrics
- `outputs/resonance_params.json` (node resonance baseline: f_resonance, Q factor)
- `outputs/simulation_results_{fractal,botanical,random,fibonacci,voronoi}.csv` (Scalar Benchmark Contract)
- `outputs/af_tensors_{fractal,botanical,random,fibonacci,voronoi}.npz` (Tensor Research Layer)
- `outputs/curve_separation_summary.csv` (curve separation descriptors: Welch t-test + Cohen's d on 30 autocorrelated sweep steps, 30 rows)
- `outputs/multi_seed_summary.csv` (mean ± std per morphology, N=30 seeds (seeds 42–71))
- `outputs/multi_seed_raw.csv` (per-seed means per morphology × metric; raw input consumed by the inference step)
- `outputs/inference_summary.csv` (classical inference: Welch t-test, Cohen's d, bootstrap CI, Holm-corrected p, post-hoc power; near-zero-variance pairs reported as n/a)
- `outputs/exploration_summary.json` (machine-readable experiment record)
- `outputs/sensitivity_analysis.png` — sensitivity curves + statistical heatmaps (also written to `data/sensitivity_analysis.png`)
- `outputs/robustness_matrix.csv` (parametric robustness grid: 125 combinations of k0, beta, Q; records the botanical-vs-random and botanical-vs-fractal curve-separation ratios and whether the botanical separation holds at each point)

---

## Principal Finding (v1.2.3)

v1.2.3 separates two analytical lenses that earlier versions conflated. The single-seed **curve-separation descriptor** (`curve_separation_summary.csv`) compares 30 autocorrelated sweep steps and is descriptive only — its Welch values are not independent-sample tests. The **classical inference** (`inference_summary.csv`) treats each seed's mean as one i.i.d. observation across N=30 seeds (seeds 42–71) and is the statistically valid test.

Crucially, the fractal and Fibonacci morphologies are seed-frozen: their per-seed standard deviation is ≈ 0.0005, roughly two orders of magnitude below the seed-variable morphologies (botanical, random, Voronoi: std ≈ 0.012–0.020). Any multi-seed test involving a seed-frozen morphology divides by a near-zero variance and produces spurious, astronomically large effect sizes (|d| up to ≈ 26). v1.2.3 detects this with a variance-floor guard and reports every such pair as **n/a** (18 of the 30 pairs) instead of as a finding.

Of the 12 statistically valid pairs, 4 survive Holm–Bonferroni correction — and all four are the same result: **botanical separates from both stochastic controls**, versus random and versus Voronoi, on Merit_Scaled (d = −0.79 and −1.05) and on Peak_AF (d = −0.86 and −1.19), with post-hoc power 0.85–0.99. Botanical sits consistently *below* the random and Voronoi controls; no claim is made about any comparison involving the seed-frozen morphologies. Merit_Scaled is an internal structural indicator within the abstract simulation space, not a physical performance measure.

Parametric robustness (v1.2.3, symmetric noise): under the symmetric noise regime (`noise_level=0.15` applied identically to all morphologies), botanical's curve separation from the random control holds across **100% of the 125-point k0 × beta × Q parameter grid** (5×5×5; see `outputs/robustness_matrix.csv`), with the botanical-vs-random separation ratio staying between 0.45 and 0.49 (well above the 0.10 threshold) at every grid point. The matrix also records the botanical-vs-fractal ratio (0.34–0.36) at each point for reference. The persistence under fair comparison conditions confirms the separation is a structural property of botanical morphology, not an artefact of perturbation or parameter tuning.

---

## Key Research Points

- **Perspective:** Application of signal processing, wave-interference modeling, and bio-inspired computational design to synthetic morphologies inspired by natural botanical branching structures.
- **Model:** Network-based representation using coupled oscillator systems, with Near-Field Magnetic Induction (NFMI) used strictly as conceptual inspiration for interaction topology design — not as a physical implementation or performance target.
- **Methodology:** Mapping of morphological geometry into abstract electromagnetic network representations for simulation, parameter exploration, and statistical comparison.
- **Validation:** Pre-simulation topology validation rejects degenerate structures before execution. Results are cross-validated against published Schumann resonance modes and stress-tested across five seeds per morphology.

Simulation baseline: [/data/parameters.json](./data/parameters.json)

---

## Objective

- Investigate whether morphological datasets can be used as structured inputs for generating consistent abstract network representations inspired by electromagnetic system analogies.
- Provide a reproducible computational framework for simulation, sensitivity analysis, and formal statistical comparison.
- Enable systematic comparison of geometric parameterizations under a unified modeling approach, with external baseline anchoring.

---

## Morphological Taxonomy Rationale

The five morphological types — fractal branching, botanical, random control, Fibonacci spiral, and Voronoi — are synthetic abstractions of structural patterns observable in nature. Each represents a distinct topology class: deterministic recursive structures, branching plant networks, unstructured spatial distributions, golden-ratio angular distributions, and proximity-based tessellations.

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

## Numerical Validation: Resonance and Response Structure

The repository includes a reproducible numerical model located at: [/data/node_resonance.py](./data/node_resonance.py)

This script evaluates resonance behavior and normalized response structure under ELF-inspired parameter regimes using lumped-element approximations.

### Model Definition

The resonance module evaluates normalized response behavior in a lumped-element RLC-inspired model using inductive, capacitive, and resistive parameters extracted from the simulation configuration. These parameters are treated as abstract numerical inputs for a simplified computational representation of oscillatory behavior.

The implemented metrics include:

- Resonance frequency (f_res)
- Quality factor (Q)
- Bandwidth estimation
- Peak-to-mean normalized response ratios

These quantities are used as comparative indicators within the simulation framework and are not interpreted as direct measurements of physical electromagnetic efficiency.

### External Baseline: Schumann Resonance

The simulated resonance frequency is compared against published Schumann resonance modes (NOAA/GFZ Potsdam). The simulated value of 12.9949 Hz positions at 9.13% deviation from mode 2 (14.30 Hz). References: Schumann 1952, Williams 1992, Nickolaenko & Hayakawa 2002.

**Note on baseline comparison:** The simulated resonance frequency follows from the stored RLC baseline in `data/parameters.json` (L ≈ 1.0 H, C ≈ 150 µF i.e. 1.5×10⁻⁴ F, R = 100 Ω), evaluated by `data/node_resonance.py`. Separately, `data/parameter_derivation.py` documents the closed-form f_target → L → C → f_check chain for the 12.5 Hz target (yielding C ≈ 162 µF i.e. 1.62×10⁻⁴ F); that derivation is documentation only and does not feed the simulation. The comparison to Schumann modes serves as an external reference frame for contextualizing the frequency regime of the model, not as a claim of physical equivalence or empirical proximity to natural ELF phenomena.

### Output

The simulation produces parametric baseline metrics. Typical numerical outputs include:

- Resonance frequency: **12.99 Hz**
- Quality factor (Q): **0.81**
- Bandwidth: **15.91 Hz**
- Effective transfer (k_eff): **2.92**

These values represent structural indicators derived from the simulated signal structure. **Note on Q:** A value of Q = 0.81 places the model in the overdamped regime (Q < 1), meaning the system does not sustain free oscillation in the strict physical sense. The coherence and merit metrics computed by the pipeline remain valid as comparative structural indicators across morphologies. The term "resonance frequency" here refers to the frequency of peak transfer function magnitude, not to sustained oscillation.

---

## Numerical Model: Distributed Phased Array (Beamforming)

The system is extended into a spatial network model: [/data/node_coupling.py](./data/node_coupling.py)

This module computes coherent field superposition using a phased array formulation applied to abstract node graphs. The terminology (array factor, phased array, beamforming) is borrowed from antenna engineering as a computational analogy. No physical antenna array is modeled.

The coupling model includes phenomenological scaling coefficients used to modulate coherence response, spatial sensitivity, and normalized quality-factor behavior across the parametric sweep. These coefficients are heuristic simulation parameters intended for exploratory system dynamics and do not represent experimentally derived electromagnetic constants.

### Spatial Configuration

Nodes are distributed dynamically based on the selected morphology (fractal, botanical, random control, Fibonacci spiral, or Voronoi control), comprising an array of N = 64 nodes.

**Geometric Treatment:** The transformation is strictly homotetic. The base topology remains fixed while the global scale is modulated continuously by a spacing parameter d from 0.1 to 2.0 meters (`positions = base_nodes * d`).

Phase assignments are applied cyclically across the N-node array to maintain controlled interference periodicity:

- Base sequence: **[0°, 90°, 180°, 270°]**

### Pre-simulation Topology Validation

Before each sweep executes, `data/topology_validator.py` validates the generated morphology using union-find with path-halving, minimum node count, and degenerate structure detection. Invalid topologies raise a `RuntimeError` and halt the pipeline.

### Scaling Parameter k0

The variable `k0_base` is a heuristic spatial scaling coefficient used to modulate the phase contribution of each node in the array factor computation. It is **not** the electromagnetic wave number k₀ = 2πf/c. At 12.99 Hz, the physical wave number would be k₀ ≈ 2.72×10⁻⁷ rad/m — several orders of magnitude smaller than the value used here. The discrepancy is intentional: the model operates in an abstract simulation space, not in physical electromagnetic space.

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

After all five sweeps complete, the pipeline executes formal statistical separation testing:

- **Curve-separation descriptor** (`outputs/curve_separation_summary.csv`, 7 columns: Metric, Pair, t_statistic, p_value, Significant_p05, Cohens_d, Effect_size): a Welch t-test + Cohen's d computed over the autocorrelated sweep steps for all 3 metric × 10 pair combinations (30 rows). This is a descriptive separation measure, not an independent-sample test.
- **Formal multi-seed inference** (`outputs/inference_summary.csv`): Welch t-test, Cohen's d, bootstrap CI, Holm-Bonferroni and post-hoc power over the N=30 per-seed means, with a variance-collapse guard that marks seed-frozen morphologies (fractal, Fibonacci) as `n/a`.

Multi-seed analysis runs each morphology through N=30 seeds (seeds 42–71) and reports mean ± std per metric, confirming result stability across random initializations.

---

## Sensitivity Analysis

A parametric sweep evaluates system response under continuous variation of the global spatial scale d. The visual analysis extracts and normalizes specific variables from the scalar CSV datasets.

The visualization generates a combined figure with two sections:

**Section 1 — Sensitivity Curves:** Normalized Coherence Ratio (`norm(c)`) and Normalized Merit Scaled (`norm(ms)`) across all five morphologies.

**Section 2 — Statistical Heatmaps:** p-value matrix (3 metrics × 10 pairs) where green = significant at p < 0.05, and |Cohen's d| matrix where blue intensity = effect size magnitude.

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

The implementation uses a hierarchical set of derived scaling variables (e.g. k0, k, k_eff) that operate at different stages of the simulation pipeline: base scaling initialization, coherence-modulated scaling, and post-response normalization. These variables are computational constructs used for numerical stability and do not represent a physically derived parameter hierarchy.

Within the resonance module, the scaling parameter is used as a direct linear scaling factor applied to the base inductance value (`L = scaling_constant_k * 1e-2`), producing L = 1.0 H as the effective inductance for the RLC model. This value is a design choice within the abstract simulation space, not a measured or derived physical quantity.

---

## Reproducibility

All simulations are fully deterministic given fixed seeds (default: 42). The pipeline is single-command executable (`python run.py`) with no external API calls or runtime downloads. Generated results are written to `outputs/` and regenerated on each run; the sensitivity figure is also committed at `data/sensitivity_analysis.png` for reference.

Pinned dependency versions are declared in `requirements.txt`. Environment reproducibility is further documented in `CHANGELOG.md`.