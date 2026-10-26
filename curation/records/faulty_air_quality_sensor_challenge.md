---
unique_name: faulty_air_quality_sensor_challenge
name: Faulty Air Quality Sensor Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: industry & manufacturing
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/umojahack-africa-2022-beginner-challenge/data
source_row: 1009
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: AirQo names the actor and decision (flag a faulty device for repair), 400k readings, but how the fault label was made is not documented.
- Source: Zindi "UmojaHack Africa 2022: Faulty Air Quality Sensor Challenge (BEGINNER)", 2022-03-19 to 03-20, 719 participants, data from AirQo (Makerere University) low-cost PM sensors deployed across Uganda. As published: train "approximately 300 000 readings", test "approximately 100 000", with missing values; target an offset fault per reading (0/1; the Data page says "multi-class", the Description and the submission format say binary); one table each.
- Use case: the source states it: "The model can be used by AirQo to automatically flag a device that is returning faulty data", "faulty devices need to be identified, isolated and fixed or replaced". Fit direct. Regime likely temporal or grouped by device ("identify a device has an off set fault or not, regardless of the device"): readings are time-stamped per device, so an IID split of readings would share a device's fault episode across folds; to be settled on the columns.
- Siblings and duplicates: other AirQo records (`airqo_african_air_quality_prediction_challenge`, `airqo_low_cost_air_quality_monitor_calibration_challenge`, `airqo_ugandan_air_quality_forecast_challenge`) are different tasks on AirQo data (prediction, calibration, forecasting), not duplicates. Same event, other tasks: `african_snake_antivenom_binding_challenge`, `monthly_insurance_claim_prediction_challenge`. External collections: none found.
- Papers and pages: Zindi description, evaluation and data pages (read through the Zindi API); no paper or codebook for this data found; column names not confirmed (no public notebook found).
- Metric: Zindi's Evaluation page: "The error metric for this competition is Accuracy" (API `straight_accuracy`); a leaderboard metric on hard labels (MET-4), kept; inputs none.
- Risks for /add-dataset: how the offset fault was labelled (an injected offset, or a rule on the difference between a device's two PM sensors, would make it `Trivial` or `AHDS`, SEL-5, SEL-16); whether a device ID and timestamp ship, for the split (SPLIT); time-series classification of a signal (SEL-12) if the task needs windows; Zindi login needed.
- Priority: gap 0 (industry not thin; environment not thin), use case + (AirQo names the decision), source 0 (no documentation of the data beyond the page), shape + (400k rows, temporal structure), risk - (label origin unknown).

Zindi UmojaHack 2022 beginner challenge: classify whether an air-quality sensor/device is faulty from its output data. This is a plausible real-world binary classification task in the industry/IoT domain. The key risk is that the sensor outputs are time-stamped readings, which could make this a per-device grouped or temporal problem (or even a time-series classification) rather than IID, and beginner-track data may be small. A human must inspect the data to confirm the feature structure, target balance, dataset size, and whether a grouped/temporal split is required.

---

Classify if a device is faulty based on its output data
