---
unique_name: chicago_traffic_crashes
name: Chicago Traffic Crashes - Crashes (CPD E-Crash)
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
year: '2017'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if
- https://data.cityofchicago.org/resource/85ca-t3if.json
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Chicago Data Portal, Chicago Police Department E-Crash system: "Data are shown as is from the electronic crash reporting system (E-Crash) at CPD, excluding any personally identifiable information"; citywide from September 2017, some districts from 2015. Socrata API on 2026-09-23: 1,096,581 crashes, 2013-03 to 2026-09-22. MOST_SEVERE_INJURY: no indication 935,239; nonincapacitating 88,254; reported not evident 51,886; incapacitating 17,675; fatal 1,142; missing 2,385. CRASH_TYPE: "INJURY AND / OR TOW DUE TO CRASH" 297,837 vs "NO INJURY / DRIVE AWAY" 798,744. Rich scene descriptors: posted speed limit, traffic control device, weather, lighting, first crash type, trafficway type, road surface, road defect, primary/secondary contributory cause, lat/lon, hit-and-run, intersection flag.

Task: MOST_SEVERE_INJURY (5 classes, heavy imbalance; collapse to injury vs none, 15%) or CRASH_TYPE (27% positive, but it mixes injury with tow-away). Drop outcome fields: DAMAGE, INJURIES_*, CRASH_TYPE when MOST_SEVERE_INJURY is the target, and the report/date-police-notified stamps. Best documented of the city registers; sibling Vehicles / People tables exist for a join. Temporal split, with the 2017 citywide roll-out as a reporting break. Data inspected only through API aggregates.

Opened 2026-09-23 as the injury-severity counterpart to `us_accidents` (rejected: its Severity is a traffic-delay code). Police crash reports carry the injury outcome the first-responder / crash-severity use case needs; the target is the standard one in road-safety research, unlike the gender target that sank `road_safety`.

## Reference

City of Chicago Data Portal, Traffic Crashes - Crashes, dataset 85ca-t3if.
