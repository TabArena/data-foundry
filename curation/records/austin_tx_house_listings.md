---
unique_name: austin_tx_house_listings
name: Austin, TX House Listings (features and images scraped from Zillow in January 2021)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2021'
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ericpierce/austinhousingprices
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: Austin homes scraped from Zillow in January 2021 for a student capstone, with the latest price (a sale or a listing) as target; a real valuation task, but a scrape with a mixed target in a family that has better-sourced housing records.
- Source: Kaggle ericpierce/austinhousingprices, "Austin, TX House Listings: Features and Images scraped in January 2021" (GPL-2.0; sources "Zillow via Apify.com"): "This data was originally sourced in support of my capstone project at Northwestern University"; "I used this data to predict home price using images in addition to the features in the datafile". As published: `austinHousingData.csv` (11.9 MB) and one image per home (`homeImages/`); version 1 holds the uncleaned data of "over 700 columns". The page gives no row count or column list (about 15,000 homes and 47 columns by the scout, to verify).
- Use case: a buyer, an agent or a platform values a home when it comes to market; the source names no actor beyond the uploader's own price model, fit approximate; regime temporal if the date of the latest price (2018-2021 by the scout) ships, else IID.
- Siblings and duplicates: `texas_real_estate_trends_2024` (`TBD -> 2nd Tier`); registry sales from other sources: `king_county_home_sales_1999_2025`, `cook_county_residential_sales`, `florida_dor_property_sales` (unscreened); no record of this upload (grep for austinhousingprices, ericpierce, Austin). External collections: none found.
- Better data: found as better data for `texas_real_estate_trends_2024`; no further search this round.
- Papers and pages: the Kaggle page only.
- Metric: none found (the page defines no metric), so the fallback `rmse`, on the log price if the curator agrees (MET-3, MET-8); inputs none.
- Risks for /add-dataset: the target mixes sale and listing prices (a price-source column, by the scout), so keep one kind (USE-5); Zillow-derived columns such as estimates or tax values would leak (LEAK-10); the uploader is the first publisher of a scrape (PROV-2); the image goes (SEL-12), the description is free text; drop street addresses.
- Priority: gap 0 (business & marketing, regression and the regimes are not thin), use case 0, source 0 (a Kaggle upload of a scrape), shape + (thousands of homes, mixed columns with text and dates), risk - (a mixed target, possible Zillow estimate columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `texas_real_estate_trends_2024`.
- as published: austinHousingData.csv (11.9 MB, about 15,000 Austin homes and about 47 columns as reported; to verify): listing description, latest price with its source and date (sales 2018-2021), home type, year ...; target: Latest price of the home (USD); access: open (Kaggle, GPL 2).
- Why: Same target (home price), same market (Texas), and the same feature mix the old record was kept for: structured attributes plus a free-text listing description.
- Adds: About 30 times the 500 rows of the Texas 2024 record, sale dates over 2018-2021 that allow a temporal split (the old record has none), coordinates and school data, and an untouched raw version to trace the cleaning. Risks: a Zillow scrape (PROV-2), and the price mixes sales and listing prices (latestPriceSource), so ...
