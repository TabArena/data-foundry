---
unique_name: national_longitudinal_survey_binary
name: national-longitudinal-survey-binary
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Duplicate
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2022'
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.nlsinfo.org/
- https://www.openml.org/d/43892
source_row: 821
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Re-upload of the NLSY data via the R fairml package with a binarized target and the original continuous target left in the data, framed as an Adult-like survey task. The curator (CC) judged it 'not a real predictive task' and it is already in the TabArena Reject collection. It is essentially survey/scientific-discovery data with a constructed target plus a leakage concern from the retained original target. Suggest No. A human should confirm the leakage and that this duplicates the well-known fairml/NLSY upload.

---

CC: "data from R package fairml, binarized target, original target still in the data. Task similar to adult dataset. Survey data. Not a real predictive task."
