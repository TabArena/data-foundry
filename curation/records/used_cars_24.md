---
unique_name: used_cars_24
name: Used cars 24
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Missing source information
tags:
- New IID
- Free Text (Short)
- AI-Filled (Verify)
collections:
- CARTE/TARTE
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/avikasliwal/used-cars-price-prediction
- (unsure) https://www.cars24.com/
source_row: 866
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: Indian used-car resale prices with mixed string columns; the rows look real (Indian cities, model names, units in the strings), so the "likely synthetic" note is not supported, but the first publisher is not named on the Kaggle page.
- Source: Kaggle upload by avikasliwal, 26 Oct 2019, "Used Cars Price Prediction: Predict the price of an unknown car. Build your own Algo for cars 24 !!" (<https://www.kaggle.com/datasets/avikasliwal/used-cars-price-prediction>, no description); as published: train-data.csv 6,019 rows x 14 columns (`Name`, `Location` (11 cities), `Year`, `Kilometers_Driven`, `Fuel_Type`, `Transmission`, `Owner_Type`, `Mileage` "26.6 km/kg", `Engine` "998 CC", `Power` "58.16 bhp", `Seats`, `New_Price` "8.61 Lakh" (missing in 5,195 rows), target `Price` in lakh) and test-data.csv without the price (preview read 2026-10-22). The columns and the 6,019 training rows match MachineHack's "Predicting The Costs Of Used Cars" hackathon (sponsored by Imarticus Learning, June 2019, over 1,700 participants), which is the likely first publication; its page and the site the data came from (the cars24 link is a guess) were not reached.
- Use case: a dealer or a listing platform suggests a resale price for a car from its listing attributes; no actor named by the source, fit approximate; regime IID (one snapshot of listings, no listing date).
- Siblings and duplicates: other used-car price records: `fiat_500` (`Yes`), `used_cars_dataset_cardekho` (Lennart, `TBD -> 2nd Tier`, `No Good Target (yet)`), `used_cars_pakistan`, `used_cars_saudi_arabia`, `used_cars_benz_italy`, `exploreml_funaab_hackathon_nigerian_cars_price_prediction`; none shares these rows. External collections: CARTE/TARTE (as `used_cars_24`).
- Papers and pages: the Kaggle page; Analytics India Magazine's report of the MachineHack winners (feature work on `Mileage`, `Engine`, `Power`, `New_Price`, brand from `Name`); no paper.
- Metric: none found (the Kaggle page has no task; the MachineHack evaluation page was not reached), so the fallback `rmse`, with the price likely shipped on a log scale (MET-3).
- Risks for /add-dataset: confirm the MachineHack origin and its metric (PROV-2, MET-1); the unit strings to parse (CLEAN); `New_Price` is the new-car list price, fine at listing time but mostly missing; only the train file is labelled.
- Priority: gap 0 (business & marketing, regression, IID), use case 0, source 0 (an undescribed Kaggle upload, likely a hackathon), shape + (6,019 rows, mixed numeric, categorical and unit-string columns), risk 0. The `Missing source information` marker stays until the MachineHack origin is confirmed.

A used-cars price-prediction dataset (Kaggle, possibly from cars24.com) — a standard tabular regression task with several string columns benefiting from preprocessing. The CC comment flags that the source is unclear and the data may be synthetic, which is the main risk; if real it would be a reasonable IID regression dataset. A human must verify the data provenance (genuine scraped listings vs synthetic), size, and whether it duplicates other used-car datasets before promoting it, so a provisional 2nd-tier hold is appropriate.

---

used cars data; many columns that could benefit from string preprocessing; likely synthetic data given the missing source and data state
