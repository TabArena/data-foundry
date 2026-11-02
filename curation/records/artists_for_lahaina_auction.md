---
unique_name: artists_for_lahaina_auction
name: Lahaina Art Auction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- Tiny Data
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2023'
domain: business & marketing
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/quillen/artists-for-lahaina-2023
- https://arxiv.org/abs/2605.10616
- https://huggingface.co/datasets/multabench/extended-img-reg-lahaina-auction
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: the winning bids of one 2023 charity art auction (968 paintings sold), scraped by a bidder; the tabular columns carry the signal (MulTaBench Table 8: structured R² 0.558, photo and text 0.093, joint 0.576), but it is one small event with no task of its own.
- Source: Kaggle quillen/artists-for-lahaina-2023 ("Artists for Lahaina 2023", uploaded 2023-09-27, CC BY-NC-SA 4.0, source https://artistslahaina.betterworld.org/): "This dataset covers all paintings sold in the Artists for Lahaina 2023 charity art auction"; plein-air painters donated work, proceeds to the Maui Pono Foundation after the August 2023 Lahaina fire; files `data/data.csv`, `data/clean_data.csv` and one image per painting; the uploader is "not affiliated with Artists for Lahaina nor the Maui Pono Foundation (although I bid on a few of these paintings)". As used by MulTaBench (extended release, Joint Signal only; https://huggingface.co/datasets/multabench/extended-img-reg-lahaina-auction): 968 rows, `artist`, `title`, `medium`, `dim1`, `dim2`, stated `value`, `buy_now`, `Gallery`, the photo, target `winning_bid` (the two preview rows: bids of 54% and 61% of the stated value).
- Use case: none in the source; the candidate is an auction organiser setting a starting bid or estimate for a donated painting (written by the curation); fit approximate: one charity event, whose bids follow goodwill as much as a market. Regime IID within the one auction, or grouped by artist (artists gave several works).
- Siblings and duplicates: none (grep over the records for lahaina, the Kaggle slug); art-price record from another source: `painting_price` (MulTaBench core). External collections: MulTaBench (extended image release).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the Kaggle page; the auction page (not reachable here, HTTP 403); MulTaBench (https://arxiv.org/abs/2605.10616), Table 8.
- Metric: none found (the Kaggle page defines no task; MulTaBench's R² is benchmark-wide, MET-5), so the fallback `rmse`, with a log target scored in dollars (MET-3); inputs none.
- Risks for /add-dataset: `buy_now` may record that a painting sold at its buy-now price, which is the outcome itself (LEAK-10: check it against `winning_bid`); only sold paintings (`Selection Bias`); 968 rows (`Tiny Data`); the photo is dropped (SEL-12); a third-party scrape of the auction platform (PROV-2).
- Priority: gap 0, use case 0, source 0 (a Kaggle scrape with a clear description, no documentation by the auction), shape 0 (968 rows, under about 1,000), risk - (the buy-now flag, one event).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 968 rows; 6 structured, 2 text, 1 image features (MulTaBench Table 9); target: Winning bid.
- Why: Predict the winning bid of a charity-auction painting
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Artists for Lahaina 2023 charity auction (Kaggle, CC BY-NC-SA); stated value and ...
