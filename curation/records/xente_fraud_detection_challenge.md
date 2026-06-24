---
unique_name: xente_fraud_detection_challenge
name: xente-fraud-detection-challenge
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
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/xente-fraud-detection-challenge/data
- https://zindi.africa/competitions/xente-fraud-dection-hackathon
- https://zindi.africa/competitions/indabax-benin-2022/data
- https://zindi.africa/competitions/multimedia-university-of-kenya-hackathon/data
source_row: 927
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Xente fraud detection (Zindi) is a transaction-level financial fraud classification task with a clear binary target (fraudulent vs not) and standard tabular transaction features (amount, channel, product, customer/timestamp). This is a representative real-world tabular classification problem, well known, and likely benefits from a temporal split given timestamps. The main caveats are extreme class imbalance and the need to confirm dataset size and feature usability after cleaning. Provisionally a Yes pending human verification of size, target, and leakage.
