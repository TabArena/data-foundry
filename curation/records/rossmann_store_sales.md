---
unique_name: rossmann_store_sales
name: Rossmann Store Sales
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
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

CC (2026-11-01, Lennart): marks on the review board of PR #37: DayOfWeek (an unordered category before) and CompetitionOpenSinceMonth are numbers (the curator's cycle rule); Assortment stays unordered as a partial order, noted.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (Rossmann's competition), shape +, risk 0 (the open issue is the choice of windows).

CC (2026-11-11, Lennart): REVIEW.md issue 1, B ("Option B: Spread over the eligible history."): the test windows are 20 June to 31 July 2015, the Christmas weeks of 2014 (22 November 2014 to 2 January 2015) and late spring 2014 (26 April to 6 June), evenly spaced over the 11 windows that keep half the store-days, in place of the newest 18 weeks.

CC (2026-11-11, Lennart): the declared horizon (42 days, a one-day gap, windows starting 2015-06-20, 2014-11-22 and 2014-04-26) is checked, as Kaggle states the store managers' horizon as six weeks and the competition's own test period, 48 days, is about as long (REVIEW.md horizon, ok).

**Assessment (AI, 2026-11-11):** applied issue 1 (B): test 40,282, 31,203 and 38,107 store-days, train 802,996, 617,355 and 443,771 (95.1%, 73.1% and 52.6%); the Christmas window sells 8,478 per open store-day against 6,837 on its train side and tests 935 stores until 31 December. The 1,114 store-days of 19 June 2015, the newest window's gap day, lie in no split (an accepted warning). `dataset check`: 0 errors, 0 warnings.

## Reference

FlorianKnauer and Will Cukierski. Rossmann Store Sales. https://kaggle.com/competitions/rossmann-store-sales, 2015. Kaggle.
