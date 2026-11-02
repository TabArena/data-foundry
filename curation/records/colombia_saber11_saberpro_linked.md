---
unique_name: colombia_saber11_saberpro_linked
name: A Linked Dataset for Analyzing Educational Trajectories from Secondary School to Higher Education in Colombia (SABER 11 to SABER PRO)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2026'
domain: education
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.17632/jg6kkv8mg6.1
- https://data.mendeley.com/datasets/jg6kkv8mg6/1
- https://doi.org/10.1016/j.dib.2020.105537
- https://revistas.javeriana.edu.co/index.php/MAGIS/article/download/41195/32027/164102
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 332,990 Colombian students linked from the SABER 11 exam at the end of secondary school (2014-2021) to the SABER PRO exit exam of their degree (2016-2023), 32 variables, a large education regression with cohorts and institutions; the use case is ours, and only students who reach the exit exam have a label.
- Source: De La Hoz, Garcia, Polanco, "A Linked Dataset for Analyzing Educational Trajectories from Secondary School to Higher Education in Colombia", Mendeley Data V1, 2026-07-30 (doi 10.17632/jg6kkv8mg6.1, CC BY 4.0), derived from the ICFES open microdata (the origin of the rows, PROV-8, PROV-11) and linked deterministically per student on the SABER 11 registration reference that SABER PRO records carry. As published: 332,990 students x 32 variables (332,993 before three rows with column shifts were removed); 361 institutions, 4,249 SNIES programmes; five SABER 11 subject scores (0-100) and the global score (0-500); five SABER PRO generic modules (0-300); demographics and school of origin; direct identifiers removed, birth dates replaced by top-coded ages; a bilingual codebook and the R script `prepare_release_v2.R`; median gap of 6 years between the exams.
- Use case: a university, at admission, predicts a student's exit-exam score from SABER 11 and background and targets academic support; this is the scout's framing and ours (the release names research on value added, institutional effectiveness, equity and educational data mining). Delahoz-Dominguez, Zuluaga-Ortiz, García-Yerena, MAGIS 18 (2025), predicted SABER PRO quantitative reasoning from the SABER 11 scores with a random forest on 12,411 engineering students (likely the 2020 set below; Crossref abstract). Fit approximate. Regime temporal by cohort (SABER PRO year) or grouped by institution, to decide (SPLIT-3).
- Siblings and duplicates: no record of ICFES data (searched SABER, ICFES, Colombia); "Dataset of academic performance evolution for engineering students" (Delahoz-Dominguez, Zuluaga, Fontalvo-Herrera, Data in Brief 30:105537, 2020; 12,411 students), linked in this record, is an earlier and smaller cut of the same ICFES source with no record of its own (PROV-6 if both are weighed). External collections: none found; the release cites two recommender-system papers that used it (Applied Sciences 2024, 14, 8311; Electronics 2025, 14, 4121), not read.
- Better data: from the gap scout for education; no further search this round.
- Papers and pages: the Mendeley Data page; the MAGIS paper and the Data in Brief article (Crossref metadata; the MAGIS PDF text was not extracted).
- Metric: the MAGIS paper reports RMSE (10.95) and R2 (69%) on another cut, two metrics with none named; nothing on this release, so the fallback `rmse` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: one target among five SABER PRO modules (quantitative reasoning as in the MAGIS paper); the other modules are outcomes of the same exam (drop, LEAK); only students who graduate and sit SABER PRO have a label, as in every dataset of this task (no marker), so the population is narrower than all admitted students (USE-8); programme and institution are known at admission; check the linkage and the derived ages against the ICFES originals (PROV-13).
- Priority: gap + (education has three accepted datasets), use case 0 (ours), source + (a documented release with codebook, built from ICFES microdata), shape + (332,990 students, mixed types, cohorts and institutions), risk - (labels only for exam takers, the choice of target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for education.
- as published: 332,990 linked students x 32 variables; SABER 11 cohorts 2014-2021, SABER PRO cohorts 2016-2023; 361 institutions, 4,249 programs; demographics, high school of origin, five SABER 11 scores, program ...; target: SABER PRO generic module scores (0-300) at the end of the degree, for example quantitative reasoning; access: open.
- Why: census-coverage national exams, a measured outcome about 6 years after the features, a documented linkage, a recent open release
- Adds: a large regression task in education with a temporal (cohort) and grouped (institution, program) structure; the 2020 Data in Brief set of the same first author (12,411 engineering students) is an earlier, smaller cut and should be compared before a record is made
