---
unique_name: xente_purchase_prediction_challenge
name: Xente Purchase Prediction Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Other
original_data_state: Other
source_links:
- https://zindi.africa/competitions/umojahack-2-xente-purchase-prediction-challenge
source_row: 1023
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9): a next-purchase recommendation over an account x day x product grid, built from a bare purchase log.
- Source: Zindi one-day student hackathon "UmojaHack #2: Xente Purchase Prediction Challenge (INTERMEDIATE)", 2020-03-21, Xente (Uganda) (https://zindi.africa/competitions/umojahack-2-xente-purchase-prediction-challenge, read through Zindi's page API); as published: `Train.csv` of transactions 2019-11-01 to 2020-02-23, "Each row contains an account ID ('acc'), the time and date of the transaction ('date') and the product ID ('PID')", `PID_Categories.csv`; the test is the week from 2020-02-23, "one row for each account for each day for each product".
- Use case: "predict what and when individuals will purchase next, based on their purchase history ... help Xente with target marketing": a recommender for the app; Zindi tags it "Forecast", "Product Recommendation", "Market Basket Analysis".
- Siblings and duplicates: other Xente records are other tasks (`xente_fraud_detection_challenge`, `sbtic_xente_credit_scoring_challenge`); the same pattern as `farm_to_feed_shopping_basket_recommendation_challenge` (customer x SKU x week grid, the 2026-10-07 assessment recommended `No` for the same reason) and `zimnat_insurance_recommendation_challenge`.
- Metric: F1 over the grid ("The error metric for this competition is the F1 Score", Evaluation tab).
- Why it fails: the task is which product each account buys on each day, a recommendation and next-event forecast over user-item pairs (SEL-9, and SEL-10 for the "when"); the data holds no attribute beyond the interaction log, so no tabular task remains after removing the framing.
- Reject check (AI, 2026-10-22): stands. SEL-9 (Must), SEL-10 as well. Zindi: "predict what and when individuals will purchase next, based on their purchase history ... help Xente with target marketing". Data: "Each row contains an account ID ('acc'), the time and date of the transaction ('date') and the product ID ('PID')". Submission: "one row for each account for each day for each product". Zindi tags include Product Recommendation, Market Basket Analysis and Personalization. The data has no attribute beyond the interaction log, so no tabular task is left once the recommender framing is removed. Andrej's open 'Yes' on farm_to_feed_shopping_basket_recommendation_challenge is not a like case: that grid has customer and SKU attributes, and it is undecided. https://zindi.africa/competitions/umojahack-2-xente-purchase-prediction-challenge

This UmojaHack/Xente challenge asks to predict when and what a customer will purchase on the Xente app, which is a recommendation/next-purchase prediction task. Such 'what will the user buy next' framings are out-of-scope RecSys/ranking tasks rather than a fixed tabular classification/regression. The data is user-item interaction logs rather than a clean predictive table. A human could confirm, but as described this is out of scope, so No.

---

Predict when and what a customer will purchase on the Xente app
