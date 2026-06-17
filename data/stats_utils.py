import numpy as np
from scipy.stats import nct, t as t_dist


def cohens_d(a, b):
    """Compute Cohen's d effect size between two samples.

    Uses the pooled standard deviation with degrees of freedom n_a + n_b - 2.

    Returns
    -------
    float
        Cohen's d, or NaN when the degrees of freedom fall below 1 or the
        pooled standard deviation collapses below 1e-4 (near-zero variance
        guard).
    """
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    n_a, n_b = len(a), len(b)
    df = n_a + n_b - 2
    if df < 1:
        return float("nan")
    pooled = np.sqrt(((n_a - 1) * np.std(a, ddof=1) ** 2 + (n_b - 1) * np.std(b, ddof=1) ** 2) / df)
    if pooled < 1e-4:
        return float("nan")
    return float((np.mean(a) - np.mean(b)) / pooled)


def hedges_g(a, b):
    """Compute Hedges' g, the small-sample bias-corrected effect size.

    Applies the standard correction factor 1 - 3 / (4 * df - 1) to Cohen's d,
    which slightly shrinks the estimate toward zero for finite samples.

    Returns
    -------
    float
        Hedges' g, or NaN when Cohen's d is undefined.
    """
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
    """Test whether a group's variance is negligible against a reference.

    Returns True when group_std is below `fraction` of reference_std, or when
    the reference standard deviation is non-positive. Used to flag seed-frozen
    groups whose effect sizes would otherwise be spurious.

    Returns
    -------
    bool
        True when the group variance is treated as near-zero.
    """
    if reference_std <= 0:
        return True
    return group_std < fraction * reference_std


def holm_correction(p_values):
    """Apply the Holm-Bonferroni step-down correction to p-values.

    Parameters
    ----------
    p_values : sequence of float
        Raw p-values, in any order.

    Returns
    -------
    list of float
        Corrected p-values aligned to the input order, each clipped to 1.0
        and monotone non-decreasing in rank.
    """
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
    """Estimate a bootstrap confidence interval for the difference in means.

    Resamples both groups with replacement n_bootstrap times and reports the
    percentile interval of the mean differences (mean(a) - mean(b)).

    Parameters
    ----------
    a, b : sequence of float
        The two samples.
    n_bootstrap : int
        Number of bootstrap resamples.
    ci : float
        Confidence level (e.g. 0.95).
    seed : int
        Seed for the resampling RNG (reproducible).

    Returns
    -------
    tuple of float
        Lower and upper bounds of the confidence interval.
    """
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
    """Compute post-hoc statistical power for a two-sample t-test.

    Uses the noncentral t-distribution with noncentrality |d| * sqrt(n / 2)
    and df = 2 * (n - 1).

    Parameters
    ----------
    d : float
        Cohen's d effect size.
    n : int
        Per-group sample size.
    alpha : float
        Two-sided significance level.

    Returns
    -------
    float
        Power in [0, 1], or NaN when d is undefined or n < 2.
    """
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
