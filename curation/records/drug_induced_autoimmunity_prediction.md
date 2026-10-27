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
- Non-IID (Grouped)
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

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: the 20 RDKit fragment counts that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): ok on the hidden-group item (SMR_VSA10, SMR_VSA7): "Yes do so, it likely is a grouped dataset, in the open PRs, there is a finding from Andrej on this as well."

**Assessment (AI, 2026-10-21):** The SMR_VSA10/SMR_VSA7 groups of the hidden-group sweep are not analog series: of the values shared by two or more drugs, 17% and 20% fall within one Bemis-Murcko scaffold (adjusted Rand index against the scaffolds 0.04 and 0.08); their larger gap comes from the value 0 (68 and 79 drugs) landing in one test fold, a shift on an informative feature. No two source rows share a canonical SMILES; without stereo marks the 9 known stereoisomer pairs match. The scaffold grouping of open PR #15 (Andrej; 443 groups, a drug without a ring its own group) is the series split: on the 587 drugs, untuned ROC AUC random vs scaffold-grouped (10 x 3 folds) is LightGBM 0.826 vs 0.771, random forest 0.828 vs 0.776, logistic regression 0.739 vs 0.705, in line with PR #15 (TabPFN 0.854 vs 0.803). Recommend merging PR #15's grouping and rebuilding; this branch leaves `dataset.py` IID because PR #15 edits the same file (issue 1 of the folder's REVIEW.md). The curator has the call.

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: the 20 RDKit fragment counts (fr_*) that hold only 0 and 1 stay numeric; `_feature_types` only.

CC (2026-10-21, Lennart): make this dataset grouped here as well ("we want to have the correct state here as well and fix the issue going forward"); PR #15 is updated later as needed.

**Assessment (AI, 2026-10-21):** PR #15's scaffold grouping is now in the working copy: the split groups on the Bemis-Murcko scaffold (`murcko_scaffolds` in `data_foundry.v2.chemistry`; 443 groups, a drug without a ring its own group), `dataset check` 0 errors and 0 warnings. Measured on the 587 drugs, untuned LightGBM ROC AUC 0.771 grouped against 0.826 random; the hidden-group probe's SMR_VSA10/SMR_VSA7 groups do not follow the scaffolds (adjusted Rand 0.04 and 0.08) and need no split of their own. Andrej's question on MACCS keys stays open on PR #15. Needs a rebuild.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Huang, Liu & Huang 2024 (InterDIA) report AUC, accuracy, sensitivity, specificity, F1 and MCC side by side, no unique metric (MET-5).

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
