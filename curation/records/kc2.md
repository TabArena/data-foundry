---
unique_name: kc2
name: kc2
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- Tiny Data
year: '2004'
required_split:
- '?'
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1063
- https://openscience.us/repo/defect/
type_adapter_id: curation-record-v1
---

# kc2

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

Might be outdated, but otherwise seems fine at first glance. Only 522 samples

Potential issue: Text domain (?) with custom expert features

Lennart: see above

Andrej: Seems fine to include, but there are many related tasks (pc1,pc2,pc3,pc4,mc1,kc1,kc2,jm1). I would suggest an additional selection step where tasks with correlated model performance results are excluded.

Duplicate of `defect_data` (NASA MDP software-defect collection; the TabArena pick from this group is `jm1`).

## Reference

https://openscience.us/repo/defect/
