---
unique_name: fpa_fod_wildfire_cause
name: 'Spatial wildfire occurrence data for the United States, 1992-2020 (FPA FOD, 6th edition): wildfire cause'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2014'
domain: environmental science & climate
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.2737/RDS-2013-0009.6
- https://doi.org/10.5194/essd-6-1-2014
- https://doi.org/10.5281/zenodo.8381129
- https://doi.org/10.5194/essd-16-3045-2024
- https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the US Forest Service's fire-occurrence database (about 2.3 million US wildfires, 1992-2020) with the general cause as a multiclass target, a task the Kaggle mirror poses; no source names a decision, several cause and name columns spell or coarsen the target, and reporting systems may code causes differently.
- Source: Short, K. C. (USDA Forest Service, Rocky Mountain Research Station), first in Earth System Science Data 6:1-27 (2014, https://doi.org/10.5194/essd-6-1-2014): "nearly 1.6 million records" of 1992-2011, compiled "for the national, interagency Fire Program Analysis (FPA) application"; 6th edition 1992-2020 (Short 2022, https://doi.org/10.2737/RDS-2013-0009.6; the archive page answered 403 or "Service unavailable" on 2026-10-31, so its fields come from the USFS map-service listing (NWCG_CAUSE_CLASSIFICATION, NWCG_GENERAL_CAUSE, NWCG_CAUSE_AGE_CATEGORY) and the screening of `fpa_fod_attributes_wildfire_size`). As published in the Kaggle mirror of the 3rd update (https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires, 1.88 million fires, 1992-2015, SQLite): one row per fire with source system, reporting agency and unit, fire name, ICS-209 and MTBS ids and names, complex name, discovery date, day and time, cause code and description, containment date and time, final size and size class, coordinates, land owner, state and county; target NWCG_GENERAL_CAUSE in the 6th edition (STAT_CAUSE_DESCR in the mirror), with the missing or undetermined causes as an unlabelled pool.
- Use case: a fire-prevention planner or investigator attributes a probable cause to a fire whose cause was not determined, to target prevention (burn restrictions, arson patrols, power-line and railway work); the Kaggle mirror only asks "Given the size, location and date, can you predict the cause of a fire wildfire?"; fit approximate (the use case is ours); regime temporal by discovery year (29 years), with the reporting unit as a grouping to weigh (SPLIT-3).
- Siblings and duplicates: `fpa_fod_attributes_wildfire_size` (`TBD -> Yes`, priority 2, screened this run): the same fires plus about 270 ignition-point covariates with the final size as target, a distinct task (PROV-7), and its covariates could enrich this one; `wildfireia_initial_attack_failure` (unscreened): a cut of the natural fires with a size label; `forest_fires` (`Yes`): another source and target. External collections: none in our vocabulary; the Kaggle mirror is an older release of the same source (PROV-6), so build from the 6th edition.
- Better data: no new search; found through the gap scout for multiclass tasks.
- Papers and pages: Short 2014 (ESSD abstract read); Pourmohamad et al. 2024 (ESSD, FPA FOD-Attributes, offered for ML models); a 2026 BIO Web of Conferences paper on four broad US cause classes (search snippet only: tree models ahead on cross-validated accuracy, with a warning that the cause may be inferred partly from post-ignition attributes in the record); an ERL 2023 study of ignition causes in southern France (another source, not read).
- Metric: none found (the ESSD 2014 abstract, the Kaggle description, the search snippets; the 2026 paper's cross-validated accuracy is one paper's habit, not read), so the fallback `log_loss` (MET-1, MET-5, MET-8). Inputs: none.
- Risks for /add-dataset: NWCG_CAUSE_CLASSIFICATION (human or natural) coarsens the target and NWCG_CAUSE_AGE_CATEGORY is filled for human causes only, both go (LEAK); fire, ICS-209, MTBS and complex names can spell the cause and go or are checked; containment date and final size are known only later, so the prediction point (at discovery, or when the record is closed) decides whether they stay (USE, LEAK); federal, state and local source systems fill causes differently (`Class-dependent Recording` to probe, LEAK-13); the class set (12 named causes; the undetermined rows dropped); 2.3 million rows (a 1M version or a year range).
- Priority: gap + (multiclass is thin), use case 0 (no source names an actor or decision), source + (USFS data archive and ESSD paper), shape + (millions of fires, categorical, date and numeric columns, 29 years), risk - (columns that spell or coarsen the cause; the prediction point to settle).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for multiclass tasks.
- as published: about 2.3 million wildfire records (Zenodo: >2.2 million in CONUS), 1992-2020; one record per fire with discovery date and time, lat/lon, state/county, reporting agency, unit and land owner, cause ...; target: NWCG_GENERAL_CAUSE (12 named causes such as debris and open burning, arson, equipment and vehicle use, lightning/natural, power lines, railroad, smoking, ...; access: open.
- Why: Federal compiled record of every reported US wildfire with an expert-determined cause; the 2017 Kaggle mirror already posed cause prediction as the task, and the FPA FOD-Attributes paper offers the data for predictive ML models. Rows to exclude: undetermined causes as the unlabeled pool; drop final size and ...
- Adds: A large, open multiclass task with a temporal (29 years) and grouped (agency, state, unit) structure and mixed types (high-cardinality categoricals, dates, coordinates, numerics); a first environmental hazard multiclass task
