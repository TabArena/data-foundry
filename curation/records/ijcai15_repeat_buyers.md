---
unique_name: ijcai15_repeat_buyers
name: IJCAI-15 Repeat Buyers Prediction Dataset (Tmall.com)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Company
year: '2015'
domain: business & marketing
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://tianchi.aliyun.com/dataset/42
- https://tianchi.aliyun.com/competition/entrance/231576/information
- https://groups.google.com/g/resys/c/oK8DzKHho1c
- https://doi.org/10.1145/2939672.2939674
- https://ijcai-15.org/index.php/repeat-buyers-prediction-competition
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Alibaba's IJCAI-15 competition on whether a buyer the merchant won on the Double 11 promotion buys from it again within six months, scored by AUC; a real retention task with demographics and a six-month behaviour log, which has to be aggregated to user x merchant pairs.
- Source: Alibaba Group with Tmall.com, IJCAI-15 Repeat Buyers Prediction Competition (April to June 2015), kept as Tianchi dataset 42. As published (call for participants on the RecSys list): "anonymized users' shopping logs in the past 6 months before and on the "Double 11" day", user demographics, and user x merchant pairs labelled "'1' denotes 'user_id' is a repeat buyer for 'merchant_id', while '0' is the opposite", "-1" for a user who is not a new customer of the merchant, "NULL" for test pairs; each log entry is `item_id:category_id:brand_id:time_stamp:action_type`. ijcai-15.org: "around 200k users" for training and a test set "of similar size". The commonly cited file counts (about 260k labelled training pairs, a test file without labels, about 424k users, a log of about 55M rows) are not confirmed: the Tianchi pages render by JavaScript and need a login.
- Use case: a merchant (or Tmall's CRM team), right after the promotion, decides which new buyers get retention offers; the competition text motivates this with sellers who "run big promotions" (seen only as a search snippet). Fit direct. Regime: every pair shares one prediction point (Double 11), so no temporal split; a user appears with several merchants, so grouped by user is likely (SPLIT-1, USE-10), to settle at add.
- Siblings and duplicates: `acquire_valued_shoppers_challenge` (Yes, `Anonymized`; Kaggle 2014, repeat purchase after an offer, US grocery), `ecom_offers_grouped_version` (TBD -> Yes, a framing of the same Kaggle data), `one_purchase_prediction_challenge_by_industrial_engineers_club` (TBD -> Yes, Temtem), `e_commerce_customer_data_for_behavior_analysis` (No, AHDS); `tianchi_o2o_coupon_redemption` (another Tianchi candidate of this run, coupon redemption, a different task). No duplicate (grep tianchi, ijcai, repeat buyer). External collections: none found.
- Better data: found as better data for `acquire_valued_shoppers_challenge`, `ecom_offers_grouped_version`, `one_purchase_prediction_challenge_by_industrial_engineers_club` and `e_commerce_customer_data_for_behavior_analysis`; another source, not a version (PROV-4).
- Papers and pages: Liu et al., "Repeat Buyer Prediction for E-Commerce", KDD 2016 (doi 10.1145/2939672.2939674; not read, the ACM page returns 403); the competition pages above.
- Metric: "The Area Under the ROC Curve (AUC), true positive versus false positive is employed as evaluation metric" (call for participants): the leaderboard metric (MET-4), `roc_auc`; inputs none.
- Risks for /add-dataset: build pair features from the log up to and on Double 11 only, and check that no later events are in it (LEAK-10); drop the -1 pairs; only the training pairs carry labels (to confirm after login); a large log to aggregate across three tables; Tianchi registration and terms (EV-4, no criterion).
- Priority: gap 0 (business & marketing, binary and grouped are well covered), use case +, source + (Alibaba competition with a paper), shape + (about 260k labelled pairs, demographics, behaviour log), risk - (heavy aggregation of the log across tables).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `acquire_valued_shoppers_challenge`, `e_commerce_customer_data_for_behavior_analysis`, `ecom_offers_grouped_version`, `one_purchase_prediction_challenge_by_industrial_engineers_club`.
- as published: about 424,170 users with a six-month behaviour log (order, click, cart, favourite events on item / category / brand ids) ending at the 11 November sale, plus a user profile (age range, gender); ...; target: binary: does a new buyer at a merchant on the promotion day buy from that merchant again within the next six months; access: registration.
- Why: the same task as Acquire Valued Shoppers: repeat purchase after a promotion, one row per customer x merchant/offer, with features built from the customer's transaction log up to the offer and nothing after it; temporal regime around one promotion date | Acquire Valued Shoppers predicts whether a shopper given an ...
- Adds: a year newer (2015) and a second market and population (Chinese e-commerce rather than US grocery); the outcome horizon is six months instead of the Kaggle 30 days; demographics (age range, gender) and category/brand ids ship, where the Kaggle file is fully anonymized ids (the old record's Anonymized marker); the log ...
