---
unique_name: chocolate_bar_ratings
name: Chocolate Bar Ratings
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Non-IID (Temporal)
- Free Text (Short)
collections:
- CARTE/TARTE
- MulTaBench
- STRABLE
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/rtatman/chocolate-bar-ratings
- https://flavorsofcacao.com/index.html
source_row: 553
type_adapter_id: curation-record-v1
---

## Comments

Chocolate ratings; contains duplicated entries for review (version history).

The task would be to predict the ratings of an individual for a new bar. This seems not to make much sense as a real predictive task, and it is unclear if it is even meaningfully predictable or worthy to predict. While this is not a scientific discovery task, it is also not an interesting task or domain.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `flavors_of_cacao_ratings_2026` (TBD -> 2nd Tier, priority 1). Each is screened in its own record; this record's verdict stays the curator's.
