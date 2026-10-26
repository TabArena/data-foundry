---
unique_name: 2024_lusaka_mobility_prediction_hackathon
name: 2024-lusaka-mobility-prediction-hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/2024-lusaka-mobility-prediction-hackathon/data
- https://zindi.africa/competitions/2024-lusaka-mobility-prediction-hackathon
- '# a different Yango dataset (average road speeds, Sept 2023), not this task''s data'
- https://zindi.africa/competitions/practice-challenge-lusaka/data
source_row: 934
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: a per-trip ride-time regression (Yango's ETA), not demand forecasting; the competition page refutes the old `No` with `Time-series (Forecasting)` and `Missing source information`.
- Source: Zindi one-day hackathon "2024 Lusaka Mobility Prediction Hackathon Powered" by Yango, 26 Oct 2024 (https://zindi.africa/competitions/2024-lusaka-mobility-prediction-hackathon, read through Zindi's page API); as published: "a sampled dataset of trips ordered via the Yango App from January 2024 in Lusaka": Train.csv (15.6 MB, with the target), Test.csv (6.4 MB, no target), Lusaka_weather.csv (49 KB, joined by time), VariableDefinitions.csv. Coordinates geomasked "by at least X meters and no more than Y meters in a random direction"; "The straight-line distance is calculated based on the original points"; "excessively short trips" removed. Rows and columns not counted (the files need a login).
- Use case: "Yango uses a wide range of data in order to predict travel and arrival times of its partners' drivers and vehicles" (Description): the platform quotes a ride time when a trip is ordered; fit direct if every column is known at ordering; regime temporal (one month of trips; quoting future trips), as for `nyc_taxi_trip_duration`.
- Siblings and duplicates: the same Yango task in other cities: `2025_accra_mobility_prediction_hackathon_powered` (Jan 2025, Train.csv 7.9 MB) and `2025_maputo_mobility_prediction_hackathon_powered_by_yango` (2024 trips, 9.0 MB), plus a 2026 Yaounde edition without a record: different data, the same task and publisher, so take one city (this one has the largest train file). The road-speed hackathons (`accra_mobility_prediction_hackathon`, practice-challenge-lusaka, the cities in `mobility_prediction`) are another task. Ride-time precedents: `nyc_taxi_trip_duration` and `pkdd_15_taxi_trip_time_prediction_ii` (`Yes`), `maps_router_eta` (`Yes`, TabReD), `yassir_eta_prediction_challenge` (`TBD -> Yes`). External collections: none found.
- Papers and pages: no paper; the competition's Description, Data and Evaluation tabs; no public solution or column list found (web search 2026-10-22).
- Metric: RMSE on the ride time ("The evaluation metric for this competition is Root Mean Squared Error", Evaluation tab); a competition's leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the column list is unread: check that no column is known only after the trip (driven distance, drop-off time) (LEAK); the target's unit; only Train.csv is labelled; the second link (practice-challenge-lusaka) is a different dataset (road speeds, Sept 2023); access: login, and the competition "is only open to Zambian users residing in Zambia" (no criterion, EV-4).
- Priority: gap 0 (technology & internet, regression and temporal are not thin), use case + (Yango's ETA, named by the source), source 0 (a competition page, no codebook read), shape + (a month of trips with time and weather), risk 0.

A Zindi 'mobility prediction' hackathon for Lusaka with no comments in the record. Mobility-prediction challenges (often ride-hailing/transport demand) typically forecast trips/demand over space and time, which is excluded forecasting rather than a fixed IID/temporal-split tabular task. The record carries essentially no descriptive content, so the verdict is unverified. A human must confirm the exact target and whether it is a one-shot prediction or a multi-step forecast; if it is genuine forecasting it stays No, but if it is a fixed per-trip prediction it could be revisited.
