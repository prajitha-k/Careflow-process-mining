## Week 3: Drill-down by diagnosis, priority and arrival

**Goal:** let the Power BI report filter the process map and bottlenecks by patient group, so one slicer shows where a specific group waits longest.

**Problem:** `edges.csv` has no diagnosis, priority or arrival column, so the first report page cannot be filtered by patient group.

**Solution:**
1. `edges.py` builds `edges_by_group.csv`, the same transitions split by diagnosis, priority, arrival mode and doctor (check: 41 loop-back patients, 90.0 min average wait)
2. `cases.csv` gives one row per case with its diagnosis, priority, arrival mode, start time and total minutes
3. In Power BI, three small filter tables (`Diagnosis`, `Priority`, `Arrival`, each made with `DISTINCT`) link to both `cases` and `edges_by_group`
4. Relationships are one-to-many with single-direction filtering, so one slicer filters every visual on the page

**Report:** page 1 (transition matrix and bottleneck chart) still reads `edges`. Page 2 reads `cases` and `edges_by_group`, with three slicers, a case-count card, and a bottleneck bar chart that changes with the slicers.

**Next:** add a doctor slicer, then rebuild page 1 from `edges_by_group` so the file has one consistent model.
