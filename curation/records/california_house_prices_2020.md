---
unique_name: california_house_prices_2020
name: CALIFORNIA_PRICES_2020
checked_by:
- Lennart
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Missing source information
tags:
- Non-IID (Temporal)
- Free Text (Sentences)
collections:
- AutoML_MM
- TabSTAR
original_source: Other
year: '2021'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46669
- https://www.kaggle.com/c/california-house-prices
notebook_path: datasets/beyond_iid/temporal/california_house_prices_2020/california_house_prices_2020.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/california_house_prices_2020/dataset.py
source_row: 734
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Split fixed: the "temporal" split ran on alphabetical address order.** The deduplication step (`groupby([Address, Zip, Year built]).idxmax()` + `df.loc[idx]`) returned rows in address order and `time_index` was then rebuilt from it (Spearman 1.000 with address rank, 0.003 with Listed On; leak audit 2026-09-24). Fix: sort back to the Kaggle Id before rebuilding `time_index`. The Id order is the sale order (checked on redfin.com earlier; in the data the latest listing date per Id decile rises from 2020-03-02 to 2020-12-30, Spearman(Id, Listed On) 0.745), so the split stays on it, not on Listed On: a house is listed before it sells, and a listing-date split could train on houses sold after the test period starts. Now: Spearman(time_index, address) 0.006, (time_index, Listed On) 0.757; in all 3 windows every training row precedes every test row. No target leak: Listed Price alone gives R^2 0.915 (legitimate, known before the sale). Leaderboard numbers on the old container come from an effectively random split.

California Houses 2020 Prices (Duplicate with calif_houses below).

Timestamp is missing! ....

Unclear if summary has an impact on predictions. A lot of spatial features, likely require spatial splits.

Very likely scraped from https://www.redfin.com/CA/Los-Altos/540-Pine-Ln-94022/home/1137626 / https://www.redfin.com/news/data-center/

Only data from redfin looks like this: https://www.kaggle.com/datasets/thuynyle/redfin-housing-market-data?select=neighborhood_market_tracker.tsv000
One could buy a scraped version: https://crawlfeeds.com/datasets/redfin-usa-properties-dataset

Summary contains free text that might not be super useful but still very much contains a lot to extract

---

Sold Price is target from the kaggle competition, the TextTabBench Paper considers Total interior livable area and Listed Price instead, data might be spatial and temporal. How do we deal with multi-categorical columns like Heating/Cooling/Parking? Also the Bedroom column is sometimes integer sometimes Text (multi-categorical), I feel like it could take a lot of preprocessing depending on what we do with columns like Heating/Cooling/Parking and similar

Unclear source of data, likely copied from somewhere with modifications. Used for teaching maybe? Data looks scraped

We need to find the original source... something from D2L website

MT: summary column feels like it makes more sense to be preprocessed into multiple columns, if it was to be converted to an embedding I can see the LM doing the conversion being confused by some fancy wording that may not mean a better apartment (like italian style of apartment) and leading to misleading results, so it makes sense just to be preprocessed in a real life scenario
Also in a real life scenario images would be used as well for such task

CC (2026-10-06, Lennart): Kept after the task-probe review (flag `one_feature`: `Listed Price`). The listing price is the natural core of predicting a sale price and is known before the sale, so its dominance is expected. On the three temporal windows of v0.2, predicting the sold price as the listed price gives R^2 0.89-0.91 (the 39 listings priced at $0 get the train mean), any curve rising with it (isotonic) 0.92, LightGBM on all numeric features 0.93, and BeyondArena's best with the text (on the old address-order split) 0.945: the methods cut the remaining error by about a fifth, so the task is not trivial. What is left to predict is the sale-to-list ratio (75% of homes sell within 10% of their list price). Data notes: 921 sales (2.2%) closed at under half or over twice their list price, some apparently one transaction booked on several houses (four listings at $1.1-1.45M each with a sold price of $8.75M).

**Assessment (AI, 2026-10-14):** 2,480 homes (6.0%) have a last sale on or after their listing date, so the listing describes an earlier sale; 125 of them give the predicted price as the last sale price. They are 5-6% of each test window but 50-54% of its squared error. LightGBM RMSE on the shipped windows: 0.196 with them, 0.140 without; also dropping 2,601 listings older than 6 months before the sale gives 0.117.

CC (2026-10-14, Lennart): Drop the 37 rows whose last sale is the sale itself and the 2,480 whose listing predates their last sale (the 37 are among them); keep listings older than 6 months. 39,048 rows.

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric stays the default RMSE: the competition scored RMSLE (Kaggle API) and the target is stored as log1p, so RMSE on it is RMSLE. The notes now say so. Needs a rebuild to reach the container (notes only).

CC (2026-10-21, Lennart): We want to keep real repeats, as houses can be sold several times; drop only exact copies of one sale.

**Assessment (AI, 2026-10-21):** Of the 63 homes that appear more than once (130 rows), 51 pairs give the same sold price a median 61 Kaggle IDs apart: one sale scraped twice; the newest entry stays. The other 28 rows (sales at another price, some of them other units at an address without a unit number) now stay instead of only the newest entry; 39,060 rows. The split also violated SPLIT-14 (Must): with min_train_fraction=0.25 the oldest of the three quarter-size windows trained on 25% of the rows. Now three windows of a sixth of the rows (6,510) from the newest half, training on 50%, 67% and 83%. Dataset check: 0 errors, 0 warnings.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSLE, the competition's evaluation metric, as RMSE on log1p(Sold Price).

## Reference

Kaggle
