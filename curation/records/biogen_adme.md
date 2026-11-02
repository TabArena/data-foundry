---
unique_name: biogen_adme
name: Biogen ADME public set (Fang et al. 2023)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Github
year: '2023'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/molecularinformatics/Computational-ADME
- https://doi.org/10.1021/acs.jcim.3c00160
- https://huggingface.co/datasets/scbirlab/fang-2023-biogen-adme
- http://arxiv.org/abs/2608.18982
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 3,521 commercially available compounds measured by Biogen in six in vitro ADME assays under its in-house protocols (2023), open with SMILES; one endpoint per task (HLM 3,087, RLM 3,054, MDR1-MDCK efflux ratio 2,642, solubility 2,173 compounds).
- Source: Fang, Wang, Grater, Kapadnis, Black, Trapa and Sciabola (Biogen), "Prospective Validation of Machine Learning Algorithms for Absorption, Distribution, Metabolism, and Excretion Prediction: An Industrial Perspective", J Chem Inf Model 2023 (doi 10.1021/acs.jcim.3c00160, online 2023-05-22); data at github.com/molecularinformatics/Computational-ADME (MIT): "a collection of 3521 diverse compounds selected from commercially available compound libraries (i.e. Enamine, eMolecules, WuXi LabNetwork, Mcule) and tested them against our internal six ADME in vitro assays ... using the same experimental conditions as of our in-house datasets" (README). As published (`ADME_public_set_3521.csv`, counted 2026-10-31): Internal ID, Vendor ID, SMILES, CollectionName and six log endpoints with partial coverage: HLM CLint 3,087, RLM CLint 3,054, MDR1-MDCK ER 2,642, solubility at pH 6.8 2,173, hPPB 194, rPPB 168; plus per-endpoint train and test files of the paper's MPNN and FCNN models.
- Use case: a medicinal chemist in early discovery predicts a designed compound's metabolic stability, efflux or solubility before synthesis or assay, to decide which compounds to make and test (the paper's setting: models predicting prospectively, retrained on a fixed schedule over 20 months of internal data); fit direct, with the public compounds standing for candidates; regime grouped on the Bemis-Murcko scaffold (SPLIT-31): the public set has no dates, and the time-ordered internal data is not public.
- Siblings and duplicates: none (grep biogen, Computational-ADME, fang); `hepatocyte_clearance_astrazeneca` and `astrazeneca_chembl_logd74` are other ADME sources (other compounds and assays). External collections: Polaris (`polaris/adme-fang-v1` and benchmarks on the paper's split, such as adme-fang-SOLU-1 with 1,578 training and 400 test compounds); the Hugging Face copy scbirlab/fang-2023-biogen-adme (adds a scaffold split); Monroe (arXiv 2608.18982) per the Zotero item.
- Better data: from the curator's Zotero collection (items 106, 247); no further search this round.
- Papers and pages: Fang et al. 2023 (paywalled; abstract read: gradient boosting and deep learning beat random forest over time, scheduled retraining helps, tuning only marginally); the Polaris benchmark page; the TDC-leaderboard critique of Zotero item 106.
- Metric: not found in a source read: the paper is paywalled; Polaris lists MAE, MSE, R2, Spearman, Pearson and explained variance on the paper's split and sorts its leaderboard by MAE (a page, not the paper's choice); so the fallback `rmse` on the log endpoint unless the paper names one criterion (MET-1, MET-5); inputs none.
- Risks for /add-dataset: HLM and RLM are left-censored at the assay limit (958 of 3,087 HLM values at the minimum 0.676, 346 of 3,054 RLM values at 1.028; counted 2026-10-31): prefer MDR1-MDCK ER or solubility, or decide how a censored target ships; hPPB and rPPB (194 and 168 compounds) are too small on their own (TP-5); several endpoints of one compound set are cuts of one release (PROV-6) unless each ships as its own task (PROV-7); 98% of the compounds come from eMolecules, and `CollectionName`, `Vendor ID` and `Internal ID` are no features; SMILES need descriptors (CLEAN-24).
- Priority: gap 0 (chemistry, regression, grouped not thin), use case +, source +, shape + (2,173 to 3,087 compounds per endpoint, scaffold groups), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 106: "Critical Assessment of ML models for ADMET Prediction in TDC leaderboards"; the curator's Zotero collection, item 247: "Monroe: A Molecular Foundation Model for In-Context Probabilistic Inference".
- as published: compounds, 3,521 (commercial libraries) measured in Biogen's in-house assays; six log endpoints with partial coverage: HLM and RLM clearance, solubility, MDR1-MDCK efflux ratio, hPPB, rPPB; SMILES ...; target: one ADME endpoint per task (for example log HLM CLint); access: open.
- Why: Single-lab, one-protocol measurements published as a cleaner alternative to aggregated ADMET sets (the item's critique of TDC) | Real measurements from one industrial lab under one protocol, published to benchmark ADME models, for a task done daily in drug discovery. Gradient boosting is competitive in the paper and ...
- Adds: Newer, consistent assay conditions, several related regression targets | The first ADME (pharmacokinetic property) task, next to the bioactivity qsar_tid_* records. Shipped descriptors avoid SMILES featurisation. A scaffold-grouped split is the field's standard.
