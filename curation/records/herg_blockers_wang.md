---
unique_name: herg_blockers_wang
name: herg_blockers
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Tiny Data
collections:
- ChemPile
original_source: Other
year: '2016'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1021/acs.molpharmaceut.6b00471
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/herg_blockers ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/herg_blockers ; original: https://tdcommons.ai/single_pred_tasks/tox/#herg-blockers'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the cardiotoxicity flag is a real early-discovery decision and TDC fixes metric and split, but this is the smallest of three hERG candidates in the same run (648 compounds against 13,445 and 306,893).
- Source: Wang, Li et al., "ADMET Evaluation in Drug Discovery. 16. Predicting hERG Blockers by Combining Multiple Pharmacophores and Machine Learning Approaches", Mol Pharm 13(8):2855 (2016), doi 10.1021/acs.molpharmaceut.6b00471; TDC serves it as hERG, "**Dataset Statistics:** 648 drugs" (tdcommons.ai/single_pred_tasks/tox), the ChemNLP config counts 655. As published: one table, SMILES and a binary blocker label ("1 = blocks, 0 = does not block", TDC).
- Use case: a medicinal chemist flagging hERG-related cardiotoxicity risk before a compound is made or sent to a patch-clamp assay; the task description names the moment ("reliable prediction of hERG liability in the early stages of drug design"), not the actor, so fit approximate; regime grouped on the Bemis-Murcko scaffold (SPLIT-31 as amended; TDC's own split for this dataset).
- Siblings and duplicates: `herg_karim` (13,445 compounds, a merge of DeepHIT, BindingDB and ChEMBL) and `herg_central` (306,893 compounds from one screen) are the same endpoint from other compilations, screened in this batch: different first publications, so not duplicates by provenance (PROV-4, PROV-7), but the benchmark needs one hERG task and this is the smallest and most pooled. External collections: ChemPile-LIFT config `herg_blockers` (arXiv 2505.12534), TDC ADMET Benchmark Group.
- Better data: a candidate of the benchmark ChemPile (this run searched no further); the two larger hERG sets are records of the same run, `herg_karim` and `herg_central`.
- Papers and pages: Wang et al. 2016 (paywalled, not read here); the TDC tox page and the ADMET Benchmark Group leaderboard.
- Metric: the TDC ADMET Benchmark Group ranks hERG by AUROC on a scaffold split (tdcommons.ai/benchmark/admet_group/overview; "AUROC is used when the number of positive and negative samples are similar"), a deliberate choice of the benchmark that defined the task (MET-1, MET-5), and the binary fallback besides; inputs none. What Wang et al. themselves ranked by was not read.
- Risks for /add-dataset: 648 rows, so count the minority class per test fold before building (TP-5); the IC50 threshold behind the label and the labs the values come from need checking (the set is pooled from the literature); large compound overlap with `herg_karim` and `herg_central`, so only one hERG record should ship and the structures should be de-duplicated across them; features are the SMILES only.
- Priority: gap 0 (chemistry not thin), use case + (a standing go/no-go in drug design), source + (a journal paper plus a benchmark that defines the task), shape 0 (648 compounds, one input column), risk - (two larger datasets of the same endpoint).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 648 drugs (TDC hERG; ChemNLP 655); in ChemPile-LIFT 12,445 text prompts over 1 config(s); target: hERG blocker (1/0).
- Why: Classify whether a drug blocks the hERG potassium channel, the cardiotoxicity flag in early drug design
- Notes: Wang et al. 2016 (Mol Pharm 13:2855). Small. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record (grep herg).
