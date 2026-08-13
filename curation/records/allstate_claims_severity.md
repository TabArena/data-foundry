---
unique_name: allstate_claims_severity
name: Allstate_Claims_Severity
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2016'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/allstate-claims-severity
- https://www.openml.org/search?type=data&id=42571
notebook_path: datasets/beyond_iid/new_iid/allstate_claims_severity/allstate_claims_severity.ipynb
source_row: 645
type_adapter_id: curation-record-v1
---

## Comments

CC: "Predict amount of insurance claims. Data anonymized. Unclear whether date is given or temporal split is required. Kaggle challenge; data does not allow us to remove/avoid temporal split or detect it from meta-data"

## Reference

https://www.kaggle.com/competitions/allstate-claims-severity
