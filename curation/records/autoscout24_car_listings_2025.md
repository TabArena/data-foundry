---
unique_name: autoscout24_car_listings_2025
name: AutoScout24 Car Listings Dataset (2025 snapshot, several European markets)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 1
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2025'
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/clkmuhammed/autoscout24-car-listings-dataset
- https://www.autoscout24.com/
- '# another upload (AutoScout24 Germany 2023, wspirat), not this dataset'
- https://www.kaggle.com/datasets/wspirat/germany-used-cars-dataset-2023
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 1: about 120,000 car listings from AutoScout24 in several European markets (snapshot of 2025-11-08) with about 80 columns; a large, current form of the listing-price task, from a scrape, with personal fields and a price-derived column to drop.
- Source: Kaggle clkmuhammed/autoscout24-car-listings-dataset, "AutoScout24 Car Listings Dataset" (MIT as declared; sources "AutoScout24 scraped data"): "Contains ~120K listings across multiple European markets"; one file `autoscout24_dataset_20251108.csv` (549 MB). Columns (data card): listing id, description, seller ratings, price with VAT and negotiable flags and `price_net`, VIN, make, model, version, mileage, first registration, production year, body, seats, doors, colours, power, transmission, gears, drive train, cylinders, displacement, weight, fuel and CO2 figures, four equipment lists, `is_used`, `is_new`, `is_preregistered`, accident, service history, previous owners, rental, emission standard, offer type, country, zip, city, street, coordinates, seller type and company name, warranty.
- Use case: a seller, a dealer or the marketplace prices a car when listing it ("Regression for price prediction", data card); no actor named, fit approximate; regime IID within one snapshot (the card lists no listing date), the country a possible group.
- Siblings and duplicates: `fiat_500` (`Yes`), `used_cars_benz_italy`, `used_cars_24`, `used_cars_dataset_cardekho` (`TBD -> 2nd Tier`), `us_used_cars_cargurus` and `pakwheels_used_cars_2022` (unscreened): other scrapes, no duplicate. An AutoScout24 Germany 2023 upload (Kaggle wspirat) is another scrape of the same platform, without a record. External collections: none found.
- Better data: found as better data for `fiat_500` and `used_cars_benz_italy`; no further search this round.
- Papers and pages: the Kaggle page only.
- Metric: none found (the page defines no metric), so the fallback `rmse`, on the log price if the curator agrees (MET-3, MET-8); inputs none.
- Risks for /add-dataset: `price_net` and the VAT fields are computed from the target (drop, LEAK-10); keep used cars offered for sale (`is_used`, `offer_type`); personal fields (street, VIN, seller company name, the free-text description) are dropped before anything leaves the machine; seller ratings accrue after the listing; the uploader is the first publisher of a scrape (PROV-2); check the country mix and duplicate listings.
- Priority: gap 0 (business & marketing and regression are not thin), use case 0, source 0 (a Kaggle upload of a scrape), shape + (about 120,000 listings, about 80 mixed columns), risk - (a target-derived column, personal fields).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `fiat_500`, `used_cars_benz_italy`.
- as published: autoscout24_dataset_20251108.csv (549 MB): '~120K listings across multiple European markets' as published, about 80 columns: price (EUR, VAT and negotiable flags), make, model, model version, first ...; target: Listed price of a used car (EUR); access: open, open (Kaggle, MIT as declared by the uploader).
- Why: Same target and use case as used_cars_benz_italy (asking price of a second-hand car from its listing), all brands including Mercedes-Benz, with AutoScout24 Italy among its markets (country mix to verify), and features of the same kind plus condition and equipment. | Same target and use case as fiat_500, a crawled ...
- Adds: About 7 times the rows and 10 times the features of the 16,392-row Benz Italy scrape, 2025 instead of 2023, a named platform instead of unnamed Italian sites, and a country column for a grouped split. Risks: personal data (street, seller company, VIN, description) to drop; new and pre-registered cars to filter ...
