---
unique_name: rossmann_store_sales
name: Rossmann Store Sales
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: Kaggle
year: '2015'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/c/rossmann-store-sales
notebook_path: datasets/beyond_iid/temporal/rossmann_store_sales/rossmann_store_sales.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/rossmann_store_sales/dataset.py
source_row: 725
type_adapter_id: curation-record-v1
---

## Comments

Awesome dataset, even the forecast horizon is given.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: Promo, SchoolHoliday, Promo2.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmspe — Root Mean Square Percentage Error (RMSPE) (https://www.kaggle.com/competitions/rossmann-store-sales/overview/evaluation (Kaggle API evaluationMetric: 'Root Mean Square Percentage Error')).

CC (2026-10-21, Lennart): the declared metric stays as it is (`rmspe`, as Kaggle scored; cross-dataset item "Metrics still to settle").

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `DayOfWeek` (a partial order); `Assortment` (a partial order).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 calendar or compass cycles ordered.

## Reference

FlorianKnauer and Will Cukierski. Rossmann Store Sales. https://kaggle.com/competitions/rossmann-store-sales, 2015. Kaggle.
