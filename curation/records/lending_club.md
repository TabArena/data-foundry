---
unique_name: lending_club
name: lending_club
checked_by:
- Lennart
- Alex
- Mustafa
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- Free Text (Sentences)
- Non-IID (Temporal)
collections:
- TexTabBench Extra
original_source: Company
year: '2020'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/imsparsh/lending-club-loan-dataset-2007-2011
- https://www.kaggle.com/datasets/wordsforthewise/lending-club
- https://zenodo.org/records/11295916
- https://www.kaggle.com/datasets/adarshsng/lending-club-loan-data-csv
- https://www.lendingclub.com/
source_row: 641
type_adapter_id: curation-record-v1
---

# lending_club

## Comments

Predict whether loan is paid back, needs to be shuffled, TextTabBench drops ['id', 'member_id', 'issue_d', 'url', 'last_pymnt_d', 'last_credit_pull_d'], we will have to make sure that there is no leakage

Text has prefix for date and HTML artifacts
Data might have spatial components
