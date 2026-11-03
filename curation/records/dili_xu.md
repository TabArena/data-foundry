---
unique_name: dili_xu
name: drug_induced_liver_injury
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Tiny Data
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2015'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1021/acs.jcim.5b00238
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/drug_induced_liver_injury ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/drug_induced_liver_injury ; original: https://tdcommons.ai/single_pred_tasks/tox/#dili-drug-induced-liver-injury'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 475 drugs labelled for human liver injury, a real safety endpoint, but `dilist_drug_induced_liver_injury` already records the FDA's larger list of the same task.
- Source: Xu, Dai, Zhang et al., "Deep Learning for Drug-Induced Liver Injury", J Chem Inf Model 55(10):2085, 2015 (https://doi.org/10.1021/acs.jcim.5b00238); the abstract gives the cohort: a model "trained on 475 drugs" and validated on "an external validation set of 198 drugs", reported with "an accuracy of 86.9%, sensitivity of 82.5%, specificity of 92.9%, and area under the curve of 0.955". As published through TDC: 475 drugs, SMILES and the binary target, "predict whether it can cause liver injury (1) or not (0)" (https://tdcommons.ai/single_pred_tasks/tox/). The paper's sources for the labels are not stated in the abstract and the full text was not read.
- Use case: a drug-safety reviewer or a project team judging hepatotoxicity risk of a candidate from its structure; the source names no actor; fit approximate; regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: `dilist_drug_induced_liver_injury` (FDA DILIst, 1,279 drugs: 768 positive, 511 negative, a regulator-curated label) is the same endpoint from a later, larger source: not a duplicate (another publisher, PROV-4), and the curator picks which one enters. `clintox` and `drug_induced_autoimmunity_prediction` are other drug-level adverse effects (PROV-7). External collections: ChemPile (config `drug_induced_liver_injury`), TDC Tox and its ADMET leaderboard.
- Better data: `dilist_drug_induced_liver_injury` (FDA, 2019, 1,279 drugs against 475 here, the same human DILI call) already has a record from this run; this record is a candidate of the benchmark ChemPile, with no new search.
- Papers and pages: the 2015 paper (abstract read on PubMed 26437739); TDC's Tox page and ADMET group overview; the curator's Zotero item 106 lists DILI among the small TDC sets.
- Metric: TDC's ADMET leaderboard scores DILI by AUROC ("AUROC is used when the number of positive and negative samples are similar"); the 2015 paper reports accuracy, sensitivity, specificity and AUC side by side, so it has no unique criterion (MET-5): the fallback `roc_auc` (MET-8), which agrees with TDC. Inputs none.
- Risks for /add-dataset: 475 rows, so `Too Small` has to be measured per fold (TP-5, TP-8); the label's assembly (which labels, which severity cut) is unread (USE-5, PROV-16); SMILES-only features (CLEAN-24) and copies after dropping stereochemistry (LEAK-16); overlap with the DILIst drugs if both ever ship.
- Priority: gap 0, use case 0 (no actor named), source + (peer-reviewed, carried by TDC), shape 0 (475 rows), risk - (better data for the same task on record: `dilist_drug_induced_liver_injury`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 475 drugs (TDC DILI); in ChemPile-LIFT 9,025 text prompts over 1 config(s); target: DILI (1/0).
- Why: Classify whether a drug causes drug-induced liver injury
- Notes: Xu et al. 2015 (J Chem Inf Model 55:2085). Small. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record ('dili' matches only a well-log record).
