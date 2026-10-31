---
unique_name: cook_county_residential_sales
name: Cook County Assessor's Office residential model (model-res-avm) training data
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/ccao-data/model-res-avm
- https://ccao-data-public-us-east-1.s3.amazonaws.com/models/inputs/res/2025/training_data.parquet
- https://ccao-data-public-us-east-1.s3.amazonaws.com/models/inputs/res/2026/run_id=2026-07-30-ecstatic-carly/training_data.parquet
- https://www.cookcountyassessoril.gov/news/cook-county-assessors-office-publicly-releases-residential-assessment-code-and-models
- https://datacatalog.cookcountyil.gov/
- https://datacatalog.cookcountyil.gov/d/wvhk-k5uv
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the Cook County Assessor's own training data for its residential valuation model, 405,195 sales with 203 columns, published per assessment year. It holds the hedonic sale-price task of `ames_housing` and `house_sales`, from the office that performs it, with leaky assessor columns to drop.
- Source: Cook County Assessor's Office (CCAO). The repository `ccao-data/model-res-avm` (GitHub, AGPL-3.0) describes the data, the model and the evaluation in its README. The training data sits on a public S3 bucket per assessment year; the README links 2022 to 2026, the 2025 file is 205 MB and the 2026 final run 201 MB (Last-Modified 2026-08-04). The 2026 file's footer, read by range request on 2026-10-31, gives 405,195 rows x 203 columns: `meta_sale_price` (the target); sale date, document number, deed type, and seller and buyer names; PIN and card ids, class, and township and neighbourhood codes; the assessor's mailed, certified and board values of the year and of the two prior years; and the column groups `char_*` (building characteristics), `loc_*` (location), `prox_*` (proximity), `shp_*` (parcel shape), `acs5_*` (census), `other_*` (tax bill, indices), `time_*`, and the sale-validation flags `sv_*`. Per the README, the file holds sales of "the 9 years prior to the next assessment date", "approximate size is 400K rows with 100 features", filtered to sales above $10k, single-PIN and single-building, arm's-length deeds, with outliers flagged.
- Use case: the assessor values every home for property tax. The model is used to "generate initial assessed values for single- and multi-family residential properties in Cook County", answering "What would the sale price of every Cook County home be if it had sold last year?" (README). Fit direct. Regime temporal by sale date; the source's own test set is "the most recent 10% of sales in our training sample".
- Siblings and duplicates: `ames_housing` (`Yes`), `house_sales` (`Yes`, King County 2014-15), `king_county_home_sales_1999_2025` (a new record of this run, another county), `housing_price_prediction` and `valuation` (`TBD -> 2nd Tier`), `house_prices_nominal` (`No`, `Duplicate`). No CCAO record existed before this run. The counties and sources differ, so this is no duplicate (PROV-4). External collections: none found.
- Better data: found as better data for `ames_housing`, `house_sales`, `housing_price_prediction` and `valuation` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the README (model, features, validation); the CCAO's announcement page was not reachable (HTTP 403); the Cook County data portal holds the source tables.
- Metric: the README reports the assessor ratio statistics (COD, PRD, PRB, MKI) and the "standard ML metrics" RMSE, MAE, MAPE and R², and compares model types by accuracy "as measured by RMSE (root mean squared error) using a test set". RMSE is the metric it names for model choice and also the fallback, so `rmse` on the price (MET-5). Shipping log price is a choice for the definition (MET-3). Inputs none.
- Risks for /add-dataset: the `meta_mailed_*`, `meta_certified_*` and `meta_board_*` values of the sale's year, and `other_tax_bill_amount_total`, come from assessments that may use the same sales (LEAK): keep only values fixed before the sale date, or drop them. The `sv_*` flags are computed from the price (LEAK): drop them, and filter on them as the CCAO does. Seller and buyer names are personal data: drop them. Multi-card PINs give several rows per sale (`meta_card_num`: group by sale), and repeat sales of a PIN over 9 years raise a grouping question (SPLIT). Check that `meta_sale_count_past_n_years` counts earlier sales only.
- Priority: gap 0 (regression and temporal not thin; house prices sit in business & marketing), use case + (the assessor names it), source + (the assessor's documented pipeline), shape + (405k sales, mixed types, temporal), risk - (assessed values and validation flags to drop).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ames_housing`, `house_sales`, `housing_price_prediction`, `valuation`.
- as published: about 405,195 arm's-length sales (2026 run; 'approximate size is 400K rows with 100 features'), residential sales of the 9 years before the assessment date (about 2017-2025 for the 2026 run), class ...; target: sale price (model trained on sales > $10k, single-parcel, single-building, non-related-party deeds); access: open, open (public S3 download links in the repository README).
- Why: same task and actor as ames_housing (De Cock's codebook names the Ames assessor's valuation of sold homes): sale price from the assessor's building characteristics (square footage, bedrooms, baths, year built, garage, basement, roof), location and time of sale | Same hedonic sale-price task as ...
- Adds: about 140x the sales (405k against 2,837), years 2017-2025 against 2006-2010, the assessor's own published training data and sale-validation filters instead of a teaching extract, temporal by sale date; also bears on house_sales (King County 2014-2015). Risks: the file is the assessor's engineered model input (ACS ...
