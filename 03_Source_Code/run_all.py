"""One-command reproduction:  python 03_Source_Code/run_all.py
Synthetic pipeline always runs.  The observed-data pipeline runs only when
OBSERVED_DATA_SPEC (a JSON file describing local data files and ColumnSpec,
see 09_Reproduction_Guide/Step_by_Step_Instructions.md) is provided."""
from __future__ import annotations
import json, os, platform, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))


def main():
    t0 = time.time()
    log = {"python": sys.version, "platform": platform.platform(), "started": time.strftime("%Y-%m-%d %H:%M:%S")}
    import experiments, figures, tables, validate
    log["experiments"] = str(experiments.run())
    figures.main_figure(); figures.supp_figures()
    tables.supplementary()
    log["validation"] = validate.run()
    spec = os.environ.get("OBSERVED_DATA_SPEC")
    if spec:
        import observed
        log["observed"] = observed.run(json.load(open(spec)))
    else:
        log["observed"] = "NOT RUN: no observed data supplied (Dataverse not reachable from build environment)"
    r = subprocess.run([sys.executable, "-m", "pytest", str(ROOT / "04_Tests"), "-q"], capture_output=True, text=True)
    log["pytest"] = r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr
    log["seconds"] = round(time.time() - t0, 1)
    out = ROOT / "05_Computational_Results" / "Execution_Log.txt"
    out.write_text(json.dumps(log, indent=2, default=str) + "\n\n=== pytest output ===\n" + r.stdout)
    print(json.dumps(log, indent=2, default=str))
    return 0 if (log["validation"]["all_passed"] and r.returncode == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
