---
unique_name: sbtic_xente_credit_scoring_challenge
name: sbtic-xente-credit-scoring-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
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
- https://zindi.africa/competitions/sbtic-xente-credit-scoring-challenge/data
- https://zindi.africa/competitions/xente-credit-scoring-challenge
source_row: 930
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi Xente credit scoring challenge, predicting loan default/repayment from financial-transaction and loan features, which is a canonical real-world tabular binary classification task in finance. Credit scoring is well-suited to the benchmark with a clear target and adequate data, though it may require a temporal split since lending data is time-ordered. A human must verify whether the original data is a single table or transactions to be aggregated/joined, the exact target definition, size, and the appropriate split regime, plus the Zindi data license.
