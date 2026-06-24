---
unique_name: wine_quality
name: wine_quality
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2009'
required_split:
- Random (IID)
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=287
- https://doi.org/10.24432/C56S3T
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Originally two datasets with red and white wine. They are diszinguishable by features such as sulfur dioxide. But still unsure whether it makes sense to use them together. Also there are many duplicates, might need to account for that.

Potential issue: Omitted variable bias? Grouped data

Lennart: use UCI version with indicator

Andrej: Add red/white wine indicator

## Reference

Modeling wine preferences by data mining from physicochemical properties
By P. Cortez, A. Cerdeira, Fernando Almeida, Telmo Matos, J. Reis. 2009

Published in Decision Support Systems
