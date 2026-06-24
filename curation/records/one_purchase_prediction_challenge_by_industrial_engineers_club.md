---
unique_name: one_purchase_prediction_challenge_by_industrial_engineers_club
name: One Purchase Prediction Challenge by Industrial Engineers Club
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://zindi.africa/competitions/iec-algeria-data-cup-by-temtem-purchase-prediction-challenge
source_row: 1008
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Zindi competition whose stated goal is to predict which customers will purchase again, i.e. a repeat-purchase / churn-style binary classification over customer records. This is a genuine real-world predictive task rather than CTR/ranking, and such e-commerce transaction data is typically tabular and adequately sized. It may need a temporal split and some transaction aggregation. Suggest TBD -> Yes; a human must verify the data layout (single table vs transaction log to aggregate), the exact target definition, and post-processing size.

---

predict which customer will purchase again
