---
unique_name: nsw_property_sales
name: NSW Bulk Property Sales Information (Valuer General of New South Wales)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://valuation.property.nsw.gov.au/embed/propertySalesInformation
- https://www.kaggle.com/datasets/josephcheng123456/nsw-australia-property-data
- https://www.kaggle.com/datasets/anthonyneav1/australia-nsw-property-sales-dataset-cleaned
- https://portal.spatial.nsw.gov.au/portal/apps/webappviewer/index.html?id=2536c8e4882140eb957e90090cb0ef97
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the NSW Valuer General's register of every recorded property sale since 1990 (about 6 million sales from 2001 to October 2025 in one re-upload), an official source for sale-price regression with a temporal split, but with thin property features (no rooms, building area or year built).
- Source: NSW Valuer General, "Bulk property sales information": weekly and yearly .DAT files back to 1990, from the Notices of Sale lodged with Land Registry Services (nsw.gov.au, "How to find property sales information"; data.infrastructure.gov.au catalogue entry rdh-bulk-property-sales-information-nsw: "address, purchase price and land area", "historic data back to 1990", updated weekly). The Valuer General's own page answered 403. As published (columns from the CC0 re-upload by anthonyneav1, converted from the .DAT files): Property ID, Sale Counter, Contract Date, Settlement Date, Purchase Price, Zoning, Nature of Property, Primary Purpose, address, Locality, Postcode, Area, Strata Lot Number, Component Code, Sale Code, % Interest, Dealing Number; "6 million lines" for 2001 to October 2025; the 1990-2000 archive has an older layout (josephcheng123456 re-upload). Licence: nsw.gov.au states CC BY-NC-ND 4.0 for non-commercial use, the catalogue "Creative Commons Attribution" (noted only, EV-4; the scout's CC BY 4.0 came from a re-upload).
- Use case: a buyer, seller, agent or lender values a property before the contract from its location, land area, zoning and type. The source names no prediction: the Valuer General uses sales as "the most important factor valuers consider when valuing land" (nsw.gov.au). Fit approximate (the curation's use case; no building attributes). Regime temporal by contract date, as `melbourne_housing_market` (SPLIT-6); repeat sales of one Property ID fall into several windows.
- Siblings and duplicates: `melbourne_housing_market` (Yes, BeyondArena; Domain.com.au auction sheets with rooms and building area); `melbourne_housing_snapshot` (No); `cook_county_residential_sales` and `king_county_home_sales_1999_2025` (TBD -> Yes, assessor sales of this run). No NSW sales record before (grep nsw, valuer general). Another source, not a duplicate (PROV-4). External collections: none found.
- Better data: found as better data for `melbourne_housing_market`; no further search this round.
- Papers and pages: the nsw.gov.au and catalogue pages; the Kaggle re-uploads (josephcheng123456, CC BY 4.0, 2001 to April 2023 plus the archive; anthonyneav1, CC0, 2001 to October 2025) are copies, not sources (PROV-8). Papers that used the data: not searched (the session's web-search budget ran out).
- Metric: none found (the Valuer General publishes a register, no task; nsw.gov.au and the catalogue checked), so as `melbourne_housing_market`: `rmsle` on the price from the context, the target shipped as log (MET-3, MET-11); inputs none.
- Risks for /add-dataset: sales that are not at market (partial interests via % Interest, the meaning of Sale Code to read in the Valuer General's data-element document) to filter (USE-5); one sale spread over several component rows (Component Code, Dealing Number) to collapse; Settlement Date comes after the contract (drop, LEAK-10); Area missing for strata units; the .DAT record layout and the 1990-2000 format break; the Valuer General's land values of the preceding base date are known at the contract and could be joined (USE-6); a sample of about 6 million rows.
- Priority: gap 0 (business & marketing, regression and temporal are well covered), use case 0 (the curation's), source + (the Valuer General's register), shape + (millions of sales over 25 years, mixed features), risk - (thin property features; non-market and multi-component sales to resolve).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `melbourne_housing_market`.
- as published: every recorded NSW property sale: about 6 million sale records 2001 to October 2025 (count from a Kaggle re-upload), plus the 1990-2000 archive; fields: property ID, sale counter, contract date, ...; target: purchase price of a property sale; access: open.
- Why: same target (sale price) and use case, with features of the same kind known before the contract (location, land area, property type and strata, zoning), from the official register rather than a scrape of auction sheets; a temporal split by contract date as the Melbourne record uses
- Adds: hundreds of times more sales, 35 years, current data, an official documented source under an open licence (CC BY 4.0 per the josephcheng123456 re-upload; NSW's bulk land-value files state CC BY 4.0 under the NSW Open Data Policy). Trade-off: no rooms, bathrooms, building area or year built, so a thinner feature set ...
