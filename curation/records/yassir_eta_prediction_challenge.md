---
unique_name: yassir_eta_prediction_challenge
name: Yassir ETA Prediction Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2020'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/umojahack-south-africa-yassir-eta-prediction-challenge
- '# the sister hackathon on the same day with the same data (Algeria; Zindi API, no parent)'
- https://zindi.africa/competitions/umojahack-algeria-yassir-eta-prediction-challenge
source_row: 1026
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: Yassir's trip-time (ETA) regression from origin, destination, route distance and time, with a date split; a clear ride-hailing quote task.
- Source: Zindi one-day hackathons "UmojaHack South Africa: Yassir ETA Prediction Challenge" and "UmojaHack Algeria: Yassir ETA Prediction Challenge", both 2020-07-25 (https://zindi.africa/competitions/umojahack-south-africa-yassir-eta-prediction-challenge, https://zindi.africa/competitions/umojahack-algeria-yassir-eta-prediction-challenge, read through Zindi's page API); as published: "details for 119,549 trips (train and test are split by date)"; columns `ID`, `Timestamp` ("Time that the trip was started"), `Origin_lat`, `Origin_lon`, `Destination_lat`, `Destination_lon` ("to within approximately 100m"), `Trip_distance` ("Distance in meters on a driving route"), target `ETA` ("Estimated trip time in seconds"); `Weather.csv` with daily ERA5 temperature, rainfall and wind, joined by date.
- Use case: "predict the estimated time of arrival at the dropoff point for a single Yassir journey" to make "Yassir's services more reliable": the app quotes a trip time when a ride is booked; fit direct (every column is known at booking); regime temporal (the source splits by date; quoting future trips).
- Siblings and duplicates: `yassir_eta_prediction_challenge_for_azubian` is a knowledge rerun of the Algeria hackathon (API parent `umojahack-algeria-yassir-eta-prediction-challenge`, the same Data Description), so a duplicate of this record (proposed `No` in the same batch); the Yango ride-time hackathons (`2024_lusaka_mobility_prediction_hackathon` and its Accra and Maputo siblings) are other cities and another company; ride-time precedents `nyc_taxi_trip_duration`, `pkdd_15_taxi_trip_time_prediction_ii`, `maps_router_eta` (TabReD). External collections: none found.
- Papers and pages: the two competition pages; no paper.
- Metric: RMSE on `ETA` in seconds ("The error metric for this competition is the Root Mean Squared Error", Evaluation tab), a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the target is named "Estimated trip time": check whether it is the realised duration or Yassir's routing estimate (USE, an unclear target); `Trip_distance` is "along the fastest route", known at booking, fine; few features (6 plus daily weather), so a check against a distance-only baseline (TP-4); only Train.csv is labelled.
- Priority: gap 0 (technology & internet, regression, temporal not thin), use case + (Yassir and the ETA quote named), source + (the page documents every column), shape + (about 120k trips, coordinates, time, a weather join), risk - (the target's meaning to confirm).

Yassir ETA prediction (Zindi/UmojaHack) is a ride-hailing estimated-time-of-arrival regression: trip-level features (origin/destination, distance, time of day, etc.) map to trip duration. This is a representative real-world tabular regression with a clear continuous target, not forecasting a future-value series. A temporal split is likely appropriate given trips occur over time. A human must verify dataset size, feature columns, and that geospatial coordinates do not constitute the dominant signal; provisionally Yes.

---

Predict the estimated time of arrival for Algerian ride-hailing business Yassir
