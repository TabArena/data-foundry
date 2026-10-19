---
unique_name: drug_induced_autoimmunity_prediction
name: Drug Induced Autoimmunity Prediction
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: UCI
year: '2025'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5332M
notebook_path: datasets/beyond_iid/new_iid/drug_induced_autoimmunity_prediction/drug_induced_autoimmunity_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/drug_induced_autoimmunity_prediction/dataset.py
source_row: 773
type_adapter_id: curation-record-v1
---

## Comments

"This dataset comprises molecular descriptors generated using RDKit," -> to ChatGPT's domain understanding, this means it collected/curated it and did not create fake data

Based on GitHub and the descriptions, it looks like real data https://github.com/Huangxiaojie2024/InterDIA


need to check SMILES ID

CC (2026-10-14, Lennart): Drop the SMILES as a feature, as in every SMILES dataset; the source's RDKit descriptors carry the structure.

**Assessment (AI, 2026-10-14):** The SMILES as text lowered LightGBM's ROC AUC from 0.835 to 0.810 (15 of 15 splits). Without it 9 pairs of stereoisomers share every descriptor (PubChem: quinine and quinidine, and eight drugs entered twice with other stereo marks, streptomycin once as positive and once as negative), 3 pairs across the source's train and test files. One row of each pair is kept and both streptomycin rows are dropped, as for qsar_oral_toxicity: 587 drugs, 140 positive.

## Reference

@article{huang2025interdia,
  title={InterDIA: Interpretable prediction of drug-induced autoimmunity through ensemble machine learning approaches},
  author={Huang, Lina and Liu, Peineng and Huang, Xiaojie},
  journal={Toxicology},
  volume={511},
  pages={154064},
  year={2025},
  publisher={Elsevier}
}
