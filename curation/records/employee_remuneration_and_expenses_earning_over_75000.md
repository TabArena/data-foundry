---
unique_name: employee_remuneration_and_expenses_earning_over_75000
name: Employee remuneration and expenses earning over 75000
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Ethical Issue
- No Good Target (yet)
tags:
- Free Text (Short)
collections:
- CARTE/TARTE
- MulTaBench
source_links:
- https://opendata.vancouver.ca/explore/dataset/employee-remuneration-and-expenses-earning-over-75000/information/?disjunctive.department&disjunctive.title&sort=year
source_row: 482
type_adapter_id: curation-record-v1
---

## Comments

Predicts remunerations of employees (earnings)

Contains PII, temporal and grouped data (repeated entries per year, across years). No target or features for a target at all

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nyc_citywide_payroll` (TBD -> 2nd Tier, priority 2). Each is screened in its own record; this record's verdict stays the curator's.
