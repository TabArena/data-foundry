---
unique_name: pc3
name: pc3
suggestion: 'No'
decision_markers:
- Duplicate
year: '2004'
required_split:
- '?'
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1050
- https://openscience.us/repo/defect/mccabehalsted/pc3.html
type_adapter_id: curation-record-v1
---

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: None-similartasks.

Might be outdated, but otherwise seems fine at first glance. Very related to the ones below - might consider including only one; correlates code with defects

Potential issue: Text domain (?) with custom expert features

Lennart: Unlcear if this is a tabular task; given many similar dataset with almost the same features, we should not include all of them.

Andrej: Seems fine to include, but there are many related tasks (pc1,pc2,pc3,pc4,mc1,kc1,kc2,jm1). I would suggest an additional selection step where tasks with correlated model performance results are excluded.

Duplicate of `defect_data` (NASA MDP software-defect collection; the TabArena pick from this group is `jm1`).

## Reference

Sayyad Shirabad, J. and Menzies, T.J. (2005) The PROMISE Repository of Software Engineering Databases. School of Information Technology and Engineering, University of Ottawa, Canada.
