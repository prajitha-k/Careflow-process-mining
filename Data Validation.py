from pathlib import Path
import pandas as pd

base = Path(__file__).parent / "data"
df = pd.read_csv(base / "Careflow.csv")

# 1) fix data types
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Activity_End_Time"] = pd.to_datetime(df["Activity_End_Time"])
df = df.sort_values(["Case_ID", "Timestamp"]).reset_index(drop=True)

# 2) checks - each line prints PASS or FAIL
g = df.groupby("Case_ID")
checks = {
    "required columns present": {"Case_ID", "Activity_Name", "Timestamp"} <= set(df.columns),
    "no missing values in required columns": df[["Case_ID", "Activity_Name", "Timestamp"]].notna().all().all(),
    "Case_ID repeats (events per case > 1)": g.size().min() > 1,
    "every case starts with Patient Registered": (g.Activity_Name.first() == "Patient Registered").all(),
    "every case ends with Discharged": (g.Activity_Name.last() == "Discharged").all(),
    "patient attributes constant within a case":
        (g[["Patient_Age", "Patient_Gender", "Diagnosis_Category", "Priority_Level"]].nunique() == 1).all().all(),
    "no duplicate events": not df.duplicated(["Case_ID", "Activity_Name", "Timestamp"]).any(),
}
for name, ok in checks.items():
    print("PASS" if ok else "FAIL", "-", name)
print(f"\n{df.Case_ID.nunique()} cases, {len(df)} events")
assert all(checks.values()), "Fix the failing checks before moving on"

df.to_csv(base / "Validation and cleaning.csv", index=False)
print("saved data/ Validation and cleaning.csv")
