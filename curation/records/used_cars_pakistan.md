---
unique_name: used_cars_pakistan
name: Used Cars Pakistan
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Free Text (Short)
- New IID
- AI-Filled (Verify)
collections:
- CARTE/TARTE
original_source: Kaggle
year: '2021'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/mustafaimam/used-car-prices-in-pakistan-2021
- http://www.pakwheels.com/
source_row: 854
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: 72,655 used-car listings scraped from PakWheels in 2021 with their asking price; a real mixed-type price task, one of several used-car records.
- Source: Kaggle upload by mustafaimam, 22 Apr 2021, "Used car prices in Pakistan 2021: Dataset scraped from Pakwheels" (<https://www.kaggle.com/datasets/mustafaimam/used-car-prices-in-pakistan-2021>, CC0): "we created our own dataset using web scraping technique in python to extract data of used vehicles from www.pakwheels.com"; as published: a raw file (6.1 MB) and Used_car_prices_in_Pakistan_cleaned.csv, 72,655 rows x 10 columns (`Make`, `Model`, `Version` (1,328 values), target `Price` (PKR), `Make_Year`, `CC`, `Assembly` (local or imported), `Mileage`, `Registered City` (182), `Transmission`), no missing values (preview read 2026-10-22).
- Use case: a seller or the platform suggests an asking price for a listed car ("features which play an important role in suggesting and evaluating the price"); no actor named, fit approximate; regime IID (one scrape, no listing date).
- Siblings and duplicates: the used-car price records (`fiat_500` `Yes`, `used_cars_dataset_cardekho` Lennart `TBD -> 2nd Tier`, `used_cars_24`, `used_cars_saudi_arabia`, `used_cars_benz_italy`); other Pakistani used-car uploads on Kaggle exist (older PakWheels scrapes, per the uploader), none recorded. External collections: CARTE/TARTE.
- Papers and pages: the Kaggle page; no paper.
- Metric: none found (a Kaggle dataset without a task), so the fallback `rmse`, with the price likely on a log scale (MET-3).
- Risks for /add-dataset: 1,507 duplicate rows in the cleaned file (re-listed cars?); start from the raw file to see what the uploader's cleaning removed (PROV-13); asking price, not sale price.
- Priority: gap 0 (business & marketing, regression, IID), use case 0, source 0 (the uploader's own scrape, described in a paragraph), shape + (72,655 rows, high-cardinality categoricals and numerics), risk 0.

Used-car listings scraped from pakwheels.com (Pakistan, ~2021), a genuine real-world tabular price-prediction regression task; the comment clarifies it is a feature-engineering / string-preprocessing problem rather than free-text handling. It satisfies the core criteria (unique source, predictive regression, representative tabular ML). A human should confirm dataset size after cleaning, the exact price target, and that it does not duplicate other regional used-car datasets in the collection.

---

used cars data

FE / string preprocessing problem, not free text handling
