use Careflow;
select count(*) as events, count(distinct Case_ID)as cases from Careflow;
SELECT COUNT(*) AS xray_patients,
       SUM(triage_runs > 1) AS sent_back,
       ROUND(100 * SUM(triage_runs > 1) / COUNT(*), 1) AS loopback_pct
FROM (SELECT Case_ID,
             SUM(Activity_Name = 'Triage Started') AS triage_runs,
             SUM(Activity_Name = 'Radiology Ordered') AS xray
      FROM Careflow
      GROUP BY Case_ID) t
WHERE xray > 0;
