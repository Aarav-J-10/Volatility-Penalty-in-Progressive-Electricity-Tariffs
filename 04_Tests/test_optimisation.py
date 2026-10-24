import numpy as np, pytest
import optimisation as opt
import simulations as sim
from tariff_models import UP_URBAN_DOMESTIC_FY2019_20 as UP, two_tier
from theory import penalty

def _X():
    p = sim.stylised_panel(n_households=60, seed=5)
    return p.pivot(index="household", columns="month", values="kwh30")[sim.MONTHS].to_numpy()

def test_design_feasible_and_constraints_hold():
    X = _X(); ref = UP.bill(X).sum(); aff = UP.bill(100.0)
    c = opt.DesignConstraints(K_grid=(50.0, 600.0, 5.0))
    for obj in ["mean", "minimax", "robust"]:
        r = opt.design(X, ref, aff, obj, c)
        assert r["feasible"]
        assert r["p2"] - r["p1"] >= c.dp_min - 1e-9
        assert c.p_min - 1e-9 <= r["p1"] and r["p2"] <= c.p_max + 1e-9
        assert c.rev_lo - 1e-7 <= r["revenue_ratio"] <= c.rev_hi + 1e-7
        assert r["afford_bill"] <= aff + 1e-6
        assert c.cover_lo <= r["coverage"] <= c.cover_hi
        # recompute penalties with the tariff object
        T = two_tier(r["p1"], r["p2"], r["K"])
        V = np.array([penalty(x, T) for x in X])
        assert V.max() == pytest.approx(r["V_max"], rel=1e-9)
        assert T.bill(X).sum() == pytest.approx(r["revenue"], rel=1e-9)

def test_infeasible_detected():
    X = _X(); ref = UP.bill(X).sum()
    c = opt.DesignConstraints(rev_lo=3.0, rev_hi=3.1, K_grid=(50.0, 600.0, 10.0))
    assert opt.design(X, ref, 550.0, "mean", c)["feasible"] is False

def test_degenerate_examples_zero():
    d = opt.degenerate_examples(_X())
    assert all(abs(v) < 1e-9 for v in d.values())
