---
unique_name: qsar_biodeg
name: qsar-biodeg
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2013'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1494
- https://doi.org/10.24432/C5H60M
notebook_path: datasets/beyond_iid/old_iid/qsar_biodeg/qsar_biodeg.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Nice chemistry dataset with (computed) molecular propeties to predict whether the sample is ready and not ready biodegradable. Linear model among best in TabRepo

Potential issue: -

Lennart: no objection

Andrej: Matches criteria

## Reference

Mansouri, K., Ringsted, T., Ballabio, D., Todeschini, R., Consonni, V. (2013). Quantitative Structure - Activity Relationship models for ready biodegradability of chemicals. Journal of Chemical Information and Modeling, 53, 867-878
