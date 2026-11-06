---
unique_name: food_delivery_time
name: Food_Delivery_Time
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: No (Retired)
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- Random (IID)
- Non-IID (Temporal)
original_source: Kaggle
year: '2023'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time
notebook_path: datasets/beyond_iid/old_iid/food_delivery_time/food_delivery_time.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Predict the time taken by the delivery person to deliver the food. Spatial. Requires special feature engineering. Might need to exclude delivery person ID. Might require temporal split; might require groups/temporal splits for delivery person ID

Potential issue: spatial data must be verifyied

Lennart: Yes, if we do some spatial feature engineering (like distance) and can ignore delivery person subgroups

Andrej: Special feature engineering necessary. Unclear whether the license is fine.

Split regime is ambiguous, so both tags are set. As shipped the dataset is IID, which contradicts the
`Non-IID (Temporal)` tag the record carried alone. The TabArena (v0.1) notebook
(`datasets/_maintenance/_old_collections/tabarena-v0pt1/food_delivery_time/food_delivery_time.ipynb`) sets
`data_tags=["IID"]`, shuffles the rows and exports the default IID splits; the BeyondArena copy under
`datasets/beyond_iid/old_iid/food_delivery_time/` is identical. The Kaggle release has no timestamp at all
(10 columns: delivery person ID/age/rating, restaurant and delivery lat/long, order type, vehicle type, and
the target), so a temporal split cannot be built from the shipped data without recovering a time index. The
only non-IID structure available is the delivery person grouping, 1320 IDs over 45,451 rows, which the
notebook records as an anomaly: using that ID as a feature may call for a cold-start (grouped or temporal)
split instead. The temporal tag reflects that open question, not the protocol the dataset actually ships with.

**Assessment (AI, 2026-10-14):** the delivery point is always the restaurant plus one of 12 equal offsets in latitude and longitude (0.01-0.14 degrees), so delivery addresses are synthetic. 424 rows (0.9%) have the restaurant latitude sign flipped (159 also the longitude); the same restaurants appear with positive coordinates. 3,630 rows (8%) have the restaurant at (0, 0), a missing code; their mean time is 26.1 min against 26.3. Blanking them costs about 0.09 RMSE, dropping them nothing.

CC (2026-10-14, Lennart): Flip the signs, keep the (0, 0) rows and document the synthetic offsets.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Kaggle dataset without a competition or paper; the data card states the task but no metric.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `meituan_food_delivery_time` (TBD -> Yes, priority 4). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Retire as generated data: in the shipped file and its 20-column parent the minute within each 5-minute block is uniform noise, every other column changes only at block edges, and a courier ID holds a median of 17 different ages. Priority 1: gap 0, use case 0, source 0, shape 1, risk -1.

CC (2026-11-05, Andrej): retired as generated data (`No (Retired)`, `AHDS`). The data: 45,451 food deliveries of an unnamed Indian platform (Kaggle, rajatkumar30, 2023), a 9-column cut of an earlier 20-column upload with no documented origin (gauravmalik26, "Food Delivery Dataset", https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset).
- **The delivery time is drawn as a 5-minute block plus a random minute:** the minute within each block is uniform (19.6% to 21.2% of the orders in every block) and no feature predicts it (LightGBM R² -0.074 against -0.075 for shuffled minutes), while every other column changes only at the block edges (of the courier age's variance across delivery minutes, 0.0006 of 0.103 lies within blocks).
- **The couriers are not people:** none of the 1,320 courier IDs keeps one age, rating or vehicle (medians of 17 ages, 9 ratings and 3 vehicle types over 41 orders), and a courier's age follows the delivery time of the order (4.2 years below the courier's mean at 10-14 minutes, 3.0 above it at 50-54).
- **Other parts were already known to be made, and the larger file shares the marks:** delivery points are the restaurant plus one of 12 equal offsets (2026-10-14); in the 20-column file age 29 and rating 4.6 fill the missing entries, and its weather, traffic and order times follow the same block rule, so a rebuild from it is no way out.
Record fields `problem_type` (Regression) and `domain` (business & marketing) set from the definition. A real source for the task, `meituan_food_delivery_time`, is screened in its own record.

## Reference

https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time
