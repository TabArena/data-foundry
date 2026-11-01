---
unique_name: flower_bouquets_rating
name: Flower Bouquets
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
- https://www.kaggle.com/datasets/samoilovmikhail/floral-bouquets-images-and-girlfriend-scores
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-12, SEL-13): one person's 1-5 aesthetic score of 600 bouquet photos; the uploader publishes it as "A multimodal computer-vision dataset for aesthetic-rating prediction", and the target is a human scoring what they see in an image.
- Source: Kaggle upload by samoilovmikhail, "Floral Bouquets: Images and Girlfriend Scores" (<https://www.kaggle.com/datasets/samoilovmikhail/floral-bouquets-images-and-girlfriend-scores>, `flowers.csv` dated 2025-08-26, Apache 2.0): "Can a model learn my girlfriend's taste in flowers?"; "Every bouquet has been manually evaluated by a single annotator and assigned a rating on a scale of 1 (dislike) to 5 (love), reflecting a consistent, personal measure of aesthetic appeal." As MulTaBench ships it (core, Table 3): 600 rows, the description, the shop's comment-based rating, the price in RUB and in USD, one photo; target `girlfriend_rating` (5 classes). MulTaBench's Appendix B.1 calls the target "a customer satisfaction rating", which the source contradicts.
- Use case: none: the label is one person's taste, and the only decision it could serve (which bouquet to buy for her) is a personal recommendation (SEL-9); regime IID.
- Siblings and duplicates: none (searched bouquet, florist). External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench (not searched in this run, by its brief).
- Papers and pages: the Kaggle page; MulTaBench (Arazi et al. 2026, arXiv 2605.10616, Appendix B.1; Table 11: AUROC 0.627 with frozen embeddings, 0.636 with target-aware ones).
- Metric: none in the source (it lists possible tasks); MulTaBench scores AUROC.
- Risks for /add-dataset: not applicable; besides, 600 rows over 5 classes (TP-5) and the price stored twice (RUB and a converted USD).
- Reject check (AI, 2026-10-31): stands. The uploader: 'A multimodal computer-vision dataset for aesthetic-rating prediction', 'Every bouquet has been manually evaluated by a single annotator ... reflecting a consistent, personal measure of aesthetic appeal', and the use it names is 'Personalized Recommendation Systems' (Kaggle description via the API, https://www.kaggle.com/datasets/samoilovmikhail/floral-bouquets-images-and-girlfriend-scores). Without the photo, price and description would predict one person's visual taste, which no actor decides with.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 600 rows; 3 structured, 1 text, 1 image features (MulTaBench Table 3); target: Rating 1-5 (5 classes).
- Why: Predict the rating of a florist's bouquet from photo, description and price
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2025 (Apache 2.0). The paper calls the target customer satisfaction at a Russian online florist; the Kaggle title calls it 'girlfriend scores' (human ...
