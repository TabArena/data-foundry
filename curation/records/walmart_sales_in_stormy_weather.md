---
unique_name: walmart_sales_in_stormy_weather
name: 'Walmart Recruiting II: Sales in Stormy Weather (Kaggle 2015)'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

Walmart's second Kaggle recruiting competition (2015): daily units of 111 items in 45 stores, 2012-01-01 to
2014-10-31, plus NOAA daily weather from the 20 stations that cover the stores. The test is the ±3 days around each
storm after 2013-04-01, cut out of the training period, and its labels were not released (test.csv is encrypted and
has no units). Measured on train.csv (2026-10-20): 4,617,600 store-item-days, 97.4% zeros, no missing or negative
values. 4,740 of the 4,995 store-item pairs never sell (the store does not carry the item); the 255 pairs that do
hold 236,038 rows with 49.7% zeros. The data page warns that a zero can also be a stockout or a discontinued item,
which the data cannot tell apart from no demand.

No as forecasting, as for `m5_forecasting_accuracy`: the task is each series' sales around storms, and the level of
the series carries it. The winner fitted a curve of log units over time per pair, then a lasso on calendar terms, and
wrote "Weather data has little effect" (forum topic 14452); the 30th place set the 4,740 dead pairs to zero and ran
kNN on the date per pair (topic 14358). Probe on the 255 active pairs, train before 2014-04-01, test after (44,220
rows): untuned LightGBM on store, item, calendar and weather reaches ROC AUC 0.971 for units > 0 and R^2 0.858 on
log1p units among positives; without the weather 0.971 and 0.856; each pair's mean over its last 28 training days
alone gives 0.953 and 0.798. Unlike `rossmann_store_sales` there are no row features beyond ids, date and weather.
Terms: Kaggle competition rules, data for the competition only.

## Reference

Walmart and Kaggle (2015). Walmart Recruiting II: Sales in Stormy Weather. Kaggle recruiting competition, closed
2015-05-25, https://www.kaggle.com/competitions/walmart-recruiting-sales-in-stormy-weather.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
