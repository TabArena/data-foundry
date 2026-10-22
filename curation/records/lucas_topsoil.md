---
unique_name: lucas_topsoil
name: LUCAS Topsoil Survey (EU, 2009 / 2015 / 2018)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
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

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: the EU's measured topsoil survey, documented by the JRC, a spatial (grouped) regression. The task and the covariate join still have to be chosen.
- Source: JRC/ESDAC LUCAS Soil module. Waves: 2009/2012 (about 20k points), 2015 (about 22k), 2018. The 2018 page: "Topsoil data for 18,984 points", most at 0-20 cm, with pH (CaCl2, H2O), organic carbon, CaCO3, N, P, K, EC and oxalate Fe/Al; texture and bulk density come as separate packages. Point coordinates and observed land cover are in the Eurostat LUCAS survey and join on `POINT_ID`; covariates for 2015 ship with that wave, and 2018 covariates are "in preparation". Access needs a request form; the terms (no sub-licensing, no maps that reveal locations) are noted, not weighed (EV-4).
- Use case: digital soil mapping. The JRC predicts topsoil properties at unsampled locations for EU soil and climate policy (organic-carbon and nutrient maps, e.g. Ballabio et al. 2016 and 2019, built from LUCAS). The actor (JRC, national agencies) and the decision (policy maps) come from that literature, not from a statement in the release, so the fit is approximate. Regime: grouped by location (spatial blocks), or temporal across waves for the revisited points.
- Siblings and duplicates: `open_soil_data` (iSDA; mostly spectroscopy predictions), `open_soil_spectral_library` (carries LUCAS spectra), `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `wosis_soil_profiles` (WoSIS includes LUCAS profiles: check overlap). None is a duplicate of the EU survey itself. External collections: OSSL (spectra, with geographic restrictions).
- Papers and pages: Orgiazzi et al. 2018 (EJSS 69:140-153, the review of LUCAS Soil); Fernandez-Ugalde et al. 2022 (EUR 31144 EN, doi:10.2760/215013, the 2018 module); Ballabio et al. 2016 (Geoderma, texture maps from LUCAS).
- Metric: none found as one deliberate choice. The mapping papers report RMSE, R2 and others side by side, so the fallback applies (MET-5). Inputs: none.
- Risks for /add-dataset: the features. Lab properties predicting each other is a discovery table (SEL-3), spectra lean out (SEL-15, raw spectral bins), and covariates need a join from Eurostat or the 2015 covariate package (heavy joins). Also the choice of one target among several (`Multi-target` until one is picked, CLEAN-18), and which wave to use.
- Priority: gap + (Grouped regime thin), use case - (approximate; actor from the literature), source + (JRC documentation and papers), shape + (about 19-22k points per wave, spatial structure), risk - (covariate join and target choice).

EU-wide harmonised topsoil survey run by JRC/ESDAC: 2009/2012 (19,967 points, 25 countries), 2015 (21,859, all 28 member states), 2018 ("18,984 samples", EU + UK), 2022 in release. Measured pH, organic carbon, N, P, K, carbonates, texture, CEC, EC, oxalate Fe/Al; VisNIR spectra for 2015 (also in OSSL as LUCAS). Repeated visits to the same points make a temporal split (2009+2015 -> 2018) possible; otherwise spatially grouped.

Access terms, noted only and not a factor in the verdict: data are "free of charge" after a request form, but the 2018 terms say results must go through "proper aggregation process that prevents any individual body from being identified", "geographic location of samples cannot be detectable on maps", and data are "restricted to licensee organization staff", i.e. no redistribution as-is; OSSL carries LUCAS spectra only "with geographic restrictions". On the data itself this is a strong candidate: measured laboratory values, ~19-22k points per wave, repeated visits, spatial or temporal split. To check: usable size per wave after cleaning, target choice, covariate join. Data not inspected.

Drafted 2026-09-23 as a follow-up to `open_soil_data` (iSDA), whose 49k rows are 96% spectroscopy-model predictions; this is one of the measured-data parents of that family (`open_soil_spectral_library`, `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles`).

## Reference

Orgiazzi A, Ballabio C, Panagos P, Jones A, Fernandez-Ugalde O (2018). LUCAS Soil, the largest expandable soil dataset for Europe: a review. European Journal of Soil Science 69(1):140-153. Fernandez-Ugalde O et al. (2022). LUCAS 2018 Soil Module. EUR 31144 EN, doi:10.2760/215013.
