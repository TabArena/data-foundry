---
unique_name: chicago_traffic_crashes
name: Chicago Traffic Crashes - Crashes (CPD E-Crash)
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

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: Chicago Police crash reports (E-Crash) on the city portal, 1.1M crashes with the officer's injury classification, a thin domain; the target is ours to pick and many fields are recorded after the crash.
- Source: City of Chicago Data Portal, "Traffic Crashes - Crashes" (85ca-t3if), published by the City of Chicago, portal entry created 2017-10: "Data are shown as is from the electronic crash reporting system (E-Crash) at CPD"; "citywide data are not available until September 2017"; "About half of all crash reports, mostly minor crashes, are self-reported at the police district"; fields follow the IDOT Traffic Crash Report SR1050 (manual linked from the page). As published: one table, one row per crash, API count on 2026-10-22: 1,106,184 rows; sibling tables Vehicles and People join on CRASH_RECORD_ID. Targets on offer: MOST_SEVERE_INJURY ("Most severe injury sustained by any person involved in the crash") or CRASH_TYPE ("Injury and/or Tow Due to Crash or No Injury / Drive Away").
- Use case: no actor named by the source; the closest decision is dispatch or triage from the reported scene (location, time, road, weather, first crash type), or a city safety team prioritising locations; fit approximate. Regime temporal (SPLIT-6): yearly drift and the 2017 citywide roll-out break.
- Siblings and duplicates: `nyc_motor_vehicle_collisions` (AI `TBD -> Yes`, priority 3, same family), `nhtsa_crss_crash_severity` (AI `TBD -> Yes`, national sample), `us_accidents` (Lennart `No`: its Severity is a traffic-delay code; this record was opened as its injury counterpart). No duplicate found. External collections: none found.
- Papers and pages: the portal page and the SR1050 manual; Kaggle copies and notebooks, no competition or paper that defines a task.
- Metric: none found (the portal page, the SR1050 manual, no competition, no defining paper), so the fallback (`roc_auc` for injury vs none, `log_loss` for the injury classes) (MET-1, MET-8, MET-11).
- Risks for /add-dataset: INJURIES_*, DAMAGE, CRASH_TYPE (when the injury is the target), REPORT_TYPE, DATE_POLICE_NOTIFIED, PHOTOS_TAKEN_I, STATEMENTS_TAKEN_I are recorded after the crash and may encode the outcome (LEAK-10); PRIM/SEC_CONTRIBUTORY_CAUSE are the officer's judgement after the fact; self-reported desk reports are mostly minor crashes, so REPORT_TYPE nearly gives the class; records are amended later; pick one target and one regime (USE-5, SPLIT-6).
- Priority: gap + (social science thin, as for `nyc_motor_vehicle_collisions`), use case 0 (no actor named by the source), source + (the City documents the table and the form), shape + (1.1M rows, mixed categorical and numeric, temporal), risk - (post-crash fields, target to choose).

Chicago Data Portal, Chicago Police Department E-Crash system: "Data are shown as is from the electronic crash reporting system (E-Crash) at CPD, excluding any personally identifiable information"; citywide from September 2017, some districts from 2015. Socrata API on 2026-09-23: 1,096,581 crashes, 2013-03 to 2026-09-22. MOST_SEVERE_INJURY: no indication 935,239; nonincapacitating 88,254; reported not evident 51,886; incapacitating 17,675; fatal 1,142; missing 2,385. CRASH_TYPE: "INJURY AND / OR TOW DUE TO CRASH" 297,837 vs "NO INJURY / DRIVE AWAY" 798,744. Rich scene descriptors: posted speed limit, traffic control device, weather, lighting, first crash type, trafficway type, road surface, road defect, primary/secondary contributory cause, lat/lon, hit-and-run, intersection flag.

Task: MOST_SEVERE_INJURY (5 classes, heavy imbalance; collapse to injury vs none, 15%) or CRASH_TYPE (27% positive, but it mixes injury with tow-away). Drop outcome fields: DAMAGE, INJURIES_*, CRASH_TYPE when MOST_SEVERE_INJURY is the target, and the report/date-police-notified stamps. Best documented of the city registers; sibling Vehicles / People tables exist for a join. Temporal split, with the 2017 citywide roll-out as a reporting break. Data inspected only through API aggregates.

Opened 2026-09-23 as the injury-severity counterpart to `us_accidents` (rejected: its Severity is a traffic-delay code). Police crash reports carry the injury outcome the first-responder / crash-severity use case needs; the target is the standard one in road-safety research, unlike the gender target that sank `road_safety`.

## Reference

City of Chicago Data Portal, Traffic Crashes - Crashes, dataset 85ca-t3if.
