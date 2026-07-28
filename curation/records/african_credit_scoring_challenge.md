---
unique_name: african_credit_scoring_challenge
name: african-credit-scoring-challenge
checked_by:
- Andrej
- AI (UNVERIFIED)
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: finance
required_split:
- Grouped (NON-IID)
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/african-credit-scoring-challenge/data
source_row: 879
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Predict loan default for an African credit-scoring challenge; this is a canonical real-world tabular classification task with a clear, meaningful target in finance. The record is already partially curated (checked by Andrej, DF WIP, original_data_state One Table) and tagged both Grouped and Temporal, so the appropriate non-IID split must be respected. Credit default is exactly the kind of representative tabular ML task the benchmark wants. A human should confirm the row count, the precise split protocol (grouped by borrower and/or temporal), and that there is no target leakage from post-default fields.

---

predict loan default
