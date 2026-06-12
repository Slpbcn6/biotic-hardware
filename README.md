# Biotic Hardware Synthesis: A Computational Framework for Morphological Benchmarking in ELF-Inspired Coupled-Oscillator Networks

![Biotic Hardware Synthesis](assets/readme1-2-2.svg)


This repository provides a reproducible computational framework for simulating structured network dynamics inspired by morphological datasets. It implements a full pipeline for parameter-driven simulation of coherence metrics, phase-based interference behavior (complex-valued phasor summation), sensitivity analysis under parametric variation, and formal statistical separation testing — producing numerical outputs, statistical artifacts, and visualization from a single executable workflow.

It operates under an ELF-inspired scalar parameterization using morphological datasets as structured inputs for abstract graph-based and lumped-element system modeling. All electromagnetic terminology used throughout (ELF, phased array, array factor, k0, NFMI) is applied in an analogical and computational sense. No physical electromagnetic system is modeled or implied.

It implements a generative computational pipeline in which morphological structures (associated with MS 408 / Voynich Manuscript treated strictly as a non-semantic morphological dataset) are mapped into simplified wave-interference and oscillator analogues inspired by abstract electromagnetic-style system analogies. These mappings enable the study of structural and dynamical properties within coupled-oscillator and network-based simulation frameworks.

The framework is designed for exploratory modeling, parametric sensitivity analysis, structural experimentation, and morphological comparison with formal statistical validation. It situates these simulations within a computational context where structural consistency is evaluated using numerical wave-interference-inspired mathematical models and lumped-parameter abstractions.

Procedural morphology generators (e.g., fractal and botanical structures) are structurally integrated into the main execution pipeline. These modules drive the deterministic benchmarking sequence via the `run.py` orchestrator, mapping structural inputs to spatial matrices before computing the array factor.

The system is strictly computational and interpretative. It does not represent a physical or biological implementation.

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

This executes the complete 11-step workflow:

- Parameter derivation: closed-form L/C derivation from the target frequency (f_target → L → C → f_check at 12.5 Hz)
- Node-level resonance baseline and external Schumann resonance comparison (NOAA/GFZ Potsdam, modes 1–5)
- Pre-simulation topology validation per sweep (connectivity, node count, degenerate structure detection)
- Distributed Phased Array simulation (phase-based interference superposition) across five morphologies: fractal, botanical, random control, Fibonacci spiral, and Voronoi control
- Statistical separation testing: Welch t-test + Cohen's d across 3 metrics and 10 morphology pairs
- Parametric sensitivity analysis and visualization of system response under geometric scaling
- Multi-seed analysis: mean ± std distributions across seeds 42–46
- Parametric robustness sweep: k0 × beta × Q grid (48 combinations) confirming botanical separation is structural, not a tuning artifact

Outputs (generated artifacts are written to `outputs/`):

- Console logs of simulation results with per-sweep summary metrics
- `outputs/resonance_params.json` (node resonance baseline: f_resonance, Q factor)
- `outputs/simulation_results_{fractal,botanical,random,fibonacci,voronoi}.csv` (Scalar Benchmark Contract)
- `outputs/af_tensors_{fractal,botanical,random,fibonacci,voronoi}.npz` (Tensor Research Layer)
- `outputs/statistical_summary.csv` (Welch t-test + Cohen's d, 30 rows)
- `outputs/multi_seed_summary.csv` (mean ± std per morphology, seeds 42–46)
- `outputs/exploration_summary.json` (machine-readable experiment record)
- `outputs/sensitivity_analysis.png` — sensitivity curves + statistical heatmaps (also written to `data/sensitivity_analysis.png`)
- `outputs/robustness_matrix.csv` (parametric robustness grid: 48 combinations of k0, beta, Q; records p and Cohen's d for botanical vs random at each point)

---

## Principal Finding (v1.2.2)

On Merit_Scaled, 9 of the 10 morphology pairs separate at p < 0.05; the sole non-significant pair is fractal vs random control (p = 0.484, d = 0.182). The two synthetic controls bound the metric range: Voronoi yields the highest Merit_Scaled (multi-seed mean 0.0575) and Fibonacci the lowest (0.0089), each separating from every other morphology with large effect (|d| > 1.1). Botanical separates from fractal (p = 0.026, d = −0.593, medium effect) and from random control (p = 0.008, d = 0.714, medium effect). Multi-seed analysis confirms the result is structural: botanical, random, and Voronoi carry seed-dependent variance (std ≈ 0.007–0.012), while fractal and Fibonacci are seed-stable (std ≈ 0.0005–0.0009). Merit_Scaled is an internal structural indicator within the abstract simulation space, not a physical performance measure.

Parametric robustness (v1.2.2, symmetric noise): under the corrected symmetric noise regime (`noise_level=0.15` applied identically to all morphologies), botanical separation holds across **100% of the 48-point k0 × beta × Q parameter grid** (see `outputs/robustness_matrix.csv`), with Cohen's d ranging from 0.642 to 0.840 across all combinations. The persistence under fair comparison conditions confirms the result is a structural property of botanical morphology, not an artefact of asymmetric perturbation.

---

## Key Research Points

- **Perspective:** Application of signal processing, wave-interference modeling, and bio-inspired computational design to morphological datasets extracted from MS 408.
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

## Dataset Rationale (MS 408)

MS 408 (Voynich Manuscript) is used as a morphological dataset.

The dataset is not interpreted in historical or semantic terms. It is used strictly as a high-complexity structural input for testing abstraction and mapping methods.

Within this framework, MS 408 functions as:

- a high-complexity structural benchmark
- a non-semantic morphological input source
- a testbed for robustness of network generation methods

Alternative datasets with similar structural properties (synthetic fractals, botanical diagrams, procedural geometries) are compatible with this framework.

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

- **Welch t-test** (unequal variance, `scipy.stats.ttest_ind(equal_var=False)`): robust comparison across all 3 metric × 10 pair combinations (30 rows).
- **Cohen's d** effect size: small (< 0.5), medium (0.5–0.8), large (> 0.8).
- Output: `outputs/statistical_summary.csv` (7 columns: Metric, Pair, t_statistic, p_value, Significant_p05, Cohens_d, Effect_size).

Multi-seed analysis runs each morphology through seeds 42–46 and reports mean ± std per metric, confirming result stability across random initializations.

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