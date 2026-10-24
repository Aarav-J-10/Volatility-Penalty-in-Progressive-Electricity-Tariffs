"""Observed-data analysis (CEEW Mathura/Bareilly).  NOT YET EXECUTED on real data.
spec = {"files": [{"path": ..., "district": ...}], "columns": {ColumnSpec fields}, "interval_minutes": 3,
        "window": ["2020-01", "2020-12"]}"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
from data_ingest import ColumnSpec, load, inspect_file
from cleaning import clean_to_daily
from build_panel import monthly_panel, eligible_households
from tariff_models import UP_URBAN_DOMESTIC_FY2019_20 as UP
from theory import penalty, pop_sd, multi_tier_bounds
from uncertainty import cluster_bootstrap

OUT = Path(__file__).resolve().parents[1] / "05_Computational_Results" / "observed"


def run(spec: dict) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    cs = ColumnSpec(**spec["columns"])
    daily, log = [], []
    for f in spec["files"]:
        raw = load(f["path"], cs)
        if "district" in f:
            raw["district"] = f["district"]
        daily.append(clean_to_daily(raw, spec.get("interval_minutes", 3.0), log))
    daily = pd.concat(daily)
    panel = monthly_panel(daily)
    el = eligible_households(panel, tuple(spec["window"]))
    rows = []
    for (h, dist), g in el.groupby(["household", "district"]):
        g = g.sort_values("ym")
        x, L = g["kwh"].to_numpy(), g["days_in_month"].to_numpy()
        bills = UP.bill(x, L)
        V = penalty(x, UP, days=L)
        rows.append(dict(household=h, district=dist, months=len(x), mean=x.mean(), sd=pop_sd(x),
                         V=V, V_share_pct=100 * V / bills.sum()))
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "Observed_Household_Penalties.csv", index=False)
    pd.DataFrame(log, columns=["rule", "count"]).to_csv(OUT / "Cleaning_Log.csv", index=False)
    summ = {"households": int(len(res)),
            "mean_share_ci": cluster_bootstrap(res, lambda d: d["V_share_pct"].mean(), strata="district")}
    return summ
