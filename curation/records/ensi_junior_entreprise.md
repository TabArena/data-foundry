---
unique_name: ensi_junior_entreprise
name: ensi-junior-entreprise
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/ensi-junior-entreprise
source_row: 1002
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi ENSI Junior Entreprise competition: predict weather temperature at a location given its X/Y coordinates. This is essentially a spatial-interpolation regression task whose covariates may be little more than coordinates, which risks being thin/not representative of general tabular ML and would need a spatial (grouped) split to avoid leakage. It is a real predictive target, so not an outright reject. A human must inspect the actual feature set (whether richer covariates exist beyond coordinates), the sample size, and the spatial split requirement before deciding.

---

Predict weather temperature at any location given by its X and Y coordinates
