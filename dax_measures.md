# Power BI DAX measures - CareFlow dashboard

All measures are created on the `cases` table (one row per patient visit).

| Measure | DAX | Expected value (no filters) |
|---|---|---|
| Total Visits | `Total Visits = COUNTROWS(cases)` | 300 |
| Avg Time in ER (h) | `Avg Time in ER (h) = DIVIDE(AVERAGE(cases[Total_Minutes]), 60)` | 4.7 |
| Xray Visits | `Xray Visits = CALCULATE([Total Visits], cases[Had_Xray] = TRUE())` | 103 |
| Loop-back Visits | `Loop-back Visits = CALCULATE([Total Visits], cases[Loop_Back] = TRUE())` | 41 |
| Loop-back % | `Loop-back % = DIVIDE([Loop-back Visits], [Xray Visits])` | 39.8% |
| Ideal Path % | `Ideal Path % = DIVIDE(CALCULATE([Total Visits], cases[Follows_Ideal_Path] = TRUE()), [Total Visits])` | 86.3% |

## KPI cards on the dashboard
1. Total Visits - how many patient visits are in the selection
2. Avg Time in ER (h) - average length of a visit
3. Loop-back % - share of X-ray patients sent back to Triage (the key finding)
4. Ideal Path % - share of visits that follow the ideal path with no loop-back

Every card reacts to the slicers (diagnosis, priority, arrival mode), so the administrator can check any patient group.

# Dashboard notes
Process matrix and bottleneck chart now read edges_by_group.csv.
Slicers: diagnosis and priority. Measures: Patients, Avg Wait (min).
Check: with no filter, X-ray result to Triage = 41 patients, about 90 min.
