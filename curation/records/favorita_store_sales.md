---
unique_name: favorita_store_sales
name: Corporacion Favorita Grocery Sales Forecasting (Kaggle) and its family-level successor Store Sales - Time Series Forecasting
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Kaggle
year: '2017'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting
- https://www.kaggle.com/competitions/store-sales-time-series-forecasting
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: the first publication of the Favorita grocery data (and of the Zindi weekly re-cuts), a 16-day unit-sales forecast per item and store; whether it is a forecast (SEL-10) or a fixed task that passes TP-10 needs the data, as on its parent.
- Source: Kaggle featured competition "Corporación Favorita Grocery Sales Forecasting", sponsor Corporación Favorita C.A., 2017-10-19 to 2018-01-15, 1,671 teams, $30,000 (Kaggle API). As published: train.csv.7z (474 MB; `unit_sales` by `date`, `store_nbr`, `item_nbr`, with `onpromotion`; "The training data does not include rows for items that had zero unit_sales for a store/date combination"; negative values are returns); test ids start at 125,497,040, so about 125.5M training rows; items (family, class, perishable), stores (city, state, type, cluster), transactions ("Only included for the training data timeframe"), oil, holidays_events (data-description page through the Kaggle API). Its successor "Store Sales - Time Series Forecasting" (Kaggle Getting Started, from 2021-10-06, rolling) sums the same data to product families ("predict sales for the thousands of product families sold at Favorita stores"), train.csv 122 MB, test "the 15 days after the last date in the training data", data use "Competition Use and Academic, Non-Commercial Use Only".
- Source's words: "Predict a little over, and grocers are stuck with overstocked, perishable goods. Guess a little under, and popular items quickly sell out ... Corporación Favorita has challenged the Kaggle community to build a model that more accurately forecasts product sales" (Description).
- Use case: the grocer ordering stock per item and store for the next days, with the planned promotions known; fit direct, for a forecast. Regime temporal ("The public / private leaderboard split is based on time"), items and stores as groups inside.
- Siblings and duplicates: `grocery_store_product_forecasting_challenge` (Zindi 2022, AI `TBD -> 2nd Tier`, priority 2, `Time-series (Forecasting)`): its 54 stores x 33 categories match the family-level Store Sales file, so a weekly cut of this source (PROV-6, PROV-8; its own screening says the same); `store_sales_forecasting_challenge_for_beginners` and `grocery_store_forecasting_challenge_for_azubian` (Zindi re-runs, `No`, `Duplicate`); the precedent `rossmann_store_sales` (`Yes`, Andrej: store-day sales over a given horizon). External collections: none found.
- Better data: found as better data for `grocery_store_product_forecasting_challenge`; no further search this round.
- Papers and pages: the two competition pages; the winning solutions not read (the session's web search budget ran out).
- Metric: NWRMSLE, the RMSLE with weight 1.25 for perishable items and 1.00 otherwise (Evaluation page; the weights come from `items.csv`), the leaderboard metric (MET-4); inputs: the perishable flag, which ships as an item column and is also a fair feature. The Store Sales successor scores plain RMSLE.
- Risks for /add-dataset: SEL-10 against SEL-11 and TP-10: a model on point-in-time features must beat each item-store's naive profile, and whether the top solutions used lagged sales is to check; the missing zero-sales rows (an absent row is a zero or an item out of stock; the page says it cannot tell), so the target needs a rule (USE-7); about 125M rows call for a cut that keeps whole windows; transactions exist only for training dates (LEAK); item level or family level is the curator's call (PROV-6).
- Priority: gap 0 (business, regression and temporal not thin), use case + (the sponsor names the stocking decision), source + (the sponsor's competition with a documented data page), shape + (about 125M item-store-days, side tables, temporal), risk - (the forecasting doubt, joins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `grocery_store_product_forecasting_challenge`.
- as published: 2017: daily unit sales per item and store, 54 stores, about 4,000 items, 2013-01-01 to 2017-08-15, train.csv.7z 474 MB (about 125M rows), with items, stores, transactions, oil and holidays tables. ...; target: unit sales per store and item (or product family) per day; access: registration (Kaggle competition rules).
- Why: The record's own screening matched its 54 stores x 33 categories with onpromotion, transactions, holidays and stores tables to Favorita's Kaggle data; if confirmed, Favorita is the first publication (PROV-8) and the Zindi weekly table a cut of it (PROV-6). Same forecasting shape as the record: SEL-10 and TP-10 decide ...
- Adds: The original daily data at item and family level instead of a weekly re-cut, with more years of side tables; one of the most studied retail sales datasets.
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
