---
unique_name: urban_air_pollution_challenge_daust_students
name: urban-air-pollution-challenge-daust-students
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
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/urban-air-pollution-challenge-daust-students/data
source_row: 938
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a 2024 student re-run of `urban_air_pollution_challenge` (2020) with the same files.
- Source: Zindi "Urban Air Pollution Challenge: DAUST Students", 18 Nov to 28 Dec 2024, 20 participants, read through Zindi's API (<https://zindi.africa/competitions/urban-air-pollution-challenge-daust-students>).
- Decisive evidence: Zindi's API lists `parent`: `urban-air-pollution-challenge` (the 2020 #ZindiWeekendz hackathon); the files are byte-identical in size to the parent's (Train.csv 37,182,338 B, Test.csv 19,024,059 B, SampleSubmission.csv 371,151 B), and the Description and Data pages repeat the parent's text ("The data covers the last three months, spanning hundreds of cities across the globe"; the sample IDs start at 2020-01-02).
- Canonical record: `urban_air_pollution_challenge` (screened 2026-10-22, `TBD -> Yes`, priority 2). The DAUST link can be kept as a `#` note on it.
- Metric: RMSE, as the parent.
- Reject check (AI, 2026-10-22): stands. PROV-4 (Must): the Zindi API (https://api.zindi.world/v1/competitions/urban-air-pollution-challenge-daust-students) lists parent = urban-air-pollution-challenge. Its three files match the 2020 parent's byte sizes exactly (Train.csv 37,182,338; Test.csv 19,024,059; SampleSubmission.csv 371,151), the Data page is word for word the same, and the metric is the same (RMSE). It is a 2024 class re-run (20 participants) with no distinct task (PROV-7 does not apply). The canonical record is urban_air_pollution_challenge (TBD -> Yes, priority 2).

This is a student/practice variant ('daust-students') of the Urban Air Pollution Challenge, almost certainly re-using the same data and target as the main challenge. It is therefore a duplicate / re-upload rather than a unique original source. A human should confirm it shares data with urban_air_pollution_challenge, but it should be rejected as a duplicate; the original entry (if any) carries the canonical decision.
