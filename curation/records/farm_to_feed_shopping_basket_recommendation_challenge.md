---
unique_name: farm_to_feed_shopping_basket_recommendation_challenge
name: farm-to-feed-shopping-basket-recommendation-challenge
checked_by:
- Andrej
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- Multi-target
collections:
- New (BeyondArena)
original_source: Zindi
year: '2025'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/farm-to-feed-shopping-basket-recommendation-challenge
source_row: 740
type_adapter_id: curation-record-v1
---

## Comments

Competition used temporal split.

Multi-target task: Predict whether purchase happens along with quantity. Performance was measured using AUC (50%) and MAE (50%)

Domain: agriculture

**Assessment (AI, 2026-10-07):** Recommend `No` + `Out-of-scope Task (CTR/RecSys/Ranking)` (criterion 3). Zindi's Description: "your challenge is to help build a recommender system for their app". Train.csv is the full customer x SKU grid (141 x 326 = 45,966 pairs in each of 46 weeks); the target is the pair's next-week purchase (equal to the next week's row in 100% of rows); test rows carry only ids and static attributes. On the last 6 training weeks, SKU popularity alone gives ROC AUC 0.848 (LightGBM on the static attributes 0.850), and the pair's purchase recency alone 0.943, above LightGBM on the row as served (0.928). The quantity targets are each pair's next-week demand (forecasting). Mirror: Kaggle `juliusmwangi/farm-to-feed-shopping-basket-recommendation` (file sizes identical).

**Open issues (AI, 2026-10-07):** not added; recommended `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`). The
competition asks for a recommender system, and the data is the full customer x product grid of every week.

1. **Scope: recommend `No` + `Out-of-scope Task (CTR/RecSys/Ranking)`.** `Time-series (Forecasting)` could be added
   as a second marker for the quantity targets. Question: is this the recommender exclusion of criterion 3? The
   record says `Yes` (Andrej), with the temporal split and the two targets described, and the recommender framing not
   discussed.
   - Evidence: Zindi's Description, "your challenge is to help build a recommender system for their app".
   - The data is the full 141 x 326 customer x SKU grid in every week, and the target is the next week's cell.
   - Test rows carry only ids and static attributes.
   - SKU popularity alone (ROC AUC 0.848) matches LightGBM on the static attributes (0.850), and the pair's purchase
     recency alone (0.943) beats LightGBM on the row as served (0.928). Rows of existing customers, last 6 training
     weeks.
   - Implemented now: nothing added.
   - Alternative: issue 2.

2. **If the `Yes` stands, the definition would need these choices (none implemented):**
   - Target: `Target_purchase_next_1w` only (binary, ROC AUC, as the competition scored it). The 2-week purchase and
     both quantities are the same series one or two weeks on, and the quantities are 97.9% zeros.
   - Rows: Train.csv only. Drop the 863,248 padding rows dated before the customer existed, which leaves 1,251,188
     rows.
   - Split: temporal, 2-week windows with a 1-week gap (a week's label is known one week later). Three windows hold
     74,654-81,174 test rows (2,497-2,920 positives). Two of the three train sides (1,129,916 and 1,053,958 rows; the
     third 980,608) exceed the 1M budget, so it would ship as `..._1m` with `subsample_to_budget`.
   - The same 45,966 pairs recur every week: a grouped-temporal structure, which v2 cannot declare.
   - Features: the row as served (LightGBM ROC AUC 0.928 on the holdout). The house rule forbids engineered history,
     which leaves the models below a no-model recency baseline (0.943). With the pair's history added, as the
     `acquire_valued_shoppers_challenge` (TabReD) and `g_research_crypto_forecasting` precedents do, 0.967.

3. **Record housekeeping:**
   - Add the Kaggle mirror to `source_links` as the download route. Zindi needs a login; the mirror's file sizes match
     the competition's file list byte for byte.
   - Note the licence line (Zindi: "Data Sharing: Open source").
   - The three other Zindi recommender records (`zimnat_insurance_recommendation_challenge`,
     `akeed_restaurant_recommendation_challenge`, `xente_purchase_prediction_challenge`) are still
     `AI (UNVERIFIED)` `No`s; this record has the first data-based evidence for the pattern.
