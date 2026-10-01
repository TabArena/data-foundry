---
unique_name: jm1
name: jm1
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
year: '2004'
required_split:
- '?'
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1053
- https://openscience.us/repo/defect/
notebook_path: datasets/beyond_iid/old_iid/jm1/jm1.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/jm1/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Might be outdated, but otherwise seems fine at first glance

Potential issue: Text domain (?) with custom expert features

Lennart: see above

Andrej: Seems fine to include, but there are many related tasks (pc1,pc2,pc3,pc4,mc1,kc1,kc2,jm1). I would suggest an additional selection step where tasks with correlated model performance results are excluded.

CC (2026-10-01, Lennart): Leak audit: deduplicated to be on the safe side. 25% of rows (2,730 in 669 groups) share their code-metric vector with another row, mostly trivial modules (e.g. 173 copies of a 4-line, complexity-1 function); 88 vectors occur with both labels. A random split puts copies on both sides (LightGBM AUC 0.743 on the shipped splits vs 0.727 grouped by identical vector). The v2 definition now drops exact duplicate rows (1,973) and every copy of a vector that appears with both labels (176 rows): 10,885 -> 8,736 rows. No feature is derived from the target; the splits stay IID.

## Reference

https://openscience.us/repo/defect/
