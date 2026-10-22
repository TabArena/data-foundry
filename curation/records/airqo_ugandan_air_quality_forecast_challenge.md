---
unique_name: airqo_ugandan_air_quality_forecast_challenge
name: airqo-ugandan-air-quality-forecast-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
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
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/airqo-ugandan-air-quality-forecast-challenge
source_row: 916
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: the proposed fast reject (SEL-10) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`Time-series (Forecasting)`, SEL-10): AirQo's 2020 Zindi challenge asks for the PM2.5 level 24 hours after a 5-day window of hourly readings, a future value of the series at five Kampala sites.
- Source: Zindi competition by AirQo (Makerere University) with the ASAP project (University of Birmingham), 2020-03-14 to 2020-05-31 ($5,000, 917 participants); as published: Train/Test as CSV and pickles, each row a sensor's 121-hour series of weather readings (temp, precip, wind_dir, wind_spd, atmos_press) and the PM2.5 target, with site metadata (airqo_metadata.csv: altitude, parish area, aspect, road distances); no dates or times.
- Source's words: "The objective of this challenge is to accurately forecast air quality (as measured by PM2.5 µ/m3) for each hour of the coming 25 hours across five locations in Kampala Uganda" and "predict the air quality level at exactly 24 hours after a 5-day series of hourly weather data readings".
- Doubt to record: the inputs are weather series, not past PM2.5 ("you may be given weather indicators (but no air quality data)"), so a TP-10 reading is possible, but the task is a fixed-horizon forecast of a series by its own words, and the rows are series windows, not a table (SEL-10, SEL-12).
- Siblings: the other AirQo records (calibration TBD -> Yes; African prediction TBD -> Yes).
- Metric: RMSE (Zindi evaluation page).
- Reject check (AI, 2026-10-22): does not stand. SEL-10 holds only if the task is a future value of the target's own series, and the source contradicts itself on that. The Data page: "predict the air quality level at exactly 24 hours after a 5-day series of hourly weather data readings ... you may be given weather indicators (but no air quality data) ... you are not given the date or time". So each row is a fixed window of exogenous weather plus static site features, with no lagged target. Zindi data_type is ["Structured","Tabular"]. This is the TP-10 case of SEL-11, and it needs the data to decide. https://zindi.africa/competitions/airqo-ugandan-air-quality-forecast-challenge
- For /add-dataset: TBD -> 2nd Tier, priority 2. The add stage must: (1) open Train.csv/Train.p and check whether the 121-hour windows hold past PM2.5. If they do, the verdict is No with SEL-10. (2) Run TP-10: a model on the weather and site features against each site's naive PM2.5 profile, and check whether the top solutions used any lagged target. (3) Check SEL-12: tabular aggregates of the windows against a sequence model. (4) Check splits: there are no timestamps (SPLIT-7/SPLIT-8), and overlapping windows from one sensor leak across a random split.

Zindi AirQo Ugandan air-quality FORECAST challenge: the task is to forecast future PM2.5/air-quality values over a horizon. Forecasting future values is explicitly excluded from the benchmark scope. The 'forecast' in the name is the decisive signal. A human could double-check whether any framing reduces it to a fixed predictive task, but as posed it is time-series forecasting and should be excluded.
