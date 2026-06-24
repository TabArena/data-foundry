---
unique_name: college_scorecard
name: College scorecard
checked_by:
- Lennart
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
- '?'
collections:
- TableShift
- TabSTAR
source_links:
- https://www.openml.org/d/46674
- https://collegescorecard.ed.gov/
- https://tableshift.org/datasets.html#college-scorecard
source_row: 704
type_adapter_id: curation-record-v1
---

## Comments

Need to figure out real task/target. Binarized version of regression by TableShift.

Data looks good, but the group split is synthetically created and not part of the real task. Real task is just temporal and we have (de facto) data from each institution at time point T. Need to take some more time to look at the data but from the description it sounds taken out of context for the sake of the benchmark (which is fine in general, but not for us where we want to have real tasks!).
