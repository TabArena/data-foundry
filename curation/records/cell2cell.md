---
unique_name: cell2cell
name: telecom churn
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- Larger IID Data
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/datasets/jpacse/datasets-for-churn-telecom?select=cell2celltrain.csv
source_row: 32
type_adapter_id: curation-record-v1
---

## Comments

"Teradata center for customer relationship management at Duke University."

Data distributions seem uniform again.

Might be fake from a game: https://www.kaggle.com/datasets/jpacse/datasets-for-churn-telecom/discussion/86887#1956995

From reading the paper, it seems this is a teaching use case and not real (ChatGPT agrees as well). We also judge the data as fake as a result.
