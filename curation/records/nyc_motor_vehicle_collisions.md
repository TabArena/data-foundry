---
unique_name: nyc_motor_vehicle_collisions
name: NYC Motor Vehicle Collisions - Crashes (NYPD MV-104AN)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
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

NYC Open Data, NYPD: one row per police-reported collision; "The police report (MV104-AN) is required to be filled out for collisions where someone is injured or killed, or where there is at least $1000 worth of damage." Queried via the Socrata API on 2026-09-23: 2,269,187 crashes, 2012-07-01 to 2026-06-11; NUMBER OF PERSONS INJURED = 0 for 1,710,566 rows, >= 1 for ~558k (1: 433,878; 2: 81,463; 3: 26,827); NUMBER OF PERSONS KILLED > 0 in 3,469 crashes. Columns: date, time, borough, zip, lat/lon, on/cross/off street, contributing factor per vehicle (1-5), vehicle type per vehicle (1-5), injured/killed counts split by pedestrians, cyclists, motorists.

Task: any-injury (binary, ~25% positive) or injured-count regression from time, place, vehicle types and contributing factors; the killed count is too rare for a target. Contributing factors are the officer's post-hoc judgement but are scene descriptors, not outcomes; the injured/killed sub-counts are the target and must all be dropped. Reporting practice changes over 14 years -> temporal split. No PII in the crash table. Data inspected only through API aggregates.

Opened 2026-09-23 as the injury-severity counterpart to `us_accidents` (rejected: its Severity is a traffic-delay code). Police crash reports carry the injury outcome the first-responder / crash-severity use case needs; the target is the standard one in road-safety research, unlike the gender target that sank `road_safety`.

## Reference

NYC Open Data / NYPD, Motor Vehicle Collisions - Crashes, dataset h9gi-nx95.
