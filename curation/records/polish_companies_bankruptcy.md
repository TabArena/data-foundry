---
unique_name: polish_companies_bankruptcy
name: Polish Companies Bankruptcy
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2016'
required_split:
- '?'
source_links:
- https://doi.org/10.24432/C5F600
notebook_path: datasets/beyond_iid/old_iid/polish_companies_bankruptcy/polish_companies_bankruptcy.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Data from companies from 2000-2012, predict for them from 2007 to 2013, likely temporal but could be made time invariant (as one has a dataset per year). features were already engineered - mostly through arithmetic interactions.

Potential issue: Temporal

Lennart: Could be used without temporal connection

Andrej: task can be conceptualized s.t. the features are time-invariant. Only need to think about whether it is feasible to combine the year datasets or to choose one. If the latter I would use the year with the most observations. Also might reverse the feature engineering.

## Reference

Ensemble boosted trees with synthetic features generation in application to bankruptcy prediction
By Maciej Ziȩba, S. Tomczak, Jakub M. Tomczak. 2016

Published in Expert systems with applications
