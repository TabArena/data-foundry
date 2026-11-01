---
unique_name: mofsimplify_mof_stability
name: 'MOFSimplify: thermal and solvent-removal stability of about 3,000 metal-organic frameworks'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2021'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1038/s41597-022-01181-0
- https://doi.org/10.5281/zenodo.5737968
- https://github.com/SimonEnsemble/porous-material-AI-gym
- https://doi.org/10.1021/jacs.1c07217
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 3,132 experimentally characterised MOFs with a thermal decomposition temperature read from published TGA traces, and 2,179 with a solvent-removal stability label mined from the papers' text, with 134 RAC and 14 pore-geometry features; a measured materials task among the simulated MOF sets, with label noise to weigh.
- Source: first published by Nandy, Duan and Kulik, "Using Machine Learning and Data Mining to Leverage Community Knowledge for the Engineering of Stable Metal-Organic Frameworks", JACS 143 (2021), doi 10.1021/jacs.1c07217 ("From nearly 4000 manuscripts, we use natural language processing and image analysis to obtain over 2000 solvent-removal stability measures and 3000 thermal degradation temperatures", abstract); data descriptor: Nandy, Terrones, Arunachalam, Duan, Kastner and Kulik, "MOFSimplify, machine learning models with extracted stability data of three thousand metal-organic frameworks", Scientific Data (2022), doi 10.1038/s41597-022-01181-0 (PMC8917177, read); Zenodo 10.5281/zenodo.5737968 (CC BY 4.0, SciData.zip, 35.7 MB: JSON and CSV of both sets, SBU and linker mol2 files, the two ANN models). As published (Methods): Td for 3,132 CoRE MOF 2019 structures, from two lines fitted to four points of each TGA trace digitised with WebPlotDigitizer, Td at their intersection; solvent-removal labels for 2,179 from regular expressions and Stanza dependency parsing, a label only when all sentences of a manuscript agree; 134 revised autocorrelation features (Table 2) and 14 Zeo++ geometric descriptors (Table 3).
- Use case: a chemist screening candidate frameworks before synthesis decides which are stable enough to make and activate (the models "enable prediction of stability on new MOFs with quantified uncertainty", abstract; the MOFSimplify web interface serves such predictions); fit direct for frameworks with a known crystal structure; regime IID by MOF (the paper's train, validation and test partitions, ratio not stated); shared linkers or metal nodes would make a grouped split the harder variant.
- Siblings and duplicates: the ChemPile MOF records `qmof_quantum`, `qmof_gcmc` and `core_mof_gas_uptake` (all `No`, AHDS, simulated labels) name this record as the measured counter-case; `mofdscribe_descriptions` (ChemPile, text). No duplicate (grep: mofsimplify, metal-organic, MOF). External collections: none in our vocabulary; listed in the SimonEnsemble porous-material-AI-gym link list (not a benchmark).
- Better data: from the awesome-chemistry-datasets list; the Assessment's Zotero item 165 ("Clinical Proteomics Program Databank - Proteomic Patterns") does not match this dataset. No further search this round.
- Papers and pages: the JACS 2021 abstract (Europe PMC) and the Scientific Data paper (read); the MOFSimplify web interface (community feedback and active learning).
- Metric: for Td the only metric reported is MAE (47 °C for the earlier ANN, 55 °C on a hand-labelled blind set of 40 MOFs), one metric, not argued: `mae` in °C is a candidate (MET-5, MET-10), else the fallback `rmse`; for solvent removal accuracy (0.76) and AUC (0.79) side by side, so the fallback `roc_auc`; inputs none.
- Risks for /add-dataset: two tasks of one source (Td regression and solvent-removal binary, PROV-7), ship one or both; the solvent-removal label is NLP-extracted (of 100 checked: 78 correct, 2 wrongly unstable, 20 ambiguous), so label noise; Td is a hand-digitised reading of a plotted curve; the RAC and Zeo++ features are computed from CIFs, so pin the featurisation (CLEAN-24); near-identical frameworks reported by one paper.
- Priority: gap 0 (chemistry & material science and regression are not thin), use case + (screening frameworks before synthesis, named by the source), source + (two papers and an open deposit), shape + (3,132 MOFs, 148 features), risk - (NLP-extracted and digitised labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 165: "Clinical Proteomics Program Databank - Proteomic Patterns".
- as published: about 3,000 MOFs with a thermal decomposition temperature read from digitised TGA traces and about 2,000 with a solvent-removal stability label mined from the text by NLP; RAC and pore-geometry ...; target: thermal decomposition temperature (regression) or stable on solvent removal (binary); access: open.
- Why: measured (TGA) target for real, structurally characterised MOFs, in a field whose other labelled sets are simulated
- Adds: a measured materials property with ready tabular features. Risks: the solvent-removal label is NLP-extracted; features computed from CIFs; digitised curves
