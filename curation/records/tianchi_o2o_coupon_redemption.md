---
unique_name: tianchi_o2o_coupon_redemption
name: Tianchi O2O coupon usage prediction (O2O优惠券使用预测), Alibaba Tianchi 2016
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Company
year: '2016'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://tianchi.aliyun.com/competition/entrance/231587/introduction
- https://tianchi.aliyun.com/competition/entrance/231593/information
- https://github.com/wepe/O2O-Coupon-Usage-Forecast
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: Alibaba Tianchi's 2016 O2O competition on whether a user redeems a received coupon within 15 days, from six months of offline and online coupon and purchase logs, scored by AUC per coupon; real redemptions where `in_vehicle_coupon_recommendation` has survey answers, but the logs must be aggregated, a known leak avoided, and the scope call (coupon targeting, close to conversion prediction) is the curator's.
- Source: Alibaba Cloud Tianchi, "O2O优惠券使用预测" (competition 231587, re-run as the newcomer race 231593 on the same data); the pages render by JavaScript and were not read. As described by the first-placed team's repository (github.com/wepe/O2O-Coupon-Usage-Forecast) and a tutorial (cnblogs, boostwei): predict whether users who receive a coupon in July 2016 redeem it within 15 days ("预测用户在2016年7月领取优惠券后15天以内是否核销"); files ccf_offline_stage1_train (offline purchases and coupon receipts), ccf_online_stage1_train (online clicks, purchases and coupons), ccf_offline_stage1_test_revised (the July receipts to score); fields User_id, Merchant_id, Coupon_id, Discount_rate (a rate, "x:y" for spend x save y, or fixed), Distance (0-10 in units of 500 m), Date_received, Date; records from 2016-01-01 to 2016-06-30. The row counts (about 1.75 million offline and 11.4 million online rows) are as widely reported, not confirmed.
- Use case: a merchant or the platform decides at issue which users get which coupon, so that coupons are redeemed and not wasted; the competition's own background was not read, so the actor is the curation's reading. Fit direct once the features stop at the receipt date. Regime temporal by Date_received (labels public for January to June 2016 only), SPLIT-6.
- Siblings and duplicates: `in_vehicle_coupon_recommendation` (Yes, `Selection Bias`; MTurk scenarios, re-split by respondent); `ijcai15_repeat_buyers` (TBD -> Yes, another Alibaba competition, a different task). No record of this competition before (grep tianchi, o2o, coupon). Another source, not a duplicate (PROV-4). External collections: none found.
- Better data: found as better data for `in_vehicle_coupon_recommendation`; no further search this round.
- Papers and pages: the winners' repository (GBDT and XGBoost on user, merchant, coupon and user-merchant aggregates); a Chinese journal paper with XGBoost (AUC about 0.82, seen only as a search snippet).
- Metric: AUC computed per coupon and averaged over coupons ("先对每个优惠券单独计算核销预测的AUC值，再对所有优惠券的AUC值求平均", the winners' README; the official page not read): the leaderboard metric (MET-4), a mean of per-group ROC AUC with `Coupon_id` as a scoring column, never a feature (MET-2); a general name and a library implementation are needed (MET-12, MET-13), and coupons with one class in a test window drop out.
- Risks for /add-dataset: features only from records before each receipt; the winners' "leak" features from the July receipts (a user's later receipts) raised AUC by about 10 points and, in their words, cannot be obtained in real business (LEAK-10); relational logs to aggregate (user, merchant, coupon, user-merchant); a label needs 15 days after receipt, so training labels near a window's start mature after it (SPLIT-9); whether coupon targeting is marketing response (in scope, as `coil_2000`) or conversion prediction (SEL-9) is the curator's call; Tianchi registration and terms (EV-4).
- Priority: gap 0 (business & marketing, binary and temporal not thin), use case 0 (the official background not read), source + (an Alibaba competition), shape + (millions of log rows over six months), risk - (heavy aggregation and a documented leak).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `in_vehicle_coupon_recommendation`.
- as published: as widely reported (to verify on the page): offline table of about 1.75 million user-merchant records with coupon receipt and use dates (User_id, Merchant_id, Coupon_id, Discount_rate, Distance, ...; target: whether the user redeems the received coupon within 15 days of receiving it (core: Date - Date_received <= 15 days); metric AUC computed per coupon and averaged; access: registration.
- Why: in_vehicle_coupon_recommendation predicts whether a driver accepts a coupon for a nearby venue from the coupon type, expiry, distance/direction and the person's habits; here the same decision (send this coupon to this user?) with the actual redemption as target, features of the same kind (discount type and rate, ...
- Adds: real behaviour instead of MTurk answers about imagined trips (the record carries Selection Bias and a stated-intention gap), about 100x more coupon events, six months of dates for a temporal split. Caveats: relational logs that need aggregation per user, merchant and coupon up to the receipt date; no context such as ...
