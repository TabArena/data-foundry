---
unique_name: herg_karim
name: herg_karim_et_al
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2021'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1186/s13321-021-00541-z
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/herg_karim_et_al ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/herg_karim_et_al ; original: https://tdcommons.ai/single_pred_tasks/tox/#herg-karim-et-al'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: 13,445 compounds for the same cardiotoxicity flag, but merged from several databases with mixed assays, and the batch holds a single-protocol screen 20 times larger.
- Source: Karim, Lee, Balle, Sattar, "CardioTox net: robust predictor for hERG induced cardiotoxicity using deep learning", J Cheminform 13:60 (2021), doi 10.1186/s13321-021-00541-z; TDC serves it as hERG_Karim, "**Dataset Statistics:** 13,445 drugs", "An integrated hERG dataset labeled as blockers (<10µM) or non-blockers (≥10µM), drawn from DeepHIT, BindingDB, ChEMBL, and literature" (tdcommons.ai/single_pred_tasks/tox). As published: one table of SMILES and the binary label; the repository github.com/Abdulk084/CardioTox ships the training file plus two external test sets (`external_test_set_pos.csv`, `external_test_set_neg.csv`) whose molecules were kept dissimilar from training by pairwise Tanimoto similarity (README).
- Use case: the same early-discovery cardiotoxicity flag as the other hERG sets; fit approximate, because the values are pooled across labs and assay formats; regime grouped on the Bemis-Murcko scaffold (SPLIT-31 as amended), which matches the authors' own dissimilar test sets.
- Siblings and duplicates: `herg_central` (306,893, one screen) and `herg_blockers_wang` (648) in the same batch; this set merges sources that contain the others, so compounds overlap, yet the first publications differ and none is a duplicate by provenance (PROV-4, PROV-7). External collections: ChemPile-LIFT config `herg_karim_et_al` (arXiv 2505.12534), TDC (not in the ADMET Benchmark Group).
- Better data: a candidate of the benchmark ChemPile (this run searched no further); within the run, `herg_central` is the larger, single-protocol set.
- Papers and pages: Karim et al. 2021 (open access; the publisher redirected both fetch attempts, so the text was not read - the README's comparison tables were); the CardioTox repository.
- Metric: several metrics side by side - the repository's comparison tables lead with MCC (CardioTox 0.599 on test set-I, 0.469 on test set-II) next to NPV, sensitivity, specificity and accuracy - so no single deliberate criterion, and MCC needs a threshold the source does not fix: the binary fallback `roc_auc` (MET-5, MET-6, MET-8); inputs none.
- Risks for /add-dataset: a merge of DeepHIT, BindingDB, ChEMBL and literature values, so duplicate structures with conflicting labels and labels from different assay formats (PROV-15, CLEAN); the authors' external sets are a deliberate dissimilarity split, so a random split would be optimistic (SPLIT-31); overlap with the other two hERG records has to be measured before one of them ships; features are the SMILES only.
- Priority: gap 0 (chemistry not thin), use case + (a standing go/no-go in drug design), source + (an open-access paper with code and data), shape + (13,445 compounds), risk - (pooled assays and heavy overlap with the larger `herg_central`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 13,445 compounds (TDC hERG_Karim); in ChemPile-LIFT 255,455 text prompts over 1 config(s); target: hERG blocker (1/0).
- Why: Classify whether a compound blocks hERG at under 10 uM
- Notes: Karim et al. 2021 (J Cheminform 13:60), merged from DeepHIT, BindingDB and ChEMBL, so it overlaps the two other hERG sets and a joined record needs care about duplicate compounds. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.
