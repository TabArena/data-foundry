---
unique_name: thai_apparel_line_productivity
name: 'Dataset for: Factory Benefits to Paying Workers More: The Critical Role of Compensation Systems in Apparel Manufacturing (line-day productivity of a ...'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2020'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.6078/D17T2G
- https://doi.org/10.1371/journal.pone.0227510
- https://zenodo.org/records/4625011
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: about 4,200 line-days of 8 sewing lines of a Thai apparel factory (2015-2017) with the day's labour-time efficiency, from a published quasi-experiment; several columns are computed from the day's output.
- Source: Lollo and O'Rourke, "Factory benefits to paying workers more: The critical role of compensation systems in apparel manufacturing", PLOS ONE 15(2):e0227510, 2020; data Dryad doi 10.6078/D17T2G (Zenodo copy 4625011, 2021, CC0), one CSV `Lollo_ORourke_2019.csv` of 40 columns: line, phase, date, treatment_name, wage, output, productivity, quality_rate, absenteeism (total, unplanned, planned), tot_wk_hr, line_workers, style1, sam_style1, base, overtime and incentive wages, tardiness minutes, working and overtime hours, downtime minutes by cause, treatment dummies, lead_time (header read). Paper: "six treatment lines, plus two control lines out of 23 total lines", January 2015 to January 2017, "over 4000 observations", one per line-day; productivity is "a measure of labor-time efficiency" (Eq 1, not read: an image). It estimates difference-in-differences with style, date and line fixed effects; no prediction.
- Use case: the factory's industrial engineers, before a day, set a line's target and staffing from the style, its standard minutes, the workers and the planned hours; not named by the source (a causal study); fit approximate; regime temporal (two years of one factory with a compensation change mid-way; 8 lines are too few groups).
- Siblings and duplicates: `garments_worker_productivity` (Yes, UCI 2021, 1,197 team-days of a Bangladeshi factory over three months): another factory, no duplicate. External collections: none found.
- Better data: found as better data for `garments_worker_productivity`; no further search this round.
- Papers and pages: the PLOS ONE paper (read for the design, the variables and the data statement); the Dryad and Zenodo records.
- Metric: none found (the paper reports regression coefficients and no prediction metric); fallback `rmse` (MET-8); inputs none.
- Risks for /add-dataset: `output`, `wage`, `OldIncentive`, `OldTHP`, `quality_rate` and the downtime minutes are known only after the day, and wages follow output (LEAK-1, LEAK-10: drop); the treatment phase shifts productivity, so test windows hold mostly treated days (note it, SPLIT-4); each line is a daily series, so TP-10 against a line's recent level; only 8 lines.
- Priority: gap 0 (industry & manufacturing, regression, temporal not thin), use case 0 (none named by the source), source + (paper and data deposit), shape + (about 4,200 rows, mixed, temporal), risk - (output-derived columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `garments_worker_productivity`.
- as published: Sewing line x working day: 8 of the factory's 23 sewing lines (6 treatment, 2 control), 2015-01-01 to 2017-01-15; 'over 4,000 line-day observations with complete data' plus about 200 with missing ...; target: productivity, the line's labour-time efficiency for the day (output x standard allowed minutes against worker minutes, Eq. 1 of the paper); output count also ...; access: open.
- Why: The same unit (a sewing line's day), the same target (daily line productivity as efficiency against a standard) and features of the same kind (workers, hours and overtime, style and its standard minutes, absenteeism, idle/downtime, incentive), from a real factory's management records.
- Adds: About 3.5 times the rows (about 4,200 line-days against 1,197), two full years instead of three months (seasonality, 170 styles), and a documented source with a paper. Risks for screening, as in the old record: wage and incentive are computed from the day's output (same leak as UCI's incentive), downtime and ...
