---
unique_name: bace1_inhibitors
name: BACE
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Many features
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
- https://doi.org/10.1021/acs.jcim.6b00290
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/BACE ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/BACE ; original: https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/bace.csv (MoleculeNet)'
- https://arxiv.org/abs/2505.12534
- https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/bace.csv
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 1,513 literature BACE-1 inhibitors with pIC50 and a binary label, the MoleculeNet BACE task; `bace_inhibitors` is a second record of the same data and one of the two has to go.
- Source: Subramanian, Ramsundar, Pande and Denny 2016, "Computational Modeling of beta-Secretase 1 (BACE-1) Inhibitors Using Ligand Based Approaches", J Chem Inf Model (doi 10.1021/acs.jcim.6b00290, online 2016-10-10); MoleculeNet merged it: "The BACE dataset provides quantitative (IC50) and qualitative (binary label) binding results for a set of inhibitors of human beta-secretase 1 (BACE-1). All data are experimental values reported in scientific literature over the past decade ... We merged a collection of 1522 compounds with their 2D structures and binary labels in MoleculeNet, built as a classification task" (Wu et al. 2018, Sec. 3.1.11). As published (the deepchem bace.csv header previewed 2026-10-31): 1,513 rows with mol (SMILES), CID, Class, Model (the authors' own train/valid/test flag), pIC50 and several hundred precomputed descriptors (MW, AlogP, PSA, E-state keys and counts). The paper's own design is 205 training compounds, 1,273 analogs for external validation and 69 prospective compounds.
- Use case: a medicinal chemist in lead identification and optimisation, before an analog is synthesised, predicts its BACE-1 potency to decide which to make; the paper asks for such models to be applied "systematically" at that stage; fit direct; regime grouped on the Bemis-Murcko scaffold ("regarding a single protein target, scaffold splitting will be more practically useful", MoleculeNet Sec. 3.1.11; SPLIT-31).
- Siblings and duplicates: `bace_inhibitors`, created in the same run from the curator's Zotero item, ends at the same paper and the same MoleculeNet file: the two are one dataset (PROV-4), and the curator picks which record stays. External collections: ChemPile / ChemNLP (config `BACE`), MoleculeNet; no TabBench-Bio twin found. Other molecule records: `qsar_tid_11` (a ChEMBL potency regression, `Yes`) is the closest precedent for the pIC50 framing.
- Better data: a candidate of the benchmark ChemPile; no further search this round.
- Papers and pages: Subramanian et al. 2016 (the data), MoleculeNet (Wu et al. 2018) for the merged file and the recommended protocol; the ChemNLP builder `data/tabular/BACE`.
- Metric: MoleculeNet's Table 1, "BACE SMILES 1 Classification 1522 Scaffold ROC-AUC", a deliberate choice of the task definer (MET-1, MET-5), equal to the fallback for a binary task. The paper reports about 70% accuracy for classification and an RMSE near 1 log unit for the pIC50 regression; accuracy with no threshold fixed is habit (MET-6). If the curator ships the pIC50 regression instead, `rmse`; inputs none.
- Risks for /add-dataset: `Class` is a thresholded pIC50, so shipping both targets at once leaks (pick one framing, as `pva_revenue_prediction_kddcup98` did); the compounds are few congeneric series, so analogs sit on both sides of a random split (LEAK-17), which the scaffold grouping fixes; the file carries the authors' `Model` split column (drop it) and several hundred descriptors from their own pipeline, which stay beside RDKit's (CLEAN-24); 1,513 rows is small for a scaffold-grouped split, so count the groups and the actives per fold (TP-5).
- Priority: gap 0, use case +, source +, shape + (1,513 rows, wide), risk - (congeneric series and the duplicate record).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 1,513 compounds (MoleculeNet BACE); in ChemPile-LIFT 15,130 text prompts over 1 config(s); target: BACE-1 inhibitor label; pIC50.
- Why: Classify whether a compound inhibits human beta-secretase 1 (BACE-1); pIC50 is also given
- Notes: Subramanian et al. 2016, literature IC50 values, curated in MoleculeNet (Wu et al. 2018, doi 10.1039/c7sc02664a). Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record (grep bace, moleculenet, deepchemdata).

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same BACE source (`bace_inhibitors`; PROV-4). The curator keeps one, or both as distinct tasks.
