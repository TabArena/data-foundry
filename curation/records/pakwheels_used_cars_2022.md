---
unique_name: pakwheels_used_cars_2022
name: Pakistan's Largest Automobile Listing - PakWheels (October 2022)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2022'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/muhammadwaqargul/pakwheels-used-car-dataset-october-2022
- https://www.pakwheels.com/
- https://www.kaggle.com/datasets/asimzahid/pakistans-largest-pakwheels-automobiles-listings
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: about 90,000 PakWheels used-car ads scraped in October 2022 with the asking price and 15 listing fields, including the ad URL, a last-updated date and the seller's description; a later scrape of the platform behind `used_cars_pakistan`.
- Source: Kaggle upload by Muhammad Waqar Gul, "Pakistan's Largest Automobile Listing - PakWheels" (dataset 2536551, one file `pakwheels.csv` of 57 MB created 2022-10-10, CC BY-NC-SA 4.0; Kaggle metadata read 2026-10-31): "The dataset was scraped from pakwheels.com. It contains almost 90,000 records with 17 different features": `ad_url`, `title`, `location`, `model_year`, `price`, `mileage`, `engine_type`, `transmission`, `registered_in`, `color`, `assembly`, `engine_capacity`, `body_type`, `ad_last_updated`, `car_features`, `description`. The page suggests a model "which predicts the price of the car, which could be deployed and used by the owners to know the worth of their cars". Rows not counted (no download).
- Use case: a seller or the platform sets an asking price when a car is listed; the upload names owners as users, without a decision; fit approximate (asking price, not sale price). Regime IID (one scrape; `ad_last_updated` is an update date, not a listing date).
- Siblings and duplicates: `used_cars_pakistan` (AI `TBD -> Yes`, priority 2: 72,655 PakWheels ads scraped in 2021, 10 columns) is the same platform at another time, a version of the same source (PROV-6): the curator picks one; ads online in both scrapes may overlap. A 2021 scrape in schema.org JSON (Kaggle asimzahid) is a third version, without a record. Other used-car records: `fiat_500` (`Yes`), `used_cars_dataset_cardekho`, `used_cars_24`, `used_cars_saudi_arabia`, `used_cars_benz_italy`, `autoscout24_car_listings_2025`. External collections: none found.
- Better data: found as better data for `used_cars_pakistan`; no further search this round.
- Papers and pages: the Kaggle page; no paper.
- Metric: none found (a Kaggle dataset without a task), so the fallback `rmse`, likely with the price on a log scale (MET-3, MET-8).
- Risks for /add-dataset: the free-text `description` and `title` may state the price or a phone number: scrub or drop them (LEAK-10; personal data); re-listed cars through `ad_url`; check the price format; how the scraper chose the ads is not described (PROV-2).
- Priority: gap 0, use case 0, source 0 (an uploader's scrape described in a paragraph), shape + (about 90,000 ads with numeric, categorical, list and text fields), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `used_cars_pakistan`.
- as published: pakwheels.csv (57 MB): 'almost 90,000 records with 17 features' as published: ad_url, title, location, model_year, price, mileage, engine_type, transmission, registered_in, color, assembly, ...; target: Asking price of a used car (PKR); access: open (Kaggle, CC BY-NC-SA 4.0).
- Why: Same platform, target and use case as used_cars_pakistan (the 2021 PakWheels scrape), with the same features plus more of the same kind known at listing time.
- Adds: About 90,000 listings against 72,655, one and a half years newer, body type, colour, the list of fitted features, a free-text description and the ad date (a temporal split becomes possible), and the ad URL to remove re-listed cars. A later, independent scrape of the same platform: treat it as a version and pick one ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
