---
unique_name: oral_bioavailability_ma
name: bioavailability_ma_et_al
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 1
tags:
- AI-Filled (Verify)
collections:
- ChemPile
original_source: Other
year: '? (2008)'
domain: chemistry & material science
problem_type: Binary Classification
source_links:
- https://doi.org/10.1016/j.jpba.2008.03.023
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/bioavailability_ma_et_al ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/bioavailability_ma_et_al ; original: https://tdcommons.ai/single_pred_tasks/adme/#bioavailability-ma-et-al'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 1: human oral bioavailability of 640 drugs as a binary label from the structure, a classic ADME task like the accepted QSAR sets, but small, from 2008, and cut at a threshold the sources read do not state.
- Source: Ma, Yang, Zhang, Xiang, Huang and Wei, "Prediction models of human plasma protein binding rate and oral bioavailability derived by using GA-CG-SVM method", J. Pharm. Biomed. Anal. 47:677-682, online 2008-03-28 (https://doi.org/10.1016/j.jpba.2008.03.023; PubMed 18455346). Abstract: "For the BIO, the training set is composed of 690 compounds and external 76 compounds form an independent validation set." As published by TDC (https://tdcommons.ai/single_pred_tasks/adme/, "Bioavailability, Ma et al."): "Binary classification. Given a drug SMILES string, predict the activity of bioavailability", "640 drugs"; columns drug name, SMILES and the label.
- Use case: a medicinal chemist in lead optimisation ranks candidates by their chance of being orally bioavailable before in-vivo studies; the sources read name no actor (the use case is ours), fit approximate (marketed and literature drugs stand for candidates). Regime IID or grouped by scaffold (TDC's ADMET group splits by scaffold); the add stage decides.
- Siblings and duplicates: no duplicate (grep over the records for bioavailab, Ma et al.). Siblings: the TDC ADMET candidates of this run (`tdc_ames`, `tdc_bbb_martins`, `tdc_cyp3a4_veith`, `tdc_ld50_zhu`, `tdc_lipophilicity_astrazeneca`, `tdc_aqsoldb`); the accepted molecule sets (`qsar_biodeg`, `qsar_oral_toxicity`, `qsar_bioconcentration`, `apistox`), whose structures ship as RDKit 2D descriptors (CC 2026-10-14, Lennart, on `apistox`). External collections: ChemPile (config `bioavailability_ma_et_al`), TDC (ADME; ADMET benchmark group).
- Better data: a candidate of the benchmark ChemPile; no further search for this run's finds.
- Papers and pages: Ma et al. 2008 (abstract read, the paper is paywalled); TDC's ADME page and ADMET group (https://tdcommons.ai/benchmark/admet_group/overview/); ChemPile, arXiv 2505.12534.
- Metric: Ma et al. report accuracy only (abstract: "The prediction accuracy for the training set by using 5-fold cross-validation and that for the independent test set are 80% and 86%, respectively"), with no threshold or costs, so the fallback (MET-6, MET-8); TDC's ADMET group scores AUROC by its class-balance rule ("AUROC is used when the number of positive and negative samples are similar"): `roc_auc`; inputs none.
- Risks for /add-dataset: the threshold that makes the label is stated neither on TDC's page nor in Ma's abstract (the run's "F at or above 20%" is unverified); the paper's 766 compounds against TDC's 640 (what was dropped is unknown); the set may come from an earlier compilation, which would be the first publication (PROV-8; not checked, the web-search budget of this session was used up); SMILES only; 640 rows, so count the minority class per test fold (TP-5).
- Priority: gap 0 (chemistry has 12 accepted datasets, binary is not thin), use case 0 (no actor named by the sources), source + (a journal paper and TDC's page), shape 0 (640 drugs, structure only), risk - (unstated threshold, a possible earlier first source).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 640 drugs (TDC Bioavailability_Ma); in ChemPile-LIFT 12,800 text prompts over 1 config(s); target: bioavailable (F at or above 20%).
- Why: Classify whether a drug's oral bioavailability is high
- Notes: Ma et al. 2008. Small. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.
