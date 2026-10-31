---
unique_name: immoscout_german_house_prices
name: ImmoScout24 German-House-Prices
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- New IID
- Free Text (Short)
collections:
- TabSTAR
original_source: Kaggle
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=43342&sort=runs&status=active (copy, uploaded 2022-03-23)
- https://www.kaggle.com/code/shritech1404/german-housing-price-prediction (Nov 2020 notebook reading the original file)
- 'Original source is a deleted Kaggle dataset: german-house-prices, file germany_housing_data_14.07.2020.csv, owner unknown'
notebook_path: datasets/beyond_iid/new_iid/immoscout_german_house_prices/immoscout_german_house_prices.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/immoscout_german_house_prices/dataset.py
source_row: 684
type_adapter_id: curation-record-v1
---

## Comments

Missing date column, but as it represents a snapshot of data at a certain time point (when scraped) it represents live data and could be used to fit a model for other houses at the same time

Moreover, this is not sold prices (as immoscout shows only prices you can ask to buy it for and how much it was sold for AFAIK), so the snapshot here represents a task where someone would want to predict the price I should offer for my house given other houses that are currently offered. Thus, it seems like a real task where someone would want to build a model to know how much they should offer the houses at in the current market (with the limitation that past trends are ignored)

**Assessment (AI, 2026-10-14):** the data first appeared on Kaggle as the dataset `german-house-prices` (the 2020 notebook above reads `/kaggle/input/german-house-prices/germany_housing_data_14.07.2020.csv`). It is deleted and its owner could not be found, so the source stays Kaggle and the download stays the OpenML copy (43342, collection date 14-07-2020, the Kaggle card's text). The year is now 2020, the scrape date, instead of 2019.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — A scraped Kaggle dataset (since deleted) and its OpenML copy; neither defines a task or metric. RMSE on the log price is the obvious choice for price prediction.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: an asking price's error matters relative to the price; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `Energy_efficiency_class` (the README lists their levels); left unordered: `Furnishing_quality` (low confidence); `Condition` (a partial order); Condition and Furnishing_quality labels are permuted in the scrape ("dilapidated": 1,137 houses, median year built 2010, the highest median price; "as new": 11, 1870, the lowest; Furnishing "refined" the oldest and cheapest); the German labels are lost, so both stay unordered with a note. Options for the curator: swap the two clear levels, neutral codes, or keep..

CC (2026-10-31, Lennart): marks on the review board of PR #37: Condition, Furnishing_quality, Type and Heating relabelled with ImmoScout24's own codes, found by matching 3,548 houses to an April 2020 scrape that keeps them (each label permuted, the missing value swapped with a real level in each column); Furnishing_quality then ordered.

## Reference

Kaggle / OpenML
