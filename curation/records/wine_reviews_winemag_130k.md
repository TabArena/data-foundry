---
unique_name: wine_reviews_winemag_130k
name: Wine Reviews (WineEnthusiast reviews, 130k)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
tags:
- Free Text (Sentences)
- AI-Filled (Verify)
collections:
- AutoML_MM
- MulTaBench
original_source: Kaggle
year: '2017'
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/zynicide/wine-reviews
- https://github.com/zackthoutt/wine-deep-learning
- https://www.winemag.com/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: the 2017 Kaggle scrape of about 130,000 Wine Enthusiast reviews, published to predict a wine's variety from the tasting note (a text task) and reused for the critic's points; the same source as `wineenthusiasts` (a later scrape), so a version (PROV-6) with that record's open target and taster-name concerns.
- Source: Zack Thoutt, Kaggle zynicide/wine-reviews: "The data was scraped from WineEnthusiast during the week of June 15th, 2017"; "I scraped the reviews again on November 22nd, 2017. This time around I collected the title of each review, which you can parse the year out of, the tasters name, and the taster's Twitter handle. This should also fix the duplicate entry issue" (scraper at github.com/zackthoutt/wine-deep-learning); CC BY-NC-SA 4.0. Files: `winemag-data-130k-v2.csv` (52.9 MB; columns country, description, designation, points, price, province, region_1, region_2, taster_name, taster_twitter_handle, title, variety, winery), `winemag-data_first150k.csv` (the June scrape) and a JSON copy.
- Original task (SEL-8): "I plan to use deep learning to predict the wine variety using words in the description/review ... My overall goal is to create a model that can identify the variety, winery, and location of a wine based on a description": a text task (SEL-12 to weigh). Points (80-100) or price as targets are reuses; a merchant estimating a critic's score or a price from origin, variety, winery and vintage is our reading, fit approximate; the tasting note is written with the score, so it is not known before it (USE-3). Regime temporal by the vintage in `title` (no review date), or grouped by winery or taster.
- Siblings and duplicates: `wineenthusiasts` (Lennart, `TBD -> 2nd Tier`, `No Good Target (yet)`, `Ethical Issue`: "names and Twitter handles of reviewers ... Could likely be fixed"; the manyregression update built on this scraper): the same source, a version (PROV-6), and at most one enters; `wine_rating_price`, `winevivino`, `spanish_wine_quality_dataset` and `x_wines` are user ratings from other sources. External collections: AutoML Multimodal `wine_reviews` (OpenML 46653: "Classify the variety of wines based on tasting descriptions from sommeliers", "collected from WineEnthusiast", linking this Kaggle page) and MulTaBench's "Wine Review", taken from it (the run's assessment on `wineenthusiasts`).
- Better data: found as better data for `wineenthusiasts`; no further search this round.
- Papers and pages: the Kaggle page (metadata read through the API); OpenML 46653 (read); the AutoML Multimodal paper (Shi et al. 2021) not read.
- Metric: none for points or price (a Kaggle dataset, no task); the AutoML Multimodal benchmark scores variety as a text-tabular task (its metric not read). Fallback `rmse` for points (MET-8). Inputs: none.
- Risks for /add-dataset: `taster_name` and `taster_twitter_handle` (the sibling's SEL-1 concern; drop); the tasting note (drop for a pre-review target, or the task turns into text); duplicate reviews between the two files and against the sibling's update; the vintage parsed from `title`.
- Priority: gap 0 (business, regression not thin), use case 0 (none in the source for points), source 0 (a Kaggle scrape with its code, no paper), shape + (about 130,000 reviews, mixed types), risk - (a version of a recorded source, a text-led original task, personal columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `wineenthusiasts`.
- as published: winemag-data-130k-v2.csv: about 130k reviews x 13 columns (country, description, designation, points, price, province, region_1, region_2, taster_name, taster_twitter_handle, title, variety, ...; target: points (Wine Enthusiast score, 80-100); price also present; access: open (CC BY-NC-SA 4.0).
- Why: The wineenthusiasts record (manyregression, 81k reviews 2017-2020) is built on this scraper ('I built it on zynicide/wine-reviews updating the scraper fetching fresh data'); same source, same columns, earlier reviews
- Adds: About 130k earlier reviews; together with the 2017-2020 update about 210k reviews over a longer span after removing the 2017 overlap, which gives a temporal split more years. A version of the same source (PROV-6); the curator decides which file enters. Same caveats as the record: taster names and Twitter handles ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
