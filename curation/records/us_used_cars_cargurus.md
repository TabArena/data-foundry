---
unique_name: us_used_cars_cargurus
name: US Used cars dataset (3 million CarGurus listings, September 2020)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 1
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2020'
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ananaymital/us-used-cars-dataset
- https://www.cargurus.com/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 1: about 3 million US used-car listings crawled from CarGurus in September 2020 with their asking price; the largest real listing-price table found, from an uploader's own crawler with little documentation, one of many used-car records.
- Source: Kaggle ananaymital/us-used-cars-dataset (Ananay Mital, 2020-09-21; one file `used_cars_data.csv`, 9.98 GB; licence "copyright-authors"); the card: "The dataset contains 3 million real world used cars details"; "This data was obtained by running a self made crawler on Cargurus inventory in September 2020"; "This data is for academic, research and individual experimentation only and is not intended for commercial purposes"; "Imagine a web app that can estimate the listing price of a vehicle". As published (the run's Assessment, not checked here): 3,000,040 rows x 66 columns, among them listed date, days on market, VIN, make, model, trim, year, mileage, engine, horsepower, fuel, body type, colours, owner count, accident and title flags, dealer and location, a free-text description and the price.
- Use case: a dealer or the marketplace sets or checks the asking price when a car is listed; the card names a price-estimating app, no actor; fit approximate (the asking price at crawl time, not a sale price); regime temporal by listing date, or IID within the one-month snapshot, to decide.
- Siblings and duplicates: `dvm_car_uk_used_car_adverts` (`TBD -> Yes`, priority 3, documented UK adverts), `used_cars_pakistan`, `used_cars_saudi_arabia` (`TBD -> Yes`, priority 2), `autoscout24_car_listings_2025` (`TBD -> Yes`, priority 1), `used_cars_24`, `used_cars_benz_italy`, `used_cars_dataset_cardekho` (`TBD -> 2nd Tier`), `cars` (`No`), `dvm_car_prices` (`No`, Duplicate); no used-car price dataset is accepted yet. No duplicate (another market and crawl). External collections: none found.
- Better data: found as better data for `cars`, `used_cars_24`, `used_cars_saudi_arabia` (the run's Assessment); no further search this round.
- Papers and pages: the Kaggle card only; no paper found.
- Metric: none found (the card names none), so the fallback `rmse` on the price, with the target shipped on a log scale if the add stage chooses (MET-1, MET-3, MET-8).
- Risks for /add-dataset: 10 GB (a documented 1M subsample); days on market and any field updated after listing are not known at listing time (LEAK, USE-3); VIN, listing and dealer ids are ids; the description may state the price or hints of it (text column); asking prices of one crawl, with possible re-listings (duplicates by VIN); the research-only terms (EV-4: no reason for a verdict); the crawler and its coverage are undocumented (PROV-2).
- Not checked: the row and column counts and the column list (a 2.3 GB zip, not downloaded).
- Priority: gap 0 (business & marketing has 25 accepted, regression not thin), use case 0 (no actor), source 0 (a crawler upload without a codebook), shape + (3 million rows, mixed types, dated), risk - (undocumented crawl, post-listing columns, size).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `cars`, `used_cars_24`, `used_cars_saudi_arabia`.
- as published: used_cars_data.csv (10 GB): '3 million real world used cars' as published (reported 3,000,040 rows x 66 columns; to verify): listed date, days on market, VIN, make, model, trim, year, mileage, ...; target: Listed price of a used car (USD); access: open (Kaggle download, research-only terms), open download (Kaggle), research-only terms.
- Why: Same target and use case as used_cars_24 and used_cars_saudi_arabia, with features of the same kind and many more known at listing time; the largest real used-car listing table found. | cars predicts the price of used 2005 GM cars from make, model, trim, body type, cylinders, engine size, doors, mileage and options ...
- Adds: Three million listings against a few thousand, a listing date for a temporal split, history flags (accidents, owners, salvage) the small scrapes lack, a description column for the text-plus-table case. Risks: 10 GB, listing terms 'Data files (c) Original Authors' and 'academic, research and individual experimentation ...
