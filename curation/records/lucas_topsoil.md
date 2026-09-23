---
unique_name: lucas_topsoil
name: LUCAS Topsoil Survey (EU, 2009 / 2015 / 2018)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
- Multi-target
- Non-IID (Grouped)
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: GOV Website
year: '2018'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://esdac.jrc.ec.europa.eu/projects/lucas
- https://esdac.jrc.ec.europa.eu/content/lucas-2018-topsoil-data
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

EU-wide harmonised topsoil survey run by JRC/ESDAC: 2009/2012 (19,967 points, 25 countries), 2015 (21,859, all 28 member states), 2018 ("18,984 samples", EU + UK), 2022 in release. Measured pH, organic carbon, N, P, K, carbonates, texture, CEC, EC, oxalate Fe/Al; VisNIR spectra for 2015 (also in OSSL as LUCAS). Repeated visits to the same points make a temporal split (2009+2015 -> 2018) possible; otherwise spatially grouped.

Access terms, noted only and not a factor in the verdict: data are "free of charge" after a request form, but the 2018 terms say results must go through "proper aggregation process that prevents any individual body from being identified", "geographic location of samples cannot be detectable on maps", and data are "restricted to licensee organization staff", i.e. no redistribution as-is; OSSL carries LUCAS spectra only "with geographic restrictions". On the data itself this is a strong candidate: measured laboratory values, ~19-22k points per wave, repeated visits, spatial or temporal split. To check: usable size per wave after cleaning, target choice, covariate join. Data not inspected.

Drafted 2026-09-23 as a follow-up to `open_soil_data` (iSDA), whose 49k rows are 96% spectroscopy-model predictions; this is one of the measured-data parents of that family (`open_soil_spectral_library`, `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles`).

## Reference

Orgiazzi A, Ballabio C, Panagos P, Jones A, Fernandez-Ugalde O (2018). LUCAS Soil, the largest expandable soil dataset for Europe: a review. European Journal of Soil Science 69(1):140-153. Fernandez-Ugalde O et al. (2022). LUCAS 2018 Soil Module. EUR 31144 EN, doi:10.2760/215013.
