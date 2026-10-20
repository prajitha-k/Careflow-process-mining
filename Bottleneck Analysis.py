from pathlib import Path
import pandas as pd

base = Path(__file__).parent
out = base / "outputs"
df = pd.read_csv(base / "data" / "Validation and cleaning.csv", parse_dates=["Timestamp"])
edges = pd.read_csv(out / "edges.csv")

# 1) slowest transitions (ignore rare ones: fewer than 10 patients)
slow = edges[edges.Patients >= 10].sort_values("Avg_Gap_Min", ascending=False)
slow.head(10).to_csv(out / "bottlenecks.csv", index=False)
print(slow.head(5)[["Transition", "Patients", "Avg_Gap_Min"]].to_string(index=False))

# 2) loop-back: Triage Started appears more than once in a case
g = df.groupby("Case_ID")
triage_count = g.Activity_Name.apply(lambda s: (s == "Triage Started").sum())
had_xray = g.Activity_Name.apply(lambda s: (s == "Radiology Ordered").any())
loop = triage_count > 1
total = g.Timestamp.apply(lambda s: (s.max() - s.min()).total_seconds() / 60)

loop_pct = 100 * loop.sum() / had_xray.sum()
extra = total[loop].mean() - total[~loop].mean()
top = slow.iloc[0]

text = f"""# Key finding (draft - edit in your own words)

**Finding:** {loop_pct:.0f}% of patients sent for an X-ray ({loop.sum()} of {had_xray.sum()}) are sent back to Triage.
Those visits last {extra/60:.1f} hours longer on average ({total[loop].mean()/60:.1f} h vs {total[~loop].mean()/60:.1f} h).
The slowest step is **{top.Transition}**, about {top.Avg_Gap_Min:.0f} minutes on average.

**Recommendation:** review what happens after the X-ray result (for example the intake form or hand-off)
so patients can go straight to the doctor instead of back to Triage.

*Note: this data is simulated, so the loop-back rate reflects the generator settings.*
"""
(out / "finding.md").write_text(text)
print("\n" + text)
