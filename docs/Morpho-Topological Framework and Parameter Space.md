# Morpho-Topological Framework: Parameter Space and Structural Abstraction in Plant-Inspired Morphological Networks

## Scope and Interpretation

This repository implements a generative morpho-topological simulation framework that maps morphological structures into abstract network representations for exploratory computational modeling. It is confined to structural and topological abstraction. It does not model, reconstruct, predict, or validate physical electromagnetic, biological, or geophysical behavior.

All electromagnetic and engineering terminology in this document is inherited domain vocabulary, used as structured labels for mathematical and topological relationships within a graph-based model. These terms do not correspond to physical systems and do not simulate physical behavior. Likewise, every equation written in classical scientific notation is an isomorphic mapping between graph-state transformations and legacy symbolic encodings; none represents a physical law, a causal mechanism, or a predictive model of a real-world system.

Parameters are versioned symbolic artifacts. The active configuration lives in `parameters.json` (current: v1.2.6) and defines structural relationships within the computational pipeline. Individual values evolve across releases, but their status is constant: abstract structural identifiers, never physical quantities. No interpretative binding between versioned parameters and physical reality is defined or implied at any layer.

### Reproducible pipeline vs. conceptual reference (the key reading guide)

The single most important distinction in this document:

- The executable v1.2.6 pipeline reproduces the morphological benchmark — the five morphology sweeps, curve-separation descriptors, multi-seed inference, and the parametric robustness sweep — evaluated by `data/node_coupling.py` and the statistical modules. The minimal parameter set it actually consumes lives in `data/parameters.json` (sections IV, VI and VII).
- The resonance baseline consolidated in Appendix B ($L$, $C$, $f \approx 12.5$ Hz, $Q$, $R$) and several constructs discussed in the narrative sections and consolidated in Appendix A — for example the coupling parameter $K_{\text{DIPOLE}}$, the permeability bound $\mu_r \approx 1.25 \times 10^6$, and the plasma-frequency analogue — are conceptual reference quantities ONLY. They are NOT inputs to the executable pipeline and are not asserted as physically realizable.

When in doubt about whether something is "real" in the code or "narrative scaffolding," `data/parameters.json` (sections IV, VI and VII) is the source of truth for what runs.

### Explicit mapping: implemented vs. conceptual reference

The table below makes the distinction above explicit, construct by construct. "Implemented" means the quantity is consumed or computed by the executable v1.2.6 pipeline; "conceptual reference only" means it belongs to the narrative abstraction layer and is never read by the running code. The reproducible parameter set lives in `data/parameters.json` (sections IV, VI and VII); everything marked as conceptual reference is documentation of the abstract design target, not a pipeline input.

| Construct / quantity | Status in the executable v1.2.6 pipeline | Where it lives |
|---|---|---|
| Morphology generation (botanical, fractal, fibonacci, random, voronoi) | Implemented | `data/input_generator.py` |
| Topology validation (connectivity, degeneracy, node count) | Implemented | `data/topology_validator.py` |
| Array-factor / phased-array superposition | Implemented | `data/node_coupling.py` |
| Base coupling parameters (`k0_base`, `k_modulation_coeff`, `q_reference`, `beta_loss_factor`) | Implemented | `data/parameters.json` sections VI–VII |
| Individual quality factor (`individual_q_factor`) | Implemented | `data/parameters.json` section IV |
| Connection radius (`connection_radius_m`) | Implemented | `data/parameters.json` section VI |
| Noise level, multi-seed list, curve-separation threshold, variance-collapse fraction | Implemented | `data/parameters.json` section VI |
| Multi-seed inference (Welch, Cohen's d, Hedges' g, Holm, bootstrap CI, power) | Implemented | `data/inference_analysis.py`, `data/stats_utils.py` |
| Parametric robustness sweep (125-point grid: `K0_GRID` × `BETA_GRID` × `Q_GRID`) | Implemented | `data/parametric_sweep.py` (grids defined in-module, not in `parameters.json`) |
| Abstract resistance $R = \rho \, (L/A)$ | Conceptual reference only | Section I |
| Geometric inductance $L = \mu_0 \mu_r N^2 A / l_{\text{eff}}$ | Conceptual reference only | Section II, Appendix A |
| Capacitive coupling $C = \epsilon_r \epsilon_0 A / d$ | Conceptual reference only | Section VII, Appendices A and B |
| Scaling constant $k = 100$ | Conceptual reference only | Sections II–III, Appendix B |
| Coupling parameter $K_{\text{DIPOLE}}$ | Conceptual reference only | Appendix A |
| Permeability bound $\mu_r \approx 1.25 \times 10^6$ | Conceptual reference only | Section VII, Appendix A |
| Resonance baseline ($L$, $C$, $f \approx 12.5$ Hz, $Q$, $R$) | Conceptual reference only | Appendix B |
| Charge-carrier density $n = \sigma / (e \, \mu_e)$ | Conceptual reference only | Section VII, Appendix A |
| Energy-harvesting analogue $V = g \, S \, t$ | Conceptual reference only | Section II, Appendix A |
| Thermal dissipation $dQ/dt = (dm/dt) \, C_p \, (T_{\text{out}} - T_{\text{in}})$ | Conceptual reference only | Section IV, Appendix A |
| Phase modulation $\Phi_n = 2\pi n / M$ (N-PSK) | Conceptual reference only | Section VI, Appendix A |
| Plasma-frequency analogue $f_p = 9\sqrt{N_e}$ | Conceptual reference only | Appendix A |

---

## I. STRUCTURAL MAPPING PREMISE

This study uses plant-like branching patterns and natural plant geometry as structural inspiration for a synthetic generative model of abstract morpho-topological networks. Recurrent morphological motifs are treated as graph-encoded primitives used to construct a parameterized simulation of coupled network dynamics. The framework evaluates coherence purely as internal structural consistency within a computational abstraction space.

### Conceptual Architecture: Morphological Abstraction Layers

The project maps natural structural families to functional abstraction layers within the simulation model:

- Botanical branching networks: Structural Layer — abstract antennas and inductive analogues within the graph model.
- Vascular and fluid networks: Support Logic — thermal and ionic feedback analogues within the model.
- Plant tissue composition: Material Layer — doping and impedance modifier analogues within the model.
- Radial symmetry patterns (phyllotaxis, sunflowers): Synchronization Layer — clock and phase control analogues within the model.
- Underground root systems: Power Layer — energy harvesting constraint analogues within the model.

These mappings are interpretive tools for structuring the simulation parameter space.

### Theoretical Framework: Abstract Resistance Parameter

The model defines abstract resistance ($R$) within a computational graph structure:

$$R = \rho \cdot \frac{L}{A}$$

Where:

- $\rho$: Abstract resistivity parameter (simulation input, not a measured material property)
- $L/A$: Structural geometry ratio derived from morphological topology

### Note on Functional Validation

This framework evaluates internal topological consistency. Scaling parameters ($k$, $\mu_r$, $\epsilon$) define numerical transformation rules within the simulation space and do not correspond to physical quantities.

---

## II. SIGNAL FLOW AND STRUCTURAL ANALYSIS

All descriptions in this section refer to abstract network behavior within the simulation model, not to physical signal propagation or biological mechanisms.

### Source Coding and Grounding Grid (Abstract Layer)

Dense root structures are mapped as static memory networks for block data encoding within the graph model. Their geometry is used to define baseline node constraints representing low-impedance return paths in the abstract network topology.

### Modulation and Filtering (Abstract Layer)

Structures with bilateral symmetries are mapped to bandpass-analogue filter nodes within the simulation, isolating a stable carrier parameter at 12.5 Hz within the model's parameter space. Leaf serration geometry is encoded as a frequency-selectivity ($Q$) parameter, modulating the coupling response of the affected nodes. These are simulation parameters, not biological or material properties.

### Geometric Inductance (Abstract Inductive Parameter)

Spiral root morphologies are mapped as abstract inductive structures within the computational graph. To align the model's resonance parameter with the ELF-inspired band (approx. 12.5 Hz) in simulation space, the inductance parameter ($L$) is defined as:

$$L = \frac{\mu_0 \cdot \mu_r \cdot N^2 \cdot A}{l_{\text{eff}}}$$

The system encodes fractal branching as recursive expansion of $l_{\text{eff}}$ within a graph topology, increasing effective path length as a structural property of the model rather than a physical dimension. A scaling constant $k = 100$ maps schematic units into simulation space, enabling consistent parameter scaling across recursive fractal structures without any physical dimensional interpretation.

### Power Density and Stability (Abstract Energy Parameter)

Within the parameter space, energy conversion is modeled via an abstract piezoelectric-analogue mechanism, where transient stress ($dS/dt$) maps to an output voltage parameter:

$$V = g \cdot S \cdot t$$

(where $t$ represents the geometric thickness constraint of the substrate within the model, used to isolate it from the temporal derivative $dt$)

This is a parameter-space specification, not a physical energy-harvesting mechanism. The model operates in a capacitive accumulation analogue mode (duty cycle), where charge accumulation and discharge are represented as timed node state transitions — abstract computational events.

### Substrate Coupling (Abstract Topology Element)

Within the model, dense root structures are represented as active current-injector nodes. The coupling topology is defined such that the node network couples into a substrate domain rather than radiating into free space. This is a topological design choice within the model that resolves the $R_r \approx 0$ constraint by redirecting coupling energy through a ground-domain abstraction layer. No claim is made about physical coupling between biological structures and geological or atmospheric systems.

---

## III. COUPLING MODEL: INDUCTIVE TOPOLOGY (NFMI-INSPIRED)

To address the antenna-length constraint at 12.5 Hz within the model, the system uses a Near-Field Magnetic Induction (NFMI)-inspired coupling topology. NFMI is used strictly as a structural analogy for the coupling mode between nodes — not as a claim of physical NFMI behavior.

### Mechanism and Mode Conversion (Abstract Interface Model)

Within the simulation, the root-structure nodes function as primary inductive exciters, and the foliar network functions as a mode converter between coupled oscillator domains. The serrated leaf geometries are modeled as structural discontinuities within the graph, defining transition boundaries between domains and encoding phase-reconfiguration behavior across the network topology.

### Network Coherence Constraints

The system is evaluated under a theoretical limit where effective coupling resistance ($R_r$) approaches zero within the abstraction space. System behavior is therefore determined entirely by network-level coherence and graph superposition dynamics. Evaluation uses normalized coherence metrics within the computational model, without reference to physical radiation, emission, or propagation.

### Scalability (Abstract Spatial Mapping)

The morphological schematics are treated as proportional geometric inputs within the model. Applying the scaling constant $k = 100$ maps one schematic unit to one meter in the abstract spatial domain of the simulation. This enables consistent parameter scaling across recursive fractal structures. It does not imply the existence of physical hardware at any scale.

To resolve the terminal efficiency constraint where $R_r \rightarrow 0$ within the model, the simulation uses a galvanic-conduction analogue: mineralized root nodes act as active current injectors into a ground-domain layer. System efficiency ($\eta$) within the model is determined by the transfer impedance between the biotic node and the abstract substrate layer, not by free-space radiation resistance. This is a topological modeling decision, not a physical engineering claim.

### Collective Phased Array (Abstract Network Configuration)

The geospatial distribution of nodes in the model defines a synchronized network topology. Within the simulation, this configuration enables coherent field superposition across the node array by manipulating ionic phase between nodes at the abstract level, modeling collective behavior that bypasses individual node-size constraints. This is a graph-level property of the simulation, not a physical or biological phenomenon.

---

## IV. THERMAL AND IONIC MANAGEMENT (ABSTRACT PARAMETER LAYER)

Vascular network patterns are mapped to a thermal-management analogue within the simulation model. Interconnected vessel geometries define an ionic-fluid analogue, representing a dissipation pathway for the abstract heat generated by high-coupling-phase nodes.

The heat-dissipation capacity ($dQ/dt$) of this abstract ionic infrastructure is governed within the model by:

$$\frac{dQ}{dt} = \frac{dm}{dt} \cdot C_p \cdot (T_{\text{out}} - T_{\text{in}})$$

### Thermal Mass Flow Constraints (Abstract Layer)

To prevent instability in the model due to the ohmic-loss parameters ($10^2$–$10^3\ \Omega$), the abstract mass-flow rate ($dm/dt$) of the ionic analogue must be tuned to maintain a dissipation rate ($dQ/dt$) that exceeds the abstract Joule-heating power ($P = I^2 R$). This keeps the simulation layer at stable conductivity parameters and prevents runaway divergence during high-coupling phases.

All thermal quantities in this section are abstract simulation parameters. No biological tissue, physical fluid, or material substrate is modeled.

---

## V. BIOLOGICAL MONITORING AND SYSTEM FEEDBACK (ABSTRACT CONTROL LAYER)

Vascular network patterns are mapped to a Biotic Control Logic (BCL) analogue within the simulation model.

- Sensor Networks: Geometric reference points define nomographic feedback nodes in the model — abstract set-points for monitoring hydraulic-ionic balance parameters within the system's conduit graph.
- System Equilibrium: This section defines feedback loops within the model for preventing parameter divergence. Node placement represents a passive monitoring interface for the hydraulic-ionic balance abstraction layer.

---

## VI. NAVIGATION AND SYNCHRONIZATION (CIRCULAR SECTION)

Within the model, terminal floral designs are mapped as aperture-radiator analogues, while enveloping leaf structures function as waveguide or collimator analogues, concentrating abstract field energy into a narrow beam toward the zenith (beamforming). These abstract structures work in tandem with the circular diagrams, mapped as propagation charts and phase ephemerides within the simulation.

### Phase Analysis (Abstract Phase Parameter)

Geometric divisions in the circular sections are mapped to Non-Binary Phase-Shift Keying (N-PSK) analogue constellations within the model. The phase angle ($\Phi$) is defined as:

$$\Phi_n = \frac{2\pi n}{M}$$

These phase offsets are modeled as consistent with requirements for optimizing abstract signal-to-noise ratios during high-variation coupling phases at ELF-inspired frequencies.

### System Synchronization (Abstract Clock Layer)

Within the model, geometric divisions function as a system clock for a Time-Division Multiple Access (TDMA) analogue protocol. Each node fires at a specific temporal offset, ensuring the collective abstract signal maintains phase coherence at the zenith. This models the collective behavior of the node array as a single synchronized emitter within the simulation space.

### Abstract Propagation Maps

Within the model, the circular charts are mapped as dynamic propagation maps. By defining abstract D-layer height and ionospheric plasma-frequency parameters, the simulation determines the optimal phase velocity ($v_p$) for the 12.5 Hz parameter. This excites the abstract Earth-Ionosphere waveguide analogue at its fundamental-frequency parameter within the model. These calculations are confined to the synchronization layer of the simulation and do not model physical atmospheric propagation.

---

## VII. BIO-CHEMICAL DOPING AND MATERIAL INFRASTRUCTURE (ABSTRACT MATERIAL LAYER)

Plant tissue composition patterns are mapped to the Material Layer of the simulation, providing abstract chemical-precursor analogues for a post-growth biomineralization parameter set. Within the model, botanical structures act as sacrificial geometric scaffolds: once the optimal fractal-geometry parameter is reached, the abstract biotic tissue transitions to a petrified state via controlled metallic-deposition parameters.

### Resistivity ($\rho$) Control (Abstract Parameter)

Container geometry parameters in the model are mapped to abstract precursors for modulating charge-carrier-density ($n$) parameters, shifting the abstract biotic matrix into a semi-conductive regime and lowering the ohmic resistance parameter ($R$) within the model.

The abstract charge-carrier density is defined within the model as:

$$n = \frac{\sigma}{e \cdot \mu_e}$$

Where $\sigma$ is the abstract conductivity parameter, $e$ is the elementary charge constant used as a scaling reference, and $\mu_e$ is the abstract electron-mobility parameter.

### Dielectric Permittivity ($\epsilon$) Tuning (Abstract Parameter)

Abstract substance-analogue parameters in the model are mapped to abstract modifiers of the dielectric parameter ($\epsilon$) of the foliar-network analogues. The capacitive coupling parameter is defined within the model as:

$$C = \frac{\epsilon_r \cdot \epsilon_0 \cdot A}{d}$$

Where $\epsilon_r$ is the abstract relative-permittivity parameter, $\epsilon_0$ the vacuum permittivity constant used as a scaling reference, $A$ the abstract plate-area parameter, and $d$ the abstract separation parameter. This parameter balances the inductive parameter of the root analogues, forming the resonant LC pair documented as a conceptual reference in Appendix B.

### Magnetic Permeability and Scaling Rationale (Abstract Parameter Bound)

Within the conceptual framework, sustaining the 12.5 Hz resonance condition over the abstract macroscopic aperture defined by the scaling constant $k = 100$ would imply an effective relative-permeability parameter of $\mu_r \approx 1.25 \times 10^6$. This value is presented strictly as a theoretical parameter bound — a conceptual-reference quantity that delimits the extreme region of the parameter space associated with the abstract NFMI-inspired topology. It is NOT an active input to the executable pipeline, and it is not asserted as a physically realizable material property. In the same conceptual layer, $k = 100$ is motivated by the phase-velocity reduction needed for internal topological coherence, notionally compensating a high abstract permittivity parameter ($\epsilon_r \approx 80$) so that the effective wavelength parameter contracts to the modeled structural scale.

### Fractal Scaling Limits (Abstract Constraint)

Recursive branching increases the effective path-length parameter ($l_{\text{eff}}$), but the abstract gain does not scale linearly with geometric complexity. Within the model, increased path length introduces parasitic-coupling and cumulative resistive-loss parameters that damp the effective current-distribution parameter. The structural resonance is therefore treated as a high-precision equilibrium between fractal density and the preservation of a coherent phase parameter across the aperture, not as an unbounded optimization.

All parameters in this section are simulation inputs defining the abstract material layer. No biological tissue modification, chemical doping process, or physical material property is claimed or modeled.

---

## Appendix A: Quantitative Functional Isomorphism Table

This appendix consolidates, as a single conceptual reference, the abstract metrics distributed across the preceding sections. It is a theoretical mapping layer: several entries — for example the coupling parameter $K_{\text{DIPOLE}}$, the permeability bound, and the plasma-frequency analogue — are conceptual constructs and are NOT active inputs to the executable v1.2.6 pipeline, whose reproducible parameter set lives in `data/parameters.json`. All quantities are structural-coherence parameters defined within the graph-based abstraction system; none denotes a physical measurement.

### Foundational Modeling Parameters

- Computational Coupling Parameter ($K_{\text{DIPOLE}}$): a conceptual scaling parameter for the abstract interaction kernel, used to discuss global coupling amplitude. It is a theoretical construct, not an active variable in the v1.2.6 pipeline — runtime node coupling is evaluated through a phased-array superposition (`data/node_coupling.py`) — and it does not represent a physical constant.
- Effective Permeability ($\mu_r$): a phenomenological parameter representing combined structural amplification within the model. It is a modeling construct, independent of the geometric scaling constant $k$, and is not constrained to physically realizable limits.

### I. Structural and Inductive Parameters

- Root spirals (fractal inductance analogue): $L = \dfrac{\mu_0 \cdot \mu_r \cdot N^2 \cdot A}{l_{\text{eff}}}$, with $l_{\text{eff}} = k \cdot l_{\text{sketch}}$ and $k = 100$ as the macroscopic scaling constant.
- Foliar network (capacitive analogue): $C = \dfrac{\epsilon_r \cdot \epsilon_0 \cdot A}{d}$
- Phase modulation (N-PSK analogue): $\Phi_n = \dfrac{2\pi n}{M}$

### II. Thermal and Material Parameters

- Doping precursors: charge-carrier-density parameter $n$ targeting an abstract resistivity $\rho < 10^{-2}\ \Omega \cdot \text{m}$ (semi-conductive regime).
- Permeability bound: $\mu_r \approx 1.25 \times 10^6$, treated as a theoretical parameter bound (conceptual only; not a pipeline input).
- Dielectric modifier: $\epsilon_r$ adjustment for resonance fine-tuning at 12.5 Hz.
- Energy-storage analogue: $W = \dfrac{1}{2} C V^2$
- Thermal-dissipation analogue: $\dfrac{dQ}{dt} = \dfrac{dm}{dt} \cdot C_p \cdot (T_{\text{out}} - T_{\text{in}})$

### III. Control and Feedback Parameters

- Biotic control logic (set-points): nomographic distribution parameters for monitoring abstract gradient balance within the model.
- Energy-harvesting analogue: $V = g \cdot S \cdot t$
- Plasma-frequency analogue (propagation map): $f_p = 9\sqrt{N_e}$ (conceptual only; not a pipeline input).

---

## Appendix B: Conceptual Resonance-Baseline Reference

This appendix documents the conceptual resonance-baseline reference of the framework. All quantities are internal coherence metrics of the abstraction system. As of v1.2.6 they are conceptual reference values only: the executable pipeline no longer derives or stores a resonance baseline, and these closed-form relations are retained here purely to document the abstract design target. The reproducible pipeline consumes the parameter set in `data/parameters.json` and evaluates the morphological benchmark through `data/node_coupling.py`.

### I. Fixed Reference Parameters

- Target frequency: $f_{\text{target}} \approx 12.5$ Hz (abstract ELF-band reference).
- Scaling constant: $k = 100$.

### II. Analytic Parameter Relation ($f_{\text{target}} \rightarrow L \rightarrow C$)

$$
\begin{aligned}
L &= k \cdot 10^{-2} = 1.0000\ \text{H} \\
\omega_0 &= 2\pi f_{\text{target}} = 78.5398\ \text{rad/s} \\
C &= \frac{1}{\omega_0^2 \cdot L} = 1.6211 \times 10^{-4}\ \text{F} \approx 162\ \mu\text{F} \\
f &= \frac{1}{2\pi\sqrt{L \cdot C}} = 12.5000\ \text{Hz} \quad (= f_{\text{target}})
\end{aligned}
$$

### III. Conceptual RLC Reference

$$
\begin{aligned}
\text{Parameters:} \quad & L = 1.0\ \text{H}, \quad C = 1.6211 \times 10^{-4}\ \text{F}, \quad R = 100\ \Omega \\
\text{Resonant frequency:} \quad & f_{\text{res}} = \frac{1}{2\pi\sqrt{L \cdot C}} = 12.5000\ \text{Hz} \\
\text{Quality factor:} \quad & Q = \frac{\omega_{\text{res}} \cdot L}{R} = 0.7854 \\
\text{Bandwidth:} \quad & \text{BW} = \frac{R}{2\pi L} = 15.9155\ \text{Hz}
\end{aligned}
$$

The conceptual RLC reference uses the same capacitance $C = 1.6211 \times 10^{-4}\ \text{F}$ derived in Section II, so the reference circuit resonates at exactly the $f_{\text{target}} = 12.5$ Hz of the abstract design target. The quality factor $Q$ and bandwidth follow directly from $L$, $C$, and $R$; no additional free parameter is introduced.

---

## Historical Note

The project's botanical structures are produced by a stochastic branching algorithm (a randomized tree generator). They are not traced, digitized, or otherwise derived from any manuscript imagery. MS 408 (the Voynich Manuscript) is mentioned only as the historical context that originally motivated interest in plant-like branching morphologies. The current pipeline does not depend on, reconstruct, or make any claim about the manuscript's content, authorship, meaning, or purpose. All structural inputs to the pipeline come from the abstract morphological parameter space defined in the versioned configuration artifacts.