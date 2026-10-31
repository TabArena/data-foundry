---
unique_name: tokopedia_product_weight
name: Tokopedia Weight
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2025'
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.34740/kaggle/ds/9118061
- https://www.kaggle.com/datasets/nsmlehq/tokopedia-products-2025
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 1,200 Tokopedia product listings scraped in December 2025, with the seller-declared shipping weight as MulTaBench's target; a plausible attribute-filling task, but small, with sales counts a new listing does not have yet, and no use case named by the source.
- Source: Kaggle "Tokopedia Products Dataset (2025)" by Fiki Pratama (`nsmlehq`), doi 10.34740/kaggle/ds/9118061, MIT: "a structured collection of product listings scraped from Tokopedia", 1,200 products collected in December 2025 from public product pages; products.csv with 37 documented columns (name, description, min and max order, weight and weight_unit, condition, status, price, discount, shop city and name, category, transaction_success and transaction_reject, sold_count, view_count, review_count, talk_count, rating), products.json and the images. MulTaBench (App. F.1): 1,197 rows, target the shipping weight, with the category and shop names as text; identifiers, URLs, the Indonesian title and the description dropped.
- Use case: the marketplace or a logistics partner fills in or checks the weight a seller declares, which sets the shipping fee; the source lists "product categorization and attribute extraction" among its uses but no actor or decision, so the fit is approximate; regime IID (one scrape).
- Siblings and duplicates: no other Tokopedia or product-weight record (grep by name, slug, "shipping weight"). External collections: MulTaBench, extended release (admitted on Joint Signal only), as "Tokopedia Weight".
- Better data: a candidate of the benchmark MulTaBench (the run searched no further).
- Papers and pages: the Kaggle page and its citation; MulTaBench (Arazi et al. 2026, arXiv 2605.10616, App. F.1).
- Metric: none found (the Kaggle page lists uses, not a metric), so the fallback `rmse`, likely with the weight modelled on a log scale (MET-3, MET-8).
- Risks for /add-dataset: the weight is what the seller declared, with a `weight_unit` column to normalise (CLEAN); sold_count, the transaction counts, views, reviews and rating accrue after a listing goes live, so a new listing has none of them (LEAK-10, USE-3); the title and description name the product and likely carry most of the signal for its weight (text); 1,197 rows; the photo goes (SEL-13).
- Priority: gap 0, use case 0 (none named), source 0 (an individual's scrape, documented column by column), shape 0 (1,197 rows, close to the size floor), risk - (post-listing columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 1,197 rows; 13 structured, 2 text, 1 image features (MulTaBench Table 9); target: Shipping weight.
- Why: Predict a Tokopedia product's shipping weight from listing data and photo
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2025 scrape (MIT).
