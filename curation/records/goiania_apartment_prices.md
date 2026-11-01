---
unique_name: goiania_apartment_prices
name: Goias Apartments
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Github
year: '2024'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/cego669/ApartmentPricesInGoiania
- https://www.kaggle.com/datasets/carloseduardogo/apartment-prices-in-goinia-gois-brazil
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a one-month scrape (August 2024) of apartment listings in Goiania with the asking price and about 70 structured attributes; a real tabular price task (MulTaBench: R² 0.931 from the structured columns alone, 0.660 from the photo alone), but one more house-price dataset among many.
- Source: Carlos Eduardo's GitHub project (<https://github.com/cego669/ApartmentPricesInGoiania>, created 2024-08-23: "data collected from the internet (August, 2024)", scraped with Selenium from vivareal.com.br), which holds the raw `1_data_extraction/data.csv` (11.8 MB), a cleaned `2_data_cleaning/data.csv`, the scraper and the modelling notebooks; the Kaggle copy (carloseduardogo, 2024-09-17, CC BY-NC-SA 4.0) lists price, condominium fee, IPTU (property tax), rooms, bathrooms, floor, parking spaces, area, amenity flags, the main photo and the advertiser's description. As MulTaBench ships it (extended release, Table 9): 9,830 rows, 73 structured columns (`tag_card`, `business_type`, area, counts, floor, about 65 amenity flags), the neighbourhood as text and one photo, target `price`; it dropped the description, address, condominium fee and IPTU. The raw row count was not checked.
- Use case: a seller, agent or buyer prices an apartment from its listing attributes when it goes on the market; the README's web app predicts the price, while it states the project is for education and its predictions are not meant for real decisions, so the source names no actor. Fit approximate (an asking price, not a sale price); regime IID (one scrape in one month, no listing date).
- Siblings and duplicates: no record of this source (searched goiania, vivareal, cego669). Accepted house-price siblings: `ames_housing`, `california_house_prices_2020`, `house_sales`, `immoscout_german_house_prices`, `melbourne_housing_market`, `miami_housing`, `perth_house_prices`; the curators called `magicbricks_house_price` "yet another house price dataset", and `lisbon_house_prices` notes "more than enough other price datasets". `brazilian_houses` (`TBD -> 2nd Tier`) is another Brazilian listing set from another source. MulTaBench's other listing-with-photo records (`sao_paulo_property_price_images`, `socal_house_prices_images`) are screened in other batches. External collections: MulTaBench (extended release, admitted on joint signal only).
- Better data: a candidate of the benchmark MulTaBench (not searched in this run, by its brief).
- Papers and pages: the GitHub README and notebooks (`5_modeling/final_model.ipynb`); the Kaggle page; MulTaBench (Arazi et al. 2026, arXiv 2605.10616, Appendix F.1 and Table 8).
- Metric: the README reports one number, a "mean percentage error" of 13.64% on held-out data, for a HistGradientBoosting model tuned by Bayesian optimisation; whether that metric drove the tuning is not stated (check the notebook), so the fallback `rmse` on a log price scored on the price is likely (MET-3, MET-5); inputs none. MulTaBench scores R².
- Risks for /add-dataset: one apartment listed by several agencies would put the same unit in train and test (check duplicates; PROV-4 within the data); `business_type` may mix sale and rent offers, so the target must be one of them (USE-5); the condominium fee and IPTU are known at listing time and belong back in (USE-6); the description may state the price (LEAK); build from the raw scrape, not MulTaBench's cut (PROV-13).
- Priority: gap 0 (business & marketing, regression, IID), use case 0 (no actor in the source), source 0 (a personal scrape with code and a README), shape + (9,830 rows, 73 mixed features), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 9,830 rows; 73 structured, 1 text, 1 image features (MulTaBench Table 9); target: Asking price.
- Why: Predict an apartment's asking price in Goiania from listing attributes and a photo
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Scraped from vivareal.com.br (Kaggle 2024, CC BY-NC-SA).
