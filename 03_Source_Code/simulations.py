"""Clearly SYNTHETIC consumption data.

1. stress_cases(): deterministic edge cases with known theoretical answers.
2. stylised_panel(): a 12-month household panel whose *design* is informed by
   published descriptive statistics for the Mathura/Bareilly sample
   (Agrawal et al. 2020, CEEW: ~280 kWh/month average over May-Oct 2019;
   fan-only homes up to ~200 kWh/month; cooler/AC homes 200-1,000 kWh/month).
   It is NOT observed data, NOT calibrated by estimation, and no empirical claim
   may be based on it.  The seasonal shape is a stylised north-Indian
   cooling season (Apr-Oct high, Dec-Feb low) chosen by assumption.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], float)
SEASON = np.array([0.05, 0.05, 0.20, 0.60, 0.95, 1.00, 0.85, 0.80, 0.75, 0.45, 0.10, 0.05])
TYPES = {  # share, cooling amplitude relative to base (uniform range)
    "fan": (0.40, (0.3, 0.9)),
    "cooler": (0.35, (0.9, 1.9)),
    "ac": (0.25, (1.8, 3.6)),
}


def stylised_panel(n_households: int = 300, seed: int = 20261024, noise_sd: float = 0.10) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    names = list(TYPES)
    shares = np.array([TYPES[t][0] for t in names])
    types = rng.choice(names, size=n_households, p=shares / shares.sum())
    base = rng.lognormal(mean=np.log(115.0), sigma=0.35, size=n_households)  # kWh per 30 days
    rows = []
    for h in range(n_households):
        lo, hi = TYPES[types[h]][1]
        amp = rng.uniform(lo, hi)
        eps = rng.lognormal(0.0, noise_sd, 12)
        kwh30 = base[h] * (1 + amp * SEASON) * eps        # per-30-day rate
        kwh = kwh30 * DAYS / 30.0                          # calendar-month energy
        for t in range(12):
            rows.append((f"S{h:04d}", types[h], MONTHS[t], DAYS[t], kwh[t], kwh30[t]))
    # kwh   : energy in the calendar month (unequal lengths)
    # kwh30 : energy in a 30-day billing cycle centred on that month (equal lengths; primary)
    return pd.DataFrame(rows, columns=["household", "type", "month", "days", "kwh", "kwh30"])


def stress_cases() -> dict:
    """Edge cases (all synthetic).  Values in kWh."""
    return {
        "constant": np.full(12, 180.0),
        "two_point_symmetric": np.array([100.0, 300.0] * 6),
        "zero_inflated": np.array([0, 0, 0, 250, 260, 240, 270, 0, 0, 255, 0, 0], float),
        "seasonal": 150 + 120 * np.sin(np.linspace(0, 2 * np.pi, 12, endpoint=False)),
        "heavy_tailed": np.random.default_rng(3).pareto(2.5, 12) * 120 + 40,
        "rare_peak": np.array([120.0] * 11 + [900.0]),
        "threshold_adjacent": np.array([149.0, 151.0] * 6),
        "mixed_regime": np.array([80, 85, 90, 95, 400, 420, 410, 390, 85, 80, 90, 95], float),
        "on_threshold": np.full(12, 150.0),
        "single_period": np.array([500.0]),
    }
