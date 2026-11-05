---
unique_name: 2024_lusaka_mobility_prediction_hackathon
name: 2024-lusaka-mobility-prediction-hackathon
checked_by:
- Myunghwan
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 2
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.world/competitions/2024-lusaka-mobility-prediction-hackathon
- https://zindi.world/competitions/2024-lusaka-mobility-prediction-hackathon/data
- https://api.zindi.world/v1/competitions/2024-lusaka-mobility-prediction-hackathon
- https://github.com/Mwandamena/yango-hackathon/tree/2fa7817be0740ea1739143ea6e61a28d6cf1462d/data
v2_path: datasets/_dev/tabarena-v0pt2/2024_lusaka_mobility_prediction_hackathon/dataset.py
source_row: 934
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-10-29, Myunghwan): Include the trip-start ride-time task with the accepted approximate endpoint/weather inputs. Preserve the supplied aligned trip/weather calendar and the identified participant copy. The source year remains 2024; no calendar correction is inferred.

**Assessment (AI, 2026-10-29):** One row is a labeled trip. Predict actual duration in minutes using trip start, four endpoint coordinates, straight-line distance and three preceding-hour weather fields. Actual traveled distance and identifiers are excluded. After dropping 21 missing start times, 112,739 rows remain. Keep positive durations and zero straight-line distances without unsupported trimming (superseded 2026-11-05: trips over 3 hours and trips faster than 120 km/h in a straight line are dropped, Lennart's issues 4 and 5; the trips under 100 m in a straight line left on 2026-11-04).

The pinned participant copy identifies this exact Yango/Zindi Lusaka challenge. Its trip timestamps run through January 2023 and early February, while the competition describes January 2024; weather and the inspected participant starter also identify January 2023. Preserve the supplied calendar, first-source year 2024 and the pinned public mirror. Train, Test, weather and sample-submission byte lengths match the organizer's listing; dictionary and starter lengths differ. Organizer-original byte equality and the reason for the calendar discrepancy remain unverified.

At trip start, recorded destination and straight-line distance stand in for the requested destination; capture timing is unverified. Weather uses floor(trip_start) minus one hour, without future fill or year/timezone shifting: 112,716 rides have exact preceding-hour matches, and 23 out-of-coverage rides retain missing weather (superseded 2026-11-05: the join lags 3 hours; the 175 trips that start on 1 January before 03:00 have no weather row). Earlier-hour measurement does not establish publication latency. These limitations were explicitly accepted as an approximation, not certified as prospectively available facts.

Use the competition's RMSE on actual minutes with identity target transform. Three chronological four-day test windows have a one-day training gap. All observed durations are below one day, so observed training trip ends precede refit; additional reporting delay and cohort-extraction maturity remain unknown. The final test includes a partial final day. This same-release city/month task does not establish all-season or other-city generalization. Source reuse restrictions remain separate from scientific acceptance.

The current measured findings and accepted task above supersede the source-only counts and provisional framing in the historical screening notes below. Priority 3 is retained for the traceable source and specified ride-time use case; approximate timing and source/calendar limits remain explicit.

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: a per-trip ride-time regression (Yango's ETA), not demand forecasting; the competition page refutes the old `No` with `Time-series (Forecasting)` and `Missing source information`.
- Source: Zindi one-day hackathon "2024 Lusaka Mobility Prediction Hackathon Powered" by Yango, 26 Oct 2024 (https://zindi.africa/competitions/2024-lusaka-mobility-prediction-hackathon, read through Zindi's page API); as published: "a sampled dataset of trips ordered via the Yango App from January 2024 in Lusaka": Train.csv (15.6 MB, with the target), Test.csv (6.4 MB, no target), Lusaka_weather.csv (49 KB, joined by time), VariableDefinitions.csv. Coordinates geomasked "by at least X meters and no more than Y meters in a random direction"; "The straight-line distance is calculated based on the original points"; "excessively short trips" removed. Rows and columns not counted (the files need a login).
- Use case: "Yango uses a wide range of data in order to predict travel and arrival times of its partners' drivers and vehicles" (Description): the platform quotes a ride time when a trip is ordered; fit direct if every column is known at ordering; regime temporal (one month of trips; quoting future trips), as for `nyc_taxi_trip_duration`.
- Siblings and duplicates: the same Yango task in other cities: `2025_accra_mobility_prediction_hackathon_powered` (Jan 2025, Train.csv 7.9 MB) and `2025_maputo_mobility_prediction_hackathon_powered_by_yango` (2024 trips, 9.0 MB), plus a 2026 Yaounde edition without a record: different data, the same task and publisher, so take one city (this one has the largest train file). The road-speed hackathons (`accra_mobility_prediction_hackathon`, practice-challenge-lusaka, the cities in `mobility_prediction`) are another task. Ride-time precedents: `nyc_taxi_trip_duration` and `pkdd_15_taxi_trip_time_prediction_ii` (`Yes`), `maps_router_eta` (`Yes`, TabReD), `yassir_eta_prediction_challenge` (`TBD -> Yes`). External collections: none found.
- Papers and pages: no paper; the competition's Description, Data and Evaluation tabs; no public solution or column list found (web search 2026-10-22).
- Metric: RMSE on the ride time ("The evaluation metric for this competition is Root Mean Squared Error", Evaluation tab); a competition's leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the column list is unread: check that no column is known only after the trip (driven distance, drop-off time) (LEAK); the target's unit; only Train.csv is labelled; the second link (practice-challenge-lusaka) is a different dataset (road speeds, Sept 2023); access: login, and the competition "is only open to Zambian users residing in Zambia" (no criterion, EV-4).
- Priority: gap 0 (technology & internet, regression and temporal are not thin), use case + (Yango's ETA, named by the source), source 0 (a competition page, no codebook read), shape + (a month of trips with time and weather), risk 0.

A Zindi 'mobility prediction' hackathon for Lusaka with no comments in the record. Mobility-prediction challenges (often ride-hailing/transport demand) typically forecast trips/demand over space and time, which is excluded forecasting rather than a fixed IID/temporal-split tabular task. The record carries essentially no descriptive content, so the verdict is unverified. A human must confirm the exact target and whether it is a one-shot prediction or a multi-step forecast; if it is genuine forecasting it stays No, but if it is a fixed per-trip prediction it could be revisited.

CC (2026-11-04, Lennart): the trips whose start and end lie under 100 m apart in a straight line are dropped ("drop them, this is not a relevant prediction goal here imo"; USE-7, as nyc_taxi_trip_duration_1m): 2,364 of 112,739, 110,375 remain. The domain is `industry & manufacturing`, as the other ride-time tasks ("align it"). The metric, RMSE in minutes, is checked as declared.

**Assessment (AI, 2026-11-04):** the dropped trips are not short rides but round trips: a median of 22.1 minutes (10.8 for the rest), 93% over 5 minutes, and a median of 4.5 km actually driven. They held 16% of the target's squared spread. This supersedes the earlier note that zero straight-line distances are kept.

CC (2026-11-04, Lennart): the trip time stays in minutes, with RMSE ("ok keep minutes"), as the other RMSE-scored ETA datasets.

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; its issues came from the light static review of the PR #33 page and the research behind each mark, and all are settled.

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes (LEAK-10 holds for the driven distance, SPLIT-1/SPLIT-9/SPLIT-14 hold, USE-7 applied as nyc and pkdd, USE-8 approximate with no routing-engine route or ETA, MET-4 and MET-2 hold with the RMSE tail written into the notes; the wording fixes are in `dataset.py`. The metric rests on MET-4, the source's own RMSE, not on the other ETA datasets, which score log targets or RMSLE. This supersedes "no panel ran" above and the screening's "no public solution found": the pinned mirror is a participant repository with a starter notebook); disputed: LEAK-10 (weather clock, 3 h lag), CLEAN-11 (20 trips over 3 h; the 19 trips over 120 km/h agreed but change rows); for the curator: issues 3-5. Priority 2: gap 0, use case 0, source 0, shape +, risk 0 (use case: Yango's ETA is named, but the fit is approximate; source: a competition page and dictionary read only through a participant mirror, with a year conflict; risk: the open issues are cleaning and a weak weather-clock question with no measured effect).

CC (2026-11-05, Lennart): the weather join lags 3 hours instead of 1 (issue 3, B; LEAK-10, EV-2): the weather's daily temperature curve fits UTC stamps against the dictionary's local clock, so the joined row now precedes the start on either clock, at no measured cost. The 175 trips that start on 1 January before 03:00 have no weather row.

CC (2026-11-05, Lennart): the 20 trips over 3 hours are dropped as not closed in the app (issue 4, B; CLEAN-11, then CLEAN-15; as pkdd_15_taxi_trip_time_prediction_ii_1m's `MAX_TRAVEL_TIME_S` and nyc_taxi_trip_duration_1m's 3 h cap): up to 788 minutes at 1.5 km/h, 11.8% of the target's squared spread, 8 of them test rows.

CC (2026-11-05, Lennart): the 19 trips faster than 120 km/h in a straight line are dropped (issue 5, B; CLEAN-11, then CLEAN-15; as pkdd's `MAX_STRAIGHT_LINE_KMH`): the straight line comes from the unmasked points, so the duration or the endpoint is wrong. The two cuts share no trip: 110,336 trips remain (110,375 before).

CC (2026-11-05, Lennart): the declared metric (RMSE on minutes, the source's) is checked and stays as declared.

**Assessment (AI, 2026-11-05):** after the two cuts the windows from 2023-01-29, 2023-01-25 and 2023-01-21 hold 94,897/11,138, 79,897/16,055 and 65,876/13,630 train/test trips, and the longest trip is 175 minutes. The RMSE tail shrank: trips over 120 minutes hold 12.0%, 6.3% and 7.9% of the windows' squared deviation (15.7%, 28.8% and 16.9% before), the largest 1% of an untuned LightGBM's errors hold 43 to 53% of its squared error (54 to 66% before), and no trip holds over 2% of a window's constant-prediction squared error (the 788-minute trip held 21% before). Leak probes as before (the weather columns alone score -0.025 to -0.001, no copies, the partial 1 February in probe 13); the task probe now raises `no_spread` (LightGBM +0.328 against the random forest's +0.278, paired SE 0.036 over 3 windows), the noise of three windows, kept (TP-3). `dataset check`: 0 errors, 0 warnings.

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask. The claim stays until the PR that takes it to `main` sets `DF: Yes`.
