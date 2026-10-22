---
unique_name: mtoto_news_childline_kenya_call_volume_prediction_challenge
name: mtoto-news-childline-kenya-call-volume-prediction-challenge
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
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/mtoto-news-childline-kenya-call-volume-prediction-challenge/data
source_row: 926
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10): hourly call counts of Childline Kenya's 116 hotline, trained on 1 January to 12 July 2016 and predicted for 13 July to 6 September 2016: future values of one series over a horizon.
- Source: Zindi competition "Mtoto News Childline Kenya Call Volume Prediction Challenge", 11 Apr to 5 Aug 2019, sponsored by Mtoto News and Childline Kenya (https://zindi.africa/competitions/mtoto-news-childline-kenya-call-volume-prediction-challenge, read through Zindi's page API; Zindi's problem type "Forecast"); as published: train.csv of "all the calls (over 135,000) that were received from 1 January 2016 to 12 July 2016" (call date and time, case status, category, priority, caller and child age, gender and county, abuser relationships), plus Nairobi school dates, Nairobi weather and Kenyan public holidays 2016; the submission is `time_index` (an hour, e.g. 2016071300) and `calls`.
- Use case: "Your solution will help Childline manage its resources and staff their call center more efficiently" (Description): staffing from a forecast of hourly demand, which is the forecasting protocol SEL-10 excludes; the call records describe past calls, not the hours to predict.
- Siblings and duplicates: `childline_kenya_call_volume_prediction_challenge` (Zindi Mentorship 3 re-run of the same task, AI `No` with the same marker): a duplicate of this one by provenance (PROV-4) if the data is the same.
- Metric: RMSE on hourly call counts ("The evaluation metric for this challenge is the Root Mean Squared Error", Evaluation tab).
- Reject check (AI, 2026-10-22): stands. 'create a forecast model to predict the number of incoming calls ... per hour per day', trained on 1 Jan to 12 Jul 2016 and predicted for 13 Jul to 6 Sep 2016; type_of_problem ['Forecast']. It is one series (hotline-wide hourly counts), not a panel, so SEL-11/TP-10 cannot apply, and the per-call fields do not exist for the future hours. https://zindi.africa/competitions/mtoto-news-childline-kenya-call-volume-prediction-challenge

A Zindi competition whose name explicitly states predicting call volume for Childline Kenya. Call-volume prediction over time is a demand/forecasting task, which is explicitly excluded from the benchmark scope. The name strongly signals forecasting future call counts over a horizon rather than a fixed predictive task. A human could verify whether any concurrent-feature (non-horizon) framing exists, but on the name and typical setup this is a No.
