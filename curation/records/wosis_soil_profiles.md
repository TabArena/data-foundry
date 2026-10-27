---
unique_name: wosis_soil_profiles
name: WoSIS snapshot 2023 (World Soil Information Service, ISRIC)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
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

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 3: ISRIC's global database of measured, standardised soil profiles; documented and large, but the source defines no task, ships no covariates, and contains `africa_soil_profiles_database`.
- Source: ISRIC - World Soil Information, WoSIS snapshot 2023 (DOI 10.17027/isric-wdcsoils-20231130), described in Batjes, Calisto and de Sousa, Earth System Science Data 16:4735-4765, 2024; as published (ESSD abstract, read 2026-10-22): "quality-assessed and standardised data for 228 000 geo-referenced profiles", "from 174 countries", "more than 900 000 soil layers (or horizons)", "over 6 million records" of chemical (carbon, pH, phosphorus, CEC, ...) and physical (texture, bulk density, water retention, ...) properties grouped by comparable analytical method; distributed as a static snapshot and through web services ("wosis_latest"); profile, layer and attribute tables to join. Coverage skewed to North America, Oceania and Europe (the old note's shares, from the paper).
- Use case: the source's purpose is to "support digital soil mapping" (abstract), as the training points of SoilGrids; no prediction task is defined. Candidates: a property at a location from covariates (the covariates are not shipped, a remote-sensing join), or a pedotransfer function (a costly property such as CEC, bulk density or water retention from routine ones such as texture and organic carbon), which soil surveys use; fit approximate either way. Regime grouped: layers of one profile, and spatial blocks.
- Siblings and duplicates: `africa_soil_profiles_database` (`TBD -> 2nd Tier`, priority 3) is ingested by WoSIS: keep one; `lucas_topsoil` (`TBD -> Yes`, EU survey, also partly in WoSIS), `open_soil_data` (`No`, mostly model predictions), `open_soil_spectral_library`, `africa_soil_property_prediction_challenge` are the same family. External collections: none found.
- Papers and pages: the ESSD paper; ISRIC's WoSIS page; SoilGrids uses it.
- Metric: none found (ESSD abstract, ISRIC WoSIS page), so the fallback (rmse).
- Risks for /add-dataset: the target and inputs are ours to define (SEL-3, USE); joins of profile and layer tables; methods harmonised after the fact across decades; "almost 27% lack documented sampling dates"; overlap with AfSP and LUCAS (PROV-6); per-provider licences (no criterion, EV-4).
- Priority: gap + (a grouped regime is thin), use case 0 (none in the source), source + (an ESSD data paper and an institution's DOI), shape + (228k profiles, many properties, grouped structure), risk - (no defined target, joins, overlap with siblings).

Batjes et al., Earth System Science Data 16:4735, 2024: ISRIC's standardised global soil profile database, snapshot 2023 with 228,000 georeferenced profiles from 174 countries, >900,000 layers, >6 million records; standardised chemical (organic/total/inorganic C, N, P, pH, CEC, EC) and physical (texture, bulk density, coarse fragments, water retention) properties. Snapshot distributed under CC BY 4.0; some sources stay internal or embargoed. Coverage is skewed: North America 35%, Oceania 19%, Europe 17%, Asia 3%; 54% sampled 1980-2020 and "almost 27% lack documented sampling dates".

Largest measured-label source for a digital-soil-mapping regression (points + covariates -> properties, spatially blocked split), but a legacy compilation: heterogeneous methods harmonised after the fact, many layers per profile, no covariates shipped, and it contains `africa_soil_profiles_database` (and much of what the iSDA maps trained on), so choose one of the two. Data not inspected.

Drafted 2026-09-23 as a follow-up to `open_soil_data` (iSDA), whose 49k rows are 96% spectroscopy-model predictions; this is one of the measured-data parents of that family (`open_soil_spectral_library`, `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles`).

## Reference

Batjes NH, Calisto L, de Sousa LM (2024). Providing quality-assessed and standardised soil data to support global mapping and modelling (WoSIS snapshot 2023). Earth System Science Data 16:4735-4765.
