---
unique_name: africa_soil_property_prediction_challenge
name: Africa Soil Property Prediction Challenge (AfSIS, Kaggle 2014)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
- Many features
- Multi-target
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2014'
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/afsis-soil-properties
- https://github.com/CharlyBi/Soil-Prediction
- https://registry.opendata.aws/afsis/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a documented AfSIS spectroscopy task with a clear lab use case, but the inputs are raw mid-infrared spectral bins (SEL-15, weighed against) and about 1,158 samples.
- Source: Kaggle competition "Africa Soil Property Prediction Challenge" (afsis-soil-properties), opened 2014-08-27, closed 2014-10-21, 1,231 teams, research category; data from the Africa Soil Information Service (AfSIS) Phase I, 2009-2013, "Georeferenced samples were collected from 19 countries in Sub-Saharan African" (AWS registry page, managed by QED, ODbL). As published: train.zip 13.3 MB and test.zip 8.4 MB (Kaggle file list, not opened); 1,158 training and 727 test samples per the 2nd-place README (CharlyBi/Soil-Prediction); five targets (Mehlich-3 Ca, P, pH, SOC, Sand) from "diffuse reflectance infrared spectroscopy measurements" plus a Topsoil/Subsoil indicator and a few covariates (column count not verified).
- Use case: a soil laboratory replaces costly wet chemistry by a spectral prediction: "The two types of data can be paired to form a training dataset for machine learning", so "certain soil properties can be predicted through cheaper spectral methods" (AWS registry); fit direct for the lab, but the task is chemometrics on spectra; regime grouped: topsoil and subsoil of one location and samples clustered in sentinel sites, while the site id is not in the Kaggle table (only in the AfSIS georeferences on S3).
- Siblings and duplicates: same family as `open_soil_spectral_library` (`TBD -> 2nd Tier`, `Wrong Domain / Source Modality`; OSSL ingests AfSIS spectra, so the two overlap), `africa_soil_profiles_database` (`TBD -> 2nd Tier`), `lucas_topsoil` (`TBD -> Yes`), `open_soil_data` (`No`, model predictions, Andrej and Lennart); Zindi `amini_soil_prediction_challenge` is related soil work, not checked. External collections: none found.
- Papers and pages: Kaggle competition and discussions (not read); 2nd-place solution README; Stanford CS229 2014 project (Akinola and Dowd) on the same five properties (PDF not reachable).
- Metric: "Mean Columnwise Root Mean Squared Error" over the five targets (Kaggle API `evaluation_metric`); a leaderboard metric (MET-4); inputs none. A single-target definition would score the RMSE of that target, the column of the MCRMSE.
- Risks for /add-dataset: spectral modality (SEL-15, "Raw spectral bins" weigh against; follow the precedent of `open_soil_spectral_library`); five targets (Multi-target: pick one or keep the MCRMSE); the grouping key needs a join to the AfSIS georeferences (SPLIT); the old `Too Small` marker is dropped: about 1,158 regression samples is no `Too Small` under TP-5 without a measurement.
- Priority: gap 0 (environmental science and regression not thin; the grouped key is not in the table), use case + (AfSIS states the spectral-for-wet-chemistry use), source + (AfSIS/QED and Kaggle document it), shape 0 (about 1,158 rows of one feature type), risk - (spectral modality, grouping join, five targets).

Kaggle competition (2014) on AfSIS Phase I sentinel-site samples: predict five soil properties (Mehlich-3 Ca and P, pH, soil organic carbon, sand) from mid-infrared absorbance spectra plus a handful of remote-sensing covariates; metric MCRMSE. Sizes from the 2nd-place repo (CharlyBi/Soil-Prediction README): training 1,158, test 727; that solution downsampled the spectra by 8 to 391 features and ensembled small neural nets, noting "the training set and test set are relatively small in size". Exact spectral column count and covariate list not verified here (Kaggle page not fetchable).

The small, famous version of the OSSL question: same modality call as `open_soil_spectral_library`, and probably too small on its own. The samples come from clustered LDSF sentinel sites, so a random split leaks spatial structure; the site id is not in the Kaggle table (only in the AWS `s3://afsis/` georeferences), so the appropriate grouped split needs a join. Kaggle discussions not read. Data not inspected.

Drafted 2026-09-23 as a follow-up to `open_soil_data` (iSDA), whose 49k rows are 96% spectroscopy-model predictions; this is one of the measured-data parents of that family (`open_soil_spectral_library`, `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles`).

## Reference

Kaggle
