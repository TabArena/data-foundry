---
unique_name: ames_mutagenicity_hansen
name: Benchmark data set for in silico prediction of Ames mutagenicity (Hansen et al.)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2009'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1021/ci900161g
- https://doc.ml.tu-berlin.de/toxbenchmark/
- https://tdcommons.ai/single_pred_tasks/tox/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: Hansen et al.'s 2009 Ames benchmark, 6,512 compounds with a per-compound source and reference, fixed CV folds and AUC as the declared criterion; the same task as `ames_mutagenicity` (Xu et al. 2012, 7,617 compounds), which is larger and newer and probably overlaps it, so the curator keeps one (PROV-6).
- Source: Hansen, Mika, Schroeter, Sutter, ter Laak, Steger-Hartmann, Heinrich and Müller 2009, "Benchmark Data Set for in Silico Prediction of Ames Mutagenicity", J Chem Inf Model 49:2077-2081 (doi 10.1021/ci900161g); data at doc.ml.tu-berlin.de/toxbenchmark: version 2, 6,512 compounds, online since April 2009 (version 1, 7,090 compounds, November 2008). As published: CSV or Excel with CAS number, source, activity (0/1), a steroid flag, World Drug Index name, canonical SMILES and reference; a SMILES file and an SD file. The abstract: "a new unique public Ames mutagenicity data set comprising about 6500 nonconfidential compounds (available as SMILES strings and SDF) together with their biological activity". The merged sources (CCRIS, Kazius/Bursi, Helma, Feng, VITIC, GeneTox) are from the run's note; the page's source pages were not opened.
- Use case: a toxicologist or medicinal chemist decides, before the bacterial reverse-mutation assay, which compounds to test or drop (as on `ames_mutagenicity`). The abstract compares three commercial tools with four machine-learning methods and names no actor; the full text is paywalled (ACS) and was not read, so the use case is ours to state; fit direct for that screening decision. Regime grouped on the Bemis-Murcko scaffold (SPLIT-31), as for `ames_mutagenicity`; the benchmark's own split, one run of 5-fold CV with "a static portion excluded from the test set" in every training set, is a claim (SPLIT-5).
- Siblings and duplicates: `ames_mutagenicity` (ChemPile; Xu et al. 2012, 7,617 compounds, TDC AMES 7,255; `TBD -> Yes`, priority 4) is the same task, and its screening says Xu's compilation "largely absorbed" Hansen's. Xu's abstract names no sources and its supplement (ci300400a_si_001.xls) was not opened, so the overlap is unmeasured: count it by InChIKey and let the curator keep one (PROV-6). `tdc_ames` (TabBench-Bio) links this record's DOI, but TDC cites its AMES file to Xu 2012, so it is a processed copy of `ames_mutagenicity`'s source, not of this one. `carcinogens_lagunin` is another endpoint (PROV-7). External collections: the TU Berlin benchmark page; awesome-chemistry-datasets.
- Better data: from the awesome-chemistry-datasets list and the curator's Zotero collection (item 93); no further search this round.
- Papers and pages: Hansen et al. 2009 (the data); Xu et al. 2012 (the larger compilation, doi 10.1021/ci300400a).
- Metric: the benchmark page says its models were optimized for "the AUC" and "For comparable results we recommend to use the same optimization criterion": the publisher's one deliberate choice (MET-5), `roc_auc`, which is also the fallback; inputs none.
- Risks for /add-dataset: the overlap with `ames_mutagenicity` (PROV-6), counted before either is built; conflicting labels across the merged sources, and salts or stereoisomers that collapse onto the same 2D descriptors (LEAK-17); features are computed from the SMILES (CLEAN-24); `source` and `reference` are provenance columns, not features.
- Priority: gap 0 (chemistry & material science and binary classification are not thin), use case 0 (no actor or decision in what could be read), source +, shape + (6,512 compounds), risk - (the larger, overlapping `ames_mutagenicity`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 93: "A Comparative Study to Benchmark Cross-Project Defect Prediction Approaches".
- as published: 6,512 compounds in version 2 (April 2009; version 1 had 7,090) with the Ames result, CAS and SMILES, compiled from CCRIS, Kazius/Bursi, Helma, Feng, VITIC and GeneTox; download page offers CSV and ...; target: Ames test result: mutagen or non-mutagen; access: open.
- Why: a measured regulatory endpoint whose prediction is written into a guideline, so the decision is explicit
- Adds: no mutagenicity task in the benchmark. Checks: overlap and label conflicts between the merged sources, and whether Xu 2012 is a version of the same compilation (PROV-6) or its own record

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: overlapping Ames compilations (Xu 2012 and Hansen 2009) (`ames_mutagenicity`; PROV-6). The curator keeps one, or both as distinct tasks.
