---
unique_name: miami_housing
name: miami_housing
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: OpenML
year: '2016'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=44983
- https://www.openml.org/search?type=data&id=43093&sort=runs&status=active
type_adapter_id: curation-record-v1
---

# miami_housing

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

housing datasets with a lot of spatial information but all within one yea

Potential issue: spatial and semi temporal

Lennart: We can likely ignore temporal and spatial influences for this housing predictive task with the given data / features

Andrej: We need to write down the reason why we consider some housing datasets as random split data and others as temporal

## Reference

https://doi.org/10.1177/0042098020982508
