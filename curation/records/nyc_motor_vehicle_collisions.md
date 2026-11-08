---
unique_name: nyc_motor_vehicle_collisions
name: NYC Motor Vehicle Collisions - Crashes (NYPD MV-104AN)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the task's table has one row per police-reported crash with "anyone injured or killed" as target: 2,303,506 crashes (2012-07-01 to 2026-11-03) with 20 inputs from the report. On 2020-04-06 the NYPD stopped taking reports of crashes with property damage only, so the negative class changes there. Within one era the table has 1,671,845 crashes (before the date) or 631,661 (from it). The call stands at priority 3.
- As published: Socrata dataset h9gi-nx95, "Motor Vehicle Collisions - Crashes" (https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95), "Each row represents a crash event". It has 29 columns: crash_date, crash_time, borough, zip_code, latitude, longitude, location, the on, cross and off street names, persons, pedestrians, cyclists and motorists injured and killed (8 counts), contributing_factor_vehicle_1 to 5, vehicle_type_code 1 to 5 and collision_id. SoQL count on 2026-11-08: 2,303,506 rows, 2012-07-01 to 2026-11-03; the rows were last updated 2026-11-06. Two companion tables join by collision_id and start in April 2016, "when crash reporting switched to an electronic system". Vehicles (bm4k-52h4, 25 columns, about 4.62 million rows by the cached column counts) adds make, model, year, pre-crash action, point of impact, damage, driver sex and licence status. Person (f55k-p6yu, 21 columns, about 6.10 million rows) holds each person's injury. The API metadata names no licence; the portal's terms of use apply.
- The task's table: one row per crash. The target is any injured or killed person (number_of_persons_injured > 0 or number_of_persons_killed > 0): 577,494 positives of 2,303,506 (25.1%) by SoQL counts. number_of_persons_injured is null in 18 rows and number_of_persons_killed in 31. Inputs from the report, 20 columns: crash_date, crash_time, borough, zip_code, latitude, longitude, the three street names, five contributing factors and five vehicle types. location repeats the coordinates, the 8 counts are the target and its parts (LEAK-10), and collision_id is an id. Fill by the cached column counts: borough is null in 674,862 rows, zip_code in 700,147 and the coordinates in 240,756; contributing factors 3 to 5 and vehicle types 3 to 5 are filled in at most 7.3% of the rows. Per year, all crashes and those with an injury or death: 2013 203,742 and 40,273; 2016 229,835 and 44,241; 2019 211,487 and 45,439; 2020 112,923 and 33,363; 2021 110,558 and 38,809; 2023 96,608 and 40,473; 2025 85,559 and 37,426; 2026 to 2026-11-03 70,720 and 31,558. The positive share moves from 17-22% (2013-2019) to 30% (2020), 35% (2021) and 38-45% (2022-2026).
- Access: open, no login, through the SoQL API and the CSV export. A full export is one table of 2.3 million rows by 29 columns; its size was not measured. Grouped counts over the whole table took one to three minutes, and one query returned "Service unavailable".
- Changes the call: the 2020 break. From Monday 2020-04-06, "vehicle collisions resulting only in property damage are not required to be reported to the police" (NYPD, https://www.nyc.gov/site/nypd/news/p0403b/nypd-expanding-successful-non-injury-collision-pilot-save-nypd-resources). Crashes without injury fell from 166,048 in 2019 to 48,133 in 2025, while crashes with injury fell from 45,439 to 37,426. After the date the negatives are the property-damage crashes police still attended, a different population. The task should use one era (SPLIT-6): from 2020-04-06 (631,661 crashes, 252,428 positives, 40.0%), or before it (1,671,845 crashes; of these, 890,938 fall in the electronic era from 2016-04-01). Second, the same task is already accepted from Chicago. `chicago_traffic_crashes` (`Yes`, a v2 folder in the working copy) predicts the police injury level of a reported crash for a city road-safety analyst, from richer crash and road facts. NYC would add a second city with more rows and thinner inputs. Half of its 20 inputs are per-vehicle factor and type slots, and the contributing factors are the officer's judgement: "Unspecified" is factor 1 in about 25% of the injury crashes and about 34% of the others (SoQL counts), a class-dependent recording to probe (LEAK-13). The screening's gap point for social science is weaker now that Chicago is accepted. The factors as written do not count a covered task, so priority 3 stands. The curator may want one police-crash task in the benchmark or both.
- Not checked: the size of a full CSV export; the Vehicles and Person row counts beyond the cached column statistics; how many crashes later amendments change (the data "is preliminary and subject to change").

## Reference

NYC Open Data / NYPD, Motor Vehicle Collisions - Crashes, dataset h9gi-nx95.
