---
unique_name: rwi_geo_red_houses_for_sale
name: 'RWI-GEO-RED: RWI Real Estate Data - Houses for Sale (HK), Scientific Use File'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Other
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.7807/immo:red:hk:suf:v10
- https://www.rwi-essen.de/en/research-advice/further/research-data-center-ruhr-fdz/data-sets/rwi-geo-red/x-real-estate-data-and-price-indices
- https://b2find.eudat.eu/dataset/1032b976-b069-5084-b956-c8426ba56f73
- https://doi.org/10.7807/immo:red:hk:suf:v15
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: every house-for-sale advert on ImmobilienScout24 since 2007, released by the RWI research data centre with the platform as a versioned scientific-use file; the asking-price task of `immoscout_german_house_prices` from the platform's own documented archive, with advert dates for a temporal split, available only on application.
- Source: RWI – Leibniz Institute for Economic Research and ImmobilienScout24, "RWI Real Estate Data - Houses for Sale (HK) - SUF", part of RWI-GEO-RED at FDZ Ruhr; a DOI per version: v10 (2024, doi 10.7807/immo:red:hk:suf:v10, B2FIND: "all houses for sale at ImmobilienScout24 (full sample)", the characteristics of the unit such as price and size plus generated items such as the duration of the advert spell, 3.9 GB in dta, csv, sas and parquet), now V15 (doi 10.7807/IMMO:RED:HK:SUF:V15) covering 2007 to June 2026 in monthly time units. Data description: Heuer (2026), "FDZ Data Description: Real-Estate Data for Germany (RWI-GEO-RED v15)", RWI Projektberichte (not read). The SUF's smallest spatial unit is the 1 km² grid cell; coordinates only on site. Sibling files for apartments for sale (WK), apartments for rent (WM) and houses for rent (HM). Row and column counts were not found on the pages read.
- Access (a note, EV-4): the SUF is free for non-commercial scientific research by researchers at publicly funded institutions, on a data request; commercial use excluded; Campus Files for teaching (RWI page). Whether a benchmark built by a company can obtain it is a question for the release checklist.
- Use case: a seller or agent sets the asking price of a house when listing it, or a buyer judges an advert against the market; RWI publishes the data for research and price indices and names no actor, so fit approximate, as for the sibling. Regime temporal: adverts carry their month (SPLIT-6); the same house can be advertised again, a grouped question inside the temporal task (SPLIT-13).
- Siblings and duplicates: `immoscout_german_house_prices` (`Yes`, BeyondArena: a 2020 scrape of about 10,000 houses from a deleted Kaggle upload), for which this was found; `immoscout24_germany_rental_offers` (`TBD -> 2nd Tier`, three 2018-2019 scrapes of rental adverts, whose screening names the RWI rental files as the better source). The same platform and target, another source (PROV-4): the curator decides which enters (TP-6). External collections: none found.
- Better data: found as better data for `immoscout_german_house_prices`; no further search this round.
- Papers and pages: the RWI page, the B2FIND record of v10, the v15 data description (not read); studies on German house prices that use RWI-GEO-RED were not looked up.
- Metric: none from the source (a research data file), so the fallback `rmse`, or `rmsle` on the price from context as the sibling declares (`Metric.from_context("rmsle", target_transform="log")`), the curator's call (MET-11); inputs none.
- Risks for /add-dataset: access by application (above); asking prices, not sale prices, as for the sibling; adverts repeated or updated across months (RWI's duplicate handling to read in the data description, LEAK-17); generated items such as the advert spell duration are known only after the advert ends (LEAK-10); the full sample is millions of rows (a cap and a recent window); the grid-cell id as a location feature.
- Priority: gap 0 (business & marketing, regression and temporal are not thin), use case 0 (no actor named), source + (a research data centre with versioned DOIs and a data description), shape + (all adverts since 2007, mixed features, monthly dates).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `immoscout_german_house_prices`.
- as published: All house-for-sale adverts on ImmobilienScout24 since 2007, monthly time unit: asking price, size and characteristics of the house, 1 km grid cell in the SUF (coordinates only in the on-site ...; target: asking price of a house for sale; access: request (SUF free of charge for non-commercial scientific research by researchers at publicly funded institutions; Campus Files for teaching on request; whether a benchmark built by a company qualifies must be checked).
- Why: Same platform, same target and the same kind of features as the record's 2020 ImmoScout24 scrape (about 10k houses, one scrape date, deleted Kaggle source).
- Adds: Over a thousand times the rows, 2007-2026 with advert dates (the temporal split the record lacks), documented by the platform and RWI with a DOI per version; sibling files for apartments for sale/rent and houses for rent.
