---
unique_name: watch_price_within_brand
name: Watch Tier
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://www.kaggle.com/datasets/mathewkouch/a-dataset-of-watches
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-12): wristwatch photos with a brand and a product name; the brand is the only tabular column, and MulTaBench's target (the price over the brand's median price) removes what the brand tells by construction, so the task is reading the photo and the name.
- Source: Kaggle "A Dataset of Watches" by `mathewkouch` (2022-11-28, CC0), subtitle "Thousands of styles, with product name, brand, and prices": "This dataset contains 2553 watch images with accompanied product name, brand, and prices"; suggested uses: "Perform unsupervised learning to cluster and classify watches by styles/colour/gender/material", "Train a regression model to predict sale price of watches given its image and brand name", "Train generative model to produce novel watch designs"; tagged computer vision. MulTaBench extended (App. F.1): 1,260 rows over fifty brands; "The regression target is the price of the watch relative to the median price of its brand, so that the label measures within-brand positioning rather than brand identity. The brand is the only structured feature, with the model name as a text feature."
- Decisive: with the photo dropped, the data holds a brand and a product name. Under the source's own price target the brand is a lookup and the rest is in the name (text) and the photo; under MulTaBench's target the brand carries nothing. Modality-specific models are the tool (SEL-12). The target is also MulTaBench's construction, not a price anyone pays (USE-5).
- Use case: a retailer pricing a watch would use the reference, movement, case and condition, none of which the data holds; the source names none.
- Siblings and duplicates: no watch record. External collections: MulTaBench, extended release (admitted on Joint Signal only), as "Watch Tier".
- Better data: a candidate of the benchmark MulTaBench (the run searched no further).
- Papers and pages: the Kaggle page; MulTaBench (Arazi et al. 2026, arXiv 2605.10616, App. F.1).
- Metric: none found (the Kaggle page names none; MulTaBench reports R² as a benchmark convention).
- Reject check (AI, 2026-10-31): stands. MulTaBench App. F.1: 'The brand is the only structured feature, with the model name as a text feature' and the target is 'the price of the watch relative to the median price of its brand' (https://arxiv.org/abs/2605.10616); the source's own suggestion is to 'predict sale price of watches given its image and brand name' (https://www.kaggle.com/datasets/mathewkouch/a-dataset-of-watches). With one categorical column, either target is a photo and text task.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 1,260 rows; 1 structured, 1 text, 1 image features (MulTaBench Table 9); target: Price / brand median price.
- Why: Predict a watch's price relative to its brand median from photo, brand and model name
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2022 (CC0); target constructed by MulTaBench.
