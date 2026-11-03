---
unique_name: oasis1_dementia_mri
name: OASIS Alzheimer's
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Selection Bias
tags:
- Tiny Data
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Other
year: '2007'
domain: medical & healthcare
source_links:
- https://doi.org/10.1162/jocn.2007.19.9.1498
- https://www.kaggle.com/datasets/shreyanmohanty/oasis-alzheimers-detection-multi-class-dataset
- https://arxiv.org/abs/2605.10616
- https://sites.wustl.edu/oasisbrains/home/oasis-1/
- https://huggingface.co/datasets/multabench/extended-img-cls-oasis-alzheimers
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: OASIS-1 (Marcus et al. 2007), 416 adults aged 18 to 96 with demographics and MRI volume measures; without the MRI slice it is the cross-sectional sibling of the accepted `dementia_prediction` (OASIS-2, partly the same people) and of the newer candidate `oasis3_dementia_status`, so the curator picks one OASIS release (PROV-6).
- Source: Open Access Series of Imaging Studies, Washington University (https://sites.wustl.edu/oasisbrains/home/oasis-1/): "a cross-sectional collection of 416 subjects aged 18 to 96", of whom 100 over 60 were "clinically diagnosed with very mild to moderate Alzheimer's disease (AD)", plus a reliability set of 20 nondemented subjects re-imaged within 90 days (434 sessions); a demographic and clinical spreadsheet next to the images; paper Marcus et al., J. Cogn. Neurosci. 19:1498-1507 (2007, doi:10.1162/jocn.2007.19.9.1498). MulTaBench (extended, https://huggingface.co/datasets/multabench/extended-img-cls-oasis-alzheimers) takes 436 rows from a Kaggle image re-upload (shreyanmohanty, skull-stripped and augmented slices, CC BY-NC-SA) with sex, age, education, SES, eTIV, ASF, delay and one slice, target `is_demented`; CDR and MMSE dropped "because they restate the diagnosis" (Appendix F.1); nWBV is not among its columns.
- Use case: none stated by the release (a data-sharing project). A candidate: a memory clinic flags dementia from an MRI's volume measures and demographics; fit approximate, since the cohort is volunteers recruited as young, middle-aged, nondemented and demented older adults (cases and controls collected apart) and the label is the clinical dementia rating. Regime IID on subjects; grouped by subject if the 20 re-scans stay.
- Siblings and duplicates: `dementia_prediction` (OASIS-2 longitudinal, 150 subjects aged 60-96, 373 sessions; `Yes (Disagreement)`, shipped in BeyondArena, markers `Wrong Domain / Source Modality`, `Time-series (Classification)`, `Selection Bias`); the OASIS-2 paper says "Many of the subjects were part of the cross-sectional OASIS data set (Marcus et al., 2007) but have been assigned new random identifiers", so the two releases overlap in people and share the features. `oasis3_dementia_status` (OASIS-3, 1,378 participants; this run's better data for `dementia_prediction`). Versions or cuts of one project without a distinct task are duplicates (PROV-6); OASIS-1 adds the cross-sectional view and the young adults. External collections: MulTaBench (extended image release).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds. OASIS-3 already has a record.
- Papers and pages: Marcus et al. 2007 (the release); the OASIS-1 page; MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Appendix F.1 and Table 8 (structured AUC 0.910, image 0.893, joint 0.931), Table 9 (436 rows; 7 structured, 1 image).
- Metric: none found (the release describes the data and group analyses; MulTaBench's AUC is benchmark-wide, MET-5), so the fallback `log_loss` (with `roc_auc`) for a binary target; inputs none.
- Risks for /add-dataset: CDR and MMSE are the diagnosis and its test (LEAK-10, drop); the clinical ratings are, as far as known, missing for the younger subjects, so labelling them nondemented is an assumption that age then decides (USE-5; check the spreadsheet); eTIV and ASF are one quantity (eTIV is derived from the atlas scaling factor), and nWBV, the atrophy measure, should come back from the source spreadsheet; the 20 re-scans repeat subjects (group by subject); about 100 demented subjects in all (TP-5 per fold); the MRI slice is dropped (SEL-12).
- Priority: gap 0 (medical & healthcare holds 44 accepted datasets, binary is not thin), use case 0 (written by the curation), source + (a paper and the institution's page), shape 0 (416 subjects, about eight features), risk - (a version of an accepted OASIS release, an assumed label for the young).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 436 rows; 7 structured, 0 text, 1 image features (MulTaBench Table 9); target: Demented (binary).
- Why: Predict dementia from a brain MRI slice and demographics
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. OASIS-1 cross-sectional (Marcus et al. 2007). Related but different release: ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: two releases of the OASIS project behind the accepted `dementia_prediction`; pick one release (`oasis3_dementia_status`; PROV-6). The curator keeps one, or both as distinct tasks.
