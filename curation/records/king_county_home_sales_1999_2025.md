---
unique_name: king_county_home_sales_1999_2025
name: King County Department of Assessments sales and property extracts, 1999-2025 (compiled as the kingCoData package)
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
- https://info.kingcounty.gov/assessor/DataDownload/default.aspx
- https://github.com/andykrause/kingCoData
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the King County Assessor's sales and property extracts over 1999-2025 (about 605,000 single-family and townhome sales as compiled by kingCoData), the source `house_sales` already reads for 13 months; a newer, wider release of the same source, so the curator picks it or `house_sales`.
- Source: King County Department of Assessments, Data Download page (sales, residential building, parcel and change-history extracts; the page asks requesters to acknowledge RCW 42.56.070(9) against commercial use of lists of individuals). Compilation: the kingCoData R package by Andy Krause (GitHub README): "All single family and townhome sales (605,000+) in King County, Washington from 1999 through December 2025" and "All single family and townhome properties (508,000+) ... as of December 31, 2025". The README states neither how a sale is joined to its property record nor a sale-validity filter; the scout's 2019 build of 458,044 rows x 46 variables with `join_status` and `join_year` was not verified.
- Use case: as `house_sales`: a valuation of the home from the property record on the sale day (the assessor, a lender, a buyer); fit direct once the record is the one at the sale. Regime temporal (`house_sales`, CC: "Time split required"); 27 years give many windows (SPLIT-14).
- Siblings and duplicates: `house_sales` (Yes, built: the 2014-2015 kc_house_data sales rebuilt from these extracts as of each sale, with the county's sale warnings handled); `housing_price_prediction` (TBD -> 2nd Tier) and `house_price_prediction_dataset` (No, AHDS); `cook_county_residential_sales` (another assessor, a candidate). A newer release of the same source as `house_sales` (PROV-6): the curator decides which one enters. External collections: none found for the 1999-2025 compilation.
- Better data: found as better data for `house_sales`, `housing_price_prediction` and `house_price_prediction_dataset`; a newer release of the same source as `house_sales` (PROV-6).
- Papers and pages: kingCoData (github.com/andykrause/kingCoData); the provenance assessment on `house_sales` (2026-10-07: kc_house_data matched to the county's sales).
- Metric: none found (the county and kingCoData define no task), so as `house_sales`: `rmsle` on the price with the target shipped as log (MET-3; the house_sales precedent of 2026-10-21).
- Risks for /add-dataset: the property record must be the one at the sale (the change history; `house_sales` found 2,151 rows whose record changed after the sale, LEAK-10); the county's sale warnings for non-market sales (USE-5, as in `house_sales`); build from the county's extracts rather than the third-party package (PROV-8, PROV-11); joins over parcels and years; repeat sales of one parcel across windows (LEAK-17).
- Priority: gap 0 (business & marketing, regression and temporal are well covered), use case 0 (the curation's, as on `house_sales`), source + (the county assessor), shape + (about 605k sales over 27 years, mixed features), risk - (as-of-sale joins across the county's tables).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `house_price_prediction_dataset`, `house_sales`, `housing_price_prediction`.
- as published: kingCoData README: 'All single family and townhome sales (605,000+) in King County, Washington from 1999 through December 2025' and 508,000+ homes as of 2025-12-31; its documented 2019 build: ...; target: sale price; access: open.
- Why: house_sales already reads these three county extracts (sales, residential building, change history; datasets/_dev/tabarena-v0pt2/house_sales/dataset.py) but keeps only the 2014-2015 sales of the kc_house_data parcels; kingCoData joins each sale to the record of its own year, the as-of-sale rebuild house_sales does by ...
- Adds: For house_sales: about 28 times the sales and 27 years instead of 13 months (many temporal windows, cycles 2008 and 2020-2022), more property fields (view ratings, noise, greenbelt, basement grade). For housing_price_prediction: about 1,000 times the rows, sale dates, and a traceable public source instead of a ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
