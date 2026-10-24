# Step-by-step reproduction

## A. Synthetic results (everything in the manuscript)
1. Python 3.11+ (built with 3.13.17). `pip install -r requirements.txt` (exact versions pinned).
2. From the archive root: `python 03_Source_Code/run_all.py`
   * regenerates `05_Computational_Results/synthetic/*`, `06_Figure_Sources/*`, `07_Additional_Tables/Supplementary_Tables.xlsx`
   * runs `validate.py` (independent recomputation) and `pytest 04_Tests`
   * writes `05_Computational_Results/Execution_Log.txt`
3. Compare with `Expected_Outputs.md`. Synthetic data are seeded (20261024), so values should match to floating-point precision on the same library versions.
4. Theorem checks only: `python -m pytest 04_Tests -q`.

## B. Observed data (not yet done by the author)
1. Follow `02_Data_Documentation/Download_Instructions.md`.
2. Create `spec.json`:
```json
{"files": [{"path": "raw/<mathura_file>", "district": "Mathura"},
           {"path": "raw/<bareilly_file>", "district": "Bareilly"}],
 "columns": {"timestamp": "<col>", "meter": "<col>", "energy": "<col>", "energy_kind": "interval"},
 "interval_minutes": 3, "window": ["2020-01", "2020-12"]}
```
   (`interval_minutes` = 1440 for daily files; `energy_kind` must come from the documentation.)
3. `OBSERVED_DATA_SPEC=spec.json python 03_Source_Code/run_all.py`
4. Inspect `05_Computational_Results/observed/Cleaning_Log.csv` before looking at penalties; then replace the synthetic Results section only after re-running all checks.
