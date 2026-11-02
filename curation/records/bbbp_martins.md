---
unique_name: bbbp_martins
name: BBBP, blood_brain_barrier_martins_et_al
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2012'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1021/ci300124c
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: BBBP, blood_brain_barrier_martins_et_al) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/BBBP ; original: https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv (MoleculeNet) and https://tdcommons.ai/single_pred_tasks/adme/#bbb-blood-brain-barrier-martins-et-al (TDC BBB_Martins)'
- https://arxiv.org/abs/2505.12534
- https://doi.org/10.1039/C7SC02664A
- https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: about 2,050 compounds labelled for blood-brain barrier penetration, the standard BBB classification; B3DB is the larger and newer compilation of the same task and has its own record in this run.
- Source: Martins, Teixeira, Pinheiro and Falcao 2012, "A Bayesian Approach to in Silico Blood-Brain Barrier Penetration Modeling", J Chem Inf Model (doi 10.1021/ci300124c, online 2012-06-06): "The data set used, gathered from the literature, totals 1970 curated molecules, one of the largest for similar studies", with an "over-representation of molecules that show an ability to permeate the BBB (BBB positives)" (abstract). The copies in use are MoleculeNet's BBBP.csv (header previewed: num, name, p_np, smiles; 2,050 rows against the 2,053 of the paper's Table 1) and TDC's BBB_Martins (1,975). One table, SMILES and a binary label.
- Use case: a medicinal chemist developing a CNS drug (or avoiding CNS exposure), before synthesis, predicts whether the compound crosses the barrier ("penetration of the barrier forms a long-standing issue in development of drugs targeting central nervous system", MoleculeNet Sec. 3.1.12; Martins aims at "a robust model capable of being applied in real-world drug research scenarios"); fit direct for that screening decision, approximate if the mixed label definition stands (USE-5); regime grouped on the Bemis-Murcko scaffold ("Scaffold splitting is also recommended", MoleculeNet Sec. 3.1.12; TDC uses it too; SPLIT-31).
- Siblings and duplicates: `tdc_bbb_martins` (TabBench-Bio) is the same Martins data as 2,048-bit ECFP4 fingerprints, a processed copy (PROV-4, PROV-6). The two ChemPile configs (`BBBP` through MoleculeNet, `blood_brain_barrier_martins_et_al` through TDC) are two cuts of this one source, not two datasets (PROV-6). `b3db_blood_brain_barrier` (Meng et al. 2021, Sci Data, 7,807 compounds with BBB+/- and 1,058 numeric logBB) is the same task from other sources, so its own record (PROV-4), not a duplicate. External collections: ChemPile / ChemNLP, MoleculeNet, TDC, TabBench-Bio.
- Better data: a candidate of the benchmark ChemPile; the run recorded `b3db_blood_brain_barrier` (https://doi.org/10.1038/s41597-021-01069-5, about four times the compounds, 2021) as the better data for this task; no further search this round.
- Papers and pages: Martins et al. 2012 (the data); MoleculeNet (Wu et al. 2018, Table 1, Sec. 3.1.12); TDC's ADMET benchmark group; the ChemNLP builder `data/tabular/BBBP`.
- Metric: MoleculeNet's Table 1, "BBBP SMILES 1 Classification 2053 Scaffold ROC-AUC", and TDC's ADMET group, AUROC with a scaffold split: a deliberate choice of both task definers (MET-1, MET-5), equal to the fallback. Martins 2012 reports 95% accuracy with a mean square contingency coefficient of 0.74, a threshold metric with no threshold fixed (MET-6). Inputs none.
- Risks for /add-dataset: the MoleculeNet file is reported to carry SMILES that RDKit cannot parse and duplicate structures, so count both before shipping (LEAK-16, CLEAN-24; unverified, from the run's note); the labels were compiled from many studies whose permeability thresholds differ, an unverified label definition that makes the fit approximate (USE-5, USE-8); BBB positives are over-represented against the drug-like population the use case screens, the authors' own words, so the record carries `Selection Bias`.
- Priority: gap 0, use case +, source +, shape + (about 2,050 compounds), risk - (better data `b3db_blood_brain_barrier`, and the mixed label definition).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 52: "Automatic Auxiliary Task Selection and Adaptive Weighting Boost Molecular Property ...".
- as published: 2,050 compounds (MoleculeNet BBBP); 1,975 (TDC BBB_Martins); in ChemPile-LIFT 61,040 text prompts over 2 config(s); target: BBB penetration (p/np); access: open.
- Why: Classify whether a drug crosses the blood-brain barrier | Standard binary ADMET task used in the item and MoleculeNet; real compiled measurements.
- Adds: | No BBB record. Known quality issues (invalid and duplicate SMILES, labels compiled from mixed literature thresholds) to check at screening. B3DB (Meng et al. 2021, Sci Data, about 7,800 compounds) may be the better data for the same task.
- Notes: Two configs of one source: Martins et al. 2012, taken once through MoleculeNet and once through TDC (the blood_brain_barrier_martins_et_al folder holds only transform.py, no meta.yaml). Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same data, once as SMILES and once as a fingerprint build (`tdc_bbb_martins`; PROV-6). The curator keeps one, or both as distinct tasks.
