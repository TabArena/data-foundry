---
unique_name: ai4d_lab_tanzania_tourism_classification_challenge
name: ai4d-lab-tanzania-tourism-classification-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/ai4d-lab-tanzania-tourism-classification-challenge/data
- https://zindi.africa/competitions/tanzania-tourism-prediction-challenge
source_row: 901
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Predict the range (bins) of expenditure a tourist spends in Tanzania; the record specifies using the 2022 multiclass version with ~24,675 rows. This is a genuine real-world tabular classification task with a clear, meaningful target and adequate size. The record carries a Temporal tag, so the split regime needs confirmation (it may simply be the year of collection rather than a true temporal dependency, in which case an IID split fits). A human must verify the row count, the number/definition of expenditure bins, and whether a temporal or random split is appropriate.

---

predict the range of expenditures a tourist spends in Tanzania

One challenge used the cost as a regression task on 2020 data with 6476 rows, the other as multi-class classification on bins with 2022 data with 24675 rows. We would use the second dataset
