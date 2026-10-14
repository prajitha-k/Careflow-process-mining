import csv
import random
from datetime import datetime, timedelta

random.seed(42) # reproducible output

# ---------- Reference data ----------

ACTIVITY_FLOW = [
    "Patient Registered",
    "Triage Started",
    "Triage Completed",
    "Vitals Recorded",
    "Doctor Consultation",
    "Lab Test Ordered",
    "Lab Result Received",
    "Radiology Ordered",
    "Radiology Result Received",
    "Treatment Administered",
    "Bed Assigned",
    "Re-evaluation",
    "Discharged",
]

ROLES = {
    "Patient Registered": "Admin",
    "Triage Started": "Nurse",
    "Triage Completed": "Nurse",
    "Vitals Recorded": "Nurse",
    "Doctor Consultation": "Doctor",
    "Lab Test Ordered": "Doctor",
    "Lab Result Received": "Technician",
    "Radiology Ordered": "Doctor",
    "Radiology Result Received": "Technician",
    "Treatment Administered": "Nurse",
    "Bed Assigned": "Admin",
    "Re-evaluation": "Doctor",
    "Discharged": "Doctor",
}

DEPARTMENTS = {
    "Patient Registered": "Reception",
    "Triage Started": "Triage",
    "Triage Completed": "Triage",
    "Vitals Recorded": "Triage",
    "Doctor Consultation": "ER",
    "Lab Test Ordered": "Lab",
    "Lab Result Received": "Lab",
    "Radiology Ordered": "Radiology",
    "Radiology Result Received": "Radiology",
    "Treatment Administered": "ER",
    "Bed Assigned": "Ward",
    "Re-evaluation": "ER",
    "Discharged": "ER",
}

PRIORITY_LEVELS = ["Emergency", "Urgent", "Normal"]
ARRIVAL_MODES = ["Walk-in", "Ambulance", "Referral"]
DIAGNOSIS_CATEGORIES = ["Cardiac", "Trauma", "Respiratory", "Neurological",
                         "Gastrointestinal", "Infection", "Orthopedic", "Other"]
INSURANCE_TYPES = ["Insured", "Self-pay", "Government Scheme"]
GENDERS = ["Male", "Female", "Other"]
OUTCOMES = ["Admitted", "Discharged", "Referred", "Deceased"]
OUTCOME_WEIGHTS = [0.30, 0.55, 0.10, 0.05]

NUM_CASES = 300 # number of patient visits (increase/decrease as needed)
STAFF_POOL_SIZE = 25 # distinct staff IDs

STAFF_IDS = [f"STF{str(i).zfill(3)}" for i in range(1, STAFF_POOL_SIZE + 1)]
BED_NUMBERS = [f"BED-{str(i).zfill(2)}" for i in range(1, 41)]

START_DATE = datetime(2026, 10, 1, 0, 0)
DAYS_SPAN = 14


def random_timestamp_within_span():
    offset_minutes = random.randint(0, DAYS_SPAN * 24 * 60)
    return START_DATE + timedelta(minutes=offset_minutes)


def build_case(case_index):
    """Builds one patient's full activity trace and returns list of row dicts."""
    case_id = f"V{1000 + case_index}"
    patient_id = f"P{str(random.randint(1, 220)).zfill(4)}"
    age = random.randint(1, 95)
    gender = random.choice(GENDERS)
    priority = random.choices(PRIORITY_LEVELS, weights=[0.25, 0.45, 0.30])[0]
    arrival_mode = random.choices(ARRIVAL_MODES, weights=[0.5, 0.3, 0.2])[0]
    diagnosis = random.choice(DIAGNOSIS_CATEGORIES)
    insurance = random.choice(INSURANCE_TYPES)
    outcome = random.choices(OUTCOMES, weights=OUTCOME_WEIGHTS)[0]
    bed_number = random.choice(BED_NUMBERS)

    # Not every case goes through every activity (adds process variation)
    activities = ["Patient Registered", "Triage Started", "Triage Completed",
                  "Vitals Recorded", "Doctor Consultation"]
    if random.random() < 0.6:
        activities += ["Lab Test Ordered", "Lab Result Received"]
    if random.random() < 0.35:
        activities += ["Radiology Ordered", "Radiology Result Received"]
    if random.random() < 0.5:
        activities.append("Treatment Administered")
    if outcome == "Admitted":
        activities.append("Bed Assigned")
    if random.random() < 0.2:
        activities.append("Re-evaluation")
    activities.append("Discharged")

    current_time = random_timestamp_within_span()
    rows = []
    case_status = "Closed"

    for activity in activities:
        duration = random.randint(5, 90)
        wait_time = random.randint(0, 60)
        start_time = current_time
        end_time = start_time + timedelta(minutes=duration)

        rows.append({
            "Case_ID": case_id,
            "Patient_ID": patient_id,
            "Activity_Name": activity,
            "Timestamp": start_time.strftime("%Y-%m-%d %H:%M"),
            "Activity_Start_Time": start_time.strftime("%Y-%m-%d %H:%M"),
            "Activity_End_Time": end_time.strftime("%Y-%m-%d %H:%M"),
            "Duration_Minutes": duration,
            "Resource_Staff_ID": random.choice(STAFF_IDS),
            "Resource_Role": ROLES[activity],
            "Department": DEPARTMENTS[activity],
            "Patient_Age": age,
            "Patient_Gender": gender,
            "Priority_Level": priority,
            "Arrival_Mode": arrival_mode,
            "Diagnosis_Category": diagnosis,
            "Bed_Number": bed_number if activity in ("Bed Assigned", "Treatment Administered") else "",
            "Insurance_Type": insurance,
            "Outcome_Status": outcome if activity == "Discharged" else "In-Progress",
            "Wait_Time_Minutes": wait_time,
            "Case_Status": case_status if activity == "Discharged" else "Open",
        })

        # next activity starts after this one ends + wait time
        current_time = end_time + timedelta(minutes=wait_time)

    return rows


def main():
    fieldnames = [
        "Case_ID", "Patient_ID", "Activity_Name", "Timestamp",
        "Activity_Start_Time", "Activity_End_Time", "Duration_Minutes",
        "Resource_Staff_ID", "Resource_Role", "Department",
        "Patient_Age", "Patient_Gender", "Priority_Level", "Arrival_Mode",
        "Diagnosis_Category", "Bed_Number", "Insurance_Type",
        "Outcome_Status", "Wait_Time_Minutes", "Case_Status",
    ]

    all_rows = []
    for i in range(1, NUM_CASES + 1):
        all_rows.extend(build_case(i))

    # Sort by Case_ID then Timestamp to mimic a realistic event log
    all_rows.sort(key=lambda r: (r["Case_ID"], r["Timestamp"]))

    with open("er_event_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Generated {len(all_rows)} events across {NUM_CASES} cases -> er_event_log.csv")


if __name__ == "__main__":
    main()