---
unique_name: aps_failure
name: APSFailure
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2016'
required_split:
- '?'
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=41138
- https://doi.org/10.24432/C5V60Q
type_adapter_id: curation-record-v1
---

# APSFailure

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Comes with a cost matrix. Originally comes with custom train/test split. Last 16k are test. Strongly imbalanced task. Might originally be time-series. Error very close to zero on TabRepo - might indicate a leak; data from daily usage indicates temporal relationship as well and potentailly future failures per seasons; data contains histograms; missing values must be nan-ed

Update: Error is close to zero because it is trivial to classify the negative cases due to the high class imbalance. However meaningful learning is possible. One paper about challenge: https://link.springer.com/chapter/10.1007/978-3-319-46349-0_33. D

Potential issue: maybe temporal, heavily preprocssed

Lennart: verify split

Andrej: need to verify that original provided split was also random

## Reference

10.24432/C5V60Q
