---
unique_name: sea_turtle_rescue_error_detection_challenge
name: sea-turtle-rescue-error-detection-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2018'
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/sea-turtle-rescue-error-detection-challenge/data
source_row: 924
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: predict, for each field of each rescue record, whether it was mistyped from the handwritten logbook, so Local Ocean Conservation's staff check fewer fields; a real decision, but a per-cell task whose label comes from diffing a dirty and a cleaned table.
- Source: Zindi, "Sea Turtle Rescue: Error Detection Challenge" (2018-11-30 to 2019-04-29, 329 participants), data from Local Ocean Conservation (Watamu, Kenya), By-Catch Release Programme, "unique sea turtle rescues that took place from 1998 until 2011". As published: `dirty_data.csv` (1.1 MB, "all of the data from 1998 to 2010 (except for 2008 and 2009) as they were originally entered into the database from the handwritten logbooks"), `cleaned_data.csv` (1.2 MB, the reviewed version), `variable_definitions.csv`; the submission scores one probability per rescue and field (`2011_RE_0001 x Date_Caught`, `x CaptureSite`, `x Researcher`).
- Use case: "At the end of the year, LOC staff review each rescue/field to compare the database entry with the hand-written log book"; a model that ranks fields by error probability saves that review; fit direct for the actor and moment; regime temporal or grouped by year (train on reviewed years, flag a new year; the test IDs are 2011), to settle when added.
- Siblings and duplicates: the Sea Turtle Rescue: Forecast Challenge (Zindi, 2019-11-29, weekly rescues per capture site, RMSE) is a different task and a forecast (SEL-10); it was in this record's `source_links` and is moved here as related work (PROV-12): https://zindi.africa/competitions/sea-turtle-rescue-forecast-challenge. No other record found.
- Papers and pages: https://zindi.africa/competitions/sea-turtle-rescue-error-detection-challenge.
- Metric: mean absolute error between the predicted probability and the 0/1 error flag (Zindi Evaluation: "The Mean Absolute Error will be used ... the average distance between the predicted likelihood that a entry is an error and the actual value"), a leaderboard metric (MET-4); MAE on probabilities rewards 0/1 answers rather than calibrated ones, so the curator may prefer the fallback (`log_loss` or `roc_auc`) when adding (MET-4 departure to argue).
- Risks for /add-dataset: build the target by aligning the dirty and cleaned rows field by field (keys, deleted or added rows); the unit is a cell, so the table is rows x fields with the field name as a feature; whether the cleaned values leak into features; the error rate per field may be tiny.
- Priority: gap 0, use case +, source +, shape 0 (size unknown), risk - (built target, per-cell unit).

Zindi 'sea turtle rescue error detection' challenge: the framing is detecting data-entry errors in a rescue records table, which is an unusual target and points to a data-cleaning rather than a standard predictive task; the companion link is a 'forecast' variant which would be out of scope. It is unclear whether the error-detection target yields a clean, well-defined tabular classification problem or is too idiosyncratic/trivial. A human must inspect the data and target definition to decide whether the error-detection task is a representative tabular predictive problem (and confirm the forecast variant is excluded).
