---
unique_name: dubai_dld_sales_transactions
name: 'Dubai Land Department open data: registered real estate transactions (sales)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://dubailand.gov.ae/en/open-data/real-estate-data/
- https://www.kaggle.com/datasets/tomasgrygar/dubai-real-estate-sales-transactions
- https://www.dubaipulse.gov.ae/data/dld-transactions/dld_transactions-open
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: about 1.37M sale transactions registered with the Dubai Land Department since 2004, a registered-price task on an official register; no source names a use case, and the Kaggle mirror adds target-derived columns.
- Source: Dubai Land Department open data (dubailand.gov.ae, "Transactions" search with "Download as CSV" behind a captcha; older years on Dubai Pulse, `dld_transactions-open`, "comprehensive details about all type of Real-Estate Transactions", from the TABU system). DLD's columns: transaction number and date, type and sub type, registration type, free hold, usage, area, property type and sub type, amount, transaction and property size, rooms, parking, nearest metro, mall and landmark, number of buyers and sellers, master project, project. The Kaggle mirror (tomasgrygar, snapshot to 2026-10-05; CC BY 4.0 as the mirror states, the DLD page names no licence) keeps sales only: 1,372,277 rows, 20 columns, target `price_aed`. The first year of publication was not found.
- Use case: a buyer, lender or valuer, before a deal, estimates the price a unit will register at; not named by the source; fit approximate; regime temporal (22 years of drifting prices; repeat sales of a building or project, SPLIT-13).
- Siblings and duplicates: `sberbank_housing_market_forecasting` (Yes, Moscow deals 2011-2015); other registered-sale tasks `cook_county_residential_sales` (TBD -> Yes) and `florida_dor_property_sales`; no Dubai record (grep for dubai). External collections: none found.
- Better data: found as better data for `sberbank_housing_market_forecasting`; no further search this round.
- Papers and pages: DLD's open-data page; the Dubai Pulse catalogue; the mirror's DATA_DICTIONARY.md; no paper.
- Metric: none found (DLD page, Dubai Pulse, the mirror's README); fallback `rmse`, on a log price as Sberbank's shipped target (MET-3, MET-8); inputs none.
- Risks for /add-dataset: build from DLD's own export (PROV-8): the mirror's `price_psf` is the target over the area and bit 4 of `quality_flags` a per-year percentile band of that ratio, so neither is a feature and a filter on them is a target-based filter to note (LEAK-27, LEAK-30); land, whole buildings and commercial units price by other logics, and off-plan and ready sales are different procedures (USE-5: filter or keep with the type); repeat sales of one unit (LEAK-16); the captcha download for recent years.
- Priority: gap 0 (business & marketing, regression, temporal not thin), use case 0 (none named by the source), source + (a land registry's own data and column list), shape + (1.37M rows, categorical, numeric and dates), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `sberbank_housing_market_forecasting`.
- as published: 1,372,277 registered sale transactions, 2004 to 2026-10-05 (Kaggle mirror, sales only: mortgages and gifts left out; quality flags per row); DLD columns: transaction number and date, type and sub ...; target: registered sale price of a residential unit (log price per sq m, as Sberbank's shipped target); access: open (DLD site: CSV per date range behind a captcha, older years on data.dubai; the mirror states CC BY 4.0 as DLD's licence, the DLD page itself names none).
- Why: the Sberbank task in another city: the same quantity measured the same way (a registered deal price, not an asking price, which is what ruled out the Russian listing sets), the same use case, and features of the same kind (size, rooms, ready vs off-plan as Sberbank's sales before completion, district and project, ...
- Adds: about 45x Sberbank's ~30k deals (2011-2015), 22 years up to 2026, an official register that keeps growing; lacks Sberbank's build year, floor, material and the hundreds of district statistics (macro series could be joined by date). Not to confuse with the Kaggle 'Dubai Real Estate: Sales & Rentals (2020-2026)' ...
