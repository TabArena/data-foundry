---
unique_name: delivery_eta
name: Delivery ETA
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
year: '2024'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/pcovkrd84mejm/delivery-eta
- https://github.com/yandex-research/tabred/tree/main/preprocessing#delivery-eta
notebook_path: datasets/beyond_iid/temporal/delivery_eta/delivery_eta_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/delivery_eta_1m/dataset.py
source_row: 713
type_adapter_id: curation-record-v1
---

## Comments

Was downsampled/filtered by TabRed via preprocessing

CC (2026-10-19, Lennart): TabReD's quantile transform of the numeric features may be fit on all rows (undocumented); kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

## Reference

TabRed
