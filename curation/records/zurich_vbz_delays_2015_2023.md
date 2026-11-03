---
unique_name: zurich_vbz_delays_2015_2023
name: Fahrzeiten der VBZ im SOLL-IST-Vergleich (yearly datasets 2015-2023)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
- Time-series (Regression)
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
year: '2015'
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2022
- https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2016
- https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2023
- https://data.stadt-zuerich.ch/api/3/action/package_search?q=fahrzeiten
- https://opendata.swiss/en/perma/istdaten@oevch
- https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2015
- https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2017
- https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2018
- https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2019
- https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2020
- https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2021
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the planned and actual stop times of every VBZ tram and bus in Zurich from 11 November 2015 to 29 July 2023, the source of `delays_zurich_transport` (four weeks of 2016 on OpenML); a newer, much larger release of the same source (PROV-6) that keeps the sibling's open questions: heavy wrangling and how close the next-stop delay is to forecasting.
- Source: Verkehrsbetriebe Zürich (VBZ, Departement der Industriellen Betriebe) on Open Data Zürich, "Fahrzeiten [year] der VBZ im SOLL-IST-Vergleich (Nachführung eingestellt)", one dataset per year (`vbz_fahrzeiten_ogd_2015` to `vbz_fahrzeiten_ogd_2023`), first published 2015-11-11, CC0. As published: weekly CSV files "Fahrzeiten_SOLL_IST_<from>_<to>.csv" of about 250 MB (52 to 54 weeks a year for 2016-2022, 12.9 to 13.8 GB a year; 30 weeks to 2023-07-29; 2015 from 11 November as one 1 GB zip), 34 columns (checked in a 3 KB preview of the week of 2022-12-25): line, direction, operating day, vehicle, course, trip id, route (`fahrweg_id`, `fw_no`, `fw_typ`: normal, pull-out, pull-in or extra trip, `fw_kurz`, `fw_lang`), block (`umlauf_von`), and for the "from" and the "to" stop their sequence, stop and stop-point ids, date, scheduled and actual arrival and departure in seconds after midnight. Two matching tables, `Haltepunkt.csv` (stop points with WGS84 coordinates and bearing) and `Haltestelle.csv` (stop names), join on `halt_punkt_id_von` and `halt_punkt_id_nach`. One row is one stop-to-stop segment of one trip; the page: "Die Haltestellenankünfte und -abfahrten jedes Fahrzeugs auf seiner Linie wird sekundengenau gemessen." For data after 2023-07-29 the page points to the national Ist-Daten on opentransportdata.swiss. Rows not counted: the OpenML cut holds 5,465,575 rows for four weeks, so the release is on the order of 500 million segments (an estimate).
- Use case: none named by the source (the page: the data allow "einen sehr genauen Vergleich zwischen den geplanten (SOLL) und den effektiv erfolgten (IST) Fahrzeiten", punctuality monitoring). Two readings, to choose at /add-dataset: a passenger-information or dispatch system that predicts, when a vehicle leaves a stop, its arrival delay at the next stop (the delay so far is known); or a timetable planner who predicts the delay of a scheduled segment from line, stop, time of day and calendar (no real-time input). Fit approximate (a use case the curation wrote); regime temporal (SEL-11, SPLIT-6; the sibling's CC: "Requires temporal split"), with lines, stops, vehicles and trips recurring across windows (SPLIT-13).
- Siblings and duplicates: `delays_zurich_transport` (TBD -> Yes, DF: Suspended, checked by Andrej; `Time-series (Regression)`, `Needs extensive data wrangling`; collections TabArena Reject and TabSTAR) is OpenML 40753, whose `original_data_url` is data.stadt-zuerich.ch/dataset/vbz-fahrzeiten-ogd and whose description reads "Zurich public transport delay data 2016-10-30 03:30:00 CET - 2016-11-27 01:20:00 CET cleaned and prepared at Open Data Day 2017"; its comments say the day-level weather leaks and that one "could likely get much more data like this by crawling the Zurich data website". This record is that data. A newer, larger release of the same source (PROV-6): the curator decides which one enters. Flight delays are another source and task: `aeolus` (accepted), `airlines`, `airlines_depdelay_10m`, `pnwflights14`. External collections: TabSTAR carries the OpenML cut; for the yearly release not checked (the session's web search budget ran out).
- Better data: found as better data for `delays_zurich_transport`.
- Papers and pages: the city's dataset pages and their CKAN API (every column documented, with the midnight rules for the times); the Open Data Day 2017 project behind OpenML 40753 (github.com/OpenDataDayZurich2016/ODDPredictDelays: a "simple linear model to predict delays in arrival times of VBZ public transportation vessels", "data of 4 weeks", "ca. 6 mio data points", weather from tecson-data.ch at Mythenquai, no metric); VBZ's example code repositories linked from the page (not read); no paper found.
- Metric: none found (the city's pages, the OpenML description, the Open Data Day README), so the fallback `rmse` on the arrival delay in seconds (MET-1, MET-11); inputs none.
- Risks for /add-dataset: the forecasting question (SEL-10, SEL-11, TP-10): with the delay accrued at the "from" stop as a feature, the next-stop delay is nearly that number (in the preview, departure and next arrival delays of 146 s and 147 s, -19 s and -19 s), a `Trivial` risk (TP-4); without it, the planner's task has a weaker signal. The target is built, not shipped: actual minus scheduled arrival at the "to" stop, with the page's midnight rules (actual times above 86,400 or negative when the operating day and the stop date differ). About 400 weekly files and two stop tables to join, a size that calls for a cut (`_1m`), and stop and route ids that change over the years (as-of joins). Weather is not in the source (the sibling's daily weather leaks at the day level; hourly weather would have to come from another source). Trips without actual times or cancelled ones to handle (USE-7). The markers `Needs extensive data wrangling` and `Time-series (Regression)` are carried from the sibling as provisional concerns.
- Priority: gap 0 (regression and temporal are well covered; transport has no domain value of its own), use case 0 (the source names no prediction), source + (VBZ through the city's portal, every column documented), shape + (hundreds of millions of segments over eight years, mixed features, temporal), risk - (heavy wrangling, a target to build, the near-trivial or forecasting question).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `delays_zurich_transport`.
- as published: One row per vehicle trip segment between two stops: scheduled and actual arrival and departure to the second, line, direction, operating date, vehicle number, course, trip id, stop sequence; weekly ...; target: arrival delay at the next stop (actual minus scheduled arrival, seconds); access: open.
- Why: The record's rows are four weeks of this very dataset: OpenML 40753's original_data_url is data.stadt-zuerich.ch/dataset/vbz-fahrzeiten-ogd and its description reads 'Zurich public transport delay data 2016-10-30 - 2016-11-27 cleaned and prepared at Open Data Day 2017'. Same target, same kind of features.
- Adds: Nine years instead of four weeks: every season and year, room for a real temporal split and point-in-time features (the delay already accrued at the previous stop), stop coordinates; CC0. The daily weather that leaks in the record can be rejoined at the hour. Beyond 2023 the national 'Ist-Daten' of ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
