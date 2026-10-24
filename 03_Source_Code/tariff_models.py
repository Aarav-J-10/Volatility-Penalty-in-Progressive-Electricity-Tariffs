"""Tariff models for the volatility-penalty study.

All tariffs are *marginal-block* (telescopic) energy-charge schedules unless the
name says otherwise.  Fixed charges are deliberately excluded from the energy
schedule: a per-period fixed charge F contributes n*F to both the actual bills
and the smoothed comparator, so it cancels from the volatility penalty.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class MarginalBlockTariff:
    """B(x) = p0*x + sum_j dp_j * (x - K_j)_+  for monthly consumption x >= 0.

    thresholds: K_1 < ... < K_m (kWh per reference period, e.g. 30 days)
    prices:     p_0, p_1, ..., p_m  (marginal price in each block, Rs/kWh)
    """

    thresholds: tuple
    prices: tuple
    name: str = "tariff"
    period_days: float = 30.0

    def __post_init__(self):
        K = np.asarray(self.thresholds, float)
        p = np.asarray(self.prices, float)
        if len(p) != len(K) + 1:
            raise ValueError("need len(prices) == len(thresholds)+1")
        if np.any(np.diff(K) <= 0) or (len(K) and K[0] <= 0):
            raise ValueError("thresholds must be positive and strictly increasing")

    @property
    def increments(self) -> np.ndarray:
        return np.diff(np.asarray(self.prices, float))

    @property
    def is_convex(self) -> bool:
        return bool(np.all(self.increments >= 0))

    def bill(self, x, days=None) -> np.ndarray:
        """Energy charge. If `days` is given, thresholds are prorated by days/period_days
        (perspective scaling B_L(x) = (L/30) B(30 x / L))."""
        x = np.asarray(x, float)
        K = np.asarray(self.thresholds, float)
        p = np.asarray(self.prices, float)
        if days is None:
            scale = 1.0
        else:
            scale = np.asarray(days, float) / self.period_days
        out = p[0] * x
        for Kj, dpj in zip(K, np.diff(p)):
            out = out + dpj * np.maximum(x - Kj * scale, 0.0)
        return out

    def bill_by_blocks(self, x: float) -> float:
        """Independent slab-by-slab implementation used for cross-checking."""
        K = list(self.thresholds)
        p = list(self.prices)
        edges = [0.0] + K + [np.inf]
        total = 0.0
        for j in range(len(p)):
            lo, hi = edges[j], edges[j + 1]
            if x > lo:
                total += p[j] * (min(x, hi) - lo)
        return total


@dataclass(frozen=True)
class AllUnitsSlabTariff:
    """Non-telescopic slab: the whole consumption is charged at the rate of the
    slab it falls in.  Discontinuous and non-convex; used only for counterexamples."""

    thresholds: tuple
    prices: tuple

    def bill(self, x) -> np.ndarray:
        x = np.asarray(x, float)
        idx = np.searchsorted(np.asarray(self.thresholds, float), x, side="left")
        return np.asarray(self.prices, float)[idx] * x


def two_tier(p1: float, p2: float, K: float, name="two-tier") -> MarginalBlockTariff:
    return MarginalBlockTariff(thresholds=(K,), prices=(p1, p2), name=name)


# Reference scenario: Uttar Pradesh urban domestic metered energy charges for
# FY 2019-20 (UPERC order of September 2019, rates retained in FY 2020-21),
# as reported by Power Line (12 Nov 2020).  Telescopic application is an
# ASSUMPTION flagged in Data_Limitations.md; the primary UPERC order text was
# not retrievable from the research environment.  Fixed charge Rs 110/kW/month
# is excluded because it cancels from the penalty.
UP_URBAN_DOMESTIC_FY2019_20 = MarginalBlockTariff(
    thresholds=(150.0, 300.0, 500.0),
    prices=(5.50, 6.00, 6.50, 7.00),
    name="UP urban domestic (FY2019-20, reported)",
)

# Clean illustrative two-tier schedule with no empirical status.
ILLUSTRATIVE_TWO_TIER = two_tier(5.0, 7.0, 200.0, name="illustrative")
