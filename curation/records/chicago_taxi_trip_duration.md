---
unique_name: chicago_taxi_trip_duration
name: Chicago Taxi Trips (2013-2023) and Taxi Trips (2024-)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2016'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://data.cityofchicago.org/Transportation/Taxi-Trips-2013-2023-/wrvz-psew
- https://data.cityofchicago.org/api/views/wrvz-psew.json
- https://data.cityofchicago.org/Transportation/Taxi-Trips-2024-/ajtu-isnz
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the City of Chicago's own register of taxi trips since 2013, about 230M trips, for the trip-duration task that `nyc_taxi_trip_duration` and `pkdd_15_taxi_trip_time_prediction_ii` ship, from a third city and up to 2026; locations and times are coarser than in the NYC data.
- Source: City of Chicago Data Portal, "Taxi Trips (2013-2023)" (wrvz-psew; created 2016-05-27, published 2016-11-14, last row update 2024-02-07; data owner the Department of Business Affairs & Consumer Protection) and "Taxi Trips (2024-)" (ajtu-isnz, published 2024-02-07), read through the Socrata metadata API on 2026-10-31. As published: 211,670,894 plus 18,658,792 trips (non-null Trip ID counts), 24 and 23 columns: trip and taxi id, start and end timestamp ("rounded to the nearest 15 minutes"), Trip Seconds, Trip Miles, pickup and dropoff census tract ("suppressed in some cases"), community area and centroid coordinates, fare, tips, tolls, extras, trip total, payment type, company. The trips are those "reported to the City of Chicago in its role as a regulatory agency"; "not all trips are reported but the City believes that most are".
- Use case: none stated by the City (a regulator's open data). The NYC competition and the Porto challenge defined the ETA at pickup: a dispatcher or rider app estimates the duration from origin, destination, time and company before the trip. Fit approximate: the City names no actor, and locations are tract or community-area centroids with times rounded to 15 min. Regime temporal: an ETA model is refit and predicts later trips; 13 years, with the 2020 drop. The NYC record uses weekly windows.
- Siblings and duplicates: `nyc_taxi_trip_duration` (`Yes`, v2 `_1m`, RMSLE) and `pkdd_15_taxi_trip_time_prediction_ii` (`Yes`) hold the same task in other cities. `chicago_rideshare_trip_duration` (a new record of this run) is the City's ride-hail table with the same layout: a sibling, not a duplicate (PROV-7), and the curator may want only one Chicago trip record. `nyc_taxi_green_dec_2016` and `nyc_taxi_fare_dataset` have other targets. No Chicago taxi record existed before this run. External collections: not searched (web search budget used up).
- Better data: found as better data for `nyc_taxi_trip_duration` and `pkdd_15_taxi_trip_time_prediction_ii` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the two portal pages and their metadata; papers that used the data were not searched (web search budget used up).
- Metric: none found (the portal publishes a register, no task), so the fallback `rmse` on the trip seconds, with the target shipped as log1p (MET-3, MET-8). The NYC competition scored RMSLE on the same task, but that is not this source's metric; the curator decides (MET-1, MET-4). Inputs none.
- Risks for /add-dataset: Trip End Timestamp, Trip Miles, Fare, Tips, Tolls, Extras, Trip Total and Payment Type are known only after the trip (LEAK); Trip Miles stands in for a route distance known at booking only if the use case is a booked trip. Trip Seconds against the rounded timestamps, and zero or multi-day durations, need cleaning rules (CLEAN). Suppressed tracts leave locations missing. 230M rows need sampling per window as in NYC's `_1m`. Taxi ID is a medallion, a grouping column rather than a feature.
- Priority: gap 0 (regression and temporal not thin), use case 0 (the City names none; the ETA framing comes from the NYC and Porto competitions), source + (the regulator's documented table), shape + (230M trips, 2013-2026, mixed types, temporal), risk 0 (the post-trip columns are named and get dropped as in NYC).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `nyc_taxi_trip_duration`, `pkdd_15_taxi_trip_time_prediction_ii`.
- as published: 211,670,894 trips 2013-2023 (wrvz-psew) plus 18,658,792 trips 2024-01-01 to 2026-10-01 (ajtu-isnz); 23-24 columns: trip id, taxi id, start/end timestamp (rounded to 15 min), trip seconds, trip ...; target: Trip Seconds (metered trip duration), log-scaled as in the NYC and Porto records; access: open.
- Why: same target (trip duration of a city taxi trip) and the same ETA-at-pickup framing as nyc_taxi_trip_duration and pkdd_15, with features of the same kind: origin and destination location, start time, a consistent per-medallion Taxi ID (the grouping both records use) and the company; Trip Miles, fare and payment fields ...
- Adds: a third city and source with far more and newer data: 13+ years of trips up to October 2026 against NYC's first half of 2016 and Porto's 2013-14, so temporal windows can sit in 2025-26 and span the pre/post-2020 shift; the regulator's own table, not a competition sample. Weaker spatial and time resolution: start time ...
