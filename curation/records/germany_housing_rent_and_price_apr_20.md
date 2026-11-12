---
unique_name: germany_housing_rent_and_price_apr_20
name: Germany Housing - Rent and Price data set - Apr 20
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 1
tags:
- AI-Filled (Verify)
- Free Text (Sentences)
original_source: Kaggle
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/phanindraparashar/germany-housing-rent-and-price-data-set-apr-20
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the Kaggle page and a download of the price file. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-01):** `TBD -> Yes`, priority 1: a larger, cleaner ImmoScout24 scrape (April 2020, the portal's own codes) of the asking-price task immoscout_german_house_prices ships; a candidate to replace it, not to sit beside it (the curator, 2026-11-01, on the PR #37 board: keep the current one, add this as a record).
- Source: Kaggle dataset `phanindraparashar/germany-housing-rent-and-price-data-set-apr-20`, uploaded 2020-04-30 by phanindraparashar, Apache 2.0; the card has no description beyond its title ("Germany Housing - Rent and Price data set - Apr 20", keyword "real estate"), so how and when the pages were scraped is not stated. Files: `apr20_price.csv` (46,262 houses for sale, 83 columns: ImmoScout24's expose variables with the API codes as values, `URL = /expose/<id>`), `apr20_price_33_col.csv`, `apr20_rental_no_duplicates.csv` and `apr20_rent_33_col.csv` (rentals, a second task), `train_price_micro_macro.csv` and `train_rent_micro_macro.csv` (the uploader's added area features), `zip_lat_lang.csv`. The portal's own documented archive is RWI-GEO-RED (FDZ Ruhr, on application), record `rwi_geo_red_houses_for_sale`.
- As published (price file, read 2026-11-01): one row per listing, unique `obj_scoutId`, no exact duplicate rows; target `obj_purchasePrice` (median 380,000 EUR, 153 below 10,000: price on request); features: state, district, zip code and place, living space, lot, rooms, floors, year built and last refurbished, condition, interior quality, building type, heating, energy class and type, cellar, parking, new building, construction phase, the listing text (`beschreibung`, German), picture count, the seller (`obj_cId`, 12,243 sellers), Telekom internet offers at the address.
- Use case: a seller or an agent sets the asking price of a house from the houses on the market (the curation's reading, as for the sibling; the source names none); fit approximate (an asking price, not a sale price); regime IID: one snapshot of the market, as for the sibling.
- Siblings and duplicates: `immoscout_german_house_prices` (the July 2020 scrape on OpenML 43342, 10,552 houses, in the TabArena v0.2 working copy): 3,548 of its houses (34%) are in this file, matched on state, living space, lot, rooms, year built and price (research of 2026-10-31); its English labels are permuted, this file carries the codes. Two scrapes of one portal three months apart overlap: ship one (PROV-4 to PROV-7). The rental files are the task of `immoscout24_germany_rental_offers` (`TBD -> 2nd Tier`, three 2018-2019 scrapes of rental adverts).
- Better data: `rwi_geo_red_houses_for_sale` (`TBD -> Yes`, priority 3, screened 2026-10-31): every house advert on ImmoScout24 since 2007, documented and dated, a scientific-use file on application only; where access is granted it holds the task with far more houses and years, and this scrape is the open alternative. Found as better data for `immoscout_german_house_prices` (4.4 times its houses, the portal's codes, three months earlier).
- Papers and pages: no paper; two Kaggle notebooks (a starter and an untitled kernel of 2020-07-01); no discussion.
- Metric: none (no task was posed; the card is empty), so a stand-in from the context as for the sibling: RMSLE on the price (MET-1).
- Risks for /add-dataset: `obj_purchasePriceRange` is the price in 11 bins (Spearman 0.992 with the price) and `obj_pricetrend`, `obj_pricetrendbuy`, `obj_pricetrendrent` may be the portal's price indices: leaks (LEAK); 3,221 listings of home builders (`ga_cd_customer_group`) and 4,651 houses still `projected` are catalogue offers rather than houses (USE-7); 6,253 listings share their text's first 200 characters with another (templated builder and agent texts, near copies across the split, LEAK-16); a seller with up to 806 listings and project ids (`obj_project_id`, `obj_groupnumber`) are groups to check (SPLIT); tracking and Telekom columns (`ga_cd_*`, `obj_telekom*`) carry no property information; price on request (153 rows).
- Priority: gap 0 (business & marketing, regression and IID are not thin), use case 0 (written by the curation), source 0 (an undocumented scrape), shape + (46,262 houses, mixed numeric, categorical, geographic and text features), risk - (the price-derived columns, the builder catalogue, the overlap with the sibling; better data on application, RWI); 1 is the floor.
