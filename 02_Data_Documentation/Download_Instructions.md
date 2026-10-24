# Download instructions (for running the observed-data analysis)

1. Open https://doi.org/10.7910/DVN/GOCHJH (Harvard Dataverse; licence CC0 1.0; no registration expected for public files — confirm on the page).
2. Download the dataset documentation/README and the **daily aggregated** files for Mathura and Bareilly if present; download the 3-minute files only if daily files are absent or insufficient (they are up to ~320 MB each).
3. Record for each file: name, version (2.0 expected), download date, and the MD5 shown by Dataverse. Compute SHA-256 locally: `sha256sum <file>`.
4. Put files in a new directory outside the code folder, e.g. `raw/`.
5. Inspect each file: `python -c "import sys; sys.path.insert(0,'03_Source_Code'); import data_ingest, json; print(json.dumps(data_ingest.inspect_file('raw/<file>'), indent=1, default=str))"`
6. From the documentation **and** the inspection report decide: timestamp column, meter-ID column, energy column, and whether energy is `interval` (consumption per row) or `cumulative` (register reading). Do not difference already-aggregated consumption; do not sum cumulative registers.
7. Write `spec.json` (see `09_Reproduction_Guide/Step_by_Step_Instructions.md`) and run `OBSERVED_DATA_SPEC=spec.json python 03_Source_Code/run_all.py`.
