# Biotic Hardware Synthesis: A Computational Framework for Bio-Inspired ELF Resonant Architectures

This repository provides a reproducible computational framework for simulating structured network dynamics inspired by morphological datasets. It implements a full pipeline for parameter-driven simulation of coherence metrics, phase-based interference behavior (complex-valued phasor summation), and sensitivity analysis under parametric variation, producing numerical outputs and visualization artifacts from a single executable workflow.

It operates under an Extremely Low Frequency (ELF)-inspired scalar parameterization using morphological datasets as structured inputs for abstract graph-based and lumped-element system modeling.

It implements a generative computational pipeline in which morphological structures (associated with MS 408 / Voynich Manuscript treated strictly as a non-semantic morphological dataset) are mapped into simplified wave-interference and oscillator analogues inspired by abstract electromagnetic-style system analogies. These mappings enable the study of structural and dynamical properties within coupled-oscillator and network-based simulation frameworks.

The framework is designed for exploratory modeling, parametric sensitivity analysis, and structural experimentation. It situates these simulations within a computational context where structural consistency is evaluated using numerical wave-interference-inspired mathematical models and lumped-parameter abstractions.

Procedural morphology generators (e.g., fractal and botanical structures) are structurally integrated into the main execution pipeline. These modules drive the deterministic benchmarking sequence via the `run.py` orchestrator, mapping structural inputs to spatial matrices before computing the array factor.

The system is strictly computational and interpretative. It does not represent a physical or biological implementation.

---

## Requirements

Install dependencies before running the pipeline:

    pip install -r requirements.txt

---

## Quick Start

To run the full computational simulation pipeline:

    python run.py

This executes the complete workflow:

- Node-level resonance and normalized response analysis in a lumped-element RLC-inspired system
- Distributed Phased Array simulation (phase-based interference superposition)
- Parametric sensitivity analysis of system response under geometric scaling

Outputs:

- Console logs of simulation results
- `data/simulation_results_fractal.csv` & `data/simulation_results_botanical.csv` (Scalar Benchmark Contract)
- `data/af_tensors_fractal.npz` & `data/af_tensors_botanical.npz` (Tensor Research Layer)
- `data/sensitivity_analysis.png`

---

## Key Research Points

- **Perspective:** Application of signal processing, wave-interference modeling, and bio-inspired computational design to morphological datasets extracted from MS 408.
- **Model**: Network-based representation using coupled oscillator systems, with Near-Field Magnetic Induction (NFMI) used strictly as conceptual and structural inspiration for interaction topology design.
- **Methodology:** Mapping of morphological geometry into abstract electromagnetic network representations for simulation and parameter exploration.

Simulation baseline:  
[/data/parameters.json](./data/parameters.json)

---

## Objective

- Investigate whether morphological datasets can be used as structured inputs for generating consistent abstract network representations inspired by electromagnetic system analogies.
- Provide a reproducible computational framework for simulation and sensitivity analysis.
- Enable systematic comparison of geometric parameterizations under a unified modeling approach.

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
- **Modulation and Filtering**: Structural symmetries mapped to abstract response modulation within lumped-parameter simulation components.
- **Inductive Coupling:** Geometric branching interpreted as coupling motifs in NFMI-inspired networks.
- **Phase Synchronization:** Radial structures represented as phase-coupled oscillators.
- **Material Layering:** Structural variation mapped to parameter heterogeneity (loss, damping, coupling strength).

These mappings are used strictly for computational simulation.

---

## Numerical Validation: Resonance and Response Structure

The repository includes a reproducible numerical model located at:

[/data/node_resonance.py](./data/node_resonance.py)

This script evaluates resonance behavior and normalized response structure under ELF-inspired parameter regimes using lumped-element approximations.

### Model Definition

The resonance module evaluates normalized response behavior in a lumped-element RLC-inspired model using inductive, capacitive, and resistive parameters extracted from the simulation configuration. These parameters are treated as abstract numerical inputs for a simplified computational representation of oscillatory behavior.

The implemented metrics include:

- Resonance frequency (f_res)
- Quality factor (Q)
- Bandwidth estimation
- Peak-to-mean normalized response ratios

These quantities are used as comparative indicators within the simulation framework and are not interpreted as direct measurements of physical electromagnetic efficiency.

### Output

The simulation produces parametric baseline metrics. Typical numerical outputs include:

- Resonance frequency: **12.99 Hz**
- Quality factor (Q): **0.81**
- Bandwidth: **15.91 Hz**
- Effective transfer (k_eff): **2.92**

These values represent efficiency metrics derived from the simulated signal structure.

---

## Numerical Model: Distributed Phased Array (Beamforming)

The system is extended into a spatial network model:

[/data/node_coupling.py](./data/node_coupling.py)

This module computes coherent field superposition using a phased array formulation.

The coupling model includes phenomenological scaling coefficients used to modulate coherence response, spatial sensitivity, and normalized quality-factor behavior across the parametric sweep. These coefficients are heuristic simulation parameters intended for exploratory system dynamics and do not represent experimentally derived electromagnetic constants.

### Spatial Configuration

Nodes are distributed dynamically based on the selected morphology (fractal or botanical), comprising an array of N = 64 nodes. 

**Geometric Treatment:** The transformation is strictly homotetic. The base topology remains fixed while the global scale is modulated continuously by a spacing parameter d from 0.1 to 2.0 meters (`positions = base_nodes * d`). 

Phase assignments are applied cyclically across the N-node array to maintain controlled interference periodicity:

- Base sequence: **[0°, 90°, 180°, 270°]**

### Data Export Architecture (Dual Layer)

To maintain a clean analytical contract while enabling deep research, the system bifurcates the computed data into two explicit layers:

#### 1. Scalar Output (Benchmarking Contract)
Exported as `data/simulation_results_*.csv`. Contains strictly the reduced variables for the analytical pipeline:

- `Distance` (Spatial scaling parameter)
- `Peak_AF` (Maximum amplitude of the Array Factor)
- `Coherence_Ratio` (Peak-to-mean field distribution ratio)
- `Merit_Function` (Base structural performance)
- `Q_effective` (Density-dependent dynamic regularization)
- `Merit_Scaled` (Post-transformation metric)

#### 2. Tensor Output (Research Layer)
Exported as `data/af_tensors_*.npz`. Contains the preserved latent state of the system for advanced topological analysis:

- `distance`: Full array of scaling steps.
- `mean`: The raw mean field distribution magnitude per step.
- `af`: The complete 200-point Array Factor magnitude vector per step.

---

## Sensitivity Analysis

A parametric sweep evaluates system response under continuous variation of the global spatial scale d. The visual analysis extracts and normalizes specific variables from the scalar CSV datasets.

The visualization plots:

- Normalized Coherence Ratio (`norm(cf)`)
- Normalized Merit Scaled (`norm(msf)`)

Outputs:

- `data/sensitivity_analysis.png`

---

## Integration: Theory vs Computational Implementation

This repository implements a computational validation of the coherence and beamforming behavior defined in the theoretical model.

The associated document [Morpho-Topological Framework and Parameter Space.md](./docs/Morpho-Topological%20Framework%20and%20Parameter%20Space.md) defines a theoretical parameter space for the full system model, including structural variables such as permeability coefficients, coupling regimes, and energy-transfer analogues.

The README specifies the implemented computational subset of this space.

The current implementation focuses exclusively on the network synchronization kernel, which evaluates:

- phase coherence  
- distributed coupling stability  
- emergent beamforming behavior in graph-based oscillator networks  

Modules related to energy conversion (e.g. plasma-like transitions, piezoelectric-like coupling) are treated as architectural specifications within the theoretical parameter space and are not instantiated in the current simulation layer.

This separation reflects a layered abstraction model, where:

- the theoretical model defines the full parameterized system space  
- the implementation evaluates a restricted subset of dynamical behaviors within that space  

The parameter **k** is defined as a schematic spatial scaling factor representing the mapping between normalized geometric space and simulation space. It is not derived from electromagnetic wave propagation constants. Consequently, it is not directly coupled to material parameters such as permeability (μr); both operate as independent parameters within the modeling abstraction.

The implementation uses a hierarchical set of derived scaling variables (e.g. k0, k, k_eff) that operate at different stages of the simulation pipeline: base scaling initialization, coherence-modulated scaling, and post-response normalization. These variables are computational constructs used for numerical stability and do not represent a physically derived parameter hierarchy.

Within the resonance module, the scaling parameter is used as a direct linear scaling factor applied to the inductance term for numerical convenience within the lumped-element model. This operation is purely computational and does not represent a physically derived transformation.

---

## Important Clarification

This project is a **computational and conceptual modeling framework**.

It does not claim:

- Historical or physical interpretation of MS 408
- Biological or physical implementation of proposed systems
- Experimental validation of electromagnetic behavior in biological structures

It provides:

- A reproducible simulation environment
- A structural abstraction framework
- A sensitivity analysis pipeline for exploratory modeling

All terminology is used strictly within a computational and analogical context.

---

## v1.1 - Morphological Benchmark Pipeline

This version introduces a deterministic benchmarking pipeline for comparing system dynamics under different structural inputs.

### Pipeline Structure & Execution State

- Morphology generation (fractal / botanical)
- Geometric mapping of node positions
- Array factor computation
- Data reduction and tensor persistence
- Plotting metrics

**Crucial Note on Execution State:** The orchestrator (`run.py`) executes a sequential benchmark by globally mutating the `data/parameters.json` file to switch between morphologies. This means the system acts as a *stateful determinist framework*. Running `data/node_coupling.py` independently outside of `run.py` will yield results exclusively tied to the last preserved configuration state of the JSON file.

### Purpose

This version ensures reproducible comparison of morphological configurations under identical, automated simulation conditions, while preserving the full tensor state for decoupled computational analysis.

---

## References

- Near-Field Magnetic Induction Communication (NFMI) – A Review  
  https://doi.org/10.1016/j.comnet.2020.107548  

- Magnetic Induction Communication: Theory and Applications  
  https://doi.org/10.1109/TAP.2010.2048858  

- Extremely Low Frequency (ELF) Electromagnetic Wave Propagation  
  https://www.nature.com/articles/s41598-024-71011-3  

- Metamaterial-Inspired Antennas: State of the Art and Design Challenges  
  https://doi.org/10.1109/ACCESS.2021.3091479  

- Bio-Inspired Electromagnetic Materials and Structures  
  https://doi.org/10.1021/acsami.2c21622  

- Piezoelectric Properties of Cellulose-Based Materials  
  https://doi.org/10.1016/j.carbpol.2025.124667