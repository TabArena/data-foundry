---
unique_name: africa_soil_profiles_database
name: Africa Soil Profiles Database (AfSP v1.2, ISRIC)
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
collections:
- New (BeyondArena)
original_source: Website
year: '2014'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://data.isric.org/geonetwork/srv/api/records/b88870b4-6af8-4e78-a3ac-38871d757525
- https://files.isric.org/public/afsp/AF-AfSP1.2.zip
- https://isric.org/projects/africa-soil-profiles-database-afsp
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 3: measured legacy soil profiles for Sub-Saharan Africa from ISRIC, documented and large, but with no target the source defines and contained in WoSIS.
- Source: ISRIC - World Soil Information, Africa Soil Profiles Database v1.2, November 2014, for the AfSIS project (Leenaars, van Oostrum and Ruiperez Gonzalez, ISRIC Report 2014/01); as published (ISRIC metadata record, read 2026-10-22): "18,532 unique soil profiles", "Soil analytical data are available for 15,564 profiles of which 14,197 are georeferenced", "profile site and layer attribute data", values "standardized according to SOTER conventions", reliability "subjectively rated, at the profile level, 1-4"; a 34.7 MB zip (AF-AfSP1.2.zip, served, not opened): profile and layer tables to join.
- Use case: no task in the source: it is a compilation for digital soil mapping. Candidate tasks: properties at a location from covariates (needs a remote-sensing join, not shipped), or a pedotransfer function (a costly property, such as CEC or water retention, from cheap ones, such as texture and organic carbon), which soil surveys use; fit approximate either way; regime grouped by profile (layers of one profile) or spatial blocks.
- Siblings and duplicates: `wosis_soil_profiles` (`TBD -> 2nd Tier`) ingests AfSP: keep one; `open_soil_data` (iSDA, mostly model predictions), `africa_soil_property_prediction_challenge`, `open_soil_spectral_library`, `lucas_topsoil` are the same family. External collections: none found.
- Papers and pages: ISRIC Report 2014/01; the AfSIS and iSDA soil maps trained on it.
- Metric: none found (the ISRIC metadata record and project page define no task), so the fallback (rmse).
- Risks for /add-dataset: the target and the task are ours to define (SEL-3, USE); joins of site and layer tables; methods harmonised after the fact across decades of surveys; many layers per profile (grouped split); licence CC BY-NC 3.0 noted (no criterion, EV-4).
- Priority: gap + (a grouped regime is thin), use case 0 (none in the source), source + (an institution's report and metadata), shape + (15,564 analysed profiles, many properties, grouped structure), risk - (no defined target, joins, overlap with WoSIS).

ISRIC compilation of legacy soil profiles for Sub-Saharan Africa, made for the AfSIS project (Leenaars, van Oostrum & Ruiperez Gonzalez, ISRIC Report 2014/01). Metadata record: "18,532 unique soil profiles", "soil analytical data are available for 15,564 profiles of which 14,197 are georeferenced", 37 countries, published 2014-11-03. Licence per the same record: "Attribution-NonCommercial 3.0 International (CC BY-NC 3.0)"; noted, not a factor at this stage. Measured laboratory values (the point where `open_soil_data` fails), but a profile/layer database from many surveys spanning decades, with no covariates: a digital-soil-mapping task needs the remote-sensing join and a spatially blocked split. WoSIS (`wosis_soil_profiles`) ingests AfSP, so the two are not independent; decide which one to keep. Data not inspected.

Drafted 2026-09-23 as a follow-up to `open_soil_data` (iSDA), whose 49k rows are 96% spectroscopy-model predictions; this is one of the measured-data parents of that family (`open_soil_spectral_library`, `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles`).

## Reference

Leenaars JGB, van Oostrum AJM, Ruiperez Gonzalez M (2014). Africa Soil Profiles Database, Version 1.2. A compilation of georeferenced and standardised legacy soil profile data for Sub-Saharan Africa (with dataset). ISRIC Report 2014/01, Wageningen.
