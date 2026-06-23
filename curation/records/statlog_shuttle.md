---
unique_name: statlog_shuttle
name: Statlog (Shuttle)
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Missing source information
- Data Quality Issue
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://doi.org/10.24432/C5WS31
- https://www.openml.org/d/40685
source_row: 543
type_adapter_id: curation-record-v1
---

# Statlog (Shuttle)

## Comments

CC: "UCI says "The examples in the original dataset were in time order, and this time order could presumably be relevant in classification.   However, this was not deemed relevant for StatLog purposes, so the order of the examples in the original dataset was randomised, and a portion of the original dataset removed for validation purposes." Need to check whether there is temporal leakage - Yes there is - clearly trees almost perfectly predict the data"

We don't have temporal indicators, and thus cannot use it for benchmarking?

Need to see if we can find the original order again

Cannot find original data, data is also too old. For now I would mark it as TBD and we can try again later but not with a high prio
