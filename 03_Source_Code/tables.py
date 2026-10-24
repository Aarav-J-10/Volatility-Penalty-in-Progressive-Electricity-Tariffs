"""Manuscript and supplementary tables built from computed CSVs (no hard-coded results)."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "05_Computational_Results" / "synthetic"
OUTX = ROOT / "07_Additional_Tables" / "Supplementary_Tables.xlsx"

BOUND_ROWS = [  # (column, label, requires, sharp)
    ("U_sd", "SD bound  nΔp·s/2", "n, s", "Only if x̄ = K and half the periods sit at K ± s"),
    ("U_mad", "MAD bound  nΔp·MAD/2", "n, MAD", "Yes, uniformly over K: equals max over K of V (Prop. 4)"),
    ("U_scarf", "Scarf-type moment bound", "n, x̄, s, K", "Sharp over distributions; not for fixed n"),
    ("U_bp", "Nonnegative-support moment bound", "n, x̄, s, K, x ≥ 0", "Sharp over nonnegative distributions"),
    ("U_finite", "Finite-sample bound (Thm 1)", "n, x̄, s, K", "Sharp over real n-vectors (attained)"),
    ("U_finite_nonneg", "Finite-sample bound, x ≥ 0 (Thm 2)", "n, x̄, s, K, x ≥ 0", "Valid; attained in all numerical tests"),
    ("U_exact", "Joint multi-tier bound (Thm 3)", "n, x̄, s, whole tariff", "Sharp over real n-vectors (attained)"),
]


def main_table() -> pd.DataFrame:
    b = pd.read_csv(RES / "Bound_Comparisons.csv").set_index("bound")
    z = pd.read_csv(RES / "Zero_Certificates.csv").iloc[0]
    rows = []
    for col, lab, req, sharp in BOUND_ROWS:
        r = b.loc[col]
        rows.append(dict(Bound=lab, Inputs=req, Sharpness=sharp,
                         Median=f"{r.median_ratio:.2f}", P90=f"{r.p90_ratio:.2f}", Gap=f"{r.median_gap_Rs:.0f}"))
    return pd.DataFrame(rows), z


def supplementary():
    OUTX.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(OUTX) as w:
        pd.DataFrame([
            ("x_t", "consumption in billing period t (kWh)"), ("n", "number of comparable periods"),
            ("x̄", "mean consumption"), ("s", "population SD (divide by n)"), ("MAD", "mean absolute deviation about x̄"),
            ("K, K_j", "block thresholds (kWh per 30-day period)"), ("Δp, Δp_j", "marginal-price increments (Rs/kWh)"),
            ("V", "volatility penalty: Σ B(x_t) − n B(x̄)"), ("W(K)", "Σ (x_t−K)+ − n (x̄−K)+, so V = Σ_j Δp_j W(K_j)"),
        ], columns=["Symbol", "Meaning"]).to_excel(w, sheet_name="S1_Notation", index=False)
        pd.read_csv(ROOT / "02_Data_Documentation" / "Historical_Tariff_Sources.csv").to_excel(w, sheet_name="S2_Tariff_Sources", index=False)
        hh = pd.read_csv(RES / "Household_Penalties.csv")
        hh.describe().T.round(3).to_excel(w, sheet_name="S3_Synthetic_Summary")
        pd.read_csv(RES / "Penalty_By_Type.csv").round(3).to_excel(w, sheet_name="S4_Penalty_By_Type", index=False)
        pd.read_csv(RES / "Bound_Comparisons.csv").round(4).to_excel(w, sheet_name="S5_Bound_Tightness", index=False)
        pd.read_csv(RES / "Optimisation_Results.csv").round(4).to_excel(w, sheet_name="S6_Optimisation", index=False)
        pd.read_csv(RES / "Optimisation_Sensitivity.csv").round(4).to_excel(w, sheet_name="S7_Design_Sensitivity", index=False)
        pd.read_csv(RES / "Billing_Period_Results.csv").round(3).to_excel(w, sheet_name="S8_Billing_Period", index=False)
        pd.read_csv(RES / "Stress_Tests.csv").round(4).to_excel(w, sheet_name="S9_Stress_Tests", index=False)
    return OUTX


if __name__ == "__main__":
    t, z = main_table(); print(t.to_string()); print(z.to_dict()); print(supplementary())
