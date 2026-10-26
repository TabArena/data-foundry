---
unique_name: be_a_trailblazer
name: be-a-trailblazer
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: social science
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/be-a-trailblazer/data
source_row: 900
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a re-run of the female-headed households data, recorded as `womxn_in_big_data_south_africa_female_headed_households_in_south_africa`.
- Source: Zindi, "Trailblazers Qualification Challenge" (slug be-a-trailblazer), 2022-02-04 to 2022-05-01, a career-programme qualifier; the Zindi API gives its `parent` as `womxn-in-big-data-south-africa-female-headed-households-in-south-africa` (2019-11-25, Women in Big Data South Africa and Microsoft).
- As published: the same Description and Data Description as the 2019 challenge: the percentage of households per ward "that are both female-headed and earn an annual income that is below R19,600", aggregated from the 2011 census, "2,822 wards in the train set and ... 1,013 wards in the test set"; only the HERE GIS paragraph is replaced by "GIS platforms and software may not be used" (PROV-5: confirmed by the parent link and the identical text and counts).
- Siblings and duplicates: the parent record (AI `TBD -> 2nd Tier`, unverified) and `international_womens_day_challenge` (the same target text; probably another re-run, to check there) carry the task; its first publication is the 2019 challenge (PROV-8).
- Metric: RMSE (Zindi Evaluation page), as in the parent.
- Reject check (AI, 2026-10-22): stands. Zindi API: parent = womxn-in-big-data-south-africa-female-headed-households-in-south-africa (2019). The files are byte-identical in size: Train.csv 2,049,620 / Test.csv 1,113,085 / SampleSubmission 20,866 / variable_descriptions 4,393. The task is kept in the womxn record (PROV-4).

Zindi 'Be a Trailblazer' challenge: predict the percentage of households per ward that are female-headed and living below an income threshold, i.e. a regression on aggregated census/ward-level socioeconomic features. The target is an aggregate proportion, which can be a valid regression task but raises representativeness questions (few rows = number of wards, ecological/aggregated data). A human must verify the number of wards (rows), the feature set (census-derived), and whether the sample size is adequate; aggregated-geography targets can be too small or not representative.

---

predict percentage of households per ward that are female-headed and living below a particular income threshold
