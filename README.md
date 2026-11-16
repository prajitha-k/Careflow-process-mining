# Careflow-process-mining

## Power BI process map
CareFlow.pbix contains the Power BI report build from the event log.
Process_map_powerbi.png shows the patient flow through the ER, with the main transitions and where patients wait the longest.
## Weeks 1-2: Event log engineering and process discovery

**Goal:** show why ER waits are long by mapping what patients actually experience, instead of relying on the average wait time.

**Data (simulated):** a Python generator creates an EHR-style event log of 300 patient visits (about 2,600 events). Each visit has one `Case_ID` repeated on all its events, and about 40% of X-ray patients are deliberately sent back to Triage to create a hidden bottleneck. See `data_dictionary.md` for every column.

**Pipeline**
1. `data.py` - generates the event log
2. `Data Validation.py` - validates and cleans it (data types, ordering, 7 checks)
3. `Process Discovery.py` - builds `edges.csv` (step to next step, patients, average gap) and `variants.csv` (patient paths)
4. `Bottleneck Analysis.py` - ranks the slowest transitions, calculates loop-back %, writes `finding.md`
5. `Conformance Checking.py` - compares each visit with the ideal path, writes `cases.csv`
6. `Pipeline_audit.py` - writes `audit_report.md`, proving the data flows cleanly
7. Power BI process view (`CareFlow.pbix`) - matrix of patient moves and a bottleneck chart

**Key finding:** 40% of patients sent for an X-ray are sent back to Triage. Those visits last about 3.3 hours longer on average. The slowest move is Radiology Result Received to Triage Started (about 90 minutes).

**How to run:** `pip install pandas`, then run the scripts in the order above.

*Note: the data is simulated, so rates such as the loop-back share reflect the generator settings.*

## Weeks 3-4: Dashboard and documentation

**Goal:** turn the Weeks 1-2 results into an interactive Power BI dashboard that a hospital administrator can filter, and document the whole project.

**Input:** the files from Weeks 1-2: `Validation and cleaning.csv` (the clean event log), `edges.csv` (step-to-step moves), `cases.csv` (one row per visit, with the loop-back and ideal path flags) and `conformance_summary.csv`. See `Data_Dictionary.md` for every column.

### What was built

1. **Filterable data for the dashboard.** `edges_by_group.py` splits the step-to-step moves by diagnosis, priority, arrival mode and doctor (`edges_by_group.csv`), so the dashboard can be filtered by patient group.
2. **KPI cards.** Total Visits, Avg Time in ER (h), Loop-back % and Ideal Path %, written as DAX measures (see `dax_measures.md`).
3. **Dashboard visuals** in `CareFlow.pbix`:
   - the actual patient flow graph, with the loop-back from the X-ray result to Triage highlighted
   - an Ideal Path donut (on the path against deviating)
   - Loop-back % by diagnosis
   - a chart of where patients wait longest
   - a table of the five most common patient paths
4. **Slicers** for diagnosis, arrival mode and priority.
5. **Polish.** A single colour theme, aligned layout, helper tables hidden, and a PDF and screenshots exported.
6. **Documentation.** Project documentation, the project report and the presentation.

**Dashboard result:** the headline reads "40% of X-ray patients are sent back to Triage". The cards show 300 visits, 4.7 h average time in the ER, 39.8% loop-back and 86.3% on the ideal path. Trauma, Orthopedic and Infection deviate most.

**How to run:** run the Weeks 1-2 scripts in order, then open `CareFlow.pbix` in Power BI Desktop and choose Refresh to load the new CSV files.

*Note: the data is simulated. The patient flow graph in the dashboard is a static picture and does not change with the slicers.*
