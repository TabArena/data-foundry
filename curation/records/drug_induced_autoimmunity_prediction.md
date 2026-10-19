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
- Grouped (NON-IID)
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

CC (2026-10-19, Andrej): Labels undocumented; not a blocker.
- The source doesn't say how negatives were chosen; likely "no autoimmune reaction reported" (as in Wu et al. 2021). A few look like gaps (venlafaxine positive, its metabolite desvenlafaxine negative). Not severe: the classic drug-induced lupus drugs are all positive.
  - Wu Y, Zhu J, Fu P, Tong W, Hong H, Chen M. Machine Learning for Predicting Risk of Drug-Induced Autoimmune Diseases by Structural Alerts and Daily Dose. Int J Environ Res Public Health. 2021;18(13):7139. doi:10.3390/ijerph18137139

CC (2026-10-19, Andrej): Split changed to scaffold-grouped; keep.
- Analog lookup under random splits: about a third of the test drugs have a close structural relative in training with the same label, and looking up the label of the most similar training drug (Tanimoto similarity of Morgan fingerprints, no model) reaches ROC AUC 0.822 against TabPFN's 0.854. Fixed by holding out whole Bemis-Murcko scaffolds (a drug's ring skeleton): the signal survives and the models still separate (LightGBM 0.815 IID vs 0.758 grouped; random forest 0.776 vs linear 0.702 on the grouped splits).
- Why a scaffold split: the use case screens new drug candidates, which come from chemical series not yet tested; the Therapeutics Data Commons ADMET benchmarks split all their endpoints by scaffold for this reason, among them drug-induced liver injury, a drug-level label like this one. The source validated on random splits (its test file is as similar to its training file as a random split is), so our scores are lower than the paper's AUC 0.88-0.89 by design.
  - Huang K, Fu T, Gao W, Zhao Y, Roohani Y, Leskovec J, Coley CW, Xiao C, Sun J, Zitnik M. Therapeutics Data Commons: Machine Learning Datasets and Tasks for Drug Discovery and Development. Proc Neural Inf Process Syst Track Datasets Benchmarks. 2021. arXiv:2102.09548
  - Bemis GW, Murcko MA. The Properties of Known Drugs. 1. Molecular Frameworks. J Med Chem. 1996;39(15):2887-2893. doi:10.1021/jm9602928
- Groups: 443 (390 ring scaffolds plus the 53 ring-free drugs, each a group of its own: they share no skeleton, and their nearest neighbour's label agrees only at the base rate, 0.925).
- Record: `required_split` set to `Grouped (NON-IID)` (was `Random (IID)`, `?`).
To do: rebuild (the build is stale).

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
