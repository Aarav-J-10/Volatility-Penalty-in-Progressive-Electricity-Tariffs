"""Exact volatility penalties and bounds.

Notation (matching the manuscript):
    x_1..x_n  consumption in n comparable periods, xbar its mean,
    s         POPULATION standard deviation (divide by n),
    MAD       mean absolute deviation about the mean, (1/n) sum |x_i - xbar|,
    d         xbar - K.
"""
from __future__ import annotations

import numpy as np

from tariff_models import MarginalBlockTariff


def _arr(x):
    x = np.asarray(x, float)
    if x.ndim != 1 or x.size == 0:
        raise ValueError("x must be a non-empty 1-D array")
    return x


def pop_sd(x) -> float:
    x = _arr(x)
    return float(np.sqrt(np.mean((x - x.mean()) ** 2)))


def mad(x) -> float:
    x = _arr(x)
    return float(np.mean(np.abs(x - x.mean())))


# ---------------------------------------------------------------- penalties
def penalty(x, tariff: MarginalBlockTariff, days=None) -> float:
    """V = sum_t B(x_t) - n B(xbar)  (equal periods), or with unequal period
    lengths L_t:  V = sum_t B_{L_t}(x_t) - B_{sum L}(sum x)  (perspective form)."""
    x = _arr(x)
    if days is None:
        return float(np.sum(tariff.bill(x)) - x.size * tariff.bill(x.mean()))
    L = np.asarray(days, float)
    return float(np.sum(tariff.bill(x, L)) - tariff.bill(x.sum(), L.sum()))


def hinge_gap(x, K: float) -> float:
    """W(K) = sum (x_i-K)_+ - n (xbar-K)_+ ; the penalty per unit price step."""
    x = _arr(x)
    return float(np.sum(np.maximum(x - K, 0)) - x.size * max(x.mean() - K, 0.0))


def penalty_abs_identity(x, K: float, dp: float) -> float:
    """Proposition 2: V = (dp/2) [ sum|x_i-K| - n|xbar-K| ]."""
    x = _arr(x)
    return float(0.5 * dp * (np.sum(np.abs(x - K)) - x.size * abs(x.mean() - K)))


def penalty_minority_identity(x, K: float, dp: float) -> float:
    """Proposition 2(b): V = dp * sum_{i}(K-x_i)_+ if xbar>=K, else dp * sum (x_i-K)_+."""
    x = _arr(x)
    if x.mean() >= K:
        return float(dp * np.sum(np.maximum(K - x, 0)))
    return float(dp * np.sum(np.maximum(x - K, 0)))


def threshold_decomposition(x, tariff: MarginalBlockTariff) -> np.ndarray:
    """Multi-tier: V = sum_j dp_j W(K_j); returns the vector of dp_j W(K_j)."""
    return np.array([dpj * hinge_gap(x, Kj) for Kj, dpj in zip(tariff.thresholds, tariff.increments)])


# ------------------------------------------------------------------- bounds
def bound_sd(x, dp: float) -> float:
    """U1 = n dp s / 2."""
    x = _arr(x)
    return 0.5 * x.size * dp * pop_sd(x)


def bound_mad(x, dp: float) -> float:
    """U_MAD = n dp MAD / 2 = max_K V(K)  (Proposition 5)."""
    x = _arr(x)
    return 0.5 * x.size * dp * mad(x)


def bound_scarf(x, K: float, dp: float) -> float:
    """U2 = (n dp / 2)(sqrt(s^2 + d^2) - |d|)  (Scarf 1958 / Lo 1987 form)."""
    x = _arr(x)
    s, d = pop_sd(x), x.mean() - K
    return 0.5 * x.size * dp * (np.sqrt(s * s + d * d) - abs(d))


def bound_scarf_moments(n, mean, s, K, dp):
    d = mean - K
    return 0.5 * n * dp * (np.sqrt(s * s + d * d) - abs(d))


def finite_sample_terms(n: int, mean: float, s: float, K: float) -> np.ndarray:
    """A_j = s sqrt(j(n-j)) - j|d|, j = 1..n-1 (Theorem 1)."""
    j = np.arange(1, n)
    return s * np.sqrt(j * (n - j)) - j * abs(mean - K)


def bound_finite(n: int, mean: float, s: float, K: float, dp: float) -> float:
    """Theorem 1: sharp finite-sample bound over all real n-vectors with given
    mean and population sd:  V <= dp * max(0, max_j A_j)."""
    if n < 2:
        return 0.0
    return float(dp * max(0.0, finite_sample_terms(n, mean, s, K).max()))


def bound_finite_nonneg(n: int, mean: float, s: float, K: float, dp: float) -> float:
    """Theorem 2: valid bound for nonnegative consumption:
    V <= dp * max_j min(A_j, c_j), c_j = jK if mean>=K, else n*mean - jK."""
    if n < 2:
        return 0.0
    j = np.arange(1, n)
    A = finite_sample_terms(n, mean, s, K)
    c = j * K if mean >= K else n * mean - j * K
    return float(dp * max(0.0, np.minimum(A, c).max()))


def bound_bp_nonneg(n, mean, s, K, dp):
    """Distributional sharp bound for X>=0 with given mean/variance
    (Lo 1987; Bertsimas & Popescu 2002), expressed for the Jensen gap:
    n dp [ sup E(X-K)_+ - (mean-K)_+ ]."""
    m2 = mean * mean + s * s
    if mean <= 0:
        return 0.0
    if K <= m2 / (2 * mean):
        sup_call = mean - K * mean * mean / m2
    else:
        sup_call = 0.5 * ((mean - K) + np.sqrt(s * s + (mean - K) ** 2))
    return float(n * dp * (sup_call - max(mean - K, 0.0)))


def extremal_configuration(n: int, mean: float, s: float, K: float):
    """Two-point n-vector attaining Theorem 1 (if the max is positive).
    Returns (x, j*)."""
    A = finite_sample_terms(n, mean, s, K)
    jstar = int(np.argmax(A)) + 1
    Aj = A[jstar - 1]
    if Aj <= 0:
        return np.full(n, mean), 0
    d = mean - K
    if d >= 0:  # minority (j points) below K, deficit total Aj
        low = K - Aj / jstar
        high_total = n * mean - jstar * low
        high = high_total / (n - jstar)
        x = np.r_[np.full(jstar, low), np.full(n - jstar, high)]
    else:       # minority (j points) above K, excess total Aj
        high = K + Aj / jstar
        low = (n * mean - jstar * high) / (n - jstar)
        x = np.r_[np.full(jstar, high), np.full(n - jstar, low)]
    return x, jstar


def multi_tier_bounds(x, tariff: MarginalBlockTariff) -> dict:
    """Componentwise bounds summed across thresholds (not jointly sharp)."""
    x = _arr(x)
    n, m, s = x.size, x.mean(), pop_sd(x)
    out = dict(V=penalty(x, tariff), sd=0.0, mad=0.0, scarf=0.0, finite=0.0, finite_nonneg=0.0)
    for Kj, dpj in zip(tariff.thresholds, tariff.increments):
        out["sd"] += bound_sd(x, dpj)
        out["mad"] += bound_mad(x, dpj)
        out["scarf"] += bound_scarf(x, Kj, dpj)
        out["finite"] += bound_finite(n, m, s, Kj, dpj)
        out["finite_nonneg"] += bound_finite_nonneg(n, m, s, Kj, dpj)
    out["mad_scarf_min"] = sum(
        min(bound_mad(x, dpj), bound_finite_nonneg(n, m, s, Kj, dpj))
        for Kj, dpj in zip(tariff.thresholds, tariff.increments))
    return out


# ------------------------------------------------- Theorem 3 (multi-tier, exact)
def _compositions(n: int, parts: int):
    if parts == 1:
        yield (n,)
        return
    for k in range(n + 1):
        for rest in _compositions(n - k, parts - 1):
            yield (k,) + rest


def bound_multitier_exact(n: int, mean: float, s: float, tariff: MarginalBlockTariff, return_x: bool = False):
    """Sharp finite-sample bound for ANY convex marginal-block tariff over real n-vectors
    with given mean and population sd.  B(x) = max_k (p_k x - c_k); for a count vector
    N=(n_0..n_m) the supremum of sum_t (p_{k(t)} x_t - c_{k(t)}) on the sphere
    {sum x = n mean, sum (x-mean)^2 = n s^2} is n*mean*pbar + n*s*sd(p) - sum n_k c_k.
    Since sum_t B(x_t) = max over assignments, the maximum over N is exact and attained."""
    p = np.asarray(tariff.prices, float)
    K = np.asarray(tariff.thresholds, float)
    c = np.r_[0.0, np.cumsum(np.diff(p) * K)]          # B(x) = p_k x - c_k on block k
    base = n * float(tariff.bill(mean))
    best, bestN = -np.inf, None
    for N in _compositions(n, len(p)):
        N = np.asarray(N)
        pbar = (N * p).sum() / n
        sdp = np.sqrt((N * (p - pbar) ** 2).sum() / n)
        val = n * mean * pbar + n * s * sdp - (N * c).sum()
        if val > best:
            best, bestN = val, N
    V = max(best - base, 0.0)
    if not return_x:
        return float(V)
    a = np.repeat(p, bestN)
    if a.std() == 0:
        return float(V), np.full(n, mean)
    x = mean + s * (a - a.mean()) / a.std()
    return float(V), x
