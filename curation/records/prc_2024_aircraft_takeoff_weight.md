---
unique_name: prc_2024_aircraft_takeoff_weight
name: 'PRC Data Challenge 2024: actual take-off weight of European flights (2022)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
year: '2024'
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.4121/8cb8484b-dbe7-4750-8b87-a5b1dbc621b4
- https://doi.org/10.59490/joas.2025.8252
- https://ansperformance.eu/study/data-challenge/dc2024/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: EUROCONTROL's PRC Data Challenge 2024, 527,162 European flights of 2022 with the take-off weight derived from the airlines' data, a public RMSE leaderboard, all teams' code and a data paper; one flight list, trajectories optional.
- Source: EUROCONTROL Performance Review Commission, PRC Data Challenge 2024 (ansperformance.eu/study/data-challenge/dc2024, launched July 2024, deadline 2024-10-28); data "Dataset for EUROCONTROL PRC 2024 Data Challenge on Aircraft Take-off Weight Estimation", 4TU.ResearchData (doi 10.4121/8cb8484b-dbe7-4750-8b87-a5b1dbc621b4; version 2 of 2025-07-14 per the run's search, the page refused the connection here); data paper Spinielli, Sun, Strohmeier, Olive, Goens, Koelle, Tart, Fitzgerald, "Aircraft Takeoff Weight Estimation: The EUROCONTROL PRC 2024 Data Challenge", Journal of Open Aviation Science 3(2), 2025 (doi 10.59490/joas.2025.8252, CC BY 4.0). The flight list is the Network Manager's, "augmented with derived Take-Off Weight (TOW) from airlines" (JOAS, Method); 527,162 flights that "represent 6.1% of the flights from the EUROCONTROL airspace"; "After the end of the data challenge, we deliver the full ground truth dataset in flight_list.csv. It consists of all the 527162 rows". Columns (dc2024 data page): `flight_id`, obfuscated `callsign` and `airline`, `adep`/`ades` with names and country codes, `date`, `actual_offblock_time`, `arrival_time`, `aircraft_type`, `wtc`, `flight_duration`, `taxiout_time`, `flown_distance`, `tow` (kg); OpenSky ADS-B trajectories at up to 1 s (about 158 GiB of parquet) join by flight.
- Use case: the source's: ATOW is "an essential input parameter for modeling the amount of fuel burnt during a flight" and its emissions (JOAS, Introduction), and analysts otherwise assume a fixed share of the maximum take-off weight (dc2024 page). An analyst of aviation's fuel burn and emissions, after the flight, estimates the take-off weight of a flight whose airline does not publish it. Fit direct for this post-flight estimate, so `flight_duration`, `flown_distance` and `taxiout_time` are known at the prediction point. Regime: the challenge split at random ("The split between training and testing is random", JOAS); the estimate serves airlines that did not share their weights, so a split by the obfuscated airline is the one to weigh (SPLIT-3, USE-10).
- Siblings and duplicates: `prc_2026_taxi_out_time` (a candidate of this run) is the same organiser's 2026 challenge on another task and other data (PROV-7); no other take-off weight or EUROCONTROL record (grep: eurocontrol, take-off weight, opensky, prc data challenge). External collections: none found; the team papers fill JOAS vol. 3, no. 2.
- Better data: from the curator's Zotero collection (item 292, PRC Data Challenge 2026); no further search this round.
- Papers and pages: the JOAS data paper; the teams' code in github.com/PRC-Data-Challenge-2024 (moved here from source_links: solutions, not the data, PROV-12); the 2026 challenge site prc-data-challenge-2026.netlify.app (moved here from source_links: another challenge, PROV-12); a team paper, "Open Machine Learning Models for Actual Takeoff Weight Prediction" (JOAS article 7963).
- Metric: RMSE, the leaderboard's (the ranking "will use Root Mean Square Error (RMSE) to compare a submission" with the ground truth, dc2024 data page), so `rmse` from the source (MET-4); inputs none.
- Risks for /add-dataset: how the airlines' TOW was derived is not stated in what was read (the data page calls `tow` "(estimated) TakeOff Weight", and JOAS drops flights with incomplete weight data such as "missing fuel weight"), so read the label's construction (USE-5); the airline split against the challenge's random split (SPLIT-3); `flight_id` and `callsign` are identifiers (drop); `arrival_time` and the trajectories run past landing, fine for the post-flight use but to state in the notes; the trajectory features are optional, and the flight list alone is the tabular task.
- Priority: gap 0 (no thin value; domain left unset), use case + (the source names the estimate and its use in fuel and emission models), source + (data paper, DOI, organiser's pages), shape + (527,162 flights, categorical and numeric columns), no risk taken off.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 292: "PRC Data Challenge 2026".
- as published: 527,162 flights flown in Europe in 2022 (6.1% of EUROCONTROL-area traffic). The full ground truth is released as flight_list.csv: the challenge's 369,013 training and 158,149 test rows. Flight-list ...; target: tow: actual take-off weight in kg, derived from airline data (regression; the challenge ranked by RMSE); access: open.
- Why: Rare real weight data from airlines, large, openly licensed (CC BY 4.0), with a peer-reviewed data paper and public solutions of all teams.
- Adds: An aviation regression with 500k rows, mostly tabular from the flight list; trajectory features are optional. Caveats: the airline is anonymized, and flown_distance and flight_duration are known only after the flight (fine for the estimation use case, not for pre-flight planning). The trajectory archive is large, so ...
