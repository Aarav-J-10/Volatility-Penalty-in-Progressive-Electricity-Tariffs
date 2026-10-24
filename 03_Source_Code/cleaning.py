"""Auditable cleaning of smart-meter readings into daily household energy.

Pre-specified primary rules (see 02_Data_Documentation/Cleaning_Protocol.md):
  R1 drop rows with unparseable timestamp, meter id or energy value;
  R2 drop exact duplicate (meter, ts) rows, keeping the first;
  R3 interval data: negative values are invalid -> set missing;
     cumulative data: daily energy = last - first register reading of the day;
     negative differences (device reset) -> missing for that day;
  R4 daily energy above DAILY_MAX_KWH flagged as implausible -> missing;
  R5 a day is 'complete' only if its interval coverage >= MIN_DAY_COVERAGE;
     incomplete days are missing, never zero-filled;
  R6 genuine zeros (complete coverage, zero energy) are retained.
Every rule logs how many rows/days it touched.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

DAILY_MAX_KWH = 100.0      # conservative ceiling for an urban Indian household-day
MIN_DAY_COVERAGE = 0.90    # share of expected intervals present


def clean_to_daily(df: pd.DataFrame, interval_minutes: float | None = 3.0, log: list | None = None) -> pd.DataFrame:
    log = log if log is not None else []
    kind = df.attrs.get("energy_kind", "interval")
    n0 = len(df)
    df = df.dropna(subset=["ts", "meter", "raw_energy"])
    log.append(("R1 drop unparseable", n0 - len(df)))
    n1 = len(df)
    df = df.drop_duplicates(subset=["meter", "ts"], keep="first")
    log.append(("R2 drop duplicate meter-ts", n1 - len(df)))
    df = df.sort_values(["meter", "ts"])
    df["date"] = df["ts"].dt.tz_convert("Asia/Kolkata").dt.date if df["ts"].dt.tz is not None else df["ts"].dt.date

    if kind == "interval":
        neg = df["raw_energy"] < 0
        log.append(("R3 negative interval readings set missing", int(neg.sum())))
        df.loc[neg, "raw_energy"] = np.nan
        g = df.groupby(["meter", "district", "date"])
        daily = g["raw_energy"].agg(kwh="sum", n_valid="count").reset_index()
        if interval_minutes:
            daily["coverage"] = daily["n_valid"] / (24 * 60 / interval_minutes)
        else:
            daily["coverage"] = 1.0
    else:
        g = df.groupby(["meter", "district", "date"])
        daily = g["raw_energy"].agg(first="first", last="last", n_valid="count").reset_index()
        daily["kwh"] = daily["last"] - daily["first"]
        bad = daily["kwh"] < 0
        log.append(("R3 negative register differences (resets) set missing", int(bad.sum())))
        daily.loc[bad, "kwh"] = np.nan
        daily["coverage"] = daily["n_valid"] / (24 * 60 / interval_minutes) if interval_minutes else 1.0
        daily = daily.drop(columns=["first", "last"])

    hi = daily["kwh"] > DAILY_MAX_KWH
    log.append(("R4 implausible daily kWh set missing", int(hi.sum())))
    daily.loc[hi, "kwh"] = np.nan
    low_cov = daily["coverage"] < MIN_DAY_COVERAGE
    log.append(("R5 incomplete days set missing", int(low_cov.sum())))
    daily.loc[low_cov, "kwh"] = np.nan
    log.append(("R6 genuine zero days retained", int(((daily["kwh"] == 0) & ~low_cov).sum())))
    daily["date"] = pd.to_datetime(daily["date"])
    return daily[["meter", "district", "date", "kwh", "coverage"]]
