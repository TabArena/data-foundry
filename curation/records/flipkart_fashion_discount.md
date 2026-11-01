---
unique_name: flipkart_fashion_discount
name: Flipkart Discount
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2022'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/kuchhbhi/stylish-product-image-dataset
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a 2022 scrape of about 65,000 Flipkart fashion listings made for an image recommender; MulTaBench's target, the discount ratio (sold price over listed price), is derived and set by the seller, with the listed price as the one structured input.
- Source: Kaggle upload by kuchhbhi, "Stylish Product Image Dataset" (2022-05-21, CC0), scraped "from flipkart.com(e-commerce website) in two formats Image and textual data in tabular format" for the uploader's "Fashion Product Recommendation" project ("upload any fashion image and it will show the 10 closest recommendations"); 65k images (400x450) and one CSV (`id`, `brand`, `title`, `sold_price`, `actual_price`, `url`, `img`). The same uploader's copy with 65x80 images (<https://www.kaggle.com/datasets/kuchhbhi/flipkart-fashion-products-65k-dataset>) is the same data (PROV-6). As MulTaBench ships it (extended release, Table 9): 60,900 rows, `actual_price`, `brand` and `title` as text, one photo, target `price_ratio` = sold price / listed price; it dropped the sold price as the numerator.
- Use case: none in the source (the CSV is offered for "your Machine Learning projects" after feature construction from the title). The discount is the seller's choice, so predicting it serves at most a shopper or a competing seller guessing it; the sold price from brand, title and photo would be the price framing. Fit approximate; regime IID (one scrape, no date per row).
- Siblings and duplicates: no record of this source (searched flipkart; `laptops` and `product_review_data` are other Flipkart scrapes). External collections: MulTaBench (extended release, admitted on joint signal only).
- Better data: a candidate of the benchmark MulTaBench (not searched in this run, by its brief).
- Papers and pages: the Kaggle page; MulTaBench (arXiv 2605.10616, Appendix F.1; Table 8: R² 0.710 from the listed price alone, 0.450 from the photo, 0.722 joint).
- Metric: none found (the Kaggle page defines no task; MulTaBench scores R²), so the fallback `rmse`; inputs none.
- Risks for /add-dataset: a target built from two columns of the source, which the actor sets rather than predicts (USE-2, USE-5); the listed price is both the input and the denominator; the rest of the signal is in text (brand, title) and the photo (SEL-12); one product in several sizes or colours as separate rows (PROV-4 within the data).
- Priority: gap 0 (business & marketing, regression, IID), use case 0, source 0 (a scrape for a side project), shape 0 (one numeric input and two text columns), risk - (a derived target with no decision).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 60,900 rows; 1 structured, 2 text, 1 image features (MulTaBench Table 9); target: Sold price / listed price.
- Why: Predict the discount ratio of a Flipkart fashion product
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2022 scrape (CC0); target is a ratio MulTaBench derives.
