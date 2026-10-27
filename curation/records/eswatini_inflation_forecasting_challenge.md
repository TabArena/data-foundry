---
unique_name: eswatini_inflation_forecasting_challenge
name: eswatini-inflation-forecasting-challenge
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
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/eswatini-inflation-forecasting-challenge
source_row: 950
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10): "Your task is to predict Eswatini's headline inflation two months ahead, using the 13 years of historical data provided" (Description).
- Source: Zindi "Eswatini Inflation Forecasting Challenge" ("Can you nowcast Eswatini headline inflation?", AI Eswatini with the Central Bank of Eswatini, 15 Sep - 15 Oct 2025, https://zindi.africa/competitions/eswatini-inflation-forecasting-challenge). As published: CPI_GDP_data.xlsx with "13 years of monthly headline inflation data" and "20 years of annual GDP data"; the submission has two rows, `September_headline` and `October_headline`.
- Use case: the central bank's inflation forecast ("The top three solutions will be delivered to the Central Bank of Eswatini"); a single national series over a horizon, the forecasting task SEL-10 excludes; about 156 monthly values, no panel for TP-10.
- Siblings and duplicates: none found. External collections: none.
- Metric: RMSE on a rolling leaderboard "rescored ... using the official September value ... the official October value" (Evaluation tab).
- Reject check (AI, 2026-10-22): stands. A single national series forecast over a horizon (SEL-10). Zindi (https://zindi.africa/competitions/eswatini-inflation-forecasting-challenge): 'predict Eswatini's headline inflation two months ahead, using the 13 years of historical data provided'. Two submission rows, no panel, so SEL-11/TP-10 cannot apply.

Zindi 'Eswatini Inflation Forecasting Challenge' is, by its name, a time-series forecasting task predicting future inflation values over a horizon. Forecasting future values is explicitly out of scope for the benchmark. Excluded as Time-series (Forecasting); a human need only confirm it is genuine horizon forecasting rather than a fixed predictive task that merely needs a temporal split.
