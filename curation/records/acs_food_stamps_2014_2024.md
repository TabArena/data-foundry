---
unique_name: acs_food_stamps_2014_2024
name: 'American Community Survey Public Use Microdata Sample, 1-year files 2019-2024 (FS: household food stamp / SNAP receipt in the past 12 months)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.census.gov/programs-surveys/acs/microdata.html
- https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/
- https://tableshift.org/datasets.html#food-stamps
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the newer ACS PUMS years of the TableShift Food Stamps task (`food_stamps`, TBD -> Yes): the same survey, variable and features, with six more survey years that allow the temporal split the curator's note on `food_stamps` asks about; a version under PROV-6.
- Source: US Census Bureau, American Community Survey Public Use Microdata Sample, 1-year files (annual; the 2024 files are on the Census server, directory dated 2025-12-04: csv_hus.zip 240 MB and csv_pus.zip 575 MB for the nation, and a pair per state). As published: a housing-unit file and a person file per year, joined by SERIALNO; FS is a housing item, "Yearly food stamp/Supplemental Nutrition Assistance Program (SNAP) recipiency" (1 yes, 2 no, 0 vacant; ACS API variable page). TableShift's task keeps "Low-income adults aged 18 to 62 who live in a household with at least one child" with income under $30,000, 840,582 rows (tableshift.org); its code reads ACS 2014-2018 (from the scout, not re-read). The record's name spans 2014-2024; the years 2019-2024 are the new part.
- Use case: TableShift names "Low-cost, low-friction screening tools powered by machine learning models" that identify likely candidates for food-security programmes (a state SNAP agency or outreach programme); fit approximate (survey respondents, not an agency's intake records); regime temporal (a programme fits on past survey years and screens the next), instead of TableShift's held-out East South Central division, which the curator found not representative.
- Siblings and duplicates: `food_stamps` (TableShift, ACS 2014-2018; TBD -> Yes with `Not Representative`, Lennart) has the same source and target: this record is a newer version of it (PROV-6), and the curator decides which one enters. Other ACS records: `folktables_acs_income` and `acs_household_broadband` (candidates of this run, other targets of the same survey, PROV-7); `adult` and `census_income` (CPS extracts, `No` with `No Good Target / Scientific Discovery`). External collections: TableShift carries the 2014-2018 version.
- Better data: found as better data for `food_stamps`; no further search this round.
- Papers and pages: Gardner, Popovic, Schmidt, "Benchmarking Distribution Shift in Tabular Data with TableShift", NeurIPS 2023 Datasets and Benchmarks (tableshift.org); Ding et al. 2021, folktables, the ACS loaders TableShift builds on; the ACS PUMS documentation.
- Metric: none found as one deliberate choice for this task (TableShift's page names none for Food Stamps; its paper compares models across tasks, not re-read here), so the fallback `roc_auc` (MET-1, MET-11); inputs none (the person and household weights ship but are no scoring input unless the curator asks for weighted scores).
- Risks for /add-dataset: SEL-7 needs the curator's call: the household reports its own SNAP receipt in the same interview as the features, while the screening use predicts it for households that were not asked; `food_stamps` is kept at TBD -> Yes by the curator, and this record should follow that call. Income items that include benefits or public assistance may encode the target (LEAK-10: check every income component); several adults of one household share the label, so group by SERIALNO (LEAK-17); the 2020 file has experimental weights (pandemic collection); the population filter and the person-housing join follow TableShift's code.
- Priority: gap + (social science: 1 accepted), use case 0 (approximate fit, SEL-7 open), source +, shape + (hundreds of thousands of rows a year, mixed types, survey years for a temporal split), risk - (a PROV-6 version of `food_stamps`; SEL-7 open).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `food_stamps`.
- as published: national 1-year person and housing files per year, about 3 million person records each (approx., not checked per year); TableShift's task keeps low-income adults 18-62 in households with children ...; target: FS (household received food stamps/SNAP in the past 12 months), the same variable TableShift uses; access: open.
- Why: Same source, same variable and same features (ACS person and household items); a newer release of the same source, so a version under PROV-6, not a new source.
- Adds: Six newer years: the record's data stop in 2018. It allows the temporal split the curator's note asks about ('given that it is temporal') instead of the held-out East South Central division, and covers the pandemic-era SNAP changes. The curator decides which version enters.
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
