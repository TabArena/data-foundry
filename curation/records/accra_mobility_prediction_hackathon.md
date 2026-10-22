---
unique_name: accra_mobility_prediction_hackathon
name: accra-mobility-prediction-hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Time-series (Forecasting)
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
- https://zindi.africa/competitions/accra-mobility-prediction-hackathon
- https://zindi.africa/competitions/accra-mobility-prediction-hackathon/data
source_row: 937
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: average road-segment speeds per weekday time slot from Yango's track logs; a spatio-temporal speed panel, so forecasting-like (SEL-11, TP-10 decide), but no clear SEL-10 failure from the page.
- Source: Zindi one-day hackathon "Accra Mobility Prediction Hackathon Powered" by Yango, 23 Nov 2024 (https://zindi.africa/competitions/accra-mobility-prediction-hackathon, read through Zindi's page API); as published: "aggregated statistics on the numbers of cars and speed of travel along Accra's main highways" from "track logs of transportation service providers (Yango partners) in September 2024"; two tables: statistics per time interval and `persistent_id` (a road section), and a road graph (geometry, name); Train.csv 37.1 MB, Test.csv 17.5 MB, Graph.csv 0.9 MB. A test ID reads `5405080210124813414_X_second_weekday_X_evening_rush_hour`: a road section x weekday x time slot.
- Use case: "Knowing the average traffic speeds helps in finding the quickest and most reliable routes. It also allows partners' drivers and Yango to provide accurate estimated time of arrival (ETA)" (Description); fit approximate: a router has measured speeds from the logs, so the task fills in sections and slots; regime unclear (grouped by road section, or a panel over slots; how Zindi chose the test rows is not stated).
- Siblings and duplicates: not a duplicate of `2025_accra_mobility_prediction_hackathon_powered` (per-trip ride times), as the old note guessed. The same road-speed format: practice-challenge-lusaka (Sept 2023, labelled "Forecast" on Zindi) and the Lusaka 2023, Luanda, Maputo and Kinshasa hackathons in `mobility_prediction` (`TBD -> 2nd Tier`): keep at most one of the family.
- Papers and pages: no paper; the competition's tabs; no public solution found.
- Metric: RMSE ("The evaluation metric for this competition is Root Mean Squared Error", Evaluation tab); MET-4; inputs none.
- Risks for /add-dataset: forecasting-like panel: a model must beat each section's own speed profile (TP-10) and the speed counts of the same slot may give the target away (LEAK); the join to Graph.csv; the target's time grain (15-minute IDs in the description, named periods in the test IDs); access: login, open only to residents of Ghana (no criterion, EV-4).
- Priority: gap 0, use case 0 (approximate), source 0, shape + (a large panel with a road graph), risk - (forecasting-like panel, join).

Another Zindi mobility-prediction hackathon for Accra with no descriptive content in the record (likely a duplicate/earlier instance of the 2025 Accra Yango challenge). Mobility-prediction tasks generally forecast transport demand over space and time, which is excluded forecasting. The record gives nothing to confirm the target. A human should check for duplication with the 2025 Accra entry and verify the exact task; as it stands it is rejected.
