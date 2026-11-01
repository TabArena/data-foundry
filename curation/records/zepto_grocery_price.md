---
unique_name: zepto_grocery_price
name: Zepto Groceries
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '? (2025)'
domain: business & marketing
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/simpleaditya/zepto-products-dataset
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 13,345 grocery products scraped from the Zepto app with their selling price; once the undiscounted price and the product name are dropped, the price is predicted from category, pack size and ratings, a weak stand-in for a pricing decision.
- Source: Kaggle "Zepto Products Dataset" by `simpleaditya` (zepto dataset.xlsx, file dated 2025-07-21, licence unknown): "information about products available on the grocery delivery platform, Zepto. The data was collected using Selenium", in two parts (the standard interface and the "Super Saver" deals); columns Image (URL), Name, Price, Original Price, Ratings, Quantity, Status, Review, Sub-Category, Category, Interface. MulTaBench (App. F.1): 13,345 rows, target the price; "the undiscounted price and the product name are dropped".
- Use case: none named; the source lists analyses ("Compare product prices, analyze discount strategies"); the nearest decision is a retailer pricing a new product from its category and pack size, so the fit is approximate; regime IID (one scrape, undated).
- Siblings and duplicates: no other Zepto or quick-commerce price record (the grocery records are sales forecasting). External collections: MulTaBench, extended release (admitted on Joint Signal only), as "Zepto Groceries".
- Better data: a candidate of the benchmark MulTaBench (the run searched no further).
- Papers and pages: the Kaggle page; MulTaBench (Arazi et al. 2026, arXiv 2605.10616, App. F.1).
- Metric: none found (the Kaggle page names none), so the fallback `rmse`, with the price modelled on a log scale (MET-3, MET-8).
- Risks for /add-dataset: `Original Price` (the MRP) fixes the selling price up to the discount and must go (LEAK); a product listed in both interfaces must not sit on both sides of a split (group by product name, SPLIT); `Quantity` is a string ("1 kg", "500 ml") to parse; without the name the target is close to a category lookup (an unclear task); the image goes (SEL-13); the scrape date is not stated.
- Priority: gap 0, use case 0, source 0 (an anonymous scrape with a short description), shape + (13,345 rows, mixed types), risk - (the MRP leak and products repeated across interfaces).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 13,345 rows; 5 structured, 2 text, 1 image features (MulTaBench Table 9); target: Price.
- Why: Predict a Zepto grocery product's price from image, rating, category and pack size
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2025 Selenium scrape, no licence.
