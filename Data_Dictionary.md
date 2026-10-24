# Data Dictionary - CareFlow ER Event Log

The data is simulated (generated with Python). One row = one event in one patient's ER visit.
A visit is identified by `Case_ID`, which is repeated on every event of that visit.

## 1. Event log (`Validation and cleaning.csv`)

| Column | Type | Meaning | Example / allowed values |
|---|---|---|---|
| Case_ID | text | Patient visit ID, the same on every event of the visit. **Process-mining case key.** | V1001 |
| Patient_ID | text | Patient identifier, one per visit in this simulation | P1001 |
| Activity_Name | text | What happened. **Process-mining activity.** | Patient Registered, Triage Started, Triage Completed, Vitals Recorded, Doctor Consultation, Lab Test Ordered, Lab Result Received, Radiology Ordered, Radiology Result Received, Re-evaluation, Treatment Administered, Bed Assigned, Discharged |
| Timestamp | date-time | When the activity started. **Process-mining timestamp.** | 2026-10-01 06:25 |
| Activity_End_Time | date-time | When the activity finished | 2026-10-01 06:31 |
| Duration_Minutes | whole number | Length of the activity in minutes | 2 to 60 |
| Resource_Staff_ID | text | Staff member who did the activity | STF001 |
| Resource_Role | text | Role of that staff member | Admin, Nurse, Doctor, Technician |
| Department | text | Where the activity happened | Reception, Triage, ER, Lab, Radiology, Ward |
| Patient_Age | whole number | Age in years (constant within a visit) | 1 to 95 |
| Patient_Gender | text | Gender (constant within a visit) | Female, Male, Other |
| Priority_Level | text | Urgency assigned to the patient | Emergency, Urgent, Normal |
| Arrival_Mode | text | How the patient arrived | Walk-in, Ambulance, Referral |
| Diagnosis_Category | text | Type of condition | Cardiac, Gastrointestinal, Infection, Neurological, Orthopedic, Respiratory, Trauma, Other |
| Insurance_Type | text | Payment type | Insured, Self-pay, Government Scheme |
| Outcome_Status | text | How the visit ended | Discharged, Admitted, Referred, Deceased |
| Case_Status | text | Whether the visit is finished | Closed |

Only `Case_ID`, `Activity_Name`, and `Timestamp` are required for process mining. The rest is context for filtering.

## 2. Edges table (`edges.csv`) - the process map as a table

| Column | Type | Meaning |
|---|---|---|
| Transition | text | "Step > Next step" label |
| Activity_Name | text | The step the patient was in |
| Next_Activity | text | The step that came next in the same visit |
| Patients | whole number | How many times patients made this move |
| Avg_Gap_Min | decimal | Average minutes between the two steps |

## 3. Cases table (`cases.csv`) - one row per patient visit

| Column | Type | Meaning |
|---|---|---|
| Case_ID | text | Visit ID |
| Diagnosis_Category, Priority_Level, Arrival_Mode | text | Patient attributes copied from the event log |
| Start | date-time | Time of the first event |
| Total_Minutes | decimal | Minutes from the first to the last event |
| Had_Xray | True/False | The visit includes Radiology Ordered |
| Loop_Back | True/False | Triage Started appears more than once (patient sent back to Triage) |
| Follows_Ideal_Path | True/False | Steps follow Registered, Triage, Vitals, Doctor, Discharged in order, with no loop-back |
| Path | text | The visit's full sequence of steps, joined by " > " |

## 4. Definitions
- **Loop-back:** a patient returns to Triage after an earlier Triage Started.
- **Ideal path:** Patient Registered, Triage Started, Vitals Recorded, Doctor Consultation, Discharged, in that order, with Triage done once.
- **Gap:** minutes between the start of one event and the start of the next event in the same visit.

