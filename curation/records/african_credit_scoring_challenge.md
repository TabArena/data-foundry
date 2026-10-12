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
notebook_path: datasets/_maintenance/_out_of_scope/_too_late_to_add/african_credit_scoring_challenge/african_credit_scoring_challenge.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/african_credit_scoring_challenge/dataset.py
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

**Assessment (AI, 2026-10-07):** Added as a temporal task (binary `default`, ROC AUC); the record's Grouped split and tag do not fit, since repeat customers are history known at disbursement. Three leaks are removed: the repay amounts, which grow with penalties after a default (AUC 0.907 with them, 0.639 without); 8,899 rows whose lender funds under one unit, all labelled 0 by construction; and 802 rows whose label was not settled at the data pull. Nine windows: six over the end of the 2022 Type_1 lending, three 30-day windows ending 2024-10-08; each trains only on loans settled 30 days before it starts. Linear AUC 0.649, CatBoost 0.672. Open: the window scheme, and the near-chance 2024 windows.
