---
unique_name: x_wines
name: 'X-Wines: a wine dataset for recommender systems and machine learning'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: Github
year: '2023'
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.3390/bdcc7010020
- https://github.com/rogerioxavier/X-Wines
- https://www.mdpi.com/2504-2289/7/1/20
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a 2023 data paper's 100,646 wines with 17 attributes and 21M dated user ratings, published for recommender systems; a wine-level mean rating from the attributes is a target we would build (a SEL-9 doubt), and the rating platform is not named.
- Source: de Azambuja, Morais and Filipe, "X-Wines: A Wine Dataset for Recommender Systems and Machine Learning", Big Data and Cognitive Computing 7(1):20 (2023, doi 10.3390/bdcc7010020); data at github.com/rogerioxavier/X-Wines, CC0-1.0. The README: "100,646 (100K) wine instances containing 17 selected attributes" and "21,013,536 (21M) ratings 5-stars instances, containing date and value a 1-5 scale", "collected on the open Web in 2022", over "10 years (2012-2021)"; three versions, Full (100,646 wines, 21M ratings, through a link in the Dataset folder), Slim (1,007 wines, 150,000 ratings) and Test (100 wines, 1,000 ratings). The 17 attribute names were not read (the paper page returned 403); the run lists type, elaboration, body, acidity, grapes, ABV, country, region, winery and vintages.
- Original task (SEL-8): the README offers it for "scientific experimentation about recommender systems and machine learning using neural networks", and the paper demonstrates "deep learning applications for recommender systems" (Semantic Scholar abstract): a user-wine rating matrix, a recommendation task (SEL-9). A wine's mean community rating from its listing attributes, for an importer or retailer before reviews accumulate, is the run's reading, not the source's; fit approximate. Regime grouped by winery or temporal by rating date, if built.
- Siblings and duplicates: `spanish_wine_quality_dataset` (AI screening, `TBD -> 2nd Tier`, priority 1, `No Good Target / Scientific Discovery`, `Not Representative`), `winevivino` (Lennart, `TBD -> 2nd Tier`, `No Good Target (yet)`) and `wine_rating_price` (Lennart, `TBD -> 2nd Tier`, `No Good Target (yet)`): the same kind of aggregated user rating from other scrapes; X-Wines does not name its platform, so a row overlap with the Vivino scrapes is possible (PROV-4 to check). External collections: none of our vocabulary.
- Better data: found as better data for `spanish_wine_quality_dataset`, `wine_rating_price` and `winevivino`; no further search this round.
- Papers and pages: the GitHub README (read); the Semantic Scholar record (abstract, 17 citations); the MDPI paper not read (403).
- Metric: none for a wine-level target (the paper's experiments are recommendation, not read), so the fallback `rmse` if the aggregate is built (MET-8). Inputs: none.
- Risks for /add-dataset: the target is our aggregate (USE-5; SEL-9 if the curator reads the source as recommendation only); the platform behind "the open Web" is unnamed (PROV-2: clarify); the Full version sits behind a link (not opened); attributes such as the list of vintages may be gathered after the ratings (USE-3).
- Priority: gap 0 (business, regression not thin), use case 0 (the source names recommendation, not this task), source + (a data paper, CC0, documented versions), shape + (100,646 wines, mixed attributes), risk - (a recommender source and a built target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `spanish_wine_quality_dataset`, `wine_rating_price`, `winevivino`.
- as published: Full: 100,646 wines x 17 attributes, 21,013,536 ratings by 1,056,079 users, ratings 2012-2021, collected on the open web 2022; Slim: 1,007 wines / 150,000 ratings; Test: 100 wines / 1,000 ratings; target: community rating of a wine on a 1-5 scale in 0.5 steps; the wine-level mean rating (and review count) by a group-by over the ratings table, i.e. the same ...; access: open, open (CC0-1.0; full version through the link in the GitHub Dataset folder).
- Why: same target as spanish_wine_quality_dataset (an aggregate user rating per wine) with features of the same kind known at that point: type, elaborate, body, acidity, grape varieties, ABV, country, region, winery, vintages - the exact column family of the Kaggle scrape | wine_rating_price (budnyak: 13k Vivino wines, ...
- Adds: 100,646 wines from 62 countries against about 2,048 unique rows after the Spanish file's 73% duplicate rows; the full 1-5 rating range instead of the scrape's 4.2 floor (Not Representative); per-rating rows with dates and user ids, so the aggregate can be rebuilt and a temporal or wine-grouped split is possible; CC0 ...
