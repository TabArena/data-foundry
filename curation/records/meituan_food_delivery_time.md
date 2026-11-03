---
unique_name: meituan_food_delivery_time
name: 'Meituan: Operational-Level On-Demand Food Delivery Data for the INFORMS TSL Data-Driven Research Challenge'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Github
year: '2024'
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/meituan/Meituan-INFORMS-TSL-Research-Challenge
- https://doi.org/10.2139/ssrn.5696423
- https://raw.githubusercontent.com/meituan/Meituan-INFORMS-TSL-Research-Challenge/main/TSL-Meituan%20challenge_background%20and%20data_20240321.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the delivery time of 568,546 real Meituan food orders over eight days of October 2022, with order, merchant and courier ids and the platform's own promised time; the challenge names the prediction of pick-up and delivery timings as one of its research questions.
- Source: as for `meituan_courier_order_acceptance`: GitHub meituan/Meituan-INFORMS-TSL-Research-Challenge (created 2024-02-01), "Background and Data Description" (21 March 2024), supplementary document (15 October 2024), Wang et al., SSRN 5696423, 2025. As published: `all_waybill_info_meituan_0322.csv.zip`, 654,343 waybills (one per dispatch attempt; a refused order gets a new waybill), with order create time, promised delivery time (`estimate_arrived_time`), estimated meal-ready time ("should be interpreted as the estimated meal ready time", supplementary document, 2.5), push, dispatch, grab, fetch and arrive times, shifted coordinates (pickup, delivery, courier), area, merchant and courier ids, prebook and weekend flags; three more tables of waves and dispatch checkpoints.
- Use case: the platform, when an order is placed or dispatched, estimates when it will arrive, to promise a time and plan the assignment ("Develop models to predict courier delivery processes in uncertain environments, like precise timings for order pick-up and delivery, to improve system responsiveness and decision-making", Sample Question 4); fit direct. Target: arrive time minus order create time of each order's accepted waybill. Regime temporal by day (eight days) with couriers and merchants repeating (SPLIT-13); grouped by courier is the alternative.
- Siblings and duplicates: `meituan_courier_order_acceptance` (the same release, courier acceptance: a distinct task, PROV-7); `food_delivery_time` (`Yes`, shipped in TabArena v0.1 and BeyondArena; a Kaggle file of 45,451 deliveries whose delivery points are the restaurant plus one of 12 fixed offsets, AI assessment 2026-10-14): the same task from another source (PROV-4); `jd_com_msom_2020_delivery_time`, `lade_last_mile_delivery_eta`, `delivery_eta` and `sendy_logistics_challenge` are other platforms' delivery-time tasks. External collections: none found.
- Better data: found as better data for `food_delivery_time`; no further search this round.
- Papers and pages: the background and supplementary documents (read); Wang et al. 2025 (abstract via Crossref); Çınar et al., arXiv 2507.03634 (uses the offers, not the times).
- Metric: none found (an open research call without a leaderboard; background document, GitHub repo), so the fallback `rmse` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: grab, fetch and arrive times and the courier position come after the prediction point (USE-3, drop); the prediction point decides whether the courier id and dispatch time are inputs (at order creation no courier is assigned); the promised time is the platform's own estimate, a legitimate input (USE-6) and maybe a strong baseline (TP-4 to watch); "For non-existent time data, the corresponding timestamp is represented by 0" (background document), and the target has to be built from the order's accepted waybill; eight days give short windows (SPLIT-14, SPLIT-18); licence CC BY-NC 4.0, no redistribution without permission (a note, EV-4).
- Priority: gap 0 (regression and temporal are not thin), use case + (the source names timing prediction for dispatch), source + (the platform's documented release with a data paper), shape + (568,546 orders with coordinates, times and ids), risk 0 (the post-outcome columns are documented and easy to drop).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `food_delivery_time`.
- as published: all_waybill_info_meituan.csv: 654,343 waybill rows (one per dispatch attempt; an order refused by a courier gets a new waybill) over 8 days from 2022-10-17. Per waybill: order and waybill ID, date, ...; target: delivery duration of an order: arrive time minus order create time (or minus fetch time), for accepted waybills; access: open (GitHub download; CC BY-NC 4.0, no redistribution without permission).
- Why: Same target (time for a food order to reach the customer) and same kind of inputs (restaurant and delivery coordinates, courier, time of day). The data are real operational records from a large platform, with a documented data description
- Adds: About 14 times the rows of the 45,451-row Kaggle file, whose delivery addresses are synthetic offsets (restaurant plus one of 12 fixed offsets, AI assessment 2026-10-14). It adds real timestamps for a temporal split, the merchant's estimated meal-ready time and courier IDs for a grouped split. The promised delivery ...
