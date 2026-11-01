---
unique_name: christchurch_lateral_spreading
name: 2011 Christchurch earthquake lateral spreading (Avon River area)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2021'
domain: environmental science & climate
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.17603/ds2-3zdj-4937
- https://doi.org/10.1177/87552930211004613
- https://arxiv.org/abs/2603.17175
- https://github.com/chhsiao93/di-ebm-lateral-spreading
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 7,291 sites of the Avon River area with lateral spreading observed after the 2011 Christchurch earthquake (displacement from satellite image correlation, positive above 0.3 m) and five geospatial inputs; a documented, open single-event table with strong spatial structure, and no coordinates in the copy previewed.
- Source: Durante and Rathje, "An exploration of the use of machine learning to predict lateral spreading", Earthquake Spectra 37(4):2288-2314 (online 2021-04-08, doi 10.1177/87552930211004613), with the data and notebooks on DesignSafe, "Machine Learning Models for the Evaluation of the Lateral Spreading Hazard in the Avon River Area Following the 2011 Christchurch Earthquake" (PRJ-2998, doi 10.17603/ds2-3zdj-4937, issued 2021, version 2; no licence in the DataCite record; the DesignSafe pages refused the fetch). Abstract (Crossref): "A dataset of more than 7300 lateral spread observations from a single event", Random Forest models for occurrence and for displacement classes at about 80% and 70% accuracy. As used by Hsiao, Kumar and Rathje 2026 (arXiv 2603.17175; data on DesignSafe PRJ-6270 and GitHub chhsiao93/di-ebm-lateral-spreading, no licence): "This dataset includes 3,055 sites that exhibited lateral spreading and 4,236 sites with no lateral spreading", classified "based on horizontal surface displacements measured through remote sensing image correlation", sites "with displacements under 0.3 m are labeled as non-lateral spreading"; GWD, PGA and elevation "extracted from the New Zealand Geotechnical Database", the distance to the Avon River or its tributaries, the slope from a 15 m DEM. The GitHub `data/data.csv` (837 kB, header and 11 rows previewed) has `Test ID`, `GWD (m)`, `Elevation`, `L (km)`, `Slope (%)`, `PGA (g)`, `Target`, `Displ`: `Target` is `Displ` above 0.3 m, `Test ID` looks like an NZGD test id (to verify), and no coordinates ship.
- Use case: a geotechnical engineer or a regional planner maps where lateral spreading is likely in a future earthquake, to prioritise ground improvement or inspections; the source models it within one event and its abstract says more research is needed before the models generalise to other earthquakes and settings, so the fit is approximate (a hindcast of one event, USE-8). Regime grouped, spatial: neighbouring sites share the regional groundwater and PGA models and the displacement field, so a random split leaks neighbours; the 2026 paper's 70/15/15 split does not say whether it is spatial (SPLIT-5). The group key needs coordinates (the DesignSafe PRJ-2998 files, or the NZGD by `Test ID`) and must be a true group or one constructed exactly from the data (SPLIT-24, SPLIT-25).
- Siblings and duplicates: no lateral-spreading or liquefaction record (grep by liquefaction, lateral spread, Christchurch); `nepal_earthquake_building_damage` is building damage, another task and event. DesignSafe PRJ-4631 (2024, a SHAP study, per the run) and PRJ-6270 (2026) re-publish the same 7,291 sites: versions of one source (PROV-6); take PRJ-2998. External collections: none found on the pages read.
- Better data: from the curator's Zotero collection (item 142); no further search this round.
- Papers and pages: Durante and Rathje 2021 (the data; text not read); Hsiao, Kumar and Rathje 2026, "Domain-informed explainable boosting machines for trustworthy lateral spread predictions" (arXiv 2603.17175, HTML read).
- Metric: Durante and Rathje 2021 report accuracy (abstract); Hsiao et al. 2026 assess "accuracy, precision, recall, F1-score, and the area under the receiver operating characteristic curve" side by side; no threshold or cost fixed, so the fallback `roc_auc` (MET-5, MET-6, MET-8); inputs none (coordinates, if used for the groups, are a group column, never a feature).
- Risks for /add-dataset: drop `Displ` (the target is its threshold; LEAK-10), or ship the displacement as the regression framing instead (the source also predicts displacement classes); the spatial group key (above); PGA varies little within the area (0.53 to 0.55 g in the rows previewed) and GWD comes from a regional model, so the signal rests mostly on distance to the river and elevation; one event only; whether the DesignSafe files carry more columns (CPT features for part of the sites) than the GitHub copy.
- Priority: gap 0 (environmental science, binary and grouped are covered), use case 0 (approximate), source + (journal paper, DesignSafe DOI), shape + (7,291 sites, spatial structure), risk - (the spatial group key must be rebuilt from coordinates absent from the copy previewed).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 142: "Domain-informed explainable boosting machines for trustworthy lateral spread predictions".
- as published: sites, 7,291 rows x 5 features (groundwater depth, PGA, elevation, distance to river, slope), one event 2011; target: lateral spreading yes/no (horizontal displacement > 0.3 m from optical image correlation); displacement also available; access: open.
- Why: real observations with remote-sensed labels, public, used by several ML papers
- Adds: a geohazard classification task; spatial data, needs a spatial/grouped split. Later versions: DesignSafe PRJ-4631 (2024, SHAP) and PRJ-6270 (this paper)
