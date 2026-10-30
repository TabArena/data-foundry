---
unique_name: 2024_lusaka_mobility_prediction_hackathon
name: 2024-lusaka-mobility-prediction-hackathon
checked_by:
- Myunghwan
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.world/competitions/2024-lusaka-mobility-prediction-hackathon
- https://zindi.world/competitions/2024-lusaka-mobility-prediction-hackathon/data
- https://api.zindi.world/v1/competitions/2024-lusaka-mobility-prediction-hackathon
- https://github.com/Mwandamena/yango-hackathon/tree/2fa7817be0740ea1739143ea6e61a28d6cf1462d/data
v2_path: datasets/_dev/tabarena-v0pt2/2024_lusaka_mobility_prediction_hackathon/dataset.py
source_row: 934
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-10-29, Myunghwan): Include the trip-start ride-time task with the accepted approximate endpoint/weather inputs. Preserve the supplied aligned trip/weather calendar and the identified participant copy. The source year remains 2024; no calendar correction is inferred.

**Assessment (AI, 2026-10-29):** One row is a labeled trip. Predict actual duration in minutes using trip start, four endpoint coordinates, straight-line distance and three preceding-hour weather fields. Actual traveled distance and identifiers are excluded. After dropping 21 missing start times, 112,739 rows remain. Keep positive durations and zero straight-line distances without unsupported trimming.

The pinned participant copy identifies this exact Yango/Zindi Lusaka challenge. Its trip timestamps run through January 2023 and early February, while the competition describes January 2024; weather and the inspected participant starter also identify January 2023. Preserve the supplied calendar, first-source year 2024 and the pinned public mirror. Train, Test, weather and sample-submission byte lengths match the organizer's listing; dictionary and starter lengths differ. Organizer-original byte equality and the reason for the calendar discrepancy remain unverified.

At trip start, recorded destination and straight-line distance stand in for the requested destination; capture timing is unverified. Weather uses floor(trip_start) minus one hour, without future fill or year/timezone shifting: 112,716 rides have exact preceding-hour matches, and 23 out-of-coverage rides retain missing weather. Earlier-hour measurement does not establish publication latency. These limitations were explicitly accepted as an approximation, not certified as prospectively available facts.

Use the competition's RMSE on actual minutes with identity target transform. Three chronological four-day test windows have a one-day training gap. All observed durations are below one day, so observed training trip ends precede refit; additional reporting delay and cohort-extraction maturity remain unknown. The final test includes a partial final day. This same-release city/month task does not establish all-season or other-city generalization. Source reuse restrictions remain separate from scientific acceptance.

The current measured findings and accepted task above supersede the source-only counts and provisional framing in the historical screening notes below. Priority 3 is retained for the traceable source and specified ride-time use case; approximate timing and source/calendar limits remain explicit.

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
