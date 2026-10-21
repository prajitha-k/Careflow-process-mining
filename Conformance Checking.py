from pathlib import Path
import pandas as pd

base = Path(__file__).parent
out = base / "outputs"
df = pd.read_csv(base / "data" / "Validation and cleaning.csv", parse_dates=["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])

IDEAL = ["Patient Registered", "Triage Started", "Vitals Recorded", "Doctor Consultation", "Discharged"]

rows = []
for cid, x in df.groupby("Case_ID"):
    steps = list(x.Activity_Name)
    loop_back = steps.count("Triage Started") > 1
    pos = [steps.index(a) if a in steps else -1 for a in IDEAL]
    in_order = -1 not in pos and pos == sorted(pos)
    first = x.iloc[0]
    rows.append({
        "Case_ID": cid,
        "Diagnosis_Category": first.Diagnosis_Category,
        "Priority_Level": first.Priority_Level,
        "Arrival_Mode": first.Arrival_Mode,
        "Start": x.Timestamp.min(),
        "Total_Minutes": round((x.Timestamp.max() - x.Timestamp.min()).total_seconds() / 60, 1),
        "Had_Xray": "Radiology Ordered" in steps,
        "Loop_Back": loop_back,
        "Follows_Ideal_Path": in_order and not loop_back,
        "Path": " > ".join(steps),
    })
cases = pd.DataFrame(rows)
cases.to_csv(out / "cases.csv", index=False)

summary = (cases.groupby("Diagnosis_Category")
           .agg(Cases=("Case_ID", "count"),
                Compliant_pct=("Follows_Ideal_Path", lambda s: round(100 * s.mean(), 1)),
                Loop_Back_pct=("Loop_Back", lambda s: round(100 * s.mean(), 1)))
           .reset_index())
summary.to_csv(out / "conformance_summary.csv", index=False)

print(f"Compliant with ideal path: {100 * cases.Follows_Ideal_Path.mean():.1f}%")
print(summary.to_string(index=False))
