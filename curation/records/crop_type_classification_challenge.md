---
unique_name: crop_type_classification_challenge
name: Crop Type Classification Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/geoai-hack-2022/data
source_row: 1012
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Image`, SEL-13): every feature is a statistic of Sentinel-2 pixel values per field, a remote-sensing spectrum
that serves to recognise what the image shows (the satimage pattern).
- Source: Zindi "GeoAI Hack 2022 Crop Type Classification Challenge", a private hackathon for Tunisian participants (22-23
  April 2022), by IEEE Sup'Com GRSS and AGEOS with InstaDeep; field labels from an AGEOS ground survey in Kairouan,
  parcels digitised from VHR imagery. As published: Train.csv (13.6 MB) and Test.csv; features `timestepT_BAND_AGG` for
  24 shuffled dates (Nov 2020 - Apr 2021), 10 bands (B02-B12), 5 aggregations (mean, median, std, max, min); 13 crop
  classes ('olive+cereals', 'wheat', 'greenhouses', ...).
- Use case: crop-type mapping for agricultural policy (Zindi description); the prediction is made from imagery, and
  remote-sensing models (pixel and time-series classifiers) are the field's tool (SEL-12, SEL-13).
- Siblings: `geoai_challenge_for_cropland_mapping_in_dry_environments` (TBD -> Yes, Andrej) is a counter-precedent of
  the same family; `opengeoai_2023_hack` (TBD -> 2nd Tier), `telangana_crop_health_challenge` (TBD -> Yes, WIP).
  The curator may want one call for the satellite-feature Zindi challenges.
- Metric: log loss (Zindi: "The evaluation metric for this challenge is Log Loss"), deliberate (MET-4).
- Reject check (AI, 2026-10-22): stands. SEL-13 lists remote-sensing spectra: "AGG is the aggregation that was applied on the pixels values per field" over 24 Sentinel-2 dates x 10 bands (Zindi data page, https://api.zindi.world/v1/competitions/geoai-hack-2022); curator precedents crowdsourced_mapping (Landsat NDVI series -> land cover, Lennart and Andrej: Image), satimage, satellite, oil_spill. For the curator (consistency, not a refutation): geoai_challenge_for_cropland_mapping_in_dry_environments is TBD -> Yes (Andrej) on a similar satellite-feature setup; one call for the family.

Zindi GeoAI-Hack-2022 crop-type classification challenge. Crop-type mapping challenges are usually built on satellite remote-sensing data (e.g. Sentinel-2 multispectral pixels, often as time series of band reflectances), which is a geospatial/image modality and frequently spatio-temporal rather than a clean IID tabular task. If the released data are per-field tabular spectral/temporal aggregates with a categorical crop label it could be usable as tabular classification. A human must determine whether the features are raw imagery/time-series bands versus engineered tabular features, the label set, the size, and the appropriate (likely spatial) split.

---

classify crop type
