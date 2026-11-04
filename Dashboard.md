# CareFlow dashboard

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

## Dashboard notes
1.Process matrix and bottleneck chart now read edges_by_group.csv.

2.Slicers: diagnosis and priority. Measures: Patients, Avg Wait (min).

3.Check: with no filter, X-ray result to Triage = 41 patients, about 90 min.

## Conformance page
1.Ideal path: Registered, Triage, Vitals, Doctor, Discharged, in order, with Triage done once.

2.Measures: Compliant Visits, Deviating Visits, Path Status (calculated column).

3.Visuals: compliant versus deviating donut, ideal path % by diagnosis, top 5 paths table.

4.Check: 259 compliant and 41 deviating of 300 visits; Trauma has the lowest compliance (about 56%).

## Dashboard
Power BI dashboard with KPI cards, a patient-flow matrix, a bottleneck chart and a conformance page.
DAX measures are listed in dax_measures.md.

## CareFlow – ER Pathway Dashboard

*CareFlow is a Power BI dashboard designed to analyze patient journeys and workflows in the Emergency Room (ER).  
*It visualizes actual patient flow, activity transitions, waiting times, and patient movement between hospital departments.  
*The dashboard highlights key insights such as average ER time, X-ray loop-backs, and adherence to the ideal patient pathway.  
*Interactive filters allow users to explore data by diagnosis category, priority level, and arrival mode.  

## Dashboard Development Process
*Organized KPI cards to highlight the most important metrics.

*Arranged slicers to provide interactive filtering options.

*Positioned charts and visualizations in a meaningful sequence.

*Applied consistent formatting, colors, and alignment.

## Project Report
- Generated a simulated Emergency Room (ER) event log containing 300 patient visits and 2,635 events using Python.
- Completed data validation and cleaning, successfully passing all eight validation checks.
- Performed process discovery, identifying 27 distinct process moves and 29 patient journey variants.
- Conducted bottleneck analysis and identified the X-ray Result → Triage transition as the slowest movement, with a 90-minute average gap.
- Completed conformance checking, revealing that 86.3% of visits followed the ideal pathway, while 13.7% deviated.
- Identified that 39.8% of X-ray patients experienced a loop-back to Triage.
- Integrated the cleaned dataset into MySQL and verified the analysis using SQL queries.
- Developed an interactive Power BI dashboard featuring KPI Overview, Process Map, and Conformance Analysis pages.
- Implemented KPI cards for Total Visits, Average Time in ER, Loop-back %, and Ideal Path %, along with Diagnosis Category and Priority Level slicers.
- Successfully completed the project by integrating Python, MySQL, and Power BI to identify patient flow inefficiencies and present recommendations for improving ER workflow efficiency.


*Created a well-structured dashboard to support easy data exploration and analysis.

*It helps identify process bottlenecks, delays, and inefficiencies to support better hospital workflow management.  

**Tools Used:** Power BI, DAX, and CSV Dataset.
