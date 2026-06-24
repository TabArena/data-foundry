---
unique_name: credrails_banking_transaction_categoriser_challenge
name: credrails-banking-transaction-categoriser-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- NLP (Text)
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: finance
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/credrails-banking-transaction-categoriser-challenge/data
source_row: 995
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi/Credrails challenge to categorise banking transactions for an API. Transaction categorisation is typically driven by free-text transaction descriptions/merchant strings, which makes it primarily an NLP (text-classification) task where text models tend to dominate, rather than a representative numeric/categorical tabular task. It could be partly tabular if amount, channel, and other structured fields carry most of the signal. A human must inspect the feature set to see whether the predictive signal is mostly in text fields versus structured columns, plus the number of target categories and the data size.

---

categorise banking transactions for the Credrails API
