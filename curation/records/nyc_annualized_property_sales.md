---
unique_name: nyc_annualized_property_sales
name: NYC Citywide Annualized Calendar Sales Update
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
year: '2018'
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.cityofnewyork.us/City-Government/NYC-Citywide-Annualized-Calendar-Sales-Update/w2pb-icbu
- https://www.nyc.gov/site/finance/property/property-rolling-sales-data.page
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the NYC Department of Finance's annualized sales file, 845,607 recorded sales from 2016 to 2025 with coordinates and parcel ids, a newer and longer release of the source behind `nyc_property_sales` (PROV-6); its target still mixes market sales with $0 and nominal transfers (277,610 rows at $10,000 or less), the open point behind the curator's `No Good Target (yet)` there.
- Source: NYC Department of Finance (DOF), "NYC Citywide Annualized Calendar Sales Update" on NYC Open Data (w2pb-icbu, made public 2018-12-19, rows updated 2026-06-09): "Annualized sales file displays yearly sales information of properties sold in New York City." 29 columns: borough, neighborhood, building class category, tax class and building class as of the final roll and at the time of sale, block, lot, easement, address, apartment number, zip code, residential, commercial and total units, land and gross square feet, year built, sale price, sale date, latitude, longitude, community board, council district, BIN, BBL, census tract, NTA. Sales per year from 68,684 (2020) to 99,090 (2021) (Socrata counts, 2026-10-31). DOF's rolling-sales page says the annualized files begin in 2003; the portal table holds 2016-2025.
- Use case: none named by DOF (a list of sales). A real one: an assessor, lender or buyer estimates a property's market value before a sale, the hedonic sale-price task of `cook_county_residential_sales` and `king_county_home_sales_1999_2025` (both `TBD -> Yes`); written by the curation here, so the fit is approximate. Regime temporal by sale date.
- Siblings and duplicates: `nyc_property_sales` (Kaggle copy of one year of DOF rolling sales, 2016-2017; Lennart: `TBD -> 2nd Tier`, `No Good Target (yet)`) is an older cut of the same source, so the curator picks one (PROV-6); `valuation` (DOF assessment roll, the assessor's own value; `TBD -> 2nd Tier`) is another DOF table. External collections: none found.
- Better data: found as better data for `nyc_property_sales`; no further search this round.
- Papers and pages: the Open Data page; DOF's rolling-sales page (https://www.nyc.gov/site/finance/property/property-rolling-sales-data.page), whose glossary was not read.
- Metric: none found, so the fallback `rmse` on the price in dollars, with the target shipped on a log scale (MET-1, MET-3), as for the other sale-price records.
- Risks for /add-dataset: define the target population: drop non-market transfers ($0 and nominal prices; 277,610 of 845,607 rows at or below $10,000) by a documented rule, and decide on sales of several lots or units under one price (USE-5); building and tax class "as of final roll" may postdate the sale (LEAK-10 check); repeat sales of one BBL; about 568,000 sales stay above $10,000, near the 500k cap.
- Priority: gap 0, use case 0 (written by the curation), source + (the city's finance department, documented columns), shape + (845k sales over ten years, mixed columns, coordinates), risk - (a target that needs a filter; a version of a recorded source).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `nyc_property_sales`.
- as published: 845,607 sales, 2016-01-01 to 2025-12-31 (Socrata count query, 2026-10-30); the record's columns plus latitude, longitude, BBL, BIN, community board, council district, census tract; target: SALE PRICE (regression); access: open.
- Why: Same source and columns as the Kaggle copy in nyc_property_sales (one year of DOF rolling sales, 2016-2017), maintained by the publisher
- Adds: Ten years instead of one (about 10x the rows), coordinates and parcel ids for spatial features and a temporal split. Does not by itself settle 'No Good Target (yet)': the file still mixes non-arm's-length $0 and nominal transfers, which need a documented filter. Version of the same source (PROV-6)
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
