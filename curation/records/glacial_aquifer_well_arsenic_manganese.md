---
unique_name: glacial_aquifer_well_arsenic_manganese
name: Groundwater data, predictor variables, and rasters used for predicting the probability of high arsenic and high manganese in the Glacial Aquifer ...
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2021'
domain: environmental science & climate
problem_type: Binary Classification
source_links:
- https://doi.org/10.5066/P94FCZJ2
- https://doi.org/10.1021/acs.est.0c06740
- https://www.sciencebase.gov/catalog/item/5f21cf8982cef313ed94004a
- https://data.usgs.gov/datacatalog/data/USGS:5f21cf8982cef313ed94004a
- https://catalog.data.gov/dataset/groundwater-data-predictor-variables-and-rasters-used-for-predicting-the-probability-of-hi
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a USGS data release of 10,001 glacial-aquifer wells in 25 northern US states with a measured arsenic exceedance (and 14,565 with manganese), 79 site and well predictors and the authors' train/test assignment, published with an ES&T paper; the predictors include other models' outputs (predicted pH, redox, nitrate, groundwater age) to check, and it likely contains the wells of `minnesota_well_arsenic`.
- Source: Elliott, Erickson & Reddy, "Groundwater data, predictor variables, and rasters used for predicting the probability of high arsenic and high manganese in the Glacial Aquifer System, northern continental United States", USGS data release, 2021 (doi 10.5066/P94FCZJ2, registered 2021-04-06), with Erickson et al., "Machine-Learning Predictions of High Arsenic and High Manganese at Drinking Water Depths of the Glacial Aquifer System, Northern Continental United States", Environ Sci Technol 2021 (doi 10.1021/acs.est.0c06740). As published (FGDC metadata, read 2026-10-31): files `as.txt`, `mn.txt`, `DataDictionary.csv`, two RDS model files, an R script, `modelgeoref.txt`, `readme.txt`; `as.txt` columns SiteID, As (µg/L), X_Albers and Y_Albers ("snapped to the center of a 2-kilometer grid"), WellDepth, "Columns 6 through 84: Predictor Variables", Data ("Indicates if the record belongs in the training or testing dataset"), As10 (the target, As > 10 µg/L) and Pred (the model's predicted probability); "The resultant dataset consisted of 10,001 As and 14,565 Mn measurements"; "In instances when more than one measurement of As and/or Mn was available for a site, only the value obtained from the most recent sampling was retained", so one row per well; samples 1988-2018 (time-period metadata); water-quality data compiled from state and local agencies, USGS NWIS and EPA SDWIS (Wilson et al. 2019); "A total of 108 predictor variables were originally considered ... After model refinement, a total of 79 and 55 predictor variables were used".
- Use case: a state drinking-water programme, a driller or a domestic well owner, before a well is tested or drilled, decides whom to prompt to test or how deep to screen; the abstract: "over 200 million people are chronically exposed to arsenic (As) and/or manganese (Mn) from drinking water", with predictions at "depth surfaces that represent moving median depths of GLAC domestic and public supply wells", but no actor named (our reading); fit approximate. Regime IID by well, as the source's train/test assignment (how it was drawn is in the unread paper); spatial clustering on the 2-km grid is a question for the split (SPLIT-1, SPLIT-26); no sample date ships, so no temporal split (SPLIT-7).
- Siblings and duplicates: `minnesota_well_arsenic` (`TBD -> Yes`, priority 2; USGS release doi 10.5066/F77H1HH8, 3,283 Minnesota glacial-aquifer wells, the same team and target): likely a subset of these wells, to check by site before both enter (PROV-4, PROV-6); `water_quality` (`No`, `AHDS`, an imaginary table), the record this was found next to; `water_quality_and_potability` (`No`, generated); `arsenic_male_bladder` and `arsenic_male_lung` (exposure and cancer, another task). External collections: not searched (web search budget used up).
- Better data: found as a related task next to `water_quality` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the FGDC metadata (data.usgs.gov/datacatalog/metadata/USGS.5f21cf8982cef313ed94004a.xml); Erickson et al. 2021, abstract via OpenAlex (the ACS full text refused scripted fetches); Wilson et al. 2019 for the water-quality compilation.
- Metric: not established, since the paper's text could not be read; the abstract stresses "a successful approach to significantly improve ML prediction sensitivity for imbalanced data sets", which suggests a threshold metric whose threshold is to be read (MET-6); without it, the fallback `roc_auc` (MET-1, MET-8); inputs none. Read the paper before the definition (PROV-17).
- Risks for /add-dataset: drop `Pred` (the authors' model output) and `As` (the measurement behind the target) (LEAK-10); "predicted nitrate", "predicted pH" and "predicted anoxic conditions" are other models' outputs: check whether those models were fit on these wells' own samples (LEAK-27) and which measurements of the same water sample they rest on (LEAK-10); the 79 kept predictors were chosen "after model refinement" on these wells (prefer the 108 considered if they can be rebuilt, CLEAN-8); the manganese table is a second target on overlapping wells (one target per dataset, or a second record, PROV-7); the overlap with `minnesota_well_arsenic`; ScienceBase blocks scripted downloads (use a browser).
- Priority: gap 0 (environmental science and binary not thin), use case 0 (no actor named), source + (USGS release with FGDC metadata and a paper), shape + (10,001 wells x 79 predictors, mixed), risk − (predictors from other models).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `water_quality`.
- as published: Groundwater well samples in the glacial aquifer system of 25 northern US states, 1988-2018: 10,001 arsenic and 14,565 manganese measurements (measurements, not distinct wells; the well count is not ...; target: Arsenic above 10 ug/L (the EPA maximum contaminant level), binary; a second target in the same release is manganese above 300 ug/L; access: open.
- Why: The record's file is made up ('created from imaginary data'), and its label is a threshold on its own contaminant columns. The real form of the question 'is this drinking water safe' is to predict an exceedance of a health limit before testing, from site and well attributes. This release has that question with ...
- Adds: Real lab measurements instead of imaginary values, about three times the wells of minnesota_well_arsenic (3,283 wells, proposed by scout_61 for water_quality_and_potability, same USGS team, and its Minnesota wells probably fall inside this glacial-aquifer compilation), 25 states and 30 years, and two contaminants. ...
