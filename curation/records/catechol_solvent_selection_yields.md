---
unique_name: catechol_solvent_selection_yields
name: 'The Catechol Benchmark: solvent selection data for a catechol rearrangement'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Kaggle
year: '2025'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/aichemy/catechol-benchmark
- https://doi.org/10.52202/085713-3994
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 1,227 flow-reactor measurements of one reaction (the rearrangement of an allyl-substituted catechol) over 24 solvents and 13 solvent pairs, residence time and temperature, with three yields as targets; a NeurIPS 2025 benchmark and a Kaggle community competition scored leave-one-solvent-out, but small, one reaction, and built from 87 continuous ramps.
- Source: Boyne, Campos, Langdon, Qing, Xie, Zhang, Tsay, Misener, Davies, Jelfs, Boyall, Dixon, Schrecker and Folch, "The Catechol Benchmark: Time-series Solvent Selection Data for Few-shot Machine Learning", NeurIPS 2025 Datasets and Benchmarks (arXiv 2506.07619; doi 10.52202/085713-3994); data on Kaggle, aichemy/catechol-benchmark (MIT, files of 2025-05-15). As published (file list through the Kaggle API; catechol_full_data_yields.csv counted 2026-10-31): 1,227 rows x 19 columns (EXP NUM, SOLVENT A and B NAME, SolventB%, Residence Time, Temperature, the yields SM, Product 2 and Product 3, the SMILES of the species and solvents, ratios, reaction SMILES, RAMP NUM), 24 solvents, 13 solvent pairs, 87 ramps; catechol_single_solvent_yields.csv (656 points, the paper's Table 1); claisen_data_clean.csv (allyl phenyl ether, 283 points, "from an external source"); solvent descriptor lookups (ACS PCA, DRFPs, fragprints, Spange).
- Use case: a process chemist replacing or choosing the solvent for this reaction predicts the yields in a solvent not yet run, to pick conditions for scale-up ("solvent replacement and sustainable manufacturing", abstract); fit direct for this one reaction, not for reactions in general; regime grouped by solvent (single solvents) or solvent pair (mixtures), the paper's leave-one-out design (Sec. 3.2).
- Siblings and duplicates: none (grep catechol); `suzuki_miyaura_hte_yields`, `cn_coupling_hte_50k`, `amide_coupling_hte_47k` and `uspto_reaction_yields` are yields of other reactions. External collections: the Kaggle "Catechol Benchmark Hackathon (NeurIPS 2025 DnB)" (AIchemy, 2025-11-03 to 2026-01-16, 227 teams, 2,600 USD).
- Better data: from the curator's Zotero collection (item 191, awesome-matchem-datasets); no further search this round.
- Papers and pages: the NeurIPS paper (arXiv HTML read: Sec. 1.2, Table 1, Sec. 3.2, Table 3); the Kaggle dataset and competition.
- Metric: the paper: "Mean squared error (MSE) and negative log predictive density (NLPD) are averaged across all leave-one-out data splits" (Table 3, Sec. 3.2), MSE for every model and NLPD for the probabilistic ones; the competition scores a custom `catechol_hackathon_metric` (Kaggle API) whose definition was not read (the evaluation page did not render); so MSE on the yield (`rmse`) unless the competition's metric says otherwise (MET-4); inputs none.
- Risks for /add-dataset: three yields measured together (starting material, products 2 and 3): ship one and drop the others (LEAK-10), or flag `Multi-target`; rows along a ramp are consecutive readings of a transient flow experiment (the paper names non-stationarity, bias and heteroskedasticity), so keep whole ramps within a group (SPLIT-24); runs with an unexpected side reaction were left out of the paper's numbers ("we removed the affected results from our benchmark numbers"), so check whether they are in the file; 24 solvents give few groups per fold (TP-5, SPLIT-27); the 283-row Claisen file is another reaction from another source.
- Priority: gap 0 (chemistry, regression, grouped not thin), use case +, source +, shape 0 (1,227 correlated readings from 87 ramps, 5 inputs), risk - (three targets, ramp-correlated rows).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 191: "blaiszik/awesome-matchem-datasets".
- as published: 1,200+ process conditions over 24 solvents and binary mixtures from flow-reactor ramps: catechol_full_data_yields.csv (520 KB), catechol_single_solvent_yields.csv (187 KB), plus solvent descriptor ...; target: yields of the starting material and the two products; access: open.
- Why: real measured flow-chemistry yields published as an ML benchmark with a leave-one-solvent-out task
- Adds: no record. Small and only one reaction; the rows come from continuous ramps, so neighbours are correlated (group by solvent and ramp)
