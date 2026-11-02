---
unique_name: ames_mutagenicity
name: ames_mutagenicity
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
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
- https://doi.org/10.1021/ci300400a
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/ames_mutagenicity ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/ames_mutagenicity ; original: https://tdcommons.ai/single_pred_tasks/tox/#ames-mutagenicity'
- https://arxiv.org/abs/2505.12534
- https://acs.figshare.com/articles/In_silico_Prediction_of_Chemical_Ames_Mutagenicity/2465989
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 7,255 compounds with a measured Ames result, the regulatory genotoxicity endpoint; a real screening decision, with split and metric fixed by TDC.
- Source: Xu et al. 2012, "In silico Prediction of Chemical Ames Mutagenicity", J Chem Inf Model 52(11):2840 (doi 10.1021/ci300400a, online 2012-10-17); the compound table is the paper's supplement (ci300400a_si_001.xls, ACS figshare 2465989). As published, the abstract: "a comprehensive database containing 7617 diverse compounds, including 4252 mutagens and 3365 nonmutagens, was constructed", plus "an external test set containing 831 diverse chemicals". The copy in use is TDC's AMES, 7,255 compounds, one table of SMILES and a 0/1 label ("The dataset is aggregated from four papers", tdcommons.ai/single_pred_tasks/tox). Features are the descriptors we compute from the SMILES (CLEAN-24).
- Use case: a toxicologist or medicinal chemist, before the bacterial reverse-mutation assay is run on a new compound, decides which compounds to test or to drop ("the most widely used assay for testing the mutagenicity of compounds is the Ames experiment", ChemNLP data card); fit direct; regime grouped on the Bemis-Murcko scaffold (SPLIT-31), which is also TDC's split ("For every dataset in the benchmark group, we use the scaffold split").
- Siblings and duplicates: `ames_mutagenicity_hansen` (Hansen et al. 2009, doi 10.1021/ci900161g, 6,512 compounds) is the earlier benchmark that Xu's compilation largely absorbed, so the two overlap heavily: one PROV-6 decision for the curator, and this one is the larger and newer. `tdc_ames` (TabBench-Bio) is the same TDC file as 2,048-bit ECFP4 fingerprints, a processed copy of this source (PROV-4, PROV-6); the SMILES route is the one CLEAN-24 asks for. Other molecule records: `qsar_oral_toxicity`, `qsar_bioconcentration`, `apistox`, `drug_induced_autoimmunity_prediction` (all `Yes`). External collections: ChemPile / ChemNLP (config `ames_mutagenicity`), TDC, TabBench-Bio.
- Better data: a candidate of the benchmark ChemPile; no further search this round.
- Papers and pages: Xu et al. 2012 (the data); Hansen et al. 2009 for the overlapping compilation; TDC's AMES page and its ADMET benchmark group; the ChemNLP builder `data/tabular/ames_mutagenicity`.
- Metric: TDC's ADMET Benchmark Group declares AUROC with a scaffold split for AMES (tdcommons.ai/benchmark/admet_group/overview; "We hold out 20% data samples for the test set"), a deliberate choice of the task definer (MET-1, MET-5). Xu 2012 reports accuracy alone ("The accuracies of fivefold cross validation were from 0.808 to 0.841 for top five models"), a threshold metric with no threshold fixed, so it is the field's habit (MET-6). `roc_auc`, which is also the fallback; inputs none.
- Risks for /add-dataset: the TDC file aggregates four compilations, so check conflicting labels for compounds in several of them and the overlap with `ames_mutagenicity_hansen` (PROV-6); salt forms and stereoisomers collapse onto the same 2D descriptors (LEAK-17, CLEAN-24); the figshare supplement is the only route to Xu's own file.
- Priority: gap 0 (chemistry & material science and binary classification are not thin), use case +, source +, shape + (7,255 compounds), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 7,255 compounds (TDC AMES; ChemNLP counts 7,278); in ChemPile-LIFT 138,282 text prompts over 1 config(s); target: Ames mutagenic (1/0).
- Why: Classify whether a compound is mutagenic in the Ames test
- Notes: Xu et al. 2012 (J Chem Inf Model 52:2840), built largely on the Hansen et al. 2009 Ames benchmark (doi 10.1021/ci900161g). Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same data, once as SMILES and once as a fingerprint build (`tdc_ames`; PROV-6). The curator keeps one, or both as distinct tasks.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: overlapping Ames compilations (Xu 2012 and Hansen 2009) (`ames_mutagenicity_hansen`; PROV-6). The curator keeps one, or both as distinct tasks.
