---
unique_name: cropharvest_crop_noncrop
name: 'CropHarvest: a global dataset for crop-type classification'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
tags:
- AI-Filled (Verify)
source_links:
- https://openreview.net/forum?id=JtjzUXPEaCu
- https://github.com/nasaharvest/cropharvest
- https://zenodo.org/record/5828893
- https://zenodo.org/record/7257688
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-13): every input is a satellite pixel time series (Sentinel-1 and Sentinel-2 bands with NDVI, ERA5 climate, SRTM elevation and slope) used to recognise what the pixel shows, crop or not: the remote-sensing spectra SEL-13 names. This is the same call as `crop_type_classification_challenge` (`No`, `Image`; its reject check stood).
- Source: Tseng, Zvonkov, Nakalembe, Kerner, "CropHarvest: A global dataset for crop-type classification", NeurIPS 2021 Datasets and Benchmarks (https://openreview.net/forum?id=JtjzUXPEaCu; PDF read from the proceedings, https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/54229abfcfa5649e7003b83dd4755294-Paper-round2.pdf). The code is at github.com/nasaharvest/cropharvest and the data on Zenodo (CC BY-SA 4.0). As published: 90,480 labels from 20 datasets in the paper (95,186 from 21 in the current README), of which 70,213 (74%) are paired with satellite data as arrays of 12 monthly timesteps x 18 bands. Every label is binary crop or non-crop; about a third also have a crop type.
- The deciding words: the dataset is "a crop dataset of geo-referenced labels with satellite data inputs, each consisting of latitude, longitude, the associated agricultural label, and a satellite pixel time series" (Sec. 3). "For each point label, the pixel with location nearest to the label location is selected ... For each label, a one-year time series with 12 timesteps is constructed, each representing an aggregated value over 30 days" (Sec. 3.2). The inputs are Sentinel-2 bands with NDVI, Sentinel-1 SAR, ERA5 precipitation and temperature, and SRTM elevation and slope.
- Use case: crop maps for food security and agricultural monitoring (Sec. 1-2), made from imagery with remote-sensing models. The paper trains an LSTM with pre-training or MAML; a random forest, "commonly used for remote sensing tasks", does well (Sec. 4.3-4.4). SEL-13 does not weigh that: the features are image values at a pixel.
- Siblings and duplicates: `crop_type_classification_challenge` (`No`, `Image`, SEL-13; its reject check cited the curators' precedents crowdsourced_mapping, satimage, satellite and oil_spill). `geoai_challenge_for_cropland_mapping_in_dry_environments` (`TBD -> Yes`, Andrej) has the same setup, a counter-precedent the curator may want to settle for the whole family. `telangana_crop_health_challenge` (`TBD -> Yes`) keeps only its tabular part. `cropmapil_orchard_type` and `oemc_eu_land_cover_classification` (new records of this run) belong to the same family.
- Better data: found as better data for `geoai_challenge_for_cropland_mapping_in_dry_environments` (the data-scouting run of 2026-10-30/31).
- Metric: the paper reports AUC ROC and F1 at a threshold of 0.5 on three evaluation tasks (Kenya, Brazil, Togo; Table 3), two metrics side by side (MET-5). The point is moot under the reject.
- For the curator: if the satellite-pixel family is kept (the geoai record), this record is its strongest member (70k labelled points across many countries, a peer-reviewed source, grouped by region or label source) and would be `TBD -> Yes`, priority 3.
- Reject check (AI, 2026-10-31): stands. Every row is 'a satellite pixel time series' of Sentinel-1/2 bands used to recognise crop or non-crop (Sec. 3, https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/54229abfcfa5649e7003b83dd4755294-Paper-round2.pdf), the 'remote-sensing spectra' SEL-13 names and SEL-15's satimage and wilt counter-case. Curator precedent crowdsourced_mapping (Landsat NDVI series; Lennart and Andrej: 'Image data'). The SEL-2 steelman, 'Random forests are commonly used for remote sensing tasks' (Sec. 4.3), is what SEL-13 already answers ('even when the columns are numeric'). geoai_challenge_for_cropland_mapping_in_dry_environments (Andrej, `TBD -> Yes`, no modality reason) contradicts the rule's text, so it is flagged, not followed: one call for the family.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `geoai_challenge_for_cropland_mapping_in_dry_environments`.
- as published: 95,186 labelled points from 20+ published datasets worldwide; 70,213 (74%) paired with satellite and climate data, each an array of 12 monthly steps x 18 bands (Sentinel-1, Sentinel-2, ERA5, SRTM ...; target: crop vs non-crop of a point (binary; the package's default task), crop type where labelled; access: open.
- Why: same task and features as the Zindi challenge: binary cropland classification of points from Sentinel-1 and Sentinel-2 time series (the challenge scores accuracy on points in Fergana and Orenburg); CropHarvest also holds dry-region points
- Adds: about 70,000 points with satellite inputs across many countries instead of one challenge's two test regions, a peer-reviewed first publication with documented label sources, and an open CC BY-SA 4.0 licence; label datasets give a grouped split by region or source
