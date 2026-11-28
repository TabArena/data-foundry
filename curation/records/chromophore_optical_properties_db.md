---
unique_name: chromophore_optical_properties_db
name: Experimental database of optical properties of organic compounds (DB for chromophore)
checked_by:
- Myunghwan
- Andrej
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
- Expanding Science Catalogue
original_source: Other
year: '2020'
collection_period: 1967-2020
domain: chemistry & material science
required_split:
- Temporal (NON-IID)
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

**Assessment (AI, 2026-11-10):** on Myunghwan's explicit build-commit request after scientific acceptance, built the unchanged definition at clean commit 8a50be6ccb71d6b8fb77047ba7603028dd37e596. UUID 01a1c4ae-5ada-74a4-b90e-d5924662a442, checksum v2:97decdfc67653a344bdbc617300599730e279e24d81cdd2d821e68525f89ccb2, format2,17510rows/3335groups/9folds. Reload verification and reproduction from the single traced3213377-byte source CSV pass; actual frame and ordered splits equal the accepted qualification. Native0errors/0unacceptedwarnings; specific gas warning remains accepted. Full tests2017passed/286skipped, exact CI lint passes; broader legacy-notebook lint findings are pre-existing and outside this change. Raw inputs/containers stay local, active claim preserved; no push or publication.

**Assessment (AI, 2026-11-21):** collection facts set from the split audit: a literature compilation that keeps growing (Figshare v1-v3), each row dated through its paper's DOI; 17,510 rows of 6,498 dyes. The source papers' publication years span 1967-2020 (Crossref `issued` on 1,176 of 1,274 DOIs; 97.9% of shipped rows dated, measured 2026-11-21); v3's added rows are back-filled papers of 2020 and earlier.

**Assessment (AI, 2026-11-21):** review panel (full re-check): ship after changes; disputed: the ET(30) rows as measurements (PROV-1, EV-2; settled: measured peaks in another unit, the gas row extrapolated, CLEAN-1), one vote per dye (MET-17), scaffold groups against windows by first publication year (SPLIT-37, SPLIT-14; one-year windows from 2015 pass the floor); for the curator: issues 3-5 and the Horizon block. Priority 3: gap 0, use case 0 (approximate fit: literature selection and unrecorded conditions), source + (traceable compilation of 1,358 papers, CC BY 4.0), shape + (17,510 rows, 6,498 dyes, two typed structures), risk 0 (no demonstrated leak; leak probe to rerun).

CC (2026-11-24, Andrej): issue 3 B, "Option B: Windows by first publication year." Each dye is dated by the earliest Crossref year of its papers (no-stereo key, aliases joined) and all its rows go with that year; the scaffold grouping is removed; `split_leaf = "L-CAT.entry-date"`.

CC (2026-11-24, Andrej): the declared horizon (one publication year, no gap, windows starting 2020, 2019, 2018, 2017, 2016 and 2015) is checked, "Option B: Six one-year windows, 2015-2020.": one year is the finest step the date gives and the use case sets no other, and the six are all the windows that train on at least half the rows; `splits_below_target` (6 against 9) accepted with that reason.

CC (2026-11-24, Andrej): issue 5 B, "Option B: Drop the row." The betaine dye's gas row (1,055 nm, the ET(30) scale's extrapolated gas value) leaves; 19 gas rows remain.

**Assessment (AI, 2026-11-24):** applied 3 B, H B and 5 B. Crossref years pinned in `raw/crossref_years.csv` (written by the recipe in `download_description`, SHA256-checked in `_load_raw`; 1,354 References, 1,240 dated; identical to the 2026-11-21 table except 4 References Crossref did not answer then). 17,509 rows, 6,498 dyes; 131 dyes (194 rows, 1.1%) undated, dated 1967 so they always train. Windows (test year: rows, dyes, train share): 2020: 297, 97, 98.3%; 2019: 2,040, 784, 86.7%; 2018: 1,959, 709, 75.5%; 2017: 1,443, 535, 67.2%; 2016: 1,611, 437, 58.0%; 2015: 1,215, 423, 51.1% (50.5% without the undated rows); 2014 would train on 44.4%. Check: 0 errors; warnings `splits_below_target` (accepted) and `dataset_smiles_column` (accepted, 19 rows). Task probe on the windows: LightGBM RMSE 46.5 nm against 97.2 for the dummy, beats it on every split, no flags (5 of 6 splits). Leak probe: exact feature copies 0.0% over 8,565 test rows, best single feature 0.40 against 0.73 for all features; its nearest-neighbour step crashes on a non-finite encoding (a probe defect); run with an inf-safe neighbour space it gives 1-NN R² 0.255 on all test rows and -1.54 on the closest tenth, far below the model, so no near-copy shortcut. The period readout shows the 90th wavelength percentile rising in the newest years (drift toward red and NIR dyes), not a fall at the end, so no sign of a cut.

CC (2026-11-24, Andrej): review issue 4, as implemented (A): the score stays per row, with a note on how unequal the dyes are per window.

CC (2026-11-24, Andrej): the declared split (six one-year windows 2015-2020 on each dye's first publication year, no gap, leaf L-CAT.entry-date) is checked, as implemented.

CC (2026-11-24, Andrej): verdict ship; nothing open in the review. The build is stale until rebuilt.

## Review

**Outcome:** added. Ship after changes (full re-check, 2026-11-21; marks of 2026-11-24 applied). Validity: a real screen of dyes before synthesis; dyes reach the literature in series of papers, so the split now follows each dye's first publication year (issue 3 B) in six one-year windows 2015-2020 that each train on at least half the rows (Horizon B); the extrapolated gas row of the betaine dye is dropped (issue 5 B); the 334 solvent rows of the betaine dye are measured peaks converted from the ET(30) scale. Value: on the windows LightGBM scores RMSE 46.5 nm against 97.2 nm for the dummy (task probe, 2026-11-24). The score stays per row, with a note on how unequally the dyes weigh per window (issue 4 A). Nothing open.

**Main points:** No open decision. Not a decision: the build is stale after this round's changes.



**Record judgment:** Priority 3: strong primary source and substantial grouped structural variation; no coverage-gap point, and approximate fit withholds the direct-fit use-case point. The shape helper reports zero from three raw fields, but two typed molecular graphs encode to 2,815 fixed coordinates for 17,510 measurements and 3,335 groups. These coordinates are encodings, not independently measured raw variables. No demonstrated leak, unclear target quantity, heavy join or irreversible damage establishes a known-risk subtraction.

**Horizon:**

* **Verdict:** one-year windows with no gap, 2015 to 2020 (medium confidence); asked only if issue 3 goes to windows.
* **Length:** one publication year: the date gives whole years only, the use case sets no refit cadence, and one year is the finest step (as qsar_tid_11); neither the source nor the use case gives a length, so this is the curator's sign-off. 2020 holds only 297 rows (97 dyes), above the minimum of 33 scored units of a test window, so it stays a window of its own; the scored unit is the row, because the RMSE has no group input and no window cuts a dye.
* **Gap:** none: the label is final when the paper appears and the catalogue has no outcome delay.
* **Time frame:** the source papers' Crossref years span 1967-2020 (97.9% of shipped rows dated); the dating is ours, from the DOI each raw row carries; v3's added rows are back-filled papers of 2020 and earlier. The 1.9% of rows of undated dyes (339 rows, 156 dyes) train in every window; dropped instead, the 2015 cut would train on 50.0% of the remaining rows. Per one-year window, untuned LightGBM, RMSE in nm (lower is better):

  | Test year | Train share | Test rows | Test dyes | Test scaffold groups | Close analogue, forward | Close analogue, random draw | RMSE per row | RMSE, each dye once | Train-mean RMSE |
  |---|---|---|---|---|---|---|---|---|---|
  | 2012 | 33.8% | 1,081 | 326 | 176 | 2.1% | 58.6% | 51.5 | 58.4 | 96.4 |
  | 2013 | 40.0% | 784 | 381 | 207 | 3.1% | 59.0% | 68.7 | 70.6 | 108.0 |
  | 2014 | 44.5% | 1,144 | 596 | 379 | 5.9% | 58.9% | 64.8 | 72.8 | 124.6 |
  | 2015 | 51.0% | 1,204 | 421 | 229 | 4.8% | 60.4% | 64.3 | 68.0 | 95.9 |
  | 2016 | 57.9% | 1,640 | 441 | 266 | 7.9% | 59.3% | 45.1 | 49.4 | 102.1 |
  | 2017 | 67.2% | 1,422 | 531 | 319 | 8.9% | 58.3% | 47.9 | 55.7 | 100.1 |
  | 2018 | 75.4% | 1,979 | 711 | 437 | 8.9% | 62.1% | 53.7 | 61.3 | 83.3 |
  | 2019 | 86.7% | 2,040 | 784 | 420 | 8.8% | 63.1% | 52.6 | 55.8 | 99.8 |
  | 2020 | 98.3% | 297 | 97 | 39 | 8.2% | 61.9% | 51.6 | 48.4 | 104.3 |

* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Scaffold folds (implemented) | The scaffold folds of issue 3; no horizon; RMSE 55.9 per row, 50.7 each dye once | 9 scaffold folds of 5,450-6,164 rows | nothing to change | applies only if issue 3 keeps scaffold groups |
  | B | Six one-year windows, 2015-2020 | Each publication year 2015 to 2020 tested on all earlier years; train shares 51.0% to 98.3%; forward analogue 4.8-8.9% against 58.3-63.1% random; mean RMSE 52.5 per row, 56.4 each dye once | 6: 421, 441, 531, 711, 784 and 97 dyes (1,204, 1,640, 1,422, 1,979, 2,040 and 297 rows; 39-437 scaffold groups) | every window one year, as the use case and qsar_tid_11; as many windows as pass the half-the-rows floor; the newest is 2020 | 2015 is 1 point above the floor (the undated dyes train in every window); 2020 is small (297 rows, 97 dyes, against the minimum of 33 scored units) |
  | C | Five one-year windows, 2016-2020 | As B without 2015; train shares 57.9% to 98.3%; forward analogue 7.9-8.9% against 58.3-63.1%; mean RMSE 50.2 per row, 54.1 each dye once | 5: 441, 531, 711, 784 and 97 dyes (1,640, 1,422, 1,979, 2,040 and 297 rows) | above the floor with room to spare, even without the undated rows | one window fewer than the floor allows |
  | D | Nine one-year windows, 2012-2020 | As B, with 2012, 2013 and 2014 under the floor (33.8%, 40.0%, 44.5% train share); forward analogue 2.1-8.9% against 58.3-63.1%; mean RMSE 55.6 per row, 60.0 each dye once | 9: 326, 381, 596 dyes and B's six (1,081, 784, 1,144 rows and B's) | reaches the target of 9 | three windows need the curator's exception down to 30%; the earliest windows are the hardest (RMSE 52-69) |
  | E | Three windows, the newest three years joined | Test 2016, 2017, 2018-2020; train shares 57.9%, 67.2%, 75.4%; forward analogue 7.9-8.9% against 58.3-59.3%; mean RMSE 48.8 per row, 54.3 each dye once | 3: 441, 531 and 1,592 dyes (1,640, 1,422 and 4,316 rows) | the first layout measured in issue 3 | a three-year newest window that nothing in the use case asks for; half the windows the floor allows, where the rule asks for as many as reach the target; the split API cannot declare it (a split-only year column or custom splits, with a horizon wrong for the newest window) |

* **Recommendation:** B: one publication year is the finest step and the use case sets no other; six windows are all that pass the half-the-rows floor, and the undated dyes train in every window, so 2015's 51.0% is its real train share; the splits comment names the target of 9, the 6 reached and what stops more (2014 trains on 44.5%); overlapping windows cannot add one, since a window's training side is set by its first test year and only six years pass the floor[^x21ch1]. **Decision:** six one-year windows (B), five (C), nine with the exception (D), the joined layout (E), or none because issue 3 keeps scaffold groups (A)?

**Notes for the AI:** apply only together with issue 3 (b); the declaration is in issue 3's notes, with `cutoffs` the chosen years (B: 2020 back to 2015) and `split_leaf = "L-CAT.entry-date"`; the splits comment names the leaf and that the curator signed off the one-year length; accept `splits_below_target` with the splits comment's reason. The window checks count rows (no `group` input in the metric, also under issue 4 B, whose weight is no group), so the target stays 9 (two thirds of 17,510 rows: 3 repeats of 3 folds). On D, the three windows under the floor need the curator's CC line and the accepted `splits_train_under_half` warning. On E: `TemporalSplits` cannot declare it (one `window` serves every cutoff, a 2018 one-year window fails the newest-window check, and `window=None` runs every window to 2020); it needs a split-only year column with 2019-2020 folded into 2018, or `_make_splits`, and the splits comment says the declared horizon is one year while the newest window spans three.

[^x21ch1]: **SPLIT-15** (Must for the newest window, Should for the others): the newest window is the deployment period; the number of windows aims at SPLIT-33's count for two thirds of the scored units (9 for 17,510 rows), never fewer than 3; the window length follows the use case and is never shortened to reach the count; within the floor and the least test window, as many windows as reach it; fewer are accepted with the target, the count and the reason in the splits comment; overlapping windows are offered only where they could reach the target. Precedent: qsar_tid_11, nine one-year windows in place of two-year ones (Andrej, 2026-11-19: "nothing in the use case asks for them"). **SPLIT-14** (Must): each window trains on at least half the data (down to 30% as the curator's exception) and tests at least 33 scored units, counted as SPLIT-33 counts them (a temporal split has no group: the metric's group input, else the row). **SPLIT-36** (Should): a test window length the source does not give is a person's sign-off; the definition names its leaf in `split_leaf`.

**Andrej (2026-11-24, change):** Option B: Six one-year windows, 2015-2020.

**Resolved (2026-11-24, Andrej):** B. `TemporalSplits(window=1, unit="unique", cutoffs=(2020, 2019, 2018, 2017, 2016, 2015))`, horizon one year, no gap. Measured on the shipped frame (17,509 rows; dating as in issue 3's Resolved line):

| Test year | Train share | Train rows | Test rows | Test dyes |
|---|---|---|---|---|
| 2020 | 98.3% | 17,212 | 297 | 97 |
| 2019 | 86.7% | 15,172 | 2,040 | 784 |
| 2018 | 75.5% | 13,213 | 1,959 | 709 |
| 2017 | 67.2% | 11,770 | 1,443 | 535 |
| 2016 | 58.0% | 10,159 | 1,611 | 437 |
| 2015 | 51.1% | 8,944 | 1,215 | 423 |

2015 trains on 50.5% without the undated rows; 2014 would train on 44.4%. The splits comment names the target (9 for 17,509 rows), the 6 reached and the floor that stops more, and `splits_below_target` is accepted with it.

**Issues for Myunghwan:**

1. **How should repeated records with the same inputs and wavelength be weighted?**

   - **Problem:** The implemented policy removes 193 records with identical dye structure, medium structure/state and measured wavelength, while only 50 excess labeled rows also match every raw field except the row number.
   - **Background:** The additional 143 removals differ in reference or other recorded optical outcomes, which establishes differing records but does not establish independent experiments or copied experiments.
   - **Effect on the task:** Keeping one record per input/target combination gives 17,510 rows; removing only full-source-record repeats gives 17,653 and increases the weight of some identical responses.
   - **Experiments:** Source, critic and mediator counts agree on the policy matrix; all qualification results use the implemented 17,510-row variant, so changing the policy requires affected qualification to be rerun.
   - **Consistency:** Equal-response deduplication follows the default for copies, while natural repeated continuous measurements have retention precedents; exact molecular graphs supply substantial information but do not identify a physical experiment.[^weighting]
   - **Panel:** The advocate supports the implemented weighting; the critic and mediator agree this is a curator choice rather than a demonstrated validity failure.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | One record per input and wavelength (implemented) | Remove 193 repeats; retain 17,510 rows | Limits repeated identical responses; current package is qualified | Removes 143 records beyond established full-record equality |
     | b | Preserve source-record multiplicity | Remove only 50 full-record repeats; retain 17,653 rows | Preserves records with differing provenance or other outcomes | Their independence is unverified; repeated responses receive more weight; requalification needed |

   - **Recommendation:** (a), explicitly as a weighting policy rather than a claim that 193 physical experiments were copied. **Decision:** Keep the implemented equal-response policy, or preserve the additional source records?

   **Notes for the AI:** Save Myunghwan's actual choice before application. Option b changes `_clean` to deduplicate labeled raw rows on all source fields except Tag before dropping nonpredictors, then canonicalizes inputs and retains the same label-free identity grouping. Recompute folds, native checks, affected probes and independent rechecks; do not transplant current fitted scores to the new row weights. Preserve the original results.

   **Myunghwan (2026-11-10, as implemented):** 1A.

   **Resolved (2026-11-10, Myunghwan):** A. Keep one row per canonical dye/environment/wavelength, removing 193 repeated input/target records and retaining 17,510 rows. Only 50 also match all raw fields except Tag; the additional 143 removals are an accepted weighting policy, not proof of copied physical experiments.

   [^weighting]: **LEAK-16 (Must)** requires an explicit duplicate decision. **LEAK-18 (Should)** distinguishes plausible natural repeats from collection copies; **LEAK-19 (Should)** defaults to removing same-label copies. These policy defaults do not prove the physical identity of each observation. The continuous-measurement superconductivity precedent retains repeated compositions under unrecorded conditions. The raw release is [Figshare v3](https://doi.org/10.6084/m9.figshare.12045567.v3).

2. **Keep differing published wavelengths for the same dye and environment?**

   - **Problem:** With the implemented weighting, 61 input sets contain 124 records with different target values, spanning 0.5–100 nm within a set.
   - **Background:** Unrecorded conditions, peak assignment and transcription are possible causes; the cause of each disagreement is not established.
   - **Effect on the task:** Retention predicts the observed variation under incomplete conditions, while removal excludes these input sets and changes the evaluation population.
   - **Experiments:** The median within-set range is 3.5 nm, 22 sets exceed 10 nm and eight exceed 30 nm; a targeted primary-source check confirms the 2012 PRODAN/chlorobenzene value of 354 nm, but does not resolve the competing 254 nm record attributed to an older paper.[^origins]
   - **Consistency:** Heterogeneous continuous measurements support the genuine-ambiguity retention precedent; source-backed errors should be repaired rather than averaged or selected by model agreement.[^conflicts]
   - **Panel:** Source, domain, blind and debate reports preserve the uncertainty; the mediator recommends retention for Myunghwan's explicit judgement.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Retain distinct reported values (implemented) | Keep the 61 sets with their observed responses | Preserves the published observations; no speculative repair | Some differences may be transcription or peak-selection errors |
     | b | Exclude all conflicting input sets | Under issue 1a remove 124 rows, leaving 17,386; under issue 1b remove 126, leaving 17,527 | Produces one response per retained input set | Conditions selection on observed disagreement; can discard valid measurements; requalification needed |
     | c | Pause inclusion for further origin checks | Leave the current package preserved while original spectra are investigated | Can support specific repairs | Does not resolve anything until new source evidence is obtained |

   - **Recommendation:** (a), retaining approximate fit and explicit uncertainty; grouping prevents identity shortcuts but does not validate the response values. **Decision:** Retain the differing measurements, exclude those input sets, or defer inclusion for further origin investigation?

   **Notes for the AI:** The questions are independent; record both choices. Counts must follow issue 1's selected weighting. For option b, remove every member of an input set with more than one distinct absorption value, not just extreme responses, and rerun the affected qualification. For option c, preserve the package and name the unresolved source-access/evidence action. Apply the genuine-ambiguity clause if that is Myunghwan's judgement; do not invent an exception or a general rule amendment. A confirmed source error is repaired from that source.

   **Myunghwan (2026-11-10, as implemented):** 2A.

   **Resolved (2026-11-10, Myunghwan):** A. Retain the 61 input sets / 124 current rows with differing published responses under the genuine-ambiguity clause for continuous measurements with incomplete conditions. Preserve approximate fit and unverified individual causes; repair any later source-proven error from its origin. Grouping does not validate labels.

   [^conflicts]: LEAK-20 is a Should default with a genuine-label-ambiguity clause. USE-8 requires the known gap to remain in approximate fit. PROV-13 requires origin-supported repair when damage is demonstrated; EV-2/6 distinguish measured disagreement from its inferred cause. The source descriptor is [Joung et al. 2020](https://doi.org/10.1038/s41597-020-00634-8).
   [^origins]: [Lopez and Abelt 2012, Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC3384555/) reports the 354 nm PRODAN value in chlorobenzene. The older [Weber and Farris paper](https://doi.org/10.1021/bi00581a025) was traced but its quantitative origin was inaccessible in the targeted check. One confirmed later value does not justify replacing the earlier release value by consensus.

3. **Hold out dyes by scaffold, or by the year they were first published?**

   - **Problem:**
     - The source aims at "newly designed organic chromophores prior to their synthesis", so the split depends on whether a forward split by publication year leaves clearly fewer close training analogues than a random draw.
     - Every raw row carries the DOI of its paper, so each dye can be dated by its first report, but this was never measured.
     - If papers report dyes in series, the scaffold split still trains on siblings published in the same paper as a test dye, which a chemist designing the next series does not have.
   - **Background:** the catalogue grows (Figshare v1, v2 with 20,236 rows, v3 of 2024 with 20,836 rows); the paper's "will be updated regularly" refers to the database of its search webpage, so the growth rests on the Figshare versions. The earlier panel set time aside without measuring it ("no defensible chronological deployment axis"), and Myunghwan chose the scaffold split on 2026-11-09 ("Pursue the discussed scaffold-grouped evaluation"); the rule that weighs the entry date against the family key came after that call, as for qsar_tid_11, whose scaffold split (2026-11-01) became windows on 2026-11-11.
   - **Effect on the task:** under scaffold groups the test stands for new scaffolds drawn from the whole span of the literature; under a year split it stands for the dyes the literature reports next, each dye's later solvents kept with its first year.
   - **Experiments:** none on time yet. Measured so far, on distinct test dyes (Morgan radius 2, Tanimoto at least 0.7):

     | Split | Test dyes with a close training analogue |
     |---|---|
     | Scaffold groups (implemented, 9 folds) | 31.4% (29.7-33.0%) |
     | Random rows | 82.2% (81.5-83.0%) |
     | Forward by first publication year | not measured |
     | Random draw of dyes, same test size | not measured |

   - **Consistency:** qsar_tid_11 and apistox ship windows on the entry date, because their date carried waves; superconductivity and the qsar sets kept the family key, where the source limited itself to known chemistry or the forward split was no stricter than a random draw[^x21c1].
   - **Panel:** the split auditor (2026-11-21) found the tree's leaf undetermined and asks for the measurement before a choice.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scaffold groups, tagged as unseen groups (implemented) | Keep the 9 scaffold folds; declare the time basis `UnseenGroup`, whose reason gives the forward split's analogue share against a random draw's | no new folds; the catalogue's default | trains on same-paper siblings of the test dyes if the literature comes in series |
     | B | Windows by first publication year | Date each dye by the earliest Crossref year of its DOIs; test each later era on the earlier ones; all rows of a dye with its first year; no gap | matches the source's aim of predicting before synthesis, if the waves are real | needs Crossref lookups of about 1,300 DOIs; windows must meet the floor; requalification and a horizon sign-off |

   - **Recommendation:** measure first: if the forward split's analogue share is clearly below a random draw of dyes of the same size and the years give at least three windows, B; otherwise A, with the measured shares in its time basis. **Decision:** after the measurement, keep scaffold groups (A) or split by first publication year (B)?

   **Notes for the AI:** The measurement, on the raw v3 CSV with the shipped `_clean` frame: map the raw `Reference` to each kept row before `drop_duplicates` and keep the earliest year per dye (no-stereo key), the year from Crossref `https://api.crossref.org/works/<doi>` (`issued`); report DOI coverage and the year histogram (rows and distinct dyes per year); on distinct dyes, take expanding windows by first year with test sizes of about a third of the dyes, and give the share of test dyes with Tanimoto at least 0.7 to a training dye against a random dye-level draw of the same size, and the scaffold split on the same test dyes (SPLIT-37: compare with random, never with the family key); per era, the share of `neat solid` / `gas` rows, the heavy-atom count and the median wavelength; results in a table in the answer. If A: `time_basis = TimeBasis("UnseenGroup", ...)` whose reason names the source's aim and the measured shares, ending with what the split cannot test (the next papers' series, new solvents). If B: `Temporal` on a first-year column that is no input (as apistox and qsar_tid_11), record facts `Samples: Over Time`, `Time: Dated`, and a Horizon block. Sources: Joung et al. 2020, Scientific Data 7:295, https://doi.org/10.1038/s41597-020-00634-8; Figshare v3, https://doi.org/10.6084/m9.figshare.12045567.v3.

   Time basis, both versions (not set yet; it follows this decision):
   - If A (scaffold groups, a departure from the split tree's leaf `L-CAT.entry-date`): `time_basis = TimeBasis("UnseenGroup", "the source aims at newly designed chromophores before synthesis, and each dye can be dated by its first paper (Crossref year; 97.9% of rows), but the curator keeps dye scaffold groups: <the curator's reason>. A forward split by first year leaves 2.1-8.9% of test dyes with a close training analogue against 58-63% for a random draw of the same size; the scaffold folds leave 31.4%, and 58-65% of their test rows have a row of their own paper in training. Not tested: the series the next papers report, new solvents.", set_by="<the curator>", on="<date>")` (the build adds the tag and renders the `- Time basis:` bullet; never a tag in `data_tags` or a hand-written line); the splits comment names the leaf, that the definition departs from it and why; `split_leaf = "L-CAT.entry-date"` only once a reviewer has added the departure to the table at the end of the split tree (the tests fail before); the record keeps `Samples: Over Time` and `Time: Dated`.
   - If B (windows, the leaf `L-CAT.entry-date`): add a `first_year` column (earliest Crossref `issued` year over the DOIs of the dye's rows, no-stereo key; undated dyes take the earliest year so they always train), sort the frame by it and reset to a RangeIndex; `temporal = Temporal(on="first_year", splits=TemporalSplits(window=1, unit="unique", cutoffs=(2020, 2019, 2018, 2017, 2016, 2015)), horizon=1, horizon_unit="years", time_of="label")` (`horizon` is required with `unit="unique"`; `first_year` is no model input, as in qsar_tid_11), with the `cutoffs` the test years the Horizon decision gives (the tuple above is its recommendation). Drop the `scaffold` grouping and its `Grouping`; `split_leaf = "L-CAT.entry-date"`; the splits comment gives each window's test dyes, rows and train share, names the SPLIT-33 target (9 splits for 17,510 rows), the count reached and what stops more (the first year under the half-the-rows floor), and accepts `splits_below_target` with it; no `time_basis` (a temporal split refuses one); record `required_split` becomes temporal, the tags `Samples: Over Time`, `Time: Dated` stay; the Horizon block below gets its turn. Rerun the native checks, the task, group and leak probes (the leak probe after its nearest-neighbour step is fixed), and requalify.

   **Answer (AI, 2026-11-21):** the measurement is done; the date carries the waves.
   - Every dye dated by the earliest Crossref year of its papers (97.6% of dyes dated); a test dye has an analogue if it reaches Morgan radius 2 Tanimoto at least 0.7 to a training dye.

     | Split | Test dyes | Test dyes with a close training analogue |
     |---|---|---|
     | Scaffold groups (implemented, 9 folds) | about a third of the groups | 31.4% (29.7-33.0%) |
     | Random rows | | 82.2% |
     | Forward, first year 2014 or later | 3,581 | 3.9% |
     | Random draw of dyes, same size | 3,581 | 43.9% |
     | Forward, first year 2017 or later | 2,123 | 7.1% |
     | Random draw of dyes, same size | 2,123 | 56.1% |
     | Scaffold groups, the same test dyes as forward 2014 | 3,581 | 1.9% |

   - Under the scaffold folds, 58.4-64.8% of test rows have a row of their own paper in training (68-77% of test papers).
   - Drift by era of first publication:

     | Era of first publication | Median wavelength (nm) | Median heavy atoms | Neat-solid rows | Gas rows |
     |---|---|---|---|---|
     | up to 2005 | 404 | 26 | 0.15% | present (papers of 1967-2006) |
     | 2006-2013 | 393 | 28 | 1.6% | present up to 2006 |
     | 2014-2020 | 400 | 31 | 3.0% | none |

   - The windows are tight: rows dated before 2014 are 42.6% of the dated rows, under the half-the-rows floor[^x21c2]; cuts at 2016 and 2017 pass it, and the years after 2019 hold only 97 dyes, so three windows need a layout checked against the floor and the least test window.
   - 2.1% of rows (98 DOIs) have no year: they would be dropped or put into the earliest training era.
   - **Recommendation:** B, on condition that a layout of three windows passes the floor and the least test window; otherwise A with these shares in its time basis. **Decision:** split by first publication year (B), or keep scaffold groups (A)?

   [^x21c2]: **SPLIT-14** (Must): every window trains on at least half the rows (down to 30% as the curator's exception) and tests at least 33 scored units.
   [^x21c1]: **SPLIT-36** (Should): walk the tree from the record's collection type; the definition names the leaf it reaches in `split_leaf`; a definition that ships another split names the leaf and the reason in its splits comment, and a reviewer confirms the departure; a question no answer fits goes to a reviewer. **SPLIT-37** (Should): the entry date replaces the family key when the use case predicts for items the catalogue does not hold yet, the date is the item's entry, the labels are final, and a forward split leaves clearly fewer close neighbours than a random draw, if the windows meet SPLIT-14 and SPLIT-15; the scaffold key is the default otherwise; the source's stated aim decides which items the test stands for. **SPLIT-31** (Should): molecules group on the Bemis-Murcko scaffold. **SPLIT-32** (Should): a grouped split carries a time basis, declared as `TimeBasis(tag, reason)`, which the build renders as the `- Time basis:` bullet.

   **Answer (AI, 2026-11-21):** Windows of first-publication years pass the training floor without an exception: split by first publication year?
   - **Problem:**
     - The first answer's condition is now measured: one-year test windows from 2015 to 2020 all train on at least half the rows without the curator's exception, and the smallest test window (2020) holds 39 scaffold groups against the minimum of 33.
     - On every window the forward split leaves far fewer close training analogues than a random draw of the same number of dyes, and far fewer test rows whose own paper is in training than the scaffold folds.
   - **Background:** every dye takes the earliest Crossref year of its papers (no-stereo key), all its rows go with that year, and the 1.9% of rows of undated dyes (339 rows, 156 dyes) go into training in every window; train share is training rows over all 17,510 rows; analogue as in the first answer; the random draw takes the same number of test dyes from the window's training and test dyes, 3 seeds; two CPU jobs of the mediator, 2026-11-21. The first answer's "the windows are tight" counted the 2014 cut (44.5%); the cuts from 2015 on pass the floor.

     | Test year | Train share | Test rows | Test dyes | Test scaffold groups | Close analogue, forward | Close analogue, random draw | Test rows with their own paper in training |
     |---|---|---|---|---|---|---|---|
     | 2012 | 33.8% | 1,081 | 326 | 176 | 2.1% | 58.6% | 9.1% |
     | 2013 | 40.0% | 784 | 381 | 207 | 3.1% | 59.0% | 8.3% |
     | 2014 | 44.5% | 1,144 | 596 | 379 | 5.9% | 58.9% | 23.8% |
     | 2015 | 51.0% | 1,204 | 421 | 229 | 4.8% | 60.4% | 6.1% |
     | 2016 | 57.9% | 1,640 | 441 | 266 | 7.9% | 59.3% | 1.6% |
     | 2017 | 67.2% | 1,422 | 531 | 319 | 8.9% | 58.3% | 7.1% |
     | 2018 | 75.4% | 1,979 | 711 | 437 | 8.9% | 62.1% | 10.8% |
     | 2019 | 86.7% | 2,040 | 784 | 420 | 8.8% | 63.1% | 10.0% |
     | 2020 | 98.3% | 297 | 97 | 39 | 8.2% | 61.9% | 0.0% |
     | Scaffold folds (implemented) | about 67% | 5,450-6,164 | - | - | 31.4% | - | 58.4-64.8% |

   - **Effect on the task:** the task stays learnable forward; untuned LightGBM (Morgan count fingerprints of radius 2 with 2,048 bits, solvent with 256 bits, medium one-hot, defaults), RMSE in nm, lower is better, mean and range over the splits:

     | Split | RMSE per row | RMSE without the betaine dye | RMSE, each dye once | Train-mean RMSE |
     |---|---|---|---|---|
     | Scaffold folds (implemented), 9 | 55.9 (39.7-79.1) | 46.5 (39.7-49.2) | 50.7 (44.4-58.0) | 95-124 |
     | One-year windows 2015-2020, 6 | 52.5 (45.1-64.3) | the same (the dye always trains) | 56.4 (48.4-68.0) | 83-104 |
     | One-year windows 2016-2020, 5 | 50.2 (45.1-53.7) | the same | 54.1 (48.4-61.3) | 83-104 |

     Under the windows Reichardt's betaine dye (first paper 1994) always trains, so the three scaffold folds where this one dye doubles the error (RMSE 72-79 against 40-49 nm) have no counterpart. The per-window scores are in the Horizon block.
   - **Consistency:** qsar_tid_11 (6-30% forward against 79.7% random, moved off scaffold groups on 2026-11-11) and apistox ship windows on the entry date; the gap here is wider than both. The sets that kept scaffolds had a forward split no stricter than a random draw, or a source limited to known chemistry; neither holds here. Myunghwan's scaffold choice of 2026-11-09 came before the rule that weighs the entry date against the family key; the split tree now reaches the entry-date leaf here, so keeping scaffolds is a departure that names the fact that sets this dataset apart and goes to a reviewer[^x21c3].
   - **Limits:** the year is the literature entry, not the catalogue entry (accepted for apistox and qsar_tid_11); the windows sit in 2015-2020; the domain practitioner calls a forward split the strict end of lead optimisation; undated dyes always train.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Scaffold groups (implemented) | Keep the 9 scaffold folds with the `UnseenGroup` time basis (a `TimeBasis` naming the curator and the reason) | no new folds; Myunghwan's choice of 2026-11-09 | trains on same-paper siblings for 58-65% of test rows; departs from the split tree's leaf, so a reviewer must confirm it and it is listed among the tree's departures |
     | b | Windows by first publication year | Temporal split on each dye's first year; which test years is the Horizon decision | the leaf the split tree reaches; the test stands for the dyes the literature reports next; windows pass the half-the-rows floor without an exception | requalification and the Horizon sign-off |

   - **Recommendation:** b: on every window measured the forward split leaves 2-9% of test dyes a close training analogue against about 60% for a random draw, and the windows pass the half-the-rows floor, which is what the rule on growing catalogues asks before the year replaces the scaffold[^x21c3]. **Decision:** split by first publication year (b), or keep scaffold groups as an exception (a)?

   [^x21c3]: **SPLIT-37** (Should): for an expanding catalogue the entry date replaces the family key when the use case predicts for items not yet held, the date is the item's entry and the labels are final, and a forward split leaves clearly fewer close neighbours than a random draw, if the windows meet SPLIT-14 and SPLIT-15. **SPLIT-36** (Should): the split tree's walk from "Expanding Science Catalogue": CAT.next-items yes (the source aims at "newly designed organic chromophores prior to their synthesis"), CAT.entry-date yes (each dye's first paper year, as for apistox and qsar_tid_11; labels not revised), CAT.arrival yes (forward 2.1-8.9% against 58-63% random), CAT.windows yes (six one-year windows pass the floor; the one-year length is the curator's sign-off in the Horizon block), leaf L-CAT.entry-date; a definition that ships another split names the leaf and its reason, and a reviewer confirms the departure. **SPLIT-14** (Must): at least 3 windows, each training on at least half the data (down to 30% as the curator's exception), each testing at least 33 scored units. Precedents: qsar_tid_11 (Andrej, 2026-11-11), apistox.

   **Andrej (2026-11-24, change):** Option B: Windows by first publication year.

   **Resolved (2026-11-24, Andrej):** B, with the Horizon's six one-year windows. `dataset.py`: each dye (no-stereo key, InChIKey and tautomer aliases joined) takes the earliest Crossref year over the papers of all its labeled rows, deduplicated ones included, as `first_year` (`time_of="label"`, no input); the 131 undated dyes (194 rows) take 1967 and always train; `temporal` on it with cutoffs 2020 back to 2015; the scaffold computation, the `scaffold` column and the `Grouping` removed; `split_leaf = "L-CAT.entry-date"`; the Crossref years are pinned in `raw/crossref_years.csv`, written once by the recipe in `download_description` and SHA256-checked in `_load_raw` (the build never calls Crossref; equal to the 2026-11-21 table but for 4 References Crossref did not answer then). Task summary, curation bullets (dating, aliases, charge forms), split walk ("the split the definition ships") and splits comment rewritten. Record: `required_split` Temporal (NON-IID), tag Non-IID (Temporal); CC lines in the comments. Check: 0 errors; `splits_below_target` (6 against 9) follows from the chosen windows and is accepted with its reason (the curator's acceptance given by the Horizon mark). Task probe on the windows: LightGBM RMSE 46.5 nm against 97.2 for the dummy, beats it on every split, no flags.

4. **Score each dye once?**

   - **Problem:**
     - A chemist decides once per proposed dye, but dyes have unequal numbers of rows: the median dye has 1 row, 287 dyes have 10 or more (23% of the rows), and Reichardt's betaine dye has 335.
     - The solvent series are a solvatochromism protocol of the source papers, and the solvent moves the peak little next to the dye (SD 19.9 nm within a dye against 108.7 nm between dyes).
     - Scored per row, the series of a few dyes weigh in the score as many decisions.
   - **Background:** one weight of 1 over the dye's rows covers every multi-row dye at once: all 2,609 of them, the betaine dye, the 287 series of 10 rows or more and the 61 sets with differing wavelengths (each inside one dye); it is one rule, not a list of dyes.
   - **Effect on the task:** under the scaffold folds the betaine dye gives 57-68% of the squared error in 3 of 9 folds, and the weight removes that; under windows the dye always trains, so the case rests on the other multi-row dyes. Untuned LightGBM, RMSE in nm (lower is better):

     | Split | RMSE per row | RMSE, each dye once |
     |---|---|---|
     | Scaffold fold 1 (holds the betaine dye) | 79.1 | 51.1 |
     | Scaffold folds, mean of 9 | 55.9 | 50.7 |
     | One-year windows 2015-2020, mean of 6 | 52.5 | 56.4 |
     | One-year windows 2016-2020, mean of 5 | 50.2 | 54.1 |

   - **Experiments:** the domain practitioner ranked 4 models both ways on the 9 scaffold folds: Kendall tau 0.93 on average and 0.67 at the lowest, inside the range seen on the earlier cases of this rule. The ranking shift on the windows of issue 3 is not measured; there, one vote per dye scores 3-8 nm above per row on the windows 2015-2019 and 3 nm below on 2020.
   - **Consistency:** superconductivity (one vote per composition, 2026-11-08), dementia_prediction and pancreatic_cancer_mouse_detection (one vote per person or mouse) weigh each unit once; asp_potassco and video_transcoding stay per row because each row is a decision of its own, which the practitioner says is not so here[^x21c4].
   - **Panel:** the advocate, the critic and the domain practitioner prefer the weight; against it, the question asks for the peak "in a specified environment", so each dye-solvent row could be a decision of its own, which the solvent's small effect weakens: LightGBM scores RMSE 54.0 nm without the solvent against 53.9 nm with it.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per-row RMSE (implemented) | Keep the score per row; a note gives how unequal the dyes are and how far one vote per dye moves the ranking | the source's per-row score; no change | a dye measured in 335 solvents counts 335 times in a decision made once; one dye decides a third of the scaffold folds |
     | B | Each dye once | RMSE weighted by 1 over the dye's rows, a scoring column declared as the task's `unit_weight`, for scoring only | one rule for all 2,609 multi-row dyes, the betaine dye and the 61 differing sets; as the other once-per-unit cases | departs from the source's per-row score (named as the original); the ranking shift on the windows is not measured |

   - **Recommendation:** B: the actor decides once per dye and the further rows are the source's solvent protocol, which the solvent's small effect on the score confirms. **Decision:** keep the per-row score (A), or score each dye once (B)?

   **Notes for the AI:** On B: in `_clean`, after deduplication, `dye_weight = 1 / rows of the dye` on the no-stereo dye key (`key`); `Metric.fallback(reason=..., inputs={"weight": "dye_weight"})` with the reason naming the per-row RMSE of the source's follow-up (Joung et al. 2021, doi:10.1021/jacsau.1c00035) as the original and saying each dye counts once (1 to 335 rows per dye); `scoring_columns = (ScoringColumn(column="dye_weight", role="weight", used_by="rmse", description="1 over the rows of the row's dye (no-stereo key), so that each dye counts once in the RMSE; for scoring only, never a feature or a training weight"),)`; `unit_weight = UnitWeight(column="dye_weight", unit=<the dye key column>)` (ship the no-stereo key as a non-feature column if the unit needs one); a curation bullet with the decision. On A: a curation bullet with the unit counts above and the practitioner's tau (0.93 mean, 0.67 lowest, 4 models, scaffold folds). Either way, measure the ranking shift on the chosen split (4 or more models) and add it to the bullet; rerun the checks. The weight is no `group` input, so B leaves the scored unit the row: the window checks of issue 3 (b) and the split counts do not change.

   [^x21c4]: **MET-17** (Should): when units have unequal numbers of rows, the score counts each unit once if the actor decides once per unit and the further rows are repeats of the source's protocol, through a weight column for scoring only, declared as the task's `unit_weight`; per row when each row is a decision of its own, with a note on how unequal the units are and how far one vote per unit moves the ranking (Kendall tau 0.66 to 0.98 on its cases). **MET-11** (Must): a score that departs from the source's names the source's score as the original.

   **Andrej (2026-11-24, discuss):** What does the use case actually require?

   **Answer (AI, 2026-11-24):** one vote per dye, shared over the media the chemist plans to use.
   - The use case the definition states: a chemist screens a proposed dye, in the solvent or host they plan to use, before synthesis, to choose candidates with useful absorption. The decision is per dye (make it or not); the medium is an input to that decision, and the chemist plans one or a few media (the domain practitioner: "I decide once per dye whether to make it, and I usually care about one or two media").
   - So a dye measured in many solvents is one decision with many conditions, not many decisions. The per-row RMSE counts it many times; the weight of 1 over the dye's rows (B) gives each dye one vote and keeps every medium of it in the score at a share of that vote.
   - Under the shipped windows (decided today) the imbalance is moderate: Reichardt's betaine dye (334 rows, first paper 1994) always trains, and the largest test dye has 11-27 rows. Per window, measured 2026-11-24 on the shipped frame:

     | Test year | Test rows | Test dyes | Dyes with one row | Test rows in dyes of 10+ rows | Test rows of the 5 largest dyes | Largest test dye (rows) |
     |---|---|---|---|---|---|---|
     | 2015 | 1,215 | 423 | 223 | 18.8% | 5.8% | 15 |
     | 2016 | 1,611 | 437 | 227 | 38.2% | 6.1% | 23 |
     | 2017 | 1,443 | 535 | 313 | 28.6% | 8.0% | 27 |
     | 2018 | 1,959 | 709 | 375 | 21.5% | 4.3% | 17 |
     | 2019 | 2,040 | 784 | 449 | 9.4% | 3.4% | 15 |
     | 2020 | 297 | 97 | 46 | 25.3% | 18.5% | 11 |

   - Per row, the dyes with 10 or more rows (5-10% of test dyes) carry 9-38% of a window's score; each dye once, they carry their share of dyes.
   - What the use case does not settle: a chemist designing a solvatochromic probe acts on the shift across solvents, and for that use each row is a decision. The solvent moves the peak little next to the dye (SD 19.9 nm within a dye against 108.7 nm between dyes; LightGBM 53.9 nm with the solvent, 54.0 without), so the task measures dye structure either way, which is the screening use the definition states.
   - The answer does not change the choice: B stays recommended. Its open con remains: how far one vote per dye moves the model ranking on the six windows is not measured (on the former scaffold folds, Kendall tau 0.93 mean, 0.67 lowest, 4 models); the notes measure it when B is applied. **Decision:** keep the per-row score (A), or score each dye once (B)?

   **Andrej (2026-11-24, ok):** As implemented (A).

   **Resolved (2026-11-24, Andrej):** A, as implemented: the score stays per row. `curation_comments` gains a "Scoring per row, kept on purpose" bullet with the per-window figures of the answer above (dyes with 10 or more rows carry 9-38% of a window's score; the solvent moves the peak little next to the dye). No change to the splits or the metric.

5. **Drop the extrapolated gas row of Reichardt's betaine dye?**

   - **Problem:**
     - The betaine dye's gas row, 1,055 nm, is 28591/27.1: the ET(30) scale's extrapolated gas-phase value, not a measured peak.
     - Its other 334 rows convert measured peaks from the same review's table and stay.
   - **Background:** Myunghwan kept all 20 gas rows on 2026-11-10 and accepted the check warning on their missing solvent; that the 1,055 nm value is extrapolated was found this round, by the blind review, and the advocate and the critic agree[^x21c5].
   - **Effect on the task:** one row; under windows it only trains, under scaffold folds it is the largest single error of its fold. The other 19 gas rows (small molecules, 128-143 nm in the vacuum UV among them) are measurements and stay with a note.
   - **Experiments:** none needed: the value equals 28591/27.1 to the table's rounding.
   - **Consistency:** a value the source did not measure leaves when the source shows it, as an expert would ship it; this departs from the 2026-11-10 call only for this one row.
   - **Panel:** the blind review, the claim auditor, the advocate, the critic and the mediator all drop it.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | Keep all 20 gas rows | as Myunghwan decided on 2026-11-10 | scores a model on an extrapolated scale value as if it were a measurement |
     | B | Drop the row | Drop the betaine dye's gas row with a note; keep the other 19 gas rows and the accepted warning | every target is a measurement or a measured peak converted | departs from the 2026-11-10 call for one row; rebuild |

   - **Recommendation:** B: the row is the scale's extrapolation, a fact not known when the gas rows were kept. **Decision:** keep the row (A), or drop it (B)?

   **Notes for the AI:** On B: in `_clean`, after the medium state is set, drop the row whose dye is the betaine dye 30 (canonical SMILES of the 335-row dye) and whose `medium_state` is `gas`, with a comment; the ET(30) curation bullet ends "The gas row (1,055 nm, ET(30) = 27.1), the scale's extrapolated gas-phase value, is dropped (<curator>, <date>)."; the gas bullet and the accepted warning say 19 gas rows; note that the gas rows of small molecules at 128-143 nm (vacuum UV) are measurements kept at the margin of the dye use case. Rerun the checks; counts become 17,509 rows.

   [^x21c5]: **CLEAN-1** (Should): clean to the state an expert would ship, including removed anomalies the source shows. **PROV-13** (Must): repair or remove damage from the origin when the origin shows it. The 2026-11-10 call: Myunghwan, "accept gas warning".

   **Andrej (2026-11-24, change):** Option B: Drop the row.

   **Resolved (2026-11-24, Andrej):** B. `_clean` drops the betaine dye 30's gas row (1,055 nm, the ET(30) scale's extrapolated gas-phase value) after the medium state is set, with an assertion that exactly one row matches; 17,509 rows, 19 gas rows (the vacuum-UV small molecules at 128-143 nm noted as measurements at the margin of the use case). The ET(30) and gas curation bullets and the accepted `dataset_smiles_column` reason say 19 gas rows; the CC line is in the comments. Check: 0 errors.

**Review panel:** ship after changes (mediator, 2026-11-21, full re-check). Applied without a decision: the ET(30) origin note, the qualified "compiles experimental values" note, the solvent's small effect in `fit_reason`, `known` naming the neat-solid and gas states, the OLED-host films note, the charge-forms note, the scope of the "updated regularly" quote. Disputed and settled: the betaine rows are measured peaks in another unit (the critic conceded), only their gas row is extrapolated; the per-dye weight is one rule for all multi-row dyes, not a list. The mediator's addendum measured one-year windows; the review editor's fixes are applied (one-year windows 2015-2020 recommended in the Horizon block; issue 3 asks windows against scaffold groups only). For the curator: issues 3-5 and the Horizon block. Earlier panel (2026-11-09): ship after changes (mediator). The original metric-origin and chemical-alias findings were corrected and independently rechecked. No demonstrated unresolved Must failure or robust task-gaming exploit remains. The panel recommends the implemented repeat policies, with both curator marks accepted as implemented by Myunghwan on 2026-11-10; RMSE and the gas warning were also accepted, with a ship verdict.

<details><summary>Mediator (2026-11-21)</summary>

**Correction (mediator addendum, 2026-11-21):** the undated share is 1.9% of rows (339 rows, 156 dyes), not 1.7%; the one-year windows are measured in the addendum.

**Mediator: chromophore_optical_properties_db (chromophore), 2026-11-21**

Read: all seven reports in `reports/`, the blind review and the task gamer, the column audit (findings and tables), the record's `## Comments` and `## Review` (issues 1-3), `dataset.py`,
`check.log`, `task.log`, `leak.log`. Decisive experiment: one CPU job of the panel's run.

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-1 holds (real pre-synthesis screen; the betaine rows are measured peaks in kcal/mol, conceded by the
  critic); LEAK family holds as far as tested (gamer: no exploit; leak probe crashed half-way, its first half clean:
  0.0% exact copies, best single feature 0.39 vs 0.70 all); SPLIT-37 step 4(b) met and SPLIT-14 met by three
  first-year windows (measured below), so SPLIT-37 gives the entry-date split (issue 3 B); SPLIT-32 not met today
  (no time basis), fixed either way.
Value: TP-1 holds (LightGBM 45-54 nm vs train-mean 83-102 nm on every window; 40-79 vs 95-124 on scaffold folds);
  the `unstable` flag is one dye under scaffold folds (rmse 72-79 with it, 44-49 without), absent under windows.
Quality: one extrapolated label (gas row, 1,055 nm) to drop; notes on ET(30) origin, solvent effect, neat solid/host
  wording, charge states.
Weighed: source +, size +, signal +; literature selection and unrecorded conditions - (approximate fit).
For the curator: issue 3 (B, now measured); new item N1, one vote per dye (MET-17, weighing call); new item N2,
  drop the extrapolated gas row (departs from the 2026-11-10 gas CC).
```

**Decisive experiment: three-window layouts**

Dyes dated by the earliest Crossref year of their papers (no-stereo key); all rows of a dye go with its first year;
the 1.7% of rows of undated dyes go into training (earliest era). Train share = training rows / all 17,510 rows.
Analogue = Morgan r2 Tanimoto >= 0.7 to a training dye. Random draw = same number of test dyes drawn from the window's
pool (training + test dyes), 3 seeds. "Own paper in train" = test rows whose DOI has a row in training.

| Layout | Test years | Train share | Test rows | Test dyes | Test scaffold groups | Analogue, forward | Analogue, random draw | Analogue, scaffold on same test dyes | Test rows with own paper in train |
|---|---|---|---|---|---|---|---|---|---|
| L1 | 2016 | 57.9% | 1,640 | 441 | 266 | 7.9% | 59.3% | 6.3% | 1.6% |
| L1 | 2017 | 67.2% | 1,422 | 531 | 319 | 8.9% | 58.3% | 6.2% | 7.1% |
| L1 | 2018-2020 | 75.4% | 4,316 | 1,592 | 886 | 8.3% | 58.3% | 4.7% | 9.7% |
| L2 | 2017 | 67.2% | 1,422 | 531 | 319 | 8.9% | 58.3% | 6.2% | 7.1% |
| L2 | 2018 | 75.4% | 1,979 | 711 | 437 | 8.9% | 62.1% | 5.2% | 10.8% |
| L2 | 2019-2020 | 86.7% | 2,337 | 881 | 457 | 8.6% | 61.4% | 5.4% | 8.7% |
| L0 | 2015 | 51.0% | 1,204 | 421 | 229 | 4.8% | 60.4% | 2.4% | 6.1% |
| Shipped scaffold folds | - | about 67% | 5,450-6,164 | - | - | 31.4% (column audit) | - | - | 58.4-64.8% (column audit) |

Train share before each first year (rows, undated in training): 2014 44.5%, 2015 51.0%, 2016 57.9%, 2017 67.2%,
2018 75.4%, 2019 86.7%, 2020 98.3% (2020 holds 97 dyes, 297 rows).

Untuned LightGBM (Morgan count r2 2048 + solvent 256 + medium one-hot, defaults, as the gamer's), RMSE in nm:

| Split | RMSE per row | RMSE without the betaine dye | RMSE, 1/rows-of-dye weight | Train-mean RMSE |
|---|---|---|---|---|
| Scaffold folds, mean of 9 | 55.9 (39.7-79.1) | 46.5 (39.7-49.2) | 50.7 (44.4-58.0) | 95-124 |
| L1 windows, mean of 3 | 48.8 (45.1-53.5) | same (dye always trains) | 54.3 (49.4-57.7) | 93-102 |
| L2 windows, mean of 3 | 51.5 (47.9-53.7) | same | 57.3 (54.8-61.3) | 83-100 |

What it settles:
- SPLIT-37 step 4(b): forward 4.8-8.9% against 58-62% for a random draw on every window. The wave holds at the
  windows' own cuts, not only at 2014/2017.
- SPLIT-14 (Must): L1 and L2 pass without the curator's exception (57.9% lowest); every test window holds 229+
  scaffold groups (floor 33). L0's 2015 window sits at 51.0% only because undated rows are counted as training
  (about 49% without them), so it is not a safe first window.
- The same-paper sibling share drops from 58-65% (scaffold) to 2-11% (windows): the forward split removes the series
  siblings the scaffold split trains on.
- Under the windows the betaine dye (first year 1994) always trains; the folds' spread is 45-54 nm, the `unstable`
  cause disappears from scoring.
- The task stays learnable forward: LightGBM halves the train-mean error on every window; windows are about 2-5 nm
  harder than scaffold folds without the betaine dye.
- SPLIT-15: years 2015-2020 would allow up to 6 one-year windows above the floor (2015 marginal, 2020 small), against
  the SPLIT-33 target; the curator picks the layout (L1 recommended: no window relies on undated rows, newest window is
  the deployment period, each window adds a year). Fewer windows than the target need the `splits_below_target` note.

**Changes to make now (no decision needed)**

| Change | Rule |
|---|---|
| Curation note: the betaine dye 30's 334 solvent rows are 28591/ET(30) from Reichardt, Chem. Rev. 1994 (doi:10.1021/cr00032a005), its measured charge-transfer peak in kcal/mol, rounded to 0.1 kcal/mol (0.2-1.6 nm); whether every tabulated value comes from dye 30 itself or a secondary standard is unverified | PROV-1, EV-2 |
| Qualify the note "the source paper compiles experimental values ... extracted from spectra": one review's ET(30) table supplies 335 rows | EV-2 |
| `fit_reason`: solvent effects are small next to dye differences (SD within dye 19.9 nm vs between dyes 108.7 nm; LightGBM 53.9 with solvent vs 54.0 without), so scores mostly rank dye-structure models | USE-8 |
| `task_summary.known` names the neat-solid and gas designations; note that about 20 OLED-host doped films stay `solvent or host` | column audit, CLEAN-2 |
| Note: protonation/charge forms (phenol vs phenolate merocyanine, oxime vs oximate) are distinct dyes in distinct groups | LEAK-17, SPLIT-31 |
| Issue 3 Background: the "will be updated regularly" quote refers to the paper's search webpage; the growth rests on Figshare v1-v3 | EV-2 |
| Time basis either way: none today; set by the issue 3 choice (B: `Temporal` on a first-year column that is no input, Horizon block; A: `UnseenGroup` with the shares above) | SPLIT-32 |
| Rerun the leak probe before ship. Its first half is clean (0.0% exact copies; best single feature 0.39 vs 0.70 all; shallow tree 0.26/0.30). It crashed in the nearest-neighbour step. The cause is not established: `neighbour_space` fills NaN with 0, so the gas rows' missing solvent alone should not produce it. Fix the probe, not the definition, and rerun on the shipped splits (the new windows if B) | verification checklist, LEAK-16..21 |

**Issues for the curator, ranked**

**Issue 3 (P4, SPLIT-37 Should with SPLIT-14 Must): revise the Answer, keep the recommendation B**

- **Problem:** the Answer's condition ("B if a layout of three windows passes the floor") is now measured: L1 passes.
- **Effect:** under B the test is the next years' dyes (forward analogue 8-9%, own-paper rows 2-11%); under A new
  scaffolds from the whole span (31.4%, own-paper rows 58-65%).
- **Advocate / critic:** both B if three windows pass, else A; no remaining difference.
- **Rule:** SPLIT-37 step 4: the source aims at "newly designed organic chromophores prior to their synthesis", the
  date is the first publication, labels final, 4(b) met, SPLIT-14 met. B is the rule's outcome; A would now be a
  departure from a Should and needs the fact that sets the case apart (an exception). The 2026-11-09 CC (Myunghwan,
  scaffold) predates step 4; the Background already cites it, so choosing B is a deliberate change, as in qsar_tid_11.
- **Limits for B's notes:** the DOI year is literature entry, not catalogue entry (accepted for apistox, qsar_tid_11);
  the windows sit in 2016-2020; the practitioner calls a forward split "the strict end" of lead optimisation; undated
  dyes (1.7% of rows) train.
- **Revise:** replace the "windows are tight" bullet with the L1/L2 table above; recommendation B with L1 (test 2016,
  2017, 2018-2020); decision: B on L1 (or L2), or A as an exception.

**N1 (P6, MET-17 Should; weighing call): score each dye once?**

- **Problem:** the actor decides once per dye; the median dye has 1 row, 287 dyes have 10 or more (23% of rows), one
  has 335. Solvent series are a solvatochromism protocol of the source papers.
- **Effect:** under scaffold folds the betaine dye gives 57-68% of the squared error in 3 of 9 folds; the per-dye
  weight removes that (fold 1: 79.1 per row, 51.1 per dye). Under B the dye always trains, so the case rests on the
  other multi-row dyes; on the L1 windows per-dye RMSE is 4-8 nm above per-row.
- **One item:** yes. A weight of 1/(rows of the dye) is one rule that covers all 2,609 multi-row dyes at once: the
  betaine dye, the 287 series of 10+ rows and the 61 sets with differing wavelengths (each inside one dye). It is not
  a per-dye list. Dropping or capping the betaine dye is only a fallback, and only under A when the weight is refused.
- **Advocate / critic / practitioner:** all three prefer the weight (scoring only, `unit_weight`, per-row RMSE named as
  the source's original, MET-11). Per-dye ranking against per-row: tau 0.93 mean, 0.67 lowest (practitioner, 4 models,
  scaffold folds), inside MET-17's 0.66-0.98.
- **Against:** the question asks for the peak "in a specified environment", so each dye-solvent row could be its own
  decision (MET-17's per-row branch). The solvent moves RMSE by 0.1 nm, which weakens that reading.
- **Precedent:** superconductivity (one vote per composition, 2026-11-08), dementia_prediction and
  pancreatic_cancer_mouse_detection (one vote per person / mouse). MET-17 allows the weight when inputs differ within
  the unit.
- **What would settle it:** the ranking shift on the chosen splits (4+ models on the B windows), not yet measured.
- **Options:** (a) `unit_weight` 1/(rows of the dye), scoring only (recommended); (b) per-row RMSE with the MET-17
  note (unit counts, tau numbers); (c) under A only, per-row RMSE and drop or cap the betaine dye.

**N2 (P5, PROV/CLEAN-1 Should): drop the extrapolated gas row of the betaine dye**

- **Problem:** the 1,055 nm gas row is ET(30) = 27.1, the scale's extrapolated gas-phase value, not a measurement
  (blind review; advocate and critic agree).
- **Effect:** one row; under B it is a training row only; under A it is the largest single error in its folds.
- **Why a decision:** Myunghwan's CC of 2026-11-10 keeps all 20 gas rows (accepted warning). The new fact (not a
  measurement) was not known then.
- **Recommendation:** drop the row with a note; keep the other 19 gas rows and the accepted warning (its count becomes
  19). The vacuum-UV small molecules (128-143 nm) stay with a note.

**Issues 1 and 2: resolved (Myunghwan, 2026-11-10); keep as written**

Nothing this round contradicts 1A or 2A with a measurement. The precedent checker's gap with superconductivity (repeat
sets scored per row) closes if N1 (a) is taken; otherwise a note (61 sets, 0.4% of the weight) suffices.

No Horizon block exists in this record yet; under B one is needed (window length one year, gap 0: final labels, a
catalogue with no outcome delay) and needs the curator's sign-off.

**Agreed facts**

- Real pre-synthesis screen; inputs are two typed SMILES and `medium_state`; no post-outcome column (all roles).
- The betaine dye's 335 rows: one review, 334 = 28591/ET(30), measured peaks in another unit; gas row extrapolated.
- No exploit beyond the noise band (gamer); 0 group and InChIKey overlap in all 9 folds (claim audit).
- Signal: LightGBM beats the mean on every split (task.log, gamer, practitioner, blind rerun, this job).
- The solvent input carries almost no signal (53.9 vs 54.0).
- Issue 3 measurement: forward 3.9-8.9% vs random 44-62% analogue share; L1 and L2 pass SPLIT-14.
- Leak probe crashed in its nearest-neighbour step; its first half is clean.

**Consistency**

- B follows qsar_tid_11 (6-30% vs 79.7%, moved off scaffold 2026-11-11) and apistox (10-24% vs 17-30%); the gap here
  (8-9% vs 58-62%) is wider than both. qsar_oral_toxicity and qsar_aquatic_toxicity kept scaffolds because forward
  matched random; superconductivity and qsar_biodeg because the source limited its scope. Neither fact holds here.
- Undated rows into training follows apistox's fallback dating rather than dropping (SPLIT-26).
- N1 (a) follows the MET-17 cases; (b) would match asp_potassco and video_transcoding, where each row is a decision
  of its own, which the practitioner says is not so here.
- Departing from the 2026-11-09 CC is a newer rule applied to a measurement, the same path as qsar_tid_11.

</details>

<details><summary>Mediator addendum (2026-11-21)</summary>

**Mediator addendum: chromophore one-year windows (2026-11-21)**

One CPU job of the panel's run, with the same method as the report's decisive experiment.

How the numbers were made:
- Each dye is dated by the earliest Crossref year of its papers (key: the dye without stereochemistry). All rows of a
  dye go with that year.
- Undated dyes always train.
- Each window tests one first-publication year and trains on all earlier years (expanding windows).
- Train share is the share of all 17,510 rows that train.
- A close analogue is Morgan radius 2, Tanimoto 0.7 or more to a training dye. The random draw takes the same number
  of dyes from the window's pool (3 seeds).
- LightGBM is untuned, on the gamer's features.

**Undated share: corrected to 1.9%**

| Count | Rows | Share of rows |
|---|---|---|
| Dyes with no dated paper (156 dyes): these always train | 339 | 1.9% |
| Rows whose own DOI has no year (some belong to dated dyes) | 362 | 2.1% |

The editor is right. My report's "1.7%" was wrong; it should read 1.9% (339 rows of 156 dyes).

A second correction:
- My report said the 2015 cut drops to "about 49%" without the undated rows. That figure divides by all 17,510 rows.
- If the undated rows were dropped from the data instead, the 2015 cut trains on 8,589 of 17,171 rows, which is 50.0%.
- Either way, 2015 is at the floor.

**Per window (one-year test windows)**

| Test year | Train share | Test rows | Test dyes | Test scaffold groups | Close analogue, forward | Close analogue, random draw | Test rows with own paper in train | LightGBM RMSE per row | RMSE, one vote per dye | Train-mean RMSE |
|---|---|---|---|---|---|---|---|---|---|---|
| 2012 | 33.8% | 1,081 | 326 | 176 | 2.1% | 58.6% | 9.1% | 51.5 | 58.4 | 96.4 |
| 2013 | 40.0% | 784 | 381 | 207 | 3.1% | 59.0% | 8.3% | 68.7 | 70.6 | 108.0 |
| 2014 | 44.5% | 1,144 | 596 | 379 | 5.9% | 58.9% | 23.8% | 64.8 | 72.8 | 124.6 |
| 2015 | 51.0% | 1,204 | 421 | 229 | 4.8% | 60.4% | 6.1% | 64.3 | 68.0 | 95.9 |
| 2016 | 57.9% | 1,640 | 441 | 266 | 7.9% | 59.3% | 1.6% | 45.1 | 49.4 | 102.1 |
| 2017 | 67.2% | 1,422 | 531 | 319 | 8.9% | 58.3% | 7.1% | 47.9 | 55.7 | 100.1 |
| 2018 | 75.4% | 1,979 | 711 | 437 | 8.9% | 62.1% | 10.8% | 53.7 | 61.3 | 83.3 |
| 2019 | 86.7% | 2,040 | 784 | 420 | 8.8% | 63.1% | 10.0% | 52.6 | 55.8 | 99.8 |
| 2020 | 98.3% | 297 | 97 | 39 | 8.2% | 61.9% | 0.0% | 51.6 | 48.4 | 104.3 |

Under the shipped scaffold folds:
- 31.4% of test dyes have a close analogue in training.
- 58-65% of test rows have a row of their own paper in training.
- Untuned LightGBM scores RMSE 55.9 per row (46.5 without the Reichardt dye) and 50.7 with one vote per dye.

**Per layout**

| Layout | Windows | Lowest train share | Below the 50% floor | Smallest test window (scaffold groups) | Mean RMSE per row | Mean RMSE, one vote per dye |
|---|---|---|---|---|---|---|
| Five years, 2016-2020 | 5 | 57.9% | none | 39 (2020) | 50.2 | 54.1 |
| Six years, 2015-2020 | 6 | 51.0% | none (2015 at the floor, see above) | 39 (2020) | 52.5 | 56.4 |
| Nine years, 2012-2020 | 9 | 33.8% | 2012, 2013, 2014 (33.8 / 40.0 / 44.5%): curator's exception, all above 30% | 39 (2020) | 55.6 | 60.0 |
| L1 (2016, 2017, 2018-2020), from the report | 3 | 57.9% | none | 266 | 48.8 | 54.3 |

**What this shows**

- **The wave holds in every year.** Forward analogue shares are 2-9% against 58-63% for a random draw, so SPLIT-37
  step 4(b) holds on every window.
- **The 2020 window passes the least test window only narrowly.** It has 39 scaffold groups against a floor of 33,
  97 dyes and 297 rows, and no test row shares a paper with training.
- **2015 is borderline.** It reaches 51.0% only because undated dyes train; it is 50.0% if they were dropped.
- **The five-year layout (2016-2020) is the largest one that passes the floor with room to spare.** It has no
  exception and five separate training sides.
- **The nine-year layout reaches nine windows only through three exceptions below the floor.** The earliest windows
  are also the hardest: RMSE 52-69 against 45-54 from 2016 on.
- **One vote per dye scores 3-8 nm above per row in every window except 2020** (48.4 against 51.6). This matches the
  report.

</details>

<details><summary>Advocate (2026-11-21)</summary>

**Advocate opening: chromophore_optical_properties_db (chromophore), 2026-11-21**

Position: ship. The task, the inputs and the data are sound. Two real problems came up this round: the Reichardt
betaine dye's weight in the score, and issue 3's split. Each has a fix that keeps the dataset. I give the mildest one
and do not deny either problem.

Evidence read: claim audit, domain practitioner, precedent check, blind review, task gamer, column audit
(findings and tables), the record's issues 1-3
and the 2026-11-21 answer, `task.log`, `check.log`. `leak.log` crashed (NaN in the gas rows) and has no result. The
blind reviewer's first baseline run crashed (LightGBM rejected its feature names), so it has no numbers.

**1. A real pre-synthesis task with strong, model-separating signal (USE-1 Must, TP-1)**

- The actor and moment are the source's own: "predict the optical properties of newly designed organic chromophores
  prior to their synthesis" (Joung et al. 2020). Both inputs (dye structure, solvent or host) exist before synthesis.
  The practitioner confirms λmax is "the number I act on" and would use the model as a coarse filter. Its MAE of 34 nm
  is below raw TD-DFT's 54-80 nm (Greenman et al. 2022).
- `task.log`, shipped encoding, 5 of 9 splits:

  | Model | RMSE (nm) | Skill |
  |---|---|---|
  | dummy | 103.6 | 0 |
  | linear | 69.6 | 0.55 |
  | random forest | 57.0 | 0.70 |
  | LightGBM | 52.0 | 0.74 |

  LightGBM beats the dummy on 100% of splits. LightGBM minus linear is +0.19 skill (paired SE 0.056), so the task
  separates model families. The gamer (43.7-79.1) and the practitioner (53.9) reproduce the numbers on their own code.
- The `unstable` flag (TP-1, TP-5) has a measured cause, one dye (point 3), and not chemical families. Without that
  dye, fold 1 drops from 81.2 to 44.3. The folds then fall in a band of 38-49 nm.

**2. No leak and no exploit (LEAK Must family, SPLIT-31)**

- The features are only the two SMILES and `medium_state`. Emission, lifetime, ε, quantum yield, Tag and the DOI are
  all dropped (claim audit; gamer's post-outcome check).
- 0 group overlaps and 0 non-empty InChIKey overlaps across all 9 folds. 0 stereo-free dyes span groups. All 17,510
  dye SMILES are RDKit-canonical, so no writing-style signal exists (gamer).
- Every gamer attack fell inside the random-column noise band (0.06-0.97 nm) or did worse: formats, row order, test
  composition, label cleaning, and copying labels across InChIKey skeletons (48.4 vs 47.7). The 1-NN Tanimoto
  neighbour is legitimate signal, since a deployed model has its training set.
- The 4 skeletons that cross groups are acid/base forms with different wavelengths (193 vs 265 nm, 424 vs 586 nm).
  They are distinct species, not aliases (claim audit finding 2). LEAK-17 holds.
- Conceded: the leak probe must be rerun with the gas rows' NaN solvent handled before ship. That is a process gap,
  not evidence of a leak. The gamer's attacks already cover its questions.

**3. Reichardt's betaine rows are measured absorption maxima in another unit. Fix the score's weighting, not the data (PROV-1 Must holds; MET-2 Must; MET-17 Should)**

- The auditors call these 335 rows "not peaks read off spectra". The objection overreaches. ET(30) is *defined* as
  28591 / λmax(nm) of this dye's long-wavelength charge-transfer band in each solvent. So 28591 / ET(30) gives back the
  measured λmax exactly, to the table's rounding. The rows are this dye's absorption maxima in 334 solvents, published
  in kcal/mol. They are the most systematic solvatochromic series in the data. The source's question, the peak "in a
  specified environment", covers them, and the source is known (PROV-1 holds).
- What I concede:
  - The gas row (1,055 nm, ET(30) = 27.1) is an extrapolated estimate, not a measurement (blind review). Drop that one
    row (CLEAN-1).
  - Some tabulated ET(30) values may come from a secondary standard dye and a correlation, not from betaine 30 itself.
    Nobody checked which ones. A note should say so.
  - The curation note "extracted from spectra" needs a sentence on this origin (claim audit's mildest remedy a).
- The real problem is the score, not the data. In the 3 folds that hold this dye, it gives 57-68% of the squared error
  (gamer). An unseen scaffold cannot be predicted across 438-1,055 nm, so a third of the folds rank models on one
  molecule (MET-2).
- The mildest remedy is the practitioner's option (a). Weight each row by 1 / (rows of its dye), for scoring only,
  through `unit_weight` (MET-17, MET-15, MET-11, with the source's per-row RMSE named as the original).
  - It keeps every row (SPLIT-26).
  - It follows the curator's superconductivity decision of 2026-11-08 (one vote per composition), and MET-17 names that
    case.
  - It matches the actor, who decides once per dye.
  - The measured cost is small: per-dye RMSE 44.6 vs 53.9, ranking tau 0.93 on average and 0.67 at the minimum (inside
    MET-17's 0.66-0.98).
  - It also covers the 287 dyes with 10 or more rows (the Boc-amino-acid series), which per-row RMSE over-weights too.
- Dropping or capping the dye is the stronger remedy (remedy ladder: fix the definition before dropping data). It
  throws away real solvatochromic measurements, and the gamer showed the dye does not hurt training (-1.2 to +0.2 nm
  on the other rows). Choose it only if the curator rejects the weight.

**4. Issue 3: either answer keeps the dataset. B is conditional on a Must that is not yet checked (SPLIT-37 Should, SPLIT-14 Must)**

- I concede the measurement. A forward cut at 2014 leaves 3.9% of test dyes a close analogue, against 43.9% for a
  random draw of dyes. At 2017 the figures are 7.1% and 56.1%. That is a stronger wave than in qsar_tid_11 and apistox,
  which moved to windows. 58-65% of scaffold-fold test rows have a row of their own paper in training. SPLIT-37
  step 4(b) is met.
- Step 4 also requires windows that pass SPLIT-14 (a Must), "where it does not, the family key stands". Not measured
  yet:
  - The 2014 cut trains on 42.6%.
  - From `year_hist.csv`, interpolating inside the bins (an estimate, not a measurement), train shares are about 50%
    up to 2014, 58% up to 2015, 66% up to 2016 and 77% up to 2017. So expanding windows that test 2016, 2017 and
    2018-2020 look feasible. Each test window would hold hundreds of dyes, well over 33.
  - Someone has to compute this from the dated rows before B is chosen.
- Two facts limit B, and they belong in its notes:
  - The DOI year is when a dye entered the literature, not this catalogue, which was compiled in one pass in
    2019-2020 and back-filled in v3. Precedent (apistox, qsar_tid_11) accepted literature years, so I do not argue
    this blocks B.
  - The windows sit in a narrow 2016-2020 band. The practitioner adds that real design is mostly lead optimisation on
    known cores, so a forward split is "the strict end of what I face".
- What follows: B if the three-window layout passes SPLIT-14, with the 2.1% undated rows put into the earliest training
  era (closest to apistox, per the precedent check). Otherwise A, with the measured shares in the `Time basis:` line.
  Both need the SPLIT-32 time basis, which is missing today. Neither is a reason to hold the dataset back.
- The Background should cite Myunghwan's 2026-11-09 CC on the scaffold split and say the rule changed after it
  (precedent finding 3). Moving to B is then a deliberate change, as in qsar_tid_11.

**5. The solvent's small effect is a fit note, not a validity failure (USE-8 Must)**

- The solvent adds little: LightGBM scores 53.9 with the solvent and 54.0 without it. The SD within a dye is 19.9 nm,
  against 108.7 nm between dyes (practitioner F1).
- The fit is already `approximate`. USE-8 asks that the gap be written down, and nothing more. The practitioner
  agrees that "that is still a real screening task, because I choose the dye first and the solvent later".
- Fix: add one sentence to `fit_reason`.
- RMSE's weight on the tail of literature errors (F3) needs a note only. MET-5 and MET-8 give `rmse`, and the
  curator accepted it on 2026-11-10.

**6. The curator's earlier decisions stand, and precedent backs them (LEAK-19, LEAK-20, MET-5; precedent register: 0 flags)**

- Myunghwan accepted 1A (drop 193 equal input+target rows), 2A (keep 61 sets / 124 rows with differing wavelengths),
  RMSE and the gas warning on 2026-11-10, each with a CC.
- The precedent register raises 0 flags.
- Dropping the 193 rows departs from superconductivity's keep-all. Scale justifies it: repeats are 0.4% of the weight
  here, against 40% of the rows there. qsar_tid_11's dropped salt copies back it too.
- The precedent checker's option (a), a note giving those shares, is enough. If point 3's per-dye weight is adopted,
  it also gives the 61 repeated sets one vote, which removes the precedent gap entirely.
- Nothing this round contradicts these decisions with a measurement.

**7. The blind reviewer's other concerns are answered by the definition or by wording fixes (CLEAN-24, SPLIT-31)**

- **"Features are only SMILES strings."** The SMILES ship as typed special features with the house encoder (2,815
  coordinates). Raw SMILES as categories score 106.1 nm, against 56.7 nm for the structural encoding (9 of 9 folds).
  apistox and drug_induced_autoimmunity set the same pattern.
- **OLED host films merged with solutions.** About 20 films. The column audit already proposes the note, and the
  `known` wording fix for neat solids is agreed.
- **20 gas rows.** The curator kept them with a CC on 2026-11-10. Only the extrapolated 1,055 nm row goes (point 3).

**Changes I support before ship**

| Change | Rule | Kind |
|---|---|---|
| Rerun the leak probe with the gas rows' NaN solvent handled | LEAK | process |
| Drop the extrapolated gas row of the betaine dye; note the ET(30) origin of its other 334 rows | CLEAN-1, PROV | definition + note |
| `unit_weight` = 1 / rows per dye, scoring only (cap or drop the dye only if refused) | MET-17, MET-2 | curator decision |
| Issue 3: check SPLIT-14 on a three-window layout; B if it passes, else A; time basis either way | SPLIT-37, SPLIT-14, SPLIT-32 | curator decision |
| `fit_reason`: solvent effect small; `known`: neat-solid and OLED-host wording; issue 3 Background cites the CC | USE-8 | note |

</details>

<details><summary>Advocate rebuttal (2026-11-21)</summary>

**Advocate rebuttal: chromophore_optical_properties_db (2026-11-21)**

The critic and I agree on the verdict (ship after changes), on the fact base, and on most remedies. The only real
dispute is how to treat the betaine dye's 335 rows: drop them, or weight the score.

**New fact: the blind reviewer's rerun**

Scaffold-grouped, 3 folds × 3 repeats:

| Model | RMSE, all rows | RMSE, without Reichardt | R², without |
|---|---|---|---|
| Overall mean | 106.2 ± 8.9 | 99.3 ± 2.4 | -0.01 |
| Per-solvent mean | 106.3 ± 9.3 | 99.0 ± 2.3 | 0.00 |
| 1-NN Tanimoto | 72.6 ± 16.6 | 61.2 ± 3.9 | 0.62 |
| LightGBM, string counts | 65.4 ± 20.7 | 53.2 ± 2.6 | 0.71 |
| LightGBM, RDKit + Morgan | 53.9 ± 20.6 | 41.2 ± 1.9 | 0.83 |

- This is a third independent confirmation of signal, and of a clear ordering of model types: molecular features beat
  string counts, which beat a nearest neighbour, which beats the mean.
- It also measures the dye's effect on stability: it raises the fold SD of the best model from 1.9 to 20.6 nm.
- Both facts are on the critic's side and mine alike. They make the dye's handling the one decision that matters for
  the score.

**Point by point**

**1. The ET(30) rows. Dispute on remedy and on "not measurements". Concede the rest.**

Conceded:
- The dye decides a third of the folds: 57-68% of the squared error, fold SD ×10.
- "Fold spread = chemical families" is refuted (EV-2).
- The 1,055 nm gas row is extrapolated and goes.
- A curation note must give the origin.

Disputed:
- *"Not a measurement; for these rows the task is 'give the solvent's ET(30)'."* ET(30) is defined as
  28591 / λmax of this dye. The table value *is* the dye's measured absorption maximum, written in kcal/mol. Predicting
  a known dye's peak in a stated solvent is inside `task_summary.question` ("in a specified environment"). The
  practitioner is right that nobody screens this dye. USE-1 asks whether the row is the task's kind of
  observation, and a dye's peak in a solvent is. What I cannot rule out: some values may come from a secondary
  standard dye through a correlation. Nobody checked which ones, and the note should say so.
- *Drop the 335 rows as the mildest remedy.* It is not the mildest. The harm is in the score, so the fix belongs in
  the score:
  - A per-dye `unit_weight` (MET-17, scoring only) makes the dye count as one of the roughly 2,000 test dyes in its
    fold. That removes the dominance and keeps the rows (SPLIT-26).
  - The same weight is needed anyway for the 287 dyes with 10 or more rows (critic point 3).
  - The remedy ladder puts "fix the definition" before "drop rows". Of the two definition fixes, a scoring weight
    changes no data.
  - Dropping is my fallback, as the critic's "minimum fix" is theirs. So we differ only on order.
- *Conceded, and it settles much of this:* under option B the dye (first year 1994) always trains and is never
  scored. The critic is right that its score effect then disappears. Dropping it from training moves the other rows
  by -1.2 to +0.2 nm (gamer), so there is no reason to drop it under B. The weight question is then decided only by
  the multi-row dyes of the later eras.

**2. Issue 3, B if three windows pass the floor.** Concede in full. My opening reached the same conclusion with the
same condition. Two details:
- The critic's train shares (65.8% before 2017, 98.3% before 2020) are bin edges from `year_hist.csv`. Mine for 2014
  and 2015 are interpolations. Neither of us measured the per-year layout, so it must be computed before B is chosen
  (SPLIT-14, Must).
- Both of us put the undated 2.1% in the earliest training era, as apistox does. The note should name the
  DOI-year-is-not-catalogue-entry caveat, which precedent does not treat as blocking.

**3. Per-row RMSE counts dyes unequally (MET-17).** Concede, and I prefer the same remedy: `unit_weight` =
1 / rows per dye, with per-row RMSE named as the original (MET-11). We also agree that the 61-input-set weight is
covered by a note.

**4. The leak probe crashed.** Concede. Rerun it with the gas rows' solvent block imputed for the probe only. This is
a process fix, as both briefs say.

**5. Refuted statements and missing fit text.** Concede, with one qualification:
- "Literature-reported measurement" still holds for the ET(30) rows. They come from a review of measured values.
  What needs saying is that they are a unit conversion from one review, rounded to 0.1 kcal/mol, possibly partly from
  a secondary standard, and that the gas row was extrapolated.
- I accept the `fit_reason` text on the solvent's small effect (USE-8), the `known` wording, the OLED-host note and
  the charge-state note as written.
- The blind rerun adds one number for the SMILES-encoding note: RDKit + Morgan beat string counts by 12 nm (41.2 vs
  53.2 nm without the dye). That backs typed SMILES with the house encoder rather than raw strings. The critic and I
  both left it unraised as a defect.

**What follows**

| Item | Joint position | Open between us |
|---|---|---|
| Gas row at 1,055 nm | drop | - |
| ET(30) origin note | add | wording: still a measurement (advocate) vs not (critic) |
| Betaine dye's 334 rows | fix needed under A | weight first (advocate) vs drop first (critic); moot under B |
| `unit_weight` per dye | preferred by both | - |
| Issue 3 | B if a three-window layout passes SPLIT-14, else A + `UnseenGroup`; time basis either way | - |
| Leak probe rerun | before ship | - |
| Text fixes (`fit_reason`, `known`, OLED, charge states, issue 3 Background cites the 11-09 CC) | apply | - |

</details>

<details><summary>Critic (2026-11-21)</summary>

**Critic opening: chromophore_optical_properties_db (2026-11-21)**

Position: **ship only after changes.** The task is real: a chemist predicts a proposed dye's first absorption peak
before synthesis. No Must failure calls for exclusion. But one dye's rows are not the task, the split ignores a
measured wave, and the leak probe never ran. Points are ordered validity first, then value, then quality.

**1. 335 rows are the ET(30) solvent-polarity table, not the use case, and they decide a third of the folds (USE-1 Must, SPLIT-23 Must, EV-2 Must)**

- **Problem.** Reichardt's betaine dye 30 has 335 rows, all from one review (Reichardt, Chem. Rev. 1994,
  doi:10.1021/cr00032a005). 334 of the 335 labels are exactly 28591 / ET(30), with ET(30) on a 0.1 kcal/mol grid.
  The 1,055 nm gas row is the scale's extrapolated gas-phase value (ET(30) = 27.1), not a measurement. The claim
  auditor, the blind reviewer and the task gamer each found this on their own.
- **Effect on the task.** This dye is a solvent-polarity probe. No chemist screens it as a candidate. For these
  rows the task becomes "give the solvent's ET(30)", which is a different question. It has one scaffold, so it is
  always unseen and always tested as a single block:

  | Split (in test) | RMSE as shipped | RMSE without the dye | Dye's share of squared error |
  |---|---|---|---|
  | r0f1 | 79.1 | 49.0 | 57% |
  | r1f2 | 75.3 | 44.1 | 68% |
  | r2f0 | 72.2 | 49.0 | 57% |

  (Task gamer, untuned LightGBM; the claim auditor gets 81.2 vs 44.3 on r0f1.) 1.9% of the rows carry 14.3% of the
  target's sum of squares. They explain the `unstable` flag (TP-1/TP-5) and the 37.8-90.1 nm fold spread that the
  record puts down to "chemical families".
- **Rules.** USE-1: every row is checked against the use case. SPLIT-23: the source's use case decides what one
  prediction is. EV-2: the measured cause (one dye) replaces the inferred one (families).
- **Remedy (mildest that works).** Drop the 335 rows, or keep the dye in a few solvents taken from primary papers if
  any exist. At the very least, drop the extrapolated 1,055 nm gas row. Write the origin in a curation note. If the
  curator keeps the rows, the per-dye weight of point 3 is the minimum fix, and the notes must give the fold shares
  above. Under option B of point 2 the dye (first year 1994) always trains and is never scored. Its score effect
  then disappears, and dropping it from training moves the other rows' RMSE by -1.2 to +0.2 (within noise, task
  gamer). Under A it must be fixed.

**2. The date carries a strong wave; issue 3 should go to B if three windows pass the floor (SPLIT-37 Should, SPLIT-14 Must, USE-10 Must, SPLIT-32 Should)**

- **Problem.** The source aims at "newly designed organic chromophores prior to their synthesis". That reaches the
  items the catalogue does not hold yet (SPLIT-37 step 3 goes on to step 4). The measurement answers step 4(b):

  | Split | Test dyes with a close training analogue (Tanimoto >= 0.7) |
  |---|---|
  | Forward, first year >= 2014 | 3.9% |
  | Random dye draw, same size | 43.9% |
  | Forward, first year >= 2017 | 7.1% |
  | Random dye draw, same size | 56.1% |
  | Scaffold folds (shipped) | 31.4% |

  The gap is wider than for both precedents that moved to windows: qsar_tid_11 (6-30% vs 79.7%) and apistox
  (10-24% vs 17-30%). Under the shipped scaffold folds, 58.4-64.8% of test rows have a row of their own paper in
  training. Those are the siblings a chemist designing the next series does not hold. This is the fact that moved
  qsar_tid_11 off scaffold groups.
- **Feasibility (SPLIT-14, Must).** Dated rows before 2014 are 42.6%, before 2017 65.8%, before 2020 98.3% (column
  audit `year_hist.csv`). A layout of three one-year-or-so windows with cuts at 2016, 2017 and 2018 should keep
  every window at or above 50% without the curator's exception, and each test window holds hundreds of dyes (the
  floor is 33). The 2014 cut needs the 30-50% exception, so it is not the first choice.
- **Undated rows (2.1%, 98 DOIs).** Put them in the earliest training era, as apistox dates its undated compounds by
  a fallback rather than dropping them (SPLIT-26, keep the rows).
- **Also missing either way.** The definition has no `data_tags` and no `Time basis:` line (SPLIT-32).
- **Remedy.** B with the cut years checked against SPLIT-14. If no three-window layout passes, then A with
  `UnseenGroup` and a `Time basis:` line giving 3.9% vs 43.9% and the same-paper share. The issue 3 Background should
  cite Myunghwan's 2026-11-09 CC ("Pursue the discussed scaffold-grouped evaluation") and say that SPLIT-37 step 4
  came after it (precedent checker, finding 3).

**3. Per-row RMSE counts the unit of decision unequally, and the notes do not say so (MET-17 Should, MET-11)**

- **Problem.** The chemist decides once per dye. The median dye has 1 row, 287 dyes have 10 or more (23% of rows),
  and one has 335. Solvent series of one dye are a solvatochromism protocol: for example, a Boc-amino-acid
  benzoxazole series adds about 36 solvents each, with an SD of 2-7 nm.
- **Evidence (domain practitioner, 9 folds).** Per-dye-weighted RMSE is 44.6 against 53.9 per row. The ranking of
  4 models has Kendall tau 0.93 on average, 0.67 at the minimum, and 0.33 at the minimum for per-dye MAE. The
  solvent input adds nothing measurable (LightGBM 53.9 with the solvent vs 54.0 without), so the scores mostly rank
  dye models anyway.
- **Rule.** MET-17: count each unit once when the actor decides once per unit; if the score stays per row, the
  notes say how unequal the units are and how far one vote per unit moves the ranking. The definition does neither.
  superconductivity (2026-11-08, Lennart) took the weight for the same kind of literature compilation.
- **Remedy.** Preferred: `unit_weight` = 1/(rows of the dye), scoring only, with the source's per-row RMSE named
  as the original (MET-11). Minimum: the MET-17 note with the numbers above. This is separate from the precedent
  checker's input-set weight (61 sets, 0.4% of rows). That one is small, and a note covers it.

**4. The leak probe crashed; the verification is incomplete (verification checklist P4, LEAK-16 to LEAK-21)**

- **Problem.** `leak.log` ends in `ValueError: Input X contains NaN` (NearestNeighbors on the 20 gas rows' missing
  solvent encoding). So there is no leak-probe result on the merged definition. The task gamer's manual attacks
  (copies, nearest neighbour, order, formats) found nothing, which lowers the risk but does not replace the probe.
- **Remedy.** Rerun the leak probe with the gas rows' solvent block imputed for the probe only, or with NaN-tolerant
  models, before ship. A process fix, not a reason to exclude.

**5. Refuted and missing statements in the definition (EV-2 Must, USE-8 Must)**

- "The source compiles experimental values" and `task_summary.row` ("literature-reported measurement") do not hold
  for the 335 ET(30) rows (point 1). The assessment's "fold spread = chemical families" is refuted.
- `fit_reason` must name the gap the data shows (USE-8): solvent effects (within-dye SD 19.9 nm) are small next to
  differences between dyes (SD 108.7 nm), and the solvent input moves RMSE by 0.1 nm, so the benchmark mostly
  scores dye-structure models.
- Column audit (KNOWN): `task_summary.known` should name the neat-solid and gas designations. A curation note should
  say that about 20 OLED-host doped films stay `solvent or host`, mixed with solutions. A separate state is not
  needed for 20 rows (CLEAN-2, minimal preprocessing). The blind reviewer's "about 350 rows" counts long solvent
  SMILES, not hosts, and does not support more.
- Remedy: the text edits, plus a curation note that charge states (phenol vs phenolate merocyanine, oxime vs
  oximate) are treated as different dyes (claim auditor, finding 2; low).

**Not raised**

- SMILES-only features (blind reviewer, concern 1): typed SMILES are the house contract, and the pipeline encodes
  them (CLEAN-2, molecules guide). Not a defect.
- The 61 conflicting input sets and the 193 dropped repeats: settled by Myunghwan (1A, 2A). Nothing new contradicts
  those decisions.
- Gas rows in the vacuum UV (128-143 nm): real measurements of small molecules. Out of the dye use case at the
  margin, but only 19 rows once the 1,055 nm row goes. A note is enough.

</details>

<details><summary>Critic rebuttal (2026-11-21)</summary>

**Critic rebuttal: chromophore_optical_properties_db (2026-11-21)**

Net position after the advocate's brief: **ship after changes.** We now agree on every remedy. The one change of
substance is that I concede the betaine rows are measured peaks. My point 1 therefore moves from a validity problem
(USE-1, SPLIT-23) to a scoring problem (MET-2, MET-17), and the per-dye weight becomes my first remedy, not dropping
the rows.

| Advocate point | Verdict | Why |
|---|---|---|
| 1. Real pre-synthesis task, signal separates models | concede | `task.log`: LightGBM beats the dummy on every split; LightGBM minus linear is +0.19 skill (SE 0.056). I never disputed the task. |
| 2. No leak, no exploit | concede, with the probe condition | The gamer's attacks all stay inside noise. The advocate also concedes the leak-probe rerun. It stays a condition before ship. |
| 3. Betaine rows are measured λmax in another unit; weight, don't drop | concede the facts and the remedy order | See below. |
| 4. Issue 3: B if three windows pass SPLIT-14, else A | concede | Same as my point 2, and the advocate adds a layout. See below. |
| 5. Solvent effect is a `fit_reason` note | concede | Same as my point 5 (USE-8). |
| 6. 1A, 2A, RMSE and the gas warning stand | concede | Nothing this round measures against them. The per-dye weight also gives the 61 repeated sets one vote, which closes the precedent checker's gap with superconductivity. |
| 7. Blind reviewer's other concerns | concede | Same as my "Not raised" section: typed SMILES (106.1 vs 56.7 nm) and about 20 host films. |

**Point 3: what I concede and what still holds**

- **Conceded: the provenance claim.** ET(30) is defined as 28591 / λmax (nm) of betaine dye 30's long-wavelength
  charge-transfer band in each solvent. So 28591 / ET(30) recovers the measured peak, up to the table's 0.1 kcal/mol
  rounding. That rounding is about 0.2 nm at 440 nm and about 1.6 nm at 925 nm, well below the label noise of
  issue 2.
- My phrase "not the use case, a converted table" was therefore wrong as a provenance claim. The claim auditor's
  "refuted for 335 rows" against "the source compiles experimental values" should be withdrawn. Only the 1,055 nm
  gas row is not a measurement.
- **Conceded: USE-1 and SPLIT-23 are not broken.** The source's question, the peak "in a specified environment",
  covers a known dye in many solvents. Being a standard probe does not take a dye out of that question.
- **Still holds, and the advocate agrees.** One molecule decides 57-68% of the squared error in 3 of the 9 folds
  (gamer). That is a MET-2 mismatch between the score and the actor's per-dye decision, not a data defect.
- **Still open: not every tabulated ET(30) value need come from betaine 30.** The advocate names this risk:
  values for solvents where the dye is insoluble may come from a secondary standard and a correlation. Nobody
  checked. The note should say "unverified per solvent", not "measured", until someone reads the review's
  footnotes.
- **Remedy, now agreed:**
  1. Drop the 1,055 nm gas row.
  2. Write a note on the ET(30) origin.
  3. Set `unit_weight` to 1 / (rows of the dye), for scoring only, with the source's per-row RMSE named as the
     original (MET-17, MET-11).
  4. Drop or cap the dye only if the curator refuses the weight. If the curator keeps per-row RMSE, the MET-17 note
     must give the fold shares and the ranking shift (tau 0.67 at the minimum, 0.33 for per-dye MAE).
- **Under B the weight still matters.** The dye's first year is 1994, so it always trains and is never scored.
  Even so, the weight still covers the 287 dyes with 10 or more rows. So the weight decision stands apart from
  issue 3.

**Point 4: one precision**

- The advocate's train shares (about 50%, 58%, 66% and 77% up to 2014-2017) interpolate inside the
  `year_hist.csv` bins, so they are estimates. The answer to issue 3 measured only that the 2016 and 2017 cuts pass.
- Both of us asked for a three-window layout testing 2016, 2017 and 2018-2020. Its per-window train share and
  distinct test dyes must be computed on the dated rows before the curator marks B.
- If the windows sit in the 2016-2020 band, the forward analogue share should be measured at those cuts too. The
  3.9% at the 2014 cut is not the windows' own figure. The 2017 cut (7.1% vs 56.1%) is the closer one.

**Remaining differences**

None on remedies. One difference in emphasis: I would make the leak-probe rerun and the SPLIT-14 window count
conditions before ship, not notes.

</details>

<details><summary>Claim audit (2026-11-21)</summary>

**Claim audit: chromophore_optical_properties_db (chromophore), 2026-11-21**

Scope: every statement of `task_summary`, each `curation_comments` bullet, `splits_comment`, the accepted warning, the
grouping definition, the metric, and the record's screening block and assessments. Tests ran on the merged definition
(raw Figshare v3 CSV, shipped `_clean` frame and the 9 shipped folds) in the panel's run.

Probe outputs read: check.log (0 errors, 0 warnings, 2 infos: conflicting duplicates, `meta_time_basis_missing`),
task.log (LightGBM beats the dummy on 100% of splits; flag `unstable`, TP-1/TP-5), dtype.log (nothing flagged),
group.log. **leak.log crashed** (`ValueError: Input X contains NaN`, probably the 20 gas rows' missing solvent
encoding): the leak probe has no result.

**Findings**

**1. NEW: the largest dye is the ET(30) solvent-polarity scale, back-computed from a review table (validity, Must)**

- **Evidence.** The dye with the most rows is Reichardt's betaine dye 30 (`[O-]c1c(-c2ccccc2)cc(-[n+]2...`):
  335 rows, 334 solvents plus 1 gas row, **all from one reference**, Reichardt, Chem. Rev. 1994
  (doi:10.1021/cr00032a005, "Solvatochromic dyes as solvent polarity indicators").
- 334 of its 335 wavelengths are exactly 28591 / ET(30), with ET(30) on a 0.1 kcal/mol grid (e.g. 437.8407351 nm,
  1055.01845 nm = 28591/27.1). So these values are a conversion of the tabulated ET(30) solvent scale, not peaks
  read off spectra by two extractors. The 1,055 nm gas row is the scale's gas-phase value. The column audit flagged
  this row as unverified but did not trace where it comes from.
- Weight in the task: 1.9% of rows, but **14.3% of the target's total sum of squares** (range 438-1055 nm).
- It drives the fold instability that the record reports but does not explain:

  | Fold (repeat 0) | LightGBM RMSE | Betaine in test | RMSE without the betaine group | Betaine group RMSE |
  |---|---|---|---|---|
  | 0 | 38.3 | no | 38.3 | - |
  | 1 | 81.2 | yes (335 rows) | 44.3 | 278.3 |
  | 2 | 39.5 | no | 39.0 | - |

  The betaine dye is in the test side of folds 1, 5 and 6, so 3 of the 9 folds. In fold 1, the 5 largest groups
  give 79% of the squared error. In folds 0 and 2 they give 17-19%.
- **Claims this refutes or qualifies.** The curation note "The source paper compiles experimental values" and
  `task_summary.row` ("literature-reported ... measurement") do not hold for these 335 rows. The panel's explanation
  of the 37.8-90.1 nm spread as "signal varies across chemical families" is wrong for the worst folds: one
  single-reference scale explains it. For this dye the use case is different too. Its 334 rows ask for a solvent's
  polarity, not for the absorption of a new dye.
- **Rules.** USE-1 and MET-2 (the score is dominated by one unit that is not the use case's decision); PROV
  (derived values presented as extracted measurements); EV-2 (the measured cause replaces the inferred one).
- **Mildest remedy.** Add a curation note giving the origin (28591/ET(30), one review, 335 rows, 3 of 9 folds) and
  extend `fit_reason`. Then a separate decision item for the curator: (a) keep it as is and document it; (b) keep
  only rows whose value comes from a spectrum (drop the 335 rows, or keep a few) because they are a solvent-scale
  table; (c) cap or down-weight rows per dye. I recommend (b) or (a)+note. Rerun qualification if the rows change.

**2. NEW (low): acid/base forms of one molecule sit in different groups**

- Four connectivity skeletons (the first block of the InChIKey) cross groups. All four are protonation or charge
  forms with different wavelengths:
  - diaminophenyl-benzothiazole, 4 forms, 300-360 nm;
  - a merocyanine as phenol vs quinoid form, 424 vs 586.5 nm;
  - acetone oxime vs oximate, 193 vs 265 nm;
  - acetic acid vs acetate, 200 vs 210 nm.
- These are distinct species, not aliases, so the claim "aliases kept together" still holds. A curation note could
  say that charge states are treated as different dyes.
- In addition, 13 dative-bond metal complexes (Zn, Ru) have an empty InChIKey. Only the tautomer key protects them.
- Rule: LEAK-17 / SPLIT-31. No change needed.

**3. KNOWN (column audit): `task_summary.known` omits the neat-solid designation**

`medium_state` has 369 `neat solid` rows. In all of them the raw dye and solvent strings are identical. The paper's
Methods confirm this convention: "the chromophore is used as both chromophore and solvent".

**4. NEW (low): the "updated regularly" quote is scoped to the search webpage**

The paper's Code availability says "The database of this webpage will be updated regularly". Issue 3's background
cites it as growth of the catalogue. The growth itself is real (Figshare v1 to v3), so this only changes wording.

**5. NEW (process): leak probe failed**

leak.log ends in `ValueError: Input X contains NaN`. The leak probe was not run. It needs a rerun with NaN-tolerant
models or with the gas rows' solvent encoding filled.

**Claims table**

| Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| v3 CSV has 20,836 rows, 17,703 absorption labels; SHA pinned | comments, download_description | load raw through the definition | holds | 20,836 / 17,703; hash check passes in `_load_raw` | PROV |
| targets positive and finite, kept in nm | comments, task_summary.predicted | min, max, finite | holds | 127.7-1055.0 nm, all finite | CLEAN |
| Tag is a row number; Reference a DOI | comments | Tag == 0..n-1 | holds | Tag unique and equal to position | LEAK |
| Molecular weight is structure-derived | comments | compare with RDKit masses | holds | 95.1% equal RDKit exact (monoisotopic) mass within 0.01; it is an exact mass, not the average molecular weight | CLEAN-24 |
| other optical outcomes are not inputs | comments | feature list | holds | features: two SMILES and medium_state; scaffold excluded as group | LEAK |
| v3 includes nonorganic species, metal complexes, up to 225 heavy atoms | comments | RDKit atom scan | holds | max 225 heavy atoms, 7 dyes above 150, 17 with a metal, 5 without carbon (Cl2, Br2, I3-, ...) | USE |
| stereochemistry and fragments kept | comments | count stereo marks and '.' | holds | 18 dyes carry stereo marks; no dye has several fragments (so the fragment claim is vacuous) | CLEAN |
| 20 gas rows; Solvent_SMILES missing only there | comments, accepted warning | count | holds | 20 gas rows, 20 missing solvents, 0 unparsable non-gas solvents | - |
| neat solid = same structure for dye and environment | comments | raw string equality | holds | 369 rows, 100% identical raw strings; paper Methods agree | - |
| dedup removes 193; only 50 are full-raw repeats | comments, Resolved 1A | duplicate counts | holds | 17,703 - 17,510 = 193; 50 labeled repeats on all fields but Tag | LEAK-16/18/19 |
| 61 input sets / 124 rows with differing wavelengths; range 0.5-100, median 3.5, 22 > 10 nm, 8 > 30 nm | comments, issue 2 | recompute | holds | 124 rows; range 0.5-100; median 3.5; 22; 8 (bundle info: 63 = 124 - 61 excess rows) | LEAK-20 |
| the source compiles experimental values extracted from spectra | comments, screening block | trace the largest dye | **refuted for 335 rows** | Finding 1: 334/335 values = 28591/ET(30), from one review | PROV, USE-1 |
| each dye and stereo form in one group; groups joined by InChIKey and tautomer key | comments, grouping | count dyes and keys across groups | holds | 0 stereo-free dyes and 0 nonempty InChIKeys span groups; 3,335 groups | SPLIT-31, LEAK-17 |
| ringless and oversized-scaffold dyes are their own groups | comments, grouping | scaffold shares | holds; the oversized case is vacuous | 41 ringless dyes (51 rows) are singletons; the largest scaffold (benzene) has 1.5% of dyes, below the 10% cap, so it never splits | SPLIT-31 |
| folds hold out whole groups | splits_comment | overlap per fold | holds | 0 group and 0 InChIKey overlap in all 9 folds | SPLIT |
| solvents recur across the split | task_summary.split | share of test rows whose solvent is in train | holds | 93.2-98.3% per fold | - |
| a dye with another scaffold can be a close analogue | splits_comment | Morgan r2 Tanimoto | holds | fold 0: 32.1% of test dyes have a train dye at >= 0.7; 2.6% have an identical fingerprint (homologues such as a 5- vs 4-thiophene chain; same-solvent difference median 8.4 nm, so not copies) | SPLIT-37 |
| the group key is never a predictor | splits_comment | `feature_cols` | holds | scaffold is excluded | LEAK |
| solvents alone carry no transferable signal | implied | solvent mean-encoding baseline | holds | 106.6 vs mean 106.5 nm RMSE | TP |
| LightGBM about 56.7 vs mean baseline 106.5 nm | assessment 11-09 | LightGBM on the shipped encoding, repeat 0 | holds | 53.0 nm on 3 folds; mean baseline 106.48 over 9 folds (exact match) | TP-1 |
| fold range 37.8-90.1 nm comes from "chemical families" | assessment, panel | per-group error split | **refuted** | Finding 1: one dye; fold 1 drops from 81.2 to 44.3 without it | EV-2 |
| paper: 20,236 combinations, 7,016 chromophores, 365 solvents, 1,358 papers; two extractors plus a cross-check | screening block | PMC7478979 | holds | quoted in the paper's Data Records and Methods | - |
| target = first absorption peak | task_summary.question | paper's Methods | holds | "the first absorption peak was selected" | MET-3 |
| paper scope: up to 150 heavy atoms | comments | Methods and data | holds | 150 in the paper; v3 has 7 dyes above it | - |
| "will be updated regularly" means the catalogue grows | issue 3 background | paper text | wording only | Finding 4 | - |
| fit approximate | task_summary | - | holds, and is stronger after Finding 1 | - | USE-8 |
| metric: RMSE fallback; the JACS Au 2021 paper reports RMSE and R², optimizes the joint standardized MSE of 7 targets | metric reason | PMC8395663 | holds | RMSE 26.6 nm for absorption, R² 0.71-0.93 in aggregate, "summing the mean squared errors of seven ... properties"; random 0.8/0.1/0.1 split. Several metrics are reported side by side, so MET-5 gives the fallback (also RMSE) | MET-1, MET-5 |
| metric computable on our folds | MET-2 | dummy score per fold | holds | per row, no scoring columns; mean dummy 95.1-123.7 nm on all 9 folds; 5,450-6,164 test rows per fold | MET-2 |
| metric means the same task as the source's | MET-2 | compare with the source | partly | same target and unit, but scaffold folds instead of random rows; one test fold in three is dominated by the ET(30) dye | MET-2 |
| collection period 1967-2020; issue 3 measurements | assessment 11-21 | - | untested | the split audit's own measurement; not redone | - |
| no feature known only after measurement | implied | feature list | holds | structures and medium only | LEAK |

**Ranked refuted and untested claims**

1. **"Experimental values extracted from spectra" / "fold spread = chemical families"** (Finding 1, validity).
   335 rows are one review's ET(30) solvent scale converted to nm. They carry 14% of the target variance and decide
   3 of the 9 folds. Changes: the curation note, `fit_reason`, and a new decision item. Mildest remedy: document it;
   the curator chooses between keep, drop and cap.
2. **Leak probe untested** (crash on NaN). Rerun it before ship.
3. Low: acid/base forms across groups (Finding 2); the neat-solid wording in `known` (Finding 3, KNOWN); the
   webpage quote (Finding 4).

</details>

<details><summary>Domain practitioner (2026-11-21)</summary>

**Domain practitioner: chromophore_optical_properties_db**

Actor: a synthetic or materials chemist (fluorescent probe, OLED emitter, photocatalyst dye) who screens proposed dye structures before making them. I decide which dyes to make.

**Fit: approximate.** I have both inputs before synthesis and λmax is the number I act on. But the solvent input adds nothing measurable. One dye from a calibration standard holds 1.9% of the rows. Literature selection and unrecorded conditions also remain, as the record already says. I agree with the declared fit (USE-8).

**Metric scores my decision: partly.** RMSE in nm is on the right scale. But 1% of the test rows carry 22% of the squared error, and the rows are not weighted per dye, which is the unit I decide on.

**What I tested**

The panel's run (CPU) ran on the shipped `_clean` frame and the 9 shipped scaffold folds. It measured rows per dye, the spread within and between dyes, and four models plus the training mean. Features were Morgan count fingerprints (r=2, 2048 bits) with 5 RDKit descriptors, and `medium_state` one-hot. Each model was scored by RMSE and MAE, per row and with weight 1/(rows of the dye).
Script, log and per-fold scores are in the panel's run.

| Model (mean of 9 folds) | RMSE | MAE | RMSE, per-dye weight | MAE, per-dye weight | top 1% rows' share of SE | rows within 20 nm |
|---|---|---|---|---|---|---|
| LightGBM, dye + solvent | 53.9 | 33.8 | 44.6 | 31.0 | 0.22 | 0.47 |
| LightGBM, dye only | 54.0 | 34.1 | 44.7 | 31.1 | 0.22 | 0.46 |
| Ridge, dye + solvent | 63.2 | 40.8 | 54.7 | 38.4 | 0.22 | 0.39 |
| kNN-5 Jaccard, dye only | 75.9 | 45.9 | 58.1 | 40.0 | 0.20 | 0.41 |
| Training mean | 106.5 | 82.6 | 109.2 | 84.5 | 0.12 | 0.13 |

Kendall tau of the per-fold ranking of the 4 models, against per-row RMSE: MAE 0.85 (min 0.67), per-dye RMSE 0.93 (min 0.67), per-dye MAE 0.85 (min 0.33).

| Rows per dye | Dyes | Share of rows |
|---|---|---|
| 1 | 3,889 | 22.2% |
| ≥ 2 | 2,609 | 77.8% |
| ≥ 10 | 287 | 23.4% |
| ≥ 20 | 21 | 5.0% |
| ≥ 50 | 1 (Reichardt's betaine dye, 335 rows) | 1.9% |

Spread of the target: total SD 106.2 nm; SD of dye means 108.7 nm; SD within a dye 19.9 nm (median range 10 nm over the 2,609 dyes with several rows).

**The five questions, as the chemist**

1. **Inputs.** I have the dye structure and the solvent or host I plan to use, so both inputs are fair. I would also know the concentration, the temperature and the pH, which matter for ionizable or aggregating dyes. The data has none of them, but I rarely fix them at the screening stage. The extra input I would really bring is a quick TD-DFT number. It is not in the data, and that is fine for this benchmark (USE-6 does not require it).
2. **Target.** The lowest-energy absorption peak in nm is what I act on. It decides the colour, whether the dye matches my laser line (405/488/532/640 nm), and whether it reaches the NIR. I want a number, and a "which window" answer would also do. One risk: the source's "first absorption peak" sometimes looks like a UV band rather than the S0→S1 band. The PRODAN row at 254 nm against 354 nm in chlorobenzene is one case. This is part of the already-settled issue 2 (KNOWN).
3. **Row and test set.** A row is a dye in one medium. I decide once per dye whether to make it, and I usually care about one or two media. The test set holds out new scaffolds while common solvents recur. That is what I face, since I never invent solvents. Whether held-out scaffolds or later papers stand for "my next dye" is issue 3 (see F4).
4. **Would I use it?** As a coarse filter, yes. A typical error of 34 nm MAE is below raw TD-DFT against experiment (MAE about 54-80 nm, Greenman et al. 2022 SI). But only 47% of predictions land within 20 nm, about the shift a chemist tunes with one substituent. So I would use it to sort UV, visible and NIR candidates, not to fine-tune a series. I would trust it more if the error were reported per dye family. I would distrust it on dye classes it has rarely seen, such as metal complexes and very large π-systems.
5. **Metric.** See F2 and F3.

**Findings**

**F1 (NEW). The solvent input carries no measurable signal under the shipped folds, so the task is in effect "dye → λmax".**
- Evidence: LightGBM with dye and solvent scores RMSE 53.9; with the dye alone, 54.0, on the same 9 folds. The spread within a dye (SD 19.9 nm, median range 10 nm) is small against the spread between dyes (SD 108.7 nm).
- Why it matters: `task_summary.question` asks for the peak "in a specified environment". The benchmark scores the dye part and barely the environment part. That is still a real screening task, because I choose the dye first and the solvent later.
- Change: no change to the data. `fit_reason` could add a sentence that solvent effects (about 20 nm SD) are small next to the differences between dyes, so the scores mostly rank dye-structure models (USE-8: write the gap down).
- Rule: USE-8.

**F2 (NEW). Units are unequal, and the notes do not say so; per-dye weighting changes RMSE and the model ranking.**
- Evidence:
  - The median dye has 1 row, 287 dyes have 10 or more (23% of rows), and one dye has 335.
  - That dye is Reichardt's betaine dye, the ET(30) solvent-polarity standard, with λmax 438-1,055 nm (SD 111 nm). Nobody screens it as a candidate: it is a calibration probe whose job is to respond to the solvent. In whichever fold holds it, its 335 rows count 335 times.
  - A paper series of Boc-amino-acid benzoxazole dyes adds about 36 solvents each, with an SD of 2-7 nm.
  - Per-dye RMSE is 44.6 against 53.9 per row. The ranking tau is 0.93 on average and 0.67 at the minimum, and 0.33 at the minimum for per-dye MAE.
- Why it matters: I decide per dye. The solvent rows are a deliberate solvatochromism protocol, not separate dyes to make. MET-17 says to count each unit once when the actor decides once per unit. If the curator keeps the per-row score because a dye in a new medium counts as its own decision, MET-17 still asks the notes to state how unequal the units are and how far one vote per unit moves the ranking. The definition says neither.
- What I did not measure: how much of the 9 nm per-dye gap comes from Reichardt's dye alone.
- Options: (a) `unit_weight` = 1/(rows of the dye), for scoring only, with the source's RMSE named as the original (MET-11, MET-17); or (b) keep per-row RMSE and add the unit-inequality note. As the actor I prefer (a).
- Rule: MET-17, MET-1, MET-11.

**F3 (NEW, inform only). RMSE leans on a tail of literature errors; the field reports MAE.**
- Evidence:
  - On the scaffold folds, the top 1% of rows carry 22% of LightGBM's squared error. These are partly label disagreements of the kind seen in issue 2 (UV band against visible band).
  - Greenman, Green and Gómez-Bombarelli (Chem. Sci. 2022), on this database with scaffold-type splits, report MAE in nm.
  - Joung et al. 2021 report RMSE among several metrics, so MET-5 gives the fallback, and MET-8's fallback is `rmse`.
  - The ranking tau between RMSE and MAE is 0.85 on average and 0.67 at the minimum.
- Why it matters: as a screener, I would pick a model by MAE, or by the share of dyes within about 20-30 nm. A single 100 nm error from a mis-assigned band should not decide my choice of model.
- Change: none required, because the rules give `rmse` here and MAE is not the source's single metric. The note could say that RMSE weights the long tail of literature errors.
- Rule: MET-5, MET-8, MET-1.

**F4 (KNOWN, issue 3). On the split, the actor's side supports the forward split by year (B), under its window conditions.**
- The source's aim is a chemist applying a model trained on the published record to the next dyes reported. A forward split mirrors that: 3.9% of test dyes have a close analogue in training, against 43.9% for a random draw of dyes.
- Under the scaffold folds, 58-65% of test rows have a row of their own paper in training. That is the same-series case: a chemist who has already measured siblings of the test dye, which a public model never holds.
- One caveat from practice: real design is mostly lead optimisation on a known core (BODIPY, coumarin, cyanine). So the forward split is the strict end of what I face, not the typical case. The `Time basis:` line or the README should say that.
- Rule: SPLIT-37, USE-10.

**F5 (KNOWN, column audit).** `task_summary.known` leaves out the neat-solid designation. About 20 OLED-host doped films stay `solvent or host`, and absorption in a film is a different measurement from absorption in solution. I agree with the audit's wording fix. For an OLED chemist, `medium_state` is the most important part of the environment input.

**Sources**

- Joung et al. 2020, Scientific Data 7:295, https://doi.org/10.1038/s41597-020-00634-8 (use case "prior to their synthesis", first absorption peak)
- Joung et al. 2021, JACS Au, https://doi.org/10.1021/jacsau.1c00035 (as summarised in the record)
- Greenman, Green, Gómez-Bombarelli 2022, Chem. Sci. 13:1152, https://doi.org/10.1039/d1sc05677h; PMC8790778 (this database, scaffold-type splits, MAE in nm, TD-DFT vs experiment MAE about 54-80 nm raw, 32-40 nm corrected)
- The record's `## Review` issue 3 answer (2026-11-21) and the column audit the column audit
- Panel probe logs (check.log, leak/, task/) were not present in the panel's run when I read it. Only `precedent/` existed.

</details>

<details><summary>Precedent check (2026-11-21)</summary>

**Precedent check: chromophore_optical_properties_db (2026-11-21)**

**What I did.** I ran the decision register (5,933 decisions, in the panel's run). It raises **0 flags** on this
dataset. I then checked each decision of `dataset.py` and each open issue in the record (issues 1-3, including this
round's issue 3 and its 2026-11-21 answer) against the same rule IDs, the curator decisions on LEAK-18/19/20, MET-17,
SPLIT-26 and SPLIT-37 in other records, the Cases tables (splits.md SPLIT-31/SPLIT-37, metrics.md MET-17, molecules.md)
and the split tree (Expanding science catalogue branch, family-key step ①).
`dataset check` and probe outputs (`check.log`, `leak/`, `task/`, `group.log`) were not in
the panel's run when I looked. Only `precedent/` was there.

**Verdict per decision**

| Decision | Rule | Closest precedents | Verdict |
|---|---|---|---|
| Target: first absorption maximum (nm); other optical outcomes and Reference/Tag leave the inputs | LEAK, USE-1 | the general outcome-as-feature leak cases | consistent |
| Molecular weight leaves (structure-derived); both SMILES ship typed, no curator descriptors | CLEAN-24 | drug_induced_autoimmunity_prediction (RDKit descriptors left), apistox (SMILES typed, 2026-11-01) | consistent |
| Fit `approximate` (literature conditions not recorded) | USE-8 | qsar_oral_toxicity (approximate after the scaffold split) | consistent |
| Metric: fallback RMSE in nm | MET-5, MET-8 | other fallback regressions | consistent |
| Gas rows kept, Solvent_SMILES missing, warning accepted with a CC | check warnings | warning accepted only after a curator CC (house rule) | consistent |
| Scaffold groups; ring-less and >10% scaffolds alone; InChIKey + tautomer merge | SPLIT-31, SPLIT-37 step 1 | qsar_bioconcentration, qsar_oral_toxicity, drug_induced_autoimmunity_prediction | consistent |
| Issue 1: drop 193 equal input+target rows (1A) | LEAK-16/18/19 | qsar_tid_11 (salt copies of one parent dropped, 2026-10-21) vs superconductivity (every entry kept, one vote per composition, 2026-11-08) | departs, with a reason evident from the data (scale) - see finding 1 |
| Issue 2: keep 61 sets / 124 rows with differing wavelengths (2A) | LEAK-20 | superconductivity (132 compositions differing by >30 K kept), qsar_tid_11 (stereoisomers with own values kept) | consistent on keeping; scoring weight see finding 1 |
| Issue 3: scaffold (A) vs first publication year (B) | SPLIT-37, SPLIT-14, SPLIT-36 | apistox, qsar_tid_11 (B-type) vs qsar_biodeg, superconductivity (A-type) | recommendation B consistent - see finding 2 |
| Issue 3 background "no curator decision covered the split" | - | CC 2026-11-09 (Myunghwan) | wording wrong - see finding 3 |

**Findings**

**1. NEW: repeated literature measurements of one input set - per-row RMSE without a unit weight, unlike superconductivity**

- **Precedent.** superconductivity is the nearest pair: a literature compilation, a continuous target, every input fixed
  by the item, repeated entries from several papers that differ for unrecorded conditions. Lennart decided on 2026-11-08
  (issue 1 B; MET-1, MET-17, SPLIT-26): keep every entry and weight the RMSE by 1 over the composition's entries
  (`composition_weight`, scoring only). MET-17 (Should, 2026-11-08) names "the SuperCon entries of a composition" as
  its example.
- **This dataset.** It drops the 193 equal input+target rows (LEAK-19 default) and scores per row. The 61 input sets
  with differing wavelengths (124 rows) each count 2 or more times. Issue 1's options (a) and (b) both leave the
  score per row. Its footnote cites superconductivity only for keeping rows, not for the unit weight decided two days
  before 1A.
- **What sets it apart.** Scale. After deduplication, 61 of about 17,450 input sets have more than one row; one vote per
  set would move about 63 of 17,510 rows' weight (0.4%). In superconductivity, repeated compositions held 40% of the
  rows. The dedup is also backed by qsar_tid_11's dropped salt copies (2026-10-21, Lennart). So the departure is
  reasonable, but its reason is not written down. MET-17 says the notes then say how unequal the units are.
- **Not a Must.** MET-17 and SPLIT-26 are Shoulds; no higher rule is broken.

Reflection prompt (issue shape):

> **Score each dye-environment set once, as superconductivity scores each composition once?**
>
> - **Problem:**
>   - superconductivity (2026-11-08, Lennart) keeps every literature entry and weights the RMSE by 1 over the
>     composition's entries (MET-17); here the 193 equal records leave and the 61 sets with differing wavelengths
>     count once per row.
>   - Issue 1 offered no unit-weight option; the decision rests on LEAK-19 alone.
> - **Options:**
>
>   | | Option | Pro | Con |
>   |---|---|---|---|
>   | a | Keep 1A and per-row RMSE; add a note: 61 sets of 2+ rows, 0.4% of the weight, against 40% of rows in superconductivity | no requalification; the scale sets it apart | a second literature compilation scored differently from the first |
>   | b | Keep 1A, add a `unit_weight` of 1 over the input set's rows (scoring only) | same scoring rule as superconductivity | a weight column for 0.4% of rows |
>   | c | Keep all source rows (undo the 193 drops) and weight per input set | follows superconductivity fully | reverses 1A; requalification |
>
> - **Recommendation:** (a): the effect is too small to change the task, and the note keeps the two datasets
>   comparable.[^met17]
>
> [^met17]: MET-17 (Should): count each unit once when the actor decides once per unit and its further rows are
> repeats. SPLIT-26 (Should): keep the source's rows. LEAK-19 (Should): drop same-label copies by default.

**2. KNOWN (issue 3): first-publication-year windows follow apistox and qsar_tid_11**

- **Walk.** Catalogue branch: the source aims at "newly designed organic chromophores prior to their synthesis", so step 3
  is yes. A dated first report (DOI year) is the entry date apistox (first PubChem article year) and qsar_tid_11 (first
  ChEMBL document year) use. Labels are final. The date carries waves: forward 2014+ leaves 3.9% of test dyes a close
  analogue against 43.9% for a random draw of the same size. That is a stronger wave than both precedents.

  | Dataset | Forward split | Random draw | Decision |
  |---|---|---|---|
  | chromophore (2014+) | 3.9% | 43.9% | open |
  | qsar_tid_11 | 6-30% | 79.7% | windows on first year (2026-11-11) |
  | apistox | 10-24% | 17-30% | decade windows |
  | qsar_oral_toxicity | 12.4% | 13.1% | scaffold kept |
  | qsar_aquatic_toxicity | 2.3% | 2.6% | scaffold kept |

- **Same-paper siblings.** 58.4-64.8% of scaffold-fold test rows have a row of their own paper in training. This is the
  fact that moved qsar_tid_11 off scaffold groups ("kept the test compound's siblings of its own year").
- **Unlike qsar_biodeg and superconductivity.** Both kept the family key because the source limited its question to
  known chemistry or to chemicals from elsewhere (SPLIT-37 step 3). This source states no such limit.
- **The floor.** The condition in the recommendation matches SPLIT-37 step 4: windows that fail SPLIT-14 leave the family
  key standing, not a forced split. A 2014 cut (42.6% train) would need the curator's CC exception (down to 30%), as
  mercedes_benz_greener_manufacturing (31.5%) and ieee_fraud_detection (38.9%). apistox needed none (train 56-95%).
- **Undated rows (2.1%, 98 DOIs).** No rule covers them. The closest precedent is apistox, which keeps every compound and
  dates the undated ones by a fallback (the PubChem record's creation date) rather than dropping them. "Put into the
  earliest training era" is closer to that precedent than "drop".
- **v3 backfill.** v3's added rows are papers of 2020 and earlier, so the DOI year is not when the row entered this
  Figshare file. apistox and qsar_tid_11 accepted literature first-publication years in the same situation, so this is
  consistent. SPLIT-37 step 4's "not a registration that predates it" is about ids like NCI numbers, not paper years.

Verdict: recommendation B (with the floor condition), else A with the shares in the `Time basis:` line, is consistent.
Either way the definition still needs its time basis: today it has no `data_tags` and no `Time basis:` line (SPLIT-32).
That is already in issue 3's notes for the AI.

**3. NEW: issue 3 says no curator decision covered the split, but one did**

- The 2026-11-09 CC (Myunghwan) reads: "Pursue the discussed scaffold-grouped evaluation." Issue 3's Background says
  "no curator decision covered the split (issues 1 and 2 were on weights and conflicting labels)".
- Reopening it is consistent with precedent. qsar_tid_11's scaffold split (Lennart, 2026-11-01) was superseded on
  2026-11-11 when SPLIT-37 arrived. Myunghwan's CC came before SPLIT-37's step 4 existed.
- Fix: the Background should cite the CC and say that the split rule changed after it, so that a change to B is a
  change made on purpose, not drift.

**No finding**

- No drift: Myunghwan has no other decision on LEAK-18/19/20, MET-17 or SPLIT-37 that this one contradicts.
- No third exception of one kind: 1A and 2A use LEAK-19's default and LEAK-20's genuine-ambiguity clause, not
  exceptions.
- The column audit's doc fixes (`known` naming neat solid; OLED-host films stay `solvent or host`) raise no precedent
  question.

</details>

<details><summary>Blind review (2026-11-21)</summary>

**Blind review: chromophore absorption max (Joung et al. 2020, figshare 12045567 v3)**

Verdict: include with changes. The task and data are real and fit for the benchmark, but the features are only SMILES strings, the 335 Reichardt's-dye rows are converted from ET(30) values (one of them extrapolated), and the model baselines have not finished.

**Concerns, most serious first**

1. **The features are only SMILES strings (chromophore, solvent), plus `medium_state` and `scaffold`.** No numeric column exists. A generic tabular method treats 6,498 chromophore strings as a high-cardinality categorical. Every test chromophore is unseen, because the split holds out whole scaffolds. So without molecular featurisation the task mostly measures whether a method can parse strings. Change: say so explicitly, or ship standard descriptors or fingerprints. My baselines (string-count features vs RDKit descriptors + Morgan fingerprints, LightGBM, scaffold GroupKFold) are in the panel's run. They had not finished when I reported (the job later crashed).
2. **335 rows (1.9%) come from Reichardt's dye, all from one review** (doi 10.1021/cr00032a005). These rows are not spectra read by the curators: the values are 28591/ET(30). For example, 1055.018 nm is ET(30) = 27.1 kcal/mol, an extrapolated gas-phase estimate, not a measurement. 334 of the 1,697 non-integer targets come from this source. Because it is one scaffold group, a whole fold must predict a 437–1055 nm range for one molecule never seen, which dominates RMSE. Change: drop the extrapolated gas row and note the conversion. Consider capping rows per chromophore or reporting results with and without this group.
3. **`medium_state` = "solvent or host" merges solutions with doped solid films** (OLED hosts such as CBP, mCP and DPEPO in the solvent column; about 350 rows have solvent SMILES over 40 characters). The paper: "for chromophores in a solid matrix, the solid matrix is used as the solvent". Change: add a separate "solid host" state.
4. **The gas-phase rows (20) are out of scope**: alkanes at 128–143 nm (vacuum UV), Cl2, Br2 and BrCl. The paper says outliers below 200 nm were only double-checked. Minor; I would drop them or keep them knowingly.
5. **Label noise from repeated measurements**: 61 (chromophore, solvent) pairs carry 2–3 differing literature values (median SD 2.5 nm, max SD 71 nm). Exact source duplicates (about 190 rows) were removed correctly. Each such pair falls in one scaffold group, so this does not leak.

**Checked and fine**

- The data are real, manually extracted from 1,358 papers and cross-checked by a third person (Sci Data 2020, CC BY 4.0). The target matches the source column "Absorption max (nm)".
- Prepared vs source: 17,703 source rows have absorption; 17,510 are kept. The drop is exact duplicates plus some metal-complex SMILES rewritten ([n], [Zn+2]). No other columns from the source (emission, which correlates 0.86 with absorption, lifetime, extinction coefficient, reference) leak into the table.
- Copies across scaffold groups: by InChIKey, only 1 full-key molecule (5 by first block) spans more than one scaffold group, 19–62 rows, mostly organometallic SMILES variants. Negligible.
- Use case: predicting the first absorption maximum of a designed dye in a given solvent before synthesis, as a cheaper alternative to TD-DFT (the paper's stated purpose). The scaffold split stands for new chemotypes, which is reasonable and a little harsh. No column is unknown at prediction time. There is no weight column.
- Sensible size (17.5k rows, 3,335 scaffold groups) with plausible values except the points above.

**Not checked**

- Baseline numbers: the baseline job was running at report time. Read its results, both subsets (all rows / no Reichardt), for: mean, solvent mean, LightGBM on string features, LightGBM on RDKit, and a 1-NN Tanimoto model.
- Whether all solvent SMILES are canonical in one convention.
- I spot-checked no individual values against the original papers.

**Addendum: baselines (rerun; the first run crashed on feature names)**

Scaffold-grouped 3-fold CV, 3 repeats; mean ± SD over the 9 folds.

| Model | RMSE, all rows | R², all rows | RMSE, without Reichardt | R², without Reichardt |
|---|---|---|---|---|
| Overall mean | 106.2 ± 8.9 | -0.01 | 99.3 ± 2.4 | -0.01 |
| Per-solvent mean | 106.3 ± 9.3 | -0.01 | 99.0 ± 2.3 | 0.00 |
| 1-NN Tanimoto | 72.6 ± 16.6 | 0.53 ± 0.14 | 61.2 ± 3.9 | 0.62 ± 0.05 |
| LightGBM, string counts | 65.4 ± 20.7 | 0.61 ± 0.19 | 53.2 ± 2.6 | 0.71 ± 0.04 |
| LightGBM, RDKit + Morgan | 53.9 ± 20.6 | 0.73 ± 0.16 | 41.2 ± 1.9 | 0.83 ± 0.02 |

- There is real signal, and the task is not trivial. Solvent alone explains nothing, so the target is driven by the chromophore.
- Molecular features beat crude string counts by about 12 nm RMSE, so the SMILES-only format matters for a tabular benchmark (concern 1).
- The single Reichardt's-dye group multiplies the fold-to-fold SD of RMSE about eightfold, from about 2 to about 21 nm (concern 2).
- In 14% of test chromophores the nearest training chromophore has Tanimoto similarity above 0.8 (median nearest similarity 0.59). The scaffold split still leaves close analogues in training. That is normal for this kind of split and is not a copy.

</details>

<details><summary>Task gamer (2026-11-21)</summary>

**Task gamer report: chromophore absorption max (grouped by scaffold, RMSE)**

**Verdict:** I found no exploit inside the kit. Every format, order, copy, transductive and lookup attack stays within the random-column noise of an untuned LightGBM, or does worse. The task's real weakness is in how it is scored. One dye, Reichardt's betaine 30, has 335 rows (1.9% of the table) whose labels are back-calculated from the ET(30) solvent-polarity table. In the 3 of 9 splits where it is in test, it causes 57–68% of the squared error.

Baseline: LightGBM with default settings (`n_jobs=2`) on Morgan count fingerprints (radius 2, 2048 bits for the chromophore, 256 for the solvent) plus one-hot `medium_state`. Scripts and results (features, attacks, per-group errors) are in the panel's run. Noise check: refitting with a random column added moves RMSE by 0.06–0.97 per split (median about 0.4).

Per split RMSE (r0f0 … r2f2):

| Model | r0f0 | r0f1 | r0f2 | r1f0 | r1f1 | r1f2 | r2f0 | r2f1 | r2f2 |
|---|---|---|---|---|---|---|---|---|---|
| train mean | 99.3 | 122.9 | 97.6 | 98.9 | 99.2 | 120.7 | 123.7 | 101.0 | 95.1 |
| baseline | 43.7 | 79.1 | 47.7 | 49.2 | 47.7 | 75.3 | 72.2 | 48.4 | 39.7 |
| baseline + random column (3 seeds, range) | 43.6–43.9 | 79.0–79.6 | 47.3–47.8 | 48.8–49.2 | 47.5–47.8 | 74.8–75.8 | 71.3–72.2 | 48.4–48.5 | 39.7–39.8 |

**Exploits, ranked by gain**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| – | None beat the noise band | run.py | 39.7–79.1 | – | – | – | – |
| (unranked) | Look up Reichardt's dye labels in the public ET(30) table (λ = 28591 / ET(30)) | groups.py (upper bound) | 79.1 / 75.3 / 72.2 | about 47.4 / 43.0 / 47.7 if those rows were exact | −25 to −32 on 3 splits | It is a lookup of published values. The circularity is real, though: ET(30) is a standard solvent descriptor, and this dye's label *is* ET(30). | Cap or drop the dye (see below) |

**A flaw that distorts the score (not an exploit, but the largest effect found)**

| What is wrong | Honest choice | Score as shipped | Score on the other rows | Fix |
|---|---|---|---|---|
| Reichardt's betaine 30 (`[O-]c1c(-c2ccccc2)cc(-[n+]2…)`) has 335 rows, one per solvent, with labels from 438 to 1055 nm. Its labels are converted from ET(30) values: 334 of 335 are non-integer, and 99.7% give ET(30) to exactly one decimal (kcal/mol). | Nothing a model can do. The dye's scaffold is unique, so it is always unseen, and the baseline's RMSE on it is 224–259 nm. | 79.1 / 75.3 / 72.2 (splits r0f1, r1f2, r2f0) | 49.0 / 44.1 / 49.0 | Keep the dye in at most a few solvents, or drop it. It is a solvent-polarity scale, not a dye-design example. Weighting the score per dye would also work. |

- **Mechanism:** the split holds out whole scaffolds and the score is RMSE per row. A single molecule therefore makes up 335 test rows and 57% / 68% / 57% of the squared error in its three splits. This decides the spread between splits (40–49 versus 72–79) and drowns out the differences between models in a third of the splits. Its labels are not read from spectra: they are back-computed from a solvatochromic polarity table.
- **Opposite-direction check (does the dye hurt honest training?):** dropping its 335 rows from training changes RMSE on the other test rows by −1.2 to +0.2 (median −0.4) in the 6 splits where it is in training. That is about the size of the noise band, so the effect is weak at most. Weighting training rows 1/(rows per dye) gives 43.0 / 47.2 / 48.5 / 47.2 / 47.9 / 40.0 against 43.7 / 47.7 / 49.2 / 47.7 / 48.4 / 39.7 on those splits, also within noise, and it is worse on the three Reichardt splits.

**Attacks that found nothing**

| Attack | Result |
|---|---|
| **Formats.** Every chromophore SMILES is already RDKit-canonical (17,510 / 17,510), and so is every solvent SMILES that is present. There is no writing-style signal. Features tried: length, aromatic share, stereo `@`, E/Z marks, isotopes, bracket atoms, explicit H, charges, Kekulé form, canonical flag, missing solvent. | Alone: 66–93, against the mean's 95–123. That signal is chemistry (size, conjugation, charge), not recording style. Added to the baseline: 44.1 / 86.3 / 45.4 / 49.1 / 45.5 / 76.2 / 72.7 / 48.8 / 40.2, mixed (−2.2 to +7.2), with no consistent gain. |
| Target precision. 1,690 labels are non-integer; 334 of them are Reichardt rows and the rest are mostly eV or cm⁻¹ conversions. | It is the label, not a feature, so there is no route to the score. |
| **Order and ids.** | Lag-1 autocorrelation of the label in row order: −0.01. Same chromophore in the next row: 0.05%. Rows are shuffled and there are no ids. |
| **Copies across the split.** Recomputed Murcko scaffold, stereo- and isotope-stripped molecule, InChIKey skeleton. | 0% of test rows have their recomputed scaffold in training, and 0 stereo-stripped molecules cross groups. 0–25 test rows per split share an InChIKey skeleton with training rows, but they are other protonation states: phenol vs phenolate merocyanine, which differ by up to 200 nm, and ammonium vs amine. Copying the training label is worse: 48.4 vs 47.7 and 40.6 vs 39.7. |
| **Nearest training neighbour (Tanimoto).** 94–150 test rows per split have a training chromophore with Tanimoto 1 on Morgan bits, and 284–380 have one at ≥ 0.9. | 1-NN label alone: 56–68 on normal splits and 125–128 on Reichardt splits. As a feature: 42.6 / 100.2 / 44.8 / 45.4 / 44.6 / 83.4 / 92.1 / 48.7 / 41.5. It gains 1–4 on four splits and loses 0.3–21 on four others. This is legitimate signal (a deployed model has its training set), not a leak. |
| **Test-set composition.** Rows per chromophore and per scaffold, counted over train and test together. | 44.1 / 82.2 / 48.4 / 49.3 / 47.3 / 76.4 / 72.2 / 48.4 / 39.7: no gain, and worse on r0f1. |
| **Columns from after the prediction point.** | The features are only the chromophore SMILES, the solvent SMILES and `medium_state`. Emission, lifetime, quantum yield, ε and the DOI from the source were all dropped. For neat solids the solvent equals the chromophore (as documented), and gas rows have no solvent. Nothing is post-outcome. |
| **Transforms over all rows; weight; time.** | None exist: raw strings, no weight, no time column. |
| **Training-label cleaning.** Drop training rows more than 100 nm from their dye's median when the dye has ≥ 3 rows (10–147 rows). | 43.4 / 80.6 / 47.4 / 49.2 / 48.1 / 75.3 / 72.9 / 47.8 / 39.7, within noise. |
| **Web.** | No leak, "magic feature" or competition threads exist for this dataset. The paper (Joung et al., Sci. Data 2020) describes double extraction from 1,358 papers plus a cross-check. Looking rows up in the figshare CSV works trivially, since it holds the same values; not ranked. |

**Kit compared with the published file (figshare v3, `DB for chromophore_Sci_Data_rev03.csv`)**

| Change | Rows |
|---|---|
| Source rows with an absorption value | 17,703 |
| Kit rows | 17,510 |
| Exact duplicate rows dropped | 193 |
| Source rows not in the kit | 48 |
| Gas rows kept, solvent set to missing | 20 |
| Non-identical repeats of the same (dye, solvent) pair left in, all within one group | 61 pairs |

- The 48 source rows missing from the kit are mostly metal complexes written with dative bonds (Ru, Zn).
- 99.7% of kit rows match a source row exactly.
- The `Reference` (DOI) column was dropped. 70% of rows come from papers whose dyes span more than one scaffold group, so paper and lab effects cross the split. No feature in the kit carries the paper, though, so it cannot be exploited here.

**Not checked**

- Whether a split grouped by source paper would score differently. It is a design question rather than an exploit, and it would need the DOI from the source.
- Rebuilding ET(30) per solvent from the training folds to set this dye's test labels. Those labels are hidden whenever the dye is in test, so the only route is the external ET(30) table, which is a source lookup.
- A tuned or larger model. All numbers are untuned LightGBM.

Sources: [paper (Sci. Data 2020)](https://www.nature.com/articles/s41597-020-00634-8), [figshare dataset](https://doi.org/10.6084/m9.figshare.12045567.v3)

</details>

<details><summary>Column audit (2026-11-21)</summary>

**chromophore column audit — built; no new issue; issue 3 measured (answer written); collection_period 1967-2020 set**
Doc fixes: task_summary.known -> "The dye structure and the solvent or host structure, or the source's neat-solid or gas-state designation."; curation note: ~20 OLED-host doped films stay `solvent or host`; optional: gas rows 1967-2006 papers, one gas row at 1,055 nm unverified.

</details>

<details><summary>Column and source audit</summary>

**Version note:** This original report predates the metric-origin correction and final tautomer repair; its source-origin interpretation and earlier identity status are historical. Final claim/split rechecks and mediation below describe the implemented fallback and repaired groups.

**Chromophore source and column audit**

Observed: 2026-11-10 UTC. Role: independent source/column auditor for the authorized add-dataset stage. No canonical definition, curation record, raw data, Git commit, build or publication was changed by this auditor. This report audits the current proposed definition, not an accepted benchmark release.

**Judgment**

The first-absorption-peak regression task is supported by the original data descriptor and a concrete premeasurement use. All 14 raw columns have an accounted role. The minimal supported inputs are the dye structure, medium structure where one exists, and the source's known medium state. Other measured optical outcomes are unavailable at this prediction point; the raw index, reference DOI and structure-derived weight leave the predictors. Canonical SMILES should ship as typed structures (USE-1/3, CLEAN-3/24).

Two findings require explicit treatment: same-InChI dye aliases can cross ordinary scaffold groups, and conflicting repeated wavelength observations cannot be certified as harmless measurement variation. Joining scaffold components by valid InChI identity resolves the first. Retaining different reported wavelengths under those groups is a defensible LEAK-20 judgment about observational response ambiguity, provided its inferential basis and unresolved source-error possibility remain explicit. Averaging, choosing a preferred value by its magnitude, or discarding an extreme solely because it is extreme is unsupported.

**Source identity and primary evidence**

The local v3 artifact is the publisher's Figshare file 49887156, DOI `10.6084/m9.figshare.12045567.v3`, MD5 `565dbb010480d94e8bb41af1bfb75ea8`, SHA256 `f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c`. Acquisition and CC BY 4.0 metadata are in the retained qualification evidence and `figshare-metadata-via-gpu.json`. I independently recomputed the raw SHA256. Local v2, separately downloaded by the parent, has the publisher MD5 `6619ca296ebbf14e8c80dda084b43ac5` in `figshare-v2-metadata.json`.

The [Scientific Data descriptor](https://www.nature.com/articles/s41597-020-00634-8), Methods, states: "the first absorption peak was selected". It describes literature-extracted experimental spectra, SMILES for structures, same dye and medium for neat solids, and a host structure for solid matrices. Data Records/Table 1 define the fields and missing values; the paper links v2. Its published 20,236-row scope and 150-heavy-atom restriction do not exactly describe v3. These are source claims, checked below against the actual release. No source correction log was recovered. The origin of each individual conflicting record was not verified from its own cited article.

The [JACS Au follow-up](https://pubs.acs.org/doi/10.1021/jacsau.1c00035), Methods, Training Our DL Model, explicitly defines the loss as "the total mean squared error" over normalized properties. Its performance comparisons use RMSE in wavelength units. This supports `rmse` on untransformed nm as source-origin metric (MET-1/3/5/11), beyond an abstract-only headline. Its 30,094-pair database and random 80:10:10 split differ from this task; the reported 26.6 nm is not a qualification result for our v3 grouped split. The paper cites Figshare v2 and describes presynthesis virtual screening, supporting the prediction point.

Publisher and PMC primary text were read through indexed web results because direct publisher/PMC opens encountered redirects or browser checks. Source-location gaps above remain explicit. No GPU inquiry or transfer was performed by this auditor.

**All-column audit**

Nonmissing counts below are measured on all 20,836 v3 raw rows, before filtering to the absorption task. The semantic interpretation uses raw headings, source Table 1 and spectroscopy context. "After measurement" means unavailable under the approved task, not that measuring these values is impossible in every different use case.

| Raw column | Nonmissing | Meaning / representation / timing | Supported treatment |
|---|---:|---|---|
| `Tag` | 20,836 | Sequential integer 0 through 20,835; storage row numbering, not a stable identity across versions | Drop predictor; retain raw lineage in audit artifacts |
| `Chromophore` | 20,836 | Molecular graph in SMILES, specified before synthesis/measurement | Keep canonical full SMILES as typed structure, including charge, isotopes and source stereo |
| `Solvent` | 20,836 | SMILES for solvent or solid host; same as dye denotes neat material; literal `gas` is a physical-state code | Keep valid medium structures; decode gas separately with missing medium structure; retain coarse solvent-or-host uncertainty |
| `Absorption max (nm)` | 17,703 | First absorption-peak wavelength, numeric nm, obtained by spectroscopy | Target; drop 3,133 missing-target rows; no log or wavelength-to-energy conversion |
| `Emission max (nm)` | 18,851 | Emission-peak wavelength in nm, another measured optical outcome | Drop predictor for this premeasurement task |
| `Lifetime (ns)` | 6,949 | Excited-state/fluorescence decay lifetime in ns; measured outcome | Drop predictor |
| `Quantum yield` | 13,978 | Photoluminescence quantum yield, dimensionless measured fraction | Drop predictor |
| `log(e/mol-1 dm3 cm-1)` | 8,300 | Logarithm of molar extinction coefficient in the stated units, measured optical outcome | Drop predictor; avoid reading the letter `e` as a free numeric covariate |
| `abs FWHM (cm-1)` | 6,953 | Absorption bandwidth in inverse centimetres; measured from the absorption spectrum | Drop predictor; same spectrum used to obtain target |
| `emi FWHM (cm-1)` | 11,325 | Emission bandwidth in inverse centimetres; measured outcome | Drop predictor |
| `abs FWHM (nm)` | 6,972 | Absorption bandwidth in wavelength units; partly alternate representation of the preceding absorption bandwidth | Drop predictor; no need to resolve all cross-unit conversions for a discarded field |
| `emi FWHM (nm)` | 11,404 | Emission bandwidth in wavelength units; partly alternate representation of preceding emission bandwidth | Drop predictor |
| `Molecular weight (g mol-1)` | 20,836 | Numeric structure-related mass; 19,830 rows exactly match RDKit exact molecular mass to 1e-6; 1,006 do not, consistent with mixed source/calculation conventions rather than one uniform mass definition | Drop as source structure-derived feature under CLEAN-24; no invented mass repair required |
| `Reference` | 20,836 | Source-publication DOI text, 1,354 unique raw values; provenance recorded after literature compilation | Drop predictor; keep raw source evidence and row-level audit tables |

The proposed `medium_state` is a deterministic decoding of existing information, not learned from labels. The raw field does not identify every liquid/solid host phase, concentration, temperature, pH or preparation condition. The chosen words `solvent or host` are appropriately bounded. A mandatory solvent input is not absent in gas: there is physically no solvent molecule; missing structure plus a known gas state preserves that setting rather than inventing a dummy molecule (USE-7, CLEAN-10/12/24).

**Measured support and representations**

The 17,703 finite positive labels span 127.7 to 1,055.01845 nm (median 397; mean 427.806; standard deviation 106.382). They cover 6,498 distinct canonical dye structures and 1,294 raw reference strings. After removing 193 exact canonical input/target copies, the proposed task has 17,510 rows. This is row support, not 17,510 independent chemical entities.

RDKit 2026.03.6 parses all 6,865 raw unique dyes. Canonical and stereo-free dye keys are each 6,865 unique; thus no two v3 dye strings collapse solely through canonicalization/stereo removal. Both raw molecular fields contain zero disconnected structures, so no salt stripping or largest-fragment reduction is supported or needed. All 1,363 distinct raw media parse except `gas` (20 rows, all labeled). Dye and medium canonical structures are equal in 983 raw rows, 369 of them labeled. These support the source's neat-solid decoding.

The source release also contains methane, ethane, diatomic halogens, metal complexes and dyes with up to 225 heavy atoms. These diverge from the historical descriptor's organic/150-atom scope. Their presence is an observation, not proof of contamination or permission to invent an organic-only filter. No general scope filter is justified without a source repair or a changed user task. It is more accurate to describe the retained population as source chromophores/materials than to imply every retained row is a conventional organic dye.

The raw source has 3,524 distinct unadjusted dye scaffolds; the labeled population has 3,305, with 51 ringless rows. The most common labeled raw scaffold is benzene (399 rows), well below 10% of labeled rows. The definition correctly measures fallback frequency on distinct dye structures rather than repeated solvent observations. Actual Data Foundry groups are a separate result from these raw scaffold counts.

Valid InChIKeys detect additional identities that simple canonical strings miss. In the labeled set, 9 nonempty shared keys cover 18 distinct dye strings; 8 keys cross two ordinary `scaffold_groups` groups and the tyrosine neutral/zwitterion pair already shares one. This is label-independent evidence for joining connected scaffold components. Thirteen labeled unique metal-complex dyes yield an empty InChI; they must use their own canonical key, never a shared empty identifier. Whole raw data have 11 nonempty repeated keys covering 22 structures. InChI aliasing can reflect proton movement or aromatic/bond representation, so preserve all shipped structures while grouping identities conservatively; do not neutralize or deduplicate chemically meaningful states solely on this key.

**Duplicates and unresolved disagreement**

Among labeled rows, 251 canonical dye/medium pairs recur, covering 507 rows and 256 excess observations. There are 193 exact pair/target excess rows; 61 pairs have different wavelengths (126 raw rows; 63 excess observations after pair/target deduplication). Their range differences span 0.5 to 100 nm, median 3.5. Sixty conflict groups cite multiple references; one has only a single raw reference.

The single-reference case is tags 2007 and 4345: the same benzothiazole derivative in cyclohexane has 387 and 384 nm, reference `10.1016/j.jphotochem.2019.03.021`; both have 427 nm emission. The 100 nm difference is tags 88/13492, the same Prodan-like structure in chlorobenzene at 254/354 nm from `10.1021/bi00581a025` and `10.1016/j.jphotochem.2012.04.011`. Tags 10/932/15245 give 373/435/376 nm for the same coumarin structure in ethanol, from three references. These examples justify retaining an explicit unresolved transcription/peak-selection risk; disagreement is not automatically genuine experimental noise.

Minimal proposed treatment: drop exact model-input/target copies under LEAK-19, retain distinct observed wavelengths without averaging, and keep every chemical identity in one scaffold component under LEAK-17. The LEAK-20 retention relies on the plausible real ambiguity of measurements compiled from heterogeneous papers, but the individual conflicts remain unverified. This is a scientific judgment with a known limitation, not a purely mechanical cleaning fact. If a cited origin later establishes an erroneous row, repair that row from the source under PROV-13 rather than selecting values by agreement with a model. Since no public repair list was found, blanket conflict deletion is not demonstrated to be more faithful.

**Version comparison without treating Tag as identity**

`compare_versions.py` compares multisets of content tuples and target sets by structures, not row number. v2 has 20,236 rows and 17,295 labels; v3 has 20,836 rows and 17,703 labels with the same 14 headings. v2 Tag begins at 1 while v3 begins at 0. Raw dye strings number 6,815 and 6,865 respectively; neither is the paper's historical 7,016 unique count.

Only 1,006 full 13-column rows, excluding Tag, match exactly across versions. Canonical structures plus normalized DOI spelling still leave 1,006 full-row matches; removing molecular weight increases matches to 3,905. These whole-table comparisons are sensitive to changed derived mass, widths and numeric precision; they do not demonstrate thousands of changed target measurements.

For labeled canonical stereo-aware `(dye, medium, wavelength)` tuples, the multiset intersection is 12,029 rows, with 5,266 v2-only and 5,674 v3-only. There are 12,655 shared unique canonical pairs, and 834 shared pairs have different target sets. For 747 of those 834, the sets agree after rounding values to 0.1 nm; 87 do not. In contrast, the stereo-free labeled `(dye, medium)` multiset intersection is 17,098 rows, with only 197 v2-only and 605 v3-only. Thus most large stereo-aware tuple differences arise from structural/stereo representation revisions, with many shared-label changes explained by numeric precision. There remain genuine unmatched tuples and unverified changed target values. Do not describe v3 as simply 600 appended observations, or equate every unmatched stereo-aware tuple with a new compound.

Both versions are primary publisher releases and v3 is a reasonable byte-pinned choice; a complete author change log and source-level correction rationale are still missing. The retained metadata must distinguish actual v3 counts from historical paper counts. Full tuple-delta CSVs and `shared_pairs_changed_targets.csv` allow later source-level investigation.

**Definition review and limits**

I read the retained qualification evidence while the parent was revising it. Its full-column treatments, gas decoding, untransformed target, source RMSE and distinct-dye scaffold weighting are supported. I sent the InChI cross-group finding and recommended softening its original claim that conflicts "are genuine response ambiguity". The parent reports incorporating both corrections. The final exact file must still be checked with the complete add-stage tests and remaining independent roles; this audit is not a substitute for those checks.

The task's approximate fit is warranted by literature selection and unrecorded conditions. No individual conflicting reference, phase metadata beyond source coding, full original spectra, or expanded 30,094-pair training file was reconstructed. No fitting or qualification experiment was performed here.

The audit compared source records, structure identities, conflicting responses, target extremes and chemical aliases. Its quantitative findings are reported below.


</details>

<details><summary>Claim audit: original and final recheck</summary>

**Historical initial audit; the final recheck below supersedes findings corrected in the definition.**

**Independent claim audit — chromophore_optical_properties_db**

Audit captured 2026-11-10 against the reviewed definition, source and participant inputs. No learners were fitted. The completed check treats unavailable InChIKeys as unavailable identities rather than one shared empty identity.

**Report Outcome:** one actionable metric-provenance finding, no independently established data-validity failure. Keep the numerical RMSE scoring. Recommend fallback origin unless a further source passage establishes a unique deliberate per-target model-selection criterion. This recommendation does not decide inclusion. The root's later split repair is outside this captured release: this report does not claim its fold measurements qualify the repaired version.

**Finding 1 — source-origin RMSE is stronger than the inspected source supports**

The active definition declares `Metric.source("rmse")`, citing Joung et al. (2021). The paper's Methods, “Training Our DL Model”, explicitly describes a loss obtained by “summing the mean squared errors of seven optical and photophysical properties with the same weight.” Its properties are standardized before that loss. RMSE is reported in nm, while Pearson correlation squared is also reported. Hyperparameters use training/validation sets. This supports a squared-error training family and a reported per-property RMSE; it does not establish that raw-nm absorption RMSE uniquely ranks/selects the models for this single-target task. [Primary paper](https://pubs.acs.org/doi/10.1021/jacsau.1c00035).

MET-5 requires one deliberate choice rather than merely a headline/reporting metric. Taking a square root and undoing a fixed affine scale preserve ordering **within one target**, but selecting by a sum over seven targets can trade absorption error against other targets. It is therefore insufficient to infer this task's unique criterion from the multivariate loss. MET-1, MET-5, MET-8, MET-11 and EV-2 apply. This is a provenance/justification correction, not evidence against RMSE, not an alternative metric recommendation, and not a reason to exclude the dataset.

**Smallest remedy:** use `Metric.fallback` with a reason saying the 2020 data descriptor defines no predictive model-selection protocol located in this audit, and the follow-up reports RMSE and correlation with a joint standardized multitarget objective; retain RMSE on untransformed nm. Alternatively retain source origin only after citing a passage proving that absorption RMSE, or an order-equivalent single-target quantity, was the deliberate model-selection criterion. The mediator/curator can weigh the stricter interpretation; this auditor has not changed the definition.

**Evidence and source-access limits**

`audit_claims.py` independently loads the SHA-pinned CSV and current `_clean`, verifies structures, identities, duplicates, target scale, feature exposure, and all participant-kit folds. `audit-results.json` is its complete measured evidence; `conflicting-inputs.csv` records the feature sets with multiple observed targets. Fold constants are training-side means, used only to test scoring computability.

For [the 2020 paper](https://www.nature.com/articles/s41597-020-00634-8), inspected primary indexed Methods, Data Records, Table 1, Technical Validation, and Background & Summary support the literature origin, target meaning and proposed pre-synthesis use. Its description covers one-component solids and dopant/host systems, with two independent extractions and a third-person cross-check. These statements are source assertions about collection, not an independent re-extraction of 1,358 publications.

The primary 2021 Methods and results were read as indexed full text. Direct full-text and supplementary-file retrieval was incomplete; no full PDF or supplementary file was downloaded. Missing details remain unverified, including target-scale and source-origin cautions.


**Claims table**

“Holds” means the stated bounded test supports the claim. It does not establish all possible chemical aliases, future applicability, independence of publications, or complete absence of leakage. “Untested” is a limitation/question, not a finding. Historical statements are evaluated in their stated version/date; superseded screening facts are not demands to rewrite preserved history.

Evidence keys: **D** = active definition; **R** = generated README; **C** = curation record; **M** = saved Figshare v3/v2 metadata and download receipt; **A** = this audit's JSON/script; **P20/P21** = primary papers and sections described above. Full local paths and SHA256s are in A.

| ID | Claim and location | Actual test/evidence | Verdict | Rules |
|---|---|---|---|---|
| 1 | D/R: source is the publisher's Figshare v3 CSV, file 49887156 | A hashes/size independently equal M: 3,213,377 bytes, MD5 `565dbb010480d94e8bb41af1bfb75ea8`, SHA256 `f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c` | holds | PROV-1, EV-2 |
| 2 | D/R: license CC BY 4.0 | Read M v3 license identity; no independent legal interpretation | holds | PROV-1, EV-4 |
| 3 | D/R: year 2020; Joung et al. Scientific Data 7:295 | P20 bibliographic metadata matches supplied citation; release version distinguished from first publication | holds | PROV-8, PROV-9 |
| 4 | D/R: 20,836 raw rows; 17,703 nonmissing absorption labels | Fresh CSV counts in A | holds | EV-1, EV-2 |
| 5 | D/R: all observed absorption values positive and finite | A checks all 17,703, range 127.7–1055.01845 nm | holds | PROV-3, MET-3 |
| 6 | D task question/predicted/row: literature measurement of first absorption peak, in nm | P20 target description; exact raw target column; A confirms no log/energy conversion | holds | USE-1, MET-3 |
| 7 | D task use: screen proposed dye/environment before synthesis/measurement | P20 Background & Summary and P21 Conclusions support that intended use; actual prospective utility is not measured here | holds, as intended use | USE-1, EV-2 |
| 8 | D known: two structures or gas designation can be supplied at design time | Inspect frame/code: predictors are only chromophore, environment structure and deterministic medium category; timing follows design input semantics | holds | USE-1, LEAK-1 |
| 9 | D fit approximate: missing conditions and literature selection limit transport | A confirms no temperature/concentration/independent phase columns; transport itself was not prospectively tested | holds for documented limitation | USE-8, EV-6 |
| 10 | D changes: single absorption target, other outcomes omitted | Compare raw schema to clean/kit columns | holds | LEAK-10, MET-2 |
| 11 | D/R: emission, widths, quantum yield, lifetime, extinction are outcomes not available pre-measurement | Their documented meanings and the declared prediction point; all absent from model inputs | holds | USE-1, LEAK-10 |
| 12 | D/R: Tag is row numbering and Reference provenance, removed | P20 Table 1; A: 20,836 unique tags. Tags need not equal this CSV's 1-based position; neither field is shipped | holds | PROV-16, LEAK-1 |
| 13 | D/R: molecular weight omitted as structure-derived rather than required independent experiment | Code/frame exclusion and its deterministic structural interpretation; no claim of necessity to drop it | holds | CLEAN-1 |
| 14 | D/R: two typed canonical SMILES ship, not curator-selected descriptors | Inspect `special_features` and kit inputs; A all 6,498 dyes and all nonmissing solvents parse; all dye strings canonical | holds | CLEAN-24 |
| 15 | D/R: fragments/stereo are kept in canonicalization | Read canonicalization call with default stereo enabled; no fragment stripping in `_clean`; no chemical-equivalence proof beyond RDKit semantics | holds | CLEAN-24, EV-6 |
| 16 | D/R: gas is an observed source token, not failed solvent parsing | Raw count is exactly 20 labelled gas rows; all retained with missing solvent and gas category | holds | CLEAN-1, USE-8 |
| 17 | D/R: equal dye/environment structure denotes neat solid | A confirms exactly 369 retained equal-structure rows assigned this label; P20 covers single-component solids but inspected text does not explicitly define this encoding convention for every v3 row | untested semantic mapping | PROV-16, EV-6 |
| 18 | D/R: other environment structures may be solvent or host, without independent phase detail | P20 Methods describes host systems; raw schema lacks phase; code deliberately retains ambiguous `solvent or host` | holds | USE-8, CLEAN-1 |
| 19 | D/R: exact input-target repeats removed after canonicalization | A independently runs `_clean`: 193 of 17,703 labels removed, 17,510 remain; zero exact model-input/target duplicates | holds | CLEAN-1, EV-2 |
| 20 | D/R: differing targets for a dye/environment remain separate measurements | A: 61 feature sets, 124 participating rows carry multiple targets; greatest range 100 nm. README's 63 is redundant conflicting rows after the first per input, consistent with 124−61 | holds | USE-5, EV-2 |
| 21 | D/R: conflict causes may be conditions or literature/transcription disagreement; unverified | This audit confirms differing observed values, not causes. Definition already says cause is unverified and avoids averaging/conflict filtering | holds as uncertainty disclosure | EV-6, CLEAN-1 |
| 22 | D/R: no row removed just for extreme wavelength | Read filters (nonmissing and exact dedup only); raw and clean extrema retained | holds | PROV-13, CLEAN-1 |
| 23 | D/R: every environment of one dye is grouped together | A: no stereo or nonstereo canonical dye crosses groups or any of nine kit splits | holds on tested keys | SPLIT-24, SPLIT-31 |
| 24 | D/R: grouping counts distinct nonstereo dyes rather than measurement repetitions | Read `key.unique()` input to scaffold helper; A confirms 6,498 distinct nonstereo dye keys | holds | SPLIT-31 |
| 25 | D/R: ringless and oversized scaffolds fall back to individual dye identity | Read active helper's empty-scaffold / share>0.1 rule and its distinct-dye input; no targets used | holds | SPLIT-31 |
| 26 | D/R: same dye InChIKey merges scaffold groups | A: zero available InChIKey identities in multiple groups; 13 structures lack a key and use structure fallback, not a shared empty key | holds on available keys | SPLIT-24, EV-6 |
| 27 | D/R: grouping keeps tautomer/resonance aliases together, broadly read | No exhaustive tautomer enumerator was run in this audit. Same InChIKey tests alone do not prove every tautomer is recognized; root reports an independent split-auditor repair underway | untested broader assertion; recheck required after repair | SPLIT-24, EV-6 |
| 28 | D/R split: solvent/host can recur; tests unseen dye families, not unseen solvents or complete novelty | A: 65–103 solvent structures recur per fold, zero exact scaffold/dye key overlap. New-family framing is bounded by documented scaffold fallback/analogue caveat | holds, bounded | SPLIT-1, SPLIT-31 |
| 29 | D/R split: group key never a predictor | Kit excludes target and `scaffold`, exposing exactly two SMILES and medium state; inspect grouping declaration | holds | LEAK-1, MET-2 |
| 30 | R: 17,510 rows, 3,336 groups, max 398 rows/group, 3×3 folds with stated sizes | A independently measured frame and kit; nine fold sizes agree with R; no row/scaffold overlap | holds for captured release | EV-2, SPLIT-1 |
| 31 | D/R: experimental rather than simulated labels | P20 Methods describes extraction from published spectroscopy; source identity pinned. Audit does not independently validate every experimental result | holds as documented provenance | PROV-1, PROV-3, EV-2 |
| 32 | D/R: follow-up reports absorption RMSE in nm | P21 body/results inspected, same wavelength quantity | holds | MET-1, MET-3, PROV-16 |
| 33 | D metric: `origin=source` means one deliberate source criterion for this task | P21 Methods/results distinction in finding 1; a joint seven-target loss and multiple reporting statistics do not establish unique per-target selection. Missing selection evidence is not proof that no further passage exists | untested uniqueness; current justification insufficient, see finding 1 | MET-5, MET-11, EV-6 |
| 34 | D metric: standard lower-is-better row RMSE, no extra inputs/target transform | A manual numpy score equals shipped scorer on all nine folds; finite 95.763–120.125 nm training-mean scores; no params/inputs needed | holds | MET-2, MET-3, MET-12 |
| 35 | D/R: source random-row/expanded-data scores are not this grouped qualification | P21 Methods uses different size and random partitions; kit uses grouped folds. No source score imported into A | holds | EV-4, SPLIT-5 |
| 36 | R: one missing-SMILES warning corresponds to meaningful gas rows | A confirms all 20 missing environments are gas, no missing dye structures. Warning remains for curator decision; no accepted warning asserted | holds | EV-3, CLEAN-1 |
| 37 | R: not built yet | R says so; this auditor performed no build and inspected no container registry | untested beyond statement/no build in audit | EV-7 |
| 38 | C screening: historical 20,236 / 7,016 / 365 / 1,358 publication counts | Matches P20 statements, not v3 measurements. Source-attributed historical scope preserved | holds as historical source claim | PROV-8, EV-2 |
| 39 | C screening: historical card claims 20,247 combinations, 7,018 dyes, 366 environments | Saved M lacks historical card description; no fresh historical-card retrieval | untested historical attribution; superseded | EV-2, EV-7 |
| 40 | C screening: target absorption has the most available values | A v3 has absorption 17,703 vs emission 18,851; cannot use this claim as current rationale | refuted for current v3; historical reading preserved | EV-1, EV-2 |
| 41 | C screening: all listed columns / NaN missing-data format | A matches 14 columns and normal parsed missingness; missing source outcomes remain unfilled | holds for schema | PROV-16, EV-2 |
| 42 | C screening: two extractors, third cross-check, outliers double-checked | P20 Technical Validation supports source attribution; no independent re-extraction | holds as source assertion | PROV-16, EV-2 |
| 43 | C screening: direct pre-synthesis use/group-by-dye proposal | Intended use supported; active definition explicitly adopts approximate fit and stronger grouping; no claim of prospective validation | holds as historical proposal, superseded | USE-1, USE-8, EV-2 |
| 44 | C screening: metric fallback pending unread follow-up | Historically conditional, not a present source-review finding; current origin audited separately | holds as historical uncertainty statement | EV-2, MET-1 |
| 45 | C: sibling search found no matching record; external collections not checked | This audit did not repeat catalog provenance/overlap search; owned by precedent role | untested | PROV-4, EV-7 |
| 46 | C: priority/domain counts, shape and ranking rationale | Historical source statistics are bounded to prior stage; this audit did not recompute current collection coverage/priority | untested current applicability | EV-2 |
| 47 | C curator approval authorizes add/panel, final inclusion later, no build/commit | Read saved dated CC and task authorization; no semantic verdict changed in this role | holds as recorded scope | principles precedence, house rules |

**Limits and next actions**

One current correction is recommended (metric origin). The legacy “absorption has most labels” statement is superseded by actual counts and does not require rewriting history; preserve it and use current measurements in the add-stage assessment. The semantic neat-solid mapping remains an evidence gap, not a proven misclassification: source documentation or spot-checking original measurement papers could settle it, or a neutral equal-structure category could avoid the inferred phase label. No issue is manufactured from that uncertainty.

Re-run the no-fit audit and refresh kit identities after root's scaffold/tautomer repair. Learned signal, challenge difficulty, full alias novelty, physical-condition effects, all-publication label correctness, and collection duplication are outside these tests. A clean claim audit cannot certify them. Fold numeric baselines here exist solely to show computable metric support.

Reproduce from the integration project root:


**Final focused claim-auditor recheck**

Captured: 2026-11-10T00:52:26.330698+00:00. This addendum supersedes the earlier split/metric-origin status in `report.md`; that report and its original script/JSON/stdout remain unchanged as historical evidence.

**Result: previous metric-origin finding fixed; zero remaining actionable findings from this focused recheck.** The current definition declares fallback RMSE and explicitly records why a unique absorption-only source model-selection criterion was not established. RMSE remains a standard per-row, lower-is-better score on untransformed nanometres with no extra inputs. This satisfies the requested correction under MET-1, MET-2, MET-3, MET-5, MET-8 and MET-11. No source-access assumptions or numerical metric changes were needed.

The current raw CSV still has 20,836 rows / 17,703 positive finite absorption labels; 193 exact canonical input-target repeats are removed, leaving 17,510 rows, 6,498 dye structures and **3,335 groups**. The regenerated participant frame exactly matches the independently rebuilt entire clean-frame row multiset, including current group assignments (not merely target values).

Independent RDKit canonical-tautomer keys, nonstereochemical dye keys and available InChIKeys cross **zero groups**. All nine shipped folds have **zero row, scaffold, exact-dye, nonstereo-dye, available-InChIKey or canonical-tautomer identity overlap** between training and test. Thirteen structures lack a usable InChIKey and correctly use distinct structure fallbacks rather than a shared empty identity. These are tests of the declared identity normalizations, not proof of recognition of every possible chemical equivalence. Solvent overlap is expected and remains 84–101 structures per fold.

Every fold's RMSE on training-mean predictions exactly equals the independently computed numpy formula; all nine are finite. The constants test metric computability only. No learner was fit, and no conclusions about the root's ongoing full-fit/model comparisons are implied.

| repeat | fold | train rows | test rows | training-mean RMSE (nm) |
|---|---|---|---|---|
| 0 | 0 | 11525 | 5985 | 99.284317 |
| 0 | 1 | 12060 | 5450 | 122.902398 |
| 0 | 2 | 11435 | 6075 | 97.635167 |
| 1 | 0 | 11616 | 5894 | 98.910738 |
| 1 | 1 | 11734 | 5776 | 99.146572 |
| 1 | 2 | 11670 | 5840 | 120.668828 |
| 2 | 0 | 11820 | 5690 | 123.694942 |
| 2 | 1 | 11854 | 5656 | 101.002653 |
| 2 | 2 | 11346 | 6164 | 95.081857 |

Each fold is a complete disjoint partition with no duplicate positions. Every sample is tested exactly once in each repeat. All captured canonical/source input files were unchanged at completion, and every participant-kit hash still matched at the integrity followup. Dataset-definition SHA256: `71e03ebb60944fcb40f2e744c329239b674275b9f50c835dabf08df039ede159`. Full definition/README/source/kit hashes and measurements are in `final-recheck-results.json`; the additional fold/kit integrity checks are in `final-recheck-integrity.json`.

The earlier evidence limitation on interpreting every equal dye/environment structure as neat solid was outside this focused repair and remains a disclosed untested semantic mapping, not a proven error or a new issue. Historical screening facts remain preserved; final inclusion is the curator's decision.

Additional no-fit checks are reported below.


The expanded recheck completed successfully. It did not change the dataset, decisions or build products.


</details>

<details><summary>Split audit: original and final recheck</summary>

**Historical initial audit; the final recheck below supersedes findings corrected in the definition.**

**Independent split audit: chromophore_optical_properties_db**

Audit date: 2026-11-10 UTC. Role: split-auditor, authorized full add-dataset panel. No models fit, no canonical edits, no build, commit, or publication. This report evaluates the frozen pre-repair `definition_snapshot.py`, SHA256 `779f4e1797f61983897581d1d176db38e20cd490ed65b33663345ecd8d5c4b7b`. Raw CSV SHA256: `f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c`. RDKit version: 2026.03.6.

Verdict: ship after one label-free split repair and its dependent checks. The scaffold regime fits the approved prospective new-dye use. The existing standard-InChI union is useful but does not eliminate four additional canonical-tautomer pairs crossing the original folds. The tested remedy joins their two groups, leaves all measurements intact, and removes this overlap in all nine regenerated native folds.

Validity: USE-1, USE-3, USE-10, SPLIT-1/2/4/24 and SPLIT-31 support holding out dyes and their chemical series; solvents may recur. LEAK-17 is triggered by the additional tautomer aliases and is mechanically resolved by the proposed union. LEAK-33 requires `scaffold` to remain metadata; the definition declares it as the grouping column. Value: no independent model-signal conclusion here; the main session's task probes and grouped model comparisons decide that. Quality: structural normalization and exact input-target deduplication are appropriate; no target-based regrouping or averaging is proposed.

**Finding 1: standard InChI misses four tautomer pairs across the split**

The executed audit computes canonical non-stereochemical SMILES, standard InChI, InChI connectivity blocks, RDKit canonical tautomers, and default FragmentRemover parent identities for every retained dye. Four exact canonical-tautomer keys each correspond to two source structures, with their eight measurements divided between two scaffold labels. The two measured peaks in each pair differ by 24-27 nm. Those label differences were observed after identifying the aliases and play no part in the grouping.

| Original native folds | Canonical-tautomer overlap identities | Affected test rows per fold |
|---|---:|---:|
| repeat 0, folds 0 and 1 | 4 | 4 |
| repeat 2, folds 0 and 1 | 4 | 4 |
| remaining five folds | 0 | 0 |

This is a narrow identity gap, not evidence of a large score exploit: no predictive gain was measured. Under LEAK-17 and SPLIT-24, joining the groups is the mildest remedy. Implement an additional identity union using `Chem.MolToSmiles(rdMolStandardize.TautomerEnumerator().Canonicalize(Chem.MolFromSmiles(nonstereo_structure)))`, without reading labels. Keep the full original SMILES and measured targets as shipped features/targets. Do not union arbitrary similarity clusters or every shared InChI connectivity block.

Executed alternative: `validate_tautomer_union.py` joins all groups sharing an exact canonical-tautomer key. It changes 3,336 groups to 3,335, touches eight rows in two existing groups, and yields zero canonical-tautomer identity overlap on all nine newly generated folds. Train sizes are 11,346-12,060; test sizes 5,450-6,164. This test validates the proposed split treatment, not a later edited canonical definition; the main session must check the actual final bytes and rerun affected probes.

Exact reproducible evidence: `cross_group_tautomer_pairs.csv`, `tautomer_alias_measurements.csv`, `tautomer_union_alternative_folds.csv`, `tautomer_remedy_summary.json`.

**Tests completed and negative results**

- The native plan has three repeats by three folds. Every fold partitions all 17,510 retained rows without intersection; within each repeat every row appears in test exactly once. Each original test fold contains 1,112 groups; original train sizes are 10,880-12,803 and test sizes 4,707-6,630.
- No assigned group, exact dye SMILES, non-stereochemical dye key, valid standard-InChI identity, FragmentRemover parent key, exact model-input tuple, or exact input-target tuple overlaps train/test in any original native fold. Missing InChI output is treated as unavailable, never as a common identity: 13 distinct dyes / 19 rows have no standard InChI output.
- The fallback independently counts distinct non-stereochemical structures, not measurement rows. There are 6,498 distinct dye keys; the largest base scaffold is benzene with 100 dyes (1.54%). No base scaffold exceeds ten percent, so the oversized-scaffold fallback is currently unexercised. The 41 ringless dye keys receive individual groups before identity unions. Their repeated environment measurements remain together. The algorithm's ten-percent condition was reviewed in source; no synthetic boundary fixture was necessary for this dataset-specific audit.
- There are no distinct retained dye SMILES collapsing solely after the native stereo-removal operation, so a retained stereoisomer pair cannot be an observed crossing here. There are no multi-fragment retained dye structures. The fragment-parent check finds no additional crossing. Isotope normalization follows the library's `isomericSmiles=False` behavior for split keys; full source isotope notation remains in the shipped structure.
- Ten nonmissing standard-InChI identities correspond to multiple non-stereochemical keys. Their group unions, including the isotope-normalized ethane representation, are verified by reconstruction; exact reconstruction results are recorded in `audit_summary.json` and `inchi_group_unions.csv`.
- No duplicate input-target row remains. There are 61 repeated input tuples with differing target values, covering 124 rows. Every such tuple remains within a group. Keeping genuine repeated continuous measurements is consistent with SPLIT-26 and the definition's explicit ambiguity note; this audit does not establish which disagreements reflect physical conditions versus transcription.
- Four broader InChI connectivity blocks span groups, largely involving protonation differences. These are not a new leak finding: distinct protonation states can be chemically distinct inputs with different optical responses, and full standard-InChI identities stay separated. No chemistry evidence was established that all connectivity-block matches must be merged.
- Morgan radius-2, 2,048-bit fingerprints, chirality disabled, measure structural familiarity on distinct test dye keys. Across all nine original folds, the mean share with a training analogue of Tanimoto >=0.7 is 31.41% (29.68-32.99%), versus 82.15% (81.53-82.98%) on seeded random-row folds. This comparison supports the actual purpose of scaffold grouping; it does not establish complete chemical novelty. The comparison is on the original splits; the final repaired folds need their own numbers if quoted as final-release results.
- Between 93.24% and 98.24% of original test rows have a solvent/host structure seen in training. This matches the declared task, which holds out dyes, rather than testing unknown solvents. Solvent reuse is expected and is not a hidden dye identity.

**Source and application fit**

The [primary data paper](https://www.nature.com/articles/s41597-020-00634-8) motivates predicting proposed chromophore properties before synthesis and defines the first absorption maximum, from literature measurements with dye and environment structures. It includes solutions, neat solid systems and dopant-host systems. These facts support the approved target and a new-dye regime. The scaffold choice is a curation application of SPLIT-31, not an official split established by the 2020 data descriptor.

No publication date is a prediction timestamp for a prospective hypothetical dye, and the retained frame supplies no defensible chronological deployment axis. A temporal split or publication-held-out task would answer a different question; there is no measured temporal-gap defect here. Shared literature sources might induce correlated measurement conventions, but source DOI recurrence alone does not establish that new dye evaluation must hold out papers. Source-specific measurement effects and transport to a genuinely untested synthesis programme remain untested; the existing approximate fit and missing experimental-condition note are warranted (USE-8).

**Reproduction and limits**

From `[local qualification artifact]`:


The first command freezes the definition once, then always imports that snapshot. Delete/replace no snapshot to disguise a new version: use a distinct audit directory for a new definition. `structure_identities.csv` and `audited_rows.parquet` contain per-dye/per-row identity evidence; `native_splits.parquet`, `fold_identity_audit.csv` and `analogue_comparison.csv` contain all tested splits and results. No data warehouse container is built.

RDKit canonical tautomer enumeration has finite toolkit defaults and is not a proof of every possible chemical equivalence. Standard InChI fails on the 13 noted structures. Unspecified experimental conditions, source transcription accuracy, model performance, large-score exploit potential and real prospective domain shift were not independently resolved. No threshold similarity clustering, external pretrained lookup, temporal pseudo-order or target-based deduplication was used. The audit corrects its own missing-InChI and isotope-key bookkeeping before final results; earlier transient counts are superseded by the final JSON/CSV outputs.


**Final focused split and prediction recheck**

Completed 2026-11-10 UTC. This follow-through preserves the original split audit as historical evidence and independently checks the actual repaired definition, regenerated participant kit, and completed strict diagnostic. No model was fit and no canonical file was edited by this auditor.

Recommendation: the split repair is complete; zero unresolved split findings in this focused recheck. The strict diagnostic's saved predictions and inner selection records pass the independent checks described below. This supports retaining the scaffold-grouped task with the documented approximate application fit, close-analogue exposure, and substantial fold variability. It does not decide final curator inclusion.

Definition SHA256: `71e03ebb60944fcb40f2e744c329239b674275b9f50c835dabf08df039ede159`. Raw SHA256: `f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c`. Current definition bytes match `definition_snapshot.py` here and the hash in the native encoder metadata. The original pre-repair report and snapshot remain one directory above.

**Actual repaired frame and folds**

The current definition retains 17,510 rows, 6,498 dye keys, and 3,335 final groups. The full feature/target row multiset, including duplicate multiplicities and missing solvents, is exactly preserved from the original audit. Group metadata and the deterministic row/fold arrangement changed; no labels or model inputs were removed, averaged, or modified by the repair. The generated participant frame has exactly the actual definition's row values and columns. The participant folds equal all nine actual native folds. Encoded folds equal the participant folds; encoded targets and group values match the actual frame row for row.

Independent reconstruction of scaffolds, distinct-molecule fallback, nonempty standard-InChI unions and canonical-tautomer unions reproduces every final assigned group: zero row mismatches. Ten valid standard-InChI identities have multiple non-stereochemical keys; nine successful InChI component unions occur before the tautomer repair. The four previously exposed tautomer pairs now remain together. The 41 ringless keys receive individual groups before identity joins; no base scaffold exceeds ten percent of distinct dyes. The largest base scaffold has 100 of 6,498 dye keys (1.54%).

| Repeat | Fold | Training rows | Test rows | Test groups | Tautomer overlaps |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 11,525 | 5,985 | 1,112 | 0 |
| 0 | 1 | 12,060 | 5,450 | 1,112 | 0 |
| 0 | 2 | 11,435 | 6,075 | 1,111 | 0 |
| 1 | 0 | 11,616 | 5,894 | 1,112 | 0 |
| 1 | 1 | 11,734 | 5,776 | 1,112 | 0 |
| 1 | 2 | 11,670 | 5,840 | 1,111 | 0 |
| 2 | 0 | 11,820 | 5,690 | 1,112 | 0 |
| 2 | 1 | 11,854 | 5,656 | 1,112 | 0 |
| 2 | 2 | 11,346 | 6,164 | 1,111 | 0 |

Every fold partitions the whole frame with no overlapping row positions; each row appears in test exactly once per repeat. All nine folds have zero shared assigned group, exact dye SMILES, non-stereochemical dye key, nonmissing standard-InChI identity, canonical-tautomer identity, FragmentRemover parent identity, exact model-input tuple, and exact input-target tuple. The expected broad connectivity-block matches involving distinct protonation states remain outside this stricter compound-identity claim, as explained in the original report. Missing InChI outputs remain unavailable, never a shared blank identity.

Executed evidence: `audit_summary.json`, `fold_identity_audit.csv`, `native_splits.parquet`, `current_kit_consistency.json`, `structure_identities.csv`, and `audited_rows.parquet`.

**Structural familiarity recomputed on final folds**

The method is Morgan radius 2, 2,048-bit fingerprints, chirality disabled; count each distinct test dye key once per fold. A close analogue has maximum training Tanimoto >=0.7. The seeded comparison reruns random-row 3-by-3 folds on the current frame.

| Split | Mean fraction with close training analogue | Range across nine folds |
|---|---:|---:|
| Actual repaired scaffold folds | 31.64% | 30.55%-33.38% |
| Recomputed random-row folds | 82.29% | 81.34%-83.26% |

Use these final figures rather than the original report's 31.41% / 82.15%. Grouping changes row/fold ordering even with preserved feature/target rows, so both arms were recomputed. The result supports the declared new-dye-family application under SPLIT-1/4/31; it is not complete chemical novelty. These are descriptive structural measurements, not model-error estimates. Per-fold results are in `analogue_comparison.csv`.

**Independent strict diagnostic inspection**

The inspected source is `strict_diagnostic.py` in the run root, SHA256 `1ac24029102b1554b271aa84858a71cc0574827d6508f8afb1775dad688cbcfe`. Its logic satisfies the requested boundaries:

- `feature_cols` excludes the target and grouping column. There are 2,815 inputs from two fixed SMILES encodings and medium state. The native `encode_smiles` implementation computes fixed per-molecule descriptor/fingerprint columns; it performs no label-driven encoding, global scaling, or dataset-dependent column selection. The strict script's float conversion and infinity-to-missing replacement are per-value operations.
- Ridge's imputation, scaling and one-hot encoder are inside its sklearn pipeline and are fit exclusively on each outer training side. Test transformation uses that fitted pipeline. Every outer test medium-state category also occurs in that fold's training side, so declared pandas category metadata supplies no otherwise unseen state here.
- LightGBM receives no globally imputed/scaled matrix. Its three fixed candidate configurations are fit on an inner group split taken exclusively from the outer training positions. Early stopping and candidate/tree-count selection use only the inner validation positions. The selected configuration is refit on the whole outer training side with the chosen tree count. No outer test target enters fitting, early stopping or the `min(choices)` decision in the inspected script.
- Independently reconstructing every inner `GroupShuffleSplit(random_state=4267, test_size=0.2)` confirms disjoint inner training/validation groups, no outer-test row in either inner side, and exact partition of the outer training rows. All nine selected candidate/tree pairs equal the recorded inner-validation minimum, using the script's tie order.

These are source and saved-record checks. They do not re-fit the models or claim bitwise reproduction of their training. They establish the inspected diagnostic's data boundaries, not a preregistered confirmatory study or every possible historical research choice.

**All predictions independently rescored**

All 18 NPZ prediction files are complete: nine LightGBM and nine ridge folds. For every file, its test positions exactly match the participant kit, saved truths exactly equal kit targets, predictions have the expected shape and are finite, independently calculated `sqrt(mean((truth-prediction)**2))` equals the participant scorer and `fold-results.csv` to absolute tolerance 1e-10, and independently recomputed R-squared equals the recorded value. All saved prediction files are hashed in `strict_independent_scores.csv`. The strict summary's encoded input hashes match the actual files.

| Model | Mean fold RMSE (nm) | SD across folds | Mean fold R-squared |
|---|---:|---:|---:|
| Inner-group selected LightGBM | 56.6552 | 23.3436 | 0.7062 |
| Strict train-only ridge | 77.6132 | 11.8784 | 0.4596 |
| Outer-training-mean baseline | 106.4808 | 12.0850 | — |

LightGBM's individual fold RMSE ranges from 37.7720 to 90.0683 nm. All its fold R-squared values are positive (0.4495-0.8380); ridge's are also positive (0.4051-0.5591). These provide clear predictive signal under the selected grouped task while preserving its large group-to-group error variability. Means are unweighted averages of fold scores, matching the run's reporting; repeated folds overlap in observations, so the displayed SD is not an independent-sample confidence interval.

Executed evidence: `strict_prediction_audit.json`, `strict_selection_boundary_checks.csv`, and `strict_independent_scores.csv`. This report does not substitute these strict scores for the separate native task-probe implementation; the native model families and results remain distinct evidence.


</details>

<details><summary>Domain practitioner</summary>

Fit: approximate. I would use this task to screen proposed chromophores before synthesis, because the molecular inputs exist then and the absorption wavelength matters, but the archive does not specify enough experimental conditions to promise the peak of my particular future preparation.

Recommendation: retain the proposed task, scaffold/identity grouping and fallback RMSE. I found no new Must failure in this role. Four documented limitations below affect interpretation; none justifies an invented filter or target repair.

I reviewed the current definition (SHA256 71e03ebb60944fcb40f2e744c329239b674275b9f50c835dabf08df039ede159) and independent source audit. I independently confirmed raw v3 SHA256, 20,836 rows, 17,703 labeled rows, 20 labeled gas observations, 369 labeled neat-material encodings and 193 excess identical raw input/target records. I did not fit a model or change files.

At prediction time, I can draw the proposed chromophore and specify the solvent or host I intend to use. I can also choose a neat preparation or gas-phase experiment. These are legitimate design inputs under USE-1, USE-3 and USE-6. Gas has no second molecular structure: missing solvent SMILES plus its gas designation faithfully represents that case and does not violate USE-7.

What I cannot infer reliably from those graphs alone is the eventual preparation, aggregation, speciation or material morphology. In practice I would also specify concentration, temperature, relevant pH and preparation conditions; which are essential depends on the experiment. The shipped medium state is therefore useful coarse information. “Solvent or host” appropriately preserves uncertainty about the archive’s phase information.

The target has a real screening use. I want a numeric absorption wavelength to decide whether a candidate is worth synthesizing or measuring for my intended spectral region. The descriptor’s Methods states that “the first absorption peak was selected”; it also identifies absorption properties as useful for designing chromophores for photovoltaics, dyes and optical filters. That supports the stated target under USE-5. It does not establish that this one peak describes the complete useful absorption spectrum. [Scientific Data descriptor](https://www.nature.com/articles/s41597-020-00634-8)

I would combine this prediction with synthesis feasibility and other required properties. A useful wavelength alone does not establish adequate absorption strength, photostability, quantum yield or device performance. Those limitations do not remove the real absorption-screening decision. The follow-up explicitly describes predicting properties of predesigned molecules, selecting a target, synthesizing it and then characterizing it, supporting the proposed prediction point. [JACS Au molecular-design example](https://pmc.ncbi.nlm.nih.gov/articles/PMC8395663/)

One row represents one candidate/environment observation I might wish to predict. Several observations for one dye are useful, but they are not independent new design decisions. Holding every environment and measurement of that dye together is appropriate under USE-10. Scaffold grouping is also appropriate for screening new chemical series; identity and tautomer unions conservatively prevent alternative representations from undermining that boundary.

I would interpret this as evaluation on unseen dye families within the archive’s chemical population. It does not establish performance on unseen solvents, arbitrary chemical novelty or future laboratory conditions. Different scaffolds can remain close analogues. An easier task involving further measurements of already characterized dyes would require its own framing; it is not grounds for weakening this split.

The material gaps, ranked by their effect on the decision, are:

1. Unrecorded conditions make the response incompletely specified. Identical dye/environment inputs can correspond to different physical experiments. The source audit identifies 61 conflicting pairs, with disagreements up to 100 nm; these have not been resolved against every original reference. I support keeping distinct reported observations with explicit uncertainty rather than averaging or selecting values by magnitude. I would distrust claims that all disagreement is genuine laboratory variation. This supports approximate fit under USE-8; EV-2 requires distinguishing measured disagreement from an inferred explanation.
2. Literature selection differs from my prospective candidate pool. Published, characterized compounds and available absorption measurements do not include all unsuccessful syntheses, insoluble candidates or unreported screens I may face. I would require prospective validation before relying on the model for synthesis allocation. The selection and transport caveats are justified under USE-8; changing the wording to force direct fit would not resolve them.
3. The v3 population is broader than conventional organic dyes. The source audit documents a few nonorganic species and structures exceeding the historical paper’s size scope. I would add a short explicit scope note to the record or generated documentation. I would keep published v3 rows unless source evidence establishes errors; an organic-only or historical-size filter would be a new population choice, not an established repair.
4. A wavelength error is only part of screening utility. Two candidates with the same error can differ in whether they land inside my desired spectral window. The source provides no universal window, tolerance, synthesis budget or error-cost rule. Inventing one would narrow the application without evidence.

Metric judgment: partly. I would accept RMSE in nm as primary because it measures wavelength accuracy in the unit I use and penalizes large mistakes. For the general task, retain it under MET-1, MET-3, MET-8 and MET-11. For an actual campaign with a specified spectral window and follow-up budget, additionally evaluate success among selected candidates; those parameters must come from that campaign under MET-7.

Fallback origin is defensible. The follow-up’s Methods defines joint training loss across seven normalized properties and uses a random 80:10:10 split; its reported absorption RMSE does not establish a unique absorption-only selection criterion for this grouped task. Its published 26.6 nm result is not qualification evidence for this release. [JACS Au Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC8395663/)

My trust would depend on honest performance under shipped groups, examination of large errors and clear applicability limits. This review establishes a plausible, useful task; it does not establish deployment accuracy.

Primary text was inspected through indexed publisher/PMC passages because direct opens encountered access checks. Individual disputed measurement references remain unverified. No Chromophore transfer or peer freshness was established by this role.


</details>

<details><summary>Blind reviewer</summary>

**Interpretation:** This reviewer intentionally saw only its blind packet. Requests for molecular representation and split details are addressed by typed structures, the encoder contract and independently rechecked folds. Its scientific repeat/conditions concerns remain in the mediation.

**Verdict: include with changes.** This is a useful experimental molecular-property task with enough distinct compounds and scaffold groups to support evaluation. Before admission, it needs an explicit tabular representation, reproducible split specifications, and provenance sufficient to resolve conflicting labels. I would not admit the current five-column artifact unchanged.

No dataset-specific preparation notes or scientific curation rules were supplied at startup. I read only `task.md` and `data.parquet` locally, apart from permitted installed-library imports, and consulted public primary sources. No data were written and no models were fitted.

**What the task represents**

The practical use is to predict a candidate molecule’s absorption wavelength in a specified medium before measurement, helping screen dyes, optical materials, or imaging probes. The source describes a literature-derived experimental database whose absorption target is the first absorption-peak maximum. It reports independent extraction and cross-checking of measurements. [Original data descriptor](https://www.nature.com/articles/s41597-020-00634-8)

A row represents a chromophore–medium observation. The prospective inputs are:

- `Chromophore_SMILES`: molecular structure.
- `Solvent_SMILES`: solvent, host material, or a special representation of the measurement environment.
- `medium_state`: gas, neat solid, or solvent/host.
- `Absorption max (nm)`: the regression target.
- `scaffold`: a derived grouping field that should ordinarily be excluded from predictors.

The observed table has:

| Property | Finding |
|---|---:|
| Rows | 17,510 |
| Distinct chromophore structures | 6,498 |
| Supplied scaffold groups | 3,335 |
| Distinct nonmissing solvent/host strings | 729 |
| Target mean / standard deviation | 427.35 / 106.21 nm |
| Target median | 397 nm |
| Target range | 127.7–1,055.01845 nm |
| Missing or nonfinite targets | 0 |
| Exact duplicate rows | 0 |

**Ranked concerns and required changes**

**1. The molecular representation needs a clear benchmark contract.**

The scientifically informative inputs are two molecular structures, currently stored as strings. All 6,498 chromophore strings parse with RDKit, and canonicalization preserves 6,498 distinct identities.

Under the proposed scaffold holdout, every test chromophore identity will be unseen in training. Treating SMILES as ordinary categorical values therefore discards the transferable structural information needed for this task. Results could depend heavily on string handling rather than on the tabular prediction methods under comparison.

For a conventional tabular benchmark, provide a fixed, documented molecular descriptor or fingerprint representation for both chromophore and medium, together with `medium_state`. Specify library versions and handling of gas and solids. Any learned preprocessing must use training data only. Alternatively, explicitly define a benchmark track that permits molecular parsing from SMILES.

Also specify that `scaffold` is split metadata. The supplied files do not establish whether the eventual benchmark loader excludes it.

**2. Source version and preparation cannot be reconstructed from these files.**

`task.md` cites both Figshare v2 and v3 without identifying which version produced the table. The paper links v2 and describes retaining references and DOIs for individual observations; those fields are absent here. [Original data descriptor](https://www.nature.com/articles/s41597-020-00634-8)

Consequently, the current artifact does not explain:

- Which source rows were retained or removed.
- Whether structures, units, or labels were corrected.
- Whether repeated measurements were selected, combined, or preserved.
- How `medium_state` and scaffold labels were constructed.

Admission should require a pinned source version and checksum, a preparation description, and a row-to-source mapping retained as metadata. References need not become prediction features.

I could not retrieve the Figshare version records directly, so I did not establish the differences between v2 and v3 or verify the dataset-specific reuse terms.

**3. Identical available inputs sometimes have materially different targets.**

There are **61 identical-input groups containing 124 rows** with differing absorption values. These account for 63 repeated input combinations beyond their first occurrence.

Within those groups:

- Median target range: **3.5 nm**.
- 22 groups span more than **10 nm**.
- Eight groups span more than **30 nm**.
- Maximum span: **100 nm**.

For example, `CCC(=O)c1ccc2cc(N(C)C)ccc2c1` in chlorobenzene has labels of **254 and 354 nm**.

These observations might reflect measurement conditions, different peak assignments, or transcription errors. The present columns cannot distinguish those explanations. The source itself acknowledges heterogeneous experimental conditions and limited reporting of uncertainty. [Original data descriptor](https://www.nature.com/articles/s41597-020-00634-8)

Review the largest disagreements against their references. Retain genuine repeated measurements under an explicit policy; correct demonstrated mistakes. Do not automatically average conflicting labels. Their small prevalence limits their overall impact, but the largest discrepancies deserve resolution.

**4. Scaffold holdout is appropriate, but its implementation remains unverified.**

The proposed split matches a meaningful deployment question: predicting absorption for compounds with previously unseen molecular cores.

Structural checks are encouraging:

- Every exact chromophore identity belongs to one supplied group.
- Every one of the **3,304 nonempty RDKit Murcko scaffold keys** maps to only one supplied group.
- The largest supplied group contains **398 rows**, or 2.27% of the table.
- There are **1,572 singleton scaffold groups**.

Thus, the supplied grouping does not visibly separate identical molecules or identical nonempty Murcko scaffolds across groups.

However, there are no fold assignments or seeds in the permitted files. “Three repeats × three folds” alone does not establish nine distinct, correctly executed splits. Publish exact assignments or a deterministic algorithm with seeds, and audit train/test group disjointness and target support.

The grouping recipe also needs documentation. Direct scaffold-string recomputation disagrees on 194 rows, including deliberately prefixed acyclic fallback labels. Nine supplied groups combine multiple recomputed scaffold keys. One nonfallback scaffold string fails RDKit parsing. These findings do **not** establish leakage or incorrect grouping, but they prevent exact reproduction from an unspecified scaffold procedure.

Finally, scaffold holdout does not guarantee separation by publication, laboratory, time, or all chemically similar analogues. Describe the evaluation as generalization across the chosen scaffold groups.

**5. Medium encoding is sensible in part, but mixes environments and contains redundant information.**

| Medium | Rows | Missing solvent |
|---|---:|---:|
| Solvent or host | 17,121 | 0 |
| Neat solid | 369 | 0 |
| Gas | 20 | 20 |

Every missing solvent occurs in a gas row. This is structural absence, not arbitrary missingness, and should remain distinguishable from an unknown solvent.

All 369 neat-solid rows repeat the chromophore as `Solvent_SMILES`. This follows the source’s stated convention. The source also uses host structures in the solvent field for solid matrices. [Original data descriptor](https://www.nature.com/articles/s41597-020-00634-8)

For descriptors, document this convention or represent an absent external medium explicitly; otherwise, solid rows receive a second copy of the chromophore representation.

The broad “solvent or host” category does not distinguish liquid solutions from hosted solids. Additional environmental information could matter but is unavailable here. Also, the 20 gas rows are too few to support a strong standalone generalization claim.

**6. Effective support is smaller and less balanced than the row count suggests.**

The 17,510 rows are repeated observations of 6,498 molecules, rather than independent molecular designs. Of these molecules, **3,889 occur once**, while one occurs **335 times**. The ten most frequent solvent strings account for approximately **70.0%** of all rows.

This is still adequate support for a useful benchmark. Report fold-level results and uncertainty, and consider a molecule- or scaffold-balanced supplementary metric so that heavily measured entities do not dominate interpretation.

There are 21 targets below 200 nm and one above 950 nm. These require provenance checks, not automatic removal. Extreme wavelengths alone do not demonstrate invalid data.

**Aliases, copies, and observation authenticity**

No exact row copies were found. All nonmissing chromophore and solvent strings parse successfully. Canonicalization found no alternative SMILES spellings for the same chromophore; removing stereochemical and isotope distinctions also produced no additional collisions.

A fragment-parent check merged 11 pairs involving 22 structures and 37 rows. Inspected examples lost coordinated zinc, so these are **not established duplicate molecules**. Aggressive normalization could erase meaningful chemical differences.

The source characterizes the observations as experimental spectra collected from published literature. [Original data descriptor](https://www.nature.com/articles/s41597-020-00634-8) I found no affirmative evidence of synthetic augmentation or model-generated labels in the prepared table. Nevertheless, without row provenance, I cannot certify the experimental origin of every retained value. Long decimal targets are not sufficient evidence of generation; conversions can produce such precision.

**Usefulness and preparation judgment**

The dataset offers a meaningful continuous target, substantial structural diversity, and a defensible challenge involving unseen molecular cores. Keeping the other optical-property measurements out of the inputs is sensible for prediction before measurement. Finite targets, valid structures, and explicit medium states are positive preparation outcomes.

Its usefulness is conditional on preserving molecular information in the benchmark interface. With documented descriptors or fingerprints and audited scaffold splits, it belongs in a tabular molecular-property benchmark. With only categorical treatment of raw SMILES, its scientific interpretation would be much weaker.

**Exact limits of this review**

- No model performance, baseline difficulty, ranking stability, or descriptor usefulness was measured.
- Actual fold membership, repeat independence, and within-training validation splits were unavailable.
- No row-by-row reconciliation with either Figshare release or original spectra was completed.
- Experimental versus calculated provenance was not verified for every observation.
- Exhaustive tautomer and protonation equivalence checks were not completed; a tautomer-normalization attempt encountered a molecular kekulization failure.
- Broader analogue similarity, publication overlap, laboratory effects, and temporal leakage were not quantified.
- Missing-target selection bias cannot be assessed from this already prepared table.
- RDKit parsing establishes structural readability, not correct chemical assignment or correct measurement attribution.

**Admission conditions:** define the molecular feature interface, pin and document preparation, publish reproducible scaffold folds, and resolve or explicitly retain the conflicting measurements under a documented policy.

</details>

<details><summary>Task gamer</summary>

The strongest measured prohibited-context candidate reduced mean RMSE from **58.121086 to 57.283176 nm**, a **0.837909 nm (1.44%)** gain over the matched honest model on the first three shipped folds. This is a weak, unstable advantage: it improved one fold and hurt two. A conditional scaffold bootstrap gives a 95% gain interval of **[-0.854895, 2.084175] nm**. I found **no confirmed robust leakage defect**. In particular, there were no exact, canonical, stereo-insensitive, or tautomer-equivalent molecule matches across train and test in any of the nine splits.

The benchmark predicts absorption maximum before synthesis or spectroscopy from the specified chromophore and planned environment, one row at a time. Its task metadata explicitly disallows group context and excludes `scaffold` from `score.features()`. Counts of other held-out rows and the supplied scaffold category code therefore violate the stated prediction contract, even though these attacks never consume test targets. Their measured gains do not establish that the standard feature API leaks those inputs: that API already excludes the group column. The concern demonstrated here is the effect of bypassing the contract when the complete labeled kit and group metadata are visible.

I received generic agent/tool/skill-catalog instructions, but no task-specific scientific curation rules or preparation notes. I opened no skill, house-rule, project, note, or other instruction files. I read the explicitly requested task/scorer files and inspected the kit's two Parquet inputs. I did not delegate, contact colleagues, connect to other compute hosts, or inspect installed library source. Public-web queries were limited to source/publication metadata. Test labels were used for descriptive audit statistics, final evaluation, and uncertainty analysis; they were never features, fitting targets outside the training portion, prediction lookups, calibration inputs, or hyperparameter-selection criteria. The one extra ablation was a diagnostic chosen after seeing the initial scores; it is therefore exploratory, not a separately validated discovery.

The input has 17,510 rows, 6,498 distinct chromophore SMILES, 729 non-null distinct solvent SMILES, 3 medium states, and 3,335 supplied scaffolds. There are 20 missing solvents. Every distinct chromophore parsed successfully in RDKit. Medium counts are 17,121 solvent/host, 369 neat solid, and 20 gas. Across every shipped split, train and test have disjoint row positions, disjoint supplied scaffolds, no duplicate side/row assignments, and together cover all 17,510 positions. Prediction experiments cover `r0f0`, `r0f1`, and `r0f2`, the first three splits returned by `score.splits()`. Their train/test sizes are 11,525/5,985; 12,060/5,450; and 11,435/6,075. Each row is tested exactly once in this repeat. The other six splits received structural/alias audits only.

The honest baseline is LightGBM regression with 400 trees, 31 leaves, learning rate 0.05, minimum leaf size 30, feature fraction 0.85, lambda 1, max bin 63, deterministic settings, seed 1729, and two threads. It uses radius-2, 2,048-bit RDKit Morgan fingerprints for each row's chromophore; radius-2, 256-bit fingerprints for its solvent/host; one-hot medium information; and own-row SMILES lengths, missingness, and character counts. Including the same legitimate syntax features in every model prevents attributing ordinary chemical representation gains to a format exploit. Missing solvent fingerprints are zero. The fixed medium vocabulary is gas/neat solid/solvent or host. No scaffold, row position, corpus frequency, other test row, target statistic, or test-informed feature selection enters this baseline. Caching a molecule's deterministic features across rows changes computation time only. Every model is fit exclusively on its own fold's training labels, with no validation/test early stopping and no hyperparameter search.

The table ranks tested candidate families by measured mean gain; the honest baseline is included for reference. RMSE is in nm, lower is better. Gain is baseline RMSE minus candidate RMSE. Means weight the three folds equally, not individual rows. Every number was recomputed from saved predictions with the supplied `score.score` function.

| Candidate | r0f0 RMSE | r0f1 RMSE | r0f2 RMSE | Mean RMSE | Mean gain |
|---|---:|---:|---:|---:|---:|
| Honest row-only baseline | 42.664385 | 88.102794 | 43.596078 | 58.121086 | +0.000000 |
| Full-batch counts only | 43.308444 | 84.791353 | 43.749732 | 57.283176 | +0.837909 |
| Full-batch counts + supplied scaffold code | 43.143140 | 87.720061 | 43.035239 | 57.966147 | +0.154939 |
| Neutral/fragment parent lookup, same environment | 42.629249 | 88.112047 | 43.624592 | 58.121963 | -0.000877 |
| Neutral/fragment parent lookup, any environment | 42.654481 | 88.125863 | 43.624592 | 58.134979 | -0.013893 |
| Average predictions over test molecule | 42.704786 | 88.128222 | 43.649950 | 58.160986 | -0.039900 |
| Row-position artifacts | 42.994938 | 88.224729 | 43.938364 | 58.386010 | -0.264924 |
| Average predictions over test scaffold | 43.416805 | 88.231553 | 44.583315 | 58.743891 | -0.622805 |

Raw, canonical, stereo-insensitive, and tautomer lookup variants, with either identical canonical solvent plus medium state or any environment, all score **42.664385 / 88.102794 / 43.596078 nm**, mean **58.121086**, gain **0.000000**. They leave the baseline unchanged because every one has zero train-to-test matches. Their individual results are preserved in `verified_results.csv` rather than repeated in the table.

The top candidate adds four forbidden contextual features to the honest baseline: full-dataset rows per scaffold, distinct chromophores per scaffold, distinct canonical environments per scaffold, and rows per canonical chromophore. For a held-out scaffold these counts derive entirely from the test batch, because no scaffold crosses the split. They expose collection density and experimental coverage, which are unavailable for a single future structure before measurement. The second candidate adds the shipped scaffold category code as a fifth feature. That code's categories are lexicographically ordered; there is no evidence it encodes absorption rank. Both candidates use identical LightGBM settings to the baseline. Counts alone help `r0f1` by 3.311441 nm while hurting `r0f0` by 0.644059 and `r0f2` by 0.153654. Counts plus category code improve the mean only 0.154939 nm, with a 95% conditional bootstrap interval of [-0.707814, 0.899912]. These are measured forbidden-context advantages on the chosen folds, with insufficient evidence of a reliable deployment exploit. Feature attribution within the four counts was not tested.

Row-position artifacts append normalized position, floor(position/32), position modulo 32, and position modulo 10 to the honest inputs. This fixed candidate worsens all three folds. I found no measured row-order advantage under this test. It does not exhaust all possible order/format attacks; arbitrary SMILES syntax improvements alone would be ordinary feature engineering, not evidence of post-measurement leakage.

Test-batch averaging replaces each baseline prediction by the average baseline prediction over all test rows of the same canonical molecule, or all test rows of the supplied scaffold. It uses no test labels but violates the row-wise/no-group-context contract. Both versions hurt every fold. Molecule averaging loses 0.039900 nm mean RMSE; scaffold averaging loses 0.622805 nm. Neither is an effective attack here.

Train-only normalized-parent lookups remove fragments/neutralize and canonicalize tautomers without stereochemistry, then use the matching training target mean to replace the baseline prediction. Same-environment lookup reaches 18/22/9 test rows; any-environment lookup reaches 28/28/9, 65 distinct tested rows overall. These rules do not improve mean RMSE. Importantly, these matches are **not proof of duplicate leakage**. Examples include neutral versus triprotonated chromophores (test row 714 versus train row 5158 in `r0f0`) and a zinc-coordinated chromophore versus its free ligand (test row 1736 versus multiple train rows). Charge, coordination, and environment can legitimately change absorption. This is training-neighbor prediction using a coarse chemical equivalence, which is available from the row's structure at deployment. No special unavailable information is involved, so even a gain would not itself be a feature exploit. Full examples are in `parent_collisions.json`.

Generic atom/bond scaffolds overlap across train/test (2,777/2,034/2,543 test rows in the first three folds), but this intentionally coarse identity merges chemically different molecules. It is neither an exact alias nor the task's specified grouping key. I did not train a generic-scaffold neighbor model or call those overlaps a defect. Exact/raw/canonical/no-stereo/tautomer overlap was zero in all nine splits.

The source [paper](https://www.nature.com/articles/s41597-020-00634-8) advertises a public experimental database and a searchable database website, and links the [Figshare dataset](https://doi.org/10.6084/m9.figshare.12045567.v2). That creates a plausible public-target memorization route for a retrospective benchmark. It is **unrun and unverified here**: direct publication/DOI-page fetches failed in the browser tool, search indexing supplied only source metadata/text, no raw dataset or public repository was downloaded/opened, and no public target was matched to kit rows. No RMSE or coverage claim is made for public lookup. The kit's supplied test labels were not used as a substitute for an independent public source.

If enforcing the stated deployment contract, keep supplied scaffold metadata in the evaluator, remove category codes and unused categorical vocabularies before exposing features, and prohibit full-test-batch count/aggregation features. Build all learned/count preprocessing using the fold's training rows; unseen held-out identities must get an explicit unseen/default value. Evaluate through a stateless single-row prediction interface if test-batch independence matters. Merely removing the scaffold column is insufficient to prevent grouping reconstructed from the molecular structure. Opaque/shuffled row IDs can reduce ordering exposure, although this experiment found no successful row-position attack. Existing scaffold holdouts and exact-identity separation passed these audits, so no split repair is warranted by the measured duplicate checks. Do not merge protonation/coordination states blindly. Public-database resistance would require a separately sourced or prospective hidden evaluation set; public availability alone is not a demonstrated defect or a deployment violation if retrieval of existing measurements is explicitly allowed.

Uncertainty estimates use 2,000 bootstrap resamples of test scaffolds independently inside each of the three evaluated folds, seed 20261110, holding trained models fixed and recomputing mean fold RMSE gain. They reflect test-scaffold sampling conditional on these models. They do not cover model-selection effects, dependence from overlapping training sets, future distribution shift, or all nine splits. No attack was selected or blended row-by-row using test error. Scores after the first three folds were not examined with newly trained models. Public lookup, ordinary nearest-neighbor models beyond the fixed parent mapping, alternate fingerprint sizes, broader model searches, randomized SMILES controls, and deployment batch perturbation tests were not run. There are no invented scores for unrun ideas.

There were **12 LightGBM learner fits**, using **17.386784 seconds** of measured `.fit()` wall time, below the 180-second total budget. Each fit was additionally bounded by a 15-second callback; every fit completed all 400 trees. There were no other fitted estimators. Lookups and averaging are fixed prediction transforms, with training-only target means for lookups. Feature construction, RDKit normalization, scoring, and bootstrap analysis are outside learner fit time. The alias audit/feature build took about 91 seconds. All runs used the required Python executable and OMP/MKL/OpenBLAS thread counts of 2.

The reviewer used only the participant inputs and public sources for task analysis. Necessary library imports caused incidental cache writes, whose contents were not inspected. Input separation was contractual rather than an independently enforced filesystem boundary.

Reproduction in a fresh copy of this kit uses the following commands, from the kit root. Do not rerun learner scripts during this already completed budgeted attempt. `experiment.py` performs nine fits and `ablation.py` consumes the remaining three; the latter refuses to exceed the recorded fit count/budget.


Evidence and scripts: `audit.py` builds own-row fingerprints and normalized keys, and writes `audit.json` for all nine splits. `experiment.py` implements the matched baseline and initial attacks. `ablation.py` isolates forbidden counts. `analyze.py` independently rescores saved predictions, checks coverage, exports parent examples, and bootstraps gains. `verified_results.csv` is the complete per-fold result table; `verified_summary.csv` is the final ranked summary, including intervals. `results.csv` and `summary.csv` are initial-run tables and do not include the later counts-only ablation; use the verified tables for final results. `fit_log.json` records all 12 actual fits and times. `r0f0_predictions.parquet`, `r0f1_predictions.parquet`, and `r0f2_predictions.parquet` contain row IDs and every candidate's predictions, with no copied target column. `keys.parquet` and `features.npz` contain deterministic derived features. `coverage.json`, `parent_collisions.json`, `input_sha256.json`, and stdout logs provide supporting evidence.


</details>

<details><summary>Precedent checker</summary>

**Chromophore precedent check**

Observed: 2026-11-10 UTC. Independent Phase A precedent-checker for the full authorized add-dataset panel. The report reviews the work definition and records, not an accepted release. No canonical definition, record, verdict, claim, live job, build, commit, push or publication was changed. No recursive delegation or remote inquiry occurred.

**Judgment record**

Recommendation from precedent consistency: **retain the current task and implementation for the existing review-added-datasets gate**, subject to the panel's actual-data qualification. There is **no confirmed rule contradiction or previously decided ship approval**. There is **one scientific weighing item**, the treatment of repeated inputs with distinct observed wavelengths; it belongs with the existing final scientific review, not a new approval loop.

Validity: the already approved target and premeasurement point remain intact (USE-1/5). Typed dye and medium structures and exclusion of measured optical outcomes follow CLEAN-24 and LEAK-10. Scaffold components plus exact identity unions follow SPLIT-24/31 and LEAK-17. Experimental labels distinguish this task from first_principles_absorption and molecularproperties.

Value: corrected fallback RMSE is consistent with MET-5/8/11. Source RMSE numbers under older/random splits do not establish qualification here (EV-4/8).

Quality and ambiguity: 193 exact canonical input-target repeats are removed (LEAK-19). Different measured targets for one input remain grouped; the superconductivity retention precedent supports that treatment, but the individual Chromophore disagreements have not been proven to arise from genuine condition variation (LEAK-20, EV-6). No blanket target-dependent removal or averaging is established as more faithful.

For the curator: weigh the bounded repeated-observation uncertainty at the final review. No reconsideration of the approved absorption target or scaffold regime is requested.

**Register first, then actual decisions**

I first read the decision-register script and generated the full register with the dedicated project interpreter and explicit paths:


It contains 4,141 decisions, 176 defined rule IDs and 21 global heuristic flags. None of those flags involves Chromophore. That absence is not a semantic pass: the register's outcome classifier reads keywords and some decisions lack rule IDs. I read the actual sibling record paragraphs and relevant definition code. A second names-filtered register is saved as `relevant-register.{md,json}`. Its flags can include opposite outcomes in dissimilar contexts; the USE-8 flag touching superconductivity is not evidence that all approximate tasks must be retired.

The applicable pin is revision `9048f36a1bcf7da3687fde04b18ef79cd7a1201e` in `source-pin.json`. I read ADAPTATION, HUMAN_REVIEW, the pinned knowledge-curation principles, metrics, molecules, splits, leakage and evidence references, the records reference and the add-stage review-panel contract. Rules outrank precedents; a newer curator decision supersedes an older one.

**Precedents and distinctions**

The table identifies sibling curation records and the actual decisions inspected; the run retains their exact source identities and hashes.

| Topic | Actual precedent or decision | Current Chromophore behavior and consistency |
|---|---|---|
| Existing approval | `curation/records/chromophore_optical_properties_db.md`, CC 2026-11-09, Myunghwan: first absorption maximum in nm, dye and solvent structures before measurement, scaffold-grouped evaluation, add qualification and independent panel; final inclusion later | **Consistent.** Keep this approval in force. It does not select emission because emission has more labels, certify the eventual implementation or authorize a build/commit. Historical source-access pause and screening counts remain dated history rather than present qualification claims. |
| What represents a molecule | `qsar_tid_11`, CC 2026-11-01, Lennart: ship SMILES only; authors' bits are a modeling choice. Same-day CC for `qsar_oral_toxicity`, `qsar_bioconcentration`, `apistox`, `drug_induced_autoimmunity_prediction`; CLEAN-24 amendment | **Consistent.** Two typed canonical SMILES plus decoded medium state ship; computed molecular weight and other optical outcomes leave. October decisions that dropped plain-text SMILES in favor of precomputed descriptors are superseded. A two-structure input does not justify reintroducing a fixed descriptor table. |
| Scaffold regime | `qsar_bioconcentration`, CC 2026-10-26, Lennart amends SPLIT-31; `qsar_oral_toxicity` same-day reversal of 2026-10-21 IID; `qsar_tid_11`, CC 2026-11-01 approves scaffolds | **Consistent.** Distinct dye structures, rather than repetitions in many media, determine scaffold frequencies. Ringless and oversized-scaffold fallback follow the rule. No result size justifies reverting to IID (SPLIT-4). Keeping solvents in train and test matches the approved new-dye use; there is no precedent requiring this task to hold out solvents or papers as well. |
| Identities beyond a SMILES string | `qsar_oral_toxicity`, Assessment 2026-11-01 and CC 2026-11-02, Lennart: deduplicate by 2D structure rather than fingerprint collisions; additional same-InChI tautomer copies leave | **Consistent in mechanism, appropriately different remedy.** Current Chromophore groups union nonempty InChIKey identities and canonical-tautomer identities. This prevents the same dye crossing folds while preserving distinct source measurements and full shipped structures. Do not merge empty InChI failures or treat a connectivity block alone as proof of chemical identity. No requirement to discard every alias row follows from a single-label-per-chemical classification precedent. |
| Exact repeated observations | `qsar_oral_toxicity` current definition drops 720 exact structure/label copies; LEAK-19 | **Consistent.** Current definition removes 193 exact canonical model-input/target repeats. No model score or target magnitude chooses which conflicting value survives. |
| Conflicting observations | `qsar_oral_toxicity` removes both-class structures; `nci_aids_antiviral_screen` Assessment 2026-11-02 removes 39 structures/104 rows whose conclusions conflict after the binary merge. **Closer continuous precedent:** `superconductivity`, CC 2026-10-06, Lennart keeps every measured row of repeated compositions despite unrecorded conditions and temperatures that can differ by over 30 K, grouped by exact composition. `qsar_tid_11`, CC 2026-10-21 retains different compounds/stereoisomers with their own potency rather than merging descriptor collisions | **One weighing item below.** The classification cases establish a default against unexplained contradictory labels. Superconductivity establishes that continuous measurements under omitted conditions may legitimately remain distinct. Different targets alone do not prove that Chromophore is damaged or that all disagreements are genuine. Grouping removes the cross-fold identity shortcut; residual uncertainty concerns faithful labels and intended measured response. |
| Metric and origin | MET-5/8/11; `apistox`, Assessment 2026-10-21: AUROC and MCC together, fallback; `drug_induced_autoimmunity_prediction`, same-date assessment: multiple metrics, fallback; knowledge Cases include gallstone_disease and early_stage_diabetes_risk_prediction. `qsar_tid_11` has a stated deliberate RMSE criterion | **Consistent after correction.** Current `Metric.fallback` records that the descriptor has no predictive metric, the follow-up reports RMSE and Pearson R-squared and optimizes joint standardized MSE over seven targets. RMSE in nm remains appropriate while source uniqueness is unestablished. Merely seeing RMSE reported is not enough to copy qsar_tid_11's `source` origin. The old superconductivity metric assessment mentions R2 alongside RMSE; it cannot override the explicit current MET-5 rule. |
| Fit and selection | `qsar_oral_toxicity`, CC 2026-10-21, approximate because a known prediction set is less familiar; `superconductivity`, CC 2026-10-27, approximate for a documented all-superconductor selection gap; NCI's CC 2026-11-02 distinguishes a direct label after the CA/CM merge | **Consistent.** Chromophore's approximate fit names literature selection and missing experimental conditions. It is not justified solely by a chosen analog percentage. No exact universal chemical novelty threshold or demand for a prospective modern deck follows from those precedents. |
| Experimental versus simulated | `molecularproperties`, CC 2026-09-23, Lennart: DFT targets and indispensable XYZ geometry drive exclusion; `first_principles_absorption` legacy No and AHDS note: formula/calibration points | **Consistent distinction.** Chromophore's labels are source-reported spectroscopy measurements and the prediction uses designed molecular structures. A related physical subject does not make the tables duplicates or make the experimental task simulated. The modality and simulated-label exclusions cannot be generalized to every chemistry structure task. |
| Missing medium for gas | No exact chemistry-sibling decision was found for this encoding | **No conflict established.** The measured source token `gas` denotes no solvent molecule. Keeping 20 labeled rows with missing solvent and decoded gas is a task-specific application, not a scope exception. The missing-SMILES check warning still needs its ordinary specific final-review disposition; no fresh add-stage permission is required. |

**Finding 1: repeated wavelengths are a bounded scientific judgment, not a certified mechanism**

Rank: P3/P5 task fidelity with a P4 LEAK-20 Should treatment; evidence standards EV-2/6. Status: **weighing call, not demonstrated Must violation**.

The source/column and claim audits agree that, after exact input-target deduplication, 61 model-input sets retain 124 rows with more than one wavelength (63 observations beyond one per input). Disagreement spans 0.5 to 100 nm; a single-reference 384/387 nm pair and larger cross-publication differences show why the cause cannot be called verified laboratory noise. These counts are from those independent audit artifacts, not a new measurement by this precedent role.

The default LEAK-20 action is to remove all copies with both labels, **unless the ambiguity is genuine to the task**. The classifier siblings implement the default. The physically measured, condition-dependent response and heterogeneous literature compilation distinguish Chromophore; the superconductivity CC explicitly preserves the analogous one-composition/multiple-measurements setting. It supports retention, not the stronger assertion that every Chromophore discrepancy has a valid physical cause. The current definition correctly leaves measurement versus literature/transcription explanations unverified.

Recommendation: **accept retention as implemented, with the explicit uncertainty, approximate fit and every dye alias in one split component**. Present the issue at final review so the curator sees that it is a scientific weighting judgment. If a cited origin later establishes a transcription or peak-selection error, repair from that origin under PROV-13. Do not automatically choose an average, majority, nearest-model value or wavelength range. No measured evidence here establishes that dropping all 124 rows would produce a more faithful task.

If the curator treats these observations as within LEAK-20's stated genuine-ambiguity clause, this is an application and needs no formal exception. If the curator instead judges the mechanism unresolved but still retains them as a deliberate departure from the Should default, record a **dataset-specific LEAK-20 exception**: heterogeneous continuous measurements under omitted experimental conditions, preserving published observations and the real measured response (P3/P5), with error causes still unverified. This report does not assign that decision or manufacture an exception on the curator's behalf. There is no basis for amending LEAK-20 globally from this case, and the register does not establish a third same-reason exception requiring an amendment.

**Catalog identity check and limits**

I searched all work curation records for the Chromophore/Joung identity, the Figshare article `12045567`, the Scientific Data identifier `00634-8`, and optical/absorption context. No second record for the same source or same optical-property task was found. `first_principles_absorption` points to this candidate as a related experimental task and remains its own rejected artificial source. Biological intestinal absorption and unrelated spectroscopy records are not duplicated measurements of this table. This is a local catalog check, not a fresh comprehensive external-benchmark search or a row-overlap experiment against every chemical archive. External collection coverage remains explicitly unverified; no external score has been used as evidence.

The inspected active definition has the InChI plus canonical-tautomer union and corrected fallback metric. The split-auditor's remedy evidence reports 3,336 to 3,335 groups and zero tautomer overlap for the repaired alternative folds. Older source/claim/split reports contain historical grouping counts, older `source` metric wording and metrics from original splits. Their historical numeric results must not be promoted to final repaired-fold qualification. Final definition/kit synchronization and affected actual-data probes are owned by the main add-stage session; this precedent check does not rerun those models or certify their completion.

The equal-structure-to-neat-solid interpretation is still a source-semantic gap in the claim report; no chemistry precedent resolves the fact. It is neither a consistency finding nor permission to assert phase from unsupported information. The main session can settle source evidence or use a neutral equal-structure category without changing the approved target.

**Approval and action boundaries**

The earlier Myunghwan CC remains a valid add-stage authorization and implementation constraint. No contradictory evidence here reopens the target or scaffold choice. Final ship, issue disposition and any explicit exception still belong to review-added-datasets. A panel recommendation, clean check, repaired split or prior screening Yes is not a ship mark. Build, commit, push and publication remain outside this audit's authority; they are not scientific defects and are not additional issues in the finding count.


**Added-review decision consistency, 2026-11-10:**

**Chromophore ship-decision consistency check**

Date: **2026-11-10 Pacific**. Independent review-added-datasets precedent check, before application of this round's marks.

**Result: zero conflicts requiring human reflection.** Myunghwan's exact decision, **“1A, 2A, RMSE as declared, accept gas warning, ship”**, is consistent with the current rules, the close precedents and the already presented uncertainty. All marks may proceed to routine application. No exception, amendment, additional question or new scientific gate is required.

**Exact decision and snapshot**

Myunghwan accepted options 1A and 2A, RMSE as declared and the gas warning on 2026-11-10, for the definition presented in this review.

I read the actual two numbered issues and options, the current definition and record, the saved approval, the fresh full `decision-register-before.json`, and the necessary rule and sibling decision texts. The four current Chromophore record/definition/README/REVIEW files **all match the hashes in that snapshot**. The session remains the reviewed version with the same snapshot at inspection. Thus 1A and 2A refer to the presented implemented rows, rather than an inferred or newly selected option.

The scoped input identities are:

| File under the retained approval evidence | SHA256 |
|---|---|
| `curation/records/chromophore_optical_properties_db.md` | `00687bd86c1b6800fe54eabbf866eb49338b9d4ff74dc0c8460b32abb6d398f0` |
| `datasets/_dev/tabarena-v0pt2/chromophore_optical_properties_db/dataset.py` | `aec1eea613e154d3b271800d40464bd34b431698328790be41c0cdacce192f48` |
| `datasets/_dev/tabarena-v0pt2/chromophore_optical_properties_db/README.md` | `7b0baa45a852d9577c617afac6166d1825af66c44e078685349b52c621500bf3` |
| `datasets/_dev/tabarena-v0pt2/chromophore_optical_properties_db/REVIEW.md` | `32d7ca085310f4afb68aacd4bcf5a9e5192c1b4c5987ca36a051d3dc9638ede2` |

**Mark-by-mark result**

| Actual mark | Rules and closest precedent | Consistency result and application meaning |
|---|---|---|
| **1A:** keep one record per canonical model-input/target combination, removing 193 records and retaining 17,510 rows | LEAK-16 requires a decision; LEAK-18/19 give Should defaults for copy treatment. `qsar_oral_toxicity` applies structure/label deduplication; `qsar_tid_11` distinguishes real distinct compounds from representation collisions. | **Consistent explicit weighting judgment.** The review clearly disclosed that only 50 excess rows match all raw fields except Tag and the additional 143 differ in reference or other outcomes. Accepting A does not claim that 193 physical experiments were proved copied. Different records do not establish independent experiments, and the rule does not require a retention assumption for every such record. Preserve the 193/50/143 distinction in the decision record and notes. |
| **2A:** retain 61 input sets/124 current rows with differing wavelengths | LEAK-20 explicitly permits genuine label ambiguity; USE-8 requires the stated gap; EV-2/6 distinguish measured differences from inferred causes. `superconductivity`, CC 2026-10-06, Lennart, retains repeated composition measurements with unrecorded sample/phase/pressure differences, including large target disagreements, under exact grouping. | **Consistent application of the genuine-ambiguity clause**, given the described continuous, condition-dependent literature-measurement task and Myunghwan's explicit acceptance of approximate fit and uncertainty. This is the weighing judgment the review requested. No separate exception is needed. The causes of individual discrepancies remain unverified; grouping does not validate labels. If future origin evidence demonstrates damage, PROV-13 still requires specific repair. |
| **RMSE as declared** | MET-5/8/11; multi-metric-paper fallback practice in `apistox`, `drug_induced_autoimmunity_prediction`, and the metrics Cases. | **Consistent.** Keep fallback RMSE on untransformed nm. The definition explains no unique absorption-only selection metric was established: follow-up RMSE and Pearson R-squared reporting accompanies joint standardized multi-target MSE. This mark accepts the present fallback declaration, not the historical source-origin draft. |
| **Accept gas warning** | The actual warning concerns 20 missing solvent structures; USE-7 distinguishes an absent required task input from missing ancillary data; CLEAN-24 types the structures. | **Consistent specific warning acceptance.** These rows have observed gas state and no solvent molecule, rather than an unexplained missing molecular input. Preserve missing solvent plus gas state and record the exact `dataset_smiles_column` reason. No dummy molecule, row removal or broad waiver of SMILES validity is approved or needed. |
| **ship** | Review-added-datasets Step 4 and HUMAN_REVIEW: curator scientific acceptance after issue/metric decisions; build is a separate explicit request. | **Consistent final scientific decision** on the qualified implemented variant, including the explained approximate fit and unresolved individual origins. Apply the two marks and ordinary warning/documentation follow-through. It does not authorize build, commit, push, publication or claim release before the workflow's normal condition. |

**Close precedents, drift and exception count**

The contrasting categorical chemistry cases do not create a new contradiction. `qsar_oral_toxicity` removes structures with both classes; `nci_aids_antiviral_screen` removes conflicting active/inactive conclusions after its binary merge. Those are not proof that every spread in a continuous condition-dependent experimental response must be erased. The closer superconductivity CC expressly retains conflicting continuous measurements while acknowledging unrecorded physical conditions. Its same-label multiplicity policy is not an obligation for all future datasets: Chromophore's two choices were separated, the equality policy's consequences and uncertain experimental independence were disclosed, and the curator chose them explicitly under the duplicate Should rules.

The 2026-11-09 Myunghwan approval remains in force: first absorption maximum in nm from premeasurement dye/environment inputs and scaffold-grouped evaluation. The new marks complete final scientific review and do not alter or contradict that earlier task choice. No new factual evidence was introduced by this consistency check. Existing source-error uncertainty is the issue Myunghwan just accepted, not a reason to repeat it as an unanswered question.

The fresh register contains **4,166 decisions and 21 global heuristic flags**, with **zero flags involving Chromophore**. I also inspected actual text rather than treat keyword classifications as verdicts. It contains 54 Myunghwan CC/exception decisions; checking the relevant rules and semantic duplicate/ambiguity/missingness/metric references found **no same-curator contradictory call on matching facts**. Decisions about absent clinical measurements, missing deployment timing or a different task's source metric have distinguishing facts and do not establish drift here.

The register's only explicit LEAK-18/19/20 exception entry is `mortgage`'s LEAK-20/PROV-13 repair of a demonstrably damaged doubled terminal period. That is a different mechanism. Chromophore 2A uses LEAK-20's existing ambiguity clause, not an additional exception; 1A is an explicit duplicate-weighting application, not a new general retention/removal amendment. **No third same-reason exception is established.** Neither the scientific acceptance nor the gas warning should be written as an invented rule exception.

The earlier precedent report left a weighting item for final review and described a conditional exception only if the curator were deliberately departing from the ambiguity clause. This round supplies the explicit judgment the presented review requested. The accepted incomplete-condition interpretation is within that clause; the earlier conditional possibility does not create a new mandatory exception or question after approval.

**Permitted follow-through and limits**

The main session may save/apply the exact marks, dated Myunghwan CC decisions and supporting AI assessment, resolve the existing issues while retaining their history, record the specific accepted warning, update current-policy documentation and regenerate/check affected generated artifacts. Since A/A keeps data, target, weighting, grouping and folds unchanged, these marks do not request a new data variant or learner run. Normal verification of the applied documentation/warning acceptance remains appropriate. Preserve the uncertainty; do not change “unverified cause” into “proved experimental variation.”

This is a consistency review of the supplied qualification evidence, not a new raw-data or model audit.

</details>

<details><summary>Advocate opening and rebuttal</summary>

**Advocate opening — Chromophore**

Observed 2026-11-10 UTC. Recommendation: **ship as currently defined, with its explicit limitations and the curator's final disposition of the repeated-observation policy and gas warning**. This is an advocacy recommendation for the full add-dataset panel, not a curator ship mark. I inspected the active definition SHA256 `71e03ebb60944fcb40f2e744c329239b674275b9f50c835dabf08df039ede159`, the Phase A reports and final rechecks, and the actual pinned rules (source pin `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`). I fit no models and changed no canonical files.

1. **The defined task has a real, bounded use.** A chemist can specify the proposed dye and medium before synthesis or spectroscopy, then use a predicted first absorption-peak wavelength to screen candidates. The source/column auditor accounts for all 14 raw columns; the domain practitioner independently endorses this actor, moment and decision. Other measured optical properties, row number, reference and source molecular weight leave the predictors. Two typed SMILES and the decoded medium remain. Missing concentration, preparation and temperature and literature selection make the declared fit **approximate**; the claim is not prospective laboratory accuracy or prediction of complete device performance. **Rules:** USE-1/3/5/8, LEAK-10, CLEAN-24. **Evidence:** the retained qualification evidence, active `dataset.py` task summary and feature declarations.

2. **The molecular interface and source pin answer the blind review's main artifact-level conditions.** The clean-room reviewer lacked the definition, encoder and fold files by design. Its objection to ordinary categorical SMILES is already addressed: the definition declares both structures as `Smiles`, and the inspected native encoder supplies 2,815 fixed structure/medium inputs, excluding `scaffold`. The exact Figshare v3 file, checksum, license evidence and deterministic preparation are retained; the audit independently reconstructs the complete clean-frame multiset. v3 has 20,836 raw rows, not the descriptor's historical v2 count. The blind review's demands for a pinned source, explicit structural interface and reproducible splits therefore do not establish missing implementation. Its row-to-source traceability concern remains useful for later repair; the retained raw CSV and audit tables preserve references outside prediction inputs, but they do not verify every cited measurement or resolve the author-version changelog. **Rules:** PROV-1/13, CLEAN-24, EV-2/6. **Evidence:** the retained qualification evidence.

3. **The previously identified identity leak is fixed on the actual final bytes and every fold.** The original split auditor found four canonical-tautomer pairs crossing pre-repair folds. Current groups union both nonempty InChI identities and canonical-tautomer identities, yielding 3,335 groups for 6,498 dyes and 17,510 rows. Independent final reconstruction exactly reproduces every group; all nine actual/participant/encoded folds agree and have zero exact-dye, nonstereo, available-InChI, tautomer or exact-input overlap. Thirteen failed InChI outputs are distinct fallbacks, never one blank identity. This is the mild label-free repair required by LEAK-17, completed rather than pending. Final close-analogue exposure is 31.64% versus 82.29% for recomputed random-row folds: scaffold holdout reduces familiarity while allowing legitimate analogues and recurring solvents. It does not promise complete chemical novelty. **Rules:** LEAK-17, SPLIT-1/4/24/31, EV-1/2/6. **Evidence:** the final Split and Claim rechecks above.

4. **The metric-origin finding is also fixed, without changing the task's score.** The earlier claim audit correctly distinguished reported absorption RMSE from the follow-up's joint standardized seven-property selection objective. Current `Metric.fallback` records that distinction and keeps standard per-row RMSE on untransformed nm. The final claim audit reports zero remaining actionable findings from its focused recheck and independently verifies metric computability on all nine folds. Thus the older source-origin recommendation in the source audit is superseded; it is not an open scientific dispute. No universal synthesis budget, spectral window or tolerance was sourced to justify inventing a different utility metric. **Rules:** MET-1/2/3/5/8/11, EV-2. **Evidence:** the retained qualification evidence, active metric declaration, the retained qualification evidence.

5. **Actual grouped results establish useful signal while leaving variability visible.** The native nine-fold task probe gives mean RMSE 68.197 nm for selected linear, 61.819 for forest and 57.311 for LightGBM, versus 106.481 for the dummy; the best method beats the dummy on every fold. A separate strict diagnostic uses training-only ridge preprocessing and three fixed LightGBM candidates selected on an inner group holdout, then refit on outer training data: mean RMSE 77.613 and 56.655 nm, respectively. The split auditor independently verifies all 18 saved predictions, scores and selection boundaries. Its 45 fits are bounded diagnostic evidence, not the full benchmark HPO suite. The `unstable` flag remains: strict LightGBM fold RMSE ranges 37.772–90.068 nm, with SD 23.344; overlapping repeated folds make that SD no confidence interval. This warrants honest fold reporting, not IID replacement or automatic exclusion. The bounded group probe is explicitly adapted to three families with RF square-root sampling and no kNN; it is not an unmodified full run. **Rules:** TP-1/2/3/4/5, SPLIT-4, EV-3/4/8. **Evidence:** the retained qualification evidence.

6. **The participant attack found no robust deployed-information shortcut.** The strongest forbidden batch-count candidate gains 0.838 nm mean RMSE on the first three folds only, improves one and harms two, and has conditional bootstrap interval −0.855 to +2.084 nm. Batch counts and group codes breach the existing row-wise/no-context contract; the standard feature API already excludes scaffold metadata. Exact and tautomer lookups have zero coverage across all nine folds. Coarser parent matches include chemically meaningful protonation/coordination differences and do not improve mean error. Public lookup remains an unrun possibility, not a measured exploit. The evidence supports preserving the contract and documenting the attack limits; it does not establish a strong leak that needs a new split or exclusion. **Rules:** LEAK-10/17/33, EV-1/3/6/8. **Evidence:** the retained qualification evidence.

7. **The remaining scientific call favors faithful retention, with unresolved causes explicitly exposed.** After 193 exact input-target copies are removed, 61 identical-input sets retain 124 differing observations; eight sets span more than 30 nm, and the maximum is 100 nm. Grouping prevents cross-fold identity shortcuts but cannot explain these labels. Heterogeneous continuous measurements under omitted conditions, and the closer superconductivity precedent, support keeping reported observations rather than choosing, averaging or deleting values without source proof. This is a **LEAK-20 Should weighing call**: the curator must decide whether retention applies its genuine-ambiguity clause or requires a specific exception serving P3/P5; this brief assigns neither decision. Unverified transcription/peak-selection causes remain explicit, and demonstrated errors would require origin repair under PROV-13. The 20 gas observations should also stay with structurally absent solvent; no gas-only performance claim follows. The neat-solid interpretation for 369 equal-structure rows has supporting source/domain/blind readings but remains an untested universal mapping in the claim audit; that bounded semantic uncertainty is not proof of mislabeled measurements. **Rules:** LEAK-19/20, USE-7/8, PROV-13/16, EV-2/6; principles' remedy ladder and curator precedence. **Evidence:** the retained qualification evidence and final addendum, the retained qualification evidence.

The positive factors are a meaningful experimental target, available premeasurement structure inputs, thousands of independently held-out groups, replicated signal and corrected identity boundaries. Negative factors are heterogeneous and selected literature observations, unresolved disagreement causes, coarse phase information and substantial family-dependent error. No observed result removes those limits; no remaining demonstrated Must failure in these reports defeats retention. Final inclusion, any LEAK-20 exception and specific missing-SMILES warning disposition remain with the curator. Build, commit and publication are outside this role.


**Advocate rebuttal — one round**

Observed 2026-11-10 UTC. I read the retained qualification evidence, its new `replicate-counts.json` and counting script. I concede all three bounded concerns as stated below. **Recommendation: retain the current data treatment and task; add the inexpensive v3 scope clarification and present the two repeat-policy choices precisely for the curator.** This refines “ship as defined” to “ship after documentation clarification and the existing final scientific disposition”; it supplies no curator decision. No additional fits, canonical edits, publication occurred.

1. **Conflicting observations: agreed facts and agreed decision boundary.** The 61 input sets / 124 rows, up-to-100-nm disagreement and unverified origins are real; grouping cannot establish label correctness. The critic appropriately supports retention over invented averaging or automatic conflict deletion while keeping the LEAK-20 application-versus-exception decision human. This is the same weighing boundary in my opening. The continuous superconductivity precedent supports preserving observational ambiguity, not claiming every discrepancy has a demonstrated physical explanation. A source-confirmed error would require PROV-13 repair. Neither side establishes an unresolved Must failure, and neither the small prevalence nor the positive model scores excuses a proven damaged label. **Rules:** LEAK-20, SPLIT-26, USE-8, PROV-13, EV-2/6. **Evidence:** both openings; source, domain and precedent reports; claim audit's uncertainty finding.

2. **Same-target repeats: concede the new count and narrow the claim.** The critic's script counts excess rows, with `Tag` excluded from the full-record key, on the SHA-pinned raw CSV. It reports 50 labeled full-record excess rows versus 193 equal-model-input/target excess rows, so **143 removals exceed full-record identity**. Its raw-string scope is explicit and the independently measured canonical total is also 193. I accept that difference and the 99 input/target repeat groups with multiple references. It does not establish 193 copied experiments, and even full-record equality alone does not prove experiment identity. The active code and my opening's “exact input-target copies” refer to task records, not verified duplicated experiments; handoff wording should make that distinction unambiguous.

   My preferred policy remains the implemented 193-row model-input/target deduplication. LEAK-19 supplies the default against repeatedly weighting indistinguishable inputs with the same observed response; structure has many degrees of freedom, and no independently established repeated-experiment sampling unit is shipped. Equal rounded continuous responses and distinct references are nevertheless plausible natural repeats under LEAK-18 and the stated measurement-row interpretation. They support a legitimate alternative weighting policy, not a proven reason to restore 143 rows. Keeping unequal observations while collapsing equal ones changes empirical multiplicity; that is exactly why the rationale belongs in the same repeat-policy issue rather than being described as pure provenance repair. The curator should explicitly retain this policy or choose a source-supported alternative; no silent full-record-only substitution, model-based value selection or claim of measured score insensitivity follows. **Rules:** LEAK-16/18/19/20, SPLIT-23/26, EV-1/2/6, P3/P5. **Evidence:** the retained qualification evidence, active `_clean`, source/column audit and precedent report.

3. **Broader v3 scope: concede the cheap improvement and preserve the source population.** I agree to a short note that the retained publisher v3 population includes unusual simple/nonorganic species, metal complexes and structures larger than the historical 150-heavy-atom scope, up to 225 heavy atoms. The current source pin and actual counts prevent confusing versions, but “dye” can still suggest a narrower population than the measured one. The critic's proposed documentation remedy is proportionate and changes no labels or inputs. No evidence here supports an organic-only or size filter, nor exclusion by wavelength magnitude. This is a P7 clarity improvement serving accurate P3/P5 interpretation, not a reopening of the approved absorption target or a hidden new inclusion gate. **Rules:** USE-8, CLEAN-1/11, EV-2; principles' mildest-remedy rule. **Evidence:** the retained qualification evidence, critic point 3.

4. **Already-fixed items remain settled; measured limitations remain visible.** We agree the final actual definition and all nine folds pass the repaired tautomer/identity checks, and fallback RMSE resolves the earlier metric-origin finding. Neither is pending. The clean-room interface/version/fold concerns are reconciled by the typed SMILES declarations, pinned bytes, encoder contract and independently matched participant/native folds; they do not require hard-coded canonical descriptor features. Strict saved predictions and inner-group selection boundaries passed independent audit. The native `unstable` flag and large family-dependent errors remain disclosures, not a reason to replace the split or request another learner run. The three-fold forbidden-count gain crosses zero in its conditional interval and supplies no robust new exploit. The gas warning still needs its specific final-review disposition; the claim audit's neat-solid universal-mapping uncertainty remains unproven rather than silently resolved. **Rules:** LEAK-17/33, SPLIT-1/4/24/31, MET-1/2/3/5/8/11, TP-1/2/3/5, EV-3/6/8. **Evidence:** final claim/split rechecks, task JSON, strict results and gamer report.

For mediation: disagreement is now narrow. Both sides support retaining the task and its current observations pending the ordinary curator decision; both support an explicit repeat-policy judgment and the scope note. My weighting favors retaining the implemented input/target deduplication, with its meaning accurately stated. The critic's new count strengthens the need to disclose that policy without demonstrating that another policy is more faithful. Preserve the unknown experimental origins and phase detail; do not promote either panel recommendation into acceptance.


</details>

<details><summary>Critic opening and rebuttal</summary>

**Chromophore critic opening**

Observed: 2026-11-10 UTC. Phase B, full panel. This is an AI argument for a careful final disposition, not a curator decision. I read the current definition and Phase A reports, including the final claim and split rechecks, against the pinned knowledge-curation principles and applicable references. No model was fit; no canonical definition, record, verdict, build, commit or publication was changed.

**Recommendation: ship after a small scope clarification and explicit presentation of the replicate-policy weighing call. Zero unresolved Must failures are demonstrated.** The strongest defensible criticism concerns what the retained and removed repeats mean, rather than a broken split or lack of signal. The current uncertainty language already improves the definition substantially; it must not be converted into a claim that all disagreements are known physical variation or all equal responses are proven copied experiments.

Definition assessed: the retained qualification evidence, SHA256 `71e03ebb60944fcb40f2e744c329239b674275b9f50c835dabf08df039ede159`. Raw v3 SHA256 `f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c`.

1. **Conflicting continuous observations warrant an actual weighing judgment; grouping does not validate their labels.** After equal-input/equal-target deduplication, 61 input sets retain 124 rows with distinct wavelengths. The median within-set span is 3.5 nm; 22 exceed 10 nm, eight exceed 30 nm, and the maximum is 100 nm. The source audit identifies the 254/354 nm chlorobenzene pair and a same-reference 384/387 nm pair. Individual original references were not resolved. These are measured disagreements; physical-condition variation, peak assignment and transcription remain alternative explanations. LEAK-20 is a **Should** default to remove contradictory copies unless ambiguity is genuine to the task. The continuous `superconductivity` precedent, which keeps differing measurements under omitted conditions and composition groups, supports retention much better than conflicting-class QSAR exclusions support blanket deletion. It nevertheless does not certify these particular measurements. **Remedy:** present retention with uncertainty as the substantive judgment it is; retain the current approximate fit and uncertainty wording. If the curator regards this as LEAK-20's genuine-ambiguity clause, record that application; if it is a deliberate departure from the default, record the dataset-specific exception and rationale. A targeted origin check of the largest discrepancy could change that interpretation; an exhaustive audit, averaging, target-range deletion or automatic removal of all 124 rows is not justified by current evidence. Rules: **LEAK-20; USE-8; EV-2/6; PROV-13 if actual damage is established.** Evidence: the Column and source audit above, the retained qualification evidence.

2. **The equality rule removes more than established full-record copies; the scientific meaning of that choice deserves precision.** The current `_clean` drops duplicates on canonical dye, medium, decoded state and target. It removes 193 rows (1.09% of the labeled source), while retaining differing target values for the same inputs. My independent read-only count check found 68 full-content excess rows excluding `Tag` in the whole 20,836-row source, but **only 50 among the 17,703 absorption-labeled rows**. Therefore 143 of the 193 excess removals go beyond identical labeled full records. There are 191 repeated raw input/target groups; 99 contain multiple reference values. Different provenance or discarded optical outcomes do not prove separate experiments, but the equality of a wavelength does not prove copying either. The case for the implemented policy is strong: LEAK-19 defaults to dropping same-input/same-label copies, exact molecular structures have many degrees of freedom, and repeated collection coverage should not multiply their benchmark weight. The countercase is that the stated row is a literature-reported measurement, the source's whole purpose repeats dye/environment observations, and continuous rounded measurements can agree naturally; LEAK-18 permits plausible natural repeats, and the superconductivity precedent preserves measured rows. **Remedy:** describe the action as deduplicating model-input/target records, as the definition already does, and explicitly distinguish that policy from proving 193 copied experiments. Do not silently replace it with full-record-only deduplication or restore rows on my authority. The evidence leaves a bounded weighting choice, not a demonstrated Must failure or a demand for another model run. Rules: **LEAK-16/18/19; SPLIT-23; EV-1/2/6; P3/P5.** Evidence: current `_clean`, `raw/chromophore_optical_properties_db.json`, the Column and source audit above, and this role's `check_replicates.py` / `replicate-counts.json`. The new check uses raw structure strings; the independent source audit also measured 193 canonical input/target excess rows, so the count is not inferred from fingerprints or descriptors.

3. **Clarify the retained v3 population rather than inheriting the historical organic-dye scope.** The source audit measured methane, ethane, diatomic halogens, metal complexes and structures up to 225 heavy atoms in v3, beyond the historical descriptor's organic/150-heavy-atom scope. The domain practitioner independently requests a brief scope note. The current definition correctly pins v3 and separates its row count from the 2020 count, but its description still chiefly calls all rows proposed dyes. **Remedy:** add one short note that the retained v3 source population includes those unusual species and larger structures. Keep the rows absent an origin-supported correction; an organic-only, size or extreme-wavelength filter would invent a new population. This is a cheap documentation improvement, not evidence that the task should be excluded. Rules: **USE-8; CLEAN-1/11; EV-2; P5.** Evidence: the Column and source audit above, the retained qualification evidence, and current `task_summary` / `curation_comments`.

The positive evidence limits this criticism. The final split recheck independently reproduces all 3,335 groups for 17,510 rows and 6,498 dyes, with zero tested exact-dye, nonstereo, InChI or canonical-tautomer overlap across all nine folds. Close-analogue exposure falls from 82.29% under random rows to 31.64% under the repaired groups. The appropriate interpretation is held-out dye families within this archive, with solvents recurring; the existing definition already says that. I do not reopen the repaired alias finding, request simultaneous solvent/publication/time holdouts, or treat a different scaffold as complete chemical novelty (SPLIT-1/4/31).

The actual task-probe JSON retains `unstable`, but its best family beats dummy in every one of nine folds; the flag is the mean-skill standard-error branch, not failure on most test groups. Current native mean RMSE is 68.197 nm for selected linear, 61.819 for random forest and 57.311 for LightGBM, versus 106.481 dummy. The separate strict diagnostic uses 45 fits with inner group selection wholly within outer training: LightGBM 56.655, ridge 77.613 nm. Saved predictions and selection boundaries passed independent rechecks. Strict LightGBM ranges 37.772–90.068 nm across folds. That spread warrants faithful fold-level reporting, not `Too Small`, `Trivial`, a switch to random rows or exclusion (TP-1/2/3/5; EV-3/8). The adapted native group diagnostic uses three families and native-task forest sampling with kNN omitted; it is supporting evidence, not an unmodified exhaustive native group test.

The blind review's missing-interface, version, folds and provenance concerns are conditional on its intentionally minimal clean room. The actual definition declares two typed SMILES, pins v3 bytes and transformations, excludes scaffold from predictors, and has independently audited exact participant/native folds and raw lineage. Those conditions must be reconciled with the actual delivered implementation, not replayed as new failures. Shipping raw typed SMILES follows CLEAN-24; hard-coding descriptors into the canonical dataset would contradict the maintained representation policy. The 20 gas rows correctly have no solvent molecule and an observed gas state; they do not establish a mandatory-input failure or a credible standalone gas benchmark claim.

The gamer found no robust exploit: forbidden full-batch counts gain only 0.838 nm over the matched honest model on three folds, improve one and hurt two, and have a conditional 95% interval crossing zero. The existing row-wise, no-context feature API excludes scaffold. Public availability and unrun memorization are not fresh defects. No split repair or feature removal follows from this attack (EV-2/3/6; CLEAN-7 applies to the prohibited count feature, not to the shipped feature frame).

The fallback metric correction is complete; the final claim recheck reports zero remaining actionable findings in that focused scope. I do not revive historical source-origin wording or require the 2021 random-row score to be reproduced. RMSE in nm remains coherent with the task (MET-1/2/3/5/8/11).


**Critic rebuttal — one round**

Observed: 2026-11-10 UTC. I read the retained qualification evidence. No new fit, canonical edit, external publication was performed. The parent states that the brief v3 scope clarification will be applied; I have not verified an updated definition hash and do not claim that edit is already installed.

**The advocate's evidence defeats exclusion.** I concede its points 1–6: a real premeasurement screening use, correctly typed molecular inputs, a pinned and reconstructible v3 preparation, independently verified repaired groups and nine folds, corrected fallback RMSE, and meaningful grouped predictive signal. The blind review's artifact-level concerns cannot become missing gates when the actual implementation and independent tests already satisfy them. The gamer provides no robust new exploit; the `unstable` flag does not establish unlearnability or inadequate fold support. I retain no demand to change the target, metric, typed-SMILES policy or split, and no demonstrated unresolved Must failure.

**The conflict-retention question is substantially agreed, not a reason to repeat a factual audit indefinitely.** The advocate's point 7 correctly exposes the 61 input sets / 124 differing observations, unresolved discrepancy causes and the continuous superconductivity precedent. Its explicit distinction between a LEAK-20 application and a dataset-specific Should exception is also sound. My caution is simply that “keeping published observations” does not prove their physical explanation. The definition already makes that distinction, so there is no additional wording defect to manufacture. The genuine curator question is whether the observed continuous-response ambiguity and missing conditions justify retaining all reported distinct wavelengths under this task. Both sides favor retention, with the advocate emphasizing fidelity and my opening emphasizing the remaining source-error possibility. A targeted original-reference finding could change that call; neither score improvement nor the mere existence of disagreement settles it (LEAK-20, EV-2/6, PROV-13). If the human treats the ambiguity clause as satisfied, a forced exception form is unnecessary; if explicitly departing from the Should default, the reason should be recorded. That is scientific weighing, not a fresh add-stage permission gate.

**I maintain the narrower correction to how same-target deduplication is characterized.** The advocate calls the 193 removals “exact input-target copies,” which is accurate as equality of shipped values. It should not be shortened in the final synthesis to “193 copied measurements.” The independent count in `replicate-counts.json` finds 68 full-content excess rows excluding `Tag` in the whole raw file, of which only 50 are absorption-labeled. Thus the 193 removals exceed labeled full-record duplication by 143 rows; 99 repeated input-target groups span different reference values. Those facts neither prove 143 independent experiments nor invalidate LEAK-19. They establish why the implemented policy should be explained as collapsing model-equivalent repeated responses, with uncertain experimental independence. LEAK-19 supports that default; LEAK-18's plausible-natural-repeat clause and the stated measurement-level row support the counterargument. With all same-dye rows already grouped, this is principally a choice of measurement weighting/fidelity rather than a demonstrated cross-fold leak. The current definition already uses the precise language. I request no unilateral restoration, no descriptor-based deduplication, and no new model run. If the curator accepts the current deduplication unit, no code change is needed. If they choose a different unit, that would be an explicit scientific decision requiring the ordinary downstream regeneration and affected checks, rather than an automatic “fix.”

**The v3 scope sentence is the one ordinary fix that needs no new scientific decision.** The measured presence of smaller nonorganic species, metal complexes and molecules beyond the historical 150-heavy-atom scope supports a short factual note. It does not support a filter. The parent has accepted this documentation correction. Once installed, it closes point 3 of my opening; it must not remain listed as an unresolved issue (USE-8, CLEAN-1/11, EV-2).

**Gas and phase concerns should stay proportional.** Missing solvent for 20 gas measurements is meaningful structural absence, with a known gas state; it is not evidence that these rows lack a mandatory available predictor. Its check warning needs a specific factual disposition in the normal review, not an invented scientific debate or a demand to remove gas. The equal-structure neat-solid convention has supporting independent source/domain/blind readings; the claim auditor's untested universal-mapping limitation is not evidence that the category is wrong. No additional repair is demonstrated.

My final recommendation is therefore **retain the current task and replicate implementation, apply the agreed scope clarification, and present the unresolved replicate interpretation transparently for the curator's final weighing**. No additional model experiment or canonical change is required by this rebuttal. The panel recommends; it does not supply a human ship mark. The parent owns checking the eventual documentation edit and preserving the final evidence in the maintained record.


</details>

<details><summary>Mediator</summary>

**Chromophore full-panel mediation**

Observed 2026-11-10 UTC. Phase C of the authorized add-dataset full panel. This is an AI recommendation, with no curator ship mark or exception inferred. No learners were fit, canonical files edited, build, commit or publication attempted by this role.

**Judgment record**

**Verdict recommendation: ship after changes and the ordinary final scientific disposition.** Retain the absorption task, typed molecular inputs, repaired scaffold/identity groups, fallback RMSE, and currently implemented repeat handling as the panel's preferred options. The agreed wording fixes have appeared in the working definition during this review; the owner should finish its ordinary documentation/check follow-through. No unresolved Must failure is demonstrated by the full panel evidence.

**Validity:** USE-1/3/5 hold for screening a proposed chromophore/environment before synthesis or spectroscopy; fit remains approximate under USE-8. Other measured optical outcomes leave under LEAK-10. SPLIT-1/4/24/31 and LEAK-17 are satisfied on all nine independently rechecked folds for the tested identity normalizations, after the tautomer repair. LEAK-16's requirement for an explicit duplicate decision remains for the curator: two independent Should judgments concern equal-response multiplicity (LEAK-18/19) and differing-response retention (LEAK-20). Neither is an established Must violation. PROV-13 would require origin repair if a particular erroneous measurement were established; that evidence is currently missing.

**Value:** actual grouped native probes and the separately audited strict diagnostic establish substantial signal; there is no demonstrated Trivial, Too Small, or all-models-below-mean failure. Keep the `unstable` flag and its reason visible under TP-1/2/5 and EV-3/8. The bounded three-candidate inner-group diagnostic is useful tuned evidence, not the full benchmark HPO suite. Current fallback RMSE in untransformed nm satisfies the metric-origin correction (MET-1/2/3/5/8/11).

**Quality:** retain typed canonical structures (CLEAN-24), meaningful gas absence, and the coarse solvent/host distinction. The factual v3 scope note and precise duplicate-count wording are cheap, supported corrections under CLEAN-1/11, USE-8 and EV-2. Missing physical conditions and unverified universal neat-solid mapping remain limitations rather than proven errors.

**Weighed:** real experimental screening use, thousands of held-out chemical groups and replicated signal favor retention. Literature selection, omitted conditions, unresolved repeat causes and large family-dependent errors limit interpretation. Positive scores do not validate particular disputed labels or override a proven defect.

**For the curator:** two independently answerable repeat questions, in LEAK rule order: (1) collapse equal model-input/target observations or preserve their source multiplicity; (2) retain the 61 sets of differing observed wavelengths or remove those sets. Recommend the current choice for each, for the reasons below. Final inclusion and the gas warning's factual acceptance remain ordinary review-added-datasets dispositions, without an extra gate.

**Evidence read and version boundaries**

I read all requested Phase A reports: the Column and source audit above as the column/source role; claim-auditor report and final-recheck addendum; split-auditor report and final-recheck report; domain-practitioner, blind-reviewer, task-gamer and precedent-checker reports. I read both advocate/critic openings and both rebuttals, the critic's replicate count/code, the active definition, ADAPTATION, HUMAN_REVIEW, and the pinned panel contract and applicable principles/rules. Pin: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. Earlier reports remain historical evidence; final independent rechecks supersede their original metric/grouping status.

The independently rechecked definition was SHA256 `71e03ebb60944fcb40f2e744c329239b674275b9f50c835dabf08df039ede159`. During mediation the owner installed the agreed scope and duplicate-policy explanation; the definition I read afterward was `aec1eea613e154d3b271800d40464bd34b431698328790be41c0cdacce192f48`. I verified that these statements appear, but did not rerun the complete definition pipeline or independently certify every byte of the owner's change. The owner retains final equivalence/check responsibility; do not attach the old report hash to the new file. Raw v3 SHA256 remains `f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c`.

My own additional no-fit check independently confirms the alternative repeat-policy row counts in `policy-counts.json`; `check_policy_counts.py` reproduces it using raw structure strings. The source and claim roles independently establish the canonical current count. Equality of full raw records is measured; physical experiment identity is not proved by that equality.

**Agreed facts and settled findings**

| Topic | Deciding evidence and resolution |
|---|---|
| Population and task | Publisher v3 has 20,836 raw rows and 17,703 positive finite absorption labels. Current task has 17,510 rows, 6,498 dyes and 3,335 groups. One row is a reported dye/environment observation; target is first absorption-peak wavelength in nm. Available inputs are dye/medium structures and decoded state. Other optical outcomes, Tag, Reference and derived source mass leave. Source/domain/claim audits support an approximate premeasurement use (USE-1/3/5/8; LEAK-10). |
| Identity repair | Original standard-InChI union missed four canonical-tautomer pairs. Label-free group union is installed. Independent final reconstruction reproduces every group and exact native/participant/encoded fold. All nine folds have zero tested exact/nonstereo dye, available-InChI, canonical-tautomer, fragment-parent or exact-input overlap. Thirteen failed InChI outputs use distinct structure fallbacks. No further identity repair is supported (LEAK-17; SPLIT-24/31). |
| Generalization boundary | Final close-analogue fraction is 31.64% under scaffold folds versus 82.29% under recomputed random rows. Solvents may recur. This measures unseen dye groups within the archive, with legitimate analogues remaining; it promises neither unseen solvents nor universal novelty (SPLIT-1/4/31). Use final figures instead of pre-repair 31.41%/82.15%. |
| Metric | Original source-origin claim exceeded the inspected joint seven-property objective. Fallback origin fixes that claim without changing numerical RMSE. Independent nine-fold manual scoring is finite and agrees. Source random-row 26.6 nm is not this task's qualification result (MET-5/8/11; EV-4/8). |
| Signal and variability | Native nine-fold mean RMSE: dummy 106.481, selected linear 68.197, RF 61.819, LightGBM 57.311 nm; best family beats dummy on every fold. Separate strict training-only ridge 77.613 and inner-group-selected LightGBM 56.655 nm, 45 fits, all 18 saved fold predictions independently rescored and selection boundaries inspected. Strict GBM range 37.772–90.068, SD 23.344 nm. This supports learnability while preserving `unstable`; overlapping repeated-fold SD is not an independent confidence interval (TP-1/2/5; EV-3/8). |
| Repeated responses | Current equality-key dedup removes 193 rows. Only 50 excess absorption-labeled rows match every raw field except Tag; 143 removals exceed full-record identity. Ninety-nine equal-input/target repeat groups have multiple reference values. Current differing-target population is 61 input sets / 124 rows / 63 excess observations; raw source has 126 such rows. Median span 3.5 nm, 22 sets above 10 nm, eight above 30 nm, maximum 100 nm. Causes and experiment independence are unresolved (EV-2/6). |
| Gas and phase | Twenty gas rows have intentionally absent molecular solvent and a known gas state; retaining them is coherent under USE-7/8 and CLEAN-10/12. There are 369 equal-structure neat-material encodings. Supporting source/domain/blind readings exist, but the claim role did not establish the universal phase mapping. No misclassification is proved and no new phase correction is ordered. |

The blind reviewer legitimately could not see typed-SMILES declarations, the pinned raw release/preparation, encoder metadata or actual folds. Its demands for that information are answered by the delivered definition, raw/audit lineage and independent fold checks. It does not establish a missing implementation. CLEAN-24 favors typed structures with benchmark encoding; hard-coding a curator descriptor table is not the remedy. References remain outside predictors and available in raw/audit evidence, without implying that every original paper was re-extracted. The blind review's repeat and conditions concerns survive and inform the choices below. Its balanced supplementary metric suggestion is optional analysis, not grounds to invent a second score or another curator issue.

**Gamer findings mapped to protocol and rules**

The gamer received only the participant inputs and public source information. Its report contains no rule IDs or task-specific curation-note citations. Incidental library-cache writes were not evidence of curation-note access. The blind report likewise shows no prohibited note access; neither report is discarded on the supplied evidence.

| Attack | Measured result | Rule and disposition |
|---|---|---|
| Full-batch scaffold/molecule counts | First three folds: matched honest 58.121086 versus counts 57.283176 nm; gain 0.837909 nm, one fold better and two worse; conditional scaffold-bootstrap interval −0.854895 to +2.084175 nm. | These are deliberately added forbidden test-context features, not shipped columns. LEAK-29/CLEAN-7 forbid whole-table count features; LEAK-9 addresses evaluation-level transduction via checked protocol. Keep row-wise/no-context evaluation; do not infer a source-data defect or excuse such features merely because gain is weak. No exclusion/split repair follows. |
| Counts plus scaffold code | Gain 0.154939 nm; interval −0.707814 to +0.899912. | LEAK-33 keeps group id as metadata. Actual `score.features()` already excludes it, and native/strict predictors exclude group. No newly exposed predictor is demonstrated. |
| Row position and test-batch averaging | Row artifacts worsen mean RMSE by 0.264924; molecule/scaffold prediction averaging worsen by 0.039900/0.622805 nm. | Storage position is not a prediction input (CLEAN-3; LEAK-1/10); batch averaging violates the declared row/no-context protocol (LEAK-9; SPLIT-23). Negative attacks are negative results, not assurance against every possible attack. |
| Exact/nonstereo/tautomer lookup | Zero cross-fold matches on all nine structural audits; evaluated lookups leave scores unchanged. | LEAK-17 is satisfied on tested identities; the historical alias finding is already fixed. No second repair. |
| Coarse neutral/fragment-parent lookup | No mean improvement; matches can be ligand/metal complex or different protonation states. | A row-derived training-neighbor method is available at deployment. Coarse normalization does not prove identity; no blanket merges under LEAK-17/SPLIT-24. |
| Public measurement lookup | Unrun; no independently retrieved public labels, coverage or score established. | EV-4/6: public availability/pretraining speculation does not settle inclusion. A prospective hidden source would answer a different evaluation question; it is not an existing missing add-stage condition. |

No attack is a newly demonstrated data leak intentionally being retained. There is therefore no reason to fabricate a `Potential leak, kept on purpose:` exception for these results. No existing note or accepted warning reports a robust gamer leak whose size must be revised; the missing-SMILES gas warning concerns meaningful structural absence. Preserve the measured attack and limits in the record. A stateless single-row interface is one possible enforcement mechanism, not a newly required platform implementation; LEAK-9 permits a checked protocol. Do not change data simply because the supplied evaluation kit deliberately exposes metadata that the feature API excludes.

**Routine fixes and follow-through, requiring no new scientific choice**

1. Keep the short v3 scope note now visible: small nonorganic species, metal complexes and structures up to 225 nonhydrogen atoms exceed the historical organic/150-atom description. Preserve rows absent origin-supported errors; no organic-only, size or wavelength filter (USE-8; CLEAN-1/11; EV-2).
2. Keep the precise statement now visible: 193 model-input/target excess records removed; 50 also match all raw fields except Tag; 143 are additional weighting removals. Never call these 193 proven copied experiments (EV-2/6; LEAK-16/18/19).
3. Refresh the generated README/record/assessment and affected ordinary checks for the owner's actual final definition bytes. Preserve historical reports; make the final split counts and numerical qualifications explicit. This report orders no extra learner run for unchanged semantic data/folds (EV-7/8).
4. Present the missing-solvent warning with its exact factual reason: every one of 20 missing solvents is a gas row with observed gas state, not an unexplained missing molecule. Acceptance is not inferred here. This belongs in the ordinary warning disposition, rather than a manufactured independent scientific issue.

**Two independent curator choices**

These choices share a topic but are independently variable. A curator can retain every distinct wavelength while preserving equal-response source multiplicity, or collapse equal responses while removing conflicting pairs. A single accept/change mark would hide those combinations. Give two independent marks, adjacent if useful; the two-by-two count table below demonstrates their independence. This refines the advocate's suggestion to keep them within one repeat-policy issue. No third issue is needed for a warning, the settled scope sentence, or the form of a LEAK-20 rationale.

**1. Equal input/target multiplicity (LEAK-18/19 Should; explicit decision under LEAK-16 Must)**

**Problem/effect:** collapsing equal responses changes training and row-RMSE weights. The 143 extra removals have equal prediction inputs/target but differ in other raw fields; their independence is unknown. The action is a scientific multiplicity policy, not proven source repair. All observations of the same dye are already grouped, so this is not an unresolved cross-fold identity shortcut.

| Option | Consequence, with differing responses retained | Best case and limitation |
|---|---|---|
| **A. Keep current model-input/target deduplication — recommend** | Remove 193, keep 17,510. | LEAK-19 default and high-dimensional exact structures support avoiding repeated weight for indistinguishable records. Precision is essential: equal rounded wavelengths/different references can also be natural repeats; copying is unproved. |
| B. Remove only full raw-record repeats excluding Tag | Remove 50, keep 17,653; restore 143 relative to current. | Better preserves the source's measurement-row multiplicity when natural repeated continuous responses are considered plausible under earlier LEAK-18 and SPLIT-26. Other raw-field differences do not prove separate experiments. This is also a policy, not automatically the more faithful repair. |
| C. Preserve every labeled source record | Remove zero, keep 17,703. | Maximum source multiplicity, but even 50 full-record repeats retain weight. Requires a supported natural-repeat rationale under LEAK-18; no such experiment-level proof is currently available. Less supported than A or B. |

Record the selected unit and rationale. A follows the default; B or C needs the distinguishing natural-repeat fact/rationale and, if explicitly departing from LEAK-19, its dataset-specific Should exception. No exception is assigned by this panel. A source-proven record/experiment identity map would settle the factual interpretation; a new score comparison alone would not. No targeted record repair is available now, and no unilateral row restoration follows from the critic's count.

**2. Differing observed wavelengths (LEAK-20 Should; USE-8, SPLIT-26, PROV-13)**

**Problem/effect:** 61 identical-input sets contain different measured wavelengths. Conditions/peak assignment/transcription are competing explanations; grouping cannot certify labels. The strongest retention evidence is the continuous superconductivity precedent preserving composition measurements under omitted conditions. The strongest caution is unverified source error, including a 100 nm pair and a same-reference 384/387 nm pair. Both debaters favor retention; their agreement does not make the scientific judgment mechanical.

| Option | Consequence under current equal-response policy | Best case and limitation |
|---|---|---|
| **A. Retain every distinct observed wavelength, with uncertainty — recommend** | Keep all current 124 conflict rows in 61 sets; task remains 17,510 rows. | Preserves observed responses without invented averaging or preferred-value selection; supported by condition-dependent continuous response and superconductivity. Does not prove every difference is physical rather than erroneous. |
| B. Drop every row of the 61 differing-target input sets | Remove 124 from current, retain 17,386. | Implements LEAK-20's default where genuine ambiguity is not accepted. Can remove valid repeated experiments and select the population for response agreement; no measured proof that this produces a more faithful task. |
| C. Seek a bounded origin check before choosing | No automatic row change; identify exact cited pair/reference and deciding claim. | A confirmed transcription or peak-selection error invokes PROV-13 repair; a confirmed physical setting supports ambiguity. A spot check cannot certify every conflict, and exhaustive re-extraction is not a new mandatory gate. |

If the curator judges continuous observational ambiguity within LEAK-20's stated clause, record an application; do not force an exception label. If retaining despite judging that clause unestablished, record the explicit Should departure serving P3/P5, with the unresolved causes. Do not make the nomenclature a third decision. Demonstrated mistakes would be repaired from origin; neither averaging, majority selection, model closeness nor extreme-value deletion is supported now.

**Independent policy combinations and counts**

Mediator's fresh count on raw keys agrees with the canonical current counts in the independent audits. Full-record-only dedup retains **126**, rather than 124, rows in the same 61 conflicting-input sets. Do not reuse 124 after changing the equality rule.

| Equal-response treatment | Retain differing-response sets | Drop all 61 differing-response sets |
|---|---:|---:|
| Current input/target dedup (193 removed) | 17,510 | 17,386 |
| Full raw-record dedup excluding Tag (50 removed) | 17,653 | 17,527 |
| Preserve all labeled source rows | 17,703 | 17,577 |

The preferred combination is current dedup plus retention. Counts are exact for these defined raw-key policies, with the independently established canonical equivalence of current count; no alternate groups/folds, warning set or model scores have been regenerated. Any selected row-policy change requires ordinary definition regeneration and affected split/probe/panel follow-through; current saved scores cannot simply be relabeled as results of that different dataset. Unchanged decisions retain existing evidence.

**Consistency and final limits**

Follow the November typed-SMILES decisions (qsar_tid_11 and molecular siblings), scaffold decisions, exact identity correction practice, and multiple-metric fallback precedents. The former single-label QSAR copy removals support equal-response dedup and LEAK-20's caution but do not erase this task's continuous-measurement distinction. Superconductivity is the closer differing-response precedent. If the curator removes all Chromophore disagreements, the focused reflection is what distinguishes these condition-dependent continuous measurements from superconductivity; cite source-error evidence or a deliberately stricter interpretation rather than imply grouping proves correctness. Retention with honest uncertainty is consistent with that precedent. Equal-response source weighting remains a distinct judgment; neither sibling precedent proves 143 rows to be independent or copied.

The task remains experimentally reported rather than a quantum-calculation dataset; related physical subject matter is not a duplicate. Local catalog evidence found no second copy of this source task, while external archive overlap remains unverified. No new source-level correction list, complete author v2→v3 change log, exhaustive original-reference reconciliation, prospective deployment validation or universal chemical-equivalence proof exists. These limits must remain explicit, not upgraded to a pass or endlessly expanded into approval conditions.

Full-panel evidence, one opening/rebuttal round per side, and this mediation are complete; the owner's cold editor follows the drafted REVIEW. The panel recommends; the curator alone settles final ship and any explicit exception. Build/commit/publication remain outside this role.


</details>

<details><summary>Review editor</summary>

**Version note:** The initial editorial repair request is preserved below; the final confirmation at the end of this section supersedes its readiness status.

**Chromophore cold review-editor report**

Observed: 2026-11-10 UTC. Read-only review of canonical files; this report is the only authored file. No new experiments or scientific changes were made.

**Verdict: the draft needs the concrete presentation repairs below before it is ready for Myunghwan; no new scientific gate or experiment is requested.** The two repeat-policy questions, current counts, stated uncertainty and mediation are substantively coherent. Keep both questions and the recommendation to retain the implemented combination, subject to the curator's actual choices and final inclusion verdict.

**Validity:** the opening needs enough task context to make the issues intelligible without reconstructing the dataset from the generated README or a panel report. The historical metric and identity findings are already corrected in the inspected definition and final rechecks; they must remain historical. No new demonstrated Must violation was found by this editorial review. Clarify LEAK-16's Must decision requirement separately from the LEAK-18/19 Should policy defaults.

**Value:** expose the existing evidence for signal and substantial fold variation in the short opening. This is a communication repair using the reported final grouped results, not independent model validation or a request to refit anything.

**Quality:** repair the review format, panel recommendation line, historical labels, remaining process chatter and broken evidence-pointer wording. Regenerate the known-stale README from the current definition through the ordinary authorized check. Do not hand-edit generated content.

**Weighed:** the draft carefully separates equal responses from differing responses, gives the consequential alternate counts, acknowledges source-error possibilities, and avoids attributing experimental independence from record differences. Those strengths should remain. The 935-line length is mostly retained scientific panel evidence, which may remain collapsible; do not compress away disagreements or measured findings merely to shorten the review.

**For the curator:** preserve issue 1 and issue 2 as independent marks, plus the ordinary final inclusion verdict and warning disposition. Neither report format repair nor this editor's sign-off grants a scientific decision.

**Exact inspected versions**

Paths in this report are relative to the integration project. The current definition is the retained qualification evidence.

| File | SHA256 |
|---|---|
| Draft REVIEW.md | `6c5ea849d2ebc9549021b4ae9a558dcc6c1a13152a247c6a0b4e1950a83a06fa` |
| dataset.py | `aec1eea613e154d3b271800d40464bd34b431698328790be41c0cdacce192f48` |
| Generated README.md, refreshed during this review | `7b0baa45a852d9577c617afac6166d1825af66c44e078685349b52c621500bf3` |

I read HUMAN_REVIEW.md, ADAPTATION.md, the review-editor definition, review_file_format.md, writing.md, principles.md, the relevant LEAK-16/18/19/20 wording, the draft issues/panel evidence, dataset.py, README.md and the full mediator report. This is an editorial assessment of their consistency, not a fresh raw-data audit. The panel's independent measurements remain attributed evidence.

**Concrete edits, most important first**

**1. Make the opening a self-contained judgment record**

The present outcome names a target and broad structural input but omits the actor, prediction point, row, wavelength unit, row/group support, interpretable evaluation evidence and large fold variation. The outcome does not yet show the required validity/value/quality/weighed judgment in a few lines. The deep mediator section contains that evidence, but the curator should not need to discover it there before understanding the decision.

Old opening:

> **Outcome:** added. The panel recommends retaining first absorption-peak regression from molecular structures, with approximate fit and the two repeat-record choices below left to Myunghwan. The corrected chemical-family evaluation and RMSE fallback are implemented; final inclusion remains undecided.

Suggested replacement, kept as one paragraph:

> **Outcome:** added. Ship after the documentation updates and Myunghwan's repeat-policy and final inclusion decisions (panel recommendation). Validity: a chemist predicts a proposed dye's first absorption-peak wavelength in nanometres before synthesis or spectroscopy, from the dye and medium structures plus known medium state; each row is a reported measurement. The 17,510 rows cover 6,498 dyes in 3,335 held-out chemical groups, with tested identity aliases kept together and solvents allowed to recur. Fit remains approximate because literature selection, missing conditions and unresolved response disagreements limit the task. Value: across nine grouped folds, native LightGBM averages 57.311 nm RMSE versus 106.481 for the mean baseline; the separate training-only diagnostic averages 56.655 nm but ranges from 37.772 to 90.068, so instability remains explicit. Quality: typed structures and the corrected RMSE fallback are implemented; gas has known state and no solvent molecule. Weighed: real experimental screening and measured signal favor retention, while missing conditions and repeat uncertainty limit interpretation. Myunghwan decides the two repeat policies independently and whether the dataset should ship.

The figures are all in the final mediator evidence. If a shorter outcome is preferred, move its row/support and score sentences into the existing Record judgment block, while keeping actor, target, point, inputs, split, limitations, recommendation and required decisions in the outcome. Do not import the source's 26.6 nm result as qualification or present repeated-fold variability as a confidence interval.

Old Main points:

> Decide equal-response multiplicity and differing-response retention independently. The implemented choices are recommended. Gas observations have no solvent molecule by definition; the missing-solvent warning is explained, with no gas-only performance claim. No build or publication is included in this review.

Suggested replacement:

> **Main points:** Choose separately whether to collapse equal input/wavelength records and whether to retain differing wavelengths, then decide final inclusion and the explained gas warning; the panel favors the implemented repeat policies.

This puts actual decisions first. Build authority and isolation mechanics can remain in the ordinary handoff or the relevant full report rather than occupy this one-line decision summary.

**2. Put the panel's recommendation in its first sentence**

Old:

> **Review panel:** full, with seven evidence roles, advocate and critic openings plus one rebuttal each, mediator and cold editor.

New:

> **Review panel:** ship after changes (mediator).

Continue with the factual summary of corrected metric/group findings, no demonstrated unresolved Must failure or robust exploit, implemented repeat recommendations, and both open curator marks. The format uses this first sentence as the recommendation next to the verdict box. A role inventory does not communicate it. Describe cold editing as complete only after this report has actually been included and its repairs applied or dispositioned; the inspected draft has no review-editor section yet.

**3. Remove Markdown headings from the embedded panel reports**

The title `# chromophore_optical_properties_db` remains the single review title. All `#`, `##` and `###` headings inside the panel violate the panel format even if a particular collector invocation does not reject them. Convert each embedded heading into an ordinary bold line, preserving every scientific paragraph and table.

Examples:

| Old | New |
|---|---|
| `# Chromophore source and column audit` | `**Chromophore source and column audit**` |
| `## Judgment` | `**Judgment**` |
| `# Final focused claim-auditor recheck` | `**Final focused claim-auditor recheck**` |
| `### 2. Differing observed wavelengths (LEAK-20 Should; USE-8, SPLIT-26, PROV-13)` | `**Differing observed wavelengths (LEAK-20 Should; USE-8, SPLIT-26, PROV-13)**` |

Keep role wrappers as standalone `<details><summary>Role</summary>` and `</details>` lines. Add one nonempty, nonnested Review editor section containing this report with its headings likewise converted. Do not place new report block labels after the panel. Issue numbering 1 and 2 remains unchanged.

**4. Distinguish the Must decision requirement from the Should weighting defaults**

Old issue 1 footnote:

> LEAK-16 requires a documented duplicate decision; LEAK-18 distinguishes plausible natural repeats from collection copies; LEAK-19 defaults to removing same-label copies. These are weighing/default rules, not proof of the physical identity of each observation.

New:

> **LEAK-16 (Must)** requires an explicit duplicate decision. **LEAK-18 (Should)** distinguishes plausible natural repeats from collection copies; **LEAK-19 (Should)** defaults to removing same-label copies. These policy defaults do not prove the physical identity of each observation.

Retain the superconductivity explanation and Figshare link. The old plural “These are weighing/default rules” can incorrectly include LEAK-16. This correction does not declare an unresolved Must violation, create a Must exception, or demand a separate approval. Issue 2 correctly treats LEAK-20's ambiguity clause as potentially an application rather than automatically an exception.

**5. Define prediction inputs where the first issue becomes visible**

Old issue 1 problem:

> The implemented policy removes 193 repeated model-input/target records, while only 50 excess labeled rows also match every raw field except the row number.

New:

> The implemented policy removes 193 records with identical dye structure, medium structure/state and measured wavelength, while only 50 excess labeled rows also match every raw field except the row number.

The current background correctly explains that the other 143 differ in provenance or discarded outcomes without establishing independent experiments. Keep that. Issue 2's “input sets” then has a concrete meaning, and its cause uncertainty remains correct.

**6. Mark historical positions before the reader encounters them**

The initial source audit says source-origin RMSE is supported; initial claim and split reports describe earlier definition/grouping bytes, and the blind report requests representation/split details absent from its permitted packet. Those reports are useful scientific evidence and should remain. Their findings must not look like newly unresolved current requirements.

Add this immediately inside Column and source audit, before the preserved report:

> **Version note:** This original report predates the metric-origin correction and final tautomer repair; its source-origin interpretation and earlier identity status are historical. The final claim/split rechecks and mediator below describe the implemented fallback and repaired groups.

At the start of each original claim/split subsection, use:

> **Version note:** Original finding on the captured earlier definition; the final focused recheck later in this section supersedes its current-action and split/metric status.

At the blind section's start, use:

> **Interpretation:** This reviewer intentionally saw only its blind packet. Its requests for molecular representation and split details are addressed by the typed structures, encoder contract and independently rechecked folds; the mediator explains the remaining scientific repeat/conditions concerns.

These annotations identify chronology and supplied evidence, not a reason to dismiss blind criticism. Preserve original uncorrected report bytes in the run evidence. Do not silently rewrite an original auditor's historical conclusion into agreement.

**7. Finish portability cleanup without deleting scientific evidence**

Artifact-only references should identify the corresponding scientific section and state the evidence they support.

Old recurring evidence pointers such as:

> Evidence: the Column and source audit above, the retained qualification evidence.

New, with the referenced role names chosen for the actual claim:

> Evidence: the Column and source audit, final Claim and Split rechecks, and Mediator sections in this panel.

Another old fragment is “the final Split and Claim rechecks above.” Replace it with “the final Split recheck and final Claim recheck below.” A bare run-local `report.md` is not portable evidence navigation. Keep useful scientific filenames only where they identify the artifact's contents, and give a self-contained result or public source with them. Do not replace source citations, measured tables, rule distinctions or uncertainty with generic “retained evidence.”


The per-role instruction says the panel stays as the run wrote it; embedding full scientific reports with transparent format/portability edits and retained originals is compatible with that purpose. Do not reduce reports to verdict-only summaries.

**8. Regenerate the README and complete ordinary format validation**

At initial inspection README had `metric_origin: source` and `origin | source: the source's metric`, whereas dataset.py uses `Metric.fallback` with the correct reason. It also lacked the latest v3-scope and 193/50/143 policy explanation. These were expected stale generated bytes pending regeneration, rather than a new scientific finding. During handoff the owner regenerated the page; this editor then directly confirmed `metric_origin: fallback`, the fallback origin row, the 225-nonhydrogen-atom scope note and the 193/50 policy paragraph. This documentation mismatch is now corrected. The owner reports the completed native check has 27 checks, zero errors, the expected gas warning and conflicting-label info; this editor did not independently execute that check. Do not hand-edit the generated page.

After applying the editorial repairs, use the ordinary authorized check to refresh the README, verify unchanged prepared rows/groups/folds as appropriate, and run the official focused collector/page generation on this review. Confirm two independent issue marks and actual panel recommendation render correctly. These checks are ordinary completion work; they do not authorize build, require a new learner run for unchanged data/folds, or create another curator gate.

**Checks that already read correctly**

| Claim | Editorial finding |
|---|---|
| Source/task | Figshare v3 and primary descriptor are identified; target remains first absorption peak in nm, not emission or simulated quantum labels. |
| Current support | 17,703 labeled source rows minus 193 input/target excess records gives 17,510. Final 6,498 dyes and 3,335 groups agree with the final panel evidence. Earlier 3,336-group results are historical. |
| Independent policy counts | Current dedup plus retention gives 17,510; full-record-only dedup plus retention gives 17,653. Removing all conflict sets gives 17,386 and 17,527 respectively. The conflict-set removal count is 124 under current weighting and 126 under full-record-only weighting. |
| Distinct issues | Changing equal-response multiplicity does not force a decision on differing responses. Both options tables identify the implemented row and end in a concrete Decision. |
| Cause uncertainty | A 354 nm primary-source value is corroborated; the competing older 254 nm origin remains unverified. Neither current grouping nor model signal validates that disputed observation. |
| Known absence | All 20 missing solvent structures correspond to observed gas state; no gas-only score is claimed. A warning disposition remains explicit. |
| Evaluation | Current identity repair is documented and rechecked; no guarantee of complete chemical novelty or unseen-solvent evaluation is asserted. Forbidden count-context attacks show weak exploratory gains rather than a demonstrated robust source-data leak. |
| Authority | No existing ship mark, blanket exception, build, commit or publication authority is inferred. |


**Cold editor final confirmation — 2026-11-10 UTC**

**Verdict: ready for Myunghwan's review-added-datasets decision.** The material presentation repairs requested in the initial editor report are now satisfied. Its earlier “needs repairs” verdict describes the preceding draft and is superseded by this confirmation.

Inspected final REVIEW SHA256: `1b71d9c5a05b890bf0cc02fd8ad1aa67f78afb20442037bb23835e6e94232d9b`. Definition SHA256: `aec1eea613e154d3b271800d40464bd34b431698328790be41c0cdacce192f48`. Regenerated README SHA256: `7b0baa45a852d9577c617afac6166d1825af66c44e078685349b52c621500bf3`.

The opening now explains the chemist, premeasurement prediction point, measured row, nm target, structural inputs, current support, grouped evaluation, useful signal, fold variability and known limits. The panel's first sentence is its actual recommendation. Historical source, claim and split positions are identified, while the blind packet's information limits are explained without erasing its scientific concerns. Embedded report headings are bold; only the dataset title remains a Markdown heading. LEAK-16's explicit-decision Must is distinguished from the LEAK-18/19 Should defaults. The refreshed README directly shows fallback metric origin and the latest scope/duplicate-policy notes.

The two independent issues remain intact with implemented options, recommendations and decisions. Counts remain consistent: 17,510 versus 17,653 with differing responses retained, and 17,386 versus 17,527 after excluding all conflicting-input sets. Source-error and experiment-independence uncertainty remains explicit; no Must exception, additional scientific gate or retrospective ship mark is invented. No further genuinely material editorial repair is required.

The owner reports the official collector passed one record, two issues, zero field disagreements and one panel without warnings. This editor independently inspected the revised text and its structure; it did not rerun the collector, fit models, edit canonical files or authorize build/integration. The original editor report and underlying scientific reports remain preserved. Curator repeat-policy marks, the ordinary gas warning disposition and final inclusion decision remain open.


</details>
