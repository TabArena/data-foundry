---
unique_name: taiwan_actual_price_registration_sales
name: Real estate actual price registration, batch open data (sales, presale and rental transactions), Ministry of the Interior, Taiwan
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: business & marketing
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://plvr.land.moi.gov.tw/DownloadOpenData
- https://data.gov.tw/en/datasets/18703
- https://data.gov.tw/en/datasets/77051
- '# a district-year cut of the same register, republished by New Taipei City (Luzhou District sales, 2014)'
- https://data.gov.tw/en/datasets/170343
- '# a Kaggle re-upload (title only, no description or source)'
- https://www.kaggle.com/datasets/sunny9999/house-price-taipei
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: Taiwan's national register of real-estate transaction prices (Ministry of the Interior, registration since August 2012), most likely the upstream of the 414-row `real_estate_valuation`; hundreds of thousands of sales a year with building attributes, a large build with detail-table joins and price columns to handle.
- Source: Department of Land Administration, Ministry of the Interior (MOI), batch open data of the actual-price registration (plvr.land.moi.gov.tw/DownloadOpenData; data.gov.tw 77051 for the current release, published on the 1st, 11th and 21st of each month, and 18703 for past seasons, "provided since 2012"; Open Government Data License 1.0, attribution required). As published: one zip per season with CSV files per county and type (sales `_a`, presale `_b`, rentals `_c`), building, land and parking detail tables per type, and schema files (schema-main-sale, -build, -land, -park). The 2025 Q2 zip (its listing and the Taipei header read) holds 81,004 sale rows across counties; the main sale file has 33 columns: district, transaction object (land, building, parking), a de-identified address range, land and building areas, zoning, transaction date (ROC calendar), floor and total floors, building type, main use, material, completion date, rooms, halls and baths, management organisation, elevator, total price, unit price per m2, parking type, area and price, a remarks field, serial number.
- Use case: an appraiser, a lender's automated valuation or a buyer estimates a dwelling's price per m2 from its registered attributes at the transaction date; the MOI publishes the register for price transparency and names no predictive use; fit direct for the valuation of a dwelling sale. Regime temporal: sales from 2012 to 2026, and prices drift with the market (`real_estate_valuation` was split by time).
- Siblings and duplicates: `real_estate_valuation` (`No`, DF: Yes, deprecated; UCI 2018, 414 sales of Sindian District, New Taipei, August 2012 to July 2013; AT: "a small dataset like this does not represent real estate prediction") most likely comes from this register, since its months start when registration began (the UCI page does not name its source); so this is the source of that cut, and no duplicate of a dataset in the benchmark. The data.gov.tw 170343 file (New Taipei City, Luzhou 2014) and the Kaggle upload are cuts or re-uploads of the register, kept as annotated links. The UCI table's distance to the MRT and store counts are not in the register (they would need geocoding, which the de-identified address limits). Other house-price records come from other sources (`house_sales`, `nyc_property_sales`, `nsw_property_sales`, `florida_dor_property_sales`, ...); none from Taiwan. External collections: none found.
- Better data: found as better data for `real_estate_valuation`.
- Papers and pages: Yeh and Hsu 2018, Applied Soft Computing 65:260 (the UCI table's paper); master's theses at NCCU and NYCU that model register prices (hedonic, clustering, stacked models); no competition on the register found (the 2023 SinoPac AI GO house-price contest on T-Brain was not confirmed to use it).
- Metric: none found (the MOI download page and the data.gov.tw pages define no task), so the fallback `rmse` on the unit price, or on its log (a MET-3 call); inputs none.
- Risks for /add-dataset: the unit price is the total price over the area, so the total price goes and the parking price is separated (LEAK, SEL-5); keep dwelling sales only (a building in the transaction, residential use) and read the remarks field, which notes special conditions of a sale, to drop non-market sales (USE-5); join the building, land and parking detail tables by serial number; ROC-calendar dates to convert; several hundred thousand rows a year, so a cut by years or region.
- Priority: gap 0 (business & marketing, regression and temporal are well covered), use case 0 (the curation's), source + (the MOI, with schema files), shape + (hundreds of thousands of sales over 14 years, mixed features), risk - (price-derived columns, special transactions, detail-table joins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `real_estate_valuation`.
- as published: One row per registered transaction for every county of Taiwan; CSV batches per season and county with schema files (main, building, land, parking); per sale: district, transaction date, object type, ...; target: Unit price of a dwelling sale (NTD per m2), the same quantity as the UCI table's price per ping; access: open (free download after accepting the government open-data terms; attribution required).
- Why: Same target and use case as real_estate_valuation, with features of the same kind (transaction date, building age, location, plus floor, type and area); the UCI table's 414 sales in Sindian District start in August 2012, the month this registration began, so the registry is most likely its upstream (the UCI page does ...
- Adds: Hundreds of thousands of sales per year across Taiwan against 414 rows from one district, 2012-2026 for a real temporal split, a government first publisher with a schema, and the curator's objection answered (AT: 'a small dataset like this does not represent real estate prediction'). Distance to MRT and store counts ...
