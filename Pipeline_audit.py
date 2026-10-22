import sys
from pathlib import Path
import pandas as pd

src = Path(sys.argv[1] if len(sys.argv) > 1 else "Validation and cleaning.csv")
df = pd.read_csv(src, parse_dates=["Timestamp"]).sort_values(["Case_ID", "Timestamp"])
g = df.groupby("Case_ID")

# ---- validity checks (same rules as the validation step) ----
attrs = [c for c in ["Patient_Age", "Patient_Gender", "Diagnosis_Category", "Priority_Level"] if c in df.columns]
checks = [
    ("Required columns present (Case_ID, Activity_Name, Timestamp)", {"Case_ID", "Activity_Name", "Timestamp"} <= set(df.columns)),
    ("No missing values in required columns", bool(df[["Case_ID", "Activity_Name", "Timestamp"]].notna().all().all())),
    ("Every case has more than one event", bool(g.size().min() > 1)),
    ("Every case starts with 'Patient Registered'", bool((g.Activity_Name.first() == "Patient Registered").all())),
    ("Every case ends with 'Discharged'", bool((g.Activity_Name.last() == "Discharged").all())),
    ("Timestamps never go backwards within a case", bool(g.Timestamp.apply(lambda s: s.is_monotonic_increasing).all())),
    ("Patient attributes constant within a case", bool((g[attrs].nunique() == 1).all().all()) if attrs else True),
    ("No duplicate events", not df.duplicated(["Case_ID", "Activity_Name", "Timestamp"]).any()),
]

# ---- summary numbers ----
per_case = g.size()
duration_h = g.Timestamp.apply(lambda s: (s.max() - s.min()).total_seconds() / 3600)
triage = g.Activity_Name.apply(lambda s: (s == "Triage Started").sum())
acts = df.Activity_Name.value_counts()

lines = [
    "# Pipeline Audit Report", "",
    f"Source file: `{src.name}` (simulated EHR event log)", "",
    "## 1. Dataset summary", "",
    "| Measure | Value |", "|---|---|",
    f"| Events (rows) | {len(df):,} |",
    f"| Cases (patient visits) | {df.Case_ID.nunique():,} |",
    f"| Distinct activities | {df.Activity_Name.nunique()} |",
    f"| Date range | {df.Timestamp.min():%Y-%m-%d %H:%M} to {df.Timestamp.max():%Y-%m-%d %H:%M} |",
    f"| Events per case (min / avg / max) | {per_case.min()} / {per_case.mean():.1f} / {per_case.max()} |",
    f"| Visit length in hours (avg / max) | {duration_h.mean():.1f} / {duration_h.max():.1f} |",
    f"| Cases with a loop-back to Triage | {(triage > 1).sum()} ({100 * (triage > 1).mean():.1f}%) |",
    "", "## 2. Validation checks", "",
    "| Check | Result |", "|---|---|",
] + [f"| {n} | {'PASS' if ok else 'FAIL'} |" for n, ok in checks] + [
    "", "## 3. Activity frequency", "",
    "| Activity | Events |", "|---|---|",
] + [f"| {a} | {n} |" for a, n in acts.items()] + [
    "", "## 4. Conclusion", "",
    f"{sum(ok for _, ok in checks)} of {len(checks)} checks passed. "
    + ("The data flows cleanly from the generator and is ready for process discovery." if all(ok for _, ok in checks)
       else "Fix the failed checks before process discovery."),
    "", "*Note: the data is simulated, so volumes and loop-back rates reflect the generator settings.*", "",
]
Path("audit_report.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
