# Cleaning protocol (pre-specified; implemented in cleaning.py / build_panel.py; NOT YET RUN on real data)

Primary rules
* R1 Drop rows whose timestamp, meter ID or energy value cannot be parsed.
* R2 Drop exact duplicate (meter, timestamp) rows, keeping the first.
* R3 Interval energy: negative values → missing. Cumulative registers: daily energy = last − first reading within the day; negative differences (device resets) → missing for that day.
* R4 Daily energy > 100 kWh → implausible → missing (flagged).
* R5 A day with < 90% of expected intervals is missing — never zero-filled.
* R6 Genuine zeros (complete coverage, zero energy) are retained.
* Timestamps localised to Asia/Kolkata if naive.
* Monthly panel: retain household-months with ≥ 90% valid days; scale to full calendar month (sum × days_in_month / valid_days), flag `scaled`.
* Eligibility: ≥ 10 retained months in the analysis window (primary window to be fixed before looking at penalties: the first complete 12 months common to most meters).
* Penalty with unequal months: prorated thresholds (perspective form; Appendix S2).
* Identifiers: meter IDs replaced by salted SHA-256 hashes; no direct identifiers released.

Sensitivity variants (pre-specified)
* 100% completeness instead of 90%.
* No scaling of partial months (drop instead).
* Alternative 12-month windows.
* Excluding months with outage-dominated days (supply-hours variable, if documented).

Every rule logs the number of rows/days it affects (`Cleaning_Log.csv`).
