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

Zindi competition whose stated task is to predict demand for each individual product four months into the future. Forecasting future values over a horizon is explicitly out of scope for the benchmark. The data is per-product/per-time stock/sales records, i.e. a forecasting setup rather than a fixed predictive task that merely needs a temporal split. A human should confirm there is no reframable static target, but on the stated framing this is a clear forecasting exclusion.

---

predict demand for each individual product, four months into the future
