"""Household-cluster bootstrap.  Households (not household-months) are the
resampling unit, optionally stratified by district.  Percentile intervals.
On synthetic data the interval describes only Monte-Carlo variability of the
synthetic design; it is not an inferential statement about any population."""
from __future__ import annotations

import numpy as np
import pandas as pd


def cluster_bootstrap(per_household: pd.DataFrame, stat, B: int = 2000, seed: int = 1,
                      strata: str | None = None, alpha: float = 0.05) -> dict:
    rng = np.random.default_rng(seed)
    est = float(stat(per_household))
    draws = np.empty(B)
    if strata is None:
        idx = np.arange(len(per_household))
        for b in range(B):
            draws[b] = stat(per_household.iloc[rng.choice(idx, idx.size, replace=True)])
    else:
        groups = [g.index.to_numpy() for _, g in per_household.groupby(strata)]
        for b in range(B):
            take = np.concatenate([rng.choice(g, g.size, replace=True) for g in groups])
            draws[b] = stat(per_household.loc[take])
    lo, hi = np.quantile(draws, [alpha / 2, 1 - alpha / 2])
    return {"estimate": est, "ci_low": float(lo), "ci_high": float(hi), "B": B, "seed": seed}
