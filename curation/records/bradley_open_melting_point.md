---
unique_name: bradley_open_melting_point
name: Jean-Claude Bradley Open Melting Point Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2014'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.6084/m9.figshare.1031637.v2
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: an open, curated compilation of 28,645 measured melting points with structures (Bradley, Williams, Lang 2014, CC0), a QSPR regression larger than the Kaggle competition; the features have to be computed from the structures.
- Source: Jean-Claude Bradley, Antony Williams, Andrew Lang, "Jean-Claude Bradley Open Melting Point Dataset", figshare, doi 10.6084/m9.figshare.1031637 (published 2014-05-20, CC0): "Jean-Claude Bradley's Legacy Dataset of Open Melting Points. 28,645 measurements including those found to be incorrect (marked as 'do not use'). csid corresponds to Chemspider ID." One file BradleyMeltingPointDataset.xlsx; the columns were not read (the run's assessment names SMILES), and "about 20,000 unique compounds after cleaning" is from later papers, not checked. It is a compilation: the Open Notebook Science collection "pooled and processed from the following sources: Alfa Aesar, MDPI, Bergstrom, PhysProp, DrugBank, Bell, Oxford MSDS, Hughes, Griffiths and the Chemical Information Validation Spreadsheet" (figshare 93086, 2012).
- Use case: a chemist or process engineer estimates a compound's melting point from its structure before making or measuring it (formulation, purification, solubility); fit approximate: the deposit names no decision. Regime: one row per compound after averaging its measurements; IID or a scaffold-grouped split, to decide at /add-dataset (SPLIT).
- Siblings and duplicates: `melting_point` (`TBD -> Yes`, the Kaggle 2025 competition, MAE in Kelvin; whether its rows come from this compilation was not checked: if so, this is their first publication, PROV-8); `melting_point_patents` (this run, about 300,000 text-mined patent values); `mtp2` (TabBench-Bio, 274 drug compounds); the OCHEM melting points noted on `melting_point`. Cuts of this compilation: the "Double Plus Good" set (3,041 values, figshare 1031638, 2014) and ONSMP029 (2,706 compounds, figshare 93086), versions without a distinct task (PROV-6). External collections: none found.
- Better data: from the run's search, found as better data for `melting_point`; no further search this round.
- Papers and pages: the figshare deposits above; Tetko, Lowe, Williams 2016 (J Cheminform, the patent melting points), which cites this collection.
- Metric: none found (a data deposit without a task; looked at the figshare descriptions), so the fallback `rmse` in degrees C (MET-8); the competition's MAE belongs to its own data.
- Risks for /add-dataset: the features must be computed from the structure (descriptors or fingerprints, a choice to document); drop the 'do not use' rows and average repeated measurements per compound, keeping one compound in one fold (LEAK-17); overlap with `melting_point` and `melting_point_patents` (PROV-6); salts, mixtures and decomposition values.
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (the deposit names no decision), source + (named curators, a DOI, a documented source list), shape + (about 20,000 compounds), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `melting_point`.
- as published: 28,645 melting point measurements with ChemSpider IDs and SMILES, including values marked 'do not use' (about 20,000 unique compounds after cleaning per later papers); one xlsx; target: melting point (degrees C) per compound; access: open (CC0).
- Why: Same target and unit as the Kaggle melting-point competition; curated measured values with structures
- Adds: Several times more compounds than the competition with curated, flagged measurements; the competition's rows may be a cut of this or another public set (not checked; if so, PROV-8 makes this the first publication of those rows)
