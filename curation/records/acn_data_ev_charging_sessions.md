---
unique_name: acn_data_ev_charging_sessions
name: 'ACN-Data: an open EV charging dataset (Caltech Adaptive Charging Network)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Other
year: '2019'
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.1145/3307772.3328313
- https://ev.caltech.edu/dataset
- https://github.com/zach401/acnportal
- https://doi.org/10.1145/3307772.3330170
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: measured EV charging sessions of Caltech's Adaptive Charging Network (three California sites, over 30,000 sessions at the 2019 paper), with the driver's own inputs at plug-in; a session-level regression (the stay or the energy delivered) for the operator's charging schedule.
- Source: Lee, Li, Low, "ACN-Data: Analysis and Applications of an Open EV Charging Dataset", ACM e-Energy 2019 (doi 10.1145/3307772.3328313); the second DOI on the record (10.1145/3307772.3330170) is the companion paper ACN-Sim (Lee, Johansson, Low, e-Energy 2019). Data through the ACN-Data API, Python client and web interface (ev.caltech.edu/dataset; registration for an API token; no licence stated, a citation asked for). As published: one JSON record per session with siteID, stationID, spaceID, connectionTime, disconnectTime, doneChargingTime, kWhDelivered, userID ("not provided for sessions not claimed via the mobile app") and userInputs (WhPerMile, kWhRequested, milesRequested, minutesAvailable, requestedDeparture, modifiedAt, paymentRequired); sites Caltech (54 EVSEs, public garage), JPL (50, employees only) and Office 1 (8, Silicon Valley). Session count: over 30,000 in the paper's abstract (through Semantic Scholar); the current total was not checked.
- Use case: the site operator, when a car plugs in, estimates when it will leave and how much energy it needs, to schedule charging under the site's capacity (the paper's applications include modelling user behaviour with Gaussian mixture models); fit direct for the departure, approximate for kWhDelivered, which the scheduler itself limits; regime temporal (sessions over years, the COVID-19 drop of 2020), with repeat users and stations as grouped structure inside it (SPLIT-13).
- Siblings and duplicates: `ev_charging_grid_optimization_dataset`, `ev_charging_station_data_california_region` and `microgrid_pv_ev_charging_dataset` (all `No`, `AHDS` and `Missing source information`): ACN-Data is real data for their task, not a copy of them. `norway_residential_ev_charging_sessions` (a candidate of this run: residential sessions in Norway) is another source for a similar task (PROV-7). No other ACN record (grep: caltech, acn-data, acnportal). External collections: none found.
- Better data: found as better data for `ev_charging_grid_optimization_dataset`, `ev_charging_station_data_california_region` and `microgrid_pv_ev_charging_dataset`; no further search this round.
- Papers and pages: the paper above (the ACM page returned 403; read through its abstract); ACN-Sim; the acnportal client on GitHub.
- Metric: none found (the paper's text could not be read, and neither its abstract nor the data page names one), so the fallback `rmse` (MET-1, MET-11); inputs none.
- Risks for /add-dataset: choose one target and say why: the stay (disconnectTime minus connectionTime) is user behaviour, while kWhDelivered depends on the scheduling algorithm and the site's limits (USE-5); doneChargingTime and disconnectTime are known only after the session (LEAK-10); userID and userInputs exist only for app users, so the rows with inputs are a selection (check the share); the web interface shifted timestamps by 7 to 8 hours before 2019-10-10, so take the data from the API; drift from March 2020.
- Priority: gap 0 (no thin value; domain unset, regression and temporal not thin), use case + (the network's scheduling, named through the paper's user-behaviour application), source +, shape + (tens of thousands of sessions with times, stations, users and inputs), risk - (two targets, one shaped by the controller).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ev_charging_grid_optimization_dataset`, `ev_charging_station_data_california_region`, `microgrid_pv_ev_charging_dataset`.
- as published: charging sessions at three sites, all in California: Caltech campus garage (54 EVSEs, public), JPL (50 EVSEs, employees only), a Silicon Valley office (8 EVSEs). Per session: site, station, space, ...; target: energy delivered in the session (kWhDelivered, kWh), or the session duration (disconnectTime minus connectionTime); access: registration.
- Why: a real, traceable session-level EV charging dataset in California with the features known at plug-in (site, station, arrival time, user history, the driver's own request); both records are EV-charging tasks whose data was judged generated (California region: uniform weather; grid optimization: AI-optimized targets ...
- Adds: measured sessions with a paper, a maintained API and the plug-in user inputs, against generated rows without a source. Notes: userID only for app users; repeated users and stations call for a grouped or temporal split; COVID-19 lowered use at Caltech from March 2020 | real, traceable measurements and a real target ...
