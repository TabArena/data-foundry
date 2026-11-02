---
unique_name: cyp_substrates_carbon_mangels
name: cyp2c9_substrate_carbonmangels, cyp2d6_substrate_carbonmangels, cyp3a4_substrate_carbonmangels
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
year: '2011'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1002/minf.201100069
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: cyp2c9_substrate_carbonmangels, cyp2d6_substrate_carbonmangels, cyp3a4_substrate_carbonmangels) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/cyp2c9_substrate_carbonmangels ; original: https://tdcommons.ai/single_pred_tasks/adme/#cyp2c9-substrate-carbon-mangels-et-al'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 666, 664 and 667 drugs labelled substrate or not for three CYP isozymes, a real ADME question on a small set whose label was merged from six papers.
- Source: Carbon-Mangels and Hutter, "Selecting Relevant Descriptors for Classification by Bayesian Estimates", Mol Inform 30(10):885, 2011 (https://doi.org/10.1002/minf.201100069; the publisher answers 403, so the text is unread, PROV-17), reached through admetSAR and TDC, which states: "TDC used a dataset from [1], which merged information on substrates and nonsubstrates from six publications" (https://tdcommons.ai/single_pred_tasks/adme/). As published in TDC: CYP2C9 666, CYP2D6 664, CYP3A4 667 drugs (ChemNLP counts 669 for 2C9), SMILES and one binary label per enzyme.
- Use case: a medicinal chemist asks which enzyme will clear a candidate, to judge interaction and variability risk before the in-vitro work; the source names no actor; fit approximate (a "non-substrate" from a literature merge is an absence of evidence); regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: `cyp450_inhibition_aid1851` (and `tdc_cyp3a4_veith`) hold the inhibition task on the same enzymes from another source: a different question, so not duplicates (PROV-7). The three enzymes here are three cuts of one compilation (PROV-6): one enzyme ships, the others stay siblings in the comments. External collections: ChemPile (three configs), TDC ADME.
- Better data: a candidate of the benchmark ChemPile (configs `cyp2c9_substrate_carbonmangels`, `cyp2d6_substrate_carbonmangels`, `cyp3a4_substrate_carbonmangels`); no new search in this run.
- Papers and pages: TDC's ADME page (task, sizes and the merge statement); admetSAR (Cheng et al. 2012); the 2011 paper itself could not be read.
- Metric: TDC's ADMET benchmark group scores CYP2C9 and CYP2D6 Substrate by AUPRC and CYP3A4 Substrate by AUROC, the stated reasons being class balance ("AUPRC is used when the number of positive samples are much smaller than negative samples"), which is not a decision-driven choice (MET-9); the 2011 paper is a descriptor-selection comparison that reports several classification figures, so no unique original (MET-5): the fallback `roc_auc` (MET-8). Looked at: the TDC ADME page, the ADMET group overview, ChemNLP's `meta.yaml`. Inputs none.
- Risks for /add-dataset: about 660 rows per enzyme with an unknown class balance, so `Too Small` must be measured (TP-5, TP-8); the label merges six publications with no common assay, so what a 0 means is unclear (USE-5); SMILES-only features (CLEAN-24) and copies after dropping stereochemistry (LEAK-16); the three enzymes overlap heavily in compounds, which matters only if more than one ships.
- Priority: gap 0, use case 0 (no actor named), source + (peer-reviewed, carried by admetSAR and TDC), shape 0 (about 660 rows), risk - (label merged from six papers, source text unread).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 666 / 664 / 667 drugs (TDC); ChemNLP counts 669 for 2C9; in ChemPile-LIFT 38,114 text prompts over 3 config(s); target: substrate (1/0), one label per enzyme.
- Why: Classify whether a drug is a substrate of CYP2C9, CYP2D6 or CYP3A4
- Notes: Three configs of one source: Carbon-Mangels and Hutter 2011 (Mol Inform 30:885), built on a Zaretzki substrate set. Small. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record (grep cyp, p450).
