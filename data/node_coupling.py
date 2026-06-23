import numpy as np
import csv

from data import input_generator
from data.config import load_parameters, ensure_output_dir
from data.topology_validator import validate_topology


def compute_array_factor(positions, Q, k0_base, k_mod_coeff, q_ref, phase_rule="sector"):
    """Compute the complex-valued array factor over the full angular domain [0, 2π].

    Each node is assigned a phase from its spatial position relative to the
    point-set centroid, so the array factor depends only on geometry and not on
    the arbitrary order in which a generator emits its nodes. Under the default
    "sector" rule the centroid-relative angle is quantised into four quadrants
    mapped to the base phases [0, π/2, π, 3π/2]; under "continuous" the
    centroid-relative angle itself is used as the phase. The spatial
    contribution is modulated by the Q-dependent wave number
    k = k0_base * (1 + k_mod_coeff * (Q - q_ref)).

    Parameters
    ----------
    positions : ndarray, shape (n_nodes, 2)
        Node coordinates.
    Q : float
        Effective quality factor at this sweep step.
    k0_base, k_mod_coeff, q_ref : float
        Array-factor wave-number parameters.
    phase_rule : {"sector", "continuous"}
        Geometry-driven phase assignment. "sector" quantises the
        centroid-relative angle into four quadrants; "continuous" uses the angle
        directly. Both are invariant to node ordering.

    Returns
    -------
    peak : float
        Maximum magnitude of the array factor.
    coherence : float
        Peak-to-mean ratio (coherence proxy).
    mean : float
        Mean magnitude across the angular domain.
    magnitude : ndarray, shape (200,)
        Magnitude of the array factor at each of the 200 angular samples.
    """
    theta = np.linspace(0, 2 * np.pi, 200)
    k = k0_base * (1 + k_mod_coeff * (Q - q_ref))

    centroid_x = positions[:, 0].mean()
    centroid_y = positions[:, 1].mean()
    angle = np.arctan2(positions[:, 1] - centroid_y, positions[:, 0] - centroid_x)
    if phase_rule == "continuous":
        phases = angle
    else:
        base_phases = np.array([0, np.pi / 2, np.pi, 3 * np.pi / 2])
        sector = np.floor(np.mod(angle, 2 * np.pi) / (np.pi / 2)).astype(int) % 4
        phases = base_phases[sector]

    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    spatial = k * (positions[:, 0:1] * cos_t + positions[:, 1:2] * sin_t)
    af = np.sum(np.exp(1j * (spatial + phases[:, None])), axis=0)

    magnitude = np.abs(af)
    peak = np.max(magnitude)
    mean = np.mean(magnitude)
    coherence = peak / (mean + 1e-12)

    return peak, coherence, mean, magnitude


def run_sweep(mode, output_file, tensor_file, seed_override=None, phase_rule="sector"):
    """Run the full distance sweep for a single morphology mode.

    Parameters
    ----------
    mode : str
        Any morphology name accepted by input_generator.load_morphology.
    output_file : str
        Path for the scalar CSV output.
    tensor_file : str
        Path for the NPZ tensor output (keys: 'distance', 'af').
    seed_override : int or None
        When set, overrides the seed from parameters.json. Used by
        multi_seed_analysis.py to iterate across seeds without mutating the
        config file.
    phase_rule : {"sector", "continuous"}
        Phase-assignment rule forwarded to compute_array_factor. "sector" is the
        primary geometry-driven rule; "continuous" backs the phase-robustness
        check.

    Returns
    -------
    str
        Topology validation report string (the PASS line).

    Notes
    -----
    noise_level (read from parameters.json section VI) is applied identically
    to every morphology — there is no morphology-conditional noise branch.
    This ensures fair comparison across all structural inputs.
    """
    params = load_parameters()

    Q0 = float(params["IV_network_performance_metrics"]["individual_q_factor"])
    cfg = params["VI_experimental_sweep_parameters"]
    af_cfg = params["VII_array_factor_parameters"]

    n_nodes = int(cfg["n_nodes"])
    seed = seed_override if seed_override is not None else int(cfg["seed"])
    beta = float(cfg["beta_loss_factor"])
    connection_radius = float(cfg.get("connection_radius_m", 2.0))
    noise_level = float(cfg.get("noise_level", 0.15))

    k0_base = float(af_cfg["k0_base"])
    k_mod_coeff = float(af_cfg["k_modulation_coeff"])
    q_ref = float(af_cfg["q_reference"])

    base_nodes = input_generator.load_morphology(mode=mode, n_nodes=n_nodes, seed=seed)

    valid, report = validate_topology(base_nodes, connection_radius=connection_radius)
    if not valid:
        raise RuntimeError(f"Topology validation failed for {mode}: {report}")

    rng = np.random.default_rng(seed)
    distances = np.linspace(0.1, 2.0, 30)

    distance_store = []
    af_store = []

    ensure_output_dir()

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Distance", "Peak_AF", "Coherence_Ratio",
            "Merit_Function", "Q_effective", "Merit_Scaled",
        ])

        for i, d in enumerate(distances):
            perturb = rng.normal(0, noise_level, base_nodes.shape)
            positions = (base_nodes + perturb) * d
            Q_eff = Q0 * (1 - beta * (i / len(distances)))

            peak, coherence, mean, magnitude = compute_array_factor(
                positions, Q_eff, k0_base, k_mod_coeff, q_ref, phase_rule=phase_rule
            )

            merit = peak * coherence
            scaled = merit * Q_eff

            writer.writerow([d, peak, coherence, merit, Q_eff, scaled])

            distance_store.append(d)
            af_store.append(magnitude)

    np.savez(
        tensor_file,
        distance=np.array(distance_store),
        af=np.array(af_store),
    )

    return report[0]