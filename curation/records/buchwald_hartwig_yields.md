---
unique_name: buchwald_hartwig_yields
name: buchwald_hartwig
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- ChemPile
original_source: Other
year: '2018'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1126/science.aar5169
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/buchwald_hartwig ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/buchwald_hartwig ; original: https://github.com/reymond-group/drfp/tree/main/data ; https://github.com/rxn4chemistry/rxn_yields (preprocessing)'
- https://arxiv.org/abs/2505.12534
- https://github.com/leojklarner/gauche/blob/main/gauche/datasets/reactions/DreherDoyle.csv
- https://github.com/open-reaction-database/ord-data/blob/main/data/46/ord_dataset-46ff9a32d9e04016b9380b1b1ef949c3.parquet
- https://github.com/rxn4chemistry/rxn_yields
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 3,955 measured C-N coupling yields from a nanomole-scale HTE screen, the standard reaction-yield table; a published comment disputes how much of its signal is chemistry, and the run found a larger set of the same reaction class.
- Source: Ahneman, Estrada, Lin, Dreher and Doyle 2018, "Predicting reaction performance in C-N cross-coupling using machine learning", Science 360:186 (doi 10.1126/science.aar5169); the ML-ready file is Schwaller et al.'s (rxn_yields, doi 10.1016/j.checat.2020.12.002) and is mirrored in gauche (DreherDoyle.csv, MIT) and in the Open Reaction Database. As published (the gauche file previewed 2026-10-31, 3,955 rows): ligand, additive, base and aryl halide as SMILES strings, the full reaction SMILES, and the yield in percent; 4 ligands, 22 additives, 3 bases and 15 aryl halides, a near-complete 4 x 22 x 3 x 15 factorial; yields 0 to 100, mean 33.1, 236 of them zero.
- Use case: a process or medicinal chemist, before running a coupling on a substrate, picks the ligand, base and additive to use ("Chemists often discover reactions by applying catalysts to a series of simple compounds. Tweaking those reactions to tolerate more structural complexity in pharmaceutical research is time-consuming", the publisher's summary of the paper); fit direct for the condition choice, approximate for a new substrate, since the screen holds one amine and 15 aryl halides; regime open: the source's own out-of-sample tests hold out additives, and a grouped split by aryl halide would have 15 groups (the weighed factor against a grouped split with few groups applies).
- Siblings and duplicates: `cn_coupling_hte_50k` (Cernak group, 50,688 Pd-, Ni- and Cu-catalysed C-N couplings), `suzuki_miyaura_hte_yields`, `pfizer_hte_39k`, `amide_coupling_hte_47k`, `uspto_reaction_yields` and `ord_reaction_yields` are the other reaction-yield records of this run: other reactions or other labs, so distinct tasks (PROV-7), to be ordered by the curator. No record carries this source. External collections: ChemPile / ChemNLP (config `buchwald_hartwig`), the Open Reaction Database, gauche, drfp.
- Better data: a candidate of the benchmark ChemPile; the run recorded `cn_coupling_hte_50k` (https://doi.org/10.1021/jacs.6c05959, 50,688 reactions, three metals, ultra-HTE) as better data for this task; no further search this round.
- Papers and pages: Ahneman et al. 2018 (the data); Chuang and Keiser 2018, "Comment on 'Predicting reaction performance in C-N cross-coupling using machine learning'", Science 362:eaat8603; Schwaller et al. 2021 (rxn_yields, the file and the splits).
- Metric: the source and its follow-ups rank models by R2 on held-out reactions (rxn_yields reports R2 over ten 70/30 random splits and on the source's out-of-sample sets); R2 and RMSE order models the same way within a fold, so declare `rmse` on the yield in percent (MET-5, MET-8); inputs none. The Science paper's own text is paywalled and was not read (PROV-17): the metric rests on the publisher's summary and the rxn_yields README, so treat it as unverified.
- Risks for /add-dataset: Chuang and Keiser 2018 state that "the experimental design is insufficient to distinguish models trained on chemical features from those trained solely on random-valued features in retrospective and prospective test scenarios, thus failing classical controls in machine learning" - on a random split the task may be little more than recognising the grid cell, so run the naive controls (random features, component identity only) before shipping and prefer the source's held-out-additive design (TP-4, TP-10); the components are 44 distinct chemicals in all, so they ship as categorical factors (with descriptors), not as text; the rows are a designed factorial rather than a draw from a population, which is how the field frames the task but worth a line in the fit (USE-8).
- Priority: gap 0, use case +, source +, shape + (3,955 rows, four categorical factors), risk - (better data `cn_coupling_hte_50k`, and the published control critique).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 149: "TabPFN Extensions for Interpretable Geotechnical Modelling"; the curator's Zotero collection, item 191: "blaiszik/awesome-matchem-datasets".
- as published: 3,955 reactions (Ahneman et al. 2018 HTE plates); in ChemPile-LIFT 47,448 text prompts over 1 config(s); target: reaction yield (%); access: open.
- Why: Predict the yield of a Buchwald-Hartwig C-N cross-coupling from the reactants, ligand, base and additive, so a chemist can pick the conditions to run | measured nanomole-scale HTE with categorical components: genuinely tabular; the standard yield benchmark | the canonical reaction-yield benchmark, real measurements
- Adds: | already proposed by the ChemPile-LIFT scouting (same name); no reaction-yield task in the benchmark. Risks: one amine and 15 aryl halides, so a grouped split by aryl halide has 15 groups; the larger Cernak set (cn_coupling_hte_50k) covers the same reaction class | already proposed as buchwald_hartwig_yields in ...
- Notes: Ahneman, Estrada, Lin, Dreher and Doyle 2018 (Science 360:186), a nanomole-scale high-throughput experimentation screen; the ML-ready version is from Schwaller et al. 2021 (doi 10.1016/j.checat.2020.12.002 / rxn_yields). Genuinely tabular once the reaction is split into its components (3-4 categorical factors plus ...
