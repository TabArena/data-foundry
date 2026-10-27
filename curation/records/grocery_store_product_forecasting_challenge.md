---
unique_name: grocery_store_product_forecasting_challenge
name: grocery-store-product-forecasting-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://zindi.africa/competitions/grocery-store-product-forecasting-challenge
source_row: 994
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: the proposed fast reject (SEL-10) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`Time-series (Forecasting)`, SEL-10): the competition asks for future weekly sales per store, a forecast of a series.
- Source: Zindi "Grocery Store Product Forecasting Challenge", a hackathon of AI Hack (Tunisia), 2022-08-29 to 2022-08-30, 171 participants, access restricted; files `train.csv` (88 MB), `test.csv`, `dates.csv` (date features per period), `holidays.csv`, `stores.csv`, `SampleSubmission.csv`. Description and data pages did not load (zindi.africa now redirects to zindi.world, whose web page refused the connection); read through the API.
- Source's words: "Can you forecast the number of products sold per store per week for a local grocery store?"; `type_of_problem`: Forecast; metric RMSE.
- Use case: a store forecasting its weekly sales for stocking, the forecasting setting SEL-10 excludes; no fixed per-row task that TP-10 could rescue was found (the store-week panel with a date table is the series itself).
- Siblings and duplicates: `grocery_store_forecasting_challenge_for_azubian` is a later knowledge re-run of this competition (the API lists this one as its parent; the same files, `test.csv` 2,766,947 bytes in both). External collections: none found.
- Reject check (AI, 2026-10-22): does not stand. SEL-10 alone does not decide a store panel: rossmann_store_sales (store sales, given forecast horizon) ships as Yes (Andrej), and TP-10 (amended 2026-10-22) admits a per-entity panel when measured. Here: "54 different stores ... 33 different products", weekly target with promotions, transactions, holidays, "forecast the next 8 weeks for the same stores and same products" (https://api.zindi.world/v1/competitions/grocery-store-product-forecasting-challenge). Whether it passes TP-10 needs the data.
- For /add-dataset: TBD -> 2nd Tier, priority 2. Add stage: (1) PROV-8/PROV-4: 54 stores x 33 categories with onpromotion, transactions, holidays and stores tables match Corporacion Favorita's Kaggle 'Store Sales - Time Series Forecasting' (daily); confirm, and if so the source is Favorita (weekly aggregation by Zindi is a cut, PROV-6), with this record and store_sales_forecasting_challenge_for_beginners checked as duplicates; (2) TP-10 on the 8-week windows: GBM on point-in-time features vs each store-category's naive profile, and whether top solutions used target lags; (3) the log1p RMSE metric (MET-4).

Zindi competition whose stated task is to forecast the number of products sold per store per week for a local grocery store. This is sales forecasting over a temporal horizon, explicitly out of scope. The data is per-store weekly sales, a forecasting setup. Confidently No on the forecasting exclusion.

---

forecast the number of products sold per store per week for a local grocery store
