---
unique_name: dvm_car_prices
name: DVM Car Prices
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://deepvisualmarketing.github.io/
- https://www.kaggle.com/datasets/osamasaifs/dvm-car-with-images
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-6): a 100,000-row cut of the DVM-CAR Ad table with one photo per advert, taken from a Kaggle re-upload of DVM-CAR; the same source and the same target as `dvm_car_uk_used_car_adverts`, which records the first publication.
- Source: DVM-CAR, Huang, Chen, Luo, Yue and Ounis, "DVM-CAR: A large-scale automotive dataset for visual marketing research and applications", IEEE Big Data 2022 (https://deepvisualmarketing.github.io/; arXiv 2109.00881); the Ad table holds "more than 0.25 million used car advertisements" in the UK. The Kaggle copy osamasaifs/dvm-car-with-images: "This dataset originates from the DVM-Car dataset and has been uploaded without preprocessing or data cleaning." As used by MulTaBench (extended release, Joint Signal only; https://huggingface.co/datasets/multabench/extended-img-reg-dvm-car): "Advertisement records from the DVM-CAR collection of the UK used car market, each paired with a photograph of the vehicle", 100,000 rows: the Ad table's `Maker`, `Genmodel`, `Adv_year`, `Adv_month`, `Color`, `Reg_year`, `Bodytype`, `Runned_Miles`, `Engin_size`, `Gearbox`, `Fuel_type`, `Seat_num`, `Door_num`, the image table's `Predicted_viewpoint` and `Quality_check`, the photo, target `Price`.
- Why out: `dvm_car_uk_used_car_adverts` (this run, found as better data for six used-car records) holds the same Ad table from the first publication (the project page, figshare, the Big Data paper), with the target "advertised used-car price (GBP)"; this record is a subsample with a photo and two image-table columns joined, and the same task (PROV-4, PROV-6). The structured columns carry the signal (MulTaBench Table 8: structured R² 0.592, photo and text 0.357, joint 0.594), so the photo sets nothing apart. MulTaBench belongs in the canonical record's collections.
- Siblings and duplicates: canonical `dvm_car_uk_used_car_adverts`; used-car price records from other sources: `used_cars_saudi_arabia`, `used_cars_pakistan`, `used_cars_24`, `used_cars_dataset_cardekho`, `used_cars_benz_italy`. External collections: MulTaBench (extended image release).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the DVM-CAR project page and paper; the Kaggle re-upload; MulTaBench (https://arxiv.org/abs/2605.10616), Table 8.
- Reject check (AI, 2026-10-31): stands. Source confirmed in the copies' own words: the Kaggle upload 'originates from the DVM-Car dataset and has been uploaded without preprocessing or data cleaning' and MulTaBench describes 'Advertisement records from the DVM-CAR collection of the UK used car market' (https://deepvisualmarketing.github.io/). Same Ad table and price target as `dvm_car_uk_used_car_adverts`; the joined photo is dropped in a tabular container, so it adds no task. Put MulTaBench on the canonical record's collections.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 100,000 rows; 14 structured, 1 text, 1 image features (MulTaBench Table 9); target: Advertised price.
- Why: Predict a UK used-car advert's price from vehicle attributes and a photo
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. DVM-CAR (Deep Visual Marketing, Huang et al.); Kaggle 2025 re-upload.
