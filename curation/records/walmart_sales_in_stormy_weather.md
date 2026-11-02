---
unique_name: walmart_sales_in_stormy_weather
name: 'Walmart Recruiting II: Sales in Stormy Weather (Kaggle 2015)'
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Time-series (Forecasting)
tags:
- Two-Regime Zeros
original_source: Kaggle
year: '2015'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/walmart-recruiting-sales-in-stormy-weather
- https://www.kaggle.com/competitions/walmart-recruiting-sales-in-stormy-weather/data
v2_path: datasets/_dev/tabarena-v0pt2/walmart_sales_in_stormy_weather/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: Walmart's store-item-day sales around storms, a
panel whose forecasting test (TP-10) has not been run; the weather, the competition's premise, carried almost no signal
for the winner or in the earlier probe.
- Source: Walmart's second Kaggle recruiting competition, April to May 2015. As published: `train.csv` (date,
  store_nbr, item_nbr, units; 111 items in 45 stores, 2012-01-01 to 2014-10-31), `weather.csv` (NOAA daily weather of
  20 stations), `key.csv` (store to station), `test.csv` (units withheld, file encrypted). The earlier AI triage
  (2026-10-20) measured 4,617,600 store-item-days with 97.4% zeros; 4,740 of the 4,995 store-item pairs never sell,
  and the 255 that do hold 236,038 rows with 49.7% zeros. Data page on the zeros: "sales number 0 doesn't necessarily
  mean there was no demand ... it could mean that the product was out of stock, or discontinued and not available".
- Use case: the Description names actor and decision: "it's difficult for replenishment managers to correctly predict
  the level of inventory needed to avoid being out-of-stock or overstock during and after that storm". Fit
  approximate: the features are the observed weather ("it's as though you have a perfect weather forecast at your
  disposal", data page), and the test days (3 days either side of each storm after 2013-04-01) are cut out of a period
  whose other days are training data, so the test interpolates rather than looks ahead. Regime temporal (SPLIT-6),
  store-item pairs recur (SPLIT-13).
- Scope doubt (SEL-10, SEL-11, TP-10): the earlier pass proposed `No` as forecasting. Not a fast reject: the task
  is fixed days around storms with an outside driver, and TP-10 has not been run on shipped windows. The evidence
  leans out: the winner (topic 14452, threecourse): "Weather data has little effect, so I believe any method will be
  the same"; the earlier probe (255 active pairs, train before 2014-04-01, test after, untuned LightGBM) reached R^2
  0.858 on log1p units among positives with weather and 0.856 without, against 0.798 for each pair's mean of its last
  28 training days (ROC AUC for units > 0: 0.971, 0.971, 0.953), not on the declared metric.
- Siblings and duplicates: `m5_forecasting_accuracy` (Walmart again, other stores, items and years; `TBD -> 2nd Tier`, Andrej 2026-10-30, after the AI's `No`),
  `rossmann_store_sales` (Yes, Andrej: store-day sales with promotions and holidays, a given horizon),
  `grocery_store_product_forecasting_challenge` (TBD -> 2nd Tier after a refuted SEL-10 reject, 2026-10-22). No
  external collection found.
- Papers and pages: the Kaggle Description, Data and Evaluation pages; forum topics 14452 (first place) and 14358
  (the 30th place set the dead pairs to 0 and ran kNN on the date per pair, per the earlier triage). No paper found.
- Metric: RMSLE on units (Evaluation page: "Submissions are evaluated one the Root Mean Squared Logarithmic Error
  (RMSLE)"), the leaderboard metric (MET-4); inputs none. On a log1p target it is `rmsle` with
  `target_transform="log1p"` (MET-3).
- Risks for /add-dataset: run TP-10 on the shipped windows with RMSLE against each pair's naive profile; the 4,740
  pairs that never sell and the stockout zeros (the family's open question on coded and censored zeros); test labels
  were never released, so the windows come from the training period; weather codes ("T" trace, "M" missing) and the
  store-station join (`key.csv`).
- Priority: gap 0, use case 0 (actor named, fit approximate), source + (Walmart's data page documents every field),
  shape + (236,038 active store-item-days, weather, dated), risk - (scope doubt, structural zeros).

**Assessment (AI, 2026-10-30):** The family's open question on coded and censored zeros is settled (Andrej, 2026-10-30,
policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task, independent
if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower priority. Stock-out
zeros and never-sold pairs are a cleaning choice at /add-dataset. The verdict and priority stay on the screening's other
points (the forecasting question, TP-10).

**Consistency check (AI, 2026-10-30):** the review page sets `Yes`, priority 2. The record carries `Time-series
(Forecasting)` and TP-10 has not run; weather, the competition's premise, added almost nothing (R^2 0.858 with it, 0.856
without, 0.798 for a 28-day mean). For `metro_manila_village_weekly_dengue` the curator asked for the TP-10 leg first
(TBD -> Yes), and `m5_forecasting_accuracy` stays 2nd Tier on the same question. Options: `Yes` with TP-10 run at
/add-dataset; or TBD -> Yes until TP-10 runs.

CC (2026-10-30, Andrej): `Yes`, priority 2 (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening
review page, after the AI's consistency check). "Do yes and then we can see what happens"

Walmart's second Kaggle recruiting competition (2015): daily units of 111 items in 45 stores, 2012-01-01 to
2014-10-31, plus NOAA daily weather from the 20 stations that cover the stores. The test is the ±3 days around each
storm after 2013-04-01, cut out of the training period, and its labels were not released (test.csv is encrypted and
has no units). Measured on train.csv (2026-10-20): 4,617,600 store-item-days, 97.4% zeros, no missing or negative
values. 4,740 of the 4,995 store-item pairs never sell (the store does not carry the item); the 255 pairs that do
hold 236,038 rows with 49.7% zeros. The data page warns that a zero can also be a stockout or a discontinued item,
which the data cannot tell apart from no demand.

No as forecasting (the AI's earlier call; `m5_forecasting_accuracy`, cited here as `No`, is `TBD -> 2nd Tier` by Andrej's call of 2026-10-30): the task is each series' sales around storms, and the level of
the series carries it. The winner fitted a curve of log units over time per pair, then a lasso on calendar terms, and
wrote "Weather data has little effect" (forum topic 14452); the 30th place set the 4,740 dead pairs to zero and ran
kNN on the date per pair (topic 14358). Probe on the 255 active pairs, train before 2014-04-01, test after (44,220
rows): untuned LightGBM on store, item, calendar and weather reaches ROC AUC 0.971 for units > 0 and R^2 0.858 on
log1p units among positives; without the weather 0.971 and 0.856; each pair's mean over its last 28 training days
alone gives 0.953 and 0.798. Unlike `rossmann_store_sales` there are no row features beyond ids, date and weather.
Terms: Kaggle competition rules, data for the competition only.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/walmart_sales_in_stormy_weather/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend `TBD -> 2nd Tier` (as m5_forecasting_accuracy) until you set the leg-1 bar in crms_phragmites_cover's issue 1, then `No` (`Time-series (Forecasting)`) unless the TP-10 test passes: over three seeds the model leads the best forecast from each pair's own sales by 1.1-1.5% (1.2-1.4 standard errors, 1.8 with trailing summaries), below that issue's line of 2, and leg 2 fails as written. Changes after the panel: the 16 observed weather columns dropped (LEAK-10), a one-day planning gap, the use case reworded to every day of the coming week. Corrections to the notes above: the test is nine weekly windows ahead in time (2013-01-28 to 2013-03-31), not days cut around storms; the table holds the 231 pairs that sold before them, 2012-01 to 2013-03 (104,041 rows, 41.1% zeros), not 255 pairs over 2012-2014 (236,038 rows, 49.7%). `suggestion` and the marker stay until your mark on issue 1. Priority 2: gap 0, use case 0 (actor named, fit approximate), source + (Walmart's data page documents every field), shape + (104,041 rows, temporal), risk - (the recommendation not to ship).

CC (2026-11-02, Andrej): TP-10 stays as written (crms_phragmites_cover issue 1, and issue 1 here, (a)): no 2-standard-error line and no amendment of leg 2; the record holds at `TBD -> 2nd Tier` with `Time-series (Forecasting)`, as m5_forecasting_accuracy, until a tuned model is tried against the forecasts built from each pair's own sales.

CC (2026-11-02, Andrej): `TBD -> Yes` (issue 2): "Does this mean the task is good and valid but we don't ship it atm because of the time-series nature? If that's the only reason, we should rather switch to tbd yes". It is the only reason (TP-10; the data, split and metric hold), so the record moves from `TBD -> 2nd Tier` to `TBD -> Yes`, `Time-series (Forecasting)` kept as the reason it waits; the folder stays. Departs from m5_forecasting_accuracy and grocery_store_product_forecasting_challenge (`TBD -> 2nd Tier`) and crms_phragmites_cover (`No`) on the same TP-10 result; whether they move is put to Andrej.

CC (2026-11-02, Andrej): don't ship for now: "Don't ship for now, but keep it as tbd yes". The record stays `TBD -> Yes` with `Time-series (Forecasting)`, the folder stays unbuilt.

## Reference

Walmart and Kaggle (2015). Walmart Recruiting II: Sales in Stormy Weather. Kaggle recruiting competition, closed
2015-05-25, https://www.kaggle.com/competitions/walmart-recruiting-sales-in-stormy-weather.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
