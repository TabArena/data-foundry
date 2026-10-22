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

**Assessment (AI, 2026-10-22):** agree with the curator's `No` (CC: "No (after preprocessing)"); the AI-set `TBD -> 2nd Tier` above contradicts that CC line, so the curator may want to restore `No`; the curator has the call.
- Source: UCI 887, "National Health and Nutrition Health Survey 2013-2014 (NHANES) Age Prediction Subset" (https://doi.org/10.24432/C5BS66, read through the UCI API): 6,287 instances listed, 7 features (gender, weekly physical activity, BMI, fasting glucose, diabetes answer, oral glucose tolerance, insulin), target `age_group` ("respondents 65 years old and older were labeled as 'senior' and all individuals under 65 years old as 'non-senior'"), `RIDAGEYR` (exact age) shipped with role Other; data from CDC/NCHS NHANES 2013-2014; intro paper Dinh et al. 2019 (BMC Medical Informatics and Decision Making), which predicts diabetes and cardiovascular disease, not age.
- Use case: none: age is known at every point where these labs are taken, so nobody predicts "senior" from glucose and BMI (SEL-3, USE-1); `RIDAGEYR` would decide the label (fixable, but the task stays). `No Good Target  / Scientific Discovery` would state that better than the current `No Good Target (yet)`.
- Siblings: `nhanes_undiagnosed_diabetes` (CC 2026-10-15) is the NHANES task with a decision (screening for undiagnosed diabetes, 1999-2023 cycles, temporal), and its notes already name this record as a 2013-2014 subset with an age-group target. The curator's alternative "predict the actual age" has no decision either.
- `Data Quality Issue` does not fit the vocabulary meaning (a leak that can be dropped is not irreparable damage).
- Metric: none (no source scores this target).

NHANES health/nutrition survey data; the OpenML-style version frames an age-group prediction target but contains an 'age_group' leakage feature, and the curator marked it 'No (after preprocessing)'. A fuller raw NHANES source exists from CDC and a 2019 paper used it for diabetes/cardiovascular prediction, so a meaningful tabular predictive task may be recoverable after careful preprocessing. The current preprocessed form has a leakage problem and an unclear real target. Suggest TBD -> 2nd Tier; a human must remove the leak, define the true target (e.g. diabetes/CVD vs age), and check post-cleaning size and feature set.

---

CC: "No (after preprocessing)"

CC: "dataset was created to assess the health and nutritional status of adults and children in the United States. Task might be to predict the actual age? There is a full dataset version available: https://wwwn.cdc.gov/nchs/nhanes/search/DataPage.aspx?Component=Questionnaire&CycleBeginYear=2013 and a 2019 paper. Need to remove age_group as leak otherwise; also the real task needs to be checked"

## Reference

A data-driven approach to predicting diabetes and cardiovascular disease with machine learning
By An Dinh, Stacey Miertschin, Amber Young, S. Mohanty. 2019

Published in BMC Medical Informatics and Decision Making
