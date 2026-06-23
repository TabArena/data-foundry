---
unique_name: cpu_act
name: cpu_act
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
- Outdated
tags:
- Non-IID (Temporal)
- New IID
collections:
- TabArena Reject
- TabSTAR
year: '2002'
source_links:
- https://www.openml.org/d/761
- DELVE repository of data.
- https://www.openml.org/search?type=data&id=44978
source_row: 554
type_adapter_id: curation-record-v1
---

# cpu_act

## Comments

CC: "Actually regression, Data collected on two separate occasions - likely need custom split, also everything related to CPU performance may be outdated, depending on how old the data is; includes different user behavior as well; cpu activity is also related to outside temperatures and usage that depend on time"
"The data was collected continuously on two separate occasions"

No time information to create a temporal split.

Very likely not representative of tasks currently used to estimate this performance / in general empirical performance models

## Reference

Luis Torgo (ltorgo@ncc.up.pt) at http://www.ncc.up.pt/~ltorgo/Regression/DataSets.html
