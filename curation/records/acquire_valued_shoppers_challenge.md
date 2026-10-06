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
notebook_path: datasets/beyond_iid/temporal/acquire_valued_shoppers_challenge/acquire_valued_shoppers_challenge.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/acquire_valued_shoppers_challenge/dataset.py
source_row: 709
type_adapter_id: curation-record-v1
---

## Comments

Follow TabRed preprocessing and how tables were merged. Investigate test.csv time range to see if it is relevant. Check if customers are unique or recurring across time and if we would need to filter customers.

TabRed uses 4 days as time horizon

CC (2026-10-06, Lennart): Kept as a real task after the task-probe review (flag `no_spread`). The signal is real but weak, and methods are hard to tell apart: the three untuned families reach skill +0.24 to +0.28 (ROC AUC about 0.62-0.64, standard deviation 0.06-0.08 over the 5 five-day windows of 2,758-30,305 test rows); on BeyondArena the best method (TabPFN-3.5-Fast) reaches AUC 0.654 and beats chance in every window, the median 0.646, and 12 of 21 methods are tied with the best. A low ceiling on a real repeat-buyer task, as in TabRed, is no reason to act.

## Reference

DMDave, Todd B, and Will Cukierski. Acquire Valued Shoppers Challenge. https://kaggle.com/competitions/acquire-valued-shoppers-challenge, 2014. Kaggle.
