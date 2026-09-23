---
unique_name: africa_soil_property_prediction_challenge
name: Africa Soil Property Prediction Challenge (AfSIS, Kaggle 2014)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Wrong Domain / Source Modality
- Too Small
tags:
- AI-Filled (Verify)
- Many features
- Multi-target
- Tiny Data
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

Kaggle competition (2014) on AfSIS Phase I sentinel-site samples: predict five soil properties (Mehlich-3 Ca and P, pH, soil organic carbon, sand) from mid-infrared absorbance spectra plus a handful of remote-sensing covariates; metric MCRMSE. Sizes from the 2nd-place repo (CharlyBi/Soil-Prediction README): training 1,158, test 727; that solution downsampled the spectra by 8 to 391 features and ensembled small neural nets, noting "the training set and test set are relatively small in size". Exact spectral column count and covariate list not verified here (Kaggle page not fetchable).

The small, famous version of the OSSL question: same modality call as `open_soil_spectral_library`, and probably too small on its own. The samples come from clustered LDSF sentinel sites, so a random split leaks spatial structure; the site id is not in the Kaggle table (only in the AWS `s3://afsis/` georeferences), so the appropriate grouped split needs a join. Kaggle discussions not read. Data not inspected.

Drafted 2026-09-23 as a follow-up to `open_soil_data` (iSDA), whose 49k rows are 96% spectroscopy-model predictions; this is one of the measured-data parents of that family (`open_soil_spectral_library`, `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles`).

## Reference

Kaggle
