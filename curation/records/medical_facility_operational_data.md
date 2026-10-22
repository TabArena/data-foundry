---
unique_name: medical_facility_operational_data
name: Medical Facility Operational Data
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Other
year: '2020'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/weirdolucifer/medical-facility-operational-data
- https://doi.org/10.7910/DVN/X4SJWS
source_row: 850
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: the Kaggle file is a re-upload of Pianykh's MGH "Operational Predictions Dataset" (Harvard Dataverse, 2020, PLoS One paper), a patient wait-time and delay regression at four imaging facilities.
- Source: Harvard Dataverse doi:10.7910/DVN/X4SJWS, "Operational Predictions Dataset", Oleg Pianykh, deposited 2020-05-24, CC0, one file `WaitData.Published.tab`. The Kaggle copy (weirdolucifer, 2021-02-10) ships the same file name, `WaitData.Published.xlsx`, and the description: "operational features, captured in four different hospital facilities, processing walk-in (F4) or scheduled (F1, F2, F3) patients ... one line per each patient visit event", with timestamps "set to the fictitious future dates ... Only their relative timing was preserved". Data paper: Crowley, Guitron, Son & Pianykh 2020, PLoS One 15(6):e0233810: F1 MRI 15,494 rows, F2 ultrasound 36,154, F3 CT 30,173, F4 X-ray 69,469 (Nov 2017-Jul 2019); 84 candidate features (congestion, customer, resource, task, time); targets delay in minutes (F1-F3) and wait in minutes (F4). Its data availability statement points to the Dataverse.
- Use case: at a patient's arrival, the facility predicts the wait or delay. The earlier MGH work put the prediction on waiting-room displays and flagged patients who waited much longer than predicted (RSNA 2014; Curtis et al. 2018, JACR). Actor: the facility's operations staff. Moment: arrival (scheduled or walk-in). Fit: direct. Regime: temporal (relative order preserved), probably per facility.
- Siblings and duplicates: none for this source (`hospital_patient_data` is a different, unsourced Kaggle wait-time upload). The old reasons "no target" and "missing source" are refuted by the Dataverse and the paper, so those markers are dropped.
- Papers and pages: Crowley et al. 2020 (the data paper); Pianykh & Rosenthal 2015 (JACR, "Can We Predict Patient Wait Time?"); Curtis et al. 2018 (JACR, ML for wait times and delays, MGH).
- Metric: MAE in minutes. Crowley et al. Table 2 is "Predictive performance, measured by mean absolute error", while MSE drives their feature selection and they also give a ratio to an intercept-only model. MAE looks like the deliberate criterion; confirm under MET-5. Inputs: none beyond the rows; the facility is a column.
- Risks for /add-dataset: "captured at the time of patient arrivals and departure", so some features may be known only after the wait (LEAK; check each of the 84 against the arrival moment). Also one task or four: wait (F4) and delay (F1-F3) are different targets, so pick one facility or one target. The timestamps are fictitious, but their order holds for a time split.
- Priority: gap - (medical, regression, temporal: none thin), use case + (direct, named by the source), source + (Dataverse and paper), shape + (about 151k visits, 84 features, temporal), risk - (features recorded at departure).

A Kaggle 'Medical Facility Operational Data' dataset that is a single Excel sheet of mixed operational data with no defined task or target, per the curator's note. Without a clear predictive target it reads as a scientific-discovery / listing table rather than a benchmark task, and provenance is thin. It is tagged 2nd Tier and temporal. There is essentially no clear target to model, so it cannot be a Yes. A human would need to determine whether any meaningful operational target (e.g., occupancy, wait time) can be carved out, but as presented this is a No.

---

Unsure what the task/target could be, is one Excel sheet with a bunch of data.
