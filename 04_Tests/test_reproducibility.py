import numpy as np, pandas as pd
import simulations as sim

def test_seeded_panel_deterministic():
    a = sim.stylised_panel(seed=123); b = sim.stylised_panel(seed=123); c = sim.stylised_panel(seed=124)
    pd.testing.assert_frame_equal(a, b)
    assert not np.allclose(a["kwh30"], c["kwh30"])

def test_output_files_generated(tmp_path, monkeypatch):
    import experiments
    monkeypatch.setattr(experiments, "OUT", tmp_path)
    panel = sim.stylised_panel(n_households=20, seed=1)
    experiments.exp_stress(); experiments.exp_household(panel); experiments.exp_billing_period(panel)
    for f in ["Stress_Tests.csv", "Household_Penalties.csv", "Bound_Comparisons.csv", "Billing_Period_Results.csv"]:
        assert (tmp_path / f).exists() and (tmp_path / f).stat().st_size > 0
