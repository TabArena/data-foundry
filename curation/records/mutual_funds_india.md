---
unique_name: mutual_funds_india
name: Mutual Funds India - Detailed
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2023'
domain: finance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ravibarnawal/mutual-funds-india-detailed
notebook_path: datasets/beyond_iid/new_iid/mutual_funds_india/mutual_funds_india.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/mutual_funds_india/dataset.py
source_row: 777
type_adapter_id: curation-record-v1
---

## Comments

Returns prediction, sounds reasonable, need to pick one target and go for it

Have to remove columns that leak target, we use 3 years return as target

CC (2026-10-01, Lennart): Leak audit: dropped `rating`. The data is a single snapshot (the uploader on Kaggle: "scraped in April 2023"), so `returns_3yr` is the trailing 3-year return at that date, not a future return. The uploader says the ratings come from "Value Research / Money Control"; the Value Research star rating ranks funds within their category on risk-adjusted return, weighting the 5-year score 60% and the 3-year score 40% (https://www.valueresearchonline.com/fund-rating-methodology/). It is therefore computed partly from the target, like the already dropped sharpe, sortino and alpha. In the data, the median within-category rank of returns_3yr is 0.18, 0.27, 0.49, 0.68 and 0.89 for 1 to 5 stars (Spearman with the rank of sharpe 0.63, 5-year return 0.58, 3-year return 0.52). Dropping it lowers R^2 from 0.811 to 0.783. If a future-return target were available, the rating would be a valid input. `fund_size_cr` also partly reflects past performance (assets grow with returns and inflows) but is not computed from the return, so it stays.

**Assessment (AI, 2026-10-14):** not fixable with this data. The file is one snapshot (April 2023), and the label is the trailing 3-year return, one window shared by all funds that starts just after the March 2020 crash. The fund's sub-category alone gives cross-validated R² 0.776 (all features 0.783): the task is mostly which market segment did well from 2020 to 2023. A forward return would need NAV histories from another source and several snapshot dates, since a random split within one window shares the market's outcome between train and test; that would be a new dataset.

## Reference

Kaggle
