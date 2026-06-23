---
unique_name: treasury
name: treasury
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
year: '2000'
source_links:
- https://www.openml.org/d/42367
- keel https://sci2s.ugr.es/keel/dataset.php?cod=42 -> http://funapp.cs.bilkent.edu.tr/DataSets/
source_row: 541
type_adapter_id: curation-record-v1
---

# treasury

## Comments

CC: "Temporal component, but unclear whether task is time-invariant"

"This file contains the Economic data information of USA from 01/04/1980 to 02/04/2000 on a weekly basis. From given features, the goal is to predict 1 Month CD Rate."

Date time column is gone. Needs temporal split. Unresolvable data issues. Could be time-invariant and still used, but otherwise task is wrong
