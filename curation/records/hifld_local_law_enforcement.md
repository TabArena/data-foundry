---
unique_name: hifld_local_law_enforcement
name: Local Law Enforcement
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- No Good Target (yet)
- Outdated
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: social science
problem_type: Regression
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::local-law-enforcement-locations/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/local-law-enforcements
- https://arxiv.org/abs/2605.12292
- '# origin of the staffing counts: BJS Census of State and Local Law Enforcement Agencies (2008 wave; a 2018 wave exists)'
- https://bjs.ojp.gov/data-collection/census-state-and-local-law-enforcement-agencies-csllea
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: ORNL's fusion of the 2008 BJS census of local police and sheriff agencies with sworn officers as STRABLE's target; no decision named, and BJS has since run a 2018 wave.
- Source: the HIFLD Open layer "Local Law Enforcement Locations" (ORNL with the NGA HSIP team): "The primary sources for this effort are the DOJ-BJS CSLLEA from 2008 and the previously mentioned 2009 feature class from Homeland Security Infrastructure Foundation-Level Data (HIFLD)" (copy in FEMA's "Local Law Enforcement Locations RAPT", ArcGIS item 333a74c8e9c64cb6870689d31e8836af, downloaded 2025-07-22); the staffing counts come from the 2008 Census of State and Local Law Enforcement Agencies (CSLLEA08ID column); the start link no longer resolves to a dataset (the ArcGIS Hub API returns none for its slug and the HIFLD organisation's feature services no longer list the layer, 2026-10-31; a PEMA backup item says "This data is being discontinued by HIFLD", ArcGIS item 18fb153120624222a96b4d7aade54e0e, 2025-08-25). As published in STRABLE: 16,159 agencies x 32 columns; target number_of_officers = log(FTSWORN + PTSWORN), built by STRABLE; POPULATION dropped as leakage (preprocess_HIFLD-local-law-enforcements.py). STRABLE Appendix C.2: "Locations of local police and sheriff departments in the US. The task is to predict officer counts."
- Use case: the nearest real use is a statistician filling the sworn count of an agency that did not answer the census, from its type, civilian staff and place; no source names it for this table; fit approximate; regime IID (one row per agency, one census year). Precedent: registry tables with a target picked by a benchmark went to `TBD -> 2nd Tier` with `No Good Target (yet)` (museums, journal_score_sjr, ai_jobs_net_salaries; Lennart).
- Siblings and duplicates: none (searched for CSLLEA, sworn officers, police departments: only incident and crash tables). External collections: STRABLE. Also the other HIFLD tables of STRABLE in this run: hifld_prison_boundaries, hifld_public_schools, hifld_transmission_lines, hifld_transmission_towers, fcc_antenna_structure_registration and the NCEI copies ncei_significant_earthquakes, ncei_significant_volcanic_eruptions.
- Better data: a candidate of the benchmark STRABLE (the run's find); no search for better data. Seen while checking the source: BJS ran the CSLLEA again in 2018 (its statistical tables appeared in October 2022, https://bjs.ojp.gov/data-collection/census-state-and-local-law-enforcement-agencies-csllea), a newer wave of the census behind these counts (PROV-6, a version for the curator).
- Papers and pages: BJS CSLLEA 2008; STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19; a benchmark of tables with strings, Lennart a co-author); preprocessing per table in github.com/soda-inria/strable, scripts/script_preprocess_data/preprocess_HIFLD-local-law-enforcements.py; no paper using the layer for prediction looked for (the run's web-search budget was used up).
- Metric: none from the first publisher (HIFLD and its sources define no task); STRABLE scores every table with "R² for regression; AUROC for classification" (Appendix D.1), a benchmark-wide default rather than a choice for this task (MET-5), so the fallback rmse on officers, with target_transform log; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: FTCIV and PTCIV (civilian staff) come from the same census answer as the sworn counts (fine for filling a census, USE-3 for any other framing); CSLLEA08ID, CI_ID and ID are identifiers; SUBTYPE1 and SUBTYPE2 are empty for 14,783 rows; the counts are from 2008 (`Outdated`); the HIFLD file is offline, so a rebuild goes to the CSLLEA files (PROV-13).
- Priority: gap + (social science is thin, 1 accepted), use case -, source + (a BJS census through ORNL), shape + (16,159 agencies, 31 mixed columns), risk - (2008 counts while a 2018 wave exists).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 16,159 rows x 32 columns incl. target (STRABLE parquet); target: number_of_officers.
- Why: Predict the number of officers of a local police or sheriff department
- Notes: HIFLD layer.
