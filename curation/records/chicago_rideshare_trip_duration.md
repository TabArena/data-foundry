---
unique_name: chicago_rideshare_trip_duration
name: Transportation Network Providers - Trips (City of Chicago)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
year: '2018'
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://data.cityofchicago.org/d/m6dm-c72p
- https://data.cityofchicago.org/d/n26f-ihde
- https://data.cityofchicago.org/stories/s/82d7-i4i2
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: every ride-hail trip in Chicago since November 2018 with its exact duration, a huge regulator-kept trip-time table; the task is already in the benchmark, and what is known at booking is coarse here (start time to 15 minutes, tract centroids).
- Source: City of Chicago, "Transportation Network Providers - Trips" on the Chicago Data Portal: m6dm-c72p (2018-2022, created 2018-10-02: "All trips, from November 2018 to December 2022, reported by Transportation Network Providers (sometimes called rideshare companies) to the City of Chicago as part of routine reporting required by ordinance"), n26f-ihde (2023-2024, three new columns) and a table from 2025. As published: trip id, start and end timestamps "rounded to the nearest 15 minutes", `trip_seconds`, `trip_miles`, pickup and dropoff census tract and community area with centroid coordinates, fare (to $2.50), tip, charges, total, shared-trip flags and, since 2023, the share of time and distance in Chicago. The scout counted 174,369,516 trips in 2023-2024 (not rechecked). The privacy note (stories/s/82d7-i4i2) explains the suppressed tracts and the rounding.
- Use case: a ride-hailing app quotes the trip time when a ride is ordered (the ETA of the Yango and Yassir records); our framing, the portal publishes the trips for regulation. Fit approximate: at order time the app knows exact points and its planned route, the table only tract centroids and a 15-minute start. Regime temporal by month.
- Siblings and duplicates: `2025_accra_mobility_prediction_hackathon_powered`, `2025_maputo_mobility_prediction_hackathon_powered_by_yango` (both `TBD -> 2nd Tier`) and `yassir_eta_prediction_challenge` (`TBD -> Yes`) are the records it was found for; `chicago_taxi_trip_duration` (candidate of this run) is the same portal's taxi table with nearly the same columns, a sibling to weigh against this one; `nyc_taxi_trip_duration`, `pkdd_15_taxi_trip_time_prediction_ii` and `maps_router_eta` (all `Yes`) already hold the trip-time task. External collections: none known.
- Better data: found as better data for `2025_accra_mobility_prediction_hackathon_powered`, `2025_maputo_mobility_prediction_hackathon_powered_by_yango` and `yassir_eta_prediction_challenge`; no further search this round.
- Papers and pages: the portal pages and the privacy note.
- Metric: none found (the portal's descriptions). The fallback `rmse`; the accepted `nyc_taxi_trip_duration` keeps its competition's RMSLE, a weighing call for the curator (MET-10); inputs none.
- Risks for /add-dataset: `trip_miles` is the driven distance, and `trip_end_timestamp`, fare, tip, charges, total, `trips_pooled` and `shared_trip_match` are known only after the trip or the match (LEAK checks; no planned distance ships, so the inputs are origin, destination and start time); tracts are suppressed in some cases; hundreds of millions of rows, so a sample by month.
- Priority: gap 0 (regression and temporal are not thin), use case 0 (our framing), source + (City portal under an ordinance, documented columns), shape + (millions of trips), risk - (post-trip columns; the task already covered).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `2025_accra_mobility_prediction_hackathon_powered`, `2025_maputo_mobility_prediction_hackathon_powered_by_yango`, `yassir_eta_prediction_challenge`.
- as published: every ride-hail trip in Chicago: 174,369,516 trips in the 2023-2024 table alone (count from the Socrata API); 21-24 columns: start timestamp (rounded to 15 min), pickup and dropoff census tract, ...; target: trip duration in seconds (Trip Seconds); access: open.
- Why: same target (ride-hail trip duration) and use case, with features of the same kind known at ordering: origin, destination, time and a route distance; the Yango and Yassir data are one month or a few months of one city
- Adds: orders of magnitude more trips, several years (2018 to now) and maintained by a regulator with a privacy note, no login or residence restriction (the Zindi hackathons are open only to residents of Ghana or Mozambique). Caveats: Trip Miles is the driven distance (a proxy for the route distance known at booking), Trip ...
