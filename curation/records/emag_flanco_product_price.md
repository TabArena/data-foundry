---
unique_name: emag_flanco_product_price
name: eMAG Products
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2024'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/furduisorinoctavian/romanian-products-from-emag-and-flanco
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a November 2023 crawl of 85,766 products from two Romanian retailers with price, rating, category and photo; MulTaBench's price task keeps only the rating and the category as structured inputs, the product's identity sits in the title and the photo, and the source names no task.
- Source: Kaggle upload by furduisorinoctavian, "Romanian products from Emag and Flanco" (file dated 2024-02-16, MIT): "Every product was crawled from Emag and Flanco websites in November 2023"; one `products.csv`, 85,766 rows x 8 columns (`id`, `name`, `price`, `rating` 0 to 5, `url`, `image_url`, `shop`, `category` with 83 values). As MulTaBench ships it (extended release, Table 9): 38,294 rows, `rating` and `category` with one photo, target `price`; it dropped the title "because the title names the object shown in the image", and the shop. Why about 47,000 rows were dropped is not stated in the parts read.
- Use case: none in the source (its "research ideas" are analyses: price across categories, rating distribution, shop comparison). A seller or a price-comparison site estimating a product's price would know the product (title, specs, brand), which MulTaBench removed; fit approximate; regime IID (one crawl).
- Siblings and duplicates: no record of this source (searched emag, flanco). E-commerce price records of MulTaBench are screened in other batches (`amazon_bestseller_price`, `zepto_grocery_price`, `khaadi_clothes_price`). External collections: MulTaBench (extended release, admitted on joint signal only).
- Better data: a candidate of the benchmark MulTaBench (not searched in this run, by its brief).
- Papers and pages: the Kaggle page; MulTaBench (arXiv 2605.10616, Appendix F.1; Table 8: R² 0.749 from the structured columns, 0.769 from the photo, 0.841 joint).
- Metric: none found (the Kaggle page defines no task; MulTaBench scores R²), so the fallback `rmse` on a log price scored on the price (MET-3); inputs none.
- Risks for /add-dataset: with the title the task is text-heavy (product names carry the specs; `NLP (Text)`, SEL-12), without it three inputs remain (category, rating, shop); the same product at both shops or in several variants gives near-duplicate rows across folds (PROV-4 within the data); unrated products may be coded 0 (CLEAN); prices in RON of one month.
- Priority: gap 0 (business & marketing, regression, IID), use case 0, source 0 (a crawl described by its columns), shape 0 (many rows, three structured inputs), risk - (a text- and image-carried signal, no decision named).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 38,294 rows; 2 structured, 0 text, 1 image features (MulTaBench Table 9); target: Price.
- Why: Predict a Romanian retail product's price from photo, rating and category
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Crawled from eMAG and Flanco in Nov 2023 (Kaggle 2024, MIT); title dropped by ...
