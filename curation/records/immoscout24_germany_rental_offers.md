---
unique_name: immoscout24_germany_rental_offers
name: Apartment rental offers in Germany (ImmoScout24 scrape)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '? (2020)'
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/corrieaar/apartment-rental-offers-in-germany
- https://github.com/corriebar/immoscout
- https://www.samples-of-thoughts.com/post/scraping-the-web-or-how-to-find-a-flat/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: three full scrapes (2018-09, 2019-05, 2019-10) of ImmoScout24 rental adverts by an individual; a real asking-rent task with a known scraper, but no task named, offers repeated across scrapes, and the platform's own research files (RWI-GEO-RED) cover the same adverts for longer.
- Source: Kaggle dataset `corrieaar/apartment-rental-offers-in-germany` by Corrie Bartelheimer, one file `immo_data.csv` (285 MB, file dated 2020-04-20), licence "copyright-authors". The card: "The data was scraped from Immoscout24 ... the data only contains offers for rental properties"; "At a given time, all available offers were scraped from the site and saved. This process was repeated three times, so the data set contains offers from the dates 2018-09-22, 2019-05-10 and 2019-10-08"; columns include living area, base and total rent, location (street, ZIP, state), energy type, two free texts (`description`, `facilities`) and the scrape `date`. Rows and columns not counted (commonly cited: about 269k offers x 49 columns). Scraper: github.com/corriebar/immoscout (R, no description); the blog post the card links did not resolve.
- Use case: a landlord or a portal sets or checks an asking rent from the listing's attributes; the card names no actor (its "Inspiration" asks descriptive questions: "Did rents increase over time? Which areas are the most expensive?"). Fit approximate (asking rents, not agreed rents). Regime: one snapshot per scrape date; three dates give at most two temporal windows (SPLIT-14), so IID within the snapshots, grouped by offer, is more likely; to settle at add.
- Siblings and duplicates: `apartment_for_rent_classified` (TBD -> 2nd Tier, unclear source; this record was found for it), `immoscout_german_house_prices` (Yes; sale offers on the same platform, a 2020 scrape; another target), `rwi_geo_red_houses_for_sale` (a candidate of this run: RWI's research files of all ImmoScout24 adverts since 2007; its record notes sibling files for apartments for rent, which would hold this task with documentation and advert dates), `kamernet_room_size` (TBD -> 2nd Tier). No duplicate (grep immoscout, corrieaar). External collections: none found.
- Better data: found as better data for `apartment_for_rent_classified`.
- Papers and pages: none besides the card and the repository.
- Metric: none found (the card and the repository state no task), so the fallback `rmse`, likely with the rent shipped on a log scale and scored on the original one (MET-3, MET-8; as `immoscout_german_house_prices`).
- Risks for /add-dataset: `totalRent` is the base rent plus service charge and heating, a copy of the target when the base rent is the target (LEAK-10); the same offer recurs across scrapes (LEAK-16, LEAK-17: dedupe or group); the free texts may state the rent (as in `apartment_for_rent_classified`); the card says the data belongs to ImmoScout24 and is "for research purposes only" (EV-4, no criterion).
- Priority: gap 0, use case 0 (none named), source 0 (an individual's scrape, documented by the card only), shape + (about 269k offers, mixed features, three dates), risk - (a target copy in `totalRent`, repeated offers).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `apartment_for_rent_classified`.
- as published: One rental offer per row; immo_data.csv 285 MB (Kaggle file listing); 'all available offers were scraped from the site ... the data set contains offers from the dates 2018-09-22, 2019-05-10 and ...; target: Monthly rent of the offer (base rent; total rent where given); access: registration.
- Why: The same target (asking monthly rent of an apartment listing) and use case as the UCI 'Apartment for Rent Classified' listings, with features of the same kind (living area, rooms, location, amenities, building data, a free-text description).
- Adds: A known source and scraping code (the UCI record is marked 'Missing source information'), about 2.7 times the rows of the 100k UCI file if the cited 269k count holds, and three dated scrapes that allow a temporal split; the price is a column, not only buried in boilerplate text. Not newer (2018-2019 against 2019). ...
