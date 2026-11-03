---
unique_name: hrsa_medically_underserved_areas
name: HRSA Medically Underserved Areas/Populations
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: medical & healthcare
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.hrsa.gov/topics/health-workforce/shortage-areas
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/medically-underserved-areas-populations
- https://arxiv.org/abs/2605.12292
- https://data.hrsa.gov/DataDownload/DD_Files/MUA_DET.csv
- https://data.hrsa.gov/DataDownload/DD_Files/MUA_DATAMART_METADATA.XLSX
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-01):** `TBD -> 2nd Tier`, priority 2: HRSA's register of Medically Underserved Areas and Populations, where STRABLE predicts the Index of Medical Underservice. HRSA sums four weighted values from published statistics to get it, its own file ships them and STRABLE dropped them, so the target is a formula and no decision predicts it (the `hrsa_health_professional_shortage_areas` precedent).
- Source: HRSA Bureau of Health Workforce, MUA/P download (https://data.hrsa.gov/DataDownload/DD_Files/MUA_DET.csv; dictionary https://data.hrsa.gov/DataDownload/DD_Files/MUA_DATAMART_METADATA.XLSX, refreshed daily): "The IMU involves four variables - ratio of primary medical care physicians per 1,000 population, infant mortality rate, percentage of the population with incomes below the poverty level, and percentage of the population age 65 or over. The value of each of these variables for the service area is converted to a weighted value, according to established criteria. The four values are summed to obtain the IMU score for the area."; "In order to qualify for designation, the IMU score must be less than or equal to 62.0, except for a Governor designation, which does not receive an IMU score." The dictionary lists the four values and their IMU scores as columns. As used by STRABLE (HF parquet, previewed): 3,882 rows x 51 columns (designation type, status, designation and update dates from 1977, withdrawal date, county, tract, state and region codes repeated under several names, rural and border flags, population), target `IMU Score` 0 to 91.9 (median 56.6), the components gone.
- Use case: none in the source; HRSA computes the score from the statistics above when a state primary care office applies, and predicting it from geography alone would stand in for looking those statistics up. Fit none to approximate; regime IID (one snapshot of designations), with several components per designation and per county to check as groups.
- Measured on the preview: 3,529 of the 3,540 designations that are not governor's exceptions score 62 or less (the designation rule); 275 rows score 0, 141 of them governor's exceptions.
- Siblings and duplicates: `hrsa_health_professional_shortage_areas` (`TBD -> 2nd Tier`, priority 2; this table was its fourth link until 2026-11-01): another HRSA file and score (PROV-7); `hrsa_clinician_dashboard` (`TBD -> Yes`, priority 2). No duplicate (grep for underserved, MUA). External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C, "Medically Underserved Areas": "Areas with populations lacking access to primary care. The task is to predict the underservice index.").
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the HRSA dictionary; 42 CFR Part 51c (the designation criteria, not read); STRABLE.
- Metric: none found (HRSA publishes a register, no task; STRABLE's R² is benchmark-wide, MET-5), so the fallback `rmse`; inputs none.
- Risks for /add-dataset: a formula target whose inputs ship in HRSA's file (SEL-5: with them `Trivial`, TP-4; without them the task guesses four area statistics); governor's exceptions carry no IMU (0 or above 62) and the rest are selected at 62 or less by the rule; status and withdrawal date are recorded after designation (LEAK-10); STRABLE's cut repeats geography columns.
- Priority: gap 0 (regression; medical & healthcare not thin), use case 0 (none), source + (HRSA dictionary), shape + (3,882 designations; categorical, dates and counts), risk - (a computed target).

**Assessment (AI, 2026-11-01):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292) as "Medically Underserved Areas"; split out on 2026-11-01 from `hrsa_health_professional_shortage_areas`, which held this table as a second link.
- as published: 3,882 rows x 51 columns incl. target (STRABLE parquet); target: IMU Score.
- Why: Predict the Index of Medical Underservice (IMU) score of a designated area
- Notes: Raw file MUA_DET.xlsx (HRSA). IMU is a formula of four component scores; check whether they are among the 51 columns.
