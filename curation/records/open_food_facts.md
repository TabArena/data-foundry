---
unique_name: open_food_facts
name: Open Food Facts
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
- Needs extensive data wrangling
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: Other
required_split:
- Random (IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/openfoodfacts/world-food-facts
source_row: 836
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Open Food Facts is a large crowdsourced product/nutrition database (Kaggle world-food-facts) rather than a dataset with a defined predictive target. It is multi-table/database-shaped with heavy missingness and would need extensive wrangling and a chosen target (e.g. nutri-score or food category). As-is it reads as a reference/scientific-discovery table. Suggest TBD -> 2nd Tier; a human must define a meaningful, non-leaking target (e.g. Nutri-Score prediction) and assess usable row count after cleaning.
