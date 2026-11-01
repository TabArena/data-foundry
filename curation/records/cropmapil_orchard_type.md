---
unique_name: cropmapil_orchard_type
name: CropMapIL Orchard Dataset - Multi-Temporal Sentinel-1/2 Features
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
tags:
- AI-Filled (Verify)
source_links:
- https://zenodo.org/records/17800953
- https://doi.org/10.1016/j.jag.2026.105495
- https://zenodo.org/records/17077905
- https://doi.org/10.3390/rs17243979
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-13): every input is a Sentinel-2 surface-reflectance band or a Sentinel-1 backscatter channel of the parcel, at 12 monthly time steps, used to recognise which orchard the parcel holds: the remote-sensing spectra SEL-13 names. The same call as `cropharvest_crop_noncrop` and `crop_type_classification_challenge` (both `No`, `Image`; their reject checks stood).
- Source: Fine, Paz-Kagan, Rozenstein (Ben-Gurion University of the Negev, Agricultural Research Organization), "CropMapIL Orchard Dataset - Multi-Temporal Sentinel-1/2 Features", Zenodo 17800953, v1.0 of 2025-12-03, CC BY 4.0; paper in the International Journal of Applied Earth Observation and Geoinformation (doi 10.1016/j.jag.2026.105495; not read, the publisher answered 403). As published (Zenodo page, read): "Each row corresponds to a single orchard sample (parcel-year)"; six yearly files orchards_2018.csv to orchards_2023.csv (agricultural years from October to September); `parcelID` (anonymised, stable across years), `crop_label` (12 orchard types: almond, apple, avocado, banana, citrus, date, jojoba, mango, nectarine/peach, olive, pomegranate, vineyard), `split`; Sentinel-2 "Bands used: b1, b2, b3, b4, b5, b6, b7, b8, b8a, b9, b11, b12" and Sentinel-1 `vv_asc`, `vv_desc`, `vh_asc`, `vh_desc`, each with `_t0` to `_t11`, "12 ordered timestamps (typically monthly composites over the year)"; "Sentinel-1 and Sentinel-2 features are derived from open Copernicus data". 106,413 rows from 19,950 parcels per the scout (the page gives no count).
- The deciding words: the columns are only image values (reflectance bands and radar backscatter per parcel and month), with no attribute measured on the orchard itself. SEL-13 counts "remote-sensing spectra" as image-derived "even when the columns are numeric"; SEL-15 names satimage and wilt as the counter-case of image values used to recognise what the image shows.
- Use case: crop-type maps for agricultural statistics and planning, made from imagery with remote-sensing models. Fit and split are moot under the reject (grouped by parcel, or leave-one-year-out as the paper's cross-year scenario, would fit).
- Siblings and duplicates: `opengeoai_2023_hack` (TBD -> 2nd Tier, `Image`), `cropharvest_crop_noncrop` (No, `Image`, this run), `crop_type_classification_challenge` (No, `Image`), `oemc_eu_land_cover_classification` and `inegi_gcim_vegetation_mapping_challenge` (TBD -> 2nd Tier, the SEL-13 boundary with some non-satellite covariates). `geoai_challenge_for_cropland_mapping_in_dry_environments` (TBD -> Yes, Andrej, no modality reason) is the counter-precedent already flagged on cropharvest: one call for the family. External collections: none found.
- Better data: found as better data for `opengeoai_2023_hack`; no further search this round.
- Links: Zenodo 17077905 and doi 10.3390/rs17243979 (Quintela, Campagnolo, Figueira 2025, Alqueva, Portugal) are another dataset the scout named, not this one's: move them from `source_links` to the comments (PROV-12).
- For the curator: if the satellite family is kept, this is a strong member (about 106k parcel-years, 12 classes, a peer-reviewed source, grouped by parcel or year) and would be `TBD -> Yes`, priority 3.
- Reject check (AI, 2026-10-31): stands. Zenodo 17800953: 'Each row corresponds to a single orchard sample (parcel-year)'. The only features are Sentinel-2 bands b1-b12 and Sentinel-1 vv/vh at _t0 to _t11, with no other attribute of the parcel. The page also says the release accompanies a manuscript that fuses very high-resolution aerial imagery with these series (https://zenodo.org/records/17800953). This is SEL-13's 'remote-sensing spectra' used to recognise what the image shows, SEL-15's satimage and wilt counter-case. Same facts as cropharvest_crop_noncrop (stood, rejectcheck_04) and crowdsourced_mapping (Lennart and Andrej: 'Image data'). geoai_challenge_for_cropland_mapping_in_dry_environments (Andrej, TBD -> Yes) stays flagged for one family call. Move Zenodo 17077905 and 10.3390/rs17243979 to the comments (PROV-12).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `opengeoai_2023_hack`.
- as published: 106,413 labelled parcel-year rows from 19,950 orchard parcels across Israel, agricultural years 2018-2023 (one CSV per year, 62-74 MB each); per row: anonymised parcelID (stable across years), ...; target: orchard type of a parcel in a year, 12 classes (almond, apple, avocado, banana, citrus, date, jojoba, mango, nectarine/peach, olive, pomegranate, vineyard); access: open.
- Why: the hackathon's task (classify olive parcels from Sentinel-2 time series at parcel level) on open per-parcel tabular features, with olive one of 12 classes; a second open set of the same kind and closer to the Tunisian olive task is Quintela, Campagnolo, Figueira 2025 (Remote Sensing 17(24):3979, Zenodo 17077905, CC ...
- Adds: about 106,000 labelled rows over six years instead of a 24-hour hackathon's few hundred parcels with access restricted to Tunisian participants; a peer-reviewed first publication, CC BY 4.0, the features already one row per parcel-year; parcelID and the year give a grouped or leave-one-year-out split (the paper's ...
