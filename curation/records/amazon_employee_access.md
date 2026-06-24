---
unique_name: amazon_employee_access
name: Amazon_employee_access
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: Kaggle
year: '2013'
required_split:
- '?'
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=4135
- https://www.kaggle.com/c/amazon-employee-access-challenge
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

I LOVE this dataset - we need to include it. BUT: Need to carefully check how the split in the Kaggle challenge was. Also could require time split - but it seems as if the task was conceptualized with time-invariant features

Potential issue: grouped data (manager-employees); test data was temporal (only on new employees!); problem in words: if the train samples in the kaggle data would have the same employee multiple times for multiple resources, then it breaks non-grouped/non-temporal assumptions

Lennart: Yes, if the groups are not a problem and we do not have repeated employee entries? Time should be ignorable as the processes did not change during collection (?);

Andrej: Fits criteria

## Reference

https://www.kaggle.com/c/amazon-employee-access-challenge
