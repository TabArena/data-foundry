---
unique_name: france_dvf_property_sales
name: Demandes de valeurs foncières (DVF), France
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
year: '2019'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/
- '# descriptive notice of the files (DGFiP)'
- https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20221017-153319/notice-descriptive-du-fichier-dvf-20221017.pdf
- '# Etalab''s geolocated copy of the same rows (UTF-8 CSV, mutation id, coordinates)'
- https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres-geolocalisees
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 2: France's register of property sales (DGFiP, "Demandes de valeurs foncières"), every sale of the last five years outside Alsace-Moselle and Mayotte, about 4 million lines a year with the price, the property type, surfaces, rooms and location; a large official source for sale-price regression with a temporal split, but with thin building features, one price repeated over the lines of a sale, and terms that forbid re-identification.
- Source: Direction générale des Finances publiques (DGFiP), on data.gouv.fr under decree n° 2018-1350 of 28 December 2018 (open since 2019), Licence Ouverte v2.0, with a descriptive notice (read) and terms of use (CGU). A rolling window of five years, updated in April and October; the October 2026 update holds 2021-S2 to 2026-S1 (zips of 31 to 87 MB). As published: one pipe-separated file per year with 43 columns, 8 of them left empty by the decree (document reference, CGI articles, local id); one line per local and land type of a disposition, and "Les données génériques (ainsi que le prix) sont alors répétées sur chaque ligne" (notice, § 4). The 2025 file is 507 MB; a 78k-line preview gives 130 bytes a line, so about 3.9 million lines (estimate); mutation types in the preview: sale 96%, then off-plan sale (VEFA), exchange, auction, building land, expropriation. Etalab's "Demandes de valeurs foncières géolocalisées" (data.gouv.fr) ships the same rows as UTF-8 CSV with a mutation id and coordinates.
- The task's table: one row per sale (disposition) of a single house or apartment at its price `Valeur fonciere`, built by grouping the lines of a disposition (the count is not stated and is well below the line count) x about 12 inputs: date, mutation type, department, commune and postcode, cadastral section, local type, built surface, main rooms, land surface and land type, number of lots and their Carrez surfaces, and coordinates from the Etalab version. Access: open, Licence Ouverte; the CGU forbid re-identifying persons and indexing by search engines.
- Use case: a buyer, seller, lender or valuer estimates a home's market price from its type, surfaces and location before a sale. DGFiP publishes DVF for "la transparence des marchés fonciers et immobiliers" and names no prediction, so the use case is ours. Fit approximate: no year built, condition or floor. Regime temporal by mutation date.
- Siblings and duplicates: the same task from other registers, each its own record (PROV-4): `nsw_property_sales`, `florida_dor_property_sales`, `taiwan_actual_price_registration_sales` (`TBD -> Yes`, priority 2) and `cook_county_residential_sales` (`TBD -> Yes`, priority 3). No other DVF record (grep: DVF, valeurs foncières). External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08).
- Papers and pages: the notice and the data.gouv.fr page; hedonic price studies on DVF exist (not read).
- Metric: none found (the notice, the page), so the fallback `rmse` on the price (MET-1, MET-8); scoring the log price is a choice for the definition (MET-3). Inputs: none.
- Risks for /add-dataset: a multi-line disposition repeats one price for several locals and parcels (keep single-dwelling sales, or aggregate per disposition; LEAK-16 for the copies); sales of several dwellings, of dependencies alone, VEFA and auctions need a rule; the window drops a year at each update, so pin one release; street numbers and cadastral plan numbers can identify owners through the cadastre, so ship commune and section (or coarsened coordinates) as the CGU require; a property resold within five years recurs (SPLIT-13).
- Priority: gap 0 (business & marketing, regression and temporal covered), use case 0 (ours), source + (DGFiP's register with a notice), shape + (millions of sales, mixed types, five years), risk - (repeated prices, thin building features, re-identification terms).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).
