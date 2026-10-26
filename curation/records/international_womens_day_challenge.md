---
unique_name: international_womens_day_challenge
name: international-womens-day-challenge
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
- https://zindi.africa/competitions/international-womens-day-challenge/data
source_row: 881
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): the International Women's Day Challenge (Zindi, 7 to 31 March 2025, a "Tutorial") re-runs "Womxn in Big Data South Africa: Female-Headed Households in South Africa" (Zindi, 25 November 2019 to 24 February 2020).
- Source: https://zindi.africa/competitions/international-womens-day-challenge; as published: 2011 South African census aggregated to wards, target "the percentage of households per ward that are both female-headed and earn an annual income that is below R19,600", "2,822 wards in the train set" and "1,013 wards in the test set"; the Zindi API lists Train.csv 2,049,620 bytes, Test.csv 1,113,085, SampleSubmission.csv 20,866 and variable_descriptions.csv 4,393, byte for byte the sizes of the 2019 competition, with the same data description and metric.
- Siblings and duplicates: the first publication is `womxn_in_big_data_south_africa_female_headed_households_in_south_africa` (AI `TBD -> 2nd Tier`); the dataset's merits (social science, a thin domain; ward aggregates of the same census as the target) belong on that record.
- Metric: RMSE, Zindi Evaluation page.
- Reject check (AI, 2026-10-22): stands. Zindi API: parent 'womxn-in-big-data-south-africa-female-headed-households-in-south-africa' (2019-11-25 to 2020-02-24), with identical files: Train.csv 2,049,620, Test.csv 1,113,085, SampleSubmission.csv 20,866, variable_descriptions.csv 4,393 B. The 2019 record (AI TBD -> 2nd Tier) carries the dataset. https://zindi.africa/competitions/international-womens-day-challenge

The target is the percentage of households per ward that are female-headed and earn below R19,600, i.e. an aggregate areal/census regression at ward level rather than individual-record prediction. Aggregated census-ward targets are small in row count and lean toward a descriptive/scientific-discovery framing, which weakens the representative-tabular case. It is a real regression task and not obviously out of scope, so 2nd Tier is appropriate pending checks. A human must verify the number of wards (rows), feature richness, and whether the target/features cause aggregation leakage.

---

predict percentage of households per ward that are both female-headed and earn an annual income that is below R19,600
