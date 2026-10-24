"""All computational experiments.  Synthetic outputs -> 05_Computational_Results/synthetic,
observed-data outputs -> 05_Computational_Results/observed (only if real data are supplied)."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

import optimisation as opt
import simulations as sim
from tariff_models import UP_URBAN_DOMESTIC_FY2019_20 as UP, ILLUSTRATIVE_TWO_TIER as ILL, two_tier, AllUnitsSlabTariff
from theory import (bound_multitier_exact, penalty, penalty_abs_identity, penalty_minority_identity, threshold_decomposition,
                    bound_sd, bound_mad, bound_scarf, bound_finite, bound_finite_nonneg, bound_bp_nonneg,
                    hinge_gap, pop_sd, mad, multi_tier_bounds)
from uncertainty import cluster_bootstrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "05_Computational_Results" / "synthetic"
SEED = 20261024


def _matrix(panel, col="kwh30"):
    return panel.pivot(index="household", columns="month", values=col)[sim.MONTHS].to_numpy()


# ---------------------------------------------------------------- A + G
def exp_stress():
    rows = []
    for name, x in sim.stress_cases().items():
        for T in (ILL, UP):
            n = x.size
            r = dict(case=name, tariff=T.name, n=n, mean=x.mean(), sd=pop_sd(x), V=penalty(x, T))
            mt = multi_tier_bounds(x, T)
            r.update({f"U_{k}": v for k, v in mt.items() if k != "V"})
            if len(T.thresholds) == 1:
                K, dp = T.thresholds[0], T.increments[0]
                r["V_abs_identity"] = penalty_abs_identity(x, K, dp)
                r["V_minority_identity"] = penalty_minority_identity(x, K, dp)
                r["U_bp"] = bound_bp_nonneg(n, x.mean(), pop_sd(x), K, dp)
            rows.append(r)
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "Stress_Tests.csv", index=False)
    return df


# ---------------------------------------------------------------- B + C
def exp_household(panel):
    X = _matrix(panel)
    hh = panel.drop_duplicates("household").set_index("household")["type"]
    rows = []
    for hid, x in zip(sorted(panel["household"].unique()), X):
        n = x.size
        bills = UP.bill(x)
        dec = threshold_decomposition(x, UP)
        mt = multi_tier_bounds(x, UP)
        rows.append(dict(
            household=hid, type=hh[hid], mean=x.mean(), sd=pop_sd(x), cv=pop_sd(x) / x.mean(), mad=mad(x),
            annual_bill=bills.sum(), V=penalty(x, UP), V_share_pct=100 * penalty(x, UP) / bills.sum(),
            V_K150=dec[0], V_K300=dec[1], V_K500=dec[2],
            crossings=int(np.sum(np.diff(np.searchsorted(UP.thresholds, x)) != 0)),
            dist_nearest_K=float(np.min(np.abs(x.mean() - np.array(UP.thresholds)))),
            U_sd=mt["sd"], U_mad=mt["mad"], U_scarf=mt["scarf"], U_finite=mt["finite"],
            U_finite_nonneg=mt["finite_nonneg"], U_best=mt["mad_scarf_min"],
            U_exact=bound_multitier_exact(n, x.mean(), pop_sd(x), UP),
            U_bp=sum(bound_bp_nonneg(n, x.mean(), pop_sd(x), K, dp) for K, dp in zip(UP.thresholds, UP.increments)),
        ))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "Household_Penalties.csv", index=False)

    # bound tightness summary (ratios only where U>0)
    summ = []
    for b in ["U_sd", "U_mad", "U_scarf", "U_bp", "U_finite", "U_finite_nonneg", "U_best", "U_exact"]:
        ok = df[b] > 1e-9
        ratio = df.loc[ok, "V"] / df.loc[ok, b]
        summ.append(dict(bound=b, households_with_U_pos=int(ok.sum()), median_ratio=ratio.median(),
                         p10_ratio=ratio.quantile(.1), p90_ratio=ratio.quantile(.9),
                         median_gap_Rs=(df.loc[ok, b] - df.loc[ok, "V"]).median(),
                         max_violation=float((df["V"] - df[b]).max())))
    pd.DataFrame(summ).to_csv(OUT / "Bound_Comparisons.csv", index=False)

    # threshold-level: zero certificates (Theorem 1 / Samuelson) vs Scarf
    cert = []
    for x in X:
        n, m, s = x.size, x.mean(), pop_sd(x)
        for K in UP.thresholds:
            cert.append(dict(K=K, W=hinge_gap(x, K), thm1=bound_finite(n, m, s, K, 1), scarf=bound_scarf(x, K, 1)))
    c = pd.DataFrame(cert)
    zc = pd.DataFrame(dict(
        pairs=[len(c)], W_zero=[int((c.W < 1e-9).sum())],
        thm1_certifies_zero=[int((c.thm1 < 1e-9).sum())],
        scarf_certifies_zero=[int((c.scarf < 1e-9).sum())]))
    zc.to_csv(OUT / "Zero_Certificates.csv", index=False)
    return df


def exp_by_type(df):
    g = df.groupby("type").agg(households=("V", "size"), mean_kwh=("mean", "mean"), cv=("cv", "median"),
                               V_median=("V", "median"), V_p90=("V", lambda v: v.quantile(.9)),
                               share_median=("V_share_pct", "median"), share_p90=("V_share_pct", lambda v: v.quantile(.9)))
    g.to_csv(OUT / "Penalty_By_Type.csv")
    return g


# ---------------------------------------------------------------- D
def exp_billing_period(panel):
    X = _matrix(panel)
    rows = []
    for name, k in [("monthly", 1), ("bimonthly", 2), ("quarterly", 3), ("annual", 12)]:
        Vs = []
        for x in X:
            agg = x.reshape(-1, k).sum(axis=1)               # k-cycle totals
            # B_k(E) = k B(E/k): thresholds scaled with period length
            bills = k * UP.bill(agg / k)
            Vs.append(bills.sum() - x.size * UP.bill(x.mean()))
        Vs = np.array(Vs)
        rows.append(dict(period=name, cycles_per_bill=k, V_mean=Vs.mean(), V_median=np.median(Vs), V_p90=np.quantile(Vs, .9)))
    # calendar months with prorated thresholds (perspective) vs equal 30-day cycles
    Xc = _matrix(panel, "kwh")
    Vcal = np.array([penalty(x, UP, days=sim.DAYS) for x in Xc])
    Vunscaled = np.array([UP.bill(x).sum() - UP.bill(x.sum() / 12) * 12 for x in Xc])  # wrong: no proration
    rows.append(dict(period="calendar_months_prorated", cycles_per_bill=np.nan, V_mean=Vcal.mean(), V_median=np.median(Vcal), V_p90=np.quantile(Vcal, .9)))
    rows.append(dict(period="calendar_months_UNPRORATED(incorrect)", cycles_per_bill=np.nan, V_mean=Vunscaled.mean(), V_median=np.median(Vunscaled), V_p90=np.quantile(Vunscaled, .9)))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "Billing_Period_Results.csv", index=False)
    return df


# ---------------------------------------------------------------- threshold sensitivity
def exp_threshold(panel, nshow=3):
    X = _matrix(panel)
    Ks = np.arange(0, 1001, 1.0)
    rows = []
    argmax_ok = 0
    for x in X:
        v = np.array([hinge_gap(x, K) for K in Ks])
        Wbar = hinge_gap(x, x.mean())
        # Proposition 5: max_K W(K) = W(xbar) = n*MAD/2; grid values may not exceed it
        if v.max() <= Wbar + 1e-9 and abs(Wbar - 0.5 * x.size * mad(x)) < 1e-9 * max(1.0, Wbar):
            argmax_ok += 1
    rng = np.random.default_rng(SEED)
    for i in rng.choice(len(X), nshow, replace=False):
        for K in Ks:
            rows.append(dict(household=i, K=K, W=hinge_gap(X[i], K), mean=X[i].mean()))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "Threshold_Sensitivity.csv", index=False)
    json.dump({"households": len(X), "max_W_equals_W_at_mean_and_nMAD/2": argmax_ok, "grid_step_kWh": 1.0},
              open(OUT / "Threshold_Argmax_Check.json", "w"), indent=2)
    return df, argmax_ok


# ---------------------------------------------------------------- E
def exp_optimisation(panel):
    X = _matrix(panel)
    ref_rev = float(UP.bill(X).sum())
    ref_aff = float(UP.bill(100.0))
    base_V = np.array([penalty(x, UP) for x in X])
    rows = [dict(design="A: reference UP 4-tier (reported FY2019-20)", K=150, p1=5.5, p2=7.0, dp=np.nan,
                 revenue_ratio=1.0, afford_bill=ref_aff, V_mean=base_V.mean(), V_max=base_V.max(),
                 V_p90=np.quantile(base_V, .9), objective=np.nan, active="", K_feasible=np.nan)]
    c = opt.DesignConstraints()
    results = {}
    for label, obj in [("B: min mean penalty", "mean"), ("C: minimax penalty", "minimax"), ("D: moment-robust minimax", "robust")]:
        r = opt.design(X, ref_rev, ref_aff, obj, c)
        results[obj] = r
        if not r["feasible"]:
            rows.append(dict(design=label, objective="infeasible"))
            continue
        rows.append(dict(design=label, K=r["K"], p1=r["p1"], p2=r["p2"], dp=r["dp"], revenue_ratio=r["revenue_ratio"],
                         afford_bill=r["afford_bill"], V_mean=r["V_mean"], V_max=r["V_max"], V_p90=r["V_p90"],
                         objective=r["objective"], active=";".join(r["active"]), K_feasible=r["K_feasible"]))
    pd.DataFrame(rows).to_csv(OUT / "Optimisation_Results.csv", index=False)

    # E: frontier of minimax penalty against required progressivity dp_min
    fr = []
    for dpmin in [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0]:
        cc = opt.DesignConstraints(dp_min=dpmin, K_grid=(50.0, 600.0, 2.0))
        r = opt.design(X, ref_rev, ref_aff, "minimax", cc)
        fr.append(dict(dp_min=dpmin, feasible=r["feasible"], V_max=r.get("V_max"), V_mean=r.get("V_mean"),
                       K=r.get("K"), p1=r.get("p1"), p2=r.get("p2")))
    pd.DataFrame(fr).to_csv(OUT / "Pareto_Progressivity.csv", index=False)

    # sensitivity of the design to the affordability and revenue constraints
    sens = []
    for aff_slack, band, cov_hi in [(1.0, (0.99, 1.01), 0.6), (1.0, (0.95, 1.05), 0.6), (None, (0.99, 1.01), 0.6),
                                    (1.0, (0.99, 1.01), 0.5), (1.0, (0.99, 1.01), 0.4), (1.0, (0.99, 1.01), 0.3),
                                    (None, (0.99, 1.01), 0.3)]:
            for obj in ["mean", "minimax", "robust"]:
                cc = opt.DesignConstraints(rev_lo=band[0], rev_hi=band[1], K_grid=(50.0, 600.0, 2.0), cover_hi=cov_hi,
                                           afford_max=(ref_aff * aff_slack) if aff_slack else 1e9)
                r = opt.design(X, ref_rev, ref_aff, obj, cc)
                sens.append(dict(cover_hi=cov_hi, coverage=r.get("coverage"), afford_cap=("none" if aff_slack is None else f"{aff_slack:.2f}x ref"),
                                 revenue_band=f"{band[0]:.2f}-{band[1]:.2f}", objective=obj, feasible=r["feasible"],
                                 K=r.get("K"), p1=r.get("p1"), p2=r.get("p2"), V_mean=r.get("V_mean"), V_max=r.get("V_max"),
                                 afford_bill=r.get("afford_bill"), active=";".join(r.get("active", []))))
    pd.DataFrame(sens).to_csv(OUT / "Optimisation_Sensitivity.csv", index=False)
    json.dump({"degenerate_unconstrained": opt.degenerate_examples(X), "reference_revenue_Rs": ref_rev,
               "reference_bill_at_100kWh": ref_aff, "solver": "scipy.optimize.linprog(method='highs') per K grid point"},
              open(OUT / "Optimisation_Diagnostics.json", "w"), indent=2, default=str)
    return pd.DataFrame(rows), pd.DataFrame(fr)


# ---------------------------------------------------------------- F
def exp_uncertainty(df):
    out = {}
    out["mean_V_share_pct"] = cluster_bootstrap(df.reset_index(drop=True), lambda d: d["V_share_pct"].mean(), B=2000, seed=SEED)
    out["mean_V_share_pct_stratified_by_type"] = cluster_bootstrap(df.reset_index(drop=True), lambda d: d["V_share_pct"].mean(), B=2000, seed=SEED, strata="type")
    seeds = []
    for s in range(20):
        p = sim.stylised_panel(seed=1000 + s)
        X = _matrix(p)
        sh = [100 * penalty(x, UP) / UP.bill(x).sum() for x in X]
        seeds.append(np.mean(sh))
    out["across_20_synthetic_seeds_mean_share_pct"] = {"min": float(np.min(seeds)), "max": float(np.max(seeds)), "mean": float(np.mean(seeds))}
    json.dump(out, open(OUT / "Uncertainty_Synthetic.json", "w"), indent=2)
    return out


# ---------------------------------------------------------------- multi-tier joint sharpness
def exp_joint_sharpness(n=12, m=280.0, s=160.0, starts=200, seed=SEED):
    """Is the sum of per-threshold sharp bounds jointly attainable for UP?"""
    rng = np.random.default_rng(seed)
    cons = [{'type': 'eq', 'fun': lambda x: x.mean() - m}, {'type': 'eq', 'fun': lambda x: np.mean((x - m) ** 2) - s * s}]
    best = 0.0
    for _ in range(starts):
        x0 = np.abs(m + s * rng.standard_normal(n) * rng.uniform(.5, 2))
        r = minimize(lambda x: -penalty(x, UP), x0, constraints=cons, bounds=[(0, None)] * n, method='SLSQP', options={'maxiter': 800})
        if abs(r.x.mean() - m) < 1e-5 and abs(pop_sd(r.x) - s) < 1e-4 and r.x.min() > -1e-7:
            best = max(best, penalty(r.x, UP))
    sum_bounds = sum(bound_finite_nonneg(n, m, s, K, dp) for K, dp in zip(UP.thresholds, UP.increments))
    exact, xstar = bound_multitier_exact(n, m, s, UP, return_x=True)
    res = dict(n=n, mean=m, sd=s, best_found_joint_V=best, exact_joint_max_Thm3=exact,
               exact_extremal_x=[round(v, 3) for v in xstar], extremal_nonnegative=bool(xstar.min() >= 0), sum_of_componentwise_sharp_bounds=sum_bounds,
               componentwise=[bound_finite_nonneg(n, m, s, K, dp) for K, dp in zip(UP.thresholds, UP.increments)],
               note="best_found is a lower bound on the joint maximum (multistart SLSQP, %d starts)" % starts)
    json.dump(res, open(OUT / "Joint_Sharpness.json", "w"), indent=2)
    return res


def exp_all_units_counterexample():
    T = AllUnitsSlabTariff(thresholds=(150.0,), prices=(5.5, 6.0))
    x = np.array([140.0, 166.0])
    V = float(T.bill(x).sum() - x.size * T.bill(x.mean()))
    res = dict(tariff="all-units slab 5.5 / 6.0 at 150 kWh", x=x.tolist(), V=V)
    json.dump(res, open(OUT / "AllUnits_Counterexample.json", "w"), indent=2)
    return res


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    panel = sim.stylised_panel(seed=SEED)
    panel.to_csv(OUT / "Synthetic_Panel.csv", index=False)
    log = {}
    log["stress"] = exp_stress().shape
    hh = exp_household(panel)
    log["by_type"] = exp_by_type(hh).shape
    log["billing"] = exp_billing_period(panel).shape
    _, ok = exp_threshold(panel)
    log["threshold_argmax_ok"] = ok
    exp_optimisation(panel)
    exp_uncertainty(hh)
    log["joint"] = exp_joint_sharpness()
    log["all_units"] = exp_all_units_counterexample()
    return log


if __name__ == "__main__":
    print(run())
