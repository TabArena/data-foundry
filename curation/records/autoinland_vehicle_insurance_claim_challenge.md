---
unique_name: autoinland_vehicle_insurance_claim_challenge
name: autoinland-vehicle-insurance-claim-challenge
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
- https://zindi.africa/competitions/autoinland-vehicle-insurance-claim-challenge
- https://zindi.africa/competitions/the-smart-cube-hackathon/data
- https://zindi.africa/competitions/women-in-data-2022/data
- https://zindi.africa/competitions/indabax-ghana-autoinland-vehicle-insurance-claim
- https://zindi.africa/competitions/vehicle-insurance-claim-hackathon
source_row: 908
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi AutoInland challenge: predict whether a vehicle-insurance customer will submit a claim within the next 3 months, a clear real-world binary classification task with a defined target. Insurance claim prediction on policyholder records is a representative tabular ML problem. Because the target is a future-window event, a temporal split is likely the right protocol. A human must verify the cleaned row count, class balance (claims are typically rare), and that features are policyholder/vehicle attributes rather than leakage from the claim itself.

---

predict if a customer will submit a claim within next 3 months
