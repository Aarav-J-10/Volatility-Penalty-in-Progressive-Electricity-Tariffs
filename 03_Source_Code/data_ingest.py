"""Loading and schema inspection for the CEEW smart-meter dataset
(Agrawal, Mani, Ganesan & Jain, Harvard Dataverse, doi:10.7910/DVN/GOCHJH, v2.0, CC0).

STATUS: the research environment could not reach Harvard Dataverse, so this
module has been tested only on synthetic files that mimic plausible layouts.
Column semantics MUST be confirmed against the dataset documentation before
any result is reported.  The loader therefore never guesses silently: it
returns a schema report and requires an explicit `ColumnSpec`.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ColumnSpec:
    timestamp: str
    meter: str
    energy: str
    energy_kind: str  # "interval" (kWh consumed in the row's interval/day) or "cumulative" (register)
    district: str | None = None
    tz: str = "Asia/Kolkata"

    def __post_init__(self):
        if self.energy_kind not in ("interval", "cumulative"):
            raise ValueError("energy_kind must be 'interval' or 'cumulative'")


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def inspect_file(path, nrows: int = 5000) -> dict:
    """Schema report used to decide (by a human) the ColumnSpec."""
    path = Path(path)
    sep = "\t" if path.suffix.lower() in (".tab", ".tsv") else ","
    df = pd.read_csv(path, sep=sep, nrows=nrows)
    report = {"file": str(path), "columns": list(df.columns), "dtypes": df.dtypes.astype(str).to_dict()}
    numeric = df.select_dtypes("number")
    mono = {}
    for c in numeric.columns:
        s = numeric[c].dropna()
        mono[c] = float((s.diff().dropna() >= 0).mean()) if len(s) > 2 else None
    report["share_nondecreasing"] = mono  # ~1.0 within a meter suggests a cumulative register
    report["head"] = df.head(3).to_dict("records")
    return report


def load(path, spec: ColumnSpec) -> pd.DataFrame:
    path = Path(path)
    sep = "\t" if path.suffix.lower() in (".tab", ".tsv") else ","
    usecols = [spec.timestamp, spec.meter, spec.energy] + ([spec.district] if spec.district else [])
    df = pd.read_csv(path, sep=sep, usecols=usecols)
    out = pd.DataFrame({
        "ts": pd.to_datetime(df[spec.timestamp], errors="coerce"),
        "meter": df[spec.meter].astype(str),
        "raw_energy": pd.to_numeric(df[spec.energy], errors="coerce"),
    })
    out["district"] = df[spec.district].astype(str) if spec.district else path.stem
    if out["ts"].dt.tz is None:
        out["ts"] = out["ts"].dt.tz_localize(spec.tz, nonexistent="NaT", ambiguous="NaT")
    out.attrs["energy_kind"] = spec.energy_kind
    out.attrs["source_sha256"] = sha256(path)
    return out
