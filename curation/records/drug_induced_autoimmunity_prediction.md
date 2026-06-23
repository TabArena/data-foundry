---
unique_name: drug_induced_autoimmunity_prediction
name: Drug Induced Autoimmunity Prediction
checked_by:
- Lennart
data_foundry_status: 'Yes'
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
- '?'
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- 10.24432/C5332M
source_row: 773
type_adapter_id: curation-record-v1
---

# Drug Induced Autoimmunity Prediction

## Comments

"This dataset comprises molecular descriptors generated using RDKit," -> to ChatGPT's domain understanding, this means it collected/curated it and did not create fake data

Based on github and the descriptions, it looks like real data https://github.com/Huangxiaojie2024/InterDIA


need to check smiles ID

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
