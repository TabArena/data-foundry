---
unique_name: zooscan_pelgas_copepods
name: Zooscan Plankton
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://www.kaggle.com/datasets/raghavdharwal/pelgass-bay-of-biscay-zooscan-zooplankton-dataset
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-13): copepod taxa recognised from ZooScan images, whose tabular part is the morphological and grey-level descriptors "automatically extracted on each individual image by the Zooprocess", with a few sampling columns beside them; image descriptors used to recognise what the image shows.
- Source: Grandrémy et al., "PELGAS Bay of Biscay ZooScan zooplankton Dataset (2004-2016)", SEANOE, March 2023, https://doi.org/10.17882/94052 (CC BY 4.0); data paper Grandremy et al., "Metazoan zooplankton in the Bay of Biscay: a 16-year record of individual sizes and abundances obtained using the ZooScan and ZooCAM imaging systems", ESSD 16:1265-1282 (2024), https://doi.org/10.5194/essd-16-1265-2024. As published: 1,153,507 objects (zooplankton, parts, particles and artefacts) in 127 taxonomic and morphological groups, a 71-column TSV with a field descriptor and a taxonomy descriptor, and one image per object; "Each object is described by 46 morphological and grey level based features ... automatically extracted on each individual image by the Zooprocess"; identified "using the web based application Ecotaxa with built-in, random forest and CNN based, semi-automatic sorting tools followed by expert validation or correction". The Kaggle link is a 2026 re-upload of the SEANOE files by `raghavdharwal`; the source is SEANOE (PROV-8). MulTaBench core (Table 3; App. D.2, F.1): 100,000 objects of 10 copepod taxa, 18 Zooprocess descriptors (grey-level spread, mode and max, circularity, skewness, percent area, fractal dimension, symmetries, thickness ratio and others) with latitude, longitude, date, time, depth, bottom depth, volume, mesh and subsample fraction, and the image; "features were extracted directly from the image, and removing them increased the image importance" (App. D.2).
- Decisive: SEL-13 names "morphological, geometric or spectral descriptors from an image-analysis pipeline", and descriptors "stay image-derived when mixed with a few non-visual columns"; the label is what the image shows. Precedents: `dry_bean_dataset`, `wdbc`, `satimage` (`No`, `Image`).
- Steelman: the ZooScan community did sort such objects with random forests on the Zooprocess features (Gorsky et al. 2010; EcoTaxa), a tabular model on image descriptors; SEL-13 rules out that case by name, and EcoTaxa now adds CNNs on the images.
- Use case: a plankton ecologist sorts imaged objects into taxa before counting abundances, a real decision; the scope rule decides here, not the use case.
- Siblings and duplicates: no record of this data (grep by ZooScan, PELGAS, EcoTaxa). External collections: MulTaBench core, as "Zooscan Plankton".
- Better data: a candidate of the benchmark MulTaBench (the run searched no further).
- Metric: none found at the source (a data publication; MulTaBench reports AUC as a benchmark convention).
- Reject check (AI, 2026-10-31): stands. SEANOE: 'Each object is described by 46 morphological and grey level based features ... automatically extracted on each individual image by the Zooprocess' (https://doi.org/10.17882/94052), and the label is what the image shows: the case SEL-13 names ('descriptors from an image-analysis pipeline', 'mixed with a few non-visual columns') with `wdbc` and `dry_bean` as precedents. Steelman checked (SEL-2): random forests on Zooprocess features were the field's tool, but the source sorts with 'random forest and CNN based' tools, so in practice the image is used.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 100,000 rows; 28 structured, 0 text, 1 image features (MulTaBench Table 3); target: Copepod taxon (10 classes).
- Why: Classify the copepod taxon of a ZooScan-imaged specimen from image, morphometrics and sampling metadata
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Subsample of 1,153,507 ZooScan objects from the Ifremer PELGAS surveys 2004-2016 (EcoTaxa-sorted); Kaggle re-upload 2026, original data publication not confirmed ...
