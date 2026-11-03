---
unique_name: onsides_adverse_drug_events
name: SIDER
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
collections:
- ChemPile
domain: chemistry & material science
problem_type: Binary Classification
source_links:
- https://doi.org/10.1093/nar/gkv1075
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/SIDER ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/SIDER ; original: https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/sider.csv.gz (MoleculeNet)'
- https://arxiv.org/abs/2505.12534
- https://github.com/tatonetti-lab/onsides
- https://doi.org/10.1016/j.medj.2025.100642
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: real side-effect labels taken from drug labels, with the structure as the only input; the record holds two sources (SIDER 4 through MoleculeNet, and the newer, larger OnSIDES), and the target (one of 27 organ classes, or a single event) is still to be chosen.
- Source: SIDER 4, Kuhn, Letunic, Jensen and Bork, "The SIDER database of drugs and side effects", Nucleic Acids Res. 44:D1075, online 2015-10-19 (https://doi.org/10.1093/nar/gkv1075), EMBL; abstract: "The current release, SIDER 4, contains data on 1430 drugs, 5880 ADRs and 140 064 drug-ADR pairs". As published in MoleculeNet's sider.csv (the file ChemNLP uses): SMILES and 27 binary columns, Sec. 3.1.15: "grouped drug side-effects into 27 system organ classes following MedDRA classifications measured for 1427 approved drugs". OnSIDES, Tatonetti lab (https://github.com/tatonetti-lab/onsides; Med 2025, https://doi.org/10.1016/j.medj.2025.100642, text not read): the README gives "more than 7.1 million drug-ADE pairs for 4,097 drug ingredients" from 51,460 labels of DailyMed (US), EMA (EU), EMC (UK) and KEGG (Japan), in seven tables (`product_label`, `product_adverse_effect`, `product_to_rxnorm`, `vocab_rxnorm_product`, `vocab_rxnorm_ingredient_to_product`, `vocab_rxnorm_ingredient`, `vocab_meddra_adverse_effect`) that join from a label to RxNorm ingredients and MedDRA terms; data CC BY 4.0.
- Use case: a drug developer predicts the side-effect profile of a candidate from its structure before trials (SIDER's abstract: side effects are "a severe impediment in the development of new drugs"); fit approximate: the label says what a regulator's label text lists, not how often it occurs, and only for marketed drugs; SIDER is a resource, and the prediction task was framed later (MoleculeNet 2018). Regime IID (MoleculeNet: random split), or by approval date to mirror new drugs; the add stage decides.
- Siblings and duplicates: no other record of SIDER or OnSIDES (grep over the records for sider, onsides); `fda_animal_veterinary_adverse_events`, `fda_cosmetic_adverse_events` and `fda_food_adverse_events` are spontaneous reports on other products, not drug labels. SIDER and OnSIDES are two sources (PROV-4) that the run merged into one record (alias `sider_adverse_reactions`); the curator decides whether SIDER gets its own record. External collections: ChemPile (config `SIDER`), MoleculeNet (SIDER).
- Better data: a candidate of the benchmark ChemPile, merged in the run with OnSIDES, which was found as newer, larger data for the SIDER task (4,097 ingredients from 51,460 labels, against SIDER's 1,430 drugs of 2015); no further search.
- Papers and pages: Kuhn et al. 2016 (abstract read); Wu et al., "MoleculeNet", Chem. Sci. 9:513, 2018 (https://pmc.ncbi.nlm.nih.gov/articles/PMC5868307/); the OnSIDES README; ChemPile, arXiv 2505.12534. The run's Assessment names a Zotero item (116, on Alzheimer's prediction) as a find path; its link to this task was not checked.
- Metric: MoleculeNet scores SIDER by ROC-AUC on a random split (Table 1), chosen by its rule on the positive rate (Sec. 3.3), not for the decision, so the fallback `roc_auc` for the shipped target (MET-5, MET-8); OnSIDES defines no prediction task (README); inputs none.
- Risks for /add-dataset: OnSIDES labels are the output of a PubMedBERT extractor (README: "The adverse drug event term extraction method is imperfect"; F1 0.942 on held-out Adverse Reactions sections, 0.847 on an independent 30-label hold-out), and SIDER's are text-mined, so label noise; the length and age of a label drive how many events it lists; products with several ingredients and biologics have no single SMILES (joins over RxNorm); the positive rate of each organ class decides whether a target is usable (TP-5, TP-4), so check it before choosing (USE-5); SMILES only, so RDKit 2D descriptors as for `apistox` (CC 2026-10-14, Lennart).
- Priority: gap 0 (chemistry and medical are not thin, binary is not thin), use case 0 (fit approximate, no decision named by the source), source + (a NAR paper; OnSIDES's paper and maintained repository), shape 0 (1,427 or about 4,000 drugs, structure-only features), risk - (target to choose, labels partly model output, two sources in one record).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 116: "An Explainable Ensemble Framework for Alzheimer's Disease Prediction Using Structured ...".
- as published: 1,427 marketed drugs; in ChemPile-LIFT 32,821 text prompts over 1 config(s); target: adverse reaction present per MedDRA system organ class; access: open.
- Why: Predict which organ-class adverse reactions a marketed drug carries | the SIDER task on current labels from four regulators: about three times the drugs of SIDER 4.1 (1,430 drugs, last release 2015), maintained, CC BY 4.0 against SIDER's CC BY-NC-SA
- Adds: | newer and larger data for the side-effect task the ChemPile-LIFT scouting proposed as sider_adverse_reactions (zotero_04 left SIDER out). Risks: the labels are extracted by a PubMedBERT model over MedDRA string matches (F1 0.85-0.94 on held-out labels), so part of the target is model output; label length and drug ...
- Notes: SIDER 4.1, Kuhn et al. 2016 (NAR 44:D1075), labels mined from package inserts, via MoleculeNet. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record ('sider' greps only match 'consider').
