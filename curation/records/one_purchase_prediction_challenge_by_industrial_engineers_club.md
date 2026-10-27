---
unique_name: one_purchase_prediction_challenge_by_industrial_engineers_club
name: One Purchase Prediction Challenge by Industrial Engineers Club
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://zindi.africa/competitions/iec-algeria-data-cup-by-temtem-purchase-prediction-challenge
source_row: 1008
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: a real repeat-purchase task from an Algerian shopping app with a stated business use and AUC; small, one snapshot, and the order items must be aggregated per customer.
- Source: Zindi hackathon "IEC ALGERIA Data Cup by Temtem One Purchase Prediction Challenge", Industrial Engineers Club with Temtem One, 17-21 December 2021, private to Algerian Data Cup participants (93 participants, 49 on the leaderboard). As published: Train.csv (2.3 MB) and Test.csv (1.6 MB), one row per order item; "The data contains 29774 order" from 1 January to 15 February 2021; columns Order ID, Order Status, Category Name, Product Name (French), Quantity, Unit Price, Total Price, Subtotal, Payment Method, Customer ID, Merchant, Order Time, Customer Country, and the target "Purchase Again": "1 corresponds to that the customer will make a new purchase after february 15th, 0 else". Customers, not orders, are the unit (the submission is per customer).
- Use case: Temtem, on 15 February, decides which customers to target for retention ("help Temtem improve it's UX, it's marketing strategy"); fit direct. Regime IID across customers: "Both train and test set contains order during the same period", one prediction point for every customer, so a temporal split has nothing to order; the old `Temporal (NON-IID)` value was AI-filled and is changed to `Random (IID)`.
- Siblings and duplicates: none in `curation/records/` (grep on temtem, purchase). External collections: none found.
- Papers and pages: the Zindi page (description, data, evaluation); discussions are private. No paper.
- Metric: "The evaluation metric for this challenge is Area Under the Curve (AUC)" (Zindi Evaluation page; API `error_metric: area_under_curve`), a competition's metric (MET-4): `roc_auc` per customer. Inputs: none.
- Risks for /add-dataset: build one row per customer from the order items (the aggregation is ours; keep Order Status, since rejected orders are not purchases); the number of customers is not stated (a 9.9 KB submission file suggests about a thousand test customers), so check `Too Small` (TP-5); Zindi data needs a login and the hackathon was private, so access is a question for the curator; the target window (15 February to 20 March) lies after the prediction point, which is fine.
- Priority: gap 0 (business), use case + (the host names its decision), source + (the competition page documents the columns and the target), shape 0 (customer count unknown, likely a few thousand), risk - (aggregation, size).

A Zindi competition whose stated goal is to predict which customers will purchase again, i.e. a repeat-purchase / churn-style binary classification over customer records. This is a genuine real-world predictive task rather than CTR/ranking, and such e-commerce transaction data is typically tabular and adequately sized. It may need a temporal split and some transaction aggregation. Suggest TBD -> Yes; a human must verify the data layout (single table vs transaction log to aggregate), the exact target definition, and post-processing size.

---

predict which customer will purchase again
