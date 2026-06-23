import numpy as np

from data.stats_utils import (
    cohens_d,
    hedges_g,
    near_zero_variance,
    holm_correction,
    bootstrap_ci,
    power_from_d,
    pearson_r,
    loocv_pearson,
)


def test_cohens_d_sign_and_magnitude():
    a = [10.0, 11.0, 12.0, 13.0, 14.0]
    b = [0.0, 1.0, 2.0, 3.0, 4.0]
    d = cohens_d(a, b)
    assert d > 0
    assert cohens_d(b, a) == -d


def test_cohens_d_zero_for_identical_groups():
    a = [1.0, 2.0, 3.0, 4.0]
    assert cohens_d(a, a) == 0.0


def test_cohens_d_nan_for_collapsed_variance():
    a = [5.0, 5.0, 5.0, 5.0]
    b = [5.0, 5.0, 5.0, 5.0]
    assert np.isnan(cohens_d(a, b))


def test_hedges_g_shrinks_toward_zero():
    a = [10.0, 11.0, 12.0, 13.0, 14.0]
    b = [0.0, 1.0, 2.0, 3.0, 4.0]
    d = cohens_d(a, b)
    g = hedges_g(a, b)
    assert abs(g) < abs(d)


def test_hedges_g_correction_factor():
    a = [10.0, 11.0, 12.0, 13.0, 14.0]
    b = [0.0, 1.0, 2.0, 3.0, 4.0]
    d = cohens_d(a, b)
    df = len(a) + len(b) - 2
    correction = 1.0 - 3.0 / (4.0 * df - 1.0)
    assert np.isclose(hedges_g(a, b), d * correction)


def test_hedges_g_nan_when_d_nan():
    a = [5.0, 5.0, 5.0, 5.0]
    b = [5.0, 5.0, 5.0, 5.0]
    assert np.isnan(hedges_g(a, b))


def test_near_zero_variance():
    assert near_zero_variance(0.01, 1.0, fraction=0.1)
    assert not near_zero_variance(0.5, 1.0, fraction=0.1)
    assert near_zero_variance(0.5, 0.0)


def test_near_zero_variance_absolute_floor_without_reference():
    assert near_zero_variance(1e-6)
    assert not near_zero_variance(1.0)
    assert near_zero_variance(1e-6, reference_std=None)
    assert not near_zero_variance(1.0, reference_std=None)


def test_near_zero_variance_floor_and_relative_intersection():
    assert near_zero_variance(0.05, reference_std=1.0, fraction=0.15)
    assert not near_zero_variance(0.2, reference_std=1.0, fraction=0.15)
    assert near_zero_variance(1e-6, reference_std=1.0, fraction=0.15)


def test_cohens_d_uses_shared_floor_for_tiny_nonzero_variance():
    a = [1.0, 1.0, 1.00001, 1.0]
    b = [1.0, 1.00001, 1.0, 1.0]
    assert np.isnan(cohens_d(a, b))


def test_holm_correction_monotone_and_bounded():
    p = [0.01, 0.02, 0.03, 0.04]
    corrected = holm_correction(p)
    assert len(corrected) == len(p)
    for c in corrected:
        assert 0.0 <= c <= 1.0
    assert corrected[0] >= p[0]


def test_holm_correction_preserves_order_positions():
    p = [0.04, 0.01, 0.03, 0.02]
    corrected = holm_correction(p)
    assert np.argmin(corrected) == np.argmin(p)


def test_bootstrap_ci_brackets_mean_difference():
    rng = np.random.default_rng(0)
    a = rng.normal(5.0, 1.0, 50)
    b = rng.normal(0.0, 1.0, 50)
    lower, upper = bootstrap_ci(a, b, n_bootstrap=10000, seed=1)
    assert lower < upper
    assert lower <= (np.mean(a) - np.mean(b)) <= upper


def test_bootstrap_ci_deterministic_with_seed():
    a = [1.0, 2.0, 3.0, 4.0, 5.0]
    b = [0.0, 1.0, 2.0, 3.0, 4.0]
    first = bootstrap_ci(a, b, n_bootstrap=1000, seed=7)
    second = bootstrap_ci(a, b, n_bootstrap=1000, seed=7)
    assert first == second


def test_power_from_d_increases_with_effect_size():
    low = power_from_d(0.2, 30)
    high = power_from_d(1.5, 30)
    assert 0.0 <= low <= 1.0
    assert 0.0 <= high <= 1.0
    assert high > low


def test_power_from_d_nan_guards():
    assert np.isnan(power_from_d(float("nan"), 30))
    assert np.isnan(power_from_d(0.5, 1))


def test_pearson_r_perfect_positive():
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [2.0, 4.0, 6.0, 8.0, 10.0]
    r, p = pearson_r(x, y)
    assert abs(r - 1.0) < 1e-9
    assert p < 1e-9


def test_pearson_r_perfect_negative():
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [10.0, 8.0, 6.0, 4.0, 2.0]
    r, p = pearson_r(x, y)
    assert abs(r + 1.0) < 1e-9


def test_pearson_r_matches_scipy():
    from scipy.stats import pearsonr
    rng = np.random.default_rng(3)
    x = rng.normal(size=12)
    y = 0.7 * x + rng.normal(size=12)
    r, p = pearson_r(x, y)
    r_ref, p_ref = pearsonr(x, y)
    assert abs(r - r_ref) < 1e-9
    assert abs(p - p_ref) < 1e-9


def test_pearson_r_threshold_n10():
    rng = np.random.default_rng(11)
    x = rng.normal(size=10)
    y = rng.normal(size=10)
    r, p = pearson_r(x, y)
    assert -1.0 <= r <= 1.0
    assert 0.0 <= p <= 1.0


def test_pearson_r_guards():
    r, p = pearson_r([1.0, 2.0], [1.0, 2.0])
    assert np.isnan(r) and np.isnan(p)
    r, p = pearson_r([5.0, 5.0, 5.0, 5.0], [1.0, 2.0, 3.0, 4.0])
    assert np.isnan(r) and np.isnan(p)


def test_loocv_pearson_stable_for_strong_signal():
    rng = np.random.default_rng(5)
    x = np.linspace(0, 1, 10)
    y = 3.0 * x + rng.normal(0, 0.02, 10)
    loo = loocv_pearson(x, y)
    assert loo["sign_stable"] is True
    assert loo["min"] > 0.9
    assert loo["std"] < 0.1


def test_loocv_pearson_guard_small_n():
    loo = loocv_pearson([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    assert np.isnan(loo["mean"])
    assert loo["sign_stable"] is False
