---
unique_name: socal_house_prices_images
name: SoCal Houses
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2019'
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ted8080/house-prices-and-images-socal
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 15,474 Southern California house listings with beds, baths, floor area, city and the listing price, scraped in 2019 for price prediction from a photo; without the photo it is a thin house-price table, and the accepted `california_house_prices_2020` covers the same task with dated sales and far more features.
- Source: Kaggle upload by `ted8080`, "House Prices and Images - SoCal" (socal2.csv, 2019-12-04, licence unknown): "I created this dataset to predict the house price from its image(s). It has the price and corresponding image. Each house has only one image." The uploader's GitHub README (github.com/ted2020/House-Price-Prediction-via-Computer-Vision): "I created a tool to collect data from Weichert's website for Southern California listings", exterior frontal images for a CNN. As published: one table (image_id, street, citi, n_citi, bed, bath, sqft, price; "n_citi is the label encode of the citi column") and one exterior photo per house; 15,474 rows in MulTaBench.
- Use case: a buyer, seller or agent values a listed house from its size and location; the source's own task is the price from the photo and it names no actor, so the fit is approximate (listing prices on one broker's site, undated); regime IID by default, since no listing date ships (SPLIT-7: a house price is temporal in nature, so this stays a known gap).
- Siblings and duplicates: no record of this upload. Same task and region: `california_house_prices_2020` (`Yes`, BeyondArena: 2020 California sales with listing dates and about 40 features), `calif_houses` (`No`), `houses` (`Yes`, 1990 census block groups). External collections: MulTaBench, extended release (admitted on Joint Signal only), as "SoCal Houses".
- Better data: a candidate of the benchmark MulTaBench (the run searched no further); the already accepted `california_house_prices_2020` is the stronger data for the same task.
- Papers and pages: MulTaBench (Arazi et al. 2026, arXiv 2605.10616, App. F.1); no paper on the data.
- Metric: none found (the Kaggle page and the GitHub README name none), so the fallback `rmse`, with the price modelled on a log scale (MET-3, MET-8).
- Risks for /add-dataset: four structured features (bed, bath, sqft, city) once the photo goes (an embedding would be image-derived, SEL-13); `n_citi` repeats `citi` (CLEAN); the street address identifies the house (check repeated houses, then drop it); listing prices without a date (SPLIT-7); the scrape date is not stated.
- Priority: gap 0, use case 0, source 0 (a hobby scrape described in a README), shape 0 (15,474 rows but four features), risk - (an accepted record covers the same task with richer, dated data).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 15,474 rows; 4 structured, 2 text, 1 image features (MulTaBench Table 9); target: Price.
- Why: Predict a Southern California house price from a photo, beds, baths and area
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2019, no licence.
