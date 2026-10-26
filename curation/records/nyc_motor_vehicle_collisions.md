---
unique_name: nyc_motor_vehicle_collisions
name: NYC Motor Vehicle Collisions - Crashes (NYPD MV-104AN)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- Larger IID Data
collections:
- New (BeyondArena)
original_source: GOV Website
year: '2012'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95
- https://data.cityofnewyork.us/resource/h9gi-nx95.json
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: NYPD's police crash table on NYC Open Data, 2.27M crashes 2012-2026 with injury counts, a thin domain; few features and post-hoc contributing factors keep it from the top.
- Source: NYPD via NYC Open Data, dataset h9gi-nx95, "Motor Vehicle Collisions - Crashes" (data from 2012-07-01; the page describes TAMS from 1999 and FORMS from March 2016). Page: "The police report (MV104-AN) is required to be filled out for collisions where someone is injured or killed, or where there is at least $1000 worth of damage"; the data "is preliminary and subject to change". As published: one table, one row per crash, 29 columns (date, time, borough, zip, lat/lon, street names, persons/pedestrians/cyclists/motorists injured and killed, contributing factor and vehicle type for up to 5 vehicles, COLLISION_ID); API count on 2026-10-22: 2,269,187 rows, 2012-07-01 to 2026-06-11. Companion tables (Vehicles, Person) exist on the portal and join by COLLISION_ID.
- Use case: no actor named by the source; the page points to Vision Zero safety analysis. Closest decision: dispatch or triage from the reported location, time and vehicles, or a city traffic-safety team prioritising locations; fit approximate. Regime temporal: 14 years, the reporting system changed in 2016 (SPLIT-6).
- Siblings and duplicates: `chicago_traffic_crashes` (AI `TBD -> Yes`, same family), `nhtsa_crss_crash_severity` (AI `TBD -> Yes`, national sample), `us_accidents` (Lennart `No`; this record was opened as its injury counterpart). External collections: none found.
- Papers and pages: the NYC Open Data page and the NYPD MV-104AN form; many Kaggle notebooks, no competition or paper that defines a task.
- Metric: none found (the Open Data page, no competition, no defining paper), so the fallback `roc_auc` for any-injury (MET-1, MET-8, MET-11).
- Risks for /add-dataset: every injured/killed sub-count is the target and must go (LEAK-10); contributing factors are the officer's judgement after the fact, check whether they encode the injury (for example how often "Unspecified" appears for injury crashes); the reporting threshold (injury or $1000 damage) makes the negatives property-damage crashes only; preliminary data that is amended; street names are free text.
- Priority: gap + (social science thin), use case 0 (no actor named by the source), source + (NYPD documents the table), shape + (2.27M rows, categorical mix, temporal), risk - (post-hoc factors, few real features).

NYC Open Data, NYPD: one row per police-reported collision; "The police report (MV104-AN) is required to be filled out for collisions where someone is injured or killed, or where there is at least $1000 worth of damage." Queried via the Socrata API on 2026-09-23: 2,269,187 crashes, 2012-07-01 to 2026-06-11; NUMBER OF PERSONS INJURED = 0 for 1,710,566 rows, >= 1 for ~558k (1: 433,878; 2: 81,463; 3: 26,827); NUMBER OF PERSONS KILLED > 0 in 3,469 crashes. Columns: date, time, borough, zip, lat/lon, on/cross/off street, contributing factor per vehicle (1-5), vehicle type per vehicle (1-5), injured/killed counts split by pedestrians, cyclists, motorists.

Task: any-injury (binary, ~25% positive) or injured-count regression from time, place, vehicle types and contributing factors; the killed count is too rare for a target. Contributing factors are the officer's post-hoc judgement but are scene descriptors, not outcomes; the injured/killed sub-counts are the target and must all be dropped. Reporting practice changes over 14 years -> temporal split. No PII in the crash table. Data inspected only through API aggregates.

Opened 2026-09-23 as the injury-severity counterpart to `us_accidents` (rejected: its Severity is a traffic-delay code). Police crash reports carry the injury outcome the first-responder / crash-severity use case needs; the target is the standard one in road-safety research, unlike the gender target that sank `road_safety`.

## Reference

NYC Open Data / NYPD, Motor Vehicle Collisions - Crashes, dataset h9gi-nx95.
