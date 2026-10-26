---
unique_name: used_cars_benz_italy
name: Used Cars Benz Italy
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- New IID
- Free Text (Short)
- AI-Filled (Verify)
collections:
- CARTE/TARTE
original_source: Kaggle
year: '2023'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/bogdansorin/second-hand-mercedes-benz-registered-2000-2023-ita
source_row: 867
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: second-hand Mercedes-Benz listing prices in Italy, scraped by the uploader from unnamed Italian sites; a real but narrow single-brand task with price errors and duplicate rows.
- Source: Kaggle upload by bogdansorin, 15 Apr 2023, "Second-hand Mercedes Benz price Italy: This is a dataset created by web scraping second-hand cars italian websites" (<https://www.kaggle.com/datasets/bogdansorin/second-hand-mercedes-benz-registered-2000-2023-ita>); as published: mercedes-benz.csv (semicolon-separated) 16,392 rows x 10 columns: an index, `brand` (one value), `model` (186), `first_reg` (month-year), `fuel`, `mileage_km`, `seller_type` (dealer or private), `swift` (the gearbox, named `shift` in the codebook), target `price` (EUR), `power_hp` (preview read 2026-10-22).
- Use case: a seller or a dealer prices a used Mercedes from its listing attributes; no actor named, fit approximate; regime IID (one scrape, no listing date).
- Siblings and duplicates: the used-car price records (`fiat_500` `Yes`, `used_cars_dataset_cardekho` Lennart `TBD -> 2nd Tier`, `used_cars_24`, `used_cars_pakistan`, `used_cars_saudi_arabia`); no other Mercedes listing record (`mercedes_benz_greener_manufacturing` is a test-bench time task); no duplicate found. External collections: CARTE/TARTE.
- Papers and pages: the Kaggle page; no paper.
- Metric: none found (a Kaggle dataset without a task), so the fallback `rmse`, with the price likely on a log scale (MET-3).
- Risks for /add-dataset: `price` runs from 1 to 500,000,000 (placeholder and typo prices to clean, CLEAN); 853 duplicate rows apart from the index; which sites were scraped (PROV-2: plausible, unclear in a detail, so the old `Missing source information` marker is dropped); only 8 features, and one brand.
- Priority: gap 0, use case 0, source 0 (an uploader's scrape, sites unnamed), shape + (16,392 rows, mixed types), risk - (price errors and duplicates).

Second-hand Mercedes-Benz listings registered 2000-2023 in Italy (Kaggle), a valid tabular price-regression task with short free-text/categorical fields useful for feature engineering. The main risks noted are that it may duplicate other Mercedes-Benz used-car datasets and that the scraping source is not fully documented. A human must check for overlap/duplication with other used-car records, confirm the price target and size, and verify the data is genuinely scraped real listings before final acceptance.

---

used mercedes data

Maybe duplicate with other Mercedes Benz datasets? Likely scraped from some website from Italy. Otherwise a valid task
