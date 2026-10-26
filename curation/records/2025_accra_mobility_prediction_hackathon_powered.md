---
unique_name: 2025_accra_mobility_prediction_hackathon_powered
name: 2025-accra-mobility-prediction-hackathon-powered
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
- https://zindi.africa/competitions/2025-accra-mobility-prediction-hackathon-powered/data
- https://zindi.africa/competitions/2025-accra-mobility-prediction-hackathon-powered
source_row: 946
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a per-trip ride-time regression (Yango's ETA), not forecasting; the same task as `2024_lusaka_mobility_prediction_hackathon` in another city, with a smaller train file.
- Source: Zindi one-day hackathon "2025 Accra Mobility Prediction Hackathon Powered" by Yango, 5 Jul 2025 (https://zindi.africa/competitions/2025-accra-mobility-prediction-hackathon-powered, read through Zindi's page API); as published: "a sampled dataset of trips ordered via the Yango App from January 2025 in Ghana": Train.csv (7.9 MB, with the target), Test.csv (3.3 MB), Accra_weather.csv, VariableDefinitions.csv; coordinates geomasked, straight-line distance from the original points, "excessively short trips" removed. Rows and columns not counted (login).
- Use case: "Yango uses a wide range of data in order to predict travel and arrival times" (Description): a ride time quoted at ordering; fit direct if every column is known then; regime temporal (one month of trips).
- Siblings and duplicates: `2024_lusaka_mobility_prediction_hackathon` (Jan 2024, 15.6 MB) and `2025_maputo_mobility_prediction_hackathon_powered_by_yango` are the same task and publisher on other cities' data: not copies, but one city is enough (this is the smallest of the three). Not a duplicate of `accra_mobility_prediction_hackathon` (road speeds per segment, Sept 2024), as the old note guessed. Precedents: `nyc_taxi_trip_duration`, `pkdd_15_taxi_trip_time_prediction_ii`, `maps_router_eta` (`Yes`).
- Papers and pages: no paper; the competition's tabs; no public solution found.
- Metric: RMSE ("The evaluation metric for this competition is Root Mean Squared Error", Evaluation tab); MET-4; inputs none.
- Risks for /add-dataset: the column list is unread (post-trip columns, LEAK); the target's unit; access: login, "only open to Ghanaian users residing in Ghana" (no criterion, EV-4).
- Priority: gap 0, use case + (Yango's ETA), source 0, shape + (a month of trips with time and weather), risk - (a sibling of the Lusaka task; keep one city).

Zindi mobility-prediction hackathon for Accra (the Yango-family ride-hailing series). These challenges generally forecast transport demand/mobility over time and space, which falls under excluded time-series forecasting and is RecSys/operations-adjacent. The record has no comments or descriptive fields to confirm the precise target. A human must check whether the task is a fixed predictive label per row (possibly viable) versus a demand-over-horizon forecast (excluded).
