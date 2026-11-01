---
unique_name: stats19_collision_severity
name: 'Road Safety Data (STATS19): reported road casualties Great Britain, collision, vehicle and casualty open data'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.gov.uk/government/statistical-data-sets/road-safety-open-data
- https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the Department for Transport's record of every police-reported injury collision in Great Britain since 1979, one row per collision with the severity of its worst casualty (fatal, serious, slight) and the scene's road, light, weather and junction descriptors; a census with a multiclass target in a thin domain, once DfT's severity-adjustment columns and the change of recording under CRASH are handled.
- Source: Department for Transport, "Road Safety Data" (STATS19 police reports), gov.uk statistical data set and data.gov.uk, Open Government Licence v3.0. As published (gov.uk page, 2026-10-31): "Record level files providing data on personal injury road collisions in Great Britain from 1979", collision, vehicle and casualty files for each year and for 1979 to 2025 (collision file 1.5 GB; 2025 alone 19.3 MB); "The statistics relate only to personal injury collisions on public roads that are reported to the police"; coded values with a data guide (xlsx); "This data contains all the non-sensitive fields that can be made public" (contributory factors only on request). Header of the 2025 collision file (preview): 44 columns, among them `collision_severity`, `number_of_vehicles`, `number_of_casualties`, `date`, `day_of_week`, `time`, location (grid reference, longitude, latitude, LSOA, local authority), `police_force`, road class and number, `road_type`, `speed_limit`, junction detail and control, pedestrian crossing, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `did_police_officer_attend_scene_of_accident`, `trunk_road_flag`, `enhanced_severity_collision`, `collision_injury_based`, `collision_adjusted_severity_serious`, `collision_adjusted_severity_slight`. On the order of 100,000 collisions a year in the 2020s (from the file sizes; not counted).
- Use case: no prediction actor in the source (DfT publishes statistics). The closest decisions: triage when a collision is reported (which response to send, from place, time, road and the number of vehicles), or a highway authority ranking sites by the severity their collisions reach; fit approximate. Regime temporal: yearly releases, coding changes across years and the move of police forces to the injury-based CRASH system ("appears to have led to a change in the reported severity of road casualties", gov.uk page; SPLIT-6).
- Siblings and duplicates: `road_safety` (`No`) and `road_safety_gender` (`No`; Lennart: "Predict sex of drivers in accidents - ethical issues"): OpenML 42803 "road-safety", "Data reported to the police about the circumstances of personal injury road accidents in Great Britain from 1979 ... This version includes data up to 2015", target `Sex_of_Driver`. The same source with another target, so no duplicate (PROV-7), and the ethics reason of that record concerns its sex target, not a severity target. `nhtsa_crss_crash_severity` (AI `TBD -> Yes`, priority 3), `chicago_traffic_crashes` and `nyc_motor_vehicle_collisions` (AI `TBD -> Yes`, priority 3), `fars_person_injury_severity` (AI `TBD -> 2nd Tier`), `us_accidents` (`No`): the same use-case family, and the curator may want one or two of them. External collections: the OpenML sex-of-driver cut is in TabSTAR (per `road_safety_gender`); the severity task: none found.
- Better data: found as better data for `nhtsa_crss_crash_severity`; no further search this round.
- Papers and pages: the gov.uk data set page with the 2025 data guide (xlsx), the severity adjustment guidance (docx) and "Understanding historical road safety data" (docx), not opened; DfT's yearly "Reported road casualties Great Britain" statistics; the independent `stats19` R package the page mentions.
- Metric: none found (the gov.uk page defines statistics, no prediction task), so the fallback `log_loss` for the three classes (MET-1, MET-8); inputs none.
- Risks for /add-dataset: `collision_adjusted_severity_serious` and `collision_adjusted_severity_slight` are DfT's severity adjustments and `enhanced_severity_collision` a re-coding of the severity: drop them (LEAK-10); `collision_injury_based` (recorded under CRASH or not) changes how serious and slight are told apart by force and year: keep it as a feature or restrict the years (PROV-13); `did_police_officer_attend_scene_of_accident` and `number_of_casualties` may follow from the severity: decide the prediction point (USE-3, LEAK-10); fatal is a rare class (TP-8 per window); the vehicle and casualty files join on `collision_index` if their fields are wanted.
- Priority: gap + (social science has 1 accepted dataset; multiclass is thin), use case 0 (no actor in the source), source + (DfT official statistics with a data guide), shape + (on the order of 100,000 collisions a year over 47 years, mixed types), risk - (the severity-adjustment columns and the CRASH recording change).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `nhtsa_crss_crash_severity`.
- as published: every police-reported personal-injury collision in Great Britain, 1979-2025, one row per collision (collision file 1979-latest 1.5 GB; on the order of 100,000 collisions a year in the 2020s, ...; target: collision severity (fatal / serious / slight), the most severe casualty; casualty severity per person; access: open.
- Why: same quantity as CRSS MAX_SEV (crash injury severity from the police report) with scene features of the same kind (road, light, weather, speed limit, junction, vehicle and driver descriptors); a census of injury collisions instead of a sample
- Adds: a single flat collision table (no three-table join needed), 47 years, a full census rather than a ~50k/yr weighted sample, no survey weights. Caveats: injury collisions only (no property-damage class, so 3 severity classes); the move of many forces to the injury-based CRASH system changed serious vs slight, and DfT ...
