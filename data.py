from pathlib import Path
import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)
N_CASES = 300
LOOPBACK_RATE = 0.40 # share of radiology cases sent back to Triage
START = datetime(2026, 10, 1, 6, 0)

STAFF = {"Admin": [f"STF{i:03d}" for i in range(1, 6)],
         "Nurse": [f"STF{i:03d}" for i in range(6, 14)],
         "Doctor": [f"STF{i:03d}" for i in range(14, 20)],
         "Technician": [f"STF{i:03d}" for i in range(20, 26)]}

# activity: (department, role, typical duration range in minutes)
ACT = {
    "Patient Registered": ("Reception", "Admin", (3, 10)),
    "Triage Started": ("Triage", "Nurse", (5, 15)),
    "Triage Completed": ("Triage", "Nurse", (2, 5)),
    "Vitals Recorded": ("Triage", "Nurse", (3, 8)),
    "Doctor Consultation": ("ER", "Doctor", (10, 30)),
    "Lab Test Ordered": ("ER", "Doctor", (2, 5)),
    "Lab Result Received": ("Lab", "Technician", (20, 60)),
    "Radiology Ordered": ("ER", "Doctor", (2, 5)),
    "Radiology Result Received": ("Radiology", "Technician", (15, 45)),
    "Re-evaluation": ("ER", "Doctor", (5, 15)),
    "Treatment Administered": ("ER", "Nurse", (10, 40)),
    "Bed Assigned": ("Ward", "Nurse", (5, 15)),
    "Discharged": ("ER", "Doctor", (3, 10)),
}

def build_path(needs_xray, needs_lab, loopback, admitted):
    p = ["Patient Registered", "Triage Started", "Triage Completed",
         "Vitals Recorded", "Doctor Consultation"]
    if needs_lab:
        p += ["Lab Test Ordered", "Lab Result Received"]
    if needs_xray:
        p += ["Radiology Ordered", "Radiology Result Received"]
        if loopback: # bottleneck: sent back to Triage after X-Ray
            p += ["Triage Started", "Triage Completed", "Re-evaluation"]
        elif random.random() < 0.3:
            p += ["Re-evaluation"]
    if random.random() < 0.5:
        p += ["Treatment Administered"]
    if admitted:
        p += ["Bed Assigned"]
    p += ["Discharged"]
    return p

rows, clock = [], START
for i in range(N_CASES):
    case_id, patient_id = f"V{1001+i}", f"P{1001+i}"
    clock += timedelta(minutes=random.randint(5, 25)) # staggered arrivals
    priority = random.choices(["Emergency", "Urgent", "Normal"], [0.25, 0.45, 0.30])[0]
    patient = dict(
        Patient_Age=random.randint(1, 95),
        Patient_Gender=random.choice(["Male", "Female", "Other"]),
        Priority_Level=priority,
        Arrival_Mode=random.choice(["Walk-in", "Ambulance", "Referral"]),
        Diagnosis_Category=random.choice(["Orthopedic", "Trauma", "Cardiac", "Respiratory",
                                          "Neurological", "Gastrointestinal", "Infection", "Other"]),
        Insurance_Type=random.choice(["Insured", "Self-pay", "Government Scheme"]))
    needs_xray = patient["Diagnosis_Category"] in ("Orthopedic", "Trauma") or random.random() < 0.15
    needs_lab = random.random() < 0.55
    admitted = random.random() < 0.15
    loopback = needs_xray and random.random() < LOOPBACK_RATE
    outcome = "Admitted" if admitted else random.choices(
        ["Discharged", "Referred", "Deceased"], [0.94, 0.05, 0.01])[0]

    t = clock
    for act in build_path(needs_xray, needs_lab, loopback, admitted):
        dept, role, (lo, hi) = ACT[act]
        dur = random.randint(lo, hi)
        wait = random.randint(2, 45) if act != "Patient Registered" else 0
        if act == "Triage Started" and loopback and t > clock + timedelta(minutes=60):
            wait = random.randint(30, 90) # extra queueing on repeat triage
        t += timedelta(minutes=wait)
        rows.append(dict(Case_ID=case_id, Patient_ID=patient_id, Activity_Name=act,
                         Timestamp=t, Activity_End_Time=t + timedelta(minutes=dur),
                         Duration_Minutes=dur, Resource_Staff_ID=random.choice(STAFF[role]),
                         Resource_Role=role, Department=dept, **patient,
                         Outcome_Status=outcome, Case_Status="Closed"))
        t += timedelta(minutes=dur)

df = pd.DataFrame(rows).sort_values(["Case_ID", "Timestamp"])
out = Path(__file__).parent / "data"; out.mkdir(exist_ok=True)
df.to_csv(out / "Careflow.csv", index=False, date_format="%Y-%m-%d %H:%M")
print(len(df), "events,", df.Case_ID.nunique(), "cases")

