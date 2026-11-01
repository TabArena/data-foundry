---
unique_name: thrive_by_five_index_2024
name: Thrive by Five Index 2024 (TB5I 2024)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Website
year: '2026'
domain: education
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.25828/k91x-gm18
- https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/1129
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the 2024 round of South Africa's Thrive by Five Index (DataDrive2030, nationally representative, 5,001 children in 1,388 early learning programmes), the same instrument, target and kind of survey as the shipped `early_learning_predictors` (2016-2023 merged); a newer release of its source (PROV-6), most useful as a newer survey round for that record.
- Source: DataDrive2030 with the Department of Basic Education, "Thrive by Five Index 2024", DataFirst (UCT) catalogue 1129, DOI 10.25828/k91x-gm18, version 1 of 2026-03-05, CC BY, microdata through DataFirst. The catalogue: "The 2024 Index is the second in a series of cross-sectional nationally and provincially representative surveys", a three-stage stratified sample (wards, programmes, children), fieldwork 28 October to 21 November 2024, plus a non-representative sub-study of children not enrolled. As published (DDI metadata): eight files, the child file `tb5i-2024-elom-sef-pub-v1` (5,001 x 89, with `n_elom_total_score`, the five domain scores and `n_elom_total_cuts`), facility (1,388 x 37), principal (1,388 x 394), practitioner (1,223 x 268), caregiver (3,841 x 106), programme quality (1,388 x 80), and two household files of the sub-study (272 rows each).
- Use case: as `early_learning_predictors`: find children at risk of not thriving from facility, staff and family surveys without a full assessment; the release itself assesses the developmental status of 4-year-olds and names no prediction; fit approximate. Regime grouped by programme (the parent's split by facility).
- Siblings and duplicates: `early_learning_predictors` (`Yes`, shipped; ELOM and Thrive by Five Index 2016-2023 merged, 18,874 children, DataFirst 962, a Zindi challenge) is the record it was found for and the same source series; the 2024 round is not in its merged release. As its own dataset it repeats the parent's task (PROV-6); as an extension it gives the parent a newer round. The curator decides which. External collections: none.
- Better data: found as better data for `early_learning_predictors`.
- Papers and pages: the DataFirst catalogue and its DDI metadata; the parent's Zindi challenge (DataDrive2030 Early Learning Predictors).
- Metric: none defined by the 2024 release; the parent declares the Zindi challenge's `rmse` on the total ELOM score (MET-4), which carries over if this round extends it.
- Risks for /add-dataset: joins of the child, facility, principal, practitioner and caregiver files by programme and child ids; the domain scores and the cut-off band are parts of the target (drop, as the parent does); question sets differ from the earlier rounds, so merging leaves blocks missing by round; survey weights, and the non-enrolled sub-study to keep out or flag; the Stata missing codes the parent decoded (CC 2026-10-30).
- Priority: gap + (education is thin), use case 0 (the parent's use case comes from its Zindi challenge, not from this release), source + (DataDrive2030 and DataFirst with DDI documentation), shape + (5,001 children in 1,388 programmes, mixed survey features, grouped), risk - (a version of a shipped dataset, multi-file joins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `early_learning_predictors`.
- as published: ELOM child file tb5i-2024-elom-sef-pub-v1: 5,001 children x 89 variables, with the total ELOM score; facility, principal, practitioner and caregiver files to join; a small household-based file of ...; target: total ELOM 4&5 score (n_elom_total_score, the sum of five domain scores), the same quantity as the record's child_total_elom; access: registration.
- Why: the same instrument, target and kind of features as the record, from the same producer: a later national survey round of the Thrive by Five series
- Adds: a newer year (2024) not in the merged 2016-2023 release the record ships (18,874 children), so either a newer test period or a stand-alone 2024 dataset; the curator decides whether it extends the record or replaces nothing
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
