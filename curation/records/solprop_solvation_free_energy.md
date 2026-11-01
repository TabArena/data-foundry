---
unique_name: solprop_solvation_free_energy
name: 'SolProp data collection: experimental solvation free energies and solid solubilities'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2022'
domain: chemistry & material science
problem_type: Regression
source_links:
- https://doi.org/10.5281/zenodo.5970538
- https://doi.org/10.1021/jacs.2c01768
- https://arxiv.org/abs/2012.11730
- https://doi.org/10.1016/j.cej.2021.129307
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: MIT's SolProp collection (Zenodo, CC BY 4.0), whose main table is CombiSolv-Exp, experimental solvation free energies of neutral solute-solvent pairs at 298 K (10,145 pairs of 291 solvents and 1,368 solutes, of which the public release leaves out the proprietary MNSol entries); a measured regression over two molecules, one step before the solvent choice it serves.
- Source: Vermeire and Green, "Transfer learning for solvation free energies: from quantum chemistry to experiments", Chem Eng J (2021, doi 10.1016/j.cej.2021.129307; arXiv 2012.11730, December 2020), Sec. 2.2: CombiSolv-Exp combines MNSol, FreeSolv, CompSol (Moine et al.) and the Abraham group's data, "Only solvation free energies at temperatures of 298K (±2K) are accounted for", ionic species and self-solvation removed, duplicates averaged or removed when their SD exceeds 0.20 kcal/mol; "The final database consists of 10145 solvent/solute combinations for 291 solvents and 1368 solutes. The CombiSolv-Exp database is provided as part of the Supporting Information, excluding the data from the proprietary MNSol database" (Table 1, entries before merging: MNSol 2,275, FreeSolv 560, CompSol 3,548, Abraham 6,091). The SolProp data collection (Vermeire, Chung and Green; Zenodo doi 10.5281/zenodo.5970538, v1.2 of 2022-07-01, one 268.6 MB zip, not opened) accompanies "Predicting Solubility Limits of Organic Solutes for a Wide Range of Solvents and Temperatures", JACS 2022 (doi 10.1021/jacs.2c01768), and holds "solvation free energy at 298K (dGsolv), solvation enthalpy at 298K (dHsolv), Abraham Solute Parameters (E,S,A,B,L), aqueous solid solubility at 298K (logSaq), and solid solubility in organic solvents at various temperatures (logS)"; "The dataset is limited to neutral solutes and solvents" (Zenodo page). The solid solubilities are "more than 5,000 experimental solubility values for validation of the model" (ChemRxiv abstract, per a search summary). The counts per table are in the zip's ReadMe, not read; SolvBERT calls its copy "CombiSolv-Exp-8780", a portion of the 10,145, and whether that is the public table was not checked.
- Use case: a chemist or process engineer screening solvents for a solute (reaction medium, extraction, crystallisation) estimates the solvation free energy, from which partition coefficients and, with the solid's properties, the solubility follow; ours to state, the papers name no actor; fit approximate, one step before the solubility or partitioning decision. Regime grouped on the solute (a new compound is the case to predict); the source scores random splits and tests transfer by holding out solvents, solute elements and molar-mass ranges (Sec. 5).
- Siblings and duplicates: `freesolv` (`TBD -> 2nd Tier`, 1; 642 hydration free energies, 560 of which entered CombiSolv-Exp, so its rows are mostly a subset of this table's water rows); `bigsoldb_2` (`TBD -> Yes`, 3) and `drug_solubility_binary_solvent_mixtures` (`TBD -> Yes`, 2) hold solid solubility, which overlaps SolProp's logS part; `aqsoldb` and `somas_aqueous_solubility` hold aqueous solubility, as SolProp's logSaq does. Not a duplicate of any (PROV-4: a compilation with a task of its own, solvation over many solvents); the solid-solubility part is a cut the BigSolDB records hold at larger size (PROV-6), so this record should ship dGsolv. External collections: awesome-chemistry-datasets.
- Better data: from the awesome-chemistry-datasets list and the curator's Zotero collection (item 91); no further search this round.
- Papers and pages: Vermeire and Green 2021 (CombiSolv-Exp and the COSMO-RS set CombiSolv-QM); Vermeire, Chung and Green 2022 (SolProp; the JACS page refused access, PROV-17); SolvBERT (uses the 8,780-row copy); the SolProp_ML package (mixtures).
- Metric: the source reports RMSE and MAE side by side (abstract: MAE 0.21 kcal/mol on a random test split; Figs. 4 to 7 give both), with no one named criterion, so the fallback `rmse` in kcal/mol (MET-5, MET-8); inputs none.
- Risks for /add-dataset: the release sits next to computed values (CombiSolv-QM, 1 million COSMOtherm solvation free energies): take the experimental table only, and never a computed dGsolv as a feature (SEL-16, LEAK); the inputs are two SMILES strings, so the definition computes descriptors for solute and solvent; count the public rows once the zip is opened (no TP-5 risk at several thousand); experimental noise across sources (the paper's 0.20 kcal/mol SD filter) is label noise, not a leak.
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (the papers name no actor or decision), source + (two papers and a versioned Zenodo release with a ReadMe), shape + (thousands of pairs over about 290 solvents, a solute grouping), risk - (the proprietary part is missing, computed values ship alongside, the solubility part overlaps BigSolDB).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 91: "Frame-Guided Synthetic Claim Generation for Automatic Fact-Checking Using High-Volume ...".
- as published: one zip of 269 MB (not opened): experimental solvation free energies at 298 K for about 10,145 solute-solvent pairs per the list, experimental solvation enthalpies, Abraham solute parameters, ...; target: experimental solvation free energy (kcal/mol) of a neutral solute in a solvent at 298 K; access: open.
- Why: measured target over many solvents, about 15 times FreeSolv (item 78, 642 hydration free energies)
- Adds: a solute-solvent thermodynamics task; lower priority: the decision is one step removed, the experimental part must be separated from the COSMO-RS part, and the solid solubilities overlap BigSolDB
