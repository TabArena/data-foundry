---
unique_name: airqo_low_cost_air_quality_monitor_calibration_challenge_2
name: AirQo Low-Cost Air Quality Monitor Calibration Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
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
- https://zindi.africa/competitions/airqo-air-sensor-calibration-challenge/data
source_row: 1021
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): the DataFest Kampala preliminary hackathon (https://zindi.africa/competitions/airqo-air-sensor-calibration-challenge, 2021-04-29 to 2021-04-30, 63 participants) of the same AirQo data as `airqo_low_cost_air_quality_monitor_calibration_challenge` (2021-04-30 to 2021-06-06).
- Source: AirQo (Makerere University) on Zindi; the two pages carry the same description, data description, variable definitions, files (Train.csv, Test.csv, SampleSubmission.csv) and metric (RMSE). The hackathon page: "This is a preliminary hackathon, all participants and the Zindi community are invited to continue with the ongoing competition until 6 June"; the competition page: "This challenge was orignally launch as a hackathon at DataFest Kampala. It is now open to the whole Zindi community."
- Siblings and duplicates: kept as `airqo_low_cost_air_quality_monitor_calibration_challenge` (TBD -> Yes, priority 4), whose record now lists this link too; the hackathon opened a day earlier, so it is the first publication by date (PROV-8), but the competition is the public release of the same data and the record the team will curate.
- Metric: RMSE (Zindi evaluation page), as for the kept record.
- Reject check (AI, 2026-10-22): stands. PROV-4. Same title, files and metric. The Data Description is identical (ratio 1.0, 4,594 chars). The hackathon page: "This is a preliminary hackathon, all participants and the Zindi community are invited to continue with the ongoing competition until 6 June". airqo_low_cost_air_quality_monitor_calibration_challenge (TBD -> Yes) already lists this link. https://zindi.africa/competitions/airqo-air-sensor-calibration-challenge

Zindi AirQo sensor-calibration challenge: learn a regression mapping from low-cost air-quality sensor readings (plus context) to a reference PM2.5 value. This is a genuine real-world tabular regression task (sensor calibration), not a forecast of future values over a horizon, so it is in scope despite 'air quality' often implying time series. Likely needs a temporal split because measurements are collocated time series. A human must verify the feature set is tabular (not raw spectra/time windows), the number of usable rows after cleaning, and that the target is a continuous reference PM2.5.

---

predict pm2_5
