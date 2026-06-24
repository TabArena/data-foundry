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
- 2nd Tier / Scientfic Discovery
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

OpenML 42732 San Francisco police incident reports (2003-2018), where the typical task is predicting crime category/resolution; it is already a TabArena Reject. The curator flags ethical problems (predictive policing bias, collection bias) and notes it would need a temporal split and that a newer version exists. Given the documented ethical concerns and biased collection, it is excluded; a human could instead consider a fresh, ethically reviewed extract if desired.

---

CC: "Interesting task, but actually requires temporal split. Could also argue that with the given features random is fine, but I believe that violent crimes may also be clustered around certain dates (i.e. due to demonstrations); moreover, the data might be biased during collection" 

Ethical problems, and we could just get a newer version
