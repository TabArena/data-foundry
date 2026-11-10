---
unique_name: meituan_food_delivery_time
name: 'Meituan: Operational-Level On-Demand Food Delivery Data for the INFORMS TSL Data-Driven Research Challenge'
checked_by:
- Myunghwan
data_foundry_status:
- WIP (Triage)
- 'DF: Yes'
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Temporal)
original_source: Github
year: '2024'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/meituan/Meituan-INFORMS-TSL-Research-Challenge
- https://doi.org/10.2139/ssrn.5696423
- https://raw.githubusercontent.com/meituan/Meituan-INFORMS-TSL-Research-Challenge/main/TSL-Meituan%20challenge_background%20and%20data_20240321.pdf
v2_path: datasets/_dev/tabarena-v0pt2/meituan_food_delivery_time/dataset.py
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

CC (2026-11-08, Myunghwan): "then run [$tabarena-add-dataset] on this" (repeated after screening explanation). Proceed to add-dataset. This authorizes qualification, not final inclusion, build or commit.

**Assessment (AI, 2026-11-08):** Implements the recommended acceptance-time ETA update with total placement-to-arrival minutes, prebooked orders retained and future-day evaluation. Exact implementation details remain agent proposals for added review, not separately confirmed human constraints. Existing triage reservation preserved; claim stage is independent of suggestion. The historical screening creation/dispatch framing above is superseded for this definition.

**Assessment (AI, 2026-11-08):** review panel (full): ship after changes; disputed: forecast snapshot availability (USE-3, USE-6, LEAK-10, EV-7); for the curator: issue 1. Data has 568,545 labeled accepted orders and 17 features; three future acceptance-day windows exclude unavailable training labels. Native task probes have no flags; full-row residual models beat the platform promise and elapsed-time baselines. No confirmed exploit. Timing uncertainty remains explicit, and neither final inclusion nor warning acceptance is inferred. Priority 4: gap 0, use case + (operational ETA update), source + (documented first-party release), shape + (substantial rows and recurring categorical entities), risk - (unverified forecast snapshots and short single-city horizon).

CC (2026-11-08, Myunghwan): "Your original proposal seems the best to me (accepted at)." Keep the acceptance-time setup. "we should not include any train sample where any time is observed after the test split's accepted_at." Require all actual observed training events before the test window; do not introduce a nominated-courier counterfactual task. Forecast availability, final inclusion and warning acceptance are not decided by this instruction.

**Assessment (AI, 2026-11-08):** Check all six actual event clocks rather than infer event completion from acceptance alone. Arrival is the latest actual event in every labeled order; the existing midnight arrival filter excludes 370/407/423 unfinished orders, with zero all-event violations and no membership change. Add fail-closed assertions; reuse previous models only after exact data/type/split equality verification.

CC (2026-11-09, Myunghwan): "Yes. I agree. The forecast-free version is more reasonable and safer". Choose forecast-free independent prediction: exclude both platform forecasts from model inputs, compare externally against the recorded promise, and retain assisted-model results as sensitivity. Preserve accepted-at point, total target, prebooks and strict observed-event cutoffs. This is issue 1 change, not final inclusion, metric/warning acceptance, build or commit.

**Assessment (AI, 2026-11-09):** Consistent with objective prediction beside an existing expert/blackbox comparator (2_month_survival_rate_prediction), distinguished from Olist or LDAPS tasks that refine their supplied estimates. Affected checks, probes and focused independent review follow; old assisted qualification remains historical.

**Assessment (AI, 2026-11-09):** Applied curator issue1 choice to a 15-feature forecast-free primary. Raw forecast deletion/perturbation leaves the cleaned frame invariant. All568545 source orders, target and train/test cohorts unchanged; tie ordering changed, so qualification was rerun rather than predictions reused. Fresh leakage/raw/task/dtype/recurrence probes complete; task flagsnone. Two-seed full-row residual LightGBM RMSE8.416-9.517 minutes versus external recorded promise11.755-12.141 and elapsed-plus-mean10.680-11.494. Check0errors,1explained62unused-tailwarning,2extra conflicting-profile rows informational. Forecast timing remains unverified for the external reference; live evaluator causal query isolation unverified. Final ship, fallback metric and warning acceptance remain pending. Forecast-assisted models are historical sensitivity, not the shipped feature set.

**Assessment (AI, 2026-11-09):** review panel (focused): ship after changes; disputed: none in the selected forecast-free definition; for the curator: final inclusion, fallback RMSE in minutes and the explained62unused-tailwarning. Required claim/column/split/precedent/isolated participant/mediator reviews complete; no required definition correction or demonstrated exploit. Isolated fixed engineered remaining-time learner scores7.322/8.209/7.700 minutes on Oct24/23/22, versus elapsed-plus-mean10.680/11.494/11.014. These use different preprocessing from simple qualification and establish useful signal, not model ranking. Eight days/onecity and live evaluator future-query isolation remain limitations. Issue1 resolved with actual curator words; no human ship/metric/warning mark inferred.

**Assessment (AI, 2026-11-09):** Final focused mediator recommendation: ship after completed routine reconciliation; cold editor confirms ready for curator review, no required edits. This is an AI recommendation only. Human final inclusion, RMSEminutes and explained62tailwarning acceptance remain pending; accepted_check_warnings stays empty.

CC (2026-11-09, Myunghwan): "yes. agreed." Approve inclusion of the reviewed forecast-free 15-feature dataset and retain the 62 October 25 acceptances outside the scored windows, accepting the explained splits_rows_unused warning. This replies to all three final approvals; build, commit, push and publication are not requested.

CC (2026-11-09, Myunghwan): the declared metric, fallback RMSE in minutes, is checked and approved ("yes. agreed.").

**Assessment (AI, 2026-11-09):** Final approval is consistent with the rules and prior decisions: useful independent prediction, fallback RMSE on the original minute scale, and specifically explained unused temporal-tail rows. No exception or rule amendment. Scientific review complete; ready for an explicitly requested build. Data, target, predictors and splits unchanged. Existing ownership and WIP state remain until later integration.

**Assessment (AI, 2026-11-09):** Curator-requested build completed: UUID `01a1c240-670c-7619-accd-dcfb6e721d9c`, checksum `v2:1c8113474925271ced300ea5c8142a758859f26f0fc76c69aa8306cf3a03c594`, format2, clean definition commit3762163a. Saved reload verifies; traced-input reproduction matches; typed frame and every ordered split equal the qualified forecast-free task. Zero errors/unaccepted warnings; existing62tailwarning accepted. No scientific change or new decision. Local build/integration commits authorized, no push/publication; claim and WIP mirror preserved pending main integration.

**Assessment (AI, 2026-11-09):** Integrate the approved and verified Meituan package into existing draft PR59 at the curator's correction. DF: Yes is the accepted integration proposal; preserve actual claim/WIP mirror until main. Existing five package files and prior rejection/holds are unchanged. Original build/source commits stay reachable; no new build or model fit. Separate PR66 will be closed as superseded once integration is published.
