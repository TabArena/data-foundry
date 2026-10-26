---
unique_name: used_cars_saudi_arabia
name: Used Cars Saudi Arabia
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
- https://www.kaggle.com/datasets/turkibintalib/saudi-arabia-used-cars-dataset
- syarah.com
source_row: 855
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: used-car listings scraped from syarah.com in 2021; a real mixed-type price task once the 2,526 negotiable listings without a price are dropped.
- Source: Kaggle upload by turkibintalib, 4 Jul 2021, "Saudi Arabia Used Cars Dataset: Used Cars Prices and Spec Scraped From Syarah Website" (<https://www.kaggle.com/datasets/turkibintalib/saudi-arabia-used-cars-dataset>): "8248 records of used cars collected from syarah.com"; as published: UsedCarsSA_Unclean_EN.csv, an Arabic xlsx and UsedCarsSA_Clean_EN.csv with 8,035 rows x 13 columns (`Make`, `Type` (381), `Year`, `Origin`, `Color`, `Options`, `Engine_Size`, `Fuel_Type`, `Gear_Type`, `Mileage`, `Region` (27), target `Price` (SAR), `Negotiable`) (preview read 2026-10-22).
- Use case: a seller or the platform prices a used car from its listing; no actor named, fit approximate; regime IID (one scrape, no listing date).
- Siblings and duplicates: the used-car price records (`fiat_500` `Yes`, `used_cars_dataset_cardekho` Lennart `TBD -> 2nd Tier`, `used_cars_24`, `used_cars_pakistan`, `used_cars_benz_italy`); no duplicate found. External collections: CARTE/TARTE.
- Papers and pages: the Kaggle page; no paper.
- Metric: none found (a Kaggle dataset without a task), so the fallback `rmse`, with the price likely on a log scale (MET-3).
- Risks for /add-dataset: `Price` is 0 in 2,527 rows, 2,526 of them `Negotiable` = True (no price asked): drop them and drop `Negotiable`, which is then True in one row only, as the old note says; 8 priced rows below 1,000 SAR; start from the unclean file to see the uploader's cleaning (PROV-13); 5,508 priced rows remain.
- Priority: gap 0, use case 0, source 0 (the uploader's own scrape, one paragraph), shape + (5,508 priced rows, 12 mixed features), risk 0.

Saudi Arabia used-car listings scraped from syarah.com (Kaggle), a valid tabular price-regression task with categorical/short-text features. The comment notes the task likely needs filtering by whether the price is negotiable, which is a cleaning step rather than a blocker. A human must define the exact target (price), apply the negotiable filter, confirm size, and check for duplication with other regional used-car datasets before acceptance.

---

used cars data

the task would likely need to be filtered by negotiable or not
