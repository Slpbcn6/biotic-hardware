# Retraction note — `biotic-hardware` v1.3.0

> A post-mortem on the central finding of v1.3.0, the confounder that invalidated it, and what the corrected v1.4.x pipeline actually shows.

**Repository:** [`Slpbcn6/biotic-hardware`](https://github.com/Slpbcn6/biotic-hardware) · **DOI:** [10.5281/zenodo.20590864](https://doi.org/10.5281/zenodo.20590864) · **Author:** Santi López Puiggené

---

![Phase assignment: the same eight node positions, coloured by index under the v1.3.0 rule (phases change when the points are re-ordered) versus by angular sector under the v1.4.0 rule (phases unchanged); the correction reverses the botanical-vs-Voronoi Merit_Scaled effect from d = -1.05 to d = +0.61, non-significant.](assets/retraction.svg)

*Figure 1 — Phase assignment: what went wrong, and the fix. Both panels show the **same** eight node positions. **Left (v1.3.0, confounded):** each node is coloured by the phase it receives under the index rule `base_phases[i % 4]`, so re-ordering the identical point set changes the phases. **Right (v1.4.0, fixed):** each node is coloured by its angular sector around the centroid, so re-ordering leaves the phases unchanged. Under the corrected rule the central botanical-vs-Voronoi effect on Merit_Scaled reverses sign (d = -1.05 -> +0.61) and is no longer significant.*

---

## TL;DR

On 20 June 2026 I released **v1.3.0** of this repository, whose headline finding was that the *botanical* morphology occupied a structurally stable mid-merit position between ordered and stochastic controls — specifically that it sat **below** the high-merit stochastic controls (Voronoi, reticulate vein growth) with Holm-corrected significance on both Merit_Scaled and Peak_AF, at post-hoc power ≥ 0.98.

Three days later, on 23 June 2026, I released **v1.4.0** retracting that finding. A systematic audit of the code against its own documentation identified that the array-factor formulation in v1.3.0 was **not invariant to node permutation**: the phase assigned to each node was determined by the node's *index in the generator output* rather than by its *position in space*. Because each morphology generator emits nodes in a different — and in some cases stochastic — order, the metric was conflating geometry with insertion order. The magnitude of the confounder was **~32.5% in the peak value of the array factor** under random permutations of the same point set.

Under the corrected, geometry-referenced phase rule (v1.4.0) the central claim does not reproduce. The botanical-vs-Voronoi effect on Merit_Scaled reverses sign — from **d = −1.05 (p_holm = 0.009, significant)** to **d = +0.61 (p_holm = 0.93, not significant)** — and botanical is no longer separable from any of the genuine stochastic controls (random, Voronoi, DLA, reticulate) on the central metrics. The corrected result is a **null**, and v1.4.x reports it as such.

A single secondary observation survives on the coherence-ratio metric and is reported with restrained framing (see *What survives the correction* below).

This note records the original claim, the technical nature of the error, how it was identified, what the corrected pipeline shows, and what I take away from the process.

---

## 1. The v1.3.0 claim, as originally stated

The v1.3.0 README presented the central finding as follows (lightly abridged for length):

> On both Merit_Scaled and Peak_AF, botanical separates with Holm-corrected significance from four of the six other seed-variable morphologies, sitting **below the two high-merit stochastic controls** — Voronoi (d = −1.05 on Merit, −1.19 on Peak_AF) and reticulate vein growth (d = −1.04, −1.22) — and **above the two low-merit regular controls** — Gaussian clusters (d = +1.64, +1.66) and concentric rings (d = +1.52, +1.57) — with post-hoc power 0.98–1.0.

The claim was further reinforced by a parametric robustness sweep reported as holding across **100 % of a 5×5×5 = 125-point** grid in (k₀, β, Q) space.

At the time of release I believed the result was solid. The pipeline was deterministic, the statistical layer was defensive (Holm-Bonferroni correction, variance-floor guard against seed-frozen morphologies, post-hoc power, bootstrap CI), and the test suite was green (137 unit tests). The result also looked stable across the 125-point parametric sweep.

I now believe the result was an artefact of the array-factor formulation, not of geometry.

---

## 2. The technical error

In `data/node_coupling.py` the array factor was computed by summing complex-valued phasors over the node set:

```python
# v1.3.0 — flawed
base_phases = np.array([0, np.pi/2, np.pi, 3*np.pi/2])
phases = base_phases[np.arange(len(positions)) % 4]
af = np.sum(np.exp(1j * (spatial + phases[:, None])), axis=0)
```

The phase assigned to each node was the cyclic pattern `base_phases[i % 4]`, where `i` is the node's index in the array returned by the generator.

**The flaw:** this assignment is not a function of the node's spatial position. It is a function of *the order in which the generator emitted the node*. Different generators emit nodes in radically different orders:

- `generate_hexagonal_lattice` emits nodes in row-major scan order. Indices and spatial positions are tightly correlated, so the phase pattern is approximately spatially regular.
- `generate_botanical_graph` emits nodes by repeatedly picking a *random parent* from the set already placed, and attaching a child at a seeded angle and radius. The index of each node therefore reflects the branching insertion history, not its spatial position.
- `generate_random_control` emits nodes in uniformly random order.

Consequence: the array factor — and every downstream metric (peak, coherence, merit, merit_scaled) — was a function of **(geometry × generator insertion order)**, not of geometry alone. Morphologies under comparison were not being compared like for like, because they carried systematically different ordering conventions baked into their generators.

### Empirical magnitude of the confounder

The simplest possible test: take a single morphology's 64 nodes (botanical, seed 42), permute the node order with 20 different random permutations, and recompute the peak of the array factor. If the formulation were geometry-only, the peak would be identical across permutations. It was not:

| Quantity                          | Value                |
|-----------------------------------|----------------------|
| Mean change in peak               | **32.5%**            |
| Standard deviation                | 25.6 %               |
| Maximum observed in 20 trials     | **74.7%**            |

Effects of this magnitude swamp the differences the v1.3.0 paper was claiming. The botanical-vs-Voronoi Cohen's d of −1.05 on Merit_Scaled, presented as a finding, sat well within the noise band of node-ordering artefacts that the formulation was silently introducing.

---

## 3. How the error was identified

The confounder was not visible from the test suite, which passed at 137/137 throughout v1.3.0. Unit tests verified that generators were deterministic, that the topology validator worked, that the statistical primitives (Holm correction, bootstrap CI, Pearson r with leave-one-out) were correct, and that `n/a` propagation through the CSV outputs was clean. All of that was true. None of it tested geometric invariance of the array-factor formulation under node permutation.

The confounder surfaced during a systematic audit of the code against its own documentation. Read line by line against what the documentation claimed it computed, the array-factor phase turned out to be indexed by node order rather than by spatial position; the permutation test reported in §2 confirmed the ~32.5% ordering effect. Two remedies were possible: make the phase spatially canonical, or document the dependence on insertion order as a known confounder. I made the phase spatially canonical — the fix and its consequences are described in §4.

The same audit surfaced three additional code-versus-README mismatches of patch-level severity (Holm correction was implemented pooled across metrics while the README claimed per-metric correction; the `finding_holds` column in the parametric robustness matrix was the conjunction of two separations while the README described only one; the parametric robustness grid ran on a single seed while the language around it conflated parametric and stochastic robustness). All four findings were addressed together in the v1.4.0 release.

---

## 4. The fix

In v1.4.0 the array-factor formulation is rewritten to assign each node's phase from the node's **angular position relative to the point-set centroid**, not from its index:

```python
# v1.4.0 — geometry-referenced
centroid = positions[:, :2].mean(axis=0)
angles   = np.arctan2(positions[:, 1] - centroid[1],
                      positions[:, 0] - centroid[0])
# 'sector' rule: quantise the centroid-relative angle into four quadrants
sector   = ((angles + 2*np.pi) % (2*np.pi)) // (np.pi / 2)
phases   = base_phases[sector.astype(int)]
```

Two phase rules are now supported, both geometry-referenced:

- **Sector** (default, pre-specified primary): the centroid-relative angle is quantised into four quadrants, each mapped to one of the base phases `[0, π/2, π, 3π/2]`. This is the closest geometry-referenced analogue of the original four-phase intention.
- **Continuous** (cross-check): the centroid-relative angle itself is used as the phase.

Both rules are invariant to node permutation by construction. Verified empirically: permuting the same 64 botanical nodes with 20 random permutations now produces a maximum peak change of **0.000%** (exact, modulo floating-point), against the **32.5% mean** under the v1.3.0 rule.

Three further methodological commitments were made at the same time, addressing the patch-level audit findings:

1. **Holm-Bonferroni correction** is documented and implemented as a single pooled family across all valid pairs across all metrics (135 = 45 × 3), with the choice stated explicitly in the README rather than contradicted by it.
2. **The near-zero-variance guard** is unified into a single authority, `stats_utils.near_zero_variance`. `cohens_d` calls it directly instead of carrying its own 1e-4 magic threshold.
3. **The parametric robustness sweep** is extended from 125 points × 1 seed to 125 points × 30 seeds = **3750 (parameter × seed) cells**. The `finding_holds` column is documented as the conjunction *"botanical separates below both the random and Voronoi controls"* at the cell.

---

## 5. The corrected result

Under the geometry-referenced sector phase rule, with Holm-Bonferroni pooled across all 135 valid pairs and N = 30 seeds per morphology:

| Comparison                       | v1.3.0 Cohen's d (Merit_Scaled) | v1.4.0 Cohen's d | v1.4.0 p_holm |
|----------------------------------|--------------------------------:|------------------:|----------------:|
| Botanical vs Random              | not previously reported as such | **+0.67**         | 0.51 (ns)       |
| Botanical vs Voronoi             | **−1.05** (sig)                 | **+0.61**         | 0.93 (ns)       |
| Botanical vs DLA                 | (variable)                      | non-significant   | (ns)            |
| Botanical vs Reticulate          | **−1.04** (sig)                 | non-significant   | (ns)            |
| Botanical vs Clusters            | +1.64 (sig)                     | **+0.93**         | (sig)           |
| Botanical vs Concentric          | +1.52 (sig)                     | **+2.16**         | (sig)           |

Two observations:

- **The botanical-vs-Voronoi effect reverses sign** (−1.05 → +0.61) and loses significance. This is decisive against the original directional claim that botanical sat *below* the high-merit stochastic controls. It does not.
- Botanical is **not statistically distinguishable from any genuine stochastic control** (random, Voronoi, DLA, reticulate) on either Merit_Scaled or Peak_AF under the primary phase rule. Its only Holm-significant separations on the central metrics are from the regular geometric controls (clusters, concentric) and from the deterministic references (fractal, Fibonacci, hexagonal), and these are no longer the interesting comparisons.

The previously reported "100 % across 125 grid points" parametric robustness becomes, under the corrected formulation and the multi-seed extension, **500 of 3750 (~13 %)** of (parameter × seed) cells holding the conjoint below-both-controls direction. This is consistent with the directional finding being an artefact of the v1.3.0 formulation, not a structural property of botanical morphology.

### What survives the correction

One observation survives both phase rules at meaningful effect size: on the **coherence ratio**, botanical sits *below* the Voronoi control (sector d ≈ −1.12, continuous d ≈ −1.56). v1.4.x reports this as a restrained secondary observation, **not** as a performance claim and **not** as a recovery of the retracted central finding. It is informative about the coherence-ratio metric specifically and should be interpreted only as such.

---

## 6. On ending here

The original direction does not survive the correction and cannot be honestly recovered. The corrected result is a null, and the project closes on it. This is the right place to end: the claim was wrong, the correction is clear, and there is nothing left to defend.

---

## 7. Status of the artefacts

- **v1.3.0** (commit [`3b2cab0`](https://github.com/Slpbcn6/biotic-hardware/commit/3b2cab09a011efac63daa332bc561630aba7d1b2), 20 Jun 2026): **retracted**. The tag and its Zenodo deposit remain available for historical reference; the README of the retracted release now links to this note.
- **v1.4.0** (23 Jun 2026): geometry-referenced phase rule, unified variance guard, pooled-Holm documented as such, multi-seed parametric robustness, null central finding reported.
- **v1.4.1** (23 Jun 2026): documentation-only patch over v1.4.0; phase-robustness wording corrected, scope of null headline restated. No code or scientific change.

Citations of v1.3.0 published before 23 June 2026 should be understood as referring to a retracted result. The corrected pipeline is v1.4.1 onward.

---

## 8. On the audit

The corrections in v1.4.0 came out of a systematic, independent audit of the code against its own documentation. The node-ordering confounder, the Holm-pooling inconsistency, the `finding_holds` mischaracterisation, and the single-seed framing of the parametric robustness sweep were all surfaced that way, in a form that made them straightforward to act on.

Comments, replication attempts, and further audits are welcome via the repository's issue tracker.

---

*Santi López Puiggené · 25 June 2026 · `biotic-hardware` v1.4.1*