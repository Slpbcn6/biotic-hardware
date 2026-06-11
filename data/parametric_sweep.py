import numpy as np
import csv
from scipy.stats import ttest_ind

from data import input_generator
from data.node_coupling import compute_array_factor
from data.config import load_parameters, ensure_output_dir, output_path, rel
from data.stats_utils import cohens_d

K0_GRID = [0.002, 0.004, 0.006, 0.008]
BETA_GRID = [0.1, 0.25, 0.4]
Q_GRID = [0.5, 0.8, 1.5, 3.0]

DISTANCES = np.linspace(0.1, 2.0, 30)


def _merit_scaled_series(
    mode, n_nodes, seed, noise_botanical,
    k0_base, beta, Q0, k_mod_coeff, q_ref,
):
    generators = {
        "botanical": input_generator.generate_botanical_graph,
        "random":    input_generator.generate_random_control,
    }
    base_nodes = generators[mode](n_nodes=n_nodes, seed=seed)
    noise = noise_botanical if mode == "botanical" else 0.0
    rng = np.random.default_rng(seed)
    n_steps = len(DISTANCES)
    results = []
    for i, d in enumerate(DISTANCES):
        perturb = rng.normal(0, noise, base_nodes.shape)
        positions = (base_nodes + perturb) * d
        Q_eff = Q0 * (1 - beta * (i / n_steps))
        peak, coherence, _, _ = compute_array_factor(
            positions, Q_eff, k0_base, k_mod_coeff, q_ref,
        )
        results.append(peak * coherence * Q_eff)
    return np.array(results)


def run_parametric_sweep(output_file=None):
    if output_file is None:
        output_file = output_path("robustness_matrix.csv")

    params = load_parameters()
    sweep_cfg = params["VI_experimental_sweep_parameters"]
    af_cfg = params["VII_array_factor_parameters"]

    n_nodes = int(sweep_cfg["n_nodes"])
    seed = int(sweep_cfg["seed"])
    noise_botanical = float(sweep_cfg.get("noise_botanical", 0.15))
    k_mod_coeff = float(af_cfg["k_modulation_coeff"])
    q_ref = float(af_cfg["q_reference"])

    rows_out = []
    total = len(K0_GRID) * len(BETA_GRID) * len(Q_GRID)

    for k0 in K0_GRID:
        for beta in BETA_GRID:
            for Q0 in Q_GRID:
                bot = _merit_scaled_series(
                    "botanical", n_nodes, seed, noise_botanical,
                    k0, beta, Q0, k_mod_coeff, q_ref,
                )
                rnd = _merit_scaled_series(
                    "random", n_nodes, seed, noise_botanical,
                    k0, beta, Q0, k_mod_coeff, q_ref,
                )
                _, p = ttest_ind(bot, rnd, equal_var=False)
                d = cohens_d(bot, rnd)
                holds = bool(p < 0.05 and not np.isnan(d))
                d_str = "n/a" if np.isnan(d) else round(d, 4)
                rows_out.append([
                    k0, beta, Q0,
                    round(float(p), 6),
                    d_str,
                    holds,
                ])

    ensure_output_dir()
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "k0_base", "beta_loss_factor", "Q_individual",
            "p_botanical_vs_random", "d_botanical_vs_random", "finding_holds",
        ])
        writer.writerows(rows_out)

    n_holds = sum(1 for r in rows_out if r[5])
    frac = n_holds / total * 100
    print(
        f"      Robustness: {n_holds}/{total} grid points — "
        f"botanical separates from random at p<0.05 in {frac:.1f}% of parameter space"
    )
    print(f"      Written: {rel(output_file)}")

    return rows_out, frac


if __name__ == "__main__":
    run_parametric_sweep()