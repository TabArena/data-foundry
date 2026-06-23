---
unique_name: ecom_offers_grouped_version
name: Ecom Offers (Grouped-Version)
checked_by:
- Lennart
suggestion: TBD -> Yes
tags:
- Non-IID (Temporal)
- Non-IID (Grouped)
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
source_row: 634
type_adapter_id: curation-record-v1
---

# Ecom Offers (Grouped-Version)

## Comments

This could be the version without preprocessing and collapsing the groups as done for amex!


Follow TabRed preprocessing and how tables were merged. Investigate test.csv time range to see if it is relevant. Check if customers are unique or recurring across time and if we would need to filter customers.

TabRed uses 4 days as time horizon

## Reference

DMDave, Todd B, and Will Cukierski. Acquire Valued Shoppers Challenge. https://kaggle.com/competitions/acquire-valued-shoppers-challenge, 2014. Kaggle.
