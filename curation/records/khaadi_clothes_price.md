---
unique_name: khaadi_clothes_price
name: Khaadi Clothes
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
tags:
- Tiny Data
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2023'
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/usman8/khaadis-clothes-data-with-images
- https://arxiv.org/abs/2605.10616
- https://huggingface.co/datasets/multabench/core-img-reg-khaadi-clothes
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 400 Khaadi apparel items scraped from the brand's Pakistani web shop in October 2023, with the retail price; without the photo the inputs are a product type, a short fabric string and a colour, the brand sets the price itself, and the source names no task.
- Source: Kaggle upload by usman8, "Khaadi's Clothes Data with Images" (files of 2023-10-17, Apache 2.0, source named as https://pk.khaadi.com/). As published: `Khaadi_Data/khaadi_data.csv`, 400 rows x 8 columns (`ID`, `Product Name` such as "Fabrics 3 Piece Suit", `Product Description` such as "Printed Embroidered Light Khaddar | Top Bottoms Dupatta", `Price` in PKR from 990 to 39,990, `Availability` (all "In Stock"), `Color`, `Img Path`, `Product Link`) and one image per item. MulTaBench (core, https://huggingface.co/datasets/multabench/core-img-reg-khaadi-clothes) keeps name, description, colour and the image, target `Price`.
- Use case: none in the source (it lists "retail analytics, fashion trend analysis, or recommendation systems"). A candidate: a merchandiser prices a new design from its fabric, pieces and embellishment; fit approximate, since the brand's own list price is the target and one season of one brand is the whole population. Regime IID on one snapshot, or grouped by design: the 400 ids fall into 82 groups by their prefix, which may be one design in several colours (to check).
- Siblings and duplicates: none (grep over the records for khaadi and the Kaggle slug). Related MulTaBench retail-price sets screened in this run: `emag_flanco_product_price`, `zepto_grocery_price`, `flipkart_fashion_discount` (all `TBD -> 2nd Tier`). External collections: MulTaBench (core image set).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the Kaggle page; MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Appendix B.1 and Table 3 (400 rows; 2 structured, 1 text, 1 image), Table 11 (frozen R² 0.565, task-aware 0.683).
- Metric: none found (the Kaggle page defines no task; MulTaBench reports R² for every regression set, a benchmark-wide choice, not one for this task, MET-5), so the fallback `rmse`, the price shipped on a log scale and scored in PKR (MET-3); inputs none.
- Risks for /add-dataset: tiny (400 items, three inputs; TP-5, TP-8 for the probes); one design in several colours may share a price (group by the id prefix, SPLIT); `Availability` is constant; the photo is dropped (SEL-12) and the description string carries most of what is left.
- Priority: gap 0 (business & marketing holds 25 accepted datasets, regression is not thin), use case 0 (written by the curation), source 0 (an individual's scrape, the columns described only by name), shape - (400 rows, three inputs).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 400 rows; 2 structured, 1 text, 1 image features (MulTaBench Table 3); target: Retail price (PKR).
- Why: Predict a Khaadi apparel item's retail price from image, colour, category and description
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2023 scrape; tiny.
