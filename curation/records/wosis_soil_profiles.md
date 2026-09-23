---
unique_name: wosis_soil_profiles
name: WoSIS snapshot 2023 (World Soil Information Service, ISRIC)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Multi-target
- Non-IID (Grouped)
- Larger IID Data
collections:
- New (BeyondArena)
original_source: Website
year: '2023'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.17027/isric-wdcsoils-20231130
- https://essd.copernicus.org/articles/16/4735/2024/
- https://www.isric.org/explore/wosis
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Batjes et al., Earth System Science Data 16:4735, 2024: ISRIC's standardised global soil profile database, snapshot 2023 with 228,000 georeferenced profiles from 174 countries, >900,000 layers, >6 million records; standardised chemical (organic/total/inorganic C, N, P, pH, CEC, EC) and physical (texture, bulk density, coarse fragments, water retention) properties. Snapshot distributed under CC BY 4.0; some sources stay internal or embargoed. Coverage is skewed: North America 35%, Oceania 19%, Europe 17%, Asia 3%; 54% sampled 1980-2020 and "almost 27% lack documented sampling dates".

Largest measured-label source for a digital-soil-mapping regression (points + covariates -> properties, spatially blocked split), but a legacy compilation: heterogeneous methods harmonised after the fact, many layers per profile, no covariates shipped, and it contains `africa_soil_profiles_database` (and much of what the iSDA maps trained on), so choose one of the two. Data not inspected.

Drafted 2026-09-23 as a follow-up to `open_soil_data` (iSDA), whose 49k rows are 96% spectroscopy-model predictions; this is one of the measured-data parents of that family (`open_soil_spectral_library`, `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles`).

## Reference

Batjes NH, Calisto L, de Sousa LM (2024). Providing quality-assessed and standardised soil data to support global mapping and modelling (WoSIS snapshot 2023). Earth System Science Data 16:4735-4765.
