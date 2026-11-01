---
unique_name: hifld_colleges_and_universities
name: Colleges and Universities
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
domain: education
problem_type: Regression
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::colleges-and-universities/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/colleges-and-universities
- https://arxiv.org/abs/2605.12292
- '# origin of the layer: IPEDS (NCES, US Department of Education), yearly'
- https://nces.ed.gov/ipeds/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: an IPEDS-based inventory of US postsecondary institutions with a target STRABLE built (enrollment per employee); no source names a decision, as for other registry tables.
- Source: the HIFLD Open layer "Colleges and Universities" (DHS GMO; compiled by ORNL with the NGA HSIP team), "composed of all Post Secondary Education facilities as defined by the Integrated Post Secondary Education System (IPEDS ...) for the 2019-2020 school year" (the layer description as copied in FEMA's "Colleges and Universities RAPT", ArcGIS item 8835ff30eaf24f299c66498958dbc018, "Downloaded from HiFLD Open on July 22, 2025"); the start link no longer resolves to a dataset (the ArcGIS Hub API returns none for its slug and the HIFLD organisation's feature services no longer list the layer, 2026-10-31; a PEMA backup item says "This data is being discontinued by HIFLD", ArcGIS item 18fb153120624222a96b4d7aade54e0e, 2025-08-25). As published in STRABLE (parquet footer read 2026-10-31): 6,128 institutions x 41 columns; target RATIO_ENROLL_EMP = log(TOT_ENROLL / TOT_EMP), built by STRABLE, which drops TOT_ENROLL, TOT_EMP, FT_ENROLL and PT_ENROLL (preprocess_HIFLD-Colleges-and-Universities.py). STRABLE's Appendix C.2 (item 16) says instead "The task is to predict student enrollment."
- Use case: none named by HIFLD, IPEDS or STRABLE; IPEDS collects enrollment and staff for every Title IV institution, so nobody estimates the ratio. The nearest is an analyst estimating staffing intensity where a staff count is missing; fit approximate at best; regime IID (one row per institution, one snapshot). Precedent: registry tables with a target picked by a benchmark went to `TBD -> 2nd Tier` with `No Good Target (yet)` (museums, journal_score_sjr, ai_jobs_net_salaries; Lennart).
- Siblings and duplicates: college_scorecard (`Yes`; Department of Education files on the same IPEDS institutions, a completion-rate target: a distinct task, PROV-7); colleges (`No`, Duplicate of college_scorecard); hifld_public_schools (NCES-based, also a ratio target STRABLE built). External collections: STRABLE. Also the other HIFLD tables of STRABLE in this run: hifld_prison_boundaries, hifld_public_schools, hifld_transmission_lines, hifld_transmission_towers, fcc_antenna_structure_registration and the NCEI copies ncei_significant_earthquakes, ncei_significant_volcanic_eruptions.
- Better data: a candidate of the benchmark STRABLE (the run's find); no search for better data. IPEDS (https://nces.ed.gov/ipeds/) is the yearly origin of the layer, with enrollment and staff by category.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19; a benchmark of tables with strings, Lennart a co-author); preprocessing per table in github.com/soda-inria/strable, scripts/script_preprocess_data/preprocess_HIFLD-Colleges-and-Universities.py; no paper using the layer for prediction looked for (the run's web-search budget was used up).
- Metric: none from the first publisher (HIFLD and its sources define no task); STRABLE scores every table with "R² for regression; AUROC for classification" (Appendix D.1), a benchmark-wide default rather than a choice for this task (MET-5), so the fallback rmse on the ratio, with target_transform log; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: the target is STRABLE's construction and its own paper names another (USE-5: which quantity, if any, an actor acts on); POPULATION, INST_SIZE (an enrollment band) and SIZE_SET relate to the numerator (Spearman with the log ratio 0.24, 0.21 and DORM_CAP 0.04 on the preview, so no shortcut); -999 and "NOT AVAILABLE" placeholders; x/y repeat the coordinates in another projection; the HIFLD file is offline, so a rebuild goes to IPEDS (PROV-13).
- Priority: gap + (education is thin, 3 accepted), use case -, source + (IPEDS through ORNL, documented), shape + (6,128 institutions, 40 mixed columns), risk - (a target the benchmark built, not the one its paper names).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 6,128 rows x 41 columns incl. target (STRABLE parquet); target: RATIO_ENROLL_EMP.
- Why: Predict a postsecondary institution's ratio of enrollment to employees
- Notes: HIFLD layer (built from IPEDS). Paper says 'student enrollment'; config target is the derived ratio RATIO_ENROLL_EMP.
