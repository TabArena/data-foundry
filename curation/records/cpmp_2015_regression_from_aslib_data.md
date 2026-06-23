---
unique_name: cpmp_2015_regression_from_aslib_data
name: CPMP-2015-regression from aslib_data
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
year: '2013'
source_links:
- https://www.openml.org/d/41700
- https://github.com/coseal/aslib_data/tree/master/CPMP-2015
source_row: 697
type_adapter_id: curation-record-v1
---

# CPMP-2015-regression from aslib_data

## Comments

CC: "Algorithm selection task. Runtime prediction. Had custom train/test split. Likely requires grouped split; otherwise leakage"

We already have two datasets from AsLib, we can add more later if we really want to.
Moreover, for these the task is a bit unclear as they treat multi-label as regression task but it is hard to know if that is the optimal solution (instead of pairwise, etc). We could include all kinds of versions in the future, but again, too much of the same might add a negative bias
