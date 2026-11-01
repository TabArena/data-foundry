---
unique_name: flash_point_sun_morgan
name: flashpoint
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2020'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1002/minf.201900101
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/flashpoint ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/flashpoint ; original: https://figshare.com/ndownloader/files/18509711'
- https://arxiv.org/abs/2505.12534
- https://doi.org/10.6084/m9.figshare.9275210.v1
- https://github.com/cheminfo/molecule-features/blob/main/data/flashpoint/meta.yaml
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: measured flash points of ~9,900 compounds, the number that sets a chemical's flammability hazard class; one table, SMILES plus a temperature in K, with the open-cup/closed-cup mix as the open question.
- Source: Sun, Krakauer, Politowicz et al., "Assessing Graph-based Deep Learning Models for Predicting Flash Point", Mol Inform 39(6):1900101 (2020), data on figshare (doi 10.6084/m9.figshare.9275210.v1), compiled from academic papers, the Gelest catalogue, DIPPR, Lange's Handbook, the Hazardous Chemicals Handbook and PubChem (cheminfo/molecule-features `data/flashpoint/meta.yaml`). As published: the paper collected "the largest flash point dataset to date, which contains 10575 unique molecules" (arXiv 2002.11315); the public file has 14,696 rows and 9,878 unique SMILES, because "DIPPR values are excluded because they are proprietary ... the curators resolved duplicate SMILES themselves" (ChemNLP `data/tabular/flashpoint/meta.yaml`, num_points 9,878). Columns: SMILES and `flashpoint` in kelvin; one table.
- Use case: a safety or process engineer assigning the storage and transport hazard class of a compound that was never measured (the classes are fixed temperature thresholds), and screening candidate solvents before a measurement; the paper gives the purpose ("flash point ... plays an important role in preventing flammability hazards") but names no actor, so fit approximate; regime grouped on the Bemis-Murcko scaffold, because a new chemical under assessment comes from a series not yet measured (SPLIT-31 as amended 2026-10-26).
- Siblings and duplicates: no flash-point or flammability record (`grep -il flash/flammab` over `curation/records/` matches this record only); the SMILES handling follows `apistox` and the `qsar_*` family (shipped: the SMILES is dropped, RDKit 2D descriptors ship). External collections: ChemPile-LIFT config `flashpoint` (a text corpus built from this table, arXiv 2505.12534), the cheminfo/molecule-features list, awesome-chemistry-datasets, CheMixHub (Zotero item 77).
- Better data: a candidate of the benchmark ChemPile (this run searched no further).
- Papers and pages: Sun et al. 2020 (preprint arXiv 2002.11315; figshare deposit 9275210); the paper compares graph models with 12 earlier QSPR studies on the same property.
- Metric: the authors tune by nested 5-fold cross-validated RMSE and report RMSE, MAE, R² and AARE (arXiv 2002.11315, Methods and Results), so RMSE is the criterion models are selected by (MET-5) and it is also the regression fallback (MET-8); inputs none. The headline is "test R² of 0.803 and an MAE of 17.8 K".
- Risks for /add-dataset: open-cup and closed-cup measurements sit in one target column with no column saying which, and the two differ by several K for the same compound (MET-2, CLEAN); 14,696 rows collapse to 9,878 unique SMILES, so duplicate structures with disagreeing values have to be resolved (PROV-6, CLEAN); the public file is not the paper's 10,575 molecules (the DIPPR rows are gone), so sizes in papers will not match; features are the SMILES only, so descriptors are computed as for `apistox`.
- Priority: gap 0 (chemistry & material science has 12 accepted, not thin), use case + (hazard labelling), source + (paper, figshare deposit, two independent metadata files), shape + (9,878 compounds), risk - (the cup method is mixed into the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 77: "CheMixHub: Datasets and Benchmarks for Chemical Mixture Property Prediction".
- as published: 9,878 compounds (ChemNLP); in ChemPile-LIFT 108,658 text prompts over 1 config(s); target: flash point (K); access: open.
- Why: Predict the flash point of a compound, the number that sets the storage and transport hazard class | a measured hazard property with a decision tied to fixed thresholds; real compounds with their sources named per row
- Adds: | no flammability or hazard task in the benchmark. Risks: open and closed cup mixed in one column; whether licensed DIPPR rows are in the public file; the source and data-type columns are provenance, not features
- Notes: Sun et al. 2020 (Mol Inform 39:1900101), a curation of academic papers, the Hazardous Chemicals Handbook and PubChem, released on figshare. Measured property, real use case (hazard labelling). Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No ...
