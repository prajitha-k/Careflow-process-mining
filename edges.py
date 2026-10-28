"""WEEK 3-4 - Edges table with filter columns, so Power BI slicers can drill down the process map.
Each row = one step-to-next-step move for one group (diagnosis, priority, arrival mode, doctor).
Total_Gap_Min and Patients are stored as SUMS, so averages stay correct after any filter:
    Avg wait (DAX) = DIVIDE(SUM(edges_by_group[Total_Gap_Min]), SUM(edges_by_group[Patients]))
Run:  python edges_by_group.py                         (uses 'Validation and cleaning.csv')
  or: python edges_by_group.py "path/to/your_clean_file.csv"
Output: edges_by_group.csv
"""
import sys
import pandas as pd

src = sys.argv[1] if len(sys.argv) > 1 else "Validation and cleaning.csv"
df = pd.read_csv(src, parse_dates=["Timestamp"]).sort_values(["Case_ID", "Timestamp"])
g = df.groupby("Case_ID")

# the doctor of each visit = staff member on the Doctor Consultation event
doctor = (df[df.Activity_Name == "Doctor Consultation"].groupby("Case_ID").Resource_Staff_ID.first()
          .rename("Doctor_ID"))
df = df.join(doctor, on="Case_ID")
df["Doctor_ID"] = df["Doctor_ID"].fillna("Unknown")

df["Next_Activity"] = g.Activity_Name.shift(-1)
df["Gap_Min"] = (g.Timestamp.shift(-1) - df.Timestamp).dt.total_seconds() / 60
pairs = df.dropna(subset=["Next_Activity"])

keys = ["Activity_Name", "Next_Activity", "Diagnosis_Category", "Priority_Level", "Arrival_Mode", "Doctor_ID"]
out = (pairs.groupby(keys).agg(Patients=("Case_ID", "count"), Total_Gap_Min=("Gap_Min", "sum"))
             .reset_index().round({"Total_Gap_Min": 1}))
out.insert(0, "Transition", out.Activity_Name + " > " + out.Next_Activity)
out.to_csv("edges_by_group.csv", index=False)

# sanity check: totals must match the overall edges table
loop = out[out.Transition == "Radiology Result Received > Triage Started"]
print(f"saved edges_by_group.csv ({len(out)} rows)")
print("loop-back patients:", loop.Patients.sum(), "| average wait:",
      round(loop.Total_Gap_Min.sum() / loop.Patients.sum(), 1), "min")   # expect 41 and about 90