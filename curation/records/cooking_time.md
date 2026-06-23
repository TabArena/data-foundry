---
unique_name: cooking_time
name: Cooking Time
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
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/pcovkrd84mejm/cooking-time
- https://github.com/yandex-research/tabred/tree/main/preprocessing#delivery-eta
source_row: 712
type_adapter_id: curation-record-v1
---

# Cooking Time

## Comments

Was downsampled/filtered by TabRed via preprocessing. Need to see what we want to resample

TabRed uses 1 week refit horizon. 36 days in train data

Tasks look reasonable even if missing all semantic information. Given that the data is from various restaurants and that it is unclear which restaurant this is from, there might be group-based leakage.

Note: numerical features are normalized with a noisy-quantile transform QuantileTransformer(X_num + 1e-5 * randn)

## Reference

TabRed
