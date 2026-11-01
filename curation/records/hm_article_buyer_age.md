---
unique_name: hm_article_buyer_age
name: H&M Fashion
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations
- https://www.kaggle.com/datasets/odins0n/handm-dataset-128x128
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9, SEL-8): the data comes from the H&M Personalized Fashion Recommendations competition, "Provide product recommendations based on previous purchases" (Kaggle, 2022, MAP@12); the buyer-age regression is MulTaBench's re-framing, an aggregate it computes from the transactions and customers, the case `yearprediction_the_million_song_dataset` settled.
- Source: H&M Group on Kaggle (<https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations>, February to May 2022, 2,952 teams): articles (product metadata and images), customers (with age) and two years of transactions. MulTaBench (core, Table 3) takes the articles with resized images from a Kaggle user's copy (odins0n/handm-dataset-128x128): 104,072 rows, 12 article attributes (product type and group, colour group and perceived colour, graphical appearance, department, index, section, garment group), the product name and description as text, one image; target `AvgConsumerAge`, "the average age of purchasing customers".
- Use case: the competition's is recommending articles to customers (SEL-9). The steelman for the re-framing: a merchandiser profiles a new article's buyers before launch; nobody in the source asks it, and the target averages purchases over two years with no prediction point (USE-3). Regime IID by article as MulTaBench ships it.
- Siblings and duplicates: no record of this competition (searched h-and-m, H&M, odins0n). External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench (not searched in this run, by its brief).
- Papers and pages: the Kaggle competition; MulTaBench (arXiv 2605.10616, Appendix B.1; Table 11: R² 0.389 frozen, 0.404 target-aware).
- Metric: MAP@{K} (the competition's `evaluationMetric` from the Kaggle API; K = 12 on its evaluation page, not re-read), a ranking metric; MulTaBench scores R².
- Risks for /add-dataset: not applicable.
- Reject check (AI, 2026-10-31): stands. The data comes from the H&M Personalized Fashion Recommendations competition, 12 recommended articles per customer scored by MAP@12 (https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations); the buyer-age target is MulTaBench's aggregate over two years of transactions, which no source asks for. Same facts as `yearprediction_the_million_song_dataset`: a recommendation source re-targeted as a regression by a re-upload.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 104,072 rows; 9 structured, 4 text, 1 image features (MulTaBench Table 3); target: Average age of purchasing customers per article.
- Why: Predict the average age of an article's buyers from its image, attributes and description
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. H&M 2022 Kaggle recommendation competition (images resized by a Kaggle user); the target is an aggregate MulTaBench derives from the transactions and customers tables.
