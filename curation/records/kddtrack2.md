---
unique_name: kddtrack2
name: kddtrack2
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/code/shivashi11/ad-click-prediction
source_row: 328
type_adapter_id: curation-record-v1
---

# kddtrack2

## Comments

CTR task, must be low latency; technically a bad task for typical predictive ML as a result; very different baselines to normal ML models (not even Catboost etc)

Need to check preprocessing to join with other tables, need to verify if impressions is leaking; need to create target; need to create features
