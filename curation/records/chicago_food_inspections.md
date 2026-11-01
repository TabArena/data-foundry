---
unique_name: chicago_food_inspections
name: Chicago Food Inspections (Department of Public Health), with the city's critical-violation prediction model
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
required_split:
- Temporal (NON-IID)
original_data_state: One Table
source_links:
- https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5
- https://github.com/Chicago/food-inspections-evaluation
- https://chicago.github.io/food-inspections-evaluation/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 317,892 City of Chicago food inspections (2010-2026) with the result and the violations, and a prediction the city deployed to send inspectors first to establishments likely to have a critical violation (a double-blind trial in 2014); temporal, mixed types; the features must be built from each licence's history.
- Source: City of Chicago Data Portal, "Food Inspections" (Department of Public Health, Food Protection Program), dataset 4ijn-s7e5, updated continuously (the year waits for the snapshot we pin, PROV-9). Preview through the portal API (2026-10-31): 317,892 rows, 2010-01-04 to 2026-10-29, 49,305 licences; results Pass 164,601, Pass w/ Conditions 47,084, Fail 61,195, Out of Business 25,987, No Entry 14,279, Not Ready 4,650, Business Not Located 96; columns inspection id, DBA and AKA name, licence, facility type, risk, address, zip, inspection date, inspection type, results, violations (text), latitude, longitude.
- Use case: CDPH ranks establishments by predicted risk of a critical violation before scheduling routine inspections; the city's evaluation page: the model "was developed to prioritize which ones should be inspected first", tested by "double-blind retrodiction" in September and October 2014; "establishments with violations were found, on average, 7 and a half days earlier", and 69% of the establishments with critical violations were found in the first half of the work, against 55%. Fit direct for the binary critical-violation target (the city's); the 3-class result is our framing. Regime temporal (inspections over time, history per licence).
- Siblings and duplicates: other Chicago portal records (`chicago_building_permit_time`, `chicago_traffic_crashes`, `chicago_beach_bacteria_advisory`, `chicago_taxi_trip_duration`, `chicago_rideshare_trip_duration`) are other tasks; no other food-inspection record (searched food inspection, restaurant, health inspection, hygiene). External collections: none found.
- Better data: from the gap scout for social science; no further search this round.
- Papers and pages: the portal page; GitHub Chicago/food-inspections-evaluation (R code that joins Business Licenses, Food Inspections, Crime, Garbage Cart and Sanitation Complaints, Weather and Sanitarian data on inspection id, licence and coordinates); chicago.github.io/food-inspections-evaluation (nine predictors: prior critical or serious violations, recent high temperatures, nearby garbage and sanitation complaints, facility type, nearby burglaries, a tobacco or incidental alcohol licence, time since the last inspection, years in operation, the assigned inspector).
- Metric: the city reports days earlier and the share found in the first half of the work, measures of the pilot rather than of the model; no model metric found (evaluation page, repository README), so the fallback `roc_auc` for the critical-violation target, or `log_loss` for the 3-class result (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the violations text is the outcome (use it only to build the label, LEAK); history features (prior fails and critical violations, days since the last inspection) must be lagged per licence; the city's other predictors need joins to other portal tables (complaints, crime, weather, licences); rows that are no inspection (Out of Business, No Entry, Not Ready) to drop (USE-7); a change of the food code and violation numbering on 2018-07-01 (the scout's note, not checked) shifts what counts as critical; complaint inspections and re-inspections differ from canvass ones (inspection type); the inspector is a person (the city used it; decide whether to keep an id).
- Priority: gap + (social science thin; multiclass if the result is shipped), use case + (the city names the decision and evaluated it), source + (the city's portal, code and evaluation), shape + (318,000 inspections, 49,000 licences, mixed types, temporal), risk - (lagged histories to build, joins for the city's feature set, the 2018 code change).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for social science.
- as published: 317,892 inspection rows, 2010-01-04 to 2026-10-29 (portal query 2026-10-30), 17 columns plus the violations text; results: Pass 164,601, Pass w/ Conditions 47,084, Fail 61,195, and 45,012 ...; target: Inspection result (Pass / Pass w/ Conditions / Fail, 3 classes), or a critical violation found (binary, the city's model target, derivable from the violations ...; access: open.
- Why: A prediction the city actually deployed, with a public evaluation and code; open government data on a real, recurring decision. The city's features (previous critical/serious violations, time since last inspection, facility type, licence age, tobacco/alcohol licence, nearby sanitation complaints and burglaries, ...
- Adds: Public services (a thin area); a multiclass target (24 of 173); temporal regime and grouping by licence; mixed types (facility type, risk category, inspection type, zip, coordinates, history counts). Risks for /add-dataset: the violations text is the outcome (drop or use only for the label); history features must be ...
