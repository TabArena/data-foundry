---
unique_name: uber_nairobi_ambulance_perambulation_challenge
name: uber-nairobi-ambulance-perambulation-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
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
- https://zindi.africa/competitions/uber-nairobi-ambulance-perambulation-challenge/data
source_row: 920
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target  / Scientific Discovery`, SEL-3; `Time-series (Forecasting)`, SEL-10): the task is a placement schedule for six ambulances, scored by the distance to future crashes, and the data is a list of crash times and coordinates with no target.
- Source: Zindi "Uber Nairobi Ambulance Perambulation Challenge" (2020-09-17 to 2021-01-24, 1,097 participants), crash data of the World Bank DIME team and Flare, read through the Zindi API. As published: `Train.csv`, "time and location for 6318 crashes in the training period (2018-01-01 to 2019-06-30)" (`Uid`, `Datetime`, `Latitude`, `Longitude`), daily GFS weather, a road-segment survey with obfuscated columns, segment geometries; Uber Movement speeds allowed.
- Use case: Flare dispatch positions ambulances ahead of crashes; the source frames it as an optimisation: "Instead of predicting crash locations or frequency, you must instead submit a location schedule for six ambulances every 3 hours over the test period". A curated crash-count-per-cell target would be ours and would be a forecast of a spatio-temporal event series over the test half-year (SEL-10).
- Siblings and duplicates: `uber_movement_sanral_cape_town_challenge` (Cape Town incidents, proposed `No` with SEL-10 in this batch); no duplicate.
- Metric: the summed distance from each test crash to the nearest scheduled ambulance (Zindi Evaluation page; metric id `uber_ambulance`), a score of a placement, not of a prediction per row.
- Reject check (AI, 2026-10-22): stands. SEL-3 (Must): the source's own Evaluation page rules out a predictive task: "Instead of predicting crash locations or frequency, you must instead submit a location schedule for six ambulances every 3 hours over the test period", scored by the summed distance to the nearest ambulance (api.zindi.world/v1/competitions/uber-nairobi-ambulance-perambulation-challenge). Train.csv is only Uid, Datetime, Latitude, Longitude of 6,318 crashes, so any classification or regression target would be ours. Unlike the Cape Town sibling, the source publishes no per-row target or metric.

A Zindi challenge to optimally place ambulances in Nairobi by predicting where/when road traffic crashes will occur, using Uber Movement and crash data. The objective is spatio-temporal crash forecasting / facility placement over future periods, not a fixed IID/grouped tabular classification or regression task, so it falls under time-series forecasting and out of scope. A human could double-check, but the forecasting framing supports a No.
