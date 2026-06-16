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

GENERATORS = {
    "botanical": input_generator.generate_botanical_graph,
    "random":    input_generator.generate_random_control,
    "fractal":   input_generator.generate_fractal_morphology,
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
    return (ref_mean - other_mean) / abs(other_mean + 1e-12)


def run_parametric_sweep(output_file=None):
    if output_file is None:
        output_file = output_path("robustness_matrix.csv")

    params = load_parameters()
    sweep_cfg = params["VI_experimental_sweep_parameters"]
    af_cfg    = params["VII_array_factor_parameters"]

    n_nodes     = int(sweep_cfg["n_nodes"])
    seed        = int(sweep_cfg["seed"])
    noise_level = float(sweep_cfg.get("noise_level", 0.15))
    threshold   = float(sweep_cfg.get("curve_separation_threshold", 0.10))
    k_mod_coeff = float(af_cfg["k_modulation_coeff"])
    q_ref       = float(af_cfg["q_reference"])

    fast_mode = os.environ.get("PIPELINE_FAST") == "1"
    k0_grid   = K0_GRID[:2]   if fast_mode else K0_GRID
    beta_grid = BETA_GRID[:2] if fast_mode else BETA_GRID
    q_grid    = Q_GRID[:2]    if fast_mode else Q_GRID

    rows_out = []
    total = len(k0_grid) * len(beta_grid) * len(q_grid)

    for k0 in k0_grid:
        for beta in beta_grid:
            for Q0 in q_grid:
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
                sep_vs_random = _curve_separation(bot, rnd)
                sep_vs_fractal = _curve_separation(bot, frac)
                holds = bool(sep_vs_random >= threshold)
                rows_out.append([
                    k0, beta, Q0,
                    round(sep_vs_random, 4),
                    round(sep_vs_fractal, 4),
                    holds,
                ])

    ensure_output_dir()
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "k0_base", "beta_loss_factor", "Q_individual",
            "curve_sep_botanical_vs_random",
            "curve_sep_botanical_vs_fractal",
            "finding_holds",
        ])
        writer.writerows(rows_out)

    n_holds = sum(1 for r in rows_out if r[5])
    frac_pct = n_holds / total * 100
    print(
        f"      Robustness: {n_holds}/{total} grid points — "
        f"botanical separates from random (curve_sep >= {threshold}) in {frac_pct:.1f}% of parameter space"
    )
    print(f"      Written: {rel(output_file)}")

    return rows_out, frac_pct


if __name__ == "__main__":
    run_parametric_sweep()