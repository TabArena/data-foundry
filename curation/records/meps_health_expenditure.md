---
unique_name: meps_health_expenditure
name: 'Medical Expenditure Panel Survey (MEPS) Household Component, Full Year Consolidated Data Files (latest: HC-251, 2023)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Regression
original_data_state: One Table
source_links:
- https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-251
- https://meps.ahrq.gov/data_stats/download_data/pufs/h251/h251doc.shtml
- https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a person's annual health-care spending (`TOTEXPyy`) in AHRQ's Medical Expenditure Panel Survey, the real quantity behind the retired simulated insurance tables; one file per data year (2023: 18,919 persons x 1,374 variables), with the features to choose from a survey and many same-year utilisation columns that add up to the target.
- Source: Agency for Healthcare Research and Quality, MEPS Household Component, Full Year Consolidated Data Files; the latest, HC-251 (data year 2023, released August 2025): "18,919 persons who participated in the MEPS HC in 2023", 18,463 with a positive person weight, 1,374 variables, from rounds 3-5 of Panel 27 and rounds 1-3 of Panel 28 (HC-251 documentation). Expenditures are collected "at the event level (e.g., doctor visit, hospital stay) and summed" (section 2.5.11). Person id `DUPERSID` (panel, dwelling unit, person); each panel is interviewed over two years, so a person sits in two consecutive annual files. Earlier annual files not counted here.
- Use case: a health insurer or a care-management programme estimates a person's spending for the coming year from demographics, coverage and health status, to price coverage or pick people for case management; fit approximate: AHRQ publishes the file for "national estimates of health care use, expenditures, sources of payment, and health insurance coverage", not for a prediction, and the survey's answers stand in for what an insurer knows (USE-8). Regime temporal by data year, with persons grouped across the two years of a panel (SPLIT-13; decide at /add-dataset).
- Siblings and duplicates: `meps_total_health_expenditure` (this run, the same HC-251 file and target: proposed `No` with `Duplicate`, PROV-4, this record kept); `insurance_premium_data_medical_cost_personal_datasets` (`No`, AHDS) and `healthcare_insurance_expenses` (`No (Retired)`, AHDS: the Lantz `insurance.csv`, simulated with a recovered formula), the task this replaces with real data; `hrsa_uds_hypertension_control` only mentions MEPS. External collections: AIF360 (`MEPSDataset19`, `MEPSDataset20`, `MEPSDataset21`: the 2015 and 2016 files with a utilisation label, at least 10 visits, a different target).
- Better data: found as better data for `insurance_premium_data_medical_cost_personal_datasets` and, through `meps_total_health_expenditure`, for `healthcare_insurance_expenses`; no further search this round.
- Papers and pages: the HC-251 documentation (read in part) and the AHRQ download pages; no paper or competition sets this prediction.
- Metric: none found (AHRQ documentation; no competition or paper on this target), so the fallback `rmse` on dollars, the target probably shipped as log1p (MET-1, MET-3, MET-8); the person weight is a survey weight, a metric input only if the curator wants population-weighted scores (MET-2).
- Risks for /add-dataset: the utilisation counts and source-of-payment amounts of the same year count or sum to the target (LEAK-10: keep what is known at the start of the year, or take the features from the panel's first year); adult BMI and other self-administered items come in alternating years (2023 lists ADBMI42 as "Deleted (included in alternating years only, will be included in 2024)"; ADSMOK42 is in), so the features differ by year; variable names carry the year (`TOTEXP23`, `AGE23X`) and the ID length changed between the 1996-2017 and 2018-2023 files, so pooling years needs a harmonisation; many zero spenders and a heavy tail; the data use agreement allows use "except for statistical reporting and analysis" only and forbids re-identification (a note, EV-4).
- Priority: gap 0 (medical and regression are not thin; insurance would be thin, 3 accepted, if filed there), use case 0 (the source names no decision), source + (a federal survey with full codebooks), shape + (thousands of persons a year over many years, mixed types, a panel), risk - (same-year utilisation leaks, features to harmonise across years).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `insurance_premium_data_medical_cost_personal_datasets`.
- as published: 2023 file: 18,919 persons ('18,463 were assigned a positive person-level weight'), 1,374 variables, from two overlapping panels (Panel 27 rounds 3-5, Panel 28 rounds 1-3; 'The panel design of the ...; target: total annual health care expenditure of a person (TOTEXPyy, all payers; name per the codebook), the real quantity behind the simulated 'charges'; access: open.
- Why: the same target and use case as the record (annual medical cost of an individual from age, sex, BMI, children/family size, smoking and region), measured on a federal survey with expenditures verified against providers; AGE23X, SEX, REGION23, FAMSZE23, INSCOV23 and ADSMOK42 are documented in the 2023 file
- Adds: real data in place of a simulated table with a recovered generator (healthcare_insurance_expenses, the same rows, was retired for it); about 14 times the persons per year, many years (temporal split by data year), panel IDs for grouping. Caveats: the adult BMI and smoking items are asked in alternating years (ADBMI42 ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: carry the out-of-pocket framing of the rejected duplicate `meps_total_health_expenditure` here.
