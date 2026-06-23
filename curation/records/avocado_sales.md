---
unique_name: avocado_sales
name: avocado_sales
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Forecasting)
- No Good Target  / Scientific Discovery
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
year: '2018'
source_links:
- https://www.kaggle.com/datasets/neuromusic/avocado-prices
- https://www.openml.org/search?type=data&id=41210
- https://hassavocadoboard.com
source_row: 51
type_adapter_id: curation-record-v1
---

# avocado_sales

## Comments

CC: "They use a version with date dropped and month & day kept - but requires temporal split anyway"

More of a forecasting task. Otherwise a bit meaningless. We want to forecast avocado prices potentially for all these regions, or transfer learn across them. But original data is clearly not for that purpose either

Data also seems to have a bunch of issues (see Kaggle discussions)

## Reference

Kaggle
