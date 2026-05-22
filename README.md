# Biotic Hardware Synthesis: A Computational Framework for Bio-Inspired ELF Resonant Architectures

This repository provides a reproducible computational framework for simulating structured network dynamics inspired by morphological datasets. It implements a full pipeline for parameter-driven simulation of coherence, phased-array behavior, and sensitivity analysis under geometric scaling, producing numerical outputs (CSV) and visualization artifacts (plots) from a single executable workflow.

It operates in Extremely Low Frequency (ELF) regimes using morphological datasets as structured inputs for abstract graph-based and lumped-element system modeling.

It implements a generative computational pipeline in which morphological structures (derived from MS 408 / Voynich Manuscript) are mapped into simplified electromagnetic analogues. These mappings enable the study of structural and dynamical properties within coupled-oscillator and network-based simulation frameworks.

The framework is designed for exploratory modeling, parametric sensitivity analysis, and structural experimentation in systems inspired by network physics and morphological computation. It situates these simulations within a computational context where structural consistency is evaluated using numerical electromagnetic models and lumped-element approximations.

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

- Node-level efficiency parametric analysis (radiation resistance limit regime $R_r \rightarrow 0$)
- Distributed Phased Array simulation (coherent field superposition via spatial phase coupling)
- Parametric sensitivity analysis of system response under geometric scaling

Outputs:

- Console logs of simulation results
- `data/simulation_results.csv`
- `data/sensitivity_analysis.png`

---

## Key Research Points

- **Perspective:** Application of signal processing, electromagnetic modeling, and bio-inspired computational design to morphological datasets extracted from MS 408.
- **Model:** Network-based representation using Near-Field Magnetic Induction (NFMI) analogies and coupled oscillator systems.
- **Methodology:** Mapping of morphological geometry into abstract electromagnetic network representations for simulation and parameter exploration.

Simulation baseline:  
[/data/parameters.json](./data/parameters.json)

---

## Objective

- Investigate whether morphological datasets can be used as structured inputs for generating consistent electromagnetic network representations.
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
- **Modulation and Filtering:** Structural symmetries mapped to frequency-selective behavior in lumped-element systems.
- **Inductive Coupling:** Geometric branching interpreted as coupling motifs in NFMI-inspired networks.
- **Phase Synchronization:** Radial structures represented as phase-coupled oscillators.
- **Material Layering:** Structural variation mapped to parameter heterogeneity (loss, damping, coupling strength).

These mappings are used strictly for computational simulation.

---

## Numerical Validation: Node-Level Efficiency Limits

The repository includes a reproducible numerical model located at:

[/data/node_resonance.py](./data/node_resonance.py)

This script evaluates the efficiency regime under ELF conditions, where radiation resistance approaches limiting values ($R_r \rightarrow 0$).

### Model Definition

The efficiency metric is defined as:

$$
\eta = \frac{R_r}{R_r + R_{loss}}
$$

Parameters:

- $R_r \approx 1 \times 10^{-9} \ \Omega$
- $R_{loss} \in [100, 1000] \ \Omega$

### Output

The simulation produces efficiency values in the order of:

- $10^{-11}$ to $10^{-12}$

This characterizes the low-efficiency regime of isolated-node emission under the assumed constraints.

---

## Numerical Model: Distributed Phased Array (Beamforming)

The system is extended into a spatial network model:

[/data/node_coupling.py](./data/node_coupling.py)

This module computes coherent field superposition using a phased array formulation.

### Spatial Configuration

Nodes are arranged on a 2D grid with spacing parameter $d \in [0.1, 0.4]$ meters.

Phase assignments:

- Node 1: 0°
- Node 2: 90°
- Node 3: 180°
- Node 4: 270°

### Outputs

- Array Factor (AF)
- Peak field amplitude
- Mean field distribution
- Coherence ratio
- CSV dataset for parametric sweep

---

## Sensitivity Analysis

A parametric sweep evaluates system response under variation of node spacing $d$.

The analysis computes:

- Peak Array Factor
- Coherence ratio
- Derived structural performance metrics

Outputs:

- `data/simulation_results.csv`
- `data/sensitivity_analysis.png`

---

## Integration: Theory vs Computational Implementation

This repository implements a computational validation of the **coherence and beamforming behavior** defined in the theoretical model.

The associated document [Functional Patterns and Electromagnetic Hypotheses in MS 408.md](./docs/Functional%20Patterns%20and%20Electromagnetic%20Hypotheses%20in%20MS%20408.md) defines a **theoretical parameter space for the full system model**, including structural variables such as permeability coefficients, coupling regimes, and energy-transfer analogues.

The README specifies the implemented computational subset of this space.

The current implementation focuses exclusively on the **network synchronization kernel**, which evaluates:

- phase coherence  
- distributed coupling stability  
- emergent beamforming behavior in graph-based oscillator networks  

Modules related to energy conversion (e.g. plasma-like transitions, piezoelectric-like coupling) are treated as **architectural specifications** within the theoretical parameter space and are not instantiated in the current simulation layer.

This separation reflects a **layered abstraction model**, where:

- the theoretical model defines the **full parameterized system space**  
- the implementation evaluates a **restricted subset of dynamical behaviors** within that space  

The parameter **k** is defined as a **schematic spatial scaling factor** representing the mapping between normalized geometric space and simulation space. It is not derived from electromagnetic wave propagation constants. Consequently, it is not directly coupled to material parameters such as **permeability (μr)**; both operate as independent parameters within the modeling abstraction.

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