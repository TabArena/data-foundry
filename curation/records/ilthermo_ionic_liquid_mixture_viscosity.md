---
unique_name: ilthermo_ionic_liquid_mixture_viscosity
name: 'ILThermo ionic liquid mixtures: viscosity and ionic conductivity'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: GOV Website
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://ilthermo.boulder.nist.gov/
- https://doi.org/10.1021/je700171f
- https://github.com/chemcognition-lab/chemixhub/tree/main/datasets/ionic-liquids
- https://arxiv.org/abs/2506.12231
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: NIST ILThermo's measured viscosities (75,992 points, 15,878 mixtures, 699 molecules) and ionic conductivities (40,904 points) of ionic-liquid mixtures at given compositions and temperatures, compiled from the literature and cut into tasks by CheMixHub (2025); a real property-screening regression with molecule inputs, but two targets share the record and CheMixHub filled missing temperatures with a default.
- Source: ILThermo, the NIST ionic liquids database (https://ilthermo.boulder.nist.gov/), described by Dong, Muzny, Kazakov, Diky, Magee, Widegren, Chirico, Marsh, Frenkel, "ILThermo: A Free-Access Web Database for Thermodynamic Properties of Ionic Liquids", J Chem Eng Data 52 (2007), https://doi.org/10.1021/je700171f (not read): experimental values curated from published papers. Task tables: CheMixHub (Rajaonson, Rajabi Kochi, Mejia Mendoza, Moosavi, Sanchez-Lengeling, arXiv 2506.12231, v2 2025-11-28; Sec. 3.2 "IlThermo (2 tasks)", Table 1): viscosity 75,992 points, 15,878 mixtures, 699 molecules, target ln(η); ionic conductivity 40,904 points, 14,438 mixtures, 479 molecules, target ln(κ) in S/m; inputs the components (SMILES), mole fractions and temperature; "Standard conditions (298.15K) are assumed if temperature values are not reported" (Sec. 3.3). The curation steps are in its Appendix A.3 (not read); the GitHub folder holds raw_data and processed_data (not opened).
- Use case: a chemist or electrolyte designer screening ionic-liquid mixtures for a viscosity or conductivity before making them (CheMixHub names battery electrolytes among its applications); fit approximate (a field, no decision named). Regime grouped: the rows of one mixture at many compositions and temperatures are near-duplicates, and the real question is a new mixture or a new ionic liquid (CheMixHub's leave-molecules-out split, Sec. 3.4, next to random, mixture-size and temperature splits).
- Siblings and duplicates: the other CheMixHub records: `drug_solubility_binary_solvent_mixtures` (`TBD -> Yes`, priority 2), `nist_binary_liquid_mixture_viscosity` (unscreened; another NIST-derived viscosity compilation, Zenodo 8042966 and Chem Eng J 2023, whose overlap with ILThermo's pairs is not checked), `solid_polymer_electrolyte_ionic_conductivity` (unscreened; polymer electrolytes, another task), `bigsoldb_2`, `flash_point_sun_morgan`. External collections: CheMixHub (not in our vocabulary).
- Better data: from the curator's Zotero collection (item 77, CheMixHub); no search for better data in this run.
- Papers and pages: Dong et al. 2007; CheMixHub (arXiv 2506.12231).
- Metric: CheMixHub writes "We report results across mean absolute error (MAE)" (Sec. 4.2), with Pearson and Kendall correlations in Appendix A.9, on the log targets: the one metric of its main tables, borderline MET-5: `mae` on ln(η) if read as its choice, else the fallback `rmse` (MET-8). Inputs none.
- Risks for /add-dataset: two targets in one record (viscosity and conductivity, two tasks of one source, PROV-7): two datasets, or one picked; the 298.15 K default for missing temperatures is CheMixHub's, so build from ILThermo with its own temperature and pressure fields, or drop those rows (PROV-13); molecule inputs need fixed descriptors or a featurization fit inside the training folds (SMILES strings are no tabular input, SEL-12); conflicting measurements of one mixture from different papers; the group key (mixture or ionic liquid) to choose (SPLIT-24).
- Priority: gap 0 (chemistry, regression and grouped are not thin), use case 0 (a field, no decision named), source + (NIST database with a JCED paper, and the CheMixHub paper), shape + (tens of thousands of points in thousands of mixtures), risk - (two targets to separate and a default temperature to undo).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 77: "CheMixHub: Datasets and Benchmarks for Chemical Mixture Property Prediction".
- as published: viscosity: 75,992 points, 15,878 mixtures, 699 molecules; ionic conductivity: 40,904 points, 14,438 mixtures, 479 molecules; components (SMILES), mole fractions, temperature; target: ln viscosity (Pa s); ln ionic conductivity (S/m) (two tasks of one source, PROV-7); access: open.
- Why: large, experimental, literature-compiled by NIST
- Adds: ionic-liquid property regression with temperature and composition
