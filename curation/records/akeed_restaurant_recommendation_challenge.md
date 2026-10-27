---
unique_name: akeed_restaurant_recommendation_challenge
name: akeed-restaurant-recommendation-challenge
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
problem_type: Other
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/akeed-restaurant-recommendation-challenge/data
- https://zindi.africa/competitions/akeed-restaurant-recommendation-hackathon/data
source_row: 917
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9): Akeed's Zindi challenge asks for a recommendation engine: which of 100 vendors each customer location will order from.
- Source: Zindi competition by Akeed (Oman food delivery app) with UK Oman Digital Hub and PhazeRo, 2020-05-18 to 2020-08-16 ($3,000, 1,428 participants), launched by the #ZindiWeekendz hackathon of 2020-05-15/17 (the record's second link, same data); as published: train/test customers and locations, orders.csv, vendors.csv; the submission is every `CID X LOC_NUM X VENDOR` pair with a 0/1 target.
- Source's words: "The objective of this competition is to build a recommendation engine to predict what restaurants customers are most likely to order from given the customer location, restaurant information, and the customer order history".
- Siblings: `farm_to_feed_shopping_basket_recommendation_challenge` (a plain `Yes` by a curator; a recommendation task too, worth a consistency look).
- Metric: F1 on the pair labels (Zindi evaluation page).
- Reject check (AI, 2026-10-22): stands. SEL-9 (Must) is out even when served as classification. Source: "The objective of this competition is to build a recommendation engine to predict what restaurants customers are most likely to order from". Every CID x LOC_NUM x VENDOR pair is labelled 0/1. https://zindi.africa/competitions/akeed-restaurant-recommendation-challenge. Consistency flag for the curator: farm_to_feed_shopping_basket_recommendation_challenge is a plain Yes (Andrej), which contradicts this rule. Its record already holds an AI No recommendation under SEL-9 that has not been settled.

Zindi Akeed restaurant RECOMMENDATION challenge: predict which restaurants/vendors a customer will order from, a recommender-system / ranking task. Recommendation/RecSys is explicitly out of scope. The data is also a multi-table customer/order/vendor structure typical of recsys. Excluded; a human need only confirm it is not secretly a simple binary order-prediction reframed as tabular.
