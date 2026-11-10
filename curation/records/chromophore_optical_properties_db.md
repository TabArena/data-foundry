---
unique_name: chromophore_optical_properties_db
name: Experimental database of optical properties of organic compounds (DB for chromophore)
checked_by:
- Myunghwan
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
original_source: Other
year: '2020'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.6084/m9.figshare.12045567.v3
- https://doi.org/10.1038/s41597-020-00634-8
- https://doi.org/10.6084/m9.figshare.12045567.v2
v2_path: datasets/_dev/tabarena-v0pt2/chromophore_optical_properties_db/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 20,236 experimental absorption and emission measurements of 7,016 organic chromophores in 365 solvents, compiled from 1,358 papers for machine learning, with a stated use: predict a new dye's optical properties before it is synthesized.
- Source: Joung, Han, Jeong, Park, "Experimental database of optical properties of organic compounds", Scientific Data 7:295 (2020) (https://doi.org/10.1038/s41597-020-00634-8, read on PMC7478979). The data is on figshare as "DB for chromophore" (https://doi.org/10.6084/m9.figshare.12045567; version 3 of 2024-10-21, CC BY 4.0), whose card says "total 20,247 combinations of chromophores and solvents ... 7,018 unique choromophores in 366 solvents or solid state", in one CSV of 3.2 MB. As published (Table 1): Tag, Chromophore (SMILES), Solvent (SMILES), Absorption max (nm), Emission max (nm), Lifetime (ns), Quantum yield, log(e), absorption and emission FWHM (cm-1, nm), Molecular weight, Reference (DOI); missing values are NaN. Collection: two people extracted the values from the published spectra separately, a third cross-checked them, and outliers were checked twice (Technical Validation).
- Use case: a chemist designing a dye, OLED emitter or imaging probe screens candidate structures before synthesis: "it would be useful to reliably and quickly predict the optical properties of newly designed organic chromophores prior to their synthesis" (Background & Summary). Fit direct for the absorption maximum from the two structures. Regime grouped by chromophore: a chromophore recurs across solvents, and a new design is a new structure (SPLIT-31, LEAK-17).
- Siblings and duplicates: `first_principles_absorption` (`No`, AHDS: 14 Beer-Lambert points of one molecule, no task); 'chromophore', 'absorption max' and 'Joung' matched no other record. External collections: not checked (web search budget used up).
- Better data: found next to `first_principles_absorption` (a related task, the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the data paper and figshare. The group's follow-up models (Joung et al., JACS Au 2021, "Deep learning optical spectroscopy based on experimental database") were not read.
- Metric: none found in the data paper (its Technical Validation checks the data and fits no model); the follow-up paper was not read. So the fallback `rmse` on the absorption maximum in nm (MET-5, MET-8), unless the follow-up names one deliberate metric. Inputs none.
- Risks for /add-dataset: one target to choose. The absorption maximum has the most values; emission maximum, bandwidths, extinction, quantum yield and lifetime are other targets read from the same spectra, so they cannot be features (LEAK), and `Multi-target` applies only if several ship. The SMILES-to-descriptor step is ours (CLEAN-24). Solid-state rows have a host instead of a solvent. A chromophore-solvent pair can come from several papers (duplicates). `Reference` and `Tag` are ids. Literature values carry lab-to-lab noise (USE-5).
- Priority: gap 0 (chemistry has 12 accepted; regression and grouped not thin), use case + (the paper names the design use), source + (peer-reviewed data paper, documented columns), shape + (20,236 rows in 7,016 chromophore groups), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `first_principles_absorption`.
- as published: 20,236 chromophore-solvent combinations (paper; figshare says 20,247), 7,016 unique organic chromophores in 365 solvents or solid state; one CSV (3.2 MB) with SMILES of chromophore and solvent and ...; target: first absorption maximum wavelength (nm); also emission maximum, bandwidths, extinction coefficient, quantum yield, fluorescence lifetime; access: open.
- Why: same domain as the record (light absorption of a molecule in solution): the record's 14 Beer-Lambert points of one molecule are a calibration curve with no prediction task, while this compiles experimental measurements from the literature with a target chemists act on; SMILES become descriptors with RDKit (apistox, ...
- Adds: thousands of real measured molecules instead of 14 points of one; CC BY 4.0. Notes: a chromophore recurs across solvents (grouped split by chromophore, LEAK-17); literature compilation, so measurement conditions vary

CC (2026-11-09, Myunghwan): Approved proceeding to add-dataset after clarifying first absorption maximum wavelength (nm) as the target, predicted from dye and solvent structures before measurement. Pursue the discussed scaffold-grouped evaluation. The explicit add-dataset invocation authorizes actual-data qualification and the required independent panel; final inclusion remains for review-added-datasets. No build, commit or publication authorized. Source access is currently paused; no data qualification result is implied.

**Assessment (AI, 2026-11-09):** review panel (full): retain first-absorption-peak regression with approximate fit, two typed SMILES inputs plus medium state, RMSE fallback and dye scaffold/identity grouping; disputed: same-response weighting (LEAK-18/19) and retention of differing responses (LEAK-20); for the curator: issues 1–2. Actual Figshare v3 has 20,836 rows / 17,703 absorption labels; the implemented policy yields 17,510 rows, 6,498 dyes and 3,335 groups. Native checks: 27, zero errors, one proposed gas/no-solvent warning; accepted warnings remain empty. All nine folds have no tested identity/tautomer overlap. Strict train-only exploratory LightGBM mean RMSE 56.655 nm (fold range 37.772–90.068); native mean baseline 106.481 nm. Signal varies across chemical families; overlapping repeated folds are not independent confidence estimates. Source access and earlier metric/identity findings are resolved; individual conflicting-label origins and downstream adapter enforcement remain unverified. Emission labels (18,851) outnumber absorption labels (17,703), correcting the historical completeness claim without reopening the approved absorption target. Priority 3: gap 0, use case 0 (approximate fit), source + (traceable primary experiment compilation), shape + (two typed molecular graphs, 17,510 rows / 3,335 groups; helper raw-field heuristic is 0), risk 0 (no established listed risk subtraction). Final inclusion, build and publication remain undecided.

CC (2026-11-10, Myunghwan): "1A, 2A, RMSE as declared, accept gas warning, ship". Scientifically accepted as implemented: keep one row per canonical dye/environment/wavelength (193 removals; 17,510 rows), recognizing only 50 also match every raw source field except Tag and the additional 143 are a weighting choice, not proven copied physical experiments. Retain the 61 input sets / 124 current rows with differing published wavelengths under the genuine-ambiguity clause, approximate fit and unverified individual causes. Keep 20 gas observations with meaningful absent solvent. This approval does not authorize build, commit, push or publication; preserve the active claim until normal integration.

CC (2026-11-10, Myunghwan): the declared metric rmse (fallback, untransformed nm) is checked and accepted as declared.

CC (2026-11-10, Myunghwan): accepted warning dataset_smiles_column for the 20 gas-state rows: no solvent molecule exists, so missing Solvent_SMILES plus known gas state is intentional.

**Assessment (AI, 2026-11-10):** applied ship and issues 1A/2A after independent decision-register/precedent review found zero conflicts; no exception or amendment required. The 193/50/143 distinction and unresolved causes remain explicit. Only curation comments and specific warning acceptance change in the definition; data, target, predictor contract, metric and grouping/fold logic are AST-identical. Preserve completed qualification and the full panel history. The same-fold SMILES comparison gives categorical RMSE 106.085 nm versus full structural encoding 56.655 nm (46.59% reduction, 9/9 wins); repeated folds are not independent trials. This is scientific acceptance, with build/integration separately requested.
