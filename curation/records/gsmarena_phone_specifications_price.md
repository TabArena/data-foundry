---
unique_name: gsmarena_phone_specifications_price
name: GSMArena Mobile Phone Devices (10,000+ device specifications scraped from GSMArena)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
original_source: Kaggle
domain: technology & internet
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/msainani/gsmarena-mobile-devices
- https://www.gsmarena.com
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a real scrape of GSMArena's phone catalogue (10,000+ models, 86 fields) whose approximate launch price could be a target, but the uploader poses no task, the price field is GSMArena's rough note, and spec-to-price scrapes have gone to the second tier (`laptops`, the curator's call).
- Source: Kaggle upload "GSMArena Mobile Phone Devices" by msainani (https://www.kaggle.com/datasets/msainani/gsmarena-mobile-devices, CC0, "Updated on June 23, 2020"; one file gsm.csv, 10.8 MB), "scraped using rvest, htmltab, and xml2 libraries in the R programming language" from gsmarena.com (scraper on the uploader's GitHub, cigarplug/scrape-gsma). As published: "116 unique phone brands and 10,000+ phone models with 86 different specification fields"; the description names no task or target. Target as the record proposes: the launch price (GSMArena's approximate price note), missing for some models (columns not inspected). Kaggle is the source under PROV-8 (the table first appeared there; gsmarena.com is where the content comes from).
- Use case: a manufacturer or retailer prices a new model from its specification at launch; the source names none; fit approximate (GSMArena's price is an editor's approximation, not a list price); regime temporal (by announcement year) or IID.
- Siblings and duplicates: `mobile_price_classification` (`No`, generated, AHDS); the spec-to-price precedents `laptops` (curator: `TBD -> 2nd Tier`, `No Good Target / Scientific Discovery`), `laptop_prices_dataset` and `mobile_phone_market_in_ghana` (both `TBD -> 2nd Tier`, priority 1, AI screenings); `dpreview_camera_specifications_price` (another spec-to-price scrape of this run). A newer scrape (madajaswanth, 2025, 8,461 phones x 35 attributes with retail price where available, MIT; https://www.kaggle.com/datasets/madajaswanth/phone-dataset-8461-phones, moved here from source_links as another upload, PROV-12) has the same origin and task (PROV-6 if both were recorded). External collections: none known.
- Better data: no new search; found as better data for `mobile_price_classification`.
- Papers and pages: the Kaggle page (metadata read through the API); the scraper's repository (not read).
- Metric: none found (the Kaggle description poses no task); fallback `rmse` on the price (MET-1, MET-8). Inputs: none.
- Risks for /add-dataset: the price column (format, currency, share missing, launch or later price) is unchecked (an unclear target); 86 text fields to parse (memory, camera, battery as strings); variants of one model as near-duplicate rows; the announcement year to parse for a temporal split.
- Priority: gap 0 (technology and regression are not thin), use case 0 (none named), source 0 (an individual's scrape without documentation of the fields), shape + (10,000+ models, mixed fields), risk - (an unclear price target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `mobile_price_classification`.
- as published: 10,000+ phone models from 116 brands x 86 specification fields, one file gsm.csv, CC0; the price column (GSMArena's approximate launch price in EUR) is not checked and is missing for some models; a ...; target: launch price (or price class, as in the record); access: open.
- Why: the same target and features (RAM, storage, battery, camera, screen, network) as mobile_price_classification, which was judged generated; these are real catalogue entries
- Adds: real phones, five times the rows, launch years for a temporal split; note the precedent for spec-to-price scrapes is 2nd Tier (laptops, laptop_prices_dataset, mobile_phone_market_in_ghana)
