---
unique_name: forest_fires
name: forest_fires
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2008'
domain: environmental science & climate
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5D88D
- https://www.kaggle.com/datasets/elikplim/forest-fires-data-set
- https://www.openml.org/search?type=data&id=44962
source_row: 748
type_adapter_id: curation-record-v1
---

# forest_fires

## Comments

CC: "Data from forest fires, used ln(x+1) target scaling; time invariant features,"

Has spatial data (x,y) and temporal (month/day). Need to see how to split the data for a real task. Spatial data represents a square on a map

Paper used default cross-validation, which makes not a lot of sense given the data/task but given their setup and goal it makes sense

"further research is needed to confirm if
direct weather conditions are preferable than accumulated values, as suggested by this
study"

## Reference

@article{cortez2007data,
  title={A data mining approach to predict forest fires using meteorological data},
  author={Cortez, Paulo and Morais, An{\'\i}bal de Jesus Raimundo},
  year={2007},
  publisher={Associa{\c{c}}{\~a}o Portuguesa para a Intelig{\^e}ncia Artificial (APPIA)}
}
