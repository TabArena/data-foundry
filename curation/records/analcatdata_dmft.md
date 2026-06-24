---
unique_name: analcatdata_dmft
name: analcatdata_dmft
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Trivial
- Outdated
- Ethical Issue
- Duplicate
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/d/469
- https://pages.stern.nyu.edu/~jsimonof/AnalCatData/Data/
source_row: 399
type_adapter_id: curation-record-v1
---

# analcatdata_dmft

## Comments

CC: ""Very few simple features available, unlikely that this is a meaningful predictive task. If it would be, many other features should likely be used and ethnicity (defined as Black, White, Dark) might not be used; original goal was also more interpretability (having a certain mean); prevention (the default target) is also wrong, the goal is regression to predict DMFT at the end; this may be even leaking!""

Duplicate / part of the `analcatdata_*` family — see the `analcatdata` record for the shared assessment and source (Simonoff, *Analyzing Categorical Data*).
