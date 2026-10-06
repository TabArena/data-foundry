---
unique_name: mercedes_benz_greener_manufacturing
name: Mercedes_Benz_Greener_Manufacturing
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2017'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing
- https://www.openml.org/search?type=data&id=42570
notebook_path: datasets/beyond_iid/temporal/mercedes_benz_greener_manufacturing/mercedes_benz_greener_manufacturing.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/mercedes_benz_greener_manufacturing/dataset.py
source_row: 708
type_adapter_id: curation-record-v1
---

## Comments

CC: "Using the index as a feature was predictive in the competition, might require a temporal split. But in general an interesting dataset, likely has groups of cars as multiple configurations could include the same car? Need to assess the impact of index as feature"

CC (2026-10-06, Lennart): Kept as a fine task after the task-probe review (flag `no_spread`: untuned skills +0.55 to +0.57; `X314` alone +0.39). Tuned methods spread: on BeyondArena TabPFN-2.6 reaches R^2 0.614, the median method 0.600 and the weakest about 0.47, with 10 of 29 methods tied with the best over the 9 windows of 320 test rows.

## Reference

https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing
