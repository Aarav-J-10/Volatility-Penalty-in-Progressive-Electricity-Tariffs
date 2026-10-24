"""Constrained two-tier tariff design.

theta = (p1, dp, K), p2 = p1 + dp.  For a FIXED threshold K every quantity is
linear in (p1, dp):
    bill_h,t   = p1 x_ht + dp (x_ht - K)_+
    V_h        = dp * W_h(K),          W_h(K) = sum_t (x_ht-K)_+ - n (xbar_h-K)_+
    revenue R  = p1 * sum x + dp * sum (x-K)_+
    afford.    = p1 * min(x_b, K) + dp * (x_b - K)_+   <= A_max
Hence for each K the design problem is a 2-variable linear programme, solved
exactly with HiGHS; K is searched on a grid (default 1 kWh).  Because the
objective is c(K)*dp with c(K) >= 0, the LP optimum puts dp at the smallest
feasible value; the threshold choice carries the substantive trade-off.

Existence: the feasible set {(p1,dp,K)} is closed and bounded (prices and K in
compact boxes) and the objectives are continuous, so minimisers exist whenever
the set is non-empty (Weierstrass).  The grid search is exact in (p1,dp) and
grid-exact in K; reported optima are 'grid-global', not certified continuous
optima.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
from scipy.optimize import linprog

from theory import bound_finite_nonneg, hinge_gap, pop_sd


@dataclass
class DesignConstraints:
    dp_min: float = 0.5          # minimum progressivity (Rs/kWh)
    p_min: float = 3.0
    p_max: float = 9.0           # bound on p2
    rev_lo: float = 0.99         # revenue as share of reference revenue
    rev_hi: float = 1.01
    basic_kwh: float = 100.0     # affordability reference consumption
    afford_max: float | None = None  # max bill at basic_kwh (Rs); default = reference bill
    cover_lo: float = 0.10       # min share of household-months above K
    cover_hi: float = 0.60       # max share
    K_grid: tuple = (50.0, 600.0, 1.0)


def _stats(X: np.ndarray, K: float):
    W = np.array([hinge_gap(row, K) for row in X])
    H = np.maximum(X - K, 0).sum()
    cover = (X > K).mean()
    return W, H, cover


def robust_U(X: np.ndarray, K: float) -> np.ndarray:
    """Per-household moment-based worst case (Theorem 2) per unit dp."""
    n = X.shape[1]
    return np.array([bound_finite_nonneg(n, r.mean(), pop_sd(r), K, 1.0) for r in X])


def design(X: np.ndarray, ref_revenue: float, ref_afford: float, objective: str = "minimax",
           c: DesignConstraints = DesignConstraints()) -> dict:
    """objective in {'mean', 'minimax', 'robust'}. X: households x periods (kWh, equal-length periods)."""
    A_max = c.afford_max if c.afford_max is not None else ref_afford
    total = X.sum()
    best = None
    diag = {"K_evaluated": 0, "K_feasible": 0}
    for K in np.arange(*c.K_grid):
        diag["K_evaluated"] += 1
        W, H, cover = _stats(X, K)
        if not (c.cover_lo <= cover <= c.cover_hi):
            continue
        if objective == "mean":
            coef = W.mean()
        elif objective == "minimax":
            coef = W.max()
        elif objective == "robust":
            coef = robust_U(X, K).max()
        else:
            raise ValueError(objective)
        # variables z = (p1, dp); minimise coef*dp (+ tiny tie-break on p1 for determinism)
        cost = np.array([1e-9, coef])
        A_ub = [
            [total, H],                     # R <= rev_hi
            [-total, -H],                   # R >= rev_lo
            [min(c.basic_kwh, K), max(c.basic_kwh - K, 0.0)],  # affordability
            [1.0, 1.0],                     # p2 <= p_max
        ]
        b_ub = [c.rev_hi * ref_revenue, -c.rev_lo * ref_revenue, A_max, c.p_max]
        bounds = [(c.p_min, c.p_max), (c.dp_min, c.p_max - c.p_min)]
        r = linprog(cost, A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=bounds, method="highs")
        if r.status != 0:
            continue
        diag["K_feasible"] += 1
        p1, dp = r.x
        val = coef * dp
        if best is None or val < best["objective"] - 1e-9:
            best = dict(objective=float(val), K=float(K), p1=float(p1), dp=float(dp), p2=float(p1 + dp),
                        coverage=float(cover), lp_status=r.message)
    if best is None:
        return {"feasible": False, **diag, "constraints": asdict(c)}
    K, p1, dp = best["K"], best["p1"], best["dp"]
    W, H, cover = _stats(X, K)
    best["_cover_prev"] = float((X > K - c.K_grid[2]).mean())
    best["_cover_next"] = float((X > K + c.K_grid[2]).mean())
    V = dp * W
    rev = p1 * total + dp * H
    best.update(
        feasible=True, revenue=float(rev), revenue_ratio=float(rev / ref_revenue),
        afford_bill=float(p1 * min(c.basic_kwh, K) + dp * max(c.basic_kwh - K, 0)),
        V_mean=float(V.mean()), V_max=float(V.max()), V_p90=float(np.quantile(V, 0.9)),
        active=_active(best, rev, ref_revenue, A_max, c), **diag, constraints=asdict(c), objective_name=objective,
    )
    return best


def _active(b, rev, ref, A_max, c, tol=1e-6):
    act = []
    if abs(b["dp"] - c.dp_min) < tol: act.append("dp_min")
    if abs(b["p1"] - c.p_min) < tol: act.append("p_min")
    if abs(b["p2"] - c.p_max) < tol: act.append("p_max")
    if abs(rev - c.rev_hi * ref) / ref < tol: act.append("revenue_upper")
    if abs(rev - c.rev_lo * ref) / ref < tol: act.append("revenue_lower")
    afford = b["p1"] * min(c.basic_kwh, b["K"]) + b["dp"] * max(c.basic_kwh - b["K"], 0)
    if abs(afford - A_max) < 1e-4: act.append("affordability")
    step = c.K_grid[2]
    if b["K"] - step >= c.K_grid[0] and b.get("_cover_prev") is not None and b["_cover_prev"] > c.cover_hi:
        act.append("coverage_upper")
    if b.get("_cover_next") is not None and b["_cover_next"] < c.cover_lo:
        act.append("coverage_lower")
    return act


def degenerate_examples(X: np.ndarray) -> dict:
    """Why constraints are needed: unconstrained minimisers are trivial."""
    return {
        "flat_tariff_dp0": float(sum(0.0 * hinge_gap(r, 150.0) for r in X)),
        "threshold_above_all_demand": float(sum(hinge_gap(r, X.max() + 1) for r in X)),
        "threshold_below_all_demand": float(sum(hinge_gap(r, max(X.min() - 1, 0)) for r in X)),
    }
