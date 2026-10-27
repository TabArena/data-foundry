---
unique_name: agribora_commodity_price_forecasting_challenge
name: agribora-commodity-price-forecasting-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
- Needs extensive data wrangling
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

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10): forecasting the weekly maize price of five Kenyan counties two weeks ahead, on a rolling leaderboard.
- Source: Zindi competition "agriBORA Commodity Price Forecasting Challenge", 2025-11-14 to 2025-12-28, 1,272 participants (Zindi API, read 2026-10-22), hosts agriBORA and Digital Africa. As published: agriBORA_maize_prices.csv ("weekly white maize prices from 2023/10 - 2025/10"), KAMIS maize prices 2021-2025/07 (raw and cleaned), the weeks 46-51 and final-week truth files.
- Use case: farmers time their sales from agriBORA's warehouses: a price forecast over a horizon.
- Metric: "MAE (50%)" and "RMSE (50%)" averaged (Zindi Evaluation page).
- Correction: the earlier AI note described a rainfall forecast; the source is a maize price forecast. The verdict is the same.
- Reject check (AI, 2026-10-22): stands. SEL-10 (Must) names a price over a horizon. Source: "predict average weekly prices of maize in the counties of Kiambu, Kirinyaga, Mombasa, Nairobi and Uasin-Gishu. At each prediction step, your model should generate forecasts for two consecutive weeks", scored on a rolling leaderboard. The use case (farmers timing sales) is itself a price forecast. https://zindi.africa/competitions/agribora-commodity-price-forecasting-challenge

Despite the 'commodity price' name, the record states the actual task is to forecast rainfall over the next 12/24 hours, generating two-week forecasts across a six-week horizon (Nov 2025-Jan 2026). That is explicit multi-step time-series forecasting, which is excluded, and the curators already flagged it as needing extensive wrangling with a temporal tag. The 50% MA / 50% RMSE metric confirms a forecasting setup. No further verification is needed to reject.

---

predict the amount of rainfall in the next 12/24 hours

Evaluation: 50% MA, 50% RMSE

At each prediction step, your model should generate forecasts for two consecutive weeks. The forecasting period spans six consecutive weeks, from November 17, 2025 to January 10, 2026.
