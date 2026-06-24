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
source_row: 663
type_adapter_id: curation-record-v1
---

# Santander_transaction_value

## Comments

CC: "From Kaggle competition. Original task was rather time-series & some weird feature engineering was applied in the competition. It is very likely that there are leaks. Might rather use the preprocessed version of Tschalzev et al. Not included in TabRepo. Various issues in the dataset, but with the right preprocessing might be usable"

Follow preprocessing of Tschalzev et al. and check if splits are usable as IID

## Reference

https://www.kaggle.com/competitions/santander-value-prediction-challenge
