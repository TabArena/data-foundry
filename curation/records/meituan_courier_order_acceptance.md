---
unique_name: meituan_courier_order_acceptance
name: 'Meituan: Operational-Level On-Demand Food Delivery Data for the 2025 INFORMS TSL Data-Driven Research Challenge'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
original_source: Github
year: '2024'
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/meituan/Meituan-INFORMS-TSL-Research-Challenge
- https://connect.informs.org/tsl/tslresources/datachallenge
- '# a paper that used the data (App. K.2), related work (PROV-12)'
- https://arxiv.org/abs/2507.03634
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: 654,343 dispatch offers of Meituan's food-delivery platform over eight days of October 2022, each with whether the courier accepted it; a real, documented release, held at 2nd Tier like the Sendy rider-response record, since an offer-acceptance label sits close to the CTR exclusion (SEL-9), and the courier's position ships only for accepted offers.
- Source: Meituan with Tsinghua University and Singapore Management University, the data of the First INFORMS TSL Data-Driven Research Challenge: GitHub meituan/Meituan-INFORMS-TSL-Research-Challenge (created 2024-02-01), "Background and Data Description" (21 March 2024), a supplementary document (15 October 2024), and the data paper Wang, Zhao, Yan, Wang, Liang, Hao, "Meituan: Operational-Level On-Demand Food Delivery Data for the 2025 INFORMS TSL Data-Driven Research Challenge", SSRN 5696423, 2025 ("568,546 orders, 4,955 couriers, and 4,962 merchants"). As published: `all_waybill_info_meituan_0322.csv.zip`, one row per waybill (654,343): order and waybill ids, date, area id, shifted pickup and delivery coordinates, merchant id, order create, promised delivery, estimated meal-ready, push and dispatch times, courier id, courier position at assignment, `is_courier_grabbed`, grab, fetch and arrive times, prebook and weekend flags ("a new waybill is created when the order is refused by a courier"); `courier_wave_info_meituan.csv` (206,748 waves); `dispatch_waybill_meituan.csv` (15,921 rows) and `dispatch_rider_meituan.csv` (62,044 candidate couriers with position and on-hand orders at a dispatch checkpoint).
- Use case: Meituan's dispatch system, every 30 seconds or minute, scores order-courier pairs by a matching degree that "considers factors that include route convenience, overtime risk, and courier willingness to accept the orders" (background document) and assigns the order; fit direct. Regime temporal by day (17-24 October 2022) or grouped by courier (4,955); couriers repeat across days, so a temporal split carries known couriers (SPLIT-13; decide at /add-dataset).
- Siblings and duplicates: `meituan_food_delivery_time` (this run, the same release, delivery duration: a distinct task, PROV-7); `delivery_rider_response_challenge_by_galsenai` (`TBD -> 2nd Tier`, priority 2; Sendy's Zindi hackathon, a 200,000-dispatch subset in Nairobi, accept, decline or ignore, scored by accuracy): the same task from another source (PROV-4); `jd_com_msom_2020_delivery_time` and `lade_last_mile_delivery_eta` are other platforms' delivery tasks. External collections: none found.
- Better data: found as better data for `delivery_rider_response_challenge_by_galsenai`; no further search this round.
- Papers and pages: the background and supplementary documents (read); Çınar, Archetti, Dullaert, Leitner, Waldherr, "Pricing, bundling, and driver behavior in crowdsourced delivery", arXiv 2507.03634, 2025, App. K.2, a pooled logit on the grab flag: "Acceptance is near-uniform at 89.1%, 30.7% of couriers never decline a single offer over the eight days".
- Metric: none found: the challenge is an open research call with "Sample Questions" and no leaderboard (background document, GitHub repo), so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: for a rejected waybill the courier position (`grab_lat`, `grab_lng`) and the grab, fetch and arrive times "are unavailable and set to 0" (supplementary document, 2.4), so they encode the label (LEAK-13, drop; the candidate positions of `dispatch_rider_meituan.csv` cover only 62,044 checkpoint rows); the courier's load at the offer has to be rebuilt from other waybills and waves; SEL-9, as on the Sendy record; 89% accepted and many couriers who never decline, so the courier id may carry much of the signal (grouped or temporal); licence CC BY-NC 4.0, "without permission, the distribution of this dataset to third parties is not allowed" (License.txt; a note, never a reason, EV-4).
- Priority: gap 0 (binary and the domain are not thin), use case + (the source names courier willingness in the dispatch score), source + (the platform's own release with documentation and a data paper), shape + (654,343 offers with coordinates, times and ids, temporal and grouped), risk - (label-coded zeros in the courier columns, the SEL-9 question).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `delivery_rider_response_challenge_by_galsenai`.
- as published: 654,343 delivery offers (waybills) to 4,955 couriers over 8 days, 17-24 October 2022 (Cinar et al., arXiv 2507.03634, App. K.2); files all_waybill_info_meituan_0322.csv.zip (38.8 MB zipped; ...; target: binary grab flag: whether the courier accepted the offered waybill (89.1% accepted; 30.7% of couriers never decline); access: open (GitHub download), CC BY-NC 4.0, academic and research use only; the licence file says no redistribution without permission, so shipping needs Meituan's consent.
- Why: same task as the Sendy dispatch record: the response of a rider to a dispatched delivery order, with order locations, rider position at dispatch and time of day as inputs; Meituan's label is accept vs not (Sendy's splits decline from ignore)
- Adds: about 3x the offers of Sendy's 200,000-dispatch subset, newer (2022 against 2019-2021), real operational data with a data paper and documented tables instead of a hackathon subset 'anonymized while preserving the distribution'; courier positions at each dispatch moment; a full week of a whole operation, so a temporal ...
