---
unique_name: hpdmobile_home_occupancy
name: 'HPDmobile: A High-Fidelity Residential Building Occupancy Detection Dataset'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Time-series (Classification)
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '2021'
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1038/s41597-021-01055-x
- https://doi.org/10.6084/m9.figshare.c.5364449.v1
- https://doi.org/10.6084/m9.figshare.14368538
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: whole-house occupancy of six Colorado homes from indoor environmental sensors, labelled from phone geofences and paper logs, published as a Scientific Data descriptor; a 10-second sensor stream that needs aggregation and a split by home or by time.
- Source: Jacoby, Tan, Henze, Sarkar, "A high-fidelity residential building occupancy detection dataset", Scientific Data 8:280 (2021), doi 10.1038/s41597-021-01055-x; data on figshare (collection 10.6084/m9.figshare.c.5364449); University of Colorado Boulder with Iowa State, the HPDmobile system. As published: six homes (H1-H6) with 30, 17, 35, 17, 15 and 38 released days and 4-5 sensor hubs each, in common areas; environmental readings every 10 seconds (temperature, relative humidity, eCO2, TVOC, illuminance), one CSV per hub per day of 8,640 rows; 32x32 grey images at one frame per second and processed audio; ground truth one CSV per day, whole-house occupied or vacant with an estimated occupant count; occupied shares 82, 61, 78, 82, 76 and 47% (Table 2). Ground truth: "every occupant was required to carry a cell phone with GPS location on them whenever they left the house", reconciled with paper logs.
- Use case: a smart thermostat or HVAC controller sets back heating and cooling while the home is empty; the descriptor names it ("by including occupancy information in model predictive control strategies", "moderate temperature setbacks as a result of vacancy information could still lead to some energy savings"). Fit direct for the environmental modality. Regime grouped by home (six homes) or temporal within a home; rows must be aggregated to control intervals.
- Siblings and duplicates: `occupancy_detection_2` (`TBD -> Yes` by Lennart, with `Time-series (Classification)`, `Trivial`, `Not Representative`: one office room, per minute) and its copy `occupancy_detection` (`No`); `robod_room_occupancy` (a candidate of this run: five rooms of a Singapore university building, another source, not a duplicate under PROV-4). External collections: none found.
- Better data: found as better data for `occupancy_detection_2`; no further search this round.
- Papers and pages: the descriptor (Methods; Ground truth establishment; Technical Validation); github.com/mhsjacoby/HPDmobile (collection and processing code).
- Metric: none for the environmental task: the technical validation scores a kNN on audio by accuracy and checks the image labels by TPR, TNR, PPV and NPV (Tables 4-5), with no occupancy model on the sensors; so the fallback `roc_auc` (MET-8). Inputs none.
- Risks for /add-dataset: images and audio stay out (SEL-12), only the environmental columns; illuminance and eCO2 may make the task near trivial (TP-4, as `occupancy_detection_2` was flagged); the label is per home and changes a few times a day, so neighbouring rows are near copies and a split must keep whole days or homes apart (SPLIT); six homes are few groups for grouped folds (TP-5); per-hub, per-day files to align by timestamp (`Needs extensive data wrangling`).
- Priority: gap 0 (binary not thin, no thin domain), use case + (the descriptor names the setback decision), source + (a peer-reviewed descriptor with a public deposit), shape + (152 home-days of hub-level readings, a home and time structure), risk - (a sensor stream whose label is nearly constant for hours, and only six homes).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `occupancy_detection_2`.
- as published: 6 homes in Boulder, Colorado, 15 to 38 released days each (152 home-days), 4 to 5 sensor hubs per home; indoor readings every 10 s (temperature, relative humidity, eCO2, TVOC, illuminance) plus ...; target: home occupied by at least one person vs vacant (binary); access: open (CC0, figshare).
- Why: Same task as occupancy_detection_2: binary occupancy from temperature, humidity, CO2 and light readings taken at the prediction time. Ground truth from phone geofences plus paper sign-in logs reconciled with the occupants and checked against image detections (descriptor, 'Ground truth establishment')
- Adds: Six homes instead of one office room, so a split by home tests transfer to unseen buildings (the record's Not Representative marker and its note on other rooms); occupied share 47% to 82% per home; newer. Caveat: 10-second time series, so rows need aggregation to intervals and a split by home or by time; the images ...
