---
unique_name: agribora_commodity_price_forecasting_challenge
name: agribora-commodity-price-forecasting-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Needs extensive data wrangling
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2025'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/agribora-commodity-price-forecasting-challenge/data
source_row: 869
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Despite the 'commodity price' name, the record states the actual task is to forecast rainfall over the next 12/24 hours, generating two-week forecasts across a six-week horizon (Nov 2025-Jan 2026). That is explicit multi-step time-series forecasting, which is excluded, and the curators already flagged it as needing extensive wrangling with a temporal tag. The 50% MA / 50% RMSE metric confirms a forecasting setup. No further verification is needed to reject.

---

predict the amount of rainfall in the next 12/24 hours

Evaluation: 50% MA, 50% RMSE

At each prediction step, your model should generate forecasts for two consecutive weeks. The forecasting period spans six consecutive weeks, from November 17, 2025 to January 10, 2026.
