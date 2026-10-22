---
unique_name: valuation
name: Valuation
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Needs extensive data wrangling
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: finance
required_split:
- Custom
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://catalog.data.gov/dataset/property-valuation-and-assessment-data-db7c2
- https://data.cityofnewyork.us/City-Government/Property-Valuation-and-Assessment-Data/yjxr-fw8i
source_row: 830
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: New York City's yearly property assessment roll; the only target is the assessor's own market value, a model output, so no real task yet (as the CC says); the sale-price task belongs to `nyc_property_sales`.
- Source: NYC Department of Finance, "Property Valuation and Assessment Data" on NYC Open Data (dataset yjxr-fw8i, attribution "Department of Finance (DOF)", created 2019, rows updated 2020; the data.gov page in the links mirrors it): "The Department of Finance values properties every year as one step in calculating property tax bills". As published (portal metadata, read 2026-10-22): 9,845,857 rows over several rolls (`year`, `period`, `valtype`), about 40 columns: lot keys (`bble`, `boro`, `block`, `lot`), `owner`, building and tax class, lot and building dimensions, `stories`, `fullval` (market value), assessed and exempt values (`avland`, `avtot`, `exland`, `extot` and their `2` versions), exemption codes, address, zip, coordinates and admin areas; the column descriptions are empty.
- Use case: none in the source. Predicting `fullval` copies the DOF's mass appraisal, not an observed outcome (SEL-3), and the assessed values are fixed shares of it by tax class (SEL-5); the outcome an actor acts on is a sale price (`nyc_property_sales`, Lennart: `TBD -> 2nd Tier`, `No Good Target (yet)`), so the marker is aligned to it (`No Good Target  / Scientific Discovery` replaced). Regime temporal (yearly rolls; the record's `Custom` kept) or grouped by lot.
- Siblings and duplicates: `nyc_property_sales` (DOF rolling sales; a join by `bble` could give a sale-price task with the roll as features). External collections: none found.
- Papers and pages: none; the NYC Open Data page and the DOF property assessment page.
- Metric: none found (NYC Open Data page, DOF assessment page), so the fallback (rmse).
- Risks for /add-dataset: no target to ship as is (SEL-3); value columns derived from each other (SEL-5, LEAK); `owner` holds names (drop); repeated lots over rolls (grouped or temporal); size and joins (millions of rows per roll).
- Priority: gap 0 (finance is not thin), use case 0 (none), source + (the city agency's own portal), shape + (millions of lots, mixed types, yearly rolls), risk - (the target is an appraisal output, derived columns).

NYC property valuation and assessment data (data.gov) — essentially a government SQL dump with geospatial and text fields and no clean predictive task out of the box. The CC comment notes that assessed value may follow a fixed formula or come from a third party, and that extensive expert feature engineering plus multi-year collection would be needed to build a sound dataset. It is potentially salvageable into a property-value regression task but requires substantial wrangling and leakage checks, so a provisional 2nd-tier hold is appropriate pending human inspection of the target and feature provenance.

---

CC: "GOV data without a real predictive task; full evaluation either depends on a clear formula from the GOV or is given by some third party. Has geospatial data; temporal impact on price; requires a lot of expert feature engineering to make it work; basically just a SQL dump but not a real dataset yet; maybe not a lot of temporal leakage as it is just one year; could collect data from prior years as well and filter it to a good dataset etc"

Also includes text otherwise
