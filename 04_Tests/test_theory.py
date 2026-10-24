import numpy as np, pytest
from tariff_models import two_tier, MarginalBlockTariff, UP_URBAN_DOMESTIC_FY2019_20 as UP
from theory import *

rng = np.random.default_rng(42)

def random_cases(N=3000):
    for _ in range(N):
        n = int(rng.integers(1, 30))
        kind = rng.integers(4)
        if kind == 0: x = rng.gamma(2, 100, n)
        elif kind == 1: x = rng.choice([0.0, 50.0, 150.0, 400.0], n)
        elif kind == 2: x = rng.pareto(2.0, n) * 100
        else: x = np.full(n, rng.uniform(0, 500))
        yield x, rng.uniform(1, 700), rng.uniform(0, 8), rng.uniform(0, 4)

def test_identities_and_bounds():
    for x, K, p1, dp in random_cases():
        T = two_tier(p1, p1 + dp, K)
        V = penalty(x, T); n = x.size; m = x.mean(); s = pop_sd(x)
        assert V >= -1e-9
        assert V == pytest.approx(penalty_abs_identity(x, K, dp), abs=1e-7)
        assert V == pytest.approx(penalty_minority_identity(x, K, dp), abs=1e-7)
        chain = [bound_finite_nonneg(n, m, s, K, dp), bound_finite(n, m, s, K, dp), bound_scarf(x, K, dp), bound_sd(x, dp)]
        assert V <= chain[0] + 1e-7
        for a, b in zip(chain, chain[1:]):
            assert a <= b + 1e-7
        assert V <= bound_mad(x, dp) + 1e-7 <= bound_sd(x, dp) + 2e-7
        assert V <= bound_bp_nonneg(n, m, s, K, dp) + 1e-7

def test_equality_constant():
    x = np.full(12, 180.0)
    assert penalty(x, UP) == pytest.approx(0.0, abs=1e-9)

def test_equality_scarf_two_point_symmetric():
    # x = K +/- s with half the points each side: V = n dp s/2 = Scarf = SD bound (d=0)
    x = np.array([100.0, 300.0] * 6); K = 200.0; dp = 2.0
    T = two_tier(5.0, 7.0, K)
    assert penalty(x, T) == pytest.approx(bound_sd(x, dp))
    assert penalty(x, T) == pytest.approx(bound_scarf(x, K, dp))
    assert penalty(x, T) == pytest.approx(bound_finite(12, 200.0, 100.0, K, dp))

def test_theorem1_attained():
    for n, m, s, K in [(3, 280, 120, 150), (5, 100, 30, 150), (12, 280, 120, 300), (12, 150, 80, 150), (7, 60, 50, 150)]:
        x, j = extremal_configuration(n, m, s, K)
        assert x.mean() == pytest.approx(m) and pop_sd(x) == pytest.approx(s)
        assert hinge_gap(x, K) == pytest.approx(bound_finite(n, m, s, K, 1.0))

def test_samuelson_zero_certificate():
    # |xbar-K| >= s sqrt(n-1) => no point can lie on the other side => V = 0 (bound must be 0)
    n, m, s, K = 12, 400.0, 50.0, 150.0
    assert bound_finite(n, m, s, K, 1.0) == 0.0
    assert bound_scarf_moments(n, m, s, K, 1.0) > 0

def test_threshold_maximiser_is_mean():
    for _ in range(200):
        x = rng.gamma(2, 100, int(rng.integers(2, 15)))
        Wbar = hinge_gap(x, x.mean())
        assert Wbar == pytest.approx(0.5 * x.size * mad(x))
        for K in rng.uniform(0, 1000, 50):
            assert hinge_gap(x, K) <= Wbar + 1e-9

def test_multitier_decomposition_and_nonneg():
    for x, *_ in random_cases(500):
        assert penalty(x, UP) == pytest.approx(threshold_decomposition(x, UP).sum(), abs=1e-7)
        assert threshold_decomposition(x, UP).min() >= -1e-9

def test_nonconvex_can_be_negative():
    T = MarginalBlockTariff((150.0,), (6.0, 5.0))   # decreasing block
    assert penalty(np.array([100.0, 200.0]), T) < 0

def test_unequal_periods_nonnegative():
    days = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], float)
    for _ in range(300):
        x = rng.gamma(2, 100, 12)
        assert penalty(x, UP, days=days) >= -1e-9

def test_single_period_zero():
    assert penalty(np.array([500.0]), UP) == pytest.approx(0.0)
    assert bound_finite(1, 500.0, 0.0, 150.0, 1.0) == 0.0

def test_theorem3_reduces_to_theorem1_and_is_valid_and_attained():
    for _ in range(300):
        n = int(rng.integers(2, 13)); m = rng.uniform(20, 500); s = rng.uniform(1, 300); K = rng.uniform(10, 600); dp = rng.uniform(.1, 3)
        assert bound_multitier_exact(n, m, s, two_tier(5, 5 + dp, K)) == pytest.approx(bound_finite(n, m, s, K, dp), abs=1e-7)
    for _ in range(500):
        x = rng.gamma(1.5, 150, int(rng.integers(2, 13)))
        assert penalty(x, UP) <= bound_multitier_exact(x.size, x.mean(), pop_sd(x), UP) + 1e-7
    V, x = bound_multitier_exact(12, 280.0, 160.0, UP, return_x=True)
    assert penalty(x, UP) == pytest.approx(V)
    assert x.mean() == pytest.approx(280.0) and pop_sd(x) == pytest.approx(160.0)
    # joint bound strictly below the sum of componentwise sharp bounds
    comp = sum(bound_finite(12, 280.0, 160.0, K, dp) for K, dp in zip(UP.thresholds, UP.increments))
    assert V < 0.75 * comp
