---
unique_name: qsar_fish_toxicity
name: QSAR_fish_toxicity
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2015'
domain: chemistry & material science
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=44970
- https://doi.org/10.24432/C5JG7B
notebook_path: datasets/beyond_iid/old_iid/qsar_fish_toxicity/qsar_fish_toxicity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_fish_toxicity/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

related to other (Meta)QSAR datasets? autocorrelation and matrix-based descriptions

Lennart: seems real, distinict from other QSAR data

Andrej: Seems fine

**Assessment (AI, 2026-10-14):** no leak found, so the remark "might have a leak" is removed (Lennart's ask). All six descriptors are computed from the structure; the strongest (MLOGP, R² 0.42 alone) is the known link of logP to baseline toxicity. The 84 shared descriptor vectors (217 rows) are isomers whose LC50 differs within every vector; keeping one row per vector gives R² 0.571 against 0.577. The descriptors were selected on the paper's training set (726 of 908 chemicals): a mild optimism that cannot be measured.

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Cassotti et al. 2015 report R2/Q2 with RMSE on training and external sets; rmse is the regression fallback.

## Reference

Cassotti, Matteo, et al. "A similarity-based QSAR model for predicting acute toxicity towards the fathead minnow (Pimephales promelas)." SAR and QSAR in Environmental Research 26.3 (2015): 217-243.
