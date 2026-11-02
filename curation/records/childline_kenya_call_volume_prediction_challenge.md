---
unique_name: childline_kenya_call_volume_prediction_challenge
name: Childline Kenya Call Volume Prediction Challenge
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
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/zindi-mentorship-3-childline-kenya-call-volume-prediction-challenge
source_row: 1013
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10; `Duplicate`, PROV-4): an hourly call-count forecast over a fixed future window, and a private re-run of `mtoto_news_childline_kenya_call_volume_prediction_challenge`.
- Source: Zindi, "Zindi Mentorship #3: Childline Kenya Call Volume Prediction Challenge", 2020-08-04 to 2020-08-26, a private hackathon for the mentorship cohort (19 participants); the Zindi API names its parent competition `mtoto-news-childline-kenya-call-volume-prediction-challenge` (2019, 272 participants), problem type "Forecast". As published: train.csv, every call from 1 Jan to 12 Jul 2016 (over 135,000 calls with case fields), plus public holidays, Nairobi school dates and weather; the submission is `time_index` (YYYYMMDDHH) and `calls`.
- Use case: Childline staffs its call centre ("manage its resources and staff their call center more efficiently"); the prediction is the future values of one series, which is forecasting (SEL-10), not a fixed task with a temporal split (SEL-11).
- Siblings and duplicates: `mtoto_news_childline_kenya_call_volume_prediction_challenge` (AI `No`, `Time-series (Forecasting)`) is the original competition on the same data; this record is its re-run.
- Metric: "The evaluation metric for this challenge is the Root Mean Squared Error" (Zindi evaluation page, read through the Zindi API).
- A per-call classification (case priority, category) would be a task the source did not set (SEL-8).
- Reject check (AI, 2026-10-22): stands. Zindi API (api.zindi.world/v1/competitions/zindi-mentorship-3-childline-kenya-call-volume-prediction-challenge): 'create a forecast model to predict the number of incoming calls that Childline Kenya will receive per hour per day', RMSE, 19 participants, parent mtoto-news-childline-kenya-call-volume-prediction-challenge (272 participants, already No). Future values of one series (SEL-10) and a re-run of the parent (PROV-4).

Zindi challenge to forecast the number of calls a child-protection hotline will receive each hour of each day. This is explicitly forecasting future call volumes over a time horizon, which is out of scope for the benchmark per the time-series-forecasting exclusion. There is no fixed predictive task that merely needs a temporal split here. Reject; no further verification needed beyond confirming the forecasting framing, which the record already states.

---

Forecast how many calls a child protection hotline will receive each hour each day.
