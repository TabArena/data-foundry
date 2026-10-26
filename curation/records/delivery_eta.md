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

CC (2026-10-21, Lennart): check SPLIT-9 on the weekly test windows and add a gap where train labels arrive late, as for nyc_taxi_trip_duration and pkdd_15 (cross-dataset review, marked ok).

**Assessment (AI, 2026-10-21):** SPLIT-9 late labels in delivery_eta_1m (order time + delivery time, from the raw file after the under-one-minute filter): 0 train orders in each of the 3 weekly windows (starts 2024-01-01 04:02, 2023-12-25 00:03, 12-18 00:02) end after the window start, because orders pause overnight and the last train order of a window is delivered 57 minutes to 6 hours before it. No gap added; the counts are in splits_comment. Script local-data-warehouse/_runs/2026-10-21_crosscut/x21-0/late_labels.py.

**Assessment (AI, 2026-10-21):** Metric declared for `delivery_eta_1m` under MET-1..13: source rmse — TabReD (Rubachev et al., ICLR 2025) scores RMSE on the log minutes.

## Reference

TabRed
