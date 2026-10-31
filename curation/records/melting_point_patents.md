---
unique_name: melting_point_patents
name: Melting point and pyrolysis point data for tens of thousands of chemicals mined from patents
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2015'
domain: chemistry & material science
problem_type: Regression
source_links:
- https://doi.org/10.6084/m9.figshare.2007426.v1
- https://doi.org/10.1186/s13321-016-0113-y
- http://ochem.eu/article/99826
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: about 242,000 compounds with a melting point text-mined from US patents (Williams, Lowe, Tetko, CC0), a QSPR regression two orders of magnitude larger than the Kaggle competition; the labels are noisy and the features have to be computed from the structures.
- Source: Antony Williams, Daniel Lowe, Igor Tetko, "Melting Point and Pyrolysis Point Data for Tens of Thousands of Chemicals", figshare, doi 10.6084/m9.figshare.2007426, published 2015-12-09, CC0: "Almost 300,000 data points have been collected"; files `melting_point.sdf` (638 MB) and `pyrolysis_point.sdf` (39 MB). Paper: Tetko, Lowe, Williams, "The development of models to predict melting and pyrolysis point data associated with several hundred thousand compounds mined from PATENTS", J Cheminform 8:2, 2016 (doi 10.1186/s13321-016-0113-y): after removing flagged values, mixtures and duplicates (records within 1 °C "were considered as full duplicates"; one record per molecule, near its median), 241,958 compounds for training, 228,173 melting and 13,785 decomposing (Table 1); "A majority of MP values were reported as intervals or ranges".
- Use case: a chemist estimates a new compound's melting point from its structure before making it, for solubility and formulation ("Melting point (MP) is an important property in regards to the solubility of chemical compounds", Background); fit approximate: no actor or decision is named. Regime: one row per compound; IID or a scaffold-grouped split, to decide at /add-dataset.
- Siblings and duplicates: `melting_point` (`TBD -> Yes`, the Kaggle 2025 competition; its comment names the OCHEM compilation of Tetko et al. 2014), `bradley_open_melting_point` (`TBD -> Yes`, priority 3, 28,645 curated measurements, 2014), `mtp2` (`TBD -> 2nd Tier`, 274 drugs of Bergström 2003): the same target from other sources, each its own record (PROV-4). The paper used Bergström (277), Bradley (2,878), OCHEM (21,832) and Enamine (22,449) compounds as validation sets, so compounds overlap across these records (check at /add-dataset). No record links figshare 2007426. External collections: none found.
- Better data: found as better data for `melting_point`; no further search this round.
- Papers and pages: Tetko et al. 2016 (read in Europe PMC, PMC4724158); the OCHEM article page in the links (not opened).
- Metric: RMSE in °C, the one criterion of the paper's model comparison (Table 3, "RMSE of models for prediction of different sets", fivefold cross-validation), so `rmse` (MET-5), which is also the fallback; inputs none.
- Risks for /add-dataset: features computed from the structures (descriptors or fingerprints, a choice to document); text-mining noise (the paper puts the experimental accuracy at about 35 °C from 18,058 duplicated measurements and quotes misprints such as "Mp. −383 °C"); ranges to reduce to one value; decomposition and sublimation points to keep apart (the pyrolysis file, the outcome qualifier); a 638 MB SDF to parse; compound overlap with the siblings.
- Priority: gap 0 (chemistry and regression are not thin), use case 0 (no decision named), source + (a CC0 deposit with a journal paper and named curators), shape + (about 242,000 compounds), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `melting_point`.
- as published: almost 300,000 melting and decomposition points text-mined from US patents (about 275,000 compounds after processing per later papers); melting_point.sdf (638 MB) and pyrolysis_point.sdf; target: melting point (degrees C) per compound; access: open (CC0).
- Why: Same target (melting point) and unit (the compound) as the Kaggle melting-point competition, with structure as the input
- Adds: About two orders of magnitude more compounds than the competition (its train.csv is 2.3 MB and test.csv 0.6 MB, a few thousand compounds, not counted); caveat: text-mined values carry label noise
