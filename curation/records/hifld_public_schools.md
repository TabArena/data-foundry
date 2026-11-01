---
unique_name: hifld_public_schools
name: Schools
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
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::public-schools/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/schools
- https://arxiv.org/abs/2605.12292
- https://nces.ed.gov/ccd/
- https://nces.ed.gov/surveys/pss/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: NCES school directory records repackaged by HIFLD, with STRABLE's target the enrollment per full-time teacher, a ratio of two columns it dropped; no decision predicts a school's ratio from its name, address and grades, since schools report both counts to NCES.
- Source: the first publisher is NCES: the Common Core of Data for public schools (https://nces.ed.gov/ccd/) and the Private School Universe Survey (https://nces.ed.gov/surveys/pss/); HIFLD Open's school layers repackaged them (the `Source` column links each row to an NCES school-search page) and went offline in August-September 2025 (archived in DataLumos). As used by STRABLE (HF parquet, previewed): 75,000 rows x 27 columns, subsampled; target `Enrollment_FT_Teachers_Ratio` on a log scale (median about 15 students per teacher, outliers near 2,000); 18.7% of the rows are private schools (PSS ids and PSS URLs), although the paper links the public-schools layer.
- Use case: none in the source; NCES publishes the counts it collects. Fit none; regime IID (one school-year snapshot), possibly grouped by district (`District ID`, missing for 19%, the private schools).
- Siblings and duplicates: no duplicate (grep for schools, NCES, CCD, the layer link); `hifld_colleges_and_universities` (IPEDS, ratio of enrollment to employees, the same construction) and the other `hifld_*` records of STRABLE; student-level education records of other sources (`els2002_bachelors_attainment`, `hsls09_*`) have other units. External collections: STRABLE (Table C.4 row 94: "Locations and metadata for public K-12 schools. The task is to predict student counts.", while its `config.json` sets the ratio).
- Better data: a candidate of the benchmark STRABLE; no further search for this run's finds.
- Papers and pages: STRABLE, Blayer et al., arXiv 2605.12292 (v2, 2026-10-19), Sec. 3; the NCES CCD and PSS pages.
- Metric: none found (NCES and HIFLD define no task; STRABLE's R², App. D.1, is benchmark-wide, MET-5), so the fallback `rmse` on the ratio; inputs none.
- Risks for /add-dataset: no task (`No Good Target (yet)`, SEL-3); the target is enrollment over teacher FTE, both dropped, and restoring either makes it near-deterministic (SEL-5); public and private schools mixed, with `Type` codes 1-7 and numeric and text `Level` values side by side; a build should read NCES directly (PROV-8, PROV-13).
- Priority: gap + (education is thin, 3 accepted), use case 0, source + (NCES documents CCD and PSS), shape + (75,000 schools, mixed columns), risk - (no task, constructed target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 75,000 rows x 27 columns incl. target (STRABLE parquet); capped at 75,000 by STRABLE; target: Enrollment_FT_Teachers_Ratio.
- Why: Predict a public school's ratio of enrollment to full-time teachers
- Notes: HIFLD layer (NCES-based). Paper says 'student counts'; config target is a derived ratio. Subsampled by STRABLE to 75,000 rows.
