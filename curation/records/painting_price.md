---
unique_name: painting_price
name: Painting Price
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2020'
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/denozavrus/paintings-price-prediction
- https://arxiv.org/abs/2605.10616
- https://huggingface.co/datasets/multabench/core-img-reg-painting-price
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 12,369 paintings with size, material, style tags and a price from an unnamed online art marketplace, uploaded to Kaggle without a description; a plausible pricing task, but the marketplace, the currency and whether the price is an asking price cannot be traced (PROV-2), and 16% of the prices are 0.
- Source: Kaggle upload by denozavrus, "Painting's price prediction" (2020-12-31, licence "unknown", no description). As published: `paintings_data.csv`, 12,369 rows x 249 columns (`image_url` holding only a local file name such as `img1.jpg`, `material`, `price`, `styles` as a comma list, `width`, `length`, and about 240 binary style tags, some misspelled such as `surrealizm`, `landsvape`) and 12,369 images. Prices from 0 to 101,000, median 970, 1,985 rows at 0, currency not stated; the sizes look like inches. MulTaBench (core, https://huggingface.co/datasets/multabench/core-img-reg-painting-price) keeps all columns, target `price`.
- Use case: the title names price prediction, no actor. A candidate: an online gallery suggests a price for a newly listed painting (as `mercari_price_suggestion`); fit approximate, since the price is most likely the artist's asking price, and the artist, a main driver of art prices, is not in the table. Regime IID (one snapshot, no dates).
- Siblings and duplicates: none (grep for painting, art and the Kaggle slug); `artists_for_lahaina_auction` (MulTaBench, the winning bids of one charity auction, `TBD -> 2nd Tier`) is an art-price set from another source. External collections: MulTaBench (core image set).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the Kaggle page; two community notebooks ("ArtExpert", 2023) use it for price regression from the image alone; MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Appendix B.1 ("an online art marketplace"), Table 3 (245 structured, 2 text, 1 image), Table 11 (frozen R² 0.270, task-aware 0.275, the one image set without a significant task-aware gain).
- Metric: none found (no description and no competition; MulTaBench's R² is benchmark-wide, MET-5), so the fallback `rmse` on a log price (MET-3); inputs none.
- Risks for /add-dataset: unknown marketplace and currency (PROV-2: keep with an approximate fit and a note, or drop); the zero prices are probably "sold" or "on request", not a price (USE-7, drop them); `styles` restates the binary tags (CLEAN); no artist id, so listings of one artist cannot be grouped; the image is dropped (SEL-12).
- Priority: gap 0, use case 0, source 0 (the marketplace cannot be traced), shape + (12,369 rows, size, material and tags), risk - (untraced source, an unclear price with many zeros).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 12,369 rows; 245 structured, 2 text, 1 image features (MulTaBench Table 3); target: Sale price.
- Why: Predict a painting's sale price on an online art marketplace from image, dimensions, material and style tags
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2020, no description or licence. Paper notes no significant TAR gain on this dataset.
