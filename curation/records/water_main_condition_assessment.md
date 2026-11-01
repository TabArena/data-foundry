---
unique_name: water_main_condition_assessment
name: 'Data for "Learning Limitations: Machine learning, value of information, and water distribution asset management" (anonymized pipe condition ...'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2026'
domain: industry & manufacturing
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.21875973
- https://zenodo.org/records/21875973
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: about 100,000 water main segments of eight Canadian and New Zealand utilities with diameter, material, installation year and length, and a green/amber/red condition rating; real, open and multiclass, but the rating may be the councils' desktop grade rather than an inspection result.
- Source: Thomas (PNNL), Iguchi (AFIT) and Chini, "Data for 'Learning Limitations: Machine learning, value of information, and water distribution asset management'", Zenodo v1.0, 2026-08-10, doi 10.5281/zenodo.21875973, CC BY 4.0. The page: "An anonymized dataset of water distribution pipes used for a condition assessment study", one row per pipe segment with the condition rating recorded at inspection; sources: eight open-data layers of municipal and district councils and Wellington Water (the first "City of Courtenay (2024). 'OpenData WaterMains'"), accessed December 2024; regions relabelled U_A to U_H, pipe ids replaced, "coordinates, criticality, internal condition scores, and unit bookkeeping columns" removed; only "diameter > 50 mm"; plastic pipes recorded as installed on or before 1960 excluded; rating "Green/amber/red mapping to good/fair/poor condition". File `condition_assessment_data_anonymized.csv` (5.1 MB): `region`, `pipe_ID`, `diameter`, `material_type`, `installation_date` (a year), `inspection_date` (a year), `age`, `condition_rating`, `length`. Preview (six byte ranges, 4,261 rows of U_A, U_C, U_G, U_H): every `inspection_date` is 2024; the class mix varies by utility (U_A 61/22/17% green/amber/red, U_H 58/41/1%); about 100,000 rows by file size, not counted.
- Use case: the title names water distribution asset management and the value of information; a utility's asset manager choosing which mains to inspect or renew from inventory attributes is our reading (the paper was not found), fit approximate until the rating's origin is known. Regime IID within utilities, or grouped by `region` (a model carried to a new utility); to decide from the paper.
- Siblings and duplicates: `predictive_maintenance_oil_and_gas_pipeline_data` (Lennart, `No`, AHDS: "This is synthetic data generated to reflect"): another, generated source; no other water-main record (`grep -il "water main\|pipe failure\|watermain"`). External collections: none.
- Better data: found as better data for `predictive_maintenance_oil_and_gas_pipeline_data`; no further search this round.
- Papers and pages: the Zenodo page (read); the paper "Learning Limitations" not found (probably not yet published); the councils' layers not opened.
- Metric: none found (the Zenodo page; no paper), so the fallback `log_loss` over the three ordered classes (MET-8). Inputs: none.
- Risks for /add-dataset: the rating may be a desktop grade from age and material (an `inspection_date` of 2024 in every previewed row looks like the access year, not an inspection): if a council's rule derives it, the task is `Trivial` for that utility (SEL-5, TP-4), so read each layer's field definition first; `age` is `inspection_date - installation_date`, a redundant copy (CLEAN); rating scales may differ by utility (USE-5); the relabelled regions and ids are no `Anonymized` case (only ids replaced).
- Priority: gap + (multiclass is thin), use case 0 (our reading of the title), source + (a documented Zenodo record naming its eight sources), shape + (about 100,000 segments, eight utilities, numeric and categorical), risk - (the rating's origin, possibly rule-derived).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `predictive_maintenance_oil_and_gas_pipeline_data`.
- as published: one CSV (5.1 MB), one row per inspected water main segment from 8 anonymized utilities (U_A..U_H); columns region, pipe_ID, diameter (mm), material_type, installation year, inspection year, age, ...; target: condition rating of the pipe segment at inspection (good/fair/poor); access: open.
- Why: The generated record's task is the maintenance need of a pipeline segment from its size, material, age and wall condition; this is the same task on real pipes, with the inventory features (diameter, material, age, length) known before the inspection and the inspected condition as the target. Water mains, not oil and ...
- Adds: Real, traceable rows (city GIS layers) under CC BY 4.0 instead of 1,000 synthetic ones; several utilities in two countries (a group or utility split is possible). Risks: only inspected pipes carry a rating (pipes picked for inspection: Selection Bias), rating scales may differ by utility, and no measured wall loss or ...
