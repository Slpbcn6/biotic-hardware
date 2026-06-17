import numpy as np
from scipy.stats import nct, t as t_dist


def cohens_d(a, b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    pooled = np.sqrt((np.std(a, ddof=1) ** 2 + np.std(b, ddof=1) ** 2) / 2)
    if pooled < 1e-4:
        return float("nan")
    return float((np.mean(a) - np.mean(b)) / pooled)


def hedges_g(a, b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    d = cohens_d(a, b)
    if np.isnan(d):
        return float("nan")
    df = len(a) + len(b) - 2
    if df < 1:
        return float("nan")
    correction = 1.0 - 3.0 / (4.0 * df - 1.0)
    return float(d * correction)


def near_zero_variance(group_std, reference_std, fraction=0.1):
    if reference_std <= 0:
        return True
    return group_std < fraction * reference_std


def holm_correction(p_values):
    p = np.array(p_values, dtype=float)
    n = len(p)
    order = np.argsort(p)
    corrected = np.empty(n)
    running_max = 0.0
    for rank, idx in enumerate(order):
        adjusted = p[idx] * (n - rank)
        running_max = max(running_max, adjusted)
        corrected[idx] = min(running_max, 1.0)
    return corrected.tolist()


def bootstrap_ci(a, b, n_bootstrap=10000, ci=0.95, seed=0):
    rng = np.random.default_rng(seed)
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    diffs = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        sample_a = rng.choice(a, size=len(a), replace=True)
        sample_b = rng.choice(b, size=len(b), replace=True)
        diffs[i] = np.mean(sample_a) - np.mean(sample_b)
    alpha = 1.0 - ci
    lower = float(np.percentile(diffs, 100 * alpha / 2))
    upper = float(np.percentile(diffs, 100 * (1 - alpha / 2)))
    return lower, upper


def power_from_d(d, n, alpha=0.05):
    if np.isnan(d) or n < 2:
        return float("nan")
    ncp = abs(d) * np.sqrt(n / 2)
    df = 2 * (n - 1)
    t_crit = t_dist.ppf(1 - alpha / 2, df)
    upper = nct.cdf(t_crit, df, ncp)
    lower = nct.cdf(-t_crit, df, ncp)
    if np.isnan(lower):
        lower = 0.0
    power = 1.0 - upper + lower
    if np.isnan(power):
        return 1.0 if ncp > t_crit else float("nan")
    return float(np.clip(power, 0.0, 1.0))
