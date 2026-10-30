---
unique_name: qsar_biodeg
name: qsar-biodeg
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2013'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1494
- https://doi.org/10.24432/C5H60M
notebook_path: datasets/beyond_iid/old_iid/qsar_biodeg/qsar_biodeg.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_biodeg/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Nice chemistry dataset with (computed) molecular propeties to predict whether the sample is ready and not ready biodegradable. Linear model among best in TabRepo

Potential issue: -

Lennart: no objection

Andrej: Matches criteria

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Mansouri et al. (2013) report error rate / NER with sensitivity and specificity, without a threshold or costs. Original rejected: NER (balanced accuracy).

CC (2026-10-30, Lennart): `N073_chemical_substructure` and `C026_chemical_substructure` are numeric: the atom-centred fragments N-073 (Ar2NH / Ar3N / Ar2N-Al / R..N..R) and C-026 (R--CX--R) count the atoms of that type (0 to 3 and 0 to 12). The definition had typed them categorical while their meaning was unknown; the dtype probe found them in the sweep after issue #34. CLEAN-14: a count stays numeric.

## Reference

Mansouri, K., Ringsted, T., Ballabio, D., Todeschini, R., Consonni, V. (2013). Quantitative Structure - Activity Relationship models for ready biodegradability of chemicals. Journal of Chemical Information and Modeling, 53, 867-878
