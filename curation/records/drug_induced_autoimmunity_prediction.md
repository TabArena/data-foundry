---
unique_name: drug_induced_autoimmunity_prediction
name: Drug Induced Autoimmunity Prediction
checked_by:
- Lennart
- Andrej
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

CC (2026-10-19, Andrej): Labels undocumented; not a blocker.
- The source doesn't say how negatives were chosen; likely "no autoimmune reaction reported" (as in Wu et al. 2021). A few look like gaps (venlafaxine positive, its metabolite desvenlafaxine negative). Not severe: the classic drug-induced lupus drugs are all positive.
  - Wu Y, Zhu J, Fu P, Tong W, Hong H, Chen M. Machine Learning for Predicting Risk of Drug-Induced Autoimmune Diseases by Structural Alerts and Daily Dose. Int J Environ Res Public Health. 2021;18(13):7139. doi:10.3390/ijerph18137139

CC (2026-10-19, Andrej): Split changed to scaffold-grouped; keep.
- Analog lookup under random splits: about a third of the test drugs have a close structural relative in training with the same label, and looking up the label of the most similar training drug (Tanimoto similarity of Morgan fingerprints, no model) reaches ROC AUC 0.822 against TabPFN's 0.854. Fixed by holding out whole Bemis-Murcko scaffolds (a drug's ring skeleton): the signal survives and the models still separate (LightGBM 0.815 IID vs 0.758 grouped; random forest 0.776 vs linear 0.702 on the grouped splits).
- Why a scaffold split: the use case screens new drug candidates, which come from chemical series not yet tested; the Therapeutics Data Commons ADMET benchmarks split all their endpoints by scaffold for this reason, among them drug-induced liver injury, a drug-level label like this one. The source validated on random splits (its test file is as similar to its training file as a random split is), so our scores are lower than the paper's AUC 0.88-0.89 by design.
  - Huang K, Fu T, Gao W, Zhao Y, Roohani Y, Leskovec J, Coley CW, Xiao C, Sun J, Zitnik M. Therapeutics Data Commons: Machine Learning Datasets and Tasks for Drug Discovery and Development. Proc Neural Inf Process Syst Track Datasets Benchmarks. 2021. arXiv:2102.09548
  - Bemis GW, Murcko MA. The Properties of Known Drugs. 1. Molecular Frameworks. J Med Chem. 1996;39(15):2887-2893. doi:10.1021/jm9602928
- Groups: 443 (390 ring scaffolds plus the 53 ring-free drugs, each a group of its own: they share no skeleton, and their nearest neighbour's label agrees only at the base rate, 0.925).
- Record: `required_split` set to `Grouped (NON-IID)` (was `Random (IID)`, `?`); tag `Non-IID (Grouped)` added.

CC (2026-10-19, Andrej): The source's descriptors lose structure; add MACCS keys before shipping. **For discussion with Lennart**, as it revisits his 2026-10-14 call for every SMILES dataset.
- Scaffold-grouped ROC AUC, mean of 30 splits (`~/claude_jobs/dia_review/`), by what the SMILES contributes next to the source's 176 descriptors:

  | features | LR | RF | boosting | TabPFN 3.5 |
  |---|---|---|---|---|
  | descriptors (shipped) | 0.717 | 0.770 | 0.774 | 0.803 |
  | + reactive-metabolite alerts (14) | 0.707 | 0.775 | 0.773 | 0.807 |
  | **+ MACCS keys (166)** | 0.715 | 0.795 | 0.790 | **0.826** |
  | + Morgan counts (1,024) | 0.771 | 0.816 | 0.780 | 0.816 |
  | MACCS keys alone | 0.678 | 0.826 | 0.794 | 0.825 |
  | Morgan counts alone | 0.742 | 0.753 | 0.764 | 0.788 |

- Dropping the SMILES costs accuracy. MACCS keys (166 yes/no flags for standard substructures, computed from the SMILES with RDKit) next to the source's descriptors lift the scaffold-grouped ROC AUC: TabPFN 3.5 0.803 -> 0.826 (better on 27 of 30 splits), random forest 0.770 -> 0.795, LightGBM-style boosting 0.774 -> 0.790. MACCS alone matches the descriptors (random forest 0.826). So the 2026-10-14 finding that the SMILES adds nothing holds only for the raw string as text, not for the structure in it.
- Reactive-metabolite alerts (14 SMARTS from Wu et al. 2021, aromatic amine, hydrazine, thiophene, ...) add nothing next to the descriptors (TabPFN +0.003): those descriptors already count such groups.
- Morgan counts are not the answer: for the best model they help less than MACCS (TabPFN 0.816 vs 0.826, worse on 20 of 30 splits) at six times the columns, and alone they are worse than the descriptors alone.
- Suggestion (pending Lennart): `Yes`, after `_clean` adds the MACCS keys as `maccs_*` columns from the SMILES (alongside `rdkit_descriptors`, before the SMILES is dropped) and the stereoisomer de-duplication is re-checked on the wider frame. 166 dense binary columns, unlike the ~1,000 sparse Morgan columns the 2026-10-14 round ruled out for a gain of 0.01-0.015.
  - Durant JL, Leland BA, Henry DR, Nourse JG. Reoptimization of MDL Keys for Use in Drug Discovery. J Chem Inf Comput Sci. 2002;42(6):1273-1280. doi:10.1021/ci010132r
To do: add the MACCS keys to `dataset.py` (a framework helper, as `rdkit_descriptors`), then rebuild (the build is stale).

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
