---
unique_name: suzuki_miyaura_hte_yields
name: Suzuki-Miyaura cross-coupling yields from a nanomole-scale flow screen (Perera et al. 2018)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2018'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1126/science.aap9112
- https://github.com/leojklarner/gauche/blob/main/gauche/datasets/reactions/SuzukiMiyaura.csv
- https://github.com/open-reaction-database/ord-data/blob/main/data/68/ord_dataset-68cb8b4b2b384e3d85b5b1efae58b203.parquet
- https://github.com/rxn4chemistry/rxn_yields
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, papers and a preview of the files, NOT from a full inspection of the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 5,760 Suzuki-Miyaura coupling yields from Pfizer's nanomole-scale flow screen (Perera et al., Science 2018), a full factorial of 15 substrate pairs x 12 ligands x 8 bases x 4 solvents; the companion of `buchwald_hartwig_yields` for a second reaction class, with the same weakness: few substrates, so a random split tests the grid.
- Source: Perera et al., "A platform for automated nanomole-scale reaction screening and micromole-scale synthesis in flow", Science 359:429-434 (2018, doi 10.1126/science.aap9112; paywalled, PROV-17): LC-MS data for 5,760 reactions at more than 1,500 reactions per day (abstract, per a search summary). The ML-ready file is Schwaller et al.'s (rxn_yields), mirrored in gauche (`SuzukiMiyaura.csv`, previewed 2026-10-31) and in the Open Reaction Database (ord_dataset-68cb8b4b...). As published in gauche: 5,760 rows x 8 columns (`reactant_1_smiles`, `reactant_2_smiles`, `catalyst_smiles`, `ligand_smiles`, `reagent_1_smiles`, `solvent_1_smiles`, `rxn`, `yield`): 7 electrophile strings (the string includes what looks like an internal standard), 4 nucleophiles, 15 pairs, one palladium source, 12 ligands, 8 bases, 4 solvents; `yield` a fraction from 0 to 1, mean 0.40, 275 zeros.
- Use case: a chemist, before running a coupling on a substrate pair, picks the ligand, base and solvent: the screen exists to find the conditions that are then run at scale (the best conditions were reproduced in flow and batch at 50 to 200 mg, per the abstract summary); fit direct for the condition choice, approximate for a new substrate pair. Regime open, as for `buchwald_hartwig_yields`: grouped by substrate pair gives 15 groups (few), a random split interpolates the grid.
- Siblings and duplicates: `buchwald_hartwig_yields` (`TBD -> Yes`, 3; Ahneman et al. 2018, C-N coupling, the same kind of designed grid); `cn_coupling_hte_50k` (`TBD -> Yes`, 3), `amide_coupling_hte_47k` (`TBD -> Yes`, 4), `pfizer_hte_39k` and `pfizer_hitea_reaction_yield` (Pfizer's batch HTE release, which includes Suzuki couplings; whether it holds these flow reactions was not checked), `uspto_reaction_yields` (`TBD -> 2nd Tier`, 2), `ord_reaction_yields` (`TBD -> 2nd Tier`, 1; ORD hosts this set), `catechol_solvent_selection_yields`: other reactions or campaigns (PROV-7), to be ordered by the curator. No other record carries this source. External collections: Open Reaction Database, gauche, rxn_yields, awesome-chemistry-datasets; not in ChemPile-LIFT (the run's note).
- Better data: from the awesome-chemistry-datasets list and the curator's Zotero collection (items 151 and 191); no further search this round.
- Papers and pages: Perera et al. 2018 (the data); Schwaller et al. (rxn_yields README: "Using 10 random splits, we demonstrate that the hyperparameters optimised on the Buchwald-Hartwig were transferable"); gauche (Griffiths et al.), which uses the set for Bayesian optimisation of conditions.
- Metric: the yield-prediction papers report R2 over random splits (rxn_yields), not a metric chosen for a decision; declare the fallback `rmse` on the yield, as for `buchwald_hartwig_yields` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: a designed factorial with 15 substrate pairs: run the naive controls (component identity only, random features) that Chuang and Keiser applied to the Buchwald-Hartwig set (TP-4, TP-10); parse the components into categorical factors with descriptors; `rxn` concatenates the other columns and adds the product, one representation, not extra information; the yield definition (an LC area ratio against an internal standard?) was not read in the paper.
- Priority: gap 0 (chemistry & material science and regression are not thin), use case + (condition choice for scale-up, the paper's own aim), source + (a Science paper, an ORD deposit), shape + (5,760 reactions, five categorical factors), risk - (a designed grid with 15 substrate pairs).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 151: "An Explainable Ensemble Learning Framework for Crop Classification with Optimized ..."; the curator's Zotero collection, item 191: "blaiszik/awesome-matchem-datasets".
- as published: 5,760 reactions: 15 electrophile-nucleophile pairs x 12 ligands (one blank) x 8 bases (one blank) x 4 solvents; columns reactant_1, reactant_2, catalyst, ligand, reagent, solvent, reaction SMILES, ...; target: LC-measured yield of the Suzuki-Miyaura coupling; access: open.
- Why: measured HTE with categorical components; a standard yield benchmark next to Buchwald-Hartwig | real measured yields on an automated nanomole platform; the standard companion to the Buchwald-Hartwig grid
- Adds: a second reaction class; not found by the scouting (ChemPile-LIFT has no Suzuki set). Risks: 15 substrate pairs only; full factorial, so a random split mostly tests interpolation | no record; a designed grid with few substrate pairs, so it needs a split grouped by substrate pair. HiTEA is the larger, more diverse ...
