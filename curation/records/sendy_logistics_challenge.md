---
unique_name: sendy_logistics_challenge
name: sendy-logistics-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
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
- https://zindi.africa/competitions/sendy-logistics-challenge/data
source_row: 929
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi Sendy logistics challenge to predict delivery ETA for parcel/motorbike deliveries in Nairobi, a genuine real-world tabular regression task with order, rider, and location features. This is a strong fit for the benchmark, though it likely involves joining multiple provided tables (orders + riders) and may need a temporal split since deliveries are time-ordered. A human must confirm the target (ETA/duration), table structure to be joined, size, split regime, and license; note potential overlap with the 'sendy_logistics_challenge_2' record.
