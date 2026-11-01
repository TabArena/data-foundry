---
unique_name: fpa_fod_attributes_wildfire_size
name: 'FPA FOD-Attributes: physical, social and biological attributes of US wildfires (FPA FOD v6 + 267 attributes)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: environmental science & climate
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.8381129
- https://essd.copernicus.org/articles/16/3045/2024/
- https://doi.org/10.22541/essoar.169774550.06744529/v1
- https://doi.org/10.2737/RDS-2013-0009.6
- https://doi.org/10.5194/essd-16-3045-2024
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: an open, documented table of 2.3 million US wildfires with about 270 covariates at the ignition point; the final fire size is a real target for initial-attack triage, but the source poses no task, a weather window reaches past ignition, and WildfireIA is a cut of the same fires for the same target.
- Source: FPA FOD-Attributes by Pourmohamad, Abatzoglou, Belval, Short, ..., Sadegh (Boise State University with USFS and others), Zenodo v1.0 of 2023-09-26 (https://doi.org/10.5281/zenodo.8381129, CC BY 4.0), paper in Earth System Science Data 16:3045-3060 (2024, https://doi.org/10.5194/essd-16-3045-2024); the fire records are the USFS fire-occurrence database FPA FOD v6 (Short 2022, https://doi.org/10.2737/RDS-2013-0009.6). As published: "more than 2.2 million wildfires" in the contiguous US, 1992-2020 (paper: about 2.3 million), "nearly 270" attributes added per ignition (the paper counts 267 added and 310 in all); 29 yearly CSVs plus FPA_FOD_Plus.csv (5.0 GB), 10.1 GB. Target as the record proposes: FIRE_SIZE (acres) or FIRE_SIZE_CLASS from the FPA FOD base columns; the paper names no target.
- Use case: a dispatcher or fire manager, when a fire is discovered, estimates how large it will grow to set initial-attack priority (the decision WildfireIA states for its cut); the ESSD data page only says the data can "support descriptive, diagnostic, predictive, and prescriptive wildfire analytics, including the development of machine learning models"; fit approximate (the use case is ours for this table); regime temporal (by discovery year, 29 years) or grouped by region, to decide.
- Siblings and duplicates: `forest_fires` (`Yes`; 517 fires of one Portuguese park, burned area from FWI codes): the same target quantity from another source, no duplicate (PROV-4). `wildfireia_initial_attack_failure` (unscreened, this run; 38,128 natural FPA-FOD fires of 2016-2020 with its own gridMET and LANDFIRE covariates and a size label, final size >= 50 ha against <= 10 ha, arXiv https://arxiv.org/abs/2606.15529, moved here from source_links, PROV-12): the same fires and the same target quantity, a cut under PROV-6, so the curator decides which framing enters. `fpa_fod_wildfire_cause` (the same table with the cause as target: a distinct task, PROV-7). External collections: none in our vocabulary; the Kaggle upload "1.88 Million US Wildfires" (2017) re-uploads FPA FOD v4 (not checked).
- Better data: no new search; found as better data for `forest_fires`, and through the curator's Zotero collection (item 208, the WildfireIA paper, which builds on FPA-FOD).
- Papers and pages: Pourmohamad et al. 2024 (ESSD page read: no model trained; "variables have substantial overlap and correlation, which need to be addressed"); Short 2022 (FPA FOD v6); Xu, Cheng, Dong 2026 (WildfireIA: AUPRC, chronological split, a forbidden-feature list).
- Metric: none found for the size task (ESSD paper: no predictive evaluation; Zenodo page); fallback `rmse` on the size (its modelling scale, a log transform, to settle under MET-3) or `roc_auc` for a size class (MET-1, MET-8); WildfireIA's AUPRC belongs to its own cut and label. Inputs: none.
- Risks for /add-dataset: the 5-day weather summaries run "from 2 d prior to 2 d after the ignition date" (LEAK: keep the ignition-day and earlier values only); post-discovery FPA FOD columns (containment date and time, the cause as determined later, the size class) must go; the size is very skewed (most fires are under 1 acre); 2.3 M rows need a subsample or a year range; overlap and correlation among the 270 covariates; the overlap with WildfireIA (PROV-6).
- Priority: gap 0 (environmental science, regression and temporal are not thin), use case 0 (the source names no actor or decision), source + (ESSD paper, Zenodo, USFS base data), shape + (millions of fires, mixed types, 29 years), risk - (a weather window past ignition, a target the source does not pose, a cut of the same fires as WildfireIA).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `forest_fires`; the curator's Zotero collection, item 208: "A Nationwide Benchmark for Wildfire Initial Attack Failure Prediction with Public ...".
- as published: more than 2.3 million wildfire records (Zenodo page: more than 2.2 million, contiguous US), 1992-2020, 310 attributes (267 added to FPA FOD v6); 29 yearly CSVs plus FPA_FOD_Plus.csv (5.0 GB), 10.1 ...; target: final fire size (FIRE_SIZE in acres, or FIRE_SIZE_CLASS), the same quantity as the burned area in ha of forest_fires; access: open, open (Zenodo, CC BY 4.0).
- Why: same task as forest_fires: the burned area of a fire from the weather and fire-danger indices at the time of the fire plus location and date (FWI codes there, ERC/BI/fuel moisture here); real records (US agency fire reports, Short 2022) joined to 24 documented covariate sources at the ignition point | The same task ...
- Adds: 2.3M fires against 517, 29 years nationwide against one Portuguese park in 2000-2003, many more covariate kinds; a temporal (by year) or spatial grouped split is possible. Risks: the weather summaries over a 5-day window centred on ignition include days after it (LEAK), post-discovery columns (containment date, ...
