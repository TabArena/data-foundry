---
unique_name: clickthrough
name: ClickThrough
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/competitions/avazu-ctr-prediction
source_row: 329
type_adapter_id: curation-record-v1
---

## Comments

Temporal by days, potentially grouped by websites which we have data for given the last day! IP, website, and domains have many high-cardinality features, requires group-aware preprocessing or other clever tricks, otherwise rather weird data. Again CTR which makes it questionable.
