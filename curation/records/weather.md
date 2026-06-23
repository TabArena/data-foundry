---
unique_name: weather
name: Weather
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2024'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/pcovkrd84mejm/tabred-weather
- https://github.com/yandex-research/tabred/tree/main/preprocessing#weather
source_row: 715
type_adapter_id: curation-record-v1
---

# Weather

## Comments

Was downsampled/filtered by TabRed via preprocessing

Maybe not a super relevant task for tabular models.... need to make a judgment call. Given it was used in TabRed, I would say we can go for it now but might need to remove it later

TabRed uses 1 month refit horizon. For weather this is a bit much. I would argue for one or two weeks at most?

## Reference

TabRed
