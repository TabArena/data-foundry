---
unique_name: mutual_funds_india
name: Mutual Funds India - Detailed
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2023'
domain: finance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ravibarnawal/mutual-funds-india-detailed
notebook_path: datasets/beyond_iid/new_iid/mutual_funds_india/mutual_funds_india.ipynb
source_row: 777
type_adapter_id: curation-record-v1
---

## Comments

Returns prediction, sounds reasonable, need to pick one target and go for it

Have to remove columns that leak target, we use 3 years return as target

## Reference

Kaggle
