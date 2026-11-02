---
unique_name: drug_solubility_binary_solvent_mixtures
name: Drug solubility in binary solvent mixtures at various temperatures
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Github
year: '2024'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://github.com/chemcognition-lab/chemixhub/tree/main/datasets/drug-solubility
- https://doi.org/10.1186/s13321-024-00911-3
- https://arxiv.org/abs/2506.12231
- https://github.com/Christine-Allen-Lab/Solubility_ML
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: about 27,000 measured solubilities (LogS, S in g/100 g) of 123 solutes in 110 binary solvent mixtures at several temperatures, compiled from 125 papers (2019 on) by Bao et al. 2024 with a split grouped by solute-mixture system; a real solvent-selection regression, while `bigsoldb_2` (MixtureSolDB, 175,166 values, 2026) holds the same task at six times the size.
- Source: Bao, Tom, Cheng, Watchorn, Aspuru-Guzik, Allen, "Towards the prediction of drug solubility in binary solvent mixtures at various temperatures using machine learning", J Cheminform 16:117 (2024), doi 10.1186/s13321-024-00911-3; data and code on GitHub (Christine-Allen-Lab/Solubility_ML, MIT; `20240621_Dataset_Raw_Exp.xlsx` with xtb solute and solvent descriptors, in an original and an expanded variant). As published (Methods, PMC11520512): a Web of Science search for "solubility" and "binary system", research articles since 2019, 125 papers; 27,000 points, 123 solutes, 44 solvents, 110 binary mixtures, 373 solute-mixture systems. CheMixHub's copy (`raw_data/DrugSolubilityData.csv`, 3.8 MB): LogS, temperature (K), drug and two solvents (names and SMILES), composition percentages, plus `Predict LogS`, `Predict uncertainty LogS` and `Train_Test_Label` from a model; the run's counts (27,166 rows, 3,259 systems, 169 molecules) are CheMixHub's and differ from the paper's.
- Use case: a formulation or process chemist, before running experiments, picks the solvent mixture, ratio and temperature in which a drug dissolves (crystallisation, formulation); the paper validates prospectively on four drugs with in-house measurements; fit approximate (the paper names the field, not a decision). Regime grouped: by solute (a new drug) or by solute-mixture system, as the paper's GroupShuffleSplit (75/25, ten-fold group CV); rows of one system at many ratios and temperatures are near-duplicates.
- Siblings and duplicates: `bigsoldb_2` (MixtureSolDB: 175,166 values, 810 solutes, 3,001 systems, 1,115 articles, 2026, CC BY 4.0) is the same task from another compilation; rows likely overlap (both from the published literature), so not a duplicate by provenance (PROV-4) but the larger set, to compare at add time. Aqueous or single-solvent records (`aqsoldb`, `tdc_aqsoldb`, `somas_aqueous_solubility`, `solprop_solvation_free_energy`) are other tasks. External collections: CheMixHub (arXiv 2506.12231, 2025; its `drug-solubility` task with five k-fold splits, CC BY 4.0 in its Croissant file).
- Better data: from the curator's Zotero collection (item 77, CheMixHub); no search for better data in this run.
- Papers and pages: the J Cheminform paper (LightGBM and XGBoost best, holdout MAE 0.33 LogS); CheMixHub.
- Metric: the paper reports MAE, MedAE, RMSE, MSE, PCC and SCC and ranks the models by MAE in the Results and the abstract, without naming the tuning objective (as read from PMC11520512): borderline MET-5, `mae` on LogS if read as its choice, else the fallback `rmse`; inputs none.
- Risks for /add-dataset: build from the source's xlsx, or drop `Predict LogS`, `Predict uncertainty LogS` and `Train_Test_Label` of the CheMixHub copy (a model's output, LEAK-27 if kept); molecule features computed from SMILES; rows from one paper's series are correlated; decide with `bigsoldb_2` which set enters (PROV-4).
- Priority: gap 0 (chemistry & material science, regression and grouped are not thin), use case 0 (field named, no decision), source + (paper and GitHub release), shape + (27,000 rows, numeric and molecule inputs, a group structure), risk - (a larger set of the same task, `bigsoldb_2`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 77: "CheMixHub: Datasets and Benchmarks for Chemical Mixture Property Prediction".
- as published: 27,166 measurements, 3,259 drug-solvent-solvent systems, 169 molecules; drug and two solvents (SMILES), solvent fraction, temperature; target: ln solubility (g/100 g); access: open.
- Why: experimental literature data with a direct lab decision
- Adds: solubility in mixed solvents; no solubility record exists
