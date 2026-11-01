---
unique_name: usgs_postfire_debris_flow
name: USGS post-wildfire debris-flow occurrence (western US basins)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2016'
domain: environmental science & climate
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://pubs.usgs.gov/publication/ofr20161106
- https://arxiv.org/abs/2608.05265
- https://doi.org/10.3133/ofr20161106
- https://doi.org/10.1016/j.geomorph.2016.10.019
- https://pubs.usgs.gov/of/2016/1106/ofr20161106_appx-1.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the USGS database behind its operational post-fire debris-flow likelihood model, 1,550 basin-and-storm records from 34 fires in seven western states, field-verified debris flow or none, with storm rainfall, burn severity, terrain and soil; a real hazard-assessment task in an open, documented table, small, with the source's own geographic train and test sets.
- Source: Staley, Negri, Kean, Laber, Tillery, Youberg, "Updated logistic regression equations for the calculation of post-fire debris-flow likelihood in the western United States", USGS Open-File Report 2016-1106 (2016-06-30, https://doi.org/10.3133/ofr20161106), appendix 1 (https://pubs.usgs.gov/of/2016/1106/ofr20161106_appx-1.xlsx, previewed 2026-10-31): 1,550 rows x 27 columns (fire name and year, segment id, Database Training or Test, state, UTM zone and coordinates, Response "Field-verified hydrologic response. 0 = no debris flow. 1 = debris flow", storm date, gauge distance, storm start, end, duration, accumulation and mean intensity, peak 15-, 30- and 60-minute intensities and accumulations, contributing area, PropHM23 (share burned at moderate or high severity on slopes over 23 degrees), dNBR/1000, KF); 334 debris flows, 1,216 none; 34 fires of 2000-2012 with storms of 2000-2014; CA 939, CO 300, AZ 209, NM 58, MT 26, ID 14, UT 4. Companion paper: Staley et al., Geomorphology 2017 (https://doi.org/10.1016/j.geomorph.2016.10.019, not read).
- Use case: the USGS emergency assessment of a new burn: for each basin, the likelihood of a debris flow at a given rainfall intensity, "for hazard assessment and early warning" (OFR, introduction; "Both models are currently being applied operationally by the U.S. Geological Survey"; one author is from the National Weather Service); fit direct for the likelihood given the storm, with rainfall as the scenario input (observed peaks in the data, design or forecast intensities in operation); regime grouped by fire (the basins of one fire share the storm and the burn) or the source's geographic design: "The training dataset consisted of 939 records from southern California ... The test dataset consisted of 611 total records (133 debris-flow events) from other areas in the Western United States" (OFR, Methods); one regime to choose (SPLIT-3, SPLIT-5).
- Siblings and duplicates: no record holds post-fire debris flows (grep by debris, postfire, post-fire); `fpa_fod_wildfire_cause`, `fpa_fod_attributes_wildfire_size` and `wildfireia_initial_attack_failure` are about the fires themselves (PROV-7). External collections: none found.
- Better data: from the curator's Zotero collection (item 234, Ledingham et al. 2026); no further search this round.
- Papers and pages: OFR 2016-1106 (logistic model M1, full text read); Ledingham, Xu, Zhu et al., "Evaluating Machine Learning Models for Post-Wildfire Debris-Flow Prediction" (arXiv 2608.05265, 2026: 15 models, TabPFN at threat score 0.637 under repeated stratified cross-validation; the data source is not named on the abstract page).
- Metric: the OFR evaluates by the threat score, "a classifier evaluation metric from receiver operating characteristics (ROC) analysis ... commonly used in post-fire debris-flow studies" (OFR, Methods), the field's deliberate choice (MET-5) but a threshold metric whose likelihood cut-off the text read does not fix (MET-6), so the fallback `roc_auc` unless the add stage finds the cut-off (OFR table 3, Staley et al. 2017); inputs none.
- Risks for /add-dataset: the 15-, 30- and 60-minute peak intensities and accumulations are rescalings of each other (keep them, or the duration the USGS uses); Fire_SegID, gauge distance and storm times are ids or metadata (drop), coordinates by decision; the training rows are all southern California (939 of 1,550), so folds grouped by fire are unbalanced by region; 334 positives over 34 fires (about 7 fires per fold).
- Priority: gap 0 (environmental science, binary and grouped are covered), use case + (the USGS names its operational assessment), source + (a USGS report with a documented appendix), shape + (1,550 records from 34 fires, a grouped structure), no known risk.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 234: "Evaluating Machine Learning Models for Post-Wildfire Debris-Flow Prediction".
- as published: one row per burned basin and storm: 1,550 rows (334 debris flow, 1,216 none), 34 fires, about 244 storms, 2000-2013, CA, AZ, CO, ID, MT, NM, UT; 10 features (storm accumulation, duration, mean and ...; target: debris flow observed in the basin during the storm (binary); access: open.
- Why: The public data behind the operational USGS likelihood model, with real field-verified responses and a natural grouped split by fire
- Adds: A geohazard early-warning task; the existing fire records cover fire occurrence, cause or size, not post-fire hazards. Caveats: small; the rainfall features are observed storm values, while operational use relies on forecasts or thresholds; 61% of rows are southern California.
