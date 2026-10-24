"""Integrity cross-checks on produced results (independent of the code that produced them)."""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
import simulations as sim
from tariff_models import UP_URBAN_DOMESTIC_FY2019_20 as UP, two_tier

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "05_Computational_Results" / "synthetic"


def brute_penalty(x, T):
    bills = [T.bill_by_blocks(v) for v in x]
    return sum(bills) - len(x) * T.bill_by_blocks(float(np.mean(x)))


def run() -> dict:
    checks = {}
    hh = pd.read_csv(RES / "Household_Penalties.csv")
    panel = pd.read_csv(RES / "Synthetic_Panel.csv")
    X = panel.pivot(index="household", columns="month", values="kwh30")[sim.MONTHS]
    brute = np.array([brute_penalty(X.loc[h].to_numpy(), UP) for h in hh["household"]])
    checks["household_V_matches_block_by_block"] = bool(np.allclose(brute, hh["V"], atol=1e-6))
    checks["decomposition_sums"] = bool(np.allclose(hh[["V_K150", "V_K300", "V_K500"]].sum(1), hh["V"], atol=1e-6))
    for b in ["U_sd", "U_mad", "U_scarf", "U_bp", "U_finite", "U_finite_nonneg", "U_best", "U_exact"]:
        checks[f"no_violation_{b}"] = bool((hh["V"] <= hh[b] + 1e-7).all())
    opt = pd.read_csv(RES / "Optimisation_Results.csv")
    for _, r in opt.iloc[1:].iterrows():
        T = two_tier(r.p1, r.p2, r.K)
        Xa = X.to_numpy()
        V = np.array([brute_penalty(x, T) for x in Xa])
        checks[f"opt_{r.design[:1]}_Vmax_recomputed"] = bool(np.isclose(V.max(), r.V_max))
        checks[f"opt_{r.design[:1]}_revenue_ratio"] = bool(np.isclose(T.bill(Xa).sum() / UP.bill(Xa).sum(), r.revenue_ratio))
    checks["all_passed"] = all(checks.values())
    json.dump(checks, open(RES / "Validation_Checks.json", "w"), indent=2)
    return checks


if __name__ == "__main__":
    c = run(); print(json.dumps(c, indent=1)); sys.exit(0 if c["all_passed"] else 1)
