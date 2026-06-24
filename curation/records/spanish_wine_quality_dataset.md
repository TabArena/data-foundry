---
unique_name: spanish_wine_quality_dataset
name: Spanish Wine Quality Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Duplicate
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: Other
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/fedesoriano/spanish-wine-quality-dataset/data
source_row: 833
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Kaggle 'Spanish Wine Quality' dataset (fedesoriano) with attributes such as winery, region, type, price and a quality/rating column. The curator already flagged it as likely a duplicate of the many wine datasets and questionable as a real predictive task; quality ratings here are aggregated review scores rather than a natural deployment target. It is a plausible small tabular regression but overlaps heavily with the well-known wine-quality family and is tagged 2nd-tier/scientific-discovery. A human should verify uniqueness vs other wine datasets, the true target (quality vs price), and size after cleaning.

---

Likely a duplicate with other wine datasets and anyhow not a real predictive task?
