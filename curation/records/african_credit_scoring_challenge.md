---
unique_name: african_credit_scoring_challenge
name: african-credit-scoring-challenge
checked_by:
- Andrej
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Zindi
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/african-credit-scoring-challenge/data
v2_path: datasets/_dev/tabarena-v0pt2/african_credit_scoring_challenge/dataset.py
source_row: 879
type_adapter_id: curation-record-v1
---

## Comments

**AI summary:**

Predict loan default for an African credit-scoring challenge; this is a canonical real-world tabular classification task with a clear, meaningful target in finance. The record is already partially curated (checked by Andrej, DF WIP, original_data_state One Table) and tagged both Grouped and Temporal, so the appropriate non-IID split must be respected. Credit default is exactly the kind of representative tabular ML task the benchmark wants. A human should confirm the row count, the precise split protocol (grouped by borrower and/or temporal), and that there is no target leakage from post-default fields.

---

predict loan default

**Assessment (AI, 2026-10-07):** Added as a temporal task (binary `default`, ROC AUC); the record's Grouped split and tag do not fit, since repeat customers are history known at disbursement. Three leaks are removed: the repay amounts, which grow with penalties after a default (AUC 0.907 with them, 0.639 without); 8,899 rows whose lender funds under one unit, all labelled 0 by construction; and 802 rows whose label was not settled at the data pull. Nine windows: six over the end of the 2022 Type_1 lending, three 30-day windows ending 2024-10-08; each trains only on loans settled 30 days before it starts. Linear AUC 0.649, CatBoost 0.672. Open: the window scheme, and the near-chance 2024 windows.
