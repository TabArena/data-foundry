---
unique_name: axa_vehicle_insurance_claim_challenge
name: AXA Vehicle Insurance Claim Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/umojahack-nigeria
source_row: 1020
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi AXA/UmojaHack challenge: predict whether a client will submit a vehicle-insurance claim in the next 3 months, a clear real-world binary classification with a defined target. Insurance claim prediction on policyholder records is representative tabular ML. The future-window target suggests a temporal split. A human must verify cleaned size, class imbalance (rare claims), absence of target leakage, and whether this overlaps/duplicates the AutoInland claim challenge.

---

predict if a client will submit a vehicle insurance claim in the next 3 months
