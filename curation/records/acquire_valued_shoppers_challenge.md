---
unique_name: acquire_valued_shoppers_challenge
name: Ecom Offers
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
- TabRed
original_source: Kaggle
year: '2014'
domain: business & marketing
required_split:
- Temporal (NON-IID)
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/c/acquire-valued-shoppers-challenge
- https://github.com/yandex-research/tabred/tree/main/preprocessing#ecom-offers-acquire-valued-shoppers-by-dmdave
source_row: 709
type_adapter_id: curation-record-v1
---

# Ecom Offers

## Comments

Follow TabRed preprocessing and how tables were merged. Investigate test.csv time range to see if it is relevant. Check if customers are unique or recurring across time and if we would need to filter customers.

TabRed uses 4 days as time horizon

## Reference

DMDave, Todd B, and Will Cukierski. Acquire Valued Shoppers Challenge. https://kaggle.com/competitions/acquire-valued-shoppers-challenge, 2014. Kaggle.
