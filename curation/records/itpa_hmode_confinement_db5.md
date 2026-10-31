---
unique_name: itpa_hmode_confinement_db5
name: ITPA Global H-mode Confinement Database (HDB5.2.3)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
year: '2021'
domain: physics & astronomy
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1088/1741-4326/abdb91
- https://doi.org/10.11578/1814950
- https://datacommons.princeton.edu/discovery/catalog/doi-10-11578-1814950
- https://indico.ukaea.uk/event/449/contributions/1660/attachments/578/978/EPS_proceedings_2026.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the ITPA multi-machine H-mode confinement database (DB5.2.3, CC BY 4.0) of measured tokamak discharges, whose thermal energy confinement time the field regresses to project machines not yet built (ITER, SPARC); a split by device mirrors that use, but the target is the ratio of two measured quantities that may ship, and the table sits close to a scaling-law study (SEL-3 to weigh).
- Source: Verdoolaege, Kaye, Angioni, Kardaun, Maslov, Romanelli, Ryter, Thomsen, "The updated ITPA global H-mode confinement database: description and analysis", Nuclear Fusion 61:076006 (2021, https://doi.org/10.1088/1741-4326/abdb91); data on Princeton Data Commons (https://doi.org/10.11578/1814950, CC BY 4.0, one xlsx, one pdf and one doc file, 14 MB). As published: one row per steady-state time slice of an H-mode discharge; after spherical tokamaks are excluded, the standard ELMy H-mode set "Std5 contains 5919 entries across 15 devices", 3,386 of them new in DB5 (Std5new), next to the older releases DB2.8 (1998) and DB4.5 (2004) (Hall, Zhang, Zhang, Angioni, Verdoolaege, EPS 2026 proceedings, linked, read); target the thermal energy confinement time tau_E,th (s), regressed on plasma current, toroidal field, line-averaged density, thermal loss power, major radius, elongation and effective mass; DB5 adds wall and divertor material, heating and isotope (per the run's Assessment; the codebook not read).
- Use case: a design team projects the confinement time of a planned device or scenario from its engineering parameters: scaling laws are "important tools for quantifying, comparing and predicting confinement performance" (Hall et al.), and both papers project ITER (and SPARC); fit direct for predicting an unseen machine, though the projections extrapolate beyond the database; regime grouped by device (SPLIT-3), with the database release (DB2, DB4, DB5) as a temporal alternative.
- Siblings and duplicates: none (grep: tokamak, confinement, H-mode, ITPA). External collections: none found.
- Better data: no new search; found through the gap scout for physics and astronomy.
- Papers and pages: Verdoolaege et al. 2021 (abstract via Crossref: OLS and two robust regressions, an ITER prediction, error bars on the parameters); Hall et al. 2026 (EPS proceedings: OLS on Std2, Std4 and Std5 with R² of 0.96 or more); the IPB98(y,2) scaling (ITER Physics Basis 1999).
- Metric: none found as a ranked criterion (both papers fit log-linear laws and report coefficients, error bars and R²), so the fallback `rmse`, with the scale (the target modelled as log tau_E, scored in seconds or on the log) to settle under MET-3 (MET-1, MET-8). Inputs: none; the device ships as the group.
- Risks for /add-dataset: tau_E,th is the thermal stored energy over the thermal loss power; if both ship, the stored energy and every quantity derived from it (beta, H factors, dimensionless parameters) go, or the task is `Trivial` (SEL-5, TP-4); which subset ships (Std5 or all of DB5) and the filters behind the standard set; about 15 to 20 devices of very different sizes, so a grouped split has few, uneven groups (TP-5 per fold to check); SEL-3: a table built for a scaling law, kept here because the law is used to predict new machines (the curator's call); the codebook is in the doc file.
- Priority: gap + (physics & astronomy has no accepted dataset), use case + (the papers name the projection to new devices), source + (ITPA with a Nuclear Fusion paper, CC BY data), shape + (5,919 standard entries, numeric and categorical, device groups), risk - (a target computed from shipped columns; few devices for a grouped split).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for physics and astronomy.
- as published: Tokamak H-mode discharge entries (one row per steady-state time slice): the standard ELMy H-mode set Std5 has 5,919 entries from 15 conventional tokamaks (Hall et al., EPS 2026 proceedings, Sec. ...; target: Thermal energy confinement time tau_E,th (s), the quantity the IPB98(y,2) and ITPA20 scaling laws regress; access: open.
- Why: Real measured multi-machine experiments under CC BY 4.0, with a paper-defined regression (the confinement scaling law, used for ITER and SPARC projections); predicting a machine not in the data is the use, so a grouped split by device mirrors it, and the database waves (Std5new = 3,386 entries added in DB5) give a ...
- Adds: The first measured physics-experiment regression; grouped (device) and temporal (database wave) structure; mixed types (device, divertor and wall material, heating method, isotope as categoricals next to numeric engineering parameters)
