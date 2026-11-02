---
unique_name: hifld_hospitals
name: Hospitals
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
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
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::hospitals/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/hospitals
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: a compiled inventory of US hospitals (ORNL, from state and federal sources) with the bed count as STRABLE's target; bed counts matter to planners, but no source names a prediction.
- Source: the HIFLD Open layer "Hospitals" (ORNL and DHS GMO): "The dataset only includes hospital facilities based on data acquired from various state departments or federal sources which has been referenced in the SOURCE field ... The source data was available in a variety of formats (pdfs, tables, webpages, etc.) which was cleaned and geocoded" (copy in FEMA's "Hospitals RAPT", ArcGIS item c4b621eb03ca4f78a05d9063629e98bf, downloaded from HIFLD Open on 2025-07-22); the start link no longer resolves to a dataset (the ArcGIS Hub API returns none for its slug and the HIFLD organisation's feature services no longer list the layer, 2026-10-31; a PEMA backup item says "This data is being discontinued by HIFLD", ArcGIS item 18fb153120624222a96b4d7aade54e0e, 2025-08-25). As published in STRABLE: 7,883 hospitals with a bed count x 32 columns; target BEDS (log); POPULATION dropped as leakage (preprocess_HIFLD-Hospitals.py); TYPE 4,203 general acute care, 1,248 critical access, 1,005 psychiatric, 490 rehabilitation and smaller groups; 332 closed; SOURCEDATE 2012-2024, 6,965 of them 2024 (preview). STRABLE Appendix C.2 (item 57): "Comprehensive list of US hospitals and their facilities. The task is to predict the number of hospital beds."
- Use case: an emergency or health planner estimating the bed capacity of a hospital whose count is not reported (HIFLD codes it -999); not named by HIFLD or STRABLE, and CMS cost reports and state licences publish bed counts; fit approximate; regime IID (one row per hospital). Precedent: registry tables with a target picked by a benchmark went to `TBD -> 2nd Tier` with `No Good Target (yet)` (museums, journal_score_sjr, ai_jobs_net_salaries; Lennart).
- Siblings and duplicates: none among the records (searched for hospital bed counts, AHA and CMS files). External collections: STRABLE. Also the other HIFLD tables of STRABLE in this run: hifld_prison_boundaries, hifld_public_schools, hifld_transmission_lines, hifld_transmission_towers, fcc_antenna_structure_registration and the NCEI copies ncei_significant_earthquakes, ncei_significant_volcanic_eruptions.
- Better data: a candidate of the benchmark STRABLE (the run's find); no search for better data.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19; a benchmark of tables with strings, Lennart a co-author); preprocessing per table in github.com/soda-inria/strable, scripts/script_preprocess_data/preprocess_HIFLD-Hospitals.py; no paper using the layer for prediction looked for (the run's web-search budget was used up).
- Metric: none from the first publisher (HIFLD and its sources define no task); STRABLE scores every table with "R² for regression; AUROC for classification" (Appendix D.1), a benchmark-wide default rather than a choice for this task (MET-5), so the fallback rmse on beds, with target_transform log; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: critical-access hospitals are limited to 25 beds by definition (median 25 here, 12.6% above it on the preview), so TYPE sets part of the target; the counts come from many state sources that may mean licensed or staffed beds, at different dates (USE-5); ALT_NAME, STATE_ID, TELEPHONE and WEBSITE are identifiers; the HIFLD file is offline, so it needs a surviving copy, such as FEMA's of 2025-07-22 (PROV-13, PROV-15).
- Priority: gap -, use case -, source + (ORNL, a SOURCE per row), shape + (7,883 hospitals, 31 mixed columns), no known risk beyond the mixed bed definitions.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 7,883 rows x 32 columns incl. target (STRABLE parquet); target: BEDS.
- Why: Predict the number of beds of a US hospital
- Notes: HIFLD Hospitals layer.
