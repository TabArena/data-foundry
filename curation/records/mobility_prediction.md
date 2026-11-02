---
unique_name: mobility_prediction
name: mobility_prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
domain: technology & internet
required_split:
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/lusaka-mobility-prediction-hackathon/data
- https://zindi.africa/competitions/luanda-mobility-prediction-hackathon
- https://zindi.africa/competitions/maputo-mobility-prediction-hackathon
- https://zindi.africa/competitions/kinshasa-mobility-prediction-hackathon
source_row: 953
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: four one-day Yango hackathons (Lusaka, Luanda, Maputo, Kinshasa, Nov to Dec 2023) with one design: average speed per road section and weekday time slot from September 2023 track logs; a speed profile to fill in, tagged "Forecast" by Zindi, and four city copies of one task.
- Source: Zindi, "Lusaka / Luanda / Maputo / Kinshasa Mobility Prediction Hackathon Powered" by Yango, 4 Nov, 25 Nov, 25 Nov and 16 Dec 2023 (the four links in `source_links`, read through Zindi's page API); as published: "aggregated statistics on the numbers of cars and speed of travel along [the city's] main highways" from "the track logs of transportation service providers (Yango partners) in September 2023"; two tables, statistics per time interval and `persistent_id` (a road section), and a road graph (geometry, name); Train.csv, Test.csv, Graph.csv and variable definitions per city. A test ID reads `5405080210124813414_X_second_weekday_X_evening_rush_hour`: road section x weekday x time slot. Rows not counted (login).
- Use case: "Knowing the average traffic speeds helps in finding the quickest and most reliable routes. It also allows drivers and Yango to provide accurate estimated time of arrival (ETA) times" (Description); fit approximate: a router has the measured speeds of the logs, so the task fills in sections and slots of one month rather than predicting ahead. Regime unclear: grouped by road section, or slots of one month; how the test rows were chosen is not stated.
- Siblings and duplicates: `accra_mobility_prediction_hackathon` (the same design for Accra, September 2024; re-screened today as `TBD -> 2nd Tier`, priority 1); the Yango ride-time hackathons `2024_lusaka_mobility_prediction_hackathon`, `2025_accra_mobility_prediction_hackathon_powered`, `2025_maputo_mobility_prediction_hackathon_powered_by_yango` are a different task (per-trip ride time). The four cities here are one task: at most one would ship (PROV-6). External collections: none found.
- Papers and pages: none; Yango starter notebooks per city.
- Metric: RMSE on the average speed ("The evaluation metric for this competition is Root Mean Squared Error", Evaluation tab, same on all four); MET-4; inputs none.
- Risks for /add-dataset: whether it is a forecast of later intervals (SEL-10) or a fill-in of a profile (SEL-11, TP-10 against each section's naive profile); speed statistics of neighbouring slots of the same section in the features; country-restricted hackathons (download is a question for the curator); four copies.
- Markers: `Time-series (Forecasting)` kept as a concern (Zindi's own "Forecast" tag), not a fail: the page asks for a speed per section and slot, not values over a horizon.
- Priority: gap 0 (technology & internet has 5 accepted), use case 0 (named by Yango, fit approximate), source 0 (a hackathon page, no documentation beyond variable definitions), shape 0 (size not counted), risk - (forecasting-like profile, unclear test design, four city copies).

A group of Zindi 'mobility prediction' hackathons across several African cities (Lusaka, Luanda, Maputo, Kinshasa). 'Mobility prediction' over time often implies forecasting movement/flows, which would be out of scope, but it could also be a fixed origin/destination or trip-attribute classification task. The record has no detail, and the multiple linked competitions complicate a single verdict. Because it may be forecasting but might be a valid fixed task, this is TBD -> 2nd Tier. A human must inspect each competition's actual task and target before deciding and avoid double-counting near-duplicate city variants.
