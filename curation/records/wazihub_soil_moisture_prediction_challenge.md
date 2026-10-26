---
unique_name: wazihub_soil_moisture_prediction_challenge
name: wazihub-soil-moisture-prediction-challenge
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
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://zindi.africa/competitions/wazihub-soil-moisture-prediction-challenge
source_row: 928
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10): a forecast of each field's soil humidity over the next days, at 5-minute steps, from its own past.
- Source: Zindi "Wazihub Soil Moisture Prediction Challenge", 29 Jul to 21 Oct 2019, sponsored by Wazihub and Microsoft (read through Zindi's API; the API's problem type is "Forecast"); as published: IoT readings every five minutes "over 4 months in 4 fields growing maize and peanuts in Senegal" (soil humidity per field, air temperature, humidity, pressure, wind, an irrigation flag) and hand-collected daily context files; Train.csv 2,033,452 bytes.
- The task: "create a machine learning model capable of predicting the humidity for a particular plot in the next few days, using data from the past"; "You will need to predict, in 5-minute increments, the last four days for soil humidities in fields 1 and 3 and ... the last six days for soil humidities in fields 2 and 4"; "You may not use data from the future". Future values of four series over a horizon, with no fixed per-row target (SEL-11 does not apply).
- Siblings and duplicates: none in `curation/records/`.
- Metric: RMSE (Evaluation page), moot.
- Reject check (AI, 2026-10-22): stands. Zindi (https://zindi.africa/competitions/wazihub-soil-moisture-prediction-challenge, API type_of_problem ['Forecast']): "predicting the humidity for a particular plot in the next few days, using data from the past" and "predict, in 5-minute increments, the last four days for soil humidities in fields 1 and 3 ... the last six days ... in fields 2 and 4". Future values of four sensor series over a horizon: SEL-10 (Must); SEL-11/TP-10 does not rescue it (no fixed per-row target, only 4 entities, the use case is anticipating the series).

WaziHub soil moisture prediction challenge (Zindi) asks competitors to forecast future soil moisture values from IoT sensor time-series streams. This is a time-series forecasting task over a horizon, which is explicitly excluded from the benchmark scope. The data is sensor logs rather than a single predictive cross-sectional table. A human should confirm the framing, but the name and known task strongly indicate forecasting, so the suggestion is No.
