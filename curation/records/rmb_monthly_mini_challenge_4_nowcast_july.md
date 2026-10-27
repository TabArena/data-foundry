---
unique_name: rmb_monthly_mini_challenge_4_nowcast_july
name: rmb-monthly-mini-challenge-4-nowcast-july
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
original_data_state: Other
source_links:
- https://zindi.africa/competitions/rmb-monthly-mini-challenge-4-nowcast-july/data
source_row: 887
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10): the fourth of five RMB Monthly Mini Challenges on Zindi (2023-07-01 to 2023-08-01): nowcast South Africa's July 2023 CPI, the headline value and 12 sub-categories, scored against the Stats SA release of 23 August 2023.
- Source: https://zindi.africa/competitions/rmb-monthly-mini-challenge-4-nowcast-july; as published: monthly CPI history from 2022 (`CPI_Historic_Values_Zindi*.csv`), CPI weights, Sentinel-5P air quality, JSE indices, vehicle sales and other macro series from March 2022 to May 2023; the submission has 13 rows (`July_headline CPI`, `July_food and non-alcoholic beverages`, ...).
- Why out: the target is the next value of 13 monthly price series, which is time-series forecasting (SEL-10); there is no row-level task, only 13 values per month. The record's note ("Could use multiple historical months to create new splits") describes building a forecasting panel, still SEL-10.
- Metric: `rmse`, Zindi Evaluation page.
- Reject check (AI, 2026-10-22): stands. SEL-10 (Must): Zindi Evaluation: "You are required to Nowcast the July CPI headline value as well as 12 sub-categories", scored on the Stats SA release of 23 Aug 2023; SampleSubmission.csv is 399 bytes (13 rows), type_of_problem 'Forecast' (api.zindi.world/v1/competitions/rmb-monthly-mini-challenge-4-nowcast-july). Next values of 13 national series, no row-level task; SEL-11 does not apply.

Zindi 'mini-challenge' to nowcast South Africa's July CPI inflation figure. Nowcasting an economic aggregate for a future/just-passed period is fundamentally a time-series forecasting task over a horizon, which is explicitly out of scope for this benchmark. The record's own note about using multiple historical months to create splits confirms its temporal/forecasting nature. Excluded as forecasting.

---

nowcast South Africa's July CPI. Could use multiple historical months to create new splits
