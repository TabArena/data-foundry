---
unique_name: carcinogens_lagunin
name: carcinogens
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
year: '2009'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1002/qsar.200860192
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/carcinogens ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/carcinogens ; original: https://tdcommons.ai/single_pred_tasks/tox/#carcinogens'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 278 compounds with a rodent carcinogenicity label, a real endpoint but a very small set whose label construction could not be read.
- Source: Lagunin, Filimonov, Zakharov et al., "Computer-Aided Prediction of Rodent Carcinogenicity by PASS and CISOC-PSCT", QSAR Comb Sci 28(8):806, 2009 (https://doi.org/10.1002/qsar.200860192), reached through admetSAR (Cheng et al. 2012, https://doi.org/10.1021/ci300367a) and TDC; as published in the copy we can see: 278 compounds in TDC Carcinogens_Lagunin (ChemNLP `carcinogens/meta.yaml`: `num_points: 280`), one SMILES column and the target "whether it is carcinogenic (1) or not (0)", licence CC BY 4.0. The 2009 paper is paywalled and returned 403, so its cohort and label rule are unverified (PROV-17).
- Use case: a toxicologist or regulator decides whether a chemical needs a two-year rodent bioassay, from its structure alone; the source names no actor; fit approximate; regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: no other carcinogenicity record ('carcinogen' matches only this one). The toxicity records of the same family are `qsar_oral_toxicity` (`Yes`, acute oral toxicity), `ld50_zhu`, `ames_mutagenicity` and `ames_mutagenicity_hansen` (mutagenicity), `tox21` and `butkiewicz_pubchem_hts`: distinct endpoints, not duplicates (PROV-7). External collections: ChemPile (config `carcinogens`), TDC Tox.
- Better data: a candidate of the benchmark ChemPile (ChemPile-LIFT config `carcinogens`); no new search in this run.
- Papers and pages: TDC's Tox page ("Binary classification. Given a drug SMILES string, predict whether it can cause carcinogen", 278 drugs, https://tdcommons.ai/single_pred_tasks/tox/); admetSAR (Cheng et al. 2012).
- Metric: none found: TDC's page states no metric, Carcinogens is not in TDC's ADMET benchmark group (which lists metrics per dataset), and the 2009 paper could not be read, so the fallback `roc_auc` (MET-8). Looked at: the TDC Tox page, the TDC ADMET group overview, ChemNLP's `meta.yaml`. Inputs none.
- Risks for /add-dataset: 278 rows with an unknown class balance, so `Too Small` has to be measured on the folds (TP-5, TP-8); the label's provenance (which bioassay compilation, which call rule, rodent species) is unverified (USE-5, PROV-2); SMILES-only, so the descriptors are ours (CLEAN-24) and copies after dropping stereochemistry must be checked (LEAK-16).
- Priority: gap 0, use case 0 (no actor named by the source), source + (peer-reviewed, carried by admetSAR and TDC), shape 0 (278 rows), risk - (label construction unverified).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 278 compounds (TDC Carcinogens_Lagunin; ChemNLP 280); in ChemPile-LIFT 5,600 text prompts over 1 config(s); target: carcinogen (1/0).
- Why: Classify whether a compound is carcinogenic
- Notes: Lagunin et al. 2009 (QSAR Comb Sci 28:806) through admetSAR (Cheng et al. 2012, doi 10.1021/ci300367a). Very small. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.
