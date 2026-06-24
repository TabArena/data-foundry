---
unique_name: nhanes_age_prediction
name: NHANES_age_prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
- No Good Target (yet)
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2013'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.24432/C5BS66
source_row: 817
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

NHANES health/nutrition survey data; the OpenML-style version frames an age-group prediction target but contains an 'age_group' leakage feature, and the curator marked it 'No (after preprocessing)'. A fuller raw NHANES source exists from CDC and a 2019 paper used it for diabetes/cardiovascular prediction, so a meaningful tabular predictive task may be recoverable after careful preprocessing. The current preprocessed form has a leakage problem and an unclear real target. Suggest TBD -> 2nd Tier; a human must remove the leak, define the true target (e.g. diabetes/CVD vs age), and check post-cleaning size and feature set.

---

CC: "No (after preprocessing)"

CC: "dataset was created to assess the health and nutritional status of adults and children in the United States. Task might be to predict the actual age? There is a full dataset version available: https://wwwn.cdc.gov/nchs/nhanes/search/DataPage.aspx?Component=Questionnaire&CycleBeginYear=2013 and a 2019 paper. Need to remove age_group as leak otherwise; also the real task needs to be checked"

## Reference

A data-driven approach to predicting diabetes and cardiovascular disease with machine learning
By An Dinh, Stacey Miertschin, Amber Young, S. Mohanty. 2019

Published in BMC Medical Informatics and Decision Making
