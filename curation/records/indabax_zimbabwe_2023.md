---
unique_name: indabax_zimbabwe_2023
name: indabax-zimbabwe-2023
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/indabax-zimbabwe-2023/data
source_row: 982
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9; `Duplicate`, PROV-4): the IndabaX Zimbabwe 2023 hackathon (21 to 23 July 2023) is the "Insurance Recommendation Challenge", a re-run of the Zimnat Insurance Recommendation Challenge (Zindi, 1 July to 13 September 2020).
- Source: https://zindi.africa/competitions/indabax-zimbabwe-2023; as published: one row per customer with joining date, birth year, occupation, branch and 21 product columns; in Test "ONE product has been removed" and the task is "to predict the missing product" for Zimnat, which "wants an ML model ... to predict which kinds of insurance products to recommend to customers".
- Why out: a next-product recommendation task (SEL-9); the files match the 2020 competition byte for byte (Train.csv 2,424,810, Test.csv 832,462, SampleSubmission.csv 3,570,017 bytes in both Zindi APIs), so it also ends at the same source as `zimnat_insurance_recommendation_challenge` (AI-proposed `No`, same marker).
- Metric: log loss over every customer x product pair, Zindi Evaluation page.
- Reject check (AI, 2026-10-22): stands. Zindi API: Train.csv 2,424,810, Test.csv 832,462 and SampleSubmission.csv 3,570,017 B are identical to zimnat-insurance-recommendation-challenge (2020, tagged 'Collaborative Filtering'), so it is a PROV-4 duplicate whatever the SEL-9 call; the task is to predict 'the missing product' to recommend. https://zindi.africa/competitions/indabax-zimbabwe-2023

IndabaX Zimbabwe 2023 is a Zindi hackathon with no comments describing the task; target, modality, and size are unknown. Such hackathons are typically genuine tabular prediction tasks, so missing info alone is not a rejection reason. A human must open the Zindi page to determine the target, confirm it is tabular, and check size and split regime.
