---
unique_name: uk_mot_test_results
name: Anonymised MOT tests and results (DVSA)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.data.gov.uk/dataset/c63fca52-ae4c-4b75-bab5-8b4735e1a4c9/anonymised-mot-tests-and-results
- https://open.data.dvsa.gov.uk/mot-anonymised/index.html
- '# user guide (post-May 2018), v5.1'
- https://edh-dvsa-data-gov-uk-files-prod.s3.eu-west-1.amazonaws.com/mot-testing-data-user-guide-v5.1.odt
v2_path: datasets/_dev/tabarena-v0pt2/uk_mot_test_results_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 3: every MOT test in Great Britain since 2005 (DVSA, OGL), about 42 million tests a year with the vehicle's make, model, age, mileage and fuel and the result; DVSA itself describes a vehicle-failure model for its enforcement officers, but each test carries only ten inputs before the vehicle's earlier tests are joined.
- Source: Driver and Vehicle Standards Agency, "Anonymised MOT tests and results" on data.gov.uk and open.data.dvsa.gov.uk (OGL v3.0): "All MOT tests and outcomes, including make and model of vehicle, odometer reading and reasons for failure, since the MOT system was computerised in 2005". data.gov.uk holds 2023 and 2024, the DVSA portal 2022-2025, and older years sit in a DfT dataset of the same name. User guide v5.1 (read): a test-result table (one row per test) and a failure-item table (Reasons for Rejection, joined by test id), plus lookups. Test-result columns: `test_id`, `vehicle_id` ("based upon the Registration and VIN", so a vehicle is tracked over time), `test_date`, `test_class_id`, `test_type` (NT normal, RT retest, PL and PV partial retests, ES appeal), `test_result` (P, F, PRS, ABA, ABR), `test_mileage`, `postcode_area`, `make`, `model`, `colour`, `fuel_type`, `cylinder_capacity`, `first_use_date`; 2024 adds `completed_date`. As published: 2023 is one pipe-separated file of 3.66 GB (1.19 GB zip); a 72k-row preview gives 86 bytes a row, so about 42 million rows (estimate), 93% normal tests, results P 70%, F 23%, PRS 6%. 2024 ships 12 monthly CSVs (1.53 GB zip, about 7.7 GB unpacked); a preview of January gives about 6 million rows, more than one month should hold, so the monthly files need a check.
- The task's table: one row per normal test (type NT) with a result of P, F or PRS, the target a fail at the initial test (F or PRS, as DVSA's "initial failure rate" counts it), about 39 million a year (estimate) x 10 inputs (test date, class, mileage, postcode area, make, model, colour, fuel type, cylinder capacity, first-use date), plus the vehicle's earlier tests through `vehicle_id` (previous result, mileage and failure items; an entity's own history, LEAK-34). Access: open, OGL, zips of 0.5 to 1.5 GB a year, no login.
- Use case: DVSA's enforcement officers compare each recorded result with the predicted chance of failure to find testers and garages whose results look wrong. DVSA's blog (Neil Barlow, 2019-06-10, "Getting smart on MOT fraud") describes "expanding the risk ratings algorithm to include a 'predictive vehicle failure model'" to "help our officers to better understand the likelihood of a vehicle passing or failing its MOT". Fit direct. Regime temporal by test date; vehicles recur yearly, so their history is a feature (USE-10).
- Siblings and duplicates: no other MOT record (grep: MOT, DVSA, roadworthiness); `fmcsa_roadside_inspection_out_of_service` (a candidate of this run) is a US truck-inspection outcome, another source and task. External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08).
- Papers and pages: the user guide; the DVSA blog; a hobby project (github.com/adin786/mot-data) fits pass or fail on age and mileage for one postcode area. No paper or competition found.
- Metric: none found (the data.gov.uk page, the user guide, the DVSA blog, one web search), so the fallback `roc_auc` (MET-1, MET-8). Inputs: none.
- Risks for /add-dataset: retests follow a failure and are no task rows (drop them, or use them only as history); PRS lies between pass and fail ("Vehicle begins the test in a fail condition", guide), so the target definition is a choice (USE-5); the label is what the tester recorded, the very thing DVSA audits, so it carries tester error; mileage before 2022 is sometimes in kilometres; a first-use date of 1971-01-01 codes unknown; the defect categories changed in May 2018; history features need a join over years of 40M-row files, and the size calls for a cut (one or two recent years).
- Priority: gap 0 (no thin domain; binary and temporal covered), use case + (DVSA names the model and its users), source + (agency release with a user guide), shape + (tens of millions of tests, ten mixed inputs, vehicle history over time), risk - (thin per-test inputs, a target recorded by the audited tester, heavy history joins).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the LEAK-9 protocol line widened to 'a fold uses only its own train rows; test rows are predicted without any other test row or later-dated row', with the task gamer's 657 / 1,509 / 1,586 linked test rows and +0.0014 to +0.0027 ROC AUC, no re-split; the metric reason reworded as a ranking use, MET-8; notes on the test-month density, the odometer read at the start of the test, the vehicle record as of June 2026 and the HYBRID ELECTRIC (CLEAN) merge, CLEAN-1, CLEAN-12; fit_reason on the missing tester id, USE-1); rebuttal round skipped (briefs converged); disputed: MET-8/MET-11 (log loss from context, decided once with sivep, nyc and nchs); for the curator: issue 1. Priority 2: gap 0, use case +, source +, shape +, risk - (use case: DVSA's own failure model; risk: thin per-test inputs and a label recorded by the audited tester).
