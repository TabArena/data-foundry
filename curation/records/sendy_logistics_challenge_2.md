---
unique_name: sendy_logistics_challenge_2
name: Sendy Logistics Challenge
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
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/zindi-mentorship-2-sendy-logistics-challenge
- https://zindi.africa/competitions/edsa-sendy-logistics-challenge
source_row: 1014
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): the Zindi Mentorship #2 (2020-07-20 to 2020-08-26) and EDSA 2020 (2020-05-11 to 2020-09-07) private re-runs of the Sendy Logistics Challenge (2019-08-23 to 2019-11-25).
- Source: both pages name `sendy-logistics-challenge` as their parent in the Zindi API, repeat its description ("predict the estimated time of delivery of orders, from the point of driver pickup to the point of arrival at final destination") and ship the same files with the same byte sizes (Train.csv 4,094,263, Test.csv 1,209,061, Riders.csv 29,751, SampleSubmission.csv 117,450).
- Siblings and duplicates: the first publication is `sendy_logistics_challenge` (screened `TBD -> Yes`, priority 3, 2026-10-22); this record ends at the same source (PROV-4, PROV-8). Its two links can move to that record's comments as re-runs.
- Metric: `rmse` on seconds, Zindi Evaluation page.
- Reject check (AI, 2026-10-22): stands. PROV-4/PROV-5 confirmed from the Zindi API: zindi-mentorship-2-sendy-logistics-challenge (2020-07-20) and edsa-sendy-logistics-challenge (2020-05-11) both have parent 'sendy-logistics-challenge' (2019-08-23) and the same Train.csv 4,094,263 / Test.csv 1,209,061 / Riders.csv 29,751 / VariableDefinitions.csv 2,661 / SampleSubmission.csv 117,450 bytes; the original is the record sendy_logistics_challenge.

This is another Sendy logistics ETA-prediction competition (mentorship/EDSA re-runs) predicting estimated time of arrival for motorbike deliveries in Nairobi, a real tabular regression task. It is almost certainly the same underlying data as 'sendy_logistics_challenge' and should be de-duplicated so only one version is kept. A human must compare the two records' data files, confirm which is the canonical source, the join/table structure, target, size, and split, and drop the duplicate.

---

Predict the estimated time of arrival (ETA) for motorbike deliveries in Nairobi
