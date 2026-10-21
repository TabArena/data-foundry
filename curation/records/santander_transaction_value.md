---
unique_name: santander_transaction_value
name: Santander_transaction_value
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- New IID
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2018'
domain: finance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/santander-value-prediction-challenge
notebook_path: datasets/beyond_iid/new_iid/santander_transaction_value/santander_transaction_value.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/santander_transaction_value/dataset.py
source_row: 663
type_adapter_id: curation-record-v1
---

## Comments

CC: "From Kaggle competition. Original task was rather time-series & some weird feature engineering was applied in the competition. It is very likely that there are leaks. Might rather use the preprocessed version of Tschalzev et al. Not included in TabRepo. Various issues in the dataset, but with the right preprocessing might be usable"

Follow preprocessing of Tschalzev et al. and check if splits are usable as IID

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — Root Mean Squared Logarithmic Error (RMSLE) (https://www.kaggle.com/competitions/santander-value-prediction-challenge/overview/evaluation).

**Assessment (AI, 2026-10-21):** metric now `Metric.source("rmsle", target_transform="log1p")` instead of rmse on the log1p target: the competition's RMSLE on the raw transaction value, computed after the inverse of the shipped log1p (MET-3); the score is the same number as before. Needs a rebuild to reach the container.

## Reference

https://www.kaggle.com/competitions/santander-value-prediction-challenge
