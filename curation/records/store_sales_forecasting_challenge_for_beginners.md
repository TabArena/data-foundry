---
unique_name: store_sales_forecasting_challenge_for_beginners
name: store-sales-forecasting-challenge-for-beginners
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
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
source_links:
- https://zindi.africa/competitions/store-sales-forecasting-challenge-for-beginners
source_row: 944
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10): forecast weekly sales per store and product category for the next eight weeks.
- Source: Zindi beginner hackathon (Young AI Leaders Kampala Hub, Tufuna Technologies), 23 May to 3 June 2025, 113 participants (https://zindi.africa/competitions/store-sales-forecasting-challenge-for-beginners, read through the Zindi API); a child of `grocery_store_product_forecasting_challenge` (AI Hack Tunisia 2022, `No`, `Time-series (Forecasting)`, AI); as published: train.csv (88 MB, "transaction information for 3 years and 6 months"), test.csv, stores, dates, holidays; "anonymised real data", 54 stores and 33 product categories (the counts of the Favorita store-sales data on Kaggle; unconfirmed).
- Use case: stock ordering for small chain stores, from a forecast of the series.
- Metric: RMSE on log1p of the target (Zindi Evaluation page).
- Reject check (AI, 2026-10-22): stands. It stands on PROV-4 (Duplicate), not on SEL-10. The Zindi API lists grocery-store-product-forecasting-challenge as its parent, and all six files have byte-identical sizes (train.csv 87,712,551; test.csv 2,766,947; dates.csv 81,765; holidays.csv 1,822; stores.csv 864; SampleSubmission.csv 520,786) (https://api.zindi.world/v1/competitions/store-sales-forecasting-challenge-for-beginners vs .../grocery-store-product-forecasting-challenge). The SEL-10 half alone does not stand: today's reject check refuted it on the parent (rossmann_store_sales ships as Yes; TP-10 needs the data), and the parent is TBD -> 2nd Tier, priority 2. The marker should be `Duplicate` (PROV-4), like grocery_store_forecasting_challenge_for_azubian, and not `Time-series (Forecasting)`.

A Zindi 'store-sales-forecasting-challenge-for-beginners'. The name makes clear it is a sales-forecasting task (predicting future store sales over time), which is explicitly excluded as time-series forecasting. There is no indication of a reframable fixed predictive target. Recommend reject.
