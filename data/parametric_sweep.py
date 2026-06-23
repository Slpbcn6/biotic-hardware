import os
import numpy as np
import csv

from data import input_generator
from data.node_coupling import compute_array_factor
from data.config import load_parameters, ensure_output_dir, output_path, rel

K0_GRID   = [0.002, 0.004, 0.006, 0.008, 0.012]
BETA_GRID = [0.10, 0.20, 0.25, 0.35, 0.40]
Q_GRID    = [0.5, 0.8, 1.2, 2.0, 3.0]

DISTANCES = np.linspace(0.1, 2.0, 30)


def effective_grids():
    if os.environ.get("PIPELINE_FAST") == "1":
        return K0_GRID[:2], BETA_GRID[:2], Q_GRID[:2]
    return K0_GRID, BETA_GRID, Q_GRID


def effective_seeds(seeds):
    if os.environ.get("PIPELINE_FAST") == "1":
        return list(seeds)[:2]
    return list(seeds)


GENERATORS = {
    "botanical": input_generator.generate_botanical_graph,
    "random":    input_generator.generate_random_control,
    "fractal":   input_generator.generate_fractal_morphology,
    "voronoi":   input_generator.generate_voronoi_control,
}


def _merit_scaled_series(
    mode, n_nodes, seed, noise_level,
    k0_base, beta, Q0, k_mod_coeff, q_ref,
):
    base_nodes = GENERATORS[mode](n_nodes=n_nodes, seed=seed)
    rng = np.random.default_rng(seed)
    n_steps = len(DISTANCES)
    results = []
    for i, d in enumerate(DISTANCES):
        perturb = rng.normal(0, noise_level, base_nodes.shape)
        positions = (base_nodes + perturb) * d
        Q_eff = Q0 * (1 - beta * (i / n_steps))
        peak, coherence, _, _ = compute_array_factor(
            positions, Q_eff, k0_base, k_mod_coeff, q_ref,
        )
        results.append(peak * coherence * Q_eff)
    return np.array(results)


def _curve_separation(reference, other):
    ref_mean = float(np.mean(reference))
    other_mean = float(np.mean(other))
    return (ref_mean - other_mean) / (abs(other_mean) + 1e-12)


def run_parametric_sweep(output_file=None):
    """Sweep the array-factor parameter grid across every multi-seed replicate.

    For each (k0, beta, Q) grid point and each seed, the botanical merit curve is
    compared against the random and Voronoi stochastic controls. A point-by-seed
    cell counts as holding the v1.3.0 signature only when botanical sits *below*
    both controls by at least the curve-separation threshold (a signed test, not
    a magnitude test). The fraction of cells that hold quantifies how much of the
    joint parameter-and-seed space supports the original directional claim under
    the corrected geometry-driven phase rule.

    Returns
    -------
    rows_out : list
        One row per (grid point, seed) cell.
    frac_pct : float
        Percentage of cells in which botanical sits below both controls.
    """
    if output_file is None:
        output_file = output_path("robustness_matrix.csv")

    params = load_parameters()
    sweep_cfg = params["VI_experimental_sweep_parameters"]
    af_cfg    = params["VII_array_factor_parameters"]

    n_nodes     = int(sweep_cfg["n_nodes"])
    noise_level = float(sweep_cfg.get("noise_level", 0.15))
    threshold   = float(sweep_cfg.get("curve_separation_threshold", 0.10))
    seeds       = effective_seeds(sweep_cfg["multi_seed_list"])
    k_mod_coeff = float(af_cfg["k_modulation_coeff"])
    q_ref       = float(af_cfg["q_reference"])

    k0_grid, beta_grid, q_grid = effective_grids()

    rows_out = []
    total = len(k0_grid) * len(beta_grid) * len(q_grid) * len(seeds)

    for k0 in k0_grid:
        for beta in beta_grid:
            for Q0 in q_grid:
                for seed in seeds:
                    bot = _merit_scaled_series(
                        "botanical", n_nodes, seed, noise_level,
                        k0, beta, Q0, k_mod_coeff, q_ref,
                    )
                    rnd = _merit_scaled_series(
                        "random", n_nodes, seed, noise_level,
                        k0, beta, Q0, k_mod_coeff, q_ref,
                    )
                    frac = _merit_scaled_series(
                        "fractal", n_nodes, seed, noise_level,
                        k0, beta, Q0, k_mod_coeff, q_ref,
                    )
                    vor = _merit_scaled_series(
                        "voronoi", n_nodes, seed, noise_level,
                        k0, beta, Q0, k_mod_coeff, q_ref,
                    )
                    sep_vs_random = _curve_separation(bot, rnd)
                    sep_vs_fractal = _curve_separation(bot, frac)
                    sep_vs_voronoi = _curve_separation(bot, vor)
                    holds = bool(
                        sep_vs_random <= -threshold and sep_vs_voronoi <= -threshold
                    )
                    rows_out.append([
                        k0, beta, Q0, seed,
                        round(sep_vs_random, 4),
                        round(sep_vs_fractal, 4),
                        round(sep_vs_voronoi, 4),
                        holds,
                    ])

    ensure_output_dir()
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "k0_base", "beta_loss_factor", "Q_individual", "seed",
            "curve_sep_botanical_vs_random",
            "curve_sep_botanical_vs_fractal",
            "curve_sep_botanical_vs_voronoi",
            "finding_holds",
        ])
        writer.writerows(rows_out)

    n_holds = sum(1 for r in rows_out if r[7])
    frac_pct = n_holds / total * 100
    print(
        f"      Robustness: botanical sits below BOTH stochastic controls "
        f"(curve_sep <= -{threshold} vs random and vs voronoi) in "
        f"{n_holds}/{total} point-by-seed cells ({frac_pct:.1f}%)"
    )
    print(f"      Written: {rel(output_file)}")

    return rows_out, frac_pct


if __name__ == "__main__":
    run_parametric_sweep()
