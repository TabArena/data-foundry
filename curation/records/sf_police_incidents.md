---
unique_name: sf_police_incidents
name: sf-police-incidents
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Ethical Issue
- Time-series (Forecasting)
tags:
- 2nd Tier / Scientific Discovery
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '2018'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/42732
- The dataset was downloaded on 05.11.2018. from  https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-Historical-2003/tmnf-yvry
source_row: 845
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's `No` (CC line, TabArena Reject: "Ethical problems") stands; one counter-argument on a marker: the task is no forecast.
- Source: City and County of San Francisco, Police Department Incident Reports, Historical 2003 to May 2018 (data.sfgov.org, dataset tmnf-yvry, PDDL); OpenML 42732 (2020) took a download of 5 Nov 2018 and built the binary target `ViolentCrime` from `Category` and `Descript` (assault, robbery, forcible sex offences, kidnapping, purse snatching), dropped Category, Descript, Date, Time, Resolution, Location and PdId, and added Hour, DayOfWeek, Month, Year; 2,215,023 rows x 9 columns, incidents with several categories span several rows (`IncidntNum`).
- Use case: the target was made by the OpenML uploader ("Using this dataset for machine learning was inspired by Nina Zumel's blogpost" on impact coding), not by the source (SEL-8). The only decision it would fit is where and when to expect violent crime from district, address and time, which is predictive policing, the ethical concern the curator names (SEL-1). Once a report exists its category is known, so no actor predicts it from the report.
- Siblings and duplicates: none among the records (grep for sfgov, SF crime). The Kaggle "San Francisco Crime Classification" (2015) uses the same source; no record. External collections: TabSTAR.
- Metric: none from the source; the fallback.
- **Counter-argument (AI):** `Time-series (Forecasting)` (SEL-10) does not fit: each row is one incident classified from its own time and place, not future values of a series; the temporal split the CC asks for is a split, not a scope rule. The verdict rests on SEL-1 and SEL-8/USE-2; suggest dropping the forecasting marker. The curator has the call.


OpenML 42732 San Francisco police incident reports (2003-2018), where the typical task is predicting crime category/resolution; it is already a TabArena Reject. The curator flags ethical problems (predictive policing bias, collection bias) and notes it would need a temporal split and that a newer version exists. Given the documented ethical concerns and biased collection, it is excluded; a human could instead consider a fresh, ethically reviewed extract if desired.

---

CC: "Interesting task, but actually requires temporal split. Could also argue that with the given features random is fine, but I believe that violent crimes may also be clustered around certain dates (i.e. due to demonstrations); moreover, the data might be biased during collection" 

Ethical problems, and we could just get a newer version
