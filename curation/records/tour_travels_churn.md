---
unique_name: tour_travels_churn
name: Tour & Travels Customer Churn Prediction
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Missing source information
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: Kaggle
year: '2021'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/tejashvi14/tour-travels-customer-churn-prediction/data
notebook_path: datasets/beyond_iid/new_iid/tour_travels_churn/tour_travels_churn.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/tour_travels_churn/dataset.py
source_row: 778
type_adapter_id: curation-record-v1
---

## Comments

We can add it for now. We are missing some information, but it seems reasonable. It might be trivial after we test it for the first time.

CC (2026-10-21, Lennart): option (a) of the consistency check on one-snapshot churn sets: tagged `ForcedIIDFromTemporal`; SPLIT-8 now covers a release with one stock month or one undated snapshot.

**Assessment (AI, 2026-10-21):** tag and one note line added; a dated window would test the model on a later season's customers; not measurable on one undated snapshot.

CC (2026-10-21, Lennart): an upload whose first platform cannot be traced is kept for now, case by case, when the data looks sound and there is a source to point to ("if the data looks good enough even without a good source but there is a source, we want to keep it for now and risk it"); PROV-1/PROV-2 amended, the gap written as an approximate fit with a note.

**Assessment (AI, 2026-10-21):** note added to `dataset.py` curation_comments; the generated-data probe raises no flag (no rule leaves, 71% of 21 column pairs dependent, no uniform column).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — bare Kaggle upload with no competition, paper or stated metric.

## Reference

Kaggle
