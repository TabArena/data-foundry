---
unique_name: be_a_trailblazer_kenya
name: be-a-trailblazer-kenya
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
- https://zindi.africa/competitions/be-a-trailblazer-kenya/data
- https://zindi.africa/competitions/be-a-trailblazer-open-to-all/data
- https://zindi.africa/competitions/be-a-trailblazer-south-africa
- https://zindi.africa/competitions/be-a-trailblazer-nigeria
source_row: 904
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): re-runs of the Urban Air Pollution data, recorded as `urban_air_pollution_challenge`; not the ward-level task of `be_a_trailblazer` that the old AI paragraph assumed.
- Source: Zindi, "Trailblazers Kenyan Qualification Challenge" and its siblings (Nigerian, South African, Open to All), all 2022-06-24 to 2022-09-25; the Zindi API chains them (kenya -> parent nigeria -> parent south-africa), and their Description and Data Description repeat the #ZindiWeekendz Urban Air Pollution Challenge (2020-04-10) word for word.
- As published: daily PM2.5 per city as the target, with GFS weather and Sentinel 5P L3 pollutant columns, "the last three months, spanning hundreds of cities"; submission keyed 'Place_ID X Date' (PROV-5: confirmed by the identical text and submission format).
- Siblings and duplicates: `urban_air_pollution_challenge` (AI `TBD -> 2nd Tier`, `Time-series (Forecasting)` as a concern) carries the task, first published in 2020 (PROV-8); `urban_air_pollution_challenge_daust_students` is another copy (AI `No`, `Duplicate`).
- Metric: RMSE (Zindi Evaluation page), as in the original.
- The domain on this record (`social science`) is wrong for this data (environmental science & climate); moot under `No`.
- Reject check (AI, 2026-10-22): stands. The Zindi parent chain (kenya -> nigeria -> south-africa) ends without a parent link, but the files are byte-identical to urban-air-pollution-challenge (2020): Train 37,182,338 / Test 19,024,059 / SampleSubmission 371,151 bytes. The Data Description and Evaluation (RMSE, 'Place_ID X Date') are the same text. The task is kept in urban_air_pollution_challenge (PROV-4, PROV-8).

A regional variant (Kenya plus open/South Africa/Nigeria editions) of the 'Be a Trailblazer' challenge, with no comments in the record but presumably the same ward-level socioeconomic prediction (e.g. female-headed / below-income-threshold proportions). Same concerns as the parent challenge: aggregated geographic targets, possibly few rows, and likely overlap/duplication across the regional editions. A human must confirm the exact target, row count, feature set, and whether these editions are duplicates that should be consolidated.
