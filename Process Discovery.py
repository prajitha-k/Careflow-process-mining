from pathlib import Path
import pandas as pd

base = Path(__file__).parent
out = base / "outputs"; out.mkdir(exist_ok=True)
df = pd.read_csv(base / "data" / "Validation and cleaning.csv", parse_dates=["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])

# pair every event with the next event of the SAME case
g = df.groupby("Case_ID")
df["Next_Activity"] = g.Activity_Name.shift(-1)
df["Gap_Min"] = (g.Timestamp.shift(-1) - df.Timestamp).dt.total_seconds() / 60

# edges = the arrows of the process map
edges = (df.dropna(subset=["Next_Activity"])
           .groupby(["Activity_Name", "Next_Activity"])
           .agg(Patients=("Case_ID", "count"), Avg_Gap_Min=("Gap_Min", "mean"))
           .reset_index().round(1))
edges.insert(0, "Transition", edges.Activity_Name + " > " + edges.Next_Activity)
edges.sort_values("Patients", ascending=False).to_csv(out / "edges.csv", index=False)

# variants = the distinct paths patients take, most common first
paths = g.Activity_Name.apply(lambda s: " > ".join(s))
span = g.Timestamp.apply(lambda s: (s.max() - s.min()).total_seconds() / 60)
v = (pd.DataFrame({"Path": paths, "Total_Min": span}).groupby("Path")
       .agg(Cases=("Total_Min", "count"), Avg_Total_Min=("Total_Min", "mean"))
       .reset_index().sort_values("Cases", ascending=False).round(1))
v["Share_%"] = (100 * v.Cases / v.Cases.sum()).round(1)
v.to_csv(out / "variants.csv", index=False)

print(edges.sort_values("Patients", ascending=False).head(8).to_string(index=False))
print(f"\n{len(edges)} transitions, {len(v)} distinct paths")
