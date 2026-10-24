import numpy as np, pandas as pd, pytest
from data_ingest import ColumnSpec, load, inspect_file
from cleaning import clean_to_daily
from build_panel import monthly_panel, eligible_households

def _fake_interval(tmp_path):
    ts = pd.date_range("2020-01-01", "2020-01-03", freq="3min", inclusive="left")
    df = pd.DataFrame({"time": ts.astype(str), "id": "M1", "kwh": 0.01})
    df = pd.concat([df, df.iloc[[5]]])                     # one duplicate
    df.loc[df.index[10], "kwh"] = -0.5                     # one negative
    df = pd.concat([df, pd.DataFrame({"time": ["bad"], "id": ["M1"], "kwh": [0.1]})])
    p = tmp_path / "fake.csv"; df.to_csv(p, index=False); return p

def test_pipeline_interval(tmp_path):
    p = _fake_interval(tmp_path)
    rep = inspect_file(p)
    assert set(rep["columns"]) == {"time", "id", "kwh"}
    raw = load(p, ColumnSpec("time", "id", "kwh", "interval"))
    log = []
    daily = clean_to_daily(raw, 3.0, log)
    d = dict(log)
    assert d["R1 drop unparseable"] == 1 and d["R2 drop duplicate meter-ts"] == 1
    assert d["R3 negative interval readings set missing"] == 1
    assert len(daily) == 2
    assert daily["kwh"].iloc[0] == pytest.approx(0.01 * 479)   # 480 intervals minus 1 negative

def test_cumulative_and_reset(tmp_path):
    ts = pd.date_range("2020-01-01", periods=960, freq="3min")
    reg = np.cumsum(np.full(960, 0.02)); reg[600:] -= 100      # device reset on day 2
    p = tmp_path / "cum.csv"
    pd.DataFrame({"t": ts.astype(str), "m": "A", "r": reg}).to_csv(p, index=False)
    daily = clean_to_daily(load(p, ColumnSpec("t", "m", "r", "cumulative")), 3.0)
    assert daily["kwh"].iloc[0] == pytest.approx(0.02 * 479)
    assert np.isnan(daily["kwh"].iloc[1])

def test_outlier_and_incomplete_month():
    dates = pd.date_range("2020-01-01", "2020-02-29")
    daily = pd.DataFrame({"meter": "A", "district": "X", "date": dates, "kwh": 5.0, "coverage": 1.0})
    daily.loc[daily.index[40:50], "kwh"] = np.nan          # Feb: 10 missing days -> dropped (19/29 < 0.9)
    panel = monthly_panel(daily)
    assert list(panel["ym"].astype(str)) == ["2020-01"]
    assert panel["kwh"].iloc[0] == pytest.approx(155.0)
    assert eligible_households(panel, ("2020-01", "2020-12"), min_months=1).shape[0] == 1
    assert eligible_households(panel, ("2020-01", "2020-12"), min_months=2).shape[0] == 0

def test_bad_spec():
    with pytest.raises(ValueError):
        ColumnSpec("a", "b", "c", "daily")
