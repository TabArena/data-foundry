---
unique_name: dementia_prediction
name: Dementia Prediction Dataset
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: Yes (Disagreement)
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
- Selection Bias
tags:
- Tiny Data
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
collections:
- New (BeyondArena)
original_source: Other
year: '2010'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/shashwatwork/dementia-prediction-dataset/data
- https://data.mendeley.com/datasets/tsy6rbc5d4/1
notebook_path: datasets/beyond_iid/grouped/dementia_prediction/dementia_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/dementia_prediction/dataset.py
source_row: 4
type_adapter_id: curation-record-v1
---

## Comments

need to figure out how to use the data, source seems likely image data?

the version of this dataset is created from the study and taken from another one

Grouped data

AT: No objection, but we need to quickly talk about how we proceed with medical image data

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — the OASIS-2 paper reports group analyses, no prediction metric.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `SES`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `oasis3_dementia_status` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 scores are numbers (SES).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target is an ordered category, no_dementia < very_mild_AD < mild_AD.

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the 150 people have 1 to 5 visits (91 two, 13 four or five), and the use case is a first visit, while every follow-up visit is scored as if it were one. On the 60 shipped splits with 8 untuned models: weighting each visit by 1 over the person's visits ranks the models at Kendall tau 0.94 per split (lowest 0.71) and 1.0 for the ranking by the mean, the same best model on 56 of 60; scoring only each test person's first visit (OASIS-2's visit 1, 48 to 52 per fold against 112 to 138 visits) at 0.87 (lowest 0.57) and 0.93, the same best on 49 of 60. Open for Lennart as issue 1 of the folder's REVIEW.md; recommended: each person counts once (B), or the first visits only (C); log loss would first need an optional weight input. Script: `one_vote_scan/apply_2026-11-08/dementia_first_visit.py` in the exposure review's run folder.

CC (2026-11-08, Lennart): issue 1, B: each person counts once. The log loss weights a visit by 1 over the person's number of visits (`person_weight`, a scoring column for the metric only); follow-up visits stay scored as if each were a first visit, at one vote per person. The weight is for scoring only, never a `sample_weight`, also though it does not follow from the inputs (Lennart's rule of 2026-11-08, MET-15 amended, MET-17); the bundle warning accepted with that reason.

**Assessment (AI, 2026-11-08):** training with the weight changes a logistic regression's weighted log loss by -0.004 (SE 0.003, lower on 35 of 60 grouped random splits), within noise. New checksum v2:85704fee... (not built); `dataset check` 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the declared metric (log_loss, weighted by person_weight) is checked.

## Reference

Rel source paper: Open Access Series of Imaging Studies: Longitudinal MRI Data in Nondemented and Demented Older Adults  https://direct.mit.edu/jocn/article/22/12/2677/4983/Open-Access-Series-of-Imaging-Studies-Longitudinal
