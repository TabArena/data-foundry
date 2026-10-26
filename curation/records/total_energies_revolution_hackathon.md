---
unique_name: total_energies_revolution_hackathon
name: total-energies-revolution-hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: TBD
source_links:
- https://zindi.africa/competitions/total-energies-revolution-hackathon/data
- https://zindi.africa/competitions/total-energies-revolution-hackathon-finals
source_row: 872
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): the TotalEnergies qualifier (Uganda, 2023) re-runs the Mobiticket "Traffic Jam" task of 2018 on the same ticket data with the same metric; the finals have no data.
- Source: Zindi "TotalEnergies rEVolution Hackathon" (2023-07-25 to 2023-08-25, a qualifier for Ugandan teams, 405 participants) and its finals (2023-09-18 to 20, 61 participants), read through the Zindi API. The finals' brief is EV charging locations in Kampala, judged by a panel ("there are no leaderboard scores"), with a 433-byte zip as the only file. The qualifier's own text is the Nairobi one: "predicts the number of seats that Mobiticket can expect to sell for each ride", Train.csv "tickets purchased from Mobiticket for the 14 routes ... between 17 October 2017 and 20 April 2018" with `ride_id`, `seat_number`, `payment_method`, `payment_receipt`, `travel_date`, `travel_time`, `travel_from`, `travel_to`, `car_type`, `max_capacity`; Test.csv the rides of 21 April to 9 May 2018; MAE on `number_of_ticket`.
- Use case and regime: those of `traffic_jam_predicting_peoples_movement_into_nairobi` (Mobiticket demand per ride, temporal).
- Siblings and duplicates: the original is `traffic_jam_predicting_peoples_movement_into_nairobi` (Zindi 2018, the same company data, task, columns, date range and metric; screened `TBD -> 2nd Tier` in this batch). No distinct task (PROV-6, PROV-7 does not apply).
- Metric: MAE (the qualifier's Evaluation page), the same as the original.
- The old `Missing source information` marker is refuted: the source is the 2018 Mobiticket release. `domain` `Other` and the energy reading came from the title only.
- Reject check (AI, 2026-10-22): stands. PROV-4 (Must): the qualifier's Data Description and Evaluation pages are word for word those of traffic-jam-predicting-peoples-movement-into-nairobi (Zindi 2018): "This challenge asks you to build a model that predicts the number of seats that Mobiticket can expect to sell for each ride ... There are 14 routes"; "The Mean Absolute Error will be used", submission ride_id,number_of_ticket (api.zindi.world/v1/competitions/total-energies-revolution-hackathon vs .../traffic-jam-predicting-peoples-movement-into-nairobi). Same source, same task, so no distinct task (PROV-7 does not apply); the EV-charging finals are judged by a panel with no data.

A Zindi 'Total Energies Revolution Hackathon' (with a finals stage) tagged Non-IID (Temporal) but otherwise with no description in the record. The energy domain plus the temporal tag raise a real risk that this is a forecasting task, which would be out of scope, but it could also be a fixed-target predictive problem needing a temporal split. There is too little information to decide the target, modality, or whether it is forecasting. A human must inspect the Zindi pages to determine the actual task before deciding.
