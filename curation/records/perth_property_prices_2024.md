---
unique_name: perth_property_prices_2024
name: Perth Property Prices (Kaggle, heptix)
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
- https://www.kaggle.com/datasets/heptix/perth-property-prices
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 42,958 sold Perth properties (2006-2024, three quarters of them in 2022-2024) with sale price, date, type, location, schools and agency, in an undocumented Kaggle scrape; it holds the dearer sales and the property types that `perth_house_prices` lacks, but the scraped site is not named.
- Source: Kaggle user heptix, "Perth Property Prices" (subtitle "Perth house sales across more than 300 suburbs."), one file `perth_property_data.csv` created 2024-12-07, CC BY-SA 4.0, no description and no source named (Kaggle API metadata). As published (a preview of the file): 42,958 rows x 21 columns: `Listing_ID` (unique; nine-digit numbers in the form of realestate.com.au listing ids, not confirmed), `Price`, `Agency_Name`, `Postcode`, `Address`, `Suburb`, `Longitude`, `Latitude`, `Property_Type` (house 35,691, apartment 2,467, villa 1,942, unit 1,299, townhouse 1,038, five rarer types), `Bedrooms`, `Bathrooms`, `Parking_Spaces`, `Date_Sold` (2006-06-13 to 2024-08-09), `Land_Size`, the nearest primary and secondary school with distance and ICSEA, `Distance_to_CBD`; 203 suburbs (not 300); prices from $1 to $6.35M, 1,163 above the $2.44M cap of `perth_house_prices`; no floor area and no build year.
- Use case: a seller, buyer or agent values a Perth property before the sale (written by the curation; the page names none); fit approximate (one portal's sold listings, selection unknown); regime temporal because prices drift and the sale date ships (SPLIT-6). The years are lopsided (2,000 sales in 2020, 9,085 in 2022, 14,039 in 2023, 8,738 in 2024 to August), so the test windows sit in 2023-2024.
- Siblings and duplicates: `perth_house_prices` (`Yes`, in the v0.2 working copy: syuzai's scrape of house.speakingsame.com, 1988-2020, capped at $2,440,000; its review used this file to measure the cap and called it "a separate candidate"). Another scrape of another site, so its own record and no duplicate (PROV-4); the curator decides which one enters. External collections: none found.
- Better data: found as better data for `perth_house_prices` (the data-scouting run of 2026-10-30/31); no further search this round.
- Papers and pages: the Kaggle page only; no paper, notebook or competition.
- Metric: none found (the Kaggle page has no description or task, and there is no competition), so the fallback `rmse` on the price (MET-8; a log-scale target is the definition's choice, MET-3); inputs none.
- Risks for /add-dataset: provenance under PROV-2 (an identifiable first upload, the scraped portal unnamed: confirm it from the listing ids); prices of $1 and other placeholders; the school ICSEA and distances are the values at the scrape, not at the sale (a weak potential leak, as kept in `perth_house_prices`); which sales the scrape kept per suburb (recent sales dominate); repeated addresses (41,531 distinct of 42,958) are resales, a question for the split (SPLIT-13).
- Priority: gap 0 (business and real estate, regression and temporal are not thin), use case 0 (written by the curation), source 0 (an undocumented Kaggle scrape), shape + (42,958 sales, 20 mixed features, sale dates).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `perth_house_prices`.
- as published: One CSV, perth_property_data.csv, 8.8 MB, created 2024-12-07, CC BY-SA 4.0; subtitle 'Perth house sales across more than 300 suburbs'; per the perth_house_prices review it has the property type, ...; target: Sale price of a Perth property; access: open.
- Why: Same target, units and city as perth_house_prices; the record's review panel named it as 'a separate candidate' and used it to measure the $2.44M truncation (1.5% of 2015-2020 sales cost more)
- Adds: No truncation at $2,440,000 (the record's known gap), exact dates instead of month and year, the property type, a scrape four years newer. Caution: the page has no description and names no scraped site, so provenance (PROV-1) must be settled from the columns before it can enter
