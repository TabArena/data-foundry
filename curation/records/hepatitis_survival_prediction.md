---
unique_name: hepatitis_survival_prediction
name: hepatitis
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/hepatitis/metadata.yaml
- https://doi.org/10.24432/C5Q59J
- https://www.kaggle.com/datasets/abdelazizsami/hepatitis
notebook_path: datasets/beyond_iid/new_iid/hepatitis_survival_prediction/hepatitis_survival_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hepatitis_survival_prediction/dataset.py
source_row: 760
type_adapter_id: curation-record-v1
---

## Comments

Already preprocessed data but otherwise looks like a good task, need to check group and cost files but would add!

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Efron & Gong 1981/1986 study how to estimate the error rate of Gregory's logistic rule on these 155 patients: a statistics-methods paper, not a decision; 32 deaths, so accuracy is coarse. Original rejected: error rate. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): the metric is the roc_auc fallback; Efron & Gong's error rate is the object of a resampling study on 155 patients, not the task's metric.

## Reference

?
