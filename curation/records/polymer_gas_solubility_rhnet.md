---
unique_name: polymer_gas_solubility_rhnet
name: Solubility of gases, vapours and supercritical fluids in amorphous polymers (rhnet dataset)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Github
year: '2023'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/Shorku/rhnet/tree/main/data
- https://doi.org/10.1039/D3PY01028G
- https://doi.org/10.26434/chemrxiv-2023-tqv4p-v4
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: about 16,000 measured uptakes of 81 gases and vapours in 107 polymers, compiled from 276 papers with a DOI per row, for predicting sorption in a polymer not yet measured; the rows are points on 518 isotherms, so the real units are far fewer than the rows.
- Source: O. I. Gromov, "Predicting the Solubility of Gases, Vapors, and Supercritical Fluids in Amorphous Polymers from Electron Density using Convolutional Neural Networks", Polym. Chem. 2024, 15, 1273-1296 (doi 10.1039/D3PY01028G); preprint ChemRxiv 2023 (doi 10.26434/chemrxiv-2023-tqv4p-v4); data in github.com/Shorku/rhnet (MIT licence; `data/experimental_dataset.csv` first committed 2023-05-12, last changed 2024-01-24; the README says the project is no longer updated and points to RhNet2, a general QSPR tool without new sorption data). Abstract (Crossref): "A dataset of almost 15000 experimentally measured uptakes (0.01-50 wt%) of 79 gases in 102 different polymers under pressures from 1E-3 – 7E+2 bar range and temperatures from 233-508 K range is collected from over 250 literature sources." As published (file read 2026-10-31): 16,004 rows x 13 columns (`expno`, `polymer` and `solvent` ids, the polymer's `mn`, `mw`, `cryst`, `tg`, `dens`, then `pressure`, `temperature`, the target `wa` (weight fraction, 0.0001 to 0.71), `doi`, `notes`); 107 polymers, 81 solvents, 518 polymer-solvent pairs, 276 DOIs. `list_of_polymers.csv` and `list_of_solvents.csv` give names and SMILES (repeat units with `*` ends), so the run's note that SMILES are missing is wrong; `solvent_macro_features.csv` adds boiling and critical temperatures and the critical pressure; `test_pairs.csv` (67 pairs) and `val_pairs.csv` (45 pairs) are the author's held-out pairs.
- Use case: for example, an engineer choosing a polymer for a gas-separation membrane, a barrier or a foaming process estimates how much of a gas the polymer takes up at a pressure and temperature before measuring it (ours to state; the abstract only names the range, "from typical low-pressure sorption in membrane glassy polymers to high-pressure solubility of supercritical fluids in molten polymers"); fit approximate. Regime grouped: the points of one isotherm are close to each other, and the abstract's test set is "1600 experimental measurements concerning 22 polymers previously unseen by the model", so split by polymer (or at least by polymer-solvent pair).
- Siblings and duplicates: no other sorption record (grep: rhnet, solubility, sorption, uptake, polymer); `bicerano_polymer_tg` (`TBD -> 2nd Tier`, 1), `block_copolymer_phase` and `solid_polymer_electrolyte_ionic_conductivity` are other polymer property tasks (PROV-7). External collections: listed in blaiszik/awesome-matchem-datasets (a list, not a benchmark).
- Better data: from the curator's Zotero collection (item 99, awesome-matchem-datasets); no further search this round.
- Papers and pages: the paper and preprint above (the RSC and ChemRxiv full texts returned 403; read through the Crossref abstract and the repository README); the per-row DOIs name the 276 original measurement papers.
- Metric: MAPE, the only error measure in the abstract ("Irreducible mean absolute percentage error (MAPE) is approximately estimated to be ~20%", and "31% MAPE on a test set"); whether the paper ranks or tunes by it is unread, and an abstract's headline is not by itself a deliberate choice (MET-5). A relative error suits a target spanning four orders of magnitude (MET-11, context), so `mape`, or `rmse` on a log target with the transform declared (MET-3), is the call at /add-dataset; inputs none.
- Risks for /add-dataset: polymer and solvent descriptors from the SMILES of a repeat unit and of the solvent (CLEAN-24; check `mn` and `mw` for gaps); points within one isotherm make a random split an interpolation (SPLIT-3), so the 16,004 rows hold 107 polymers as units; systems measured by several papers may disagree (the abstract's ~20% irreducible error; check overlaps); `notes` is free text on the material grade.
- Priority: gap 0 (chemistry, regression and grouped are not thin), use case 0 (ours to state), source + (paper, a DOI per row, open file), shape + (16,004 points, polymer properties and conditions, grouped structure), risk - (107 polymers as the real units; descriptors to build).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 99: "blaiszik/awesome-matchem-datasets".
- as published: 'almost 15000 experimentally measured uptakes (0.01-50 wt%) of 79 gases in 102 different polymers', pressures 1e-3 to 7e2 bar, 233-508 K, almost 500 solvent-polymer systems from more than 250 ...; target: Uptake of the gas or vapour in the polymer at the given pressure and temperature (wt%, regression); access: open.
- Why: Real measurements compiled with a source DOI per row, open, with a stated prediction task; one of the awesome list's 'TODO' entries the first pass left for later.
- Adds: Polymer sorption, no record. Caveats: polymer and solvent appear as ids, so descriptors must be built (names and geometries are given, SMILES are not); rows are points on isotherms, dense within a system; the author estimates the irreducible error at about 20% MAPE. Low to medium priority.
