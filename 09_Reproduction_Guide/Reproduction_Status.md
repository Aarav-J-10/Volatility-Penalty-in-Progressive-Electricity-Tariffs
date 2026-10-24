# Reproduction status (24 Oct 2026)
* Synthetic pipeline: reproduced end-to-end by `run_all.py`; validation all passed; 26/26 tests passed.
* Clean-room check: archive extracted to an empty directory and `pytest` + `run_all.py` re-run — see the verification line appended below by the build script.
* Observed-data pipeline: implemented and unit-tested on synthetic files only; **not run on real data**.
* Clean-room check PASSED (24 Oct 2026): archive unzipped into an empty directory; all SHA-256 checksums verified; pytest 26 passed; run_all.py validation all_passed; regenerated household results identical to shipped results (max abs diff < 1e-9).
