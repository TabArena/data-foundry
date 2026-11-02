---
unique_name: cryptocurrency_closing_price_prediction
name: cryptocurrency-closing-price-prediction
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/cryptocurrency-closing-price-prediction
- https://zindi.africa/competitions/kabarak-2022
source_row: 911
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10): the organisers frame the task as forecasting future prices of one
hourly series.
- Source: Zindi "Cryptocurrency Closing Price Prediction" by Think.iT (25 June - 19 September 2021; a parent
  "cryptocurrency-closing-price-prediction-challenge" closed April 2021); re-run as a learning hackathon `kabarak-2022`
  (Developer Student Club Kabarak University, Nov-Dec 2022) with the same files (Train.csv 3.4 MB, Test.csv 1.6 MB).
  As published: hourly rows from 1 March 2020 to 1 March 2021, `asset_id`, open/high/low/volume, market cap and
  about 40 social-media counts and scores (tweets, Reddit, sentiment, `price_score` from a moving average); target `close`.
- Use case: investment decisions on a volatile asset (Zindi); the target is the next values of a price series (SEL-10),
  not a fixed task that only needs a temporal split (SEL-11).
- Siblings: `g_research_crypto_forecasting` (`Yes`, Lennart) predicts residualised 15-minute returns across 14 assets,
  a fixed target over a cross-section; this record has the raw price level of one series.
  `the_ultimate_hacking_challenge_by_uct_cryptocurrency_and_ai_society` is a different challenge.
- Metric: RMSE (Zindi: "The error metric for this competition is the Root Mean Squared Error").
- Reject check (AI, 2026-10-22): stands. SEL-10: the source frames forecasting of one series, "we would like to build a model that forecasts a cryptocurrency's price ... We will predict future cryptocurrency prices", hourly data 2020-03-01 to 2021-03-01 (Zindi description via https://api.zindi.world/v1/competitions/cryptocurrency-closing-price-prediction). Unlike g_research_crypto_forecasting (residualised returns across 14 coins, TP-10 passed) this is the raw price level of a cryptocurrency, so no cross-entity panel for TP-10 to rescue.

Zindi challenge to predict the closing price of a cryptocurrency. Predicting a future closing price is financial time-series forecasting over a horizon, which is explicitly out of scope for the benchmark. There is no fixed, non-temporal predictive task here that would merely need a temporal split. Reject; the forecasting framing is clear from the title and the record's description.

---

predict the closing price for a cryptocurrency
