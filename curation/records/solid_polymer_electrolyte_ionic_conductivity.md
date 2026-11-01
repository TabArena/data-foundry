---
unique_name: solid_polymer_electrolyte_ionic_conductivity
name: Solid polymer electrolyte ionic conductivity
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Github
year: '2023'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/chemcognition-lab/chemixhub/tree/main/datasets/polymer-electrolyte
- https://doi.org/10.1021/acscentsci.2c01123
- https://github.com/learningmatter-mit/Chem-prop-pred
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: about 12,000 literature measurements of solid polymer electrolyte ionic conductivity (Bradford et al., MIT, 2023) with polymer and salt structures, composition and temperature; a real materials-screening task, but the inputs are molecules as SMILES and each formulation repeats over temperatures.
- Source: Bradford, Lopez, Ruza, Stolberg, Osterude, Johnson, Gomez-Bombarelli, Shao-Horn, "Chemistry-Informed Machine Learning for Polymer Electrolyte Discovery", ACS Cent Sci 9(2):206-216 (2023), doi 10.1021/acscentsci.2c01123, PMC9951296 (read): 7,133 points extracted by hand from 135 publications screened for experimental practice (SI Table S1), plus 6,250 from two earlier data sets; "over 12,000 ionic conductivity data points for over 3,000 unique electrolyte formulations" (Table 1: 12,383 points, 247 polymers, 3,195 unique species in total). Data: GitHub `learningmatter-mit/Chem-prop-pred` (MIT), `data/PolymerElectrolyteData.csv` (6.1 MB; per polymer and salt the name, SMILES, BigSMILES, end groups, mol and weight fractions, Mw, Mn, dispersity, with the source DOI and who recorded it) and `clean_train_data.csv`. CheMixHub (Rajaonson et al., arXiv 2506.12231, 2025) serves the same raw file (`raw_data/PolymerElectrolyteData.csv`, same size), processed to 11,350 measurements of 1,749 mixtures (the run's note; not checked).
- Use case: a battery-materials researcher ranks candidate polymer-salt formulations by predicted conductivity before synthesising them; the paper screens over 20,000 candidate formulations "for future experimental characterization". Fit direct. Regime grouped by polymer: the paper's 10-fold CV holds polymers out ("each test and validation set contained only polymers that did not appear in the training set").
- Siblings and duplicates: no other polymer-electrolyte record (grep: ionic conductivity, polymer electrolyte, Chem-prop-pred). Other CheMixHub tasks with records: `drug_solubility_binary_solvent_mixtures`, `bigsoldb_2`, `ilthermo_ionic_liquid_mixture_viscosity`, `nist_binary_liquid_mixture_viscosity` (other properties, PROV-7). External collections: CheMixHub (not in the vocabulary).
- Better data: from the curator's Zotero collection (item 77, CheMixHub); no further search this round.
- Papers and pages: the ACS Cent Sci paper; CheMixHub, https://arxiv.org/abs/2506.12231 (moved here from source_links as related work, PROV-12; the source's GitHub added).
- Metric: MAE of log10 conductivity with Spearman R (Table 2), two side by side, so the fallback `rmse` on log10 conductivity (MET-5, MET-8); MAE is the paper's headline and the curator may prefer `mae`. Inputs none.
- Risks for /add-dataset: take the source's file, not CheMixHub's processing (PROV-8); the inputs are SMILES, BigSMILES and fractions, so features are computed (CLEAN-24), and graph models are the field's tool (ChemArr, Chemprop; weigh under SEL-12); several temperatures per formulation (group by polymer, SPLIT-24); the target's units and log scale, and the temperature units, to check; data pooled from 217 papers, with the DOI as a possible group.
- Priority: gap 0 (chemistry and regression covered), use case + (the paper's screening of candidate formulations), source + (a peer-reviewed paper with an MIT-licensed release), shape + (about 12,000 measurements, 247 polymers), risk - (molecule-string inputs where graph models are the field's tool).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 77: "CheMixHub: Datasets and Benchmarks for Chemical Mixture Property Prediction".
- as published: 11,350 measurements, 1,749 polymer-salt mixtures, 402 molecules; components (SMILES), composition, temperature; target: ln ionic conductivity; access: open.
- Why: experimental literature data, an active materials-discovery task
- Adds: battery-materials property regression
