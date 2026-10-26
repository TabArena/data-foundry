---
unique_name: zimnat_insurance_recommendation_challenge
name: zimnat-insurance-recommendation-challenge
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
domain: insurance
required_split:
- '?'
problem_type: Other
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/zimnat-insurance-recommendation-challenge
- https://zindi.africa/competitions/indabax-sa-2022-intermediate
source_row: 919
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9): a hold-one-out product recommendation over a customer x product holdings matrix, which Zindi itself tags as collaborative filtering.
- Source: Zindi competition "Zimnat Insurance Recommendation Challenge", 2020-07-01 to 2020-09-13, Zimnat (Zimbabwe) (https://zindi.africa/competitions/zimnat-insurance-recommendation-challenge, read through Zindi's page API); as published: "data on nearly 40,000 customers who have purchased two or more insurance products"; one row per customer with "some information on the customer (when they joined, birth year etc)", the occupation, occupation category and branch codes, then "The final 21 columns correspond to the 21 products on offer"; in Test "for each customer ONE product has been removed (the 1 replaced with a 0). Your goal is to build a model to predict the missing product".
- Use case: "Zimnat wants an ML model to use customer data to predict which kinds of insurance products to recommend to customers ... This same model can then be applied to any customer to identify insurance products that might be useful to them".
- Siblings and duplicates: the second link, `indabax-sa-2022-intermediate` ("Insurance Recommendation Challenge", Dec 2022), is a rerun (API parent `zimnat-insurance-recommendation-challenge`, the same text); other Zimnat records are other tasks (`zimnat_loan_default_predictio`, `the_zimnat_insurance_assurance_challenge`); same pattern: `farm_to_feed_shopping_basket_recommendation_challenge`, `xente_purchase_prediction_challenge`.
- Metric: log loss over every customer x product pair ("For every customer ID in the test set, for each product code, you must submit a prediction", Evaluation tab).
- Steelman: insurance is a thin domain, and a per-product propensity model on the customer attributes is a classification; but the source's task is to recover a masked item from the other items a customer holds (the holdings are the main input), a recommendation set-up, and no observed later purchase is the label.
- Why it fails: a recommendation task by the source's own words and design (SEL-9).
- Reject check (AI, 2026-10-22): stands. SEL-9 (Must) in the source's own words and design. "Zimnat wants an ML model to use customer data to predict which kinds of insurance products to recommend to customers". Test: "for each customer ONE product has been removed (the 1 replaced with a 0). Your goal is to build a model to predict the missing product". Zindi type_of_problem: ["Prediction", "Collaborative Filtering"]. The label is an artificially masked held item, not an observed later purchase, so a per-product propensity reframing would be our own task (SEL-8). It is consistent with the curator's RecSys rejects (kasandr, reasoner_recommendation, anime_planet; Lennart). The one counter-precedent, Andrej's 'Yes' on farm_to_feed, is still open, and the AI recommended 'No' there. https://zindi.africa/competitions/zimnat-insurance-recommendation-challenge

Zimnat insurance recommendation challenge (Zindi) asks to predict which insurance product a client wants next, an explicit recommendation/next-product task. This is an out-of-scope RecSys/ranking problem rather than a standard tabular classification/regression with a single fixed target. Even though the underlying customer table is tabular, the task framing is recommendation. The name itself flags it; suggestion is No.

---

Predict which insurance a client wants next
