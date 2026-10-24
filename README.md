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
