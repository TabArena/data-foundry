---
unique_name: portugal_real_estate_listings
name: Real Estate Listings in Portugal (asking prices from Portuguese real estate websites)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Kaggle
year: '2024'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: over 100,000 Portuguese property listings with asking price, type, energy certificate, several area measures, rooms, location and publish date, scraped and updated weekly by a named Kaggle uploader from portals the page does not name.
- Source: Kaggle user luvathoms, "Real Estate Listings in Portugal" (slug `portugal-real-estate-2024`), MIT licence, "weekly updated"; the page: "more than 100k real asking prices for real estate properties listed on Portuguese real estate websites. The data was legally and ethically scraped from several online platforms"; its source field: "publicly available real estate websites that list properties across Portugal" (Kaggle API metadata). As published: one file `portugal_listinigs.csv` (24.0 MB, file dated 2026-10-31), columns per the page: `Price` (euros), `District`, `City`, `Town`, `Type` ("Apartment, House, Garage, Land"), `EnergyCertificate`, `GrossPrivateArea`, `UsableArea`, `LivingArea`, `LotSize`, `BuiltArea`, `Rooms`, `Bedrooms`, `Bathrooms`, `WCs`, `Floor`, `Parking`, `Garage`, `Elevator`, `ElectricCarsCharging`, `ConstructionYear`, `PublishDate`. Rows and date range not checked (no preview taken).
- Use case: a seller or agent sets the asking price of a dwelling when listing it, or a portal shows a price estimate (written by the curation; the page names analyses, not a decision); fit approximate (asking prices, not sales; portals unnamed); regime temporal by `PublishDate` (SPLIT-6).
- Siblings and duplicates: `lisbon_house_prices` (`TBD -> Yes`, `Missing source information`, `Tiny Data`: 246 Lisbon listings, the record this was found for); the other Portuguese records (`wholesale_customers_portugal`, `bank_marketing`, `pkdd_15_taxi_trip_time_prediction_ii`) are other tasks; no duplicate. External collections: none found.
- Better data: found as better data for `lisbon_house_prices` (the data-scouting run of 2026-10-30/31); no further search this round.
- Papers and pages: the Kaggle page only.
- Metric: none found (no task or competition on the page), so the fallback `rmse` on the price (MET-8; the target's scale is the definition's choice, MET-3); inputs none.
- Risks for /add-dataset: PROV-2 (an identifiable first upload, the portals unnamed); the same property listed on several portals would sit in train and test (look for near-duplicates by location, areas and price); the weekly updates change the file, so pin a snapshot; keep dwellings only (garages and land are listed); several overlapping area columns with gaps.
- Priority: gap 0 (business and real estate, regression and temporal are not thin), use case 0 (written by the curation), source 0 (an undocumented scrape), shape + (over 100,000 listings, mixed features, a publish date).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `lisbon_house_prices`.
- as published: listings; 'more than 100k real asking prices'; one CSV of 23.9 MB (portugal_listinigs.csv); about 25 columns: Price, District, City, Town, Type, EnergyCertificate, GrossPrivateArea, UsableArea, ...; target: Price (asking price in euros) of a listed property; access: registration.
- Why: The same target and use case as lisbon_house_prices (asking price of a Lisbon dwelling from area, rooms, bathrooms, parish, condition, year of construction), with features of the same kind, over all Portuguese districts with Lisbon as a subset.
- Adds: Over 400 times the rows (more than 100k against 246), recent listing dates (PublishDate) for a temporal split, the energy certificate and several area measures. Same weakness as the old record: the portals are not named, so PROV-2 applies (an identifiable first upload, scraped). The data is weekly updated, so a ...
