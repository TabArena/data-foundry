---
unique_name: ili_external_corrosion_cross_country_pipeline
name: 'Dataset for: Cross-country Pipeline Inspection Data Analysis and Testing of Probabilistic Degradation Models (in-line inspection reports of external ...'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: Other
year: '2021'
domain: industry & manufacturing
source_links:
- https://doi.org/10.17632/c2h2jf5c54.1
- https://data.mendeley.com/datasets/c2h2jf5c54
- https://doi.org/10.1016/j.jpse.2021.09.004
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: real in-line inspection reports of external corrosion on one cross-country pipeline (four runs), published to test degradation models; no per-anomaly prediction target is defined, and anomalies are not matched across runs.
- Source: "Cross-country pipeline inspection data analysis and testing of probabilistic degradation models", Journal of Pipeline Science and Engineering 1(3):308-320, 2021 (doi 10.1016/j.jpse.2021.09.004); data by Yarveisy, Khan and Abbassi on Mendeley Data c2h2jf5c54 v1 (2021-10-04, CC BY 4.0): four Excel files, "Corrosion features reported in the first report (first year)" up to the seventh year (56 to 74 MB each), an RData of "All inspection reports from year one to seven with categorical time stamps", R scripts and a README. Variables (README Table 3): Year ("The inspection year does not reflect real asset age"), GWNUM (girth weld number), joint length, relative and absolute positions, seam and feature orientations, nominal wall thickness WT.mm, feature length L.mm and width W.mm, and MD.mm, "Feature maximum depth". "Data acquired by Filtering four consecutive inline inspection datasets"; the operator is not named.
- Use case: a pipeline integrity engineer, after an inspection run, decides which anomalies to excavate before the next run from their predicted depth; fit approximate at best, since the data has no anomaly matching across runs; regime temporal by run, grouped by joint (GWNUM).
- Siblings and duplicates: `pipeline_dataset_in_oil_and_gas_sector_fertilizer` (TBD -> 2nd Tier, `No Good Target (yet)`, a likely generated table); no other inspection record. External collections: none found.
- Better data: found as better data for `pipeline_dataset_in_oil_and_gas_sector_fertilizer`; no further search this round.
- Papers and pages: the paper (title and metadata only); the Mendeley README.
- Metric: none found (README; the paper not read); fallback `rmse` once a depth target is defined (MET-8).
- Risks for /add-dataset: the target has to be built: depth at the next run needs anomalies matched across runs by joint and position, which the deposit does not hold (`No Good Target (yet)`); depth from length and width of the same run is one reading of the tool predicted from others, which no decision needs (USE-2); SO.deg missing in year three and EPD.m in year five; rows not counted (files not opened).
- Priority: gap 0 (industry & manufacturing), use case 0 (none named for a per-anomaly prediction), source + (paper, deposit and README), shape + (many anomalies over runs and joints), risk - (no target yet).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `pipeline_dataset_in_oil_and_gas_sector_fertilizer`.
- as published: one row per external corrosion anomaly reported by in-line inspection of one cross-country steel pipeline, four consecutive inspection reports (years 1, 3, 5, 7; 'the inspection year does not ...; target: MD.mm, the maximum depth of a corrosion anomaly (wall loss measured by the ILI tool), e.g. the depth at the next inspection or the growth between runs; access: open.
- Why: The old record's own Kaggle description says its 1,000 pipes were 'generated through API ... and ASME' (Kaggle metadata, pipe_thickness_loss_dataset.csv), and the record has no good target. This is real, traceable wall-loss data of the same quantity (metal loss in mm), from an operator's ILI runs, with a paper and a ...
- Adds: Real measured wall loss instead of a likely generated table; orders of magnitude more rows; four inspection runs give a natural temporal split and pipe joints (GWNUM) a group. Caveats: the features are anomaly geometry and location, not pipe material and grade as in the old record; matching anomalies across runs to ...
