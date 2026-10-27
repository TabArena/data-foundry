---
unique_name: farm_to_feed_shopping_basket_recommendation_challenge
name: farm-to-feed-shopping-basket-recommendation-challenge
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
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

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape +, risk - (Run recommended not adding: out-of-scope recommender (CTR/RecSys) task, open issue 1). A weekly customer-by-SKU recommender grid whose purchase-recency baseline beats the models; out of scope as RecSys and forecasting.

CC (2026-10-26, Lennart): leave out: "Yes, retire it, and no, it seems to be recsys or at least weirdly translated recsys setting".

**Assessment (AI, 2026-10-26):** the open issues of 2026-10-07 are settled and removed from this record. Zindi asks "to help build a recommender system for their app"; the data is the full 141 x 326 customer x SKU grid of every week with next week's cell as the target, and the pair's purchase recency alone (ROC AUC 0.943) beats LightGBM on the row as served (0.928). The three other Zindi recommender records (zimnat_insurance_recommendation_challenge, akeed_restaurant_recommendation_challenge, xente_purchase_prediction_challenge) follow the same pattern.
