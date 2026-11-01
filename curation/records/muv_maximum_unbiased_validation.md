---
unique_name: muv_maximum_unbiased_validation
name: MUV_466, MUV_548, MUV_600, MUV_644, MUV_652, MUV_689, MUV_692, MUV_712, MUV_713, MUV_733, MUV_737, MUV_810, MUV_832, MUV_846, MUV_852, MUV_858, ...
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
collections:
- ChemPile
original_source: Other
year: '2009'
domain: chemistry & material science
problem_type: Binary Classification
source_links:
- https://doi.org/10.1021/ci8002649
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: MUV_466, MUV_548, MUV_600, MUV_644, MUV_652, MUV_689, MUV_692, MUV_712, MUV_713, MUV_733, MUV_737, MUV_810, MUV_832, MUV_846, MUV_852, MUV_858, MUV_859) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/MUV_466 ; original: https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/muv.csv.gz (MoleculeNet), built from PubChem BioAssay'
- https://arxiv.org/abs/2505.12534
- https://www.tu-braunschweig.de/pharmchem/forschung/baumann/muv
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: real PubChem screening outcomes, but a designed benchmark: per target about 30 actives, picked to be spread out among about 15,000 decoys, in 17 target sets of one source.
- Source: Rohrer and Baumann, "Maximum Unbiased Validation (MUV) Data Sets for Virtual Screening Based on PubChem Bioactivity Data", J. Chem. Inf. Model. 49:169-184, online 2009-01-22 (https://doi.org/10.1021/ci8002649); the data from the authors on request (https://www.tu-braunschweig.de/pharmchem/forschung/baumann/muv: "please contact us") and in Riniker and Landrum 2013 (J. Cheminform. 5:26, additional file 5). Abstract: "refined nearest neighbor analysis is used to design benchmark data sets for virtual screening based on PubChem bioactivity data ... Topological optimization using experimental design strategies ... is applied to generate corresponding data sets of actives and decoys that are unbiased with regard to analogue bias and artificial enrichment." As published in MoleculeNet's muv.csv (the file ChemNLP uses): 93,087 compounds, 17 binary columns `MUV-<AID>`, about 14,800-15,000 labelled per target (MUV_466: 14,841), SMILES the only input. MoleculeNet gives the positive rate as 0.20% (Sec. 4.1); the 30 actives and 15,000 decoys per target are from secondary pages, not read in the paper's text.
- Use case: a medicinal chemist runs a virtual screen to choose which compounds to test against a target; fit approximate: the paper built the sets to validate virtual-screening methods, with actives chosen to be spread out among decoys that resemble them, which a real screening library is not. Regime IID (MoleculeNet: random split) or grouped by scaffold; the add stage decides.
- Siblings and duplicates: no duplicate (grep over the records for muv, maximum unbiased). Siblings: `lit_pcba_virtual_screening` (a later PubChem virtual-screening benchmark from confirmatory dose-response assays), `hiva_agnostic` (`Yes`, the MoleculeNet HIV screen), `tox21` with its per-assay records `tox21_nr_ahr` and `tox21_sr_mmp`, `drug_discovery_virtual_screening_dataset` (`No`, synthetic). The 17 targets are distinct tasks of one source (PROV-7), so the curator picks one or a few, as with the Tox21 assays. External collections: ChemPile (17 configs `MUV_<AID>`), MoleculeNet (Wu et al. 2018, Sec. 3.1.8).
- Better data: a candidate of the benchmark ChemPile; no further search for this run's finds.
- Papers and pages: Rohrer and Baumann 2009 (abstract read, not the text); Wu et al., "MoleculeNet", Chem. Sci. 9:513, 2018 (https://pmc.ncbi.nlm.nih.gov/articles/PMC5868307/), Sec. 3.1.8: "The MUV dataset contains 17 challenging tasks for around 90 thousand compounds and is specifically designed for validation of virtual screening techniques"; ChemPile, arXiv 2505.12534.
- Metric: MoleculeNet scores MUV by PRC-AUC on a random split (Table 1), set by a rule on the positive rate (Sec. 3.3: "PRC-AUC is used for datasets with positive rates less than 2%"), which is class imbalance alone (MET-9), so the fallback `roc_auc` or `log_loss`, unless the curator takes an early-enrichment metric from the virtual-screening field (the paper's own evaluation not read); inputs none (MET-1, MET-5).
- Risks for /add-dataset: about 30 actives per target, about 6 per test fold of a 5-fold split (TP-5); the designed choice of actives and decoys (`Selection Bias`); SMILES only, so the structure ships as RDKit 2D descriptors as for `apistox` (CC 2026-10-14, Lennart); the ChemNLP MUV meta.yaml links the SIDER paper as its publication, an error of that copy (PROV-15); the same compound can sit in several target sets.
- Priority: gap 0 (chemistry has 12 accepted datasets, binary is not thin), use case 0 (built to validate methods, fit approximate), source + (a journal paper defines the sets), shape 0 (about 15,000 compounds, but about 30 positives and a single structure column), risk - (few actives per target, designed selection).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 93,087 compounds over 17 targets in muv.csv; about 14,800-15,000 labelled per target (ChemNLP MUV_466: 14,841); in ChemPile-LIFT 1,249,430 text prompts over 17 config(s); target: active in MUV-<AID>, one binary label per target.
- Why: Virtual screening: classify whether a compound is active in one of 17 PubChem HTS targets
- Notes: 17 configs, one source: Maximum Unbiased Validation, Rohrer and Baumann 2009 (J Chem Inf Model 49:169). Each config is named by the PubChem AID it was built from: 466 S1P1 agonists, 548 PKA inhibitors, 600 SF1 inhibitors, 644 Rho-kinase 2, 652 HIV RT-RNase, 689 Eph receptor A4, 692 SF1 agonists, 712 HSP90, 713 ...
