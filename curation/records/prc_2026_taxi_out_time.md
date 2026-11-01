---
unique_name: prc_2026_taxi_out_time
name: 'PRC Data Challenge 2026: taxi-out time of departures at 10 major European airports'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Other
year: '2026'
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://prc-data-challenge-2026.netlify.app/data.html
- https://prc-data-challenge-2026.netlify.app/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: EUROCONTROL's PRC Data Challenge 2026, about 4.2 million movements at 10 major European airports (2025 for training, months of 2026 for ranking) with the taxi-out time of departures as an RMSE target; the stated use is post-operations analysis, the take-off time ships beside the blanked off-block time, and the data is not yet open.
- Source: EUROCONTROL Performance Review Commission with the OpenSky Network, PRC Data Challenge 2026 (prc-data-challenge-2026.netlify.app; 1 September to 14 October 2026). As published (data page, read 2026-10-31): "a total of 4,167,797 movements at the 10 airports" (EDDF, EDDM, EGLL, EHAM, LEBL, LEMD, LFPG, LIRF, LTFM, LSZH), with "Military, Head of State, and Sensitive movements" removed; monthly training files for 2025, `ranking.parquet` with January and July 2026, and a final set adding February and June 2026. Movement columns (`_mvt`) include `MVT_TIME_UTC_mvt` ("takeoff if `PHASE` = `DEP`"), `BLOCK_TIME_UTC_mvt` and `SCHED_TIME_UTC_mvt`; flight columns (`_flt`) from the Network Manager include `LOBT_flt`, `IOBT_flt`, `EOBT_1_flt`, `AOBT_3_flt` ("actual off-block time, flown trajectory") and `ARVT_3_flt`. Target: "`TAXITIME_SEC_mvt` = `MVT_TIME_UTC_mvt` - `BLOCK_TIME_UTC_mvt` (for the departure)"; in the ranking set `BLOCK_TIME_UTC_mvt` and `TAXITIME_SEC_mvt` of departures "have been blanked out". Access: teams apply by form and get OpenSky (MinIO) keys; no licence stated; the home page plans an open release of the dataset with a JOAS data paper "before the end of Q1 2027".
- Use case: the rationale page: "A model to estimate taxi-out time can be used in post-operations analysis to identify constrained operations intervals"; it names no actor or prediction time for a live prediction (an airport's or the Network Manager's taxi-time estimate before off-block would be ours to state). Fit approximate until the inputs are fixed. Regime temporal: the challenge trains on 2025 and ranks on months of 2026 (SEL-11: a fixed per-movement duration with a temporal split, not forecasting).
- Siblings and duplicates: `prc_2024_aircraft_takeoff_weight` (a candidate of this run, the same organiser's 2024 challenge on take-off weight; another task, PROV-7); the flight-delay records `airlines_depdelay_10m` and `pnwflights14` (`No`, `Duplicate`) are US departure delays, not taxi times. External collections: none.
- Better data: from the curator's Zotero collection (item 292, PRC Data Challenge 2026); no further search this round.
- Papers and pages: the challenge's home, data, ranking and rationale pages; the leaderboard at prc-challenge-2026.vercel.app (not read); the Zenodo deposit doi 10.5281/zenodo.23133051 is one team's (funny-firefly) auxiliary inputs (OpenStreetMap stand-to-runway distances, adsb.lol off-block events, METAR) and "does not contain the challenge data" (moved here from source_links, PROV-12).
- Metric: RMSE, the leaderboard's (ranking page: teams are ranked on the "best Root Mean Square Error (RMSE) achieved across their submissions"), so `rmse` from the source (MET-4); inputs none.
- Risks for /add-dataset: the target is the take-off time minus the off-block time, and the take-off time (`MVT_TIME_UTC_mvt`) and the Network Manager's `AOBT_3_flt` stay in the ranking set, so the taxi time may be close to a difference of two shipped columns: fix the prediction point first, then keep or drop them (USE-3, LEAK-10, TP-4); the data is not public until the planned release (no criterion, EV-4, but nothing to build before it); arrivals share the files and are no task rows; inconsistencies between movement and flight records ("Real world data is messy", data page).
- Priority: gap 0 (no thin value), use case 0 (post-operations analysis, no actor or decision named), source + (the organiser's data page defines every column; a data paper is announced), shape + (about 4.2 million movements over 10 airports and 16 months), risk - (the target may follow from two shipped times; data not yet released).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 292: "PRC Data Challenge 2026".
- as published: 4,167,797 movements (arrivals and departures) at EDDF, EDDM, EGLL, EHAM, LEBL, LEMD, LFPG, LIRF, LTFM and LSZH. Training covers Jan-Dec 2025; ranking uses Jan and Jul 2026, and the final set adds ...; target: TAXITIME_SEC_mvt of departures: taxi-out time in seconds from off-block to take-off (regression, RMSE); access: registration.
- Why: Real Network Manager and airport movement data at large scale, from a running challenge with an RMSE leaderboard. The challenge plans an open release with a JOAS data paper, as for the 2024 and 2025 editions.
- Adds: An airport-operations task (aviation is thin), a fixed delay-like target with a temporal split (SEL-11), and big, recent, multi-airport data. Caveats: access is now limited to approved teams through OSN keys; the licence is not stated; the open release is announced for Q1 2027. Leak risk: MVT_TIME_UTC (actual ...
