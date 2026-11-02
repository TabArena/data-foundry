---
unique_name: ny_sparcs_inpatient_length_of_stay
name: Hospital Inpatient Discharges (SPARCS De-Identified), New York State, annual files
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Regression
original_data_state: One Table
source_links:
- https://health.data.ny.gov/d/sf4k-39ay
- https://health.data.ny.gov/d/5dtw-tffi
- https://health.data.ny.gov/d/46xm-urtu
- https://www.health.ny.gov/statistics/sparcs/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: New York State's all-payer inpatient discharge file, about 2.1-2.2 million discharges a year for 2009-2024 with 33 documented columns and length of stay as the target; real records where the length-of-stay and hospital-record siblings are synthetic or untraceable, but several columns are coded at discharge.
- Source: New York State Department of Health, Statewide Planning and Research Cooperative System (SPARCS), "Hospital Inpatient Discharges (SPARCS De-Identified)" on health.data.ny.gov, one dataset per discharge year 2009-2024 (2024: sf4k-39ay, 2,196,737 rows, created 2025-10-08; 2023: 46xm-urtu, 2,125,754; 2022: 5dtw-tffi, 2,103,433; Socrata counts read 2026-10-31). Columns: health service area, county, operating certificate, facility id and name, age group (0-17, 18-29, 30-49, 50-69, 70 or older), 3-digit zip, gender, race, ethnicity, length of stay, type of admission, disposition, discharge year, CCSR diagnosis and procedure, APR DRG and MDC, severity of illness, risk of mortality, medical or surgical, three payment typologies, birth weight, ED indicator, total charges, total costs. "Individual secondary diagnoses and procedures, as well as revenue codes have been excluded"; dates keep only the year; abortion records lose the facility.
- Use case: none named by SPARCS (planning and transparency). The scout's actor (bed planners estimating length of stay at admission) comes from Microsoft's sample behind `length_of_stay`, not from this source, so it does not count (USE-1); fit approximate. Regime temporal by discharge year, with facility groups inside (SPLIT-13).
- Siblings and duplicates: `length_of_stay` (Microsoft, synthetic; `TBD -> 2nd Tier`, AHDS), `healthcare_dataset` (`No`, generated with Faker), `hospital_patient_records_dataset` (`TBD -> 2nd Tier`, unclear source), `medicare_inpatient_cost` (CMS hospital x DRG averages; `TBD -> 2nd Tier`), `av_healthcare_analytics_length_of_stay` (Analytics Vidhya, 318k admissions, undocumented hospitals; not screened yet). None shares the source. External collections: none found.
- Better data: found as better data for `length_of_stay`, `healthcare_dataset`, `hospital_patient_records_dataset` and `medicare_inpatient_cost`; no further search this round.
- Papers and pages: the Open Data NY pages with their column descriptions and notes; https://www.health.ny.gov/statistics/sparcs/. Papers that predict length of stay on SPARCS were not searched: the session's web search budget ran out.
- Metric: none found (the portal and the SPARCS page define no task), so the fallback `rmse` on days (MET-1, MET-8); the target is skewed and capped at "120 +", so the shipped scale (log1p) is a decision for the add stage (MET-3).
- Risks for /add-dataset: for an at-admission task drop what is coded at or after discharge: APR DRG, MDC, severity, risk of mortality, CCSR procedure, disposition, total charges and costs (LEAK-10, USE-3), and decide whether the principal diagnosis (CCSR, coded at discharge) may stand in for the admitting diagnosis; "120 +" is text in a numeric target; newborn records (with birth weight) are another population; about 2.1 million rows a year are over the 500k cap (one year, a region or a sample); facility is a group inside the temporal split.
- Priority: gap 0 (medical & healthcare and regression are not thin), use case 0 (written by the curation), source + (a state agency with column descriptions), shape + (millions of rows a year, mixed columns, 16 years, facility groups), risk - (several columns coded after the prediction point).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `healthcare_dataset`, `hospital_patient_records_dataset`, `length_of_stay`, `medicare_inpatient_cost`.
- as published: 2,196,737 discharges in 2024 (Socrata count), about 2 million per year, 33 columns: facility, county, age group, sex, race, ethnicity, admission type, ED indicator, CCSR diagnosis and procedure, APR ...; target: Length of Stay in days (capped at '120 +'); for medicare_inpatient_cost, Total Costs per discharge; access: open, open (Open Data NY).
- Why: real all-payer discharge records with the same target as length_of_stay, whose Microsoft data is synthetic; for medicare_inpatient_cost, the cost per discharge with patient features instead of a hospital x DRG average with no task | The Kaggle record is 1,000 patients of unknown origin (likely generated), with ...
- Adds: real data instead of simulated (length_of_stay's AHDS marker), millions of rows over 16 years (temporal split), facility groups; risks: APR DRG, severity, risk of mortality, procedures, disposition and charges are coded at or after discharge (leaks for an at-admission task), age in groups, Total Costs = charges x ...
