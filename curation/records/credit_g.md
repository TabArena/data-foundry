---
unique_name: credit_g
name: credit-g
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '1994'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=31
- https://doi.org/10.24432/C5NC77
notebook_path: datasets/beyond_iid/old_iid/credit_g/credit_g.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/credit_g/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Comes with a cost matrix. TabRed says that task requires time based split, but no time feature given. However, if time-invariant features are used that might not matter. Also might be outdated as nowadays other features might be used; only time dependency could be the bank's and the world's financial state as a confounding factor

Potential issue: Outdated (Deutsche Mark)

Lennart: Temporal impact unclear and not resolvable, otherwise ok and not too old

Andrej: Fits criteria, but honestly this dataset with only 1000 samples from 1994 is not representative of a credit scoring task anymore. If no better dataset is available I would not use it

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source cost_matrix {"labels":["good","bad"],"matrix":[[0,1],[5,0]],"prediction":"proba"} — the Statlog cost matrix (5 for a bad customer predicted good, 1 for the reverse; UCI german.doc, Michie et al. 1994), from probabilities by least expected cost.

CC (2026-10-21, Lennart): Unsure whether the cost matrix should score probabilities or labels (TabArena tunes thresholds); the AI's choice, probabilities with the least expected cost, is applied.

## Reference

10.24432/C5NC77
