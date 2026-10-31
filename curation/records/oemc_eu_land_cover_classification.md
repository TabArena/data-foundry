---
unique_name: oemc_eu_land_cover_classification
name: 'OEMC Hackathon 2023: EU Land Cover Classification Dataset'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- Many class
- Many features
- AI-Filled (Verify)
original_source: Kaggle
year: '2023'
domain: environmental science & climate
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.8306554
- https://doi.org/10.7717/peerj.15478
- https://ec.europa.eu/eurostat/web/lucas
- https://www.kaggle.com/competitions/oemc-hackathon-eu-land-cover-classification
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: the OEMC hackathon's EU land-cover table (OpenGeoHub, 2023), 42,237 LUCAS field-survey points with 72 classes and 416 covariates, scored by weighted F1 on Kaggle; in-situ labels where the INEGI sibling has noisy map labels, but 342 of the 416 covariates are satellite products (optical reflectance, vegetation indices, land-surface temperature), the SEL-13 boundary that put satellite-only tables out.
- Source: Parente, Witjes and Hengl (OpenGeoHub Foundation) for the Open-Earth-Monitor (OEMC) project, Zenodo doi:10.5281/zenodo.8306554 (published 2023-09-01, CC BY 4.0), and the Kaggle community competition "OEMC Hackathon: EU Land Cover Classification" (deadline 2023-09-15, 31 teams). As published: train.csv 42,237 rows x 420 columns (sample_id, land_cover, land_cover_label, year and 416 covariates), test.csv 42,271 rows without labels; LUCAS points of 2006, 2009, 2012, 2015 and 2018; 72 level-3 classes. Header preview: 220 MODIS land-surface temperature columns, 84 Landsat GLAD ARD band columns, 38 MODIS vegetation columns (EVI, NDVI, bands), 47 CHELSA climate columns, and 27 others (accessibility to cities and ports, road, water and burned-area distance, elevation, slope, population, snow duration, human footprint).
- Use case: OpenGeoHub maps land cover for every unsampled location in Europe from such covariates (the competition: "classifying 72 multi-annual land cover classes for Europe using LUCAS ground-truth samples and Earth Observation data"); the decision a map serves is not named, so the fit is approximate. Regime grouped by location (spatial blocks; LUCAS revisits points across surveys) or temporal by survey year.
- Siblings and duplicates: `inegi_gcim_vegetation_mapping_challenge` (Zindi 2024, one tile in Mexico, noisy labels; `TBD -> 2nd Tier`, priority 2, the same SEL-13 boundary); `crowdsourced_mapping` (`No`, `Image`) and `crop_type_classification_challenge` (`No`, `Image`, SEL-13: every feature a Sentinel-2 pixel statistic) are the satellite-only precedents; `lucas_topsoil` uses the same LUCAS survey for soil properties (PROV-7, another task); `covertype` (accepted) classifies cover from cartographic covariates without spectra. External collections: none found.
- Better data: found as better data for `inegi_gcim_vegetation_mapping_challenge`; no further search this round.
- Papers and pages: the Zenodo record; the Kaggle competition and its discussion "evaluation metric" (topic 437301); Witjes et al. 2023, PeerJ, doi:10.7717/peerj.15478, cited for the covariate layers (not read).
- Metric: weighted F1, the competition's leaderboard metric; the organiser Martijn Witjes confirmed "sklearn.metrics.f1_score(average='weighted')" in topic 437301 (MET-4, a competition's choice on hard labels, kept); inputs none.
- Risks for /add-dataset: the SEL-13 call first (is the class recognised from the image, as in satimage, or predicted from a mixed stack in which climate, terrain and access count?); only the training file has labels, so 42,237 rows; 72 classes leave some with few points per fold (TP-5); spatial autocorrelation and revisited points need a spatial or point-grouped split (SPLIT-24); the covariates' periods must match each point's survey year.
- Priority: gap + (multiclass is thin), use case 0 (approximate), source + (a documented release and a competition), shape + (42k points, 416 covariates, five survey years), risk - (the SEL-13 doubt).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `inegi_gcim_vegetation_mapping_challenge`.
- as published: LUCAS survey points: train.csv 42,237 labelled rows, test.csv 42,271 rows (labels not published); sample_id, land_cover, land_cover_label, year + 416 covariates; survey years 2006, 2009, 2012, 2015, ...; target: land-cover class observed in the field at the LUCAS point; access: open.
- Why: same task as the INEGI record: a point's vegetation / land-cover class from Landsat composites, bioclimate (CHELSA), terrain and other covariates known without a field visit; same SEL-13 question (Landsat GLAD ARD and MODIS bands sit next to climate, terrain, distance, population and snow covariates)
- Adds: about 10x the rows, labels from an in-situ field survey instead of noisy map labels (the INEGI challenge's own problem), five survey years and a whole continent instead of one 150 km tile; documented Zenodo release with a CC BY 4.0 licence
