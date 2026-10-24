"""Household-month panel from cleaned daily energy.

Monthly energy for a complete month is the sum of daily kWh.  A month is
retained (primary rule) only if >= MIN_MONTH_DAYS_SHARE of its calendar days
are valid; retained months with a few missing days are scaled to the full month
(x = sum_valid * days_in_month / n_valid_days) and flagged.  Sensitivity:
strict rule (100% days) and 'no scaling' variants.
Households enter the penalty analysis only with >= MIN_MONTHS retained months
inside a common 12-month window (or a reported alternative window).
"""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

MIN_MONTH_DAYS_SHARE = 0.90
MIN_MONTHS = 10


def anonymise(meter_ids: pd.Series, salt: str = "volatility-penalty") -> pd.Series:
    return meter_ids.map(lambda m: "H" + hashlib.sha256((salt + str(m)).encode()).hexdigest()[:8])


def monthly_panel(daily: pd.DataFrame, min_share: float = MIN_MONTH_DAYS_SHARE, scale: bool = True) -> pd.DataFrame:
    d = daily.copy()
    d["ym"] = d["date"].dt.to_period("M")
    g = d.groupby(["meter", "district", "ym"])
    m = g["kwh"].agg(kwh_valid="sum", n_valid_days="count").reset_index()
    m["days_in_month"] = m["ym"].dt.days_in_month
    m["completeness"] = m["n_valid_days"] / m["days_in_month"]
    m = m[m["completeness"] >= min_share].copy()
    m["kwh"] = m["kwh_valid"] * (m["days_in_month"] / m["n_valid_days"]) if scale else m["kwh_valid"]
    m["scaled"] = scale & (m["completeness"] < 1)
    m["household"] = anonymise(m["meter"])
    return m[["household", "district", "ym", "days_in_month", "kwh", "completeness", "scaled"]]


def eligible_households(panel: pd.DataFrame, window: tuple[str, str], min_months: int = MIN_MONTHS) -> pd.DataFrame:
    lo, hi = pd.Period(window[0], "M"), pd.Period(window[1], "M")
    p = panel[(panel["ym"] >= lo) & (panel["ym"] <= hi)]
    counts = p.groupby("household")["ym"].nunique()
    keep = counts[counts >= min_months].index
    return p[p["household"].isin(keep)].copy()
