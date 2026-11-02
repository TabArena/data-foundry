---
unique_name: fossil_stock_forecasting_challenge
name: fossil-stock-forecasting-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
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
- https://zindi.africa/competitions/fossil-stock-forecasting-challenge/data
- https://zindi.africa/competitions/fossil-top-5-challenge/data
source_row: 894
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10): Fossil's monthly sell-in per SKU, to be forecast four months ahead.
- Source: Zindi "Fossil Demand Forecasting Challenge" (2022-05-24 to 2022-08-28, $5,000) and its invite-only follow-up "Fossil Top 5 Challenge" (2022-10); Zindi problem type "Forecast". Data: "the number of items sold of each item (or SKU) each month", sales per major channel, beginning-of-period and on-hand inventory; target "sellin" four months ahead; Train.csv, Test.csv, DataDictionary.csv.
- Deciding words: "The objective of this challenge is to build a forecasting or other predictive model to determine as accurately as possible the demand for each individual product, four months into the future" and (Top 5) "Predictions are calculated on a monthly basis, pointing to the 4-month-out forecast ... the forecast has to be computed with the data available at the moment of the prediction" (https://zindi.africa/competitions/fossil-stock-forecasting-challenge, https://zindi.africa/competitions/fossil-top-5-challenge).
- Not SEL-11: the target is the future value of each SKU's own monthly series, not a fixed outcome of a unit; the submission IDs are SKU_month.
- Metric: MAE (Zindi Evaluation page; Fossil also reviewed ME, RMSE, MPE, MAPE). Siblings: none (grep fossil).
- Reject check (AI, 2026-10-22): stands. SEL-10 (Must). Zindi Description: "The objective of this challenge is to build a forecasting or other predictive model to determine as accurately as possible the demand for each individual product, four months into the future"; type_of_problem ["Forecast"]; submission ids are SKU_month (YOSHTLYNYOSHZZ_11_2021), so the target is each SKU's own monthly sell-in series over a horizon. Fossil also scores ME/RMSE/MPE/MAPE "of the quantity being forecast". No fixed per-unit outcome to rescue under SEL-11. https://zindi.africa/competitions/fossil-stock-forecasting-challenge

Zindi competition whose stated task is to predict demand for each individual product four months into the future. Forecasting future values over a horizon is explicitly out of scope for the benchmark. The data is per-product/per-time stock/sales records, i.e. a forecasting setup rather than a fixed predictive task that merely needs a temporal split. A human should confirm there is no reframable static target, but on the stated framing this is a clear forecasting exclusion.

---

predict demand for each individual product, four months into the future
