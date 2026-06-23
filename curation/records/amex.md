---
unique_name: amex
name: amex
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2022'
domain: finance
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/amex-default-prediction/data?select=train_data.csv
source_row: 690
type_adapter_id: curation-record-v1
---

# amex

## Comments

CC: ""Target is binary classification from a survival prediction task (thus some noise); mostly anonymized data, some categorical data; dataset made imbalanced by default and scoring is affected by this; 

Temporal split needed, see train/test shift; likely also grouped-based splits (same customers in the data);

Manye weird features, likely lagged-data from temporal original data; unsure how to treat re-ocuring users""

Can be used as IID and non-iid. Several final versions of kaggle made the task iid. Moreover, you could use the non-iid version as well

TODO: decide if add groupby features or not -> add not and leave it to the pipeline but make sure good baselines create the features

## Reference

Kaggle
