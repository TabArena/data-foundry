---
unique_name: absa_customer_income_prediction_challenge
name: absa-customer-income-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
tags:
- New IID
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: finance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/absa-customer-income-prediction-challenge/data
source_row: 896
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Predict a bank customer's income from their transaction history, tagged 'New IID' by curators. This is a genuine real-world tabular regression task in finance with a clear, meaningful target. The main caveat is that transaction-level data must be aggregated to one row per customer, so it requires non-trivial feature engineering and the final row count after wrangling is unknown. A human must verify the post-aggregation table size, that the target is true income (not leakage from balance), and the absence of ethical issues around financial profiling.

---

predict a customer's income based on their transaction history
