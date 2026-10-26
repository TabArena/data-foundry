---
unique_name: cooking_time
name: Cooking Time
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
- https://www.kaggle.com/datasets/pcovkrd84mejm/cooking-time
- https://github.com/yandex-research/tabred/tree/main/preprocessing#cooking-time
notebook_path: datasets/beyond_iid/temporal/cooking_time/cooking_time_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/cooking_time_1m/dataset.py
source_row: 712
type_adapter_id: curation-record-v1
---

## Comments

Was downsampled/filtered by TabRed via preprocessing. Need to see what we want to resample

TabRed uses 1 week refit horizon. 36 days in train data

Tasks look reasonable even if missing all semantic information. Given that the data is from various restaurants and that it is unclear which restaurant this is from, there might be group-based leakage.

Note: numerical features are normalized with a noisy-quantile transform QuantileTransformer(X_num + 1e-5 * randn)

CC (2026-10-19, Lennart): TabReD's quantile transform of the numeric features may be fit on all rows (undocumented); kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): check SPLIT-9 on the weekly test windows and add a gap where train labels arrive late, as for nyc_taxi_trip_duration and pkdd_15 (cross-dataset review, marked ok).

**Assessment (AI, 2026-10-21):** SPLIT-9 late labels in cooking_time_1m (order time + cooking time, from the raw file after the under-one-minute filter): without a gap 172, 126 and 108 train orders per weekly window (newest first; starts 2023-12-28, 12-21, 12-14) end after the window start; with a gap of one day (TemporalSplits(..., gap=1)) none. The gap removes 280k, 264k and 239k of the 11.1M, 9.1M and 7.2M earlier orders (2.5 to 3.3%); each train side is still a random 1M. Gap set in dataset.py, counts in splits_comment; script local-data-warehouse/_runs/2026-10-21_crosscut/x21-0/late_labels.py.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSE (TabReD regression tasks), Rubachev et al., TabReD, ICLR 2025 (https://arxiv.org/abs/2406.19380), Sec. 4 / App.: RMSE for regression, ROC AUC for classification.

## Reference

TabRed
