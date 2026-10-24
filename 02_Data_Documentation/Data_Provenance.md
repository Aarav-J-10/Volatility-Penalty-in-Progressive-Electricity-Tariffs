# Data provenance

## Intended primary source (NOT ACQUIRED)
* **Citation:** Agrawal, S., Mani, S., Ganesan, K., Jain, A. (2021). *High frequency smart meter data from two districts in India (Mathura and Bareilly)*, version 2.0. Harvard Dataverse. doi:10.7910/DVN/GOCHJH
* **Metadata verified via DataCite API on 24 Oct 2026:** creators (CEEW), publisher Harvard Dataverse, year 2021, version 2.0, licence **CC0 1.0**; description: three-minute smart-meter readings from about 100 urban households in Mathura and Bareilly, Uttar Pradesh, May 2019–October 2021, with supply-quality variables (supply hours, voltage, current). DataCite lists 10 files (5 CSV, 4 TSV, 2 text; sizes from 4.4 kB to 323 MB).
* **Not verified (file inventory not reachable):** file names, which files are daily aggregates, column names, units, whether energy is interval or cumulative, timezone, checksums.
* **Acquisition attempts (24 Oct 2026):** shell download from dataverse.harvard.edu → refused by the environment's egress proxy (HTTP 403); web fetch of the dataset page and API → disallowed by the site's robots policy; no browser connected. **Result: no data acquired.**

## Companion report (used only for descriptive context)
Agrawal, S., Mani, S., Ganesan, K., Jain, A. (2020). *What Smart Meters Can Tell Us*. CEEW. Reported (via the CEEW web page): 93 meters in urban households, May–Oct 2019; average 280 kWh/month; fan-only homes up to ~200 kWh/month (the page also says <250 elsewhere); cooler/AC homes 200–1,000 kWh/month. These figures informed the *design* of the synthetic panel; they were not used to estimate anything.

## Synthetic data (USED)
`03_Source_Code/simulations.py::stylised_panel(seed=20261024)`, saved as `05_Computational_Results/synthetic/Synthetic_Panel.csv`. Every manuscript number derives from this file.
