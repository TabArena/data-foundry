---
unique_name: traffic_jam_predicting_peoples_movement_into_nairobi
name: traffic-jam-predicting-peoples-movement-into-nairobi
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2018'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/traffic-jam-predicting-peoples-movement-into-nairobi/data
- https://zindi.africa/competitions/traffic-jam-predicting-peoples-movement-into-nairobi
source_row: 922
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: tickets sold per scheduled bus ride into Nairobi, a real operator task, but the inputs only index the route, date and time, so it is a forecasting-like demand panel that TP-10 has to clear.
- Source: Zindi competition "Traffic Jam: Predicting People's Movement into Nairobi" (2018-09-06 to 2019-01-14, 1,517 participants), sponsored by Uber, Mobiticket and insight2impact; the data is Mobiticket's ticket sales (read through the Zindi API, `api.zindi.africa/v1/competitions/traffic-jam-predicting-peoples-movement-into-nairobi`). As published: one row per ticket for 14 routes "between 17 October 2017 and 20 April 2018" with `ride_id`, `seat_number`, `payment_method`, `payment_receipt`, `travel_date`, `travel_time`, `travel_from`, `travel_to`, `car_type`, `max_capacity` (train zip 0.68 MB); the target `number_of_ticket` per `ride_id` has to be counted from the ticket rows; the test file holds the rides of the following weeks without the ticket columns. Uber Movement hourly travel times were an allowed external source (the platform has since closed). Rows and rides not counted here.
- Use case: Mobiticket and the bus operators, before a scheduled departure, decide on vehicles and promotions ("anticipate customer demand for certain rides, to manage resources and vehicles more efficiently"); fit direct for the count per ride. Regime temporal: the test is the period after the training window, and demand per route and slot drifts.
- Siblings and duplicates: `total_energies_revolution_hackathon` (2023 qualifier) re-runs this same task on the same Mobiticket files (proposed as its duplicate in this batch); the Yango mobility hackathons (`2024_lusaka_mobility_prediction_hackathon` and others) are other data. External collections: none found.
- Papers and pages: the Zindi pages; a public tutorial blog by Johnowhitaker linked from the data page; no paper.
- Metric: MAE on `number_of_ticket` per ride (Zindi Evaluation page: "The Mean Absolute Error will be used"), a competition's deliberate choice (MET-4); inputs none.
- Risks for /add-dataset: the target is built by counting ticket rows (rides with zero sales are absent from train, USE-7); the features are route, departure date and time, vehicle type and capacity only, so it is demand per series slot (SEL-10 against SEL-11): run TP-10 (a per-route-and-slot naive profile against a model) before shipping; `payment_method`, `seat_number` and `payment_receipt` are per-ticket and not known before sales (LEAK checks).
- Priority: gap 0 (transport demand, temporal regime not thin), use case + (operator and decision named by the source), source + (company data, variables documented on the competition page), shape 0 (some thousands of rides but five features that only index the series), risk - (forecasting-like, SEL-10 / TP-10).

A well-known Zindi 'Traffic Jam: Predicting People's Movement into Nairobi' challenge, where the task is to predict the number of seats/tickets sold for bus rides into Nairobi from route and time features. This is a concrete tabular regression with a clear count target, plausibly fitting the benchmark scope, with a temporal structure (ride dates) suggesting a temporal split. A human should confirm the exact target (seats sold per ride), the modality is tabular, dataset size, and the correct split regime. Provisionally a plausible Yes.
