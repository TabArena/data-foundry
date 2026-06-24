---
unique_name: fremtpl2
name: freMTPL2
checked_by:
- AI (UNVERIFIED)
suggestion: 'Yes'
tags:
- AI-Filled (Verify)
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/karansarpal/fremtpl2-french-motor-tpl-insurance-claims
source_row: 1044
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

freMTPL2 is the well-known French Motor Third-Party Liability insurance dataset from CASdatasets, a standard actuarial benchmark. The canonical predictive task is claim frequency modelling (Poisson/count regression of claim number against exposure and policy features), a genuine real-world tabular regression/count task that is widely used and adequately sized (hundreds of thousands of policies). It maps cleanly to the criteria: unique original source, real predictive target, representative tabular data, no ethical issue. Note it comes as freq + severity tables (freMTPL2freq / freMTPL2sev) so a human should confirm which table/target is used and how exposure is handled; an IID split is standard.

---

Also see https://arxiv.org/abs/2605.22892 and https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf
