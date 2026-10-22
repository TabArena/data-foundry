---
unique_name: 2025_maputo_mobility_prediction_hackathon_powered_by_yango
name: 2025-maputo-mobility-prediction-hackathon-powered-by-yango
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2025'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/2025-maputo-mobility-prediction-hackathon-powered-by-yango/data
- https://zindi.africa/competitions/2025-maputo-mobility-prediction-hackathon-powered-by-yango
source_row: 949
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a per-trip ride-time regression (Yango's ETA), not forecasting; the same task as `2024_lusaka_mobility_prediction_hackathon` in another city.
- Source: Zindi one-day hackathon "2025 Maputo Mobility Prediction Hackathon Powered" by Yango, 11 Oct 2025 (https://zindi.africa/competitions/2025-maputo-mobility-prediction-hackathon-powered-by-yango, read through Zindi's page API); as published: "a sampled dataset of trips via the Yango platform from March 2024 in Maputo" (Description), but "from April 2024 in Mozambique" (Data tab, which ends in a stray "xxx"): the month is to check. Train.csv (9.0 MB, with the target), Test.csv (3.7 MB), Maputo_weather.csv, VariableDefinitions.csv; coordinates geomasked, straight-line distance from the original points, short trips removed. Rows and columns not counted (login).
- Use case: "Yango uses a wide range of data in order to predict travel and arrival times" (Description): a ride time quoted at ordering; fit direct if every column is known then; regime temporal (one month of trips).
- Siblings and duplicates: `2024_lusaka_mobility_prediction_hackathon` (15.6 MB) and `2025_accra_mobility_prediction_hackathon_powered` are the same task and publisher on other cities' data: one city is enough. An older Maputo hackathon (maputo-mobility-prediction-hackathon, listed in `mobility_prediction`) is the road-speed task. Precedents: `nyc_taxi_trip_duration`, `pkdd_15_taxi_trip_time_prediction_ii`, `maps_router_eta` (`Yes`).
- Papers and pages: no paper; the competition's tabs; no public solution found.
- Metric: RMSE ("The evaluation metric for this competition is Root Mean Squared Error", Evaluation tab); MET-4; inputs none.
- Risks for /add-dataset: the column list is unread (post-trip columns, LEAK); the data month (March or April 2024); access: login, "only open to Mozambique users residing in Mozambique" (no criterion, EV-4).
- Priority: gap 0, use case + (Yango's ETA), source 0 (the page contradicts itself on the month), shape + (a month of trips with time and weather), risk - (a sibling of the Lusaka task; keep one city).

Zindi mobility-prediction hackathon for Maputo, explicitly powered by Yango (a ride-hailing platform), so the task is almost certainly ride/trip demand forecasting. That is excluded forecasting and operations/RecSys-adjacent rather than a fixed tabular classification/regression task. The record contains no descriptive content. A human must verify the actual target and split regime before any reconsideration.
