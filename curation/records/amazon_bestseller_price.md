---
unique_name: amazon_bestseller_price
name: Amazon Bestseller
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
year: '2025'
domain: business & marketing
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/amankumar20d/amazon-best-seller-all-departments-us
- https://arxiv.org/abs/2605.10616
- https://huggingface.co/datasets/multabench/core-img-reg-amazon-bestseller
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a January 2025 Kaggle snapshot of Amazon US bestseller lists published for market research, not for a prediction; MulTaBench predicts the price from four popularity columns and the thumbnail, and it dropped the product title and department the source ships.
- Source: Kaggle amankumar20d/amazon-best-seller-all-departments-us (one file `Amazon_Best_Seller.csv`, 1.3 MB, uploaded 2025-01-12, MIT): "The data was collected using the RapidAPI Amazon Online Data API", "Total Departments: 40", "Total Records: ~80 records per department (40 departments × 2 pages)"; fields `product_title`, `product_link`, `rank`, `price`, `ratings`, `reviews`, `department`, `page`, and a photo URL. As used by MulTaBench (core image-tabular; https://huggingface.co/datasets/multabench/core-img-reg-amazon-bestseller): 3,488 rows, `num_ratings`, `rank`, `star_rating`, `page`, the thumbnail, target log(1 + price).
- Use case: none in the source; its "Usage Examples" are market research, trend analysis, price comparison and "Recommendation Systems: Train machine learning models to recommend products". A seller pricing a new product would not know its rank or ratings, and a bestseller's price is listed next to them; with the title and department it would be a price suggestion on bestsellers only, close to `mercari_price_suggestion`. Fit none to approximate; regime IID (one snapshot).
- Siblings and duplicates: none (grep over the records for bestseller, best seller, the Kaggle slug); price-from-listing records from other sources: `mercari_price_suggestion`, `amazon_book_prices_2023`. External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the Kaggle page; MulTaBench (https://arxiv.org/abs/2605.10616), Table 3, Appendix D.2 (target log(1+price)), Table 11 (0.543 frozen, 0.566 task-aware, averaged over learners).
- Metric: none found (the Kaggle page defines no task; MulTaBench's R² is benchmark-wide, MET-5), so the fallback `rmse` on the price, shipped as log1p (MET-3); inputs none.
- Risks for /add-dataset: no task (`No Good Target (yet)`; SEL-3, USE-2); rank, ratings and stars come after the listing (LEAK-10 for a pricing use case); without the thumbnail (SEL-12) four weak columns remain, and with the title it becomes a short-text task; bestsellers only (`Selection Bias`); a scrape through a third-party API, the uploader is the first publisher (PROV-2).
- Priority: gap 0, use case 0 (none in the source), source 0 (a Kaggle upload with a field list), shape 0 (3,488 rows, four popularity columns in MulTaBench's cut), risk - (no task, post-listing columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 3,488 rows; 4 structured, 0 text, 1 image features (MulTaBench Table 3); target: log(1 + product price).
- Why: Predict a bestseller product's price from its thumbnail, rating count, rank and stars
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2025, collected through a RapidAPI Amazon data API (snapshot of bestseller lists).
