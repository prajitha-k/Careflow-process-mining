# Pipeline Audit Report

Source file: `Validation and cleaning.csv` (simulated EHR event log)

## 1. Dataset summary

| Measure | Value |
|---|---|
| Events (rows) | 2,635 |
| Cases (patient visits) | 300 |
| Distinct activities | 13 |
| Date range | 2026-10-01 06:25 to 2026-10-04 18:43 |
| Events per case (min / avg / max) | 6 / 8.8 / 15 |
| Visit length in hours (avg / max) | 4.7 / 10.1 |
| Cases with a loop-back to Triage | 41 (13.7%) |

## 2. Validation checks

| Check | Result |
|---|---|
| Required columns present (Case_ID, Activity_Name, Timestamp) | PASS |
| No missing values in required columns | PASS |
| Every case has more than one event | PASS |
| Every case starts with 'Patient Registered' | PASS |
| Every case ends with 'Discharged' | PASS |
| Timestamps never go backwards within a case | PASS |
| Patient attributes constant within a case | PASS |
| No duplicate events | PASS |

## 3. Activity frequency

| Activity | Events |
|---|---|
| Triage Started | 341 |
| Triage Completed | 341 |
| Patient Registered | 300 |
| Vitals Recorded | 300 |
| Doctor Consultation | 300 |
| Discharged | 300 |
| Treatment Administered | 153 |
| Lab Test Ordered | 139 |
| Lab Result Received | 139 |
| Radiology Ordered | 103 |
| Radiology Result Received | 103 |
| Re-evaluation | 65 |
| Bed Assigned | 51 |

## 4. Conclusion

8 of 8 checks passed. The data flows cleanly from the generator and is ready for process discovery.

*Note: the data is simulated, so volumes and loop-back rates reflect the generator settings.*
