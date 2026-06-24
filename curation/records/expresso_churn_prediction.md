---
unique_name: expresso_churn_prediction
name: expresso-churn-prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- Review Prio 1 (Atlas)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/expresso-churn-prediction/data
- https://zindi.africa/competitions/dsn-pre-bootcamp-hackathon-expresso-churn-prediction-challenge
- https://zindi.africa/competitions/customer-churn-prediction-learning-experience/data
- https://zindi.africa/competitions/expresso-churn-prediction-challenge
- https://zindi.africa/competitions/microsoft-x-dsn-free-ai-classes-in-every-city-hackathon-expresso-churn-prediction/data
source_row: 912
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Expresso (telecom operator in Senegal & Mauritania) customer churn prediction (Zindi). One row per customer (~2.5M) with usage/tenure features aggregated over a 90-day window; target is binary churn. No explicit per-row time index, so a random split is plausible; verify there is no hidden temporal leakage from the aggregation window. Real telco data with a clear task → likely usable for the benchmark, pending verification of size after cleaning and of the split regime.
