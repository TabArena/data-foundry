---
unique_name: grocery_store_forecasting_challenge_for_azubian
name: grocery-store-forecasting-challenge-for-azubian
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
- Duplicate
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
- https://zindi.africa/competitions/grocery-store-forecasting-challenge-for-azubian/data
source_row: 962
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10; `Duplicate`, PROV-4): weekly sales forecasting, and a re-run of `grocery_store_product_forecasting_challenge` on the same files.
- Source: Zindi "Grocery Store Forecasting Challenge For Azubian", a knowledge hackathon (Senegal cohort, 2022-11-07 to 2024-06-06, 25 participants, "As this is a learning challenge, aside from the rules in the Terms of Use, no other particular rules apply"); the API names `grocery-store-product-forecasting-challenge` (AI Hack, 2022-08) as its parent, and the files are the same (`train.csv` 88 MB, `test.csv` 2,766,947 bytes, `dates.csv`, `holidays.csv`, `stores.csv`). Read through the API; the web page refused the connection.
- Source's words: "Can you forecast the number of products sold per store per week for a local grocery store?"; `type_of_problem`: Forecast; metric RMSE.
- Use case: a store forecasting weekly sales (SEL-10).
- Siblings and duplicates: `grocery_store_product_forecasting_challenge` (the parent, also proposed `No`); the other Azubian re-runs follow the same pattern (`customer_churn_prediction_challenge_for_azubian` is `No`, `Duplicate` of `expresso_churn_prediction`). External collections: none found.
- Reject check (AI, 2026-10-22): stands. PROV-4: a learning re-run of grocery_store_product_forecasting_challenge; the Zindi API lists that competition as its parent, and description, data description and file list are word-for-word the same (https://api.zindi.world/v1/competitions/grocery-store-forecasting-challenge-for-azubian). The SEL-10 half is refuted on the parent (see there), but the duplicate holds whatever the parent's verdict.

Zindi 'grocery store forecasting' competition; the name indicates demand/sales forecasting for a grocery store. Forecasting future sales over a horizon is explicitly out of scope. The data is per-store/per-time sales records, a forecasting setup rather than a static predictive task. No, pending only a human confirmation that there is no reframable fixed target.
