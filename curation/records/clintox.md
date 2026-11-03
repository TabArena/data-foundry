---
unique_name: clintox
name: clintox
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2017'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1016/j.chembiol.2016.07.023
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/clintox ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/clintox ; original: https://tdcommons.ai/single_pred_tasks/tox/#clintox'
- https://arxiv.org/abs/2505.12534
- https://arxiv.org/abs/1703.00564
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 1,478 drugs labelled "failed a clinical trial for toxicity" against FDA-approved, a real safety question on a proxy label whose two classes come from two different registries.
- Source: the dataset was introduced by MoleculeNet, not by Gayvert et al. as the note below assumed: Wu, Ramsundar, Feinberg et al., "MoleculeNet: A Benchmark for Molecular Machine Learning", arXiv:1703.00564 (2017), Sec. "ClinTox": "The ClinTox dataset, introduced as part of this work, compares drugs approved by the FDA and drugs that have failed clinical trials for toxicity reasons. The dataset includes two classification tasks for 1491 drug compounds with known chemical structures: (1) clinical trial toxicity (or absence of toxicity) and (2) FDA approval status." The SI adds how the classes were built: the approved drugs from SWEETLEAD, the failures from the AACT database, where "the overall status was 'terminated,' 'suspended,' or 'withdrawn,' and the explanation for the status included the terms 'adverse,' 'toxic,' or 'death'". As published: 1,478 rows in MoleculeNet's table (TDC ships 1,484; ChemNLP 1,478), SMILES plus the two labels.
- Use case: a sponsor deciding whether to take a compound into clinical trials, from its structure; the source names no actor and the label is the trial's outcome rather than a measured toxicity, so fit approximate; regime grouped on the Bemis-Murcko scaffold (SPLIT-31; MoleculeNet itself used a random split).
- Siblings and duplicates: `dili_xu` and `dilist_drug_induced_liver_injury` (hepatotoxicity) and `drug_induced_autoimmunity_prediction` (`Yes`, autoimmunity) are the other drug-level human adverse-effect records: distinct endpoints (PROV-7). No other ClinTox record. External collections: ChemPile (config `clintox`), MoleculeNet, TDC Tox.
- Better data: a candidate of the benchmark ChemPile (ChemPile-LIFT config `clintox`); no new search in this run.
- Papers and pages: MoleculeNet (arXiv:1703.00564), which reports ClinTox at ROC-AUC 0.827-0.832 for its best models; Gayvert, Madhukar and Elemento 2016 (https://doi.org/10.1016/j.chembiol.2016.07.023), the PrOCTOR work MoleculeNet cites for the idea; TDC's Tox page.
- Metric: MoleculeNet, the benchmark that introduced the data, declares ROC-AUC for ClinTox (dataset table: "ClinTox SMILES 2 Classification 1478 Random ROC-AUC"), one deliberate choice (MET-5), and it is the fallback for a binary task anyway (MET-8). Inputs none.
- Risks for /add-dataset: the two classes come from two different databases (SWEETLEAD against AACT), so the recording may separate them for reasons other than toxicity (`Selection Bias` set; LEAK-13 to LEAK-15 to be probed); the positive class is small (roughly 7% in the published file, to be counted), so TP-5 and TP-8 need the fold counts; the FDA-approval label is a framing of the same signal, not a second dataset (CLEAN-18); a trial stopped for "adverse", "toxic" or "death" wording is a noisy stand-in for the compound's toxicity (USE-5); SMILES-only features (CLEAN-24).
- Priority: gap 0, use case 0 (no actor named), source + (MoleculeNet documents the construction), shape + (1,478 molecules, scaffold groups), risk - (classes from two registries).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 1,478 drugs (ChemNLP; TDC 1,484); in ChemPile-LIFT 28,082 text prompts over 1 config(s); target: clinical trial toxicity (1/0).
- Why: Classify whether a drug failed clinical trials for toxicity
- Notes: Gayvert, Madhukar and Elemento 2016 (Cell Chem Biol 23:1294), via MoleculeNet and TDC; MoleculeNet adds an FDA-approval label as a second column. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.
