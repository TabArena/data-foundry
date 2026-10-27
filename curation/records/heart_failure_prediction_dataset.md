---
unique_name: heart_failure_prediction_dataset
name: Heart Failure Prediction Dataset
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- New IID
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction
source_row: 35
type_adapter_id: curation-record-v1
---

## Comments

Super set of several heart prediction datasets, unsure if we should use this or take the original datasets (to avoid shift) or use this as grouped data?

We include/use the original versions where appropriate and not the superset that introduced leakage and other concerns.

**Assessment (AI, 2026-10-27):** a duplicate of `heart_disease`, which since PR #20 holds the Cleveland, Budapest and Long Beach files of the Detrano study in one dataset (the single-hospital datasets are retired into it).
