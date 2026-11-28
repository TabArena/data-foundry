---
unique_name: meituan_food_delivery_time
name: 'Meituan: Operational-Level On-Demand Food Delivery Data for the INFORMS TSL Data-Driven Research Challenge'
checked_by:
- Myunghwan
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Entities: Recur'
- Dated Event Log
original_source: Github
year: '2024'
collection_period: 17 Oct 2022 - 24 Oct 2022
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

**Assessment (AI, 2026-11-21):** collection facts set from the split audit: one row per order event with its own timestamps; arrival comes minutes to hours after acceptance; 4,962 merchants and 4,901 couriers recur. The period is the source's `dt` cohorts; acceptances run to 25 Oct 00:23 and some placements, mostly prebooked (199 of 213), go back to 11 Oct.

**Assessment (AI, 2026-11-21):** review panel (full re-check): ship after changes; disputed: the last-hour selection of the delivered-before-midnight filter (SPLIT-10; measured: kept orders 1.8-2.1 min faster, scores within 0.02 RMSE of all true labels, so an exception of Fugaku's kind or a 1-hour gap), the booked slot of prebooks (USE-6, EV-7), the courier's next acceptances in the test day (LEAK-9, protocol line added); for the curator: H and issues 2-4. Wording fixes applied to the definition, build 01a1c240 stale. Priority 4: gap 0 (regression and temporal are not thin), use case + (acceptance-time ETA update), source + (first-party documented release), shape + (568,545 orders, recurring couriers and merchants), risk - (two Must fixes pending in issues 2 and 3, eight days in one city).

CC (2026-11-23, Andrej): issue 2 C: "Option C: Stretch the last window to 00:23 on 25 October. Can we just keep the samples as part of the last test window, since they are perfectly valid?" The newest test window holds every acceptance from 24 October 00:00 to the end of the data, with the 62 acceptances up to 00:23 on 25 October; no row is left unscored.

CC (2026-11-23, Andrej): issue 3 B: "Option B: Minutes from acceptance to arrival." The target is `remaining_minutes`, arrival minus acceptance; `elapsed_minutes` stays an input and all prebooked orders stay. The declared metric (RMSE in minutes) now scores `remaining_minutes`.

CC (2026-11-23, Andrej): issue 4 A, as implemented: no promise on any row; `fit_reason` says prebooked orders lack their booked slot.

**Assessment (AI, 2026-11-23):** applied issues 2 C, 3 B and 4 A. Windows: 24 October to the end of the data 67,411 test / 500,764 train (88.1%), 23 October 77,719 / 423,008 (74.4%), 22 October 77,637 / 345,355 (60.7%); 568,545 rows, all used. On the new target the training mean scores 10.68 / 11.49 / 11.01 RMSE minutes and the recorded promise 12.14 / 11.79 / 11.76 (24 / 23 / 22 October). The check has 0 errors; its one warning (the newest window spans 24 hours 23 minutes, which it counts as 2 days against the 1-day horizon) is accepted as the consequence of issue 2 C. For H (open): the sources state no evaluation window, refit cadence or deployment delay; a data snapshot 1 or 3 hours before midnight moves LightGBM RMSE by -0.03 to +0.09, 6 or 12 hours by +0.24 to +0.69.

CC (2026-11-24, Andrej): H: "Agree. Implement the three hour gap." Implement option c of the answer of 2026-11-23: each training side is the data snapshot 3 hours before the test window's midnight (21:00), keeping orders accepted and delivered before it, for the time a nightly refit needs to extract its data, train with per-split tuning and roll out; the test windows stay 22, 23 and 24 October (the newest to the end of the data).

CC (2026-11-24, Andrej): the declared horizon (one day, a 3-hour gap, windows starting 24, 23 and 22 October 2022) is checked: the source states no horizon, cadence or deployment delay, a nightly refit is assumed, the gap is the deployment time of that refit, and the three newest days are the only ones above the half-the-rows floor.

CC (2026-11-24, Andrej): issue 5 B: "Option B: Accept it." `meta_time_horizon_mismatch` is accepted: the newest window keeps the 62 acceptances up to 00:23 on 25 October (issue 2 C) and spans 24 hours 23 minutes, which the check counts as 2 days.

**Assessment (AI, 2026-11-24):** applied H (3-hour gap) and issue 5 B; `split_leaf` set to L-ORDER.windows. Windows (test / train, share of 568,545 rows): 24 October to the end of the data 67,411 / 494,654 (87.0%), 23 October 77,719 / 416,321 (73.2%), 22 October 77,637 / 338,395 (59.5%); all above the half-the-rows floor. Left out of training by the gap: 5,179 / 5,768 / 5,827 orders accepted in the 3 hours and 1,301 / 1,325 / 1,556 accepted before the snapshot but undelivered at it (24 / 23 / 22 October). The kept orders of the last hour before the snapshot are 1.8-2.2 minutes faster than all of that hour, as at midnight. `dataset check`: 0 errors, 0 warnings (the horizon warning accepted), 1 info (2 conflicting duplicate rows). Leak probe: all features R^2 0.293, no exact feature copy across the split, the 62-row 25 October tail out of band in rows only (mean and median in band). Task probe: random forest RMSE 9.17 against 11.06 for the dummy, beats it on 3 of 3 splits, flags none.

CC (2026-11-24, Andrej): the declared split (three one-day windows on the acceptance time, the newest to the end of the data, training data taken 3 hours before each test day, leaf L-ORDER.windows) is checked, as implemented.

CC (2026-11-24, Andrej): verdict ship; nothing open in the review. The build is stale until rebuilt.

## Review

**Outcome:** added. Ship: the full re-check of 2026-11-21 keeps the acceptance-time ETA task, its rows, inputs and one-day windows, and nothing argues for exclusion. Andrej decided on 2026-11-23 that the newest test window runs to the end of the data (issue 2 C), that the target is the minutes from acceptance to delivery (issue 3 B) and that prebooked orders get no booked slot (issue 4 A); on 2026-11-24 a 3-hour gap between each window's training snapshot and its midnight (H) and the acceptance of the newest window's 24 hours 23 minutes (issue 5 B). Windows 22, 23 and 24 October train on 59.5%, 73.2% and 87.0% of the rows; `dataset check` gives 0 errors and 0 warnings. No row is copied across the split and every training event precedes the snapshot; the same courier's next acceptances within a test day are worth 0.65-0.70 RMSE, so the splits comment carries the protocol line against reading other test rows. Value: random forest 9.17 RMSE against 11.06 for the dummy (task probe, 2026-11-24), so the task is not trivial. Nothing open. The build 01a1c240 is stale.

**Main points:** Open: none. Settled on 2026-11-24: a 3-hour gap before each test window's midnight for the refit's extraction, tuning and rollout (H), and the newest window's longer span accepted (issue 5).


**Record judgment:** Each row is an accepted order; predict the minutes from acceptance to delivery immediately after acceptance. Known elapsed time, courier, merchant and the accepted waybill's business area, shifted coordinates, prebook flag, acceptance time and dispatch/push delays are inputs. Both platform forecasts are excluded. Three future-day windows (the newest to the end of the data) retain the same source cohorts, with every actual training event before the data snapshot 3 hours before each window's midnight (gap decided 2026-11-24); 1,556/1,325/1,301 orders (22/23/24 October) undelivered at the snapshot are excluded. Recorded-promise timing remains unverified; reading other test rows is ruled out by the protocol line, not by the data.

**Horizon:**

* **Verdict:** keep the one-day windows on 22, 23 and 24 October 2022 with the delivered-before-midnight filter and no fixed gap, as an exception to the gap rule[^x21h4] (a selection is measured but does not move the scores); high confidence on the windows, since no other three one-day windows keep half the rows for training.
* **Length:**
  - One day, cut at local midnight, which is also the assumed refit cadence.
  - The source states no horizon or refit cadence: the daily refit is our assumption.
  - An acceptance-time ETA looks minutes ahead, so the length only says how long one fitted model serves.
* **Gap:**
  - No fixed gap. Each training side keeps only orders delivered before the window's midnight, which withholds about a third of the last training hour's orders (99-100% of the withheld orders were accepted in that hour); the kept ones are faster in remaining time than all orders of that hour (minutes):

    | Cut | Orders accepted in the last hour | Withheld | Mean remaining, all | Mean remaining, kept | Shift |
    |---|---|---|---|---|---|
    | 22 Oct | 1,259 | 423 | 23.18 | 21.39 | -1.79 |
    | 23 Oct | 1,220 | 405 | 22.72 | 20.60 | -2.13 |
    | 24 Oct | 1,134 | 370 | 23.06 | 21.06 | -2.00 |

  - On scores the selection does not show: training on the filtered side scores within 0.02 RMSE of training on every earlier order with its true label, and a 1-hour gap costs 0.00 / 0.00 / +0.07 (remaining-time target, LightGBM 500 trees, mean of 2 seeds, seed spread up to 0.06):

    | Training side | 22 Oct | 23 Oct | 24 Oct |
    |---|---|---|---|
    | Filter, no gap (implemented) | 8.101 | 8.464 | 7.644 |
    | Every order before the cut with its true label (not available live) | 8.116 | 8.476 | 7.665 |
    | Filter + 1-hour gap (about the p99 delay) | 8.097 | 8.461 | 7.713 |
    | Filter + 3-hour gap | 8.143 | 8.460 | 7.725 |
    | Filter + 11-hour gap (about the longest delay) | 8.207 | 8.525 | 7.979 |

  - Arrival is the latest of the six event clocks of every order, so no training event falls after the cut.
  - The label delay is the remaining time after acceptance: p99 55-58 minutes, at most 652 minutes.
  - A one-day gap, as the NYC and Porto taxi and Lusaka trip tasks use, would leave the 22 October window training on about 48.7%; a 1-hour gap keeps all three windows.
* **Time frame:**
  - The release covers eight acceptance days, Monday 17 to Monday 24 October 2022, in one city; the windows are ours.
  - Only the last three days keep half the rows for training; Friday 21 October would train on about 48.7%[^x21h2].
  - Two of the three test days are weekend days, and the Saturday window trains on weekdays only.
  - Seasons, holidays and other cities are not tested.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One day, 22-24 Oct, filter only (implemented) | Daily midnight refit, the three newest days; training keeps orders delivered before midnight | 3: 77,637 / 77,719 / 67,349 rows; train 60.7% / 74.4% / 88.1% | meets the half-the-rows floor and the target of 3 windows; newest day included; whole daily cycles; exactly what a midnight refit knows | an exception to the gap rule (the newest training hour is about 2 minutes faster than it was); Saturday trains with no weekend day; 2 of 3 test days are weekend days |
  | B | A + 1-hour gap | As A, and training also drops orders accepted in the last hour before midnight (about the p99 delay) | 3: the same test rows; train about 0.2% smaller than A | removes the selection; applies the gap rule instead of an exception; keeps all three windows | costs up to 0.07 RMSE (24 Oct); drops labels a live refit would have |
  | C | 12 hours, newest six half-days | Refit at midnight and noon | about 6, roughly 33-40k rows each (to measure) | splits the lunch and dinner peaks; more windows | the target is already met; noisier windows; a noon refit is not in the source |
  | D | Two days | Refit every two days | 1 window above half (23-24 Oct, 145,068 rows); 21-22 Oct at about 48.7% | fewer, larger windows | fewer than 3 windows: fails the rules |
  | E | One day, 21, 23 and 24 Oct | Friday replaces Saturday | 3: about 69k / 77,719 / 67,349 rows | two weekdays and one weekend day | 21 Oct trains on about 48.7%, a curator's exception; Saturday untested |

* **Recommendation:** A, recorded as an exception to the gap rule: the selection is measured, and training on the filtered side scores within 0.02 of training on every true label, as for the Fugaku supercomputer job-failure dataset[^x21h5]; B is the choice if the letter of the gap rule weighs more than 0.07 RMSE on one day. The windows are the only three above the floor, with the newest day[^x21h1][^x21h3]. **Decision:** keep A, add a 1-hour gap (B), or change to C or E?

**Notes for the AI:** Applied already (no decision): the splits comment names the leaf (L-ORDER.windows: windows on the acceptance time, the gap by the late-label gap rule; until 2026-11-24 named "Temporal, arrival date, label-delay gap"), says the source is silent on horizon and cadence and that the floor fixed the windows, gives the training shares 60.7/74.4/88.1% with 21 October at about 48.7%, the count 3 against SPLIT-33's 3, and the filter's measured selection and score effect. On A, add a curation bullet "Exception to SPLIT-10 (<date>, <curator>): no fixed gap; the delivered-before-midnight filter is the exact as-of knowledge of a midnight refit; it withholds about a third of the last training hour (kept orders 1.8-2.1 minutes faster), and training on it scores within 0.02 RMSE of training on all true labels", with a CC line (no gap is a person's exception), citing fugaku_hpc_job_failure (2026-11-03, Myunghwan) as precedent and the one-day gaps of nyc_taxi_trip_duration, pkdd_15_taxi_trip_time_prediction_ii and 2024_lusaka_mobility_prediction_hackathon as the contrast (date-level windows; here a one-day gap leaves 48.7%). On B, in `_make_splits` add `train = train[(df["accepted_at"].iloc[train] < start - pd.Timedelta(hours=1)).to_numpy()]` before the delivered-before-start filter and the assertions; replace the gap sentences of the splits comment with the 1-hour gap and its cost; run `dataset check`. On C, build the six half-day windows in `_make_splits` (cuts at midnight and noon; `TemporalSplits` has no hour windows and `Temporal` no hour horizon, so the horizon is declared as 1 day or left to the curator), keep the delivered-before-cut filter at each cut, run `dataset check`. On E, set the cutoffs to 21, 23 and 24 October, lower the `len(train) >= len(df) / 2` assertion to 30%, and accept `splits_train_under_half` only after the curator's CC line. Evidence: the mediator's run folder (`sel.py` and its log).

[^x21h1]: **SPLIT-12** (Should): the horizon, the refit cadence, the gap and the time unit come from the use case and the source; the splits comment names each, or says the source is silent and what is assumed; the curator signs off the horizon of every new temporal dataset.
[^x21h2]: **SPLIT-14** (Must): at least three windows, each training on at least half the rows (down to 30% only as the curator's exception), each test window with at least 33 scored units.
[^x21h3]: **SPLIT-15** (Must for the newest window, Should for the others): the newest window is always tested; the count aims at SPLIT-33's count for two thirds of the scored units (here 3); walking back from the newest needs its reason.
[^x21h4]: **SPLIT-10** (Should): train only on rows whose outcome is known by the window's start, with a gap of about the label's delay; no gap only where the measurements show neither a shortcut through recent labels nor a selection by the outcome, and a departure otherwise is an exception.
[^x21h5]: fugaku_hpc_job_failure: no fixed gap after exact completion filtering, fast-completer selection measured (2026-11-03, Myunghwan), exception.

**Andrej (2026-11-23, discuss):** "Did the source make any decisions on that?

Otherwise, no gap at all is unrealistic. What would be the most realistic setting here, given that we also have optimization time for model hyperparameter tuning per split."

**Answer (AI, 2026-11-23):** How long before midnight should the refit's data snapshot be taken?

* **What the source says:**
  - The challenge background (March 2024), the October 2024 supplement and Wang et al. (2025) set no evaluation windows, no train/test protocol, no refit cadence and no model training or deployment delay; they define no predictive benchmark at all (Sample Question 4 only asks for models of pick-up and delivery timings).
  - The only latencies they give are operational: dispatch runs in batches every 30 seconds or 1 minute, and an assignment must be decided within about 10 seconds (background, Challenges 1). These bound the time to score one order, not the time to retrain a model.
  - The release is delivered in daily `dt` cohorts, which fits a daily batch pipeline, but the source does not say how its own forecasts are refreshed. The midnight refit stays our assumption.
* **Problem:**
  - A refit at the cut cannot serve at the cut: the data must be extracted, the model trained and tuned (a benchmark method tunes its hyperparameters on every split), checked and rolled out. The realistic gap is the time from the last training data to deployment, not only the label delay (p99 55-58 minutes).
  - A gap only drops training rows: the snapshot moves to midnight minus the gap, training keeps orders accepted and delivered before the snapshot (the filter stays, applied at the snapshot), and the test windows stay the same local days (24 October now to 00:23 on 25 October).
* **Experiments:** LightGBM (500 trees, 127 leaves) on the remaining-time target and the 15 inputs, the definition's windows after issues 2 C and 3 B, mean of 2 seeds (spread up to 0.06, 0.15 for 12 hours on 22 October); RMSE in minutes, lower is better:

  | Gap (snapshot) | 22 Oct train | 22 Oct RMSE | 23 Oct train | 23 Oct RMSE | 24 Oct train | 24 Oct RMSE | Change against no gap |
  |---|---|---|---|---|---|---|---|
  | 0 h (midnight, implemented) | 345,355 (60.7%) | 8.118 | 423,008 (74.4%) | 8.482 | 500,764 (88.1%) | 7.655 | - |
  | 1 h (23:00) | 343,929 (60.5%) | 8.108 | 421,530 (74.1%) | 8.487 | 499,473 (87.9%) | 7.626 | -0.03 to +0.01 |
  | 3 h (21:00) | 338,395 (59.5%) | 8.138 | 416,322 (73.2%) | 8.572 | 494,654 (87.0%) | 7.694 | +0.02 to +0.09 |
  | 6 h (18:00) | 317,187 (55.8%) | 8.514 | 394,931 (69.5%) | 8.935 | 473,767 (83.3%) | 7.891 | +0.24 to +0.45 |
  | 12 h (12:00) | 289,365 (50.9%) | 8.807 | 362,696 (63.8%) | 9.121 | 440,620 (77.5%) | 8.102 | +0.45 to +0.69 |

  - The cost jumps between 3 and 6 hours, when the snapshot moves before the previous day's evening peak; that this is the cause is likely, not tested. Every gap keeps all three windows above the half-the-rows floor[^x23h1].
  - A deployment gap does not remove the last-hour selection of the filter: it moves it to the snapshot (measured at midnight on 2026-11-21: within 0.02 RMSE).
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | No gap (implemented) | Snapshot at midnight; the model serves the moment its data ends | best scores; the exact as-of knowledge at midnight | a refit with tuning cannot serve at the cut; an exception to the gap rule[^x23h2] |
  | b | 1-hour gap | Snapshot at 23:00 | about the label delay's p99; costs nothing measurable | leaves about an hour to train, tune and roll out |
  | c | 3-hour gap | Snapshot at 21:00, after the evening peak | room for extraction, tuning and rollout of a nightly refit; costs at most 0.09 RMSE; trains on 59.5-87.0% | an assumed pipeline length; the source gives none |
  | d | 6-hour gap | Snapshot at 18:00 | room for a long tuning run | loses the previous evening's peak; costs 0.24-0.45 RMSE |
  | e | 12-hour gap | Snapshot at noon | a full afternoon for tuning | costs 0.45-0.69 RMSE; 22 October trains on 50.9%, near the floor |

* **Recommendation:** c: a nightly refit that tunes per split needs hours between its data and serving, and 21:00 is the latest snapshot after the evening peak; it costs at most 0.09 RMSE and keeps all three windows. b if the curator holds that training and tuning fit in an hour. **Decision:** keep a, or change to b, c, d or e?

**Notes for the AI:** On b to e, in `_make_splits` set `snapshot = start - pd.Timedelta(hours=<gap>)` and keep training rows with `accepted_at < snapshot` and `delivered_at < snapshot` (the assertions compare with the snapshot), declare the gap on `Temporal` (`gap=<gap>, gap_unit="hours"`), apply the same snapshot in `_decisions`, replace the gap sentences of the splits comment with the chosen gap, its reason (deployment time: extraction, training with tuning, rollout) and its measured cost, and run `dataset check`. Evidence: the run folder (`run.py`, the log of 2026-11-23).

[^x23h1]: **SPLIT-14** (Must): at least three windows, each training on at least half the rows (down to 30% only as the curator's exception).
[^x23h2]: **SPLIT-10** (Should): train only on rows whose outcome is known by the window's start, with a gap of about the label's delay; no gap only where the measurements show neither a shortcut through recent labels nor a selection by the outcome, and a departure otherwise is an exception.

**Answer (AI, 2026-11-24):** What the split rules of 2026-11-24 change for H: the windows and the options stay; the decision is now named as one a person makes.

* **Leaf:** the split tree now starts from the record's collection type. A dated event log whose model meets orders after the data, with a recorded acceptance time and three one-day windows, reaches the leaf "Temporal · windows on the time key" [L-ORDER.windows], with the gap set by the gap rules[^x24h1]. The former leaf "arrival date, label-delay gap" is merged into it; the splits comment now names the leaf by its ID. No change to the windows.
* **Gap rules:**
  - For late labels the tree allows "a gap of about the delay, or training only on cases whose outcome is known before the window", with a delivery as its example. The delivered-before-midnight filter is that second form.
  - The gap rule itself is unchanged: it still asks for a gap where a measurement shows a selection by the outcome at the end of the training data[^x23h2]. That selection is measured here (the kept orders of the last hour are 1.8-2.1 minutes faster), so option a stays an exception.
  - New: "no gap" is one of five questions only a person answers. Until a person answers it, the agent answers no.
* **The gap the source does not give:** this is the second person-only question. The agent proposes a gap and the curator signs it off[^x24h2]. The answer of 2026-11-23 is that proposal (c).
  - The deployment time is neither a label delay nor a planning lead the source states, so it enters the task only through this sign-off.
  - b covers the label delay (p99 55-58 minutes). c to e add time for extraction, tuning and rollout.
* **Window size:** the window check now counts a scored unit by its rows wherever a window cuts it across training and test. This task scores rows (RMSE, no group), so the counts are unchanged:

  | | 22 Oct | 23 Oct | 24 Oct |
  |---|---|---|---|
  | Test rows (each needs at least 33) | 77,637 | 77,719 | 67,411 |
  | Training share at no gap (floor 50%) | 60.7% | 74.4% | 88.1% |

  - The target is 3 windows for 568,545 rows, and 3 are reached. Every gap in the table of 2026-11-23 keeps all three windows above the floor.
* **Checks (2026-11-24):** `dataset check` reports 0 errors, the one warning of issue 5 and one info line. The record and definition are consistent. The leaf fits the shipped temporal split.
* **Recommendation:** unchanged: c; b if the curator holds that training and tuning fit in an hour. Under the new tree, a (no gap) needs the curator's explicit exception and a CC line. **Decision:** keep a as a person's exception, or change to b, c, d or e?

**Notes for the AI:** As in the answer of 2026-11-23. With `_make_splits` the gap is declared on `Temporal(on="accepted_at", horizon=1, horizon_unit="days", gap=<hours>, gap_unit="hours")` (accepted, resolves to the hour gap). On a, add the exception bullet and CC line of the Horizon notes, and name it the "no gap" exception at [L-ORDER.windows]. With the decision, set `split_leaf = "L-ORDER.windows"` (cross-dataset item, Andrej 2026-11-24: every definition names its leaf with its split decision): the placement check finds nothing for it (no v0.2 definition sets it yet).

[^x24h1]: **SPLIT-36** (Should): a definition's split is decided by walking the split tree from the record's collection type; the leaf names the split, and for a temporal split the windows and the gap.
[^x24h2]: **SPLIT-12** (Should): the horizon, the refit cadence, the planning gap and the label delay, and the time unit come from the use case and the source; the splits comment names each or says the source is silent; the curator signs off on the horizon and the test windows of every new temporal dataset.

**Andrej (2026-11-24, discuss):** "Agree. Implement the three hour gap."

**Resolved (2026-11-24, Andrej):** Implement c, a 3-hour gap. `_make_splits` builds each training side at the data snapshot 3 hours before the window's midnight (`GAP`): orders accepted and delivered before 21:00 of the previous day; the assertions compare with the snapshot. `Temporal` declares `gap=3, gap_unit="hours"`, `split_leaf = "L-ORDER.windows"`, and `_decisions` applies the same snapshot. The splits comment states the gap, its reason (extraction, training with per-split tuning, rollout; the source states none) and its measured cost (+0.02 to +0.09 RMSE); the split-walk bullet, the curation bullet on the windows and the task summary say the same. Training 338,395 / 416,321 / 494,654 rows (59.5% / 73.2% / 87.0%) for 22 / 23 / 24 October, test rows unchanged (77,637 / 77,719 / 67,411). `dataset check`: 0 errors, 0 warnings, 1 info; the gap brings no new warning. Leak and task probes after the change: no flag (task probe: random forest 9.17 RMSE against 11.06 for the dummy).

**Issues for Myunghwan:**

1. **Retain forecasts whose exact recording time is unverified?**

   - **Problem:** The source identifies a promised arrival and predicted meal readiness, but does not provide issuance or revision timestamps proving that the accepted row stores the versions available at courier acceptance.[^timing]
   - **Background:** This is an ETA update immediately after acceptance, using the accepted courier, merchant and known elapsed time; later pickup and delivery events are excluded from predictors.
   - **Effect on the task:** If a stored forecast was revised after acceptance, the model would receive information unavailable during a real ETA update.
   - **Experiments:** Meal-ready forecasts vary across attempts for 8,794 orders while the promise is constant per order, establishing revisions but no demonstrated post-acceptance revision. Models predicting remaining delivery time, then adding known elapsed time, achieve root mean squared errors of 7.16-7.93 minutes across three future days and two seeds, versus 8.40-9.53 minutes without both forecasts; useful prediction survives removal, but these scores cannot establish when the stored versions became available.
   - **Consistency:** A platform's own timely estimate belongs in the inputs, as in the Olist delivery task; that precedent does not prove this release's snapshot timing.[^promise]
   - **Panel:** Advocate, critic and mediator agree that no leak is demonstrated, the short summary must disclose the uncertainty, and the decision to retain the forecasts under that assumption remains human.
   - **Unknown:** Issuance/version history or an authoritative account of the accepted-row snapshots would settle the factual question; another predictive ablation cannot.
   - **Sources:** [Official source](https://github.com/meituan/Meituan-INFORMS-TSL-Research-Challenge), 2025 paper section 3.1 and October 2024 supplement section 2.5.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Retain with explicit uncertainty (implemented) | Keep both accepted-attempt forecasts and the stated availability assumption | Preserves the source-described ETA inputs | Snapshot timing remains unverified |
     | B | Qualify an alternative | Require logging evidence or request a variant without the unresolved fields before acceptance | Avoids accepting the current timing assumption | Requires scoped follow-through before a final ship decision |

   - **Recommendation:** A, with the uncertainty prominent, because source-supported forecast meaning and the current tests establish no late-information mechanism; if later evidence demonstrates unavailable values, repair or remove them rather than treating this choice as permission to retain leakage. **Decision:** Accept the implemented retention assumption, or require further evidence or alternative qualification?

   **Notes for the AI:** Issue 1 concerns uncertainty, not an exception to a demonstrated leak. Preserve total placement-to-arrival minutes, all prebooks, the three explicit future-day windows and label-maturity guards. An alternative changes the feature set and requires affected checks/probes and focused independent review; the completed combined ablation is sensitivity evidence, not a silently substituted dataset. Keep accepted_check_warnings empty until actual curator input: the one explained warning is 62 retained October 25 tail rows outside the complete-day windows. Retain closed issue numbers and actual human words when applying review.

   [^timing]: USE-3 and USE-6 (Must), LEAK-10 (Must), EV-2 and EV-7 (Must): meaning and predictive sensitivity do not establish availability, and cannot-verify must remain explicit.
   [^promise]: USE-6 (Must), brazilian_ecommerce precedent; USE-12 favors repairing unavailable inputs while retaining the real task if new evidence establishes a problem.

   **Myunghwan (2026-11-09, change):** "Yes. I agree. The forecast-free version is more reasonable and safer".

   **Resolved (2026-11-09, Myunghwan):** Option B selected and qualified: independent ETA prediction excludes both platform forecasts, their derivatives and missingness; the recorded promise is an external reference only, and prior forecast-assisted models remain sensitivity evidence. Acceptance-time prediction, total placement-to-arrival target, all prebooks and strict observed-event cutoffs remain. Fresh checks and three-day, two-seed models support the revised 15-feature definition. This resolves the feature choice, without final inclusion, metric or warning acceptance.

2. **Drop the 62 acceptances after midnight on 25 October, now that the newest window must be tested?**

   - **Problem:**
     - Under the split rules the definition stops with an error, because the 62 acceptances on 25 October lie after the last test window.
     - Myunghwan approved keeping these rows unscored on 9 November, before that requirement existed.
   - **Effect on the task:** the dataset cannot be checked or built until the 62 rows leave or get a window of their own.
   - **Experiments:** the 62 rows are accepted between 00:00 and 00:23 on 25 October, all from the 24 October cohort; a window of their own would hold 62 rows against 67,349-77,719 in each full day. `TemporalSplits(...).splits` raises: "The newest cutoff's window ends at 2022-10-25 00:00:00, before the newest data (2022-10-25 00:23:29)". With B applied, `dataset check` (2026-11-21) gives 0 errors and 0 warnings; of its two infos, the unused accepted warning goes when the notes below remove it, and the other (2 rows with equal inputs and different targets) stays.
   - **Consistency:** the newest window is always a test window[^x21colA]; B follows the cross-dataset ruling that dropped a short tail after the last full period (coffee ratings, Kickstarter), and C follows the Lusaka trips, which keep a short last day inside their last window, though there the window ends where the data ends[^x21colB].
   - **Panel:** the column audit (2026-11-21) found no other use for these rows; they are ordinary late-evening orders.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the 62 rows outside the windows (implemented) | As approved on 9 November | no rows lost | fails the newest-window requirement; the definition does not run |
     | B | Drop acceptances after 24 October | Filter acceptances before 25 October 00:00 local in `_clean`; the newest window is 24 October | runs; whole local days only; loses 0.01% of rows | changes an approved row choice |
     | C | Stretch the last window to 00:23 on 25 October | The newest test window holds 24 October plus the tail | keeps every row | the newest test window is 24 hours 23 minutes long, unlike the other two |

   - **Recommendation:** B: 62 rows of a cohort's tail, and every test day stays a whole local day. **Decision:** keep A, or change to B or C?

   **Notes for the AI:** On B, add `df = df.loc[pd.to_datetime(df["grab_time"], unit="s") + pd.Timedelta(hours=8) < pd.Timestamp("2022-10-25")]` before the assertions in `_clean`, then remove `accepted_check_warnings`, the 62-row sentence in `task_summary.row` and the last sentence of the splits bullet in `curation_comments`; update the counts of the decision "One labeled accepted waybill per order", run `dataset check`, add a CHANGELOG entry. Evidence: the run folder; the check with B applied: the run folder.

   [^x21colA]: **SPLIT-15** (Must for the newest window): the newest window is always a test window, because it is the deployment period.
   [^x21colB]: Cross-dataset ruling of 2026-11-11 (Lennart): coffee_rating_prediction drops its 2 reviews of October 2023, as kickstarter cuts its last 60 days; 2024_lusaka keeps a 70-row partial last day inside its last window (RMSE moves by 0.002).

   **Andrej (2026-11-23, change):** "Option C: Stretch the last window to 00:23 on 25 October.
   Can we just keep the samples as part of the last test window, since they are perfectly valid?"

   **Resolved (2026-11-23, Andrej):** C. `_make_splits` builds the three windows by hand (`TemporalSplits` cannot end the newest window past a whole day): the newest holds every acceptance from 24 October 00:00 to the end of the data (00:23 on 25 October), 67,411 test rows including the 62, against 500,764 training rows (88.1%); 23 October 77,719 / 423,008 (74.4%); 22 October 77,637 / 345,355 (60.7%). The delivered-before-midnight filter stays on each training side (370/407/423 left out). The `splits_rows_unused` acceptance and every text about 62 unscored rows are gone; `task_summary.split`, the splits bullet of `curation_comments` and the splits comment say the newest window runs to the end of the data. `dataset check`: 0 errors, no newest-window error, no unused-rows warning; one warning, `meta_time_horizon_mismatch` (the check counts the 24-hour-23-minute window as 2 days against the 1-day horizon), left open for the curator (issue 5); the info on 2 rows with equal inputs and different targets stays.

3. **Predict the minutes remaining after acceptance instead of the total since placement?**

   - **Problem:**
     - The target adds the elapsed minutes, already known at acceptance and an input, to the unknown remaining time, so 98% of the target's variance is a known input.
     - A model fitted directly on this target scores 43-69 minutes RMSE against 10.7-11.5 for elapsed plus a training mean, and 96-98% of its squared error falls on the 4% of prebook rows.
     - The total target was the AI's proposal; Myunghwan's quoted words fix only the prediction point ("accepted at").
   - **Effect on the task:** the ranking would reward methods that extrapolate the known elapsed time on prebook orders (elapsed up to 10,293 minutes), not those that predict the delivery after acceptance, which is what the ETA update acts on.
   - **Experiments:** LightGBM (500 trees, 127 leaves, one seed) on the 15 shipped inputs, the definition's three windows with the 62 tail rows kept, RMSE in minutes (lower is better); the two-seed runs of the Horizon block give 7.6-8.5 for the remaining-time fit:

     | Test day | Total target, fitted directly | Remaining time + elapsed | Elapsed + training mean remaining | Share of squared error on prebooks (direct) | Direct, non-prebook rows | Remaining + elapsed, non-prebook rows |
     |---|---|---|---|---|---|---|
     | 22 Oct | 68.99 | 8.33 | 11.01 | 98.3% | 9.23 | 7.96 |
     | 23 Oct | 42.86 | 8.70 | 11.49 | 96.0% | 8.67 | 8.43 |
     | 24 Oct | 57.84 | 7.73 | 10.68 | 98.3% | 7.75 | 7.55 |
   - **Consistency:** the target should be what the actor acts on[^x21colC]; every other delivery and trip-time task counts from its prediction point (Sendy deliveries from pickup, the NYC and Porto taxis and the Lusaka trips from trip start, the Olist orders from purchase); the one exception, the medical-facility delay, is the source's own target, while here the total was the AI's proposal.
   - **Panel:** the advocate, critic, mediator and precedent checker all back B; earlier rounds only ran models that predict the remaining time and add the elapsed minutes, so a direct fit on the total was first measured on 2026-11-21.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Total minutes since placement (implemented) | The current target, with elapsed as an input | the question as written; nothing changes | the score is dominated by extrapolating a known input on prebooks |
     | B | Minutes from acceptance to arrival | Target = arrival minus acceptance; elapsed stays an input | the unknown part only; the same ETA for the customer | changes the question wording and the record's comparisons |
     | C | Total target, prebooks dropped | Removes 22,181 rows | removes most of the extrapolation | loses a real order type; the prebook decision was made on purpose |

   - **Recommendation:** B: the same information for the ETA, and a score that measures the delivery rather than the addition of a known number. **Decision:** keep A, or change to B or C?

   **Notes for the AI:** On B, set `result[self.target] = (df["arrive_time"] - df["grab_time"]) / 60` and rename the target to `remaining_minutes`; rewrite `question` and `predicted` ("Minutes from courier acceptance to delivery") and the first curation bullet; in `_decisions`, set `remaining = df[self.target]`, make the baseline the training mean of the target (drop "elapsed plus"), and rename that column; the promise RMSE is unchanged (raw arrival minus promise); keep `elapsed_minutes` and all prebooks; run `dataset check` and the task probes; add a CHANGELOG entry. The metric stays RMSE in minutes: a prediction's error on the remaining time equals its error on the total, so the metric CC line only needs the target's new name.

   [^x21colC]: **USE-5** (Must): predict what the actor acts on, at the resolution they act on it; a target the source defined badly can often be redefined into the real one.

   **Andrej (2026-11-23, change):** "Option B: Minutes from acceptance to arrival."

   **Resolved (2026-11-23, Andrej):** B. The target is `remaining_minutes` = (arrive_time − grab_time) / 60; `elapsed_minutes` stays an input and all 22,181 prebooked orders stay. `question` ("How many minutes after courier acceptance ...") and `predicted` ("Minutes from courier acceptance to delivery.") are rewritten, `changes` names the redefinition, the first curation bullet and the prebook bullet say the elapsed time is an input, not part of the target. In `_decisions` the baseline is the training side's mean of the target, measured again: 10.68 / 11.49 / 11.01 RMSE minutes on 24 / 23 / 22 October (equal to the former elapsed plus mean remaining, as it must be), the recorded promise 12.14 / 11.79 / 11.76 (24 October now with the 62 tail rows). The metric stays RMSE in minutes; its CC line names `remaining_minutes`. `dataset check` as in issue 2; task probes (3 of 3 windows, default models) flag nothing: random forest 9.04 RMSE against 11.06 for the dummy, ahead on 3 of 3 windows.

4. **Give prebooked orders their booked delivery time as an input?**

   - **Problem:**
     - On prebooked orders (3.9% of rows) `estimate_arrived_time` is very likely the slot the customer booked at checkout, known at placement, not a platform forecast.
     - Issue 1 dropped the field from every row as a forecast with unverified snapshot timing; it never separated a booked slot from a forecast.
     - That the field holds the booked slot is inferred from the data; the source does not say so.
   - **Effect on the task:** a model on prebooks misses the customer's own requested time; the requested time alone beats the shipped model on prebooks by about 0.75 minutes RMSE, and a model given both was not run.
   - **Experiments:** on prebooks (domain practitioner; column audit):

     | Measure | Value |
     |---|---|
     | Correlation of promise − acceptance with the remaining time | 0.854 |
     | RMSE of the bare promise as the prediction | 9.75 min |
     | RMSE of the model on the shipped inputs | about 10.5 min |
     | Orders whose promise varies across their waybills | 0 |

   - **Consistency:** a customer's request known at the prediction point is a legitimate input[^x21m1]; a meaning the source does not document stays cannot-verify[^x21m2]. Issue 1 stays resolved: this item asks only about the prebooked rows.
   - **Panel:** the critic asks for a decision item (the booked slot is a legitimate input); the advocate holds that the meaning is inferred, that option B partly reopens issue 1 and that the gain is small; the mediator ranks it last.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the exclusion (implemented) | No promise on any row; `fit_reason` says prebooked orders lack their booked slot | issue 1 as decided; no inferred meaning in the inputs | prebooks miss a request the customer made at placement |
     | B | Booked slot for prebooks only | Add `booked_minutes_after_acceptance` = promise − acceptance for `is_prebook = 1`, missing elsewhere | a known customer request enters; the bare value beats the shipped model on prebooks | rests on an inferred meaning; partly reopens issue 1; affects 3.9% of rows |

   - **Recommendation:** A: the booked-slot meaning is inferred, not documented, and it touches 3.9% of rows; B if documentation shows the field is the booked slot on prebooks. **Decision:** keep A, or change to B?

   **Notes for the AI:** A is applied (the `fit_reason` sentence on the booked slot). On B, in `_clean` add `result["booked_minutes_after_acceptance"] = ((df["estimate_arrived_time"] - df["grab_time"]) / 60).where(df["is_prebook"].eq(1))`; rewrite `known` ("for prebooked orders, the booked delivery slot") and the issue 1 bullet of `curation_comments` (the promise stays out for non-prebooks); remove the `fit_reason` sentence; run `dataset check`, the leak and task probes; add a CHANGELOG entry. Evidence: the run folder.

   [^x21m1]: **USE-6** (Must): anything known at the prediction point is a legitimate input, including a number the company itself computed.
   [^x21m2]: **EV-7** (Must): never claim a check you did not run; cannot-verify is never upgraded to pass and goes to the curator.

   **Andrej (2026-11-23, ok):** As implemented (A).

   **Resolved (2026-11-23, Andrej):** A: no promise on any row; the `fit_reason` sentence on the missing booked slot of prebooked orders stays. No change to `dataset.py`.

5. **Accept the check warning that the newest test window is longer than one day?**

   - **Problem:**
     - After issue 2 C, the newest test window runs from 24 October 00:00 to the end of the data at 00:23 on 25 October (67,411 rows), so `dataset check` warns that the window is longer than the declared one-day horizon (it counts the span as 2 days).
     - The other two windows are whole local days; nothing else in the check is open (0 errors).
   - **Effect on the task:** none on rows or scores: the warning only says the newest window is 23 minutes longer than a day.
   - **Consistency:** a warning stays open until the curator accepts it with a reason; 2024_lusaka_mobility_prediction_hackathon keeps a partial last day in its final window the same way[^x23m5].
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave the warning open (implemented) | `accepted_check_warnings` stays empty | nothing accepted without a decision | the check keeps reporting a warning |
     | B | Accept it | Add `meta_time_horizon_mismatch` to `accepted_check_warnings` with the reason (issue 2 C, the 62 rows to 00:23) | the check is clean; the reason is written down | none beyond the 23 minutes already decided |

   - **Recommendation:** B: the longer window is the direct result of issue 2 C, and the reason can be stated in one line. **Decision:** leave it open (A), or accept it (B)?

   **Notes for the AI:** On B, set `accepted_check_warnings = {"meta_time_horizon_mismatch": "Andrej (<date>, issue 5 B): the newest test window keeps the 62 acceptances up to 00:23 on 25 October (issue 2 C), so it runs 24 hours 23 minutes (67,411 rows); the check counts its span as 2 days against the 1-day horizon. The other two windows are whole local days."}` and add a CC line.

   [^x23m5]: The definition rules: a warning is accepted only with the curator's dated reason.

   **Answer (AI, 2026-11-24):** The split rules of 2026-11-24 leave this item as it stands. `dataset check` on the new rules still reports exactly this warning: the newest window spans 24 hours 23 minutes, which the check counts as 2 days against the 1-day horizon. The new count by rows changes nothing here. A gap chosen under H would move only the training sides, so the warning remains whatever H decides. The recommendation stays B, with the reason given in the notes. **Decision:** leave it open (A), or accept it (B)?

   **Andrej (2026-11-24, change):** "Option B: Accept it."

   **Resolved (2026-11-24, Andrej):** B: `accepted_check_warnings` holds `meta_time_horizon_mismatch` with the reason of the notes (issue 2 C, the 62 acceptances up to 00:23 on 25 October, 24 hours 23 minutes, 67,411 rows) and the curator's date. `dataset check`: 0 errors, 0 warnings, 1 info (2 conflicting duplicate rows), with the 3-hour gap of H applied.

**Review panel:** ship after changes (mediator, 2026-11-21, full re-check). Applied without a decision: the note on the courier's next acceptances in the test day (kept on purpose) and the rule that a test order is predicted without other test rows (same courier's next acceptances, 0.65-0.70 RMSE), the splits comment (source silent on horizon and cadence, the floor fixed the windows, the filter's measured selection), the 9 long non-prebook orders note, the business-area, structural-zero, dt and metric wording, the fit_reason sentence on prebooks' booked slot, the collection-facts Assessment (199 of 213 early placements prebooked). Disputed and settled: the last-hour selection is real (kept orders 1.8-2.1 min faster) but changes no score by more than 0.02 (H revised: a 1-hour-gap option added, the gap footnote corrected); the advocate's figure for the meal-ready estimate (0.63-0.76 RMSE) does not hold, since it was measured only together with the promise; the booked slot of prebooks becomes its own item. For the curator: H and issues 2-4. Earlier panels (2026-11-08, 2026-11-09): ship (focused mediator); Myunghwan approved final inclusion, the declared metric and the unused-tail warning on November 9, 2026; issue 2 reopens the tail warning, since the rule changed the next day. Those earlier panels found no required correction; this round found two (issues 2 and 3) and the courier exploit (now a protocol line). Issue 1 stays resolved. The original full panel and boundary reports below are historical: their 17-feature counts, forecast-retention question and positional evidence reuse do not describe the revised primary.

<details><summary>Mediator (2026-11-21)</summary>

**Mediator: meituan_food_delivery_time (meituan), 2026-11-21**

Read: the advocate's and critic's openings and rebuttals, the claim, domain, precedent, blind and gamer reports, the
column audit, `check.log`, `check_patched.log`, `leak.log`, `task.log`, the record's `## Review` (Horizon block,
issues 1-3), `dataset.py`, SPLIT-10 in `splits.md` and `split_tree.md`. **`group.log` is missing**; no point depends
on it (entities recur by design under a forward split, claim 15).

Decisive experiment: one run, script and log in the run folder
(`sel.py`, `1401963.log`). Issue 2 B applied (62 rows dropped), remaining-time target (issue 3 B), the 15 inputs,
LightGBM 500 trees / 127 leaves, two seeds, the definition's three windows.

**Recommendation (judgment record)**

**Ship after changes.** Validity: two Musts fail as merged and each has a one-rung fix (SPLIT-15: issue 2 B; USE-5:
issue 3 B); LEAK-9 needs a protocol line; LEAK-10 holds (no row copy across the split, every training event before
the cut). Value: a real signal, LightGBM 7.6-8.5 min against 10.7-11.5 for elapsed plus the training mean; not Trivial.
Quality: doc fixes, one new low-ranked decision (booked slot of prebooks), the Horizon sign-off. Both sides reach the
same verdict; nothing argues for exclusion.

**Settled disputes**

**Is the last-hour comparison a measured selection effect? (critic point 5 / advocate rebuttal point 5)**

**Settled: the advocate is right about the gamer's numbers, the critic is right that a selection exists. It is now
measured, and it has no measurable effect on scores.**

- The gamer's comparison (last training hour against the same hour a day earlier) is confounded by day: on the
  remaining target, the same hours a day earlier vary by up to 0.9 min from day to day. It is not the measurement.
- The direct measurement compares, within the same hour before each cut, all orders against the ones the filter keeps:

  | Cut | Orders accepted in the last hour | Withheld | Mean remaining, all | Mean remaining, kept | Shift |
  |---|---|---|---|---|---|
  | 22 Oct | 1,259 | 423 | 23.18 | 21.39 | -1.79 |
  | 23 Oct | 1,220 | 405 | 22.72 | 20.60 | -2.13 |
  | 24 Oct | 1,134 | 370 | 23.06 | 21.06 | -2.00 |

  Over the last 2 hours the shift is -0.57 to -0.69 min; over 6 hours about 0. 99-100% of withheld orders were
  accepted in the last hour. So the newest training hour is about 2 minutes faster than it really was: SPLIT-10's
  "newest training rows are the fast ones", in one hour of each training side.
- Its effect on scores, test RMSE on the remaining target (mean of 2 seeds; seed spread 0.00-0.03, up to 0.06 at 3 h):

  | Training side | 22 Oct | 23 Oct | 24 Oct |
  |---|---|---|---|
  | filter, no gap (shipped) | 8.101 | 8.464 | 7.644 |
  | oracle: every order before the cut with its true label (not available live) | 8.116 | 8.476 | 7.665 |
  | filter + 1-hour gap (about the p99 delay) | 8.097 | 8.461 | 7.713 |
  | filter + 3-hour gap | 8.143 | 8.460 | 7.725 |
  | filter + 11-hour gap (about the maximum delay) | 8.207 | 8.525 | 7.979 |

  The filter scores like the oracle (within 0.02, slightly better), so the selection does not bias the model
  measurably. A 1-hour gap removes the selection and costs 0.00 / 0.00 / +0.07 (24 Oct: what the newest hour's
  labels add). Mean test residuals move by at most 0.27 min between filter and oracle.
- **What the splits comment should say:** the filter withholds about a third of the last hour's orders, the kept ones
  are 1.8-2.1 min faster, and the filter scores within 0.02 RMSE of training on all true labels; a 1-hour gap costs up
  to 0.07. The excluded share (0.07-0.12%) alone understates the selection: the critic's point holds on substance.

**Wording of footnote [^x21h4] (SPLIT-10)**

**Settled for the precedent checker.** `splits.md` SPLIT-10 reads "train on the rows whose outcome is known by the
window's start, **with** a gap of about the label's delay"; the 2026-11-05 amendment allows no gap only where the
measurements show neither a shortcut through recent labels nor a selection by the outcome; where the needed gap breaks
a floor, the departure is an exception. "Gap or filter" is not the rule. The paraphrase comes from `split_tree.md`
(lines 59-60 and 347-348: "a gap of about the delay, or training only on cases whose outcome is known before the
window"), which contradicts `splits.md` (see the cross item below).

Proposed footnote: "SPLIT-10: train only on rows whose outcome is known by the window's start, with a gap of about the
label's delay; no gap only where the measurements show neither a shortcut through recent labels nor a selection by the
outcome, and a departure otherwise is an exception."

Under that wording the shipped design (filter, no gap) is an **exception**, since a selection is measured, of
fugaku_hpc_job_failure's kind (exact completion timestamps, filter only, fast-completer selection measured; 2026-11-03,
Myunghwan). It is not forced by the floor: a 1-hour gap keeps all three windows (training shares fall by 0.2%), so the
Horizon block's and precedent F3's "a gap would cost a window" holds only for a one-day gap. Whether the filter alone
is enough is a weighing (the filter is the exact as-of knowledge of a midnight refit, P4; the letter of SPLIT-10 asks
for a gap once selection is shown), so it goes to the curator as part of H.

**Smaller disputes**

| Point | Settled | Why |
|---|---|---|
| "meal-ready estimate worth 0.63-0.76 RMSE" (advocate opening 6) | critic right | the gamer's "honest+src" adds the promise and the meal-ready estimate together; neither was measured alone |
| "26 of 28 claims held" (advocate opening 1) | critic right | claims 19, 25, 26 are substantive; 27-28 untested; the verdict does not change |
| Booked slot of prebooks: note only, or a decision item? | critic right: a decision item | issue 1 asked about forecasts with unverified snapshot timing and never separated a customer-booked slot; one decision per issue. Advocate right that the booked-slot meaning is inferred (EV-7) and that the mildest option suffices to ship |
| Probe 13 "no newest period outside the band" | neither fully | the probe's own line shows p50 z = +3.8 for 23 Oct, so its reading sentence is wrong for that statistic (a probe-text bug); probe 13 tests release-end censoring, not the per-cut selection, which the table above measures |

**Open issues in the record**

| Issue | Verdict | What, why |
|---|---|---|
| **H** (Horizon) | **revise** | (1) Footnote [^x21h4] as above. (2) Gap bullet 1: replace "No fixed gap ... (0.07-0.12% of the eligible rows)" with the measured selection (a third of the last hour withheld, kept orders 1.8-2.1 min faster) and its score effect (filter within 0.02 of all true labels; a 1-hour gap costs 0.00/0.00/+0.07). (3) Add an option "A + 1-hour gap": same windows, gap about the p99 delay, removes the selection, costs up to 0.07 RMSE on 24 Oct, makes the design an application of SPLIT-10 instead of an exception. (4) Recommendation stays A (one-day windows 22-24 Oct, filter only), recorded as a SPLIT-10 exception of fugaku's kind with the measurement; the decision line becomes "keep A, add a 1-hour gap, or change to B or D?". (5) Notes for the AI on A: cite fugaku as precedent and the nyc/pkdd/lusaka one-day gaps as the contrast (date-level windows; a one-day gap here leaves 48.7%). The 1-hour-gap option needs `train = train[accepted_at < start - 1h]` before the delivered-before-start filter and the assertions |
| **2** (62 rows on 25 Oct) | **keep as written** | B is the only option consistent with SPLIT-15 (Must) and the 2026-11-11 cross-dataset ruling (coffee_rating_prediction, kickstarter). Add to Experiments: `check_patched.log` with B applied: 0 errors, 0 warnings, `accepted_check_warnings_unused` info, which the notes' removal of `accepted_check_warnings` clears |
| **3** (remaining minutes) | **keep as written** | USE-5 (Must); four independent runs agree (direct fit 41-75 RMSE against 10.7-11.7 for a rule); every ETA sibling counts from its prediction point (precedent F1); the total was an AI proposal, so B reverses no curator ruling. The metric CC re-look stays in the notes |

Merge: none. Issue 1 is resolved and stays closed; the new prebook item below is separate from it.

**Changes to make now (no decision needed)**

| Change | Rule |
|---|---|
| LEAK-9 protocol line: a `Potential leak, kept on purpose:` bullet with the gamer's numbers (courier's next acceptances within the test day: RMSE 7.72/8.29/7.45 to 7.07/7.61/6.76, gain 0.65-0.70 on 3 of 3 days; no column drop closes it), and in `splits_comment`: each test row is predicted from the training rows and its own features only; a method that reads other test rows is called out and not benchmarked. No data change | LEAK-9 (Should), loan_default_prediction_imperial_college (2026-11-10, Andrej) |
| `splits_comment`: drop "Cadence and window count follow the eight-day operational release" (claim 28, unsupported); say the source is silent on horizon and cadence, a daily refit is assumed, SPLIT-14's floor fixed the windows, and the filter's measured selection and score effect (table above) | SPLIT-12, SPLIT-10 |
| Note in `curation_comments`: 42 orders over 3 h remaining, 33 prebooks; 9 non-prebook (2 over 6 h, max 652 min), kept; the ETA family drops trips over 3 h (lusaka, nyc, pkdd) and the gamer found dropping training rows over 180 min changes nothing | CLEAN-11 (Should) |
| `known`: "district" → "business area of the accepted waybill" | EV-2 |
| "structural zero event times" → grab, fetch and arrive times and the courier coordinates only | EV-2 |
| "redundant dt" → `dt` is the source's cohort date (differs from the local creation date for 1,758 orders) | EV-2 |
| 2026-11-21 Assessment: 14 of the 213 pre-17-October placements are not prebooked | EV-2 |
| Metric note: RMSE scores the mean remaining time, not the padded ETA a customer sees | MET-8 |
| `## Review` Outcome and Main points: say issues 2, 3, H (and the new item) are open | EV-2 |

**New issue for the curator**

**4. Give prebooked orders their booked delivery time as an input?** (USE-6 Must, EV-7 Must; rank last)

- Problem: on prebooks (3.9% of rows) `estimate_arrived_time` is very likely the slot the customer booked at checkout,
  known at placement, not a platform forecast; issue 1 dropped it as a forecast.
- Evidence: on prebooks, promise − acceptance correlates 0.854 with the remaining time; the bare promise scores 9.75
  min RMSE against about 10.5 for the shipped-input model; the promise is constant across an order's waybills.
- Critic: a customer request known at placement is a legitimate input (USE-6); issue 1 never separated it.
  Advocate: the meaning is inferred, not documented (EV-7); option (a) partly reopens issue 1; under issue 3 B the gap
  is under 1 min on 3.9% of rows.
- Options: (a) add promise − acceptance as an input for `is_prebook = 1` rows only; (b) keep the exclusion, say in
  `fit_reason` that prebooks lack their booked time. Recommendation: (b), unless documentation shows the field is the
  booked slot. Decision: (a) or (b)?

**Cross item (rule text, not this dataset)**

`split_tree.md` (the gap paragraph and the "late labels" leaf) says "a gap of about the delay, **or** training only
on cases whose outcome is known before the window"; `splits.md` SPLIT-10 says both, with no gap only on measurement.
One of the two texts needs aligning; the amendment of 2026-11-05 (Lennart) is the authority. Also the probe 13 reading
sentence ignores per-period |z| ≥ 3 (p50 z = +3.8 here).

**Agreed facts**

- 568,545 labeled accepted orders, 568,483 after issue 2 B; 15 inputs; none from after acceptance.
- `check.log` errors on SPLIT-15; `check_patched.log` (B applied): 0 errors, 0 warnings, 2 info.
- 0.0% of test rows have an exact feature copy in train; every training event before the cut (claim 12).
- Training shares 60.7 / 74.4 / 88.1%; 21 Oct would train on 48.7%; the filter drops 370/407/423 orders, nearly all
  accepted in the last hour.
- Direct fit on the total target 41-75 RMSE against 10.7-11.7 for elapsed plus a mean; 96-98% of its squared error
  on prebooks; remaining-time fit 7.2-8.7.
- Courier's future within the test day: gain 0.65-0.70 RMSE, no clean column fix.
- Licence CC BY-NC 4.0 with a no-redistribution clause: a note under EV-4 (lucas_topsoil), never a reason.

**Consistency with precedent**

- Issue 2 B: coffee_rating_prediction, kickstarter (2026-11-11). Issue 3 B: sendy, nyc/pkdd taxi, lusaka, brazilian
  (counter-case medical_facility is the source's own target). LEAK-9 line: loan_default_prediction_imperial_college.
- Gap: fugaku_hpc_job_failure (filter only, exception, 2026-11-03) is the closest precedent; the fact that sets meituan
  apart from the one-day-gap ETA family is the eight-day release with daily windows (a one-day gap breaks SPLIT-14's
  floor). With the measurement written down this is a second exception of fugaku's reason; the register's SPLIT-10
  `amendment_due` flag should count it, and two exceptions of the same reason (exact completion timestamps, selection
  measured without score effect) may make an amendment due at the third.
- Forecast exclusion (issue 1): departs from USE-6's default with a stated reason (snapshot timing); unchanged.

</details>

<details><summary>Advocate (2026-11-21)</summary>

**Advocate opening: meituan_food_delivery_time (meituan), 2026-11-21**

**Position: ship after two definition fixes (issue 2 B, issue 3 B), plus notes.** I do not defend the definition as merged on two points. It fails a Must on each (SPLIT-15: it does not run; USE-5: the target), and each has a cheap fix one rung down the remedy ladder. Everything else holds or needs only a note.

**1. A real, first-party ETA task with clear signal and no data leak (USE-1, LEAK-10, TP rules)**
- **Use case:** the source's Sample Question 4 names it: "predict ... precise timings for order pick-up and delivery" (claim auditor, claim 21). The domain practitioner, acting as the ETA team, has all 15 inputs at acceptance and none from after it. The fit is direct for ordinary orders (96% of rows).
- **Signal:** on the remaining-time target, LightGBM gets 7.19 / 8.12 / 7.78 min RMSE. The recorded platform promise gets 12.14 / 11.79 / 11.76, and elapsed plus the training mean gets 10.68 / 11.49 / 11.01 (domain practitioner; claim 17). The blind reviewer found the same independently: R² 0.63 on non-prebook rows, against 0.27 for the rule. The task is not trivial and not noise.
- **No leak:** 0.0% of test rows have an exact copy in train (leak.log). Every training event falls before the cut, including events of rejected waybills (claim 12). `check_patched.log` reports 0 errors and 0 warnings. 26 of the 28 tested claims held or were wording-only.
- **Why it outranks the objections:** none of them is a validity failure without a fix. Under principles step 5, exclusion is for a Must that cannot be fixed.

**2. Issue 3 (target): I concede the problem; re-target with option B, don't exclude (USE-5 Must; remedy ladder)**
- **The problem is real.** Fitted directly on the total target, LightGBM gets RMSE 43-69 against 10.7-11.5 for elapsed plus the mean. 96-98% of the squared error falls on the 3.9% prebook rows. The task probe ranks linear (10.4) far ahead of random forest (31.2) and LightGBM (62.8). The blind reviewer and the task gamer measured the same.
- **Fix:** target = arrival minus acceptance. `elapsed_minutes` stays an input and all prebooks stay. The customer sees the same ETA, and the score then measures the unknown part only. This is "fix the definition (re-target)", the second rung.
- **Precedent:** every shipped ETA sibling counts from its prediction point: sendy, nyc/pkdd taxi, 2024_lusaka, brazilian_ecommerce (precedent checker, F1).
- **Reverses no human ruling:** the total target was an AI proposal. Myunghwan's quoted words fix only the prediction point.
- **The task survives the fix:** remaining-time RMSE is 7.7-8.7 against a no-learning baseline of 10.7-11.5 (issue 3 table).

**3. Issue 2 (62 rows after midnight): option B, a 0.01% filter (SPLIT-15 Must)**
- **Fix:** drop the 62 acceptances between 00:00 and 00:23 on 25 October. With them gone, the patched check runs clean (`check_patched.log`). Also remove the stale `accepted_check_warnings` entry, which is now `accepted_check_warnings_unused`.
- **Precedent:** the 2026-11-11 cross-dataset ruling (Lennart, A) cut coffee_rating_prediction's and kickstarter's partial newest periods the same way.
- **Not drift:** Myunghwan approved A on 2026-11-09, before SPLIT-15 was amended on 2026-11-10. That is a rule change after the decision.

**4. The split is sound and is the only design that meets the floors (SPLIT-10, SPLIT-14, SPLIT-15, SPLIT-33)**
- **Windows:** one-day windows on 22, 23 and 24 October train on 60.7% / 74.4% / 88.1% of rows. That gives three windows, SPLIT-33's count, with the newest tested. Any earlier day falls below half (21 October: 48.7%).
- **Filter instead of a gap:** training keeps only orders delivered before midnight. This excludes 0.07-0.12% of orders (370 / 407 / 423). A 1-day gap would cost a window under the floor.
- **Precedent:** fugaku uses the same filter-only design (2026-11-03, Myunghwan). Probe 13 shows no censoring at the release end (|z| < 3 everywhere).
- **Remaining step:** write both facts into the splits comment (precedent checker, F3; Horizon notes on A). That is documentation, not a change.

**5. The gamer's exploit is an evaluation leak, fixed by a protocol line (LEAK-9 Should)**
- **The exploit (NEW):** reading the same courier's next acceptances within the test day lowers RMSE by 0.65-0.70. The gamer found no column drop that closes it without also losing legitimate history.
- **Rule:** LEAK-9 covers exactly this case: "a model can read other test rows" is "fixed in the scoring ... or by a protocol line the benchmark checks, not in the data".
- **Precedent:** loan_default_prediction_imperial_college (Andrej, 2026-11-10) kept its columns and added the line. So did spanish_motor, medical_facility and bank_marketing.
- **Remedy:** add to the notes and `splits_comment`: each test row is predicted from the training rows and its own features only; a method that reads other test rows is called out and not benchmarked.
- **Not a data defect:** coarsening `accepted_at` would damage a legitimate input. The exploit needs transductive use of the test block.

**6. Missing inputs make prebooks approximate, not the task invalid (USE-6; resolved issue 1)**
- **The gap:** the booked delivery time of prebooked orders is missing (domain practitioner, F1: the model is at about 10.5 min against 9.75 for the bare promise, on 3.9% of rows). So are the meal-ready estimate (gamer flaw B, worth 0.63-0.76 RMSE) and courier load (worth about 2%).
- **Why the forecasts are out:** Myunghwan excluded both forecasts on 2026-11-09, citing the unverified snapshot timing (LEAK-10, EV-7). That is a stated reason, not drift: the meal-ready forecast changes across waybills for 8,794 orders (precedent checker, F5).
- **Prebooks after issue 3 B:** prebook rows weigh only their share in the score. The booked-time gap then costs little.
- **Remedy:**
  - State in `fit_reason` that the booked slot of a prebook is not an input.
  - The prebook-only carve-out stays the curator's choice (it partly reopens issue 1).
  - Courier load is an engineered cross-row feature. Under minimal preprocessing it stays out, with a note.

**7. The rest is notes; the licence never decides (EV-4 Must, MET-8, CLEAN-11 Should)**
- **Licence:** CC BY-NC 4.0 with a no-redistribution clause. Under EV-4 that is a one-line note, "never the reason for a `No`" (precedent: lucas_topsoil).
- **Metric:** RMSE in minutes is the fallback. No source metric exists (claim 23), and it matches 2024_lusaka ("ok keep minutes"). After issue 3 B, the metric CC needs a new look, and RMSE on remaining minutes stays the natural choice. The asymmetric customer-ETA point (domain practitioner, F3) belongs in the metric note.
- **Doc fixes, all cheap:**
  - `da_id` is the "business area of the accepted waybill".
  - "Structural zeros" applies to the grab, fetch and arrive times and the courier coordinates only.
  - `dt` is the source's cohort date, not "redundant".
  - 14 of the pre-17-October placements are not prebooked.
  - The "Main points" block is stale.
- **Long non-prebook orders:** 9 non-prebook orders with more than 3 h remaining (precedent checker, F4). A note is enough; CLEAN-11 is a Should, and the count is tiny.

**Verdict sketch:**
- **Validity:** USE-5 triggered, fixed by re-target (issue 3 B). SPLIT-15 triggered, fixed by the filter (issue 2 B). LEAK-9 triggered, fixed by a protocol line. LEAK-10 holds. SPLIT-10 and SPLIT-14 hold.
- **Value:** a real signal (learner 7.2-8.1 against 10.7-11.5 for the rule).
- **Quality:** doc fixes; prebook booked time, licence and long tail kept with notes.
- **Ship after changes.**

</details>

<details><summary>Advocate rebuttal (2026-11-21)</summary>

**Advocate rebuttal: meituan_food_delivery_time (meituan), 2026-11-21**

The critic and I agree on the verdict: ship after changes, with no case for exclusion. All seven of the critic's points match points of my opening, and I dispute none of them. Below I concede each and add what follows. On two points, 4 and 5, I narrow the weight the critic gives them.

| Critic point | Answer | What follows |
|---|---|---|
| 1. Target (issue 3) | concede | Option B. Four independent runs agree (direct LightGBM 41-75 min RMSE against 10.7-11.7 for the rule). USE-5 is a Must and the fix costs nothing. Re-look at the RMSE CC line afterwards. |
| 2. Does not run (issue 2) | concede | Option B, plus removing the stale `accepted_check_warnings` entry and the two 62-row sentences. Option A cannot stand under SPLIT-15. |
| 3. Courier's future in the test day (LEAK-9) | concede | Add a "Potential leak, kept on purpose" bullet with the gamer's numbers (gain 0.65-0.70, 3 of 3 days) and the protocol sentence in `splits_comment`. No data change, since no column drop closes the channel. |
| 4. Booked time of prebooks | concede the facts; narrow the weight | See below. |
| 5. Filter in place of a gap, reason unwritten | concede; narrow one piece of evidence | See below. |
| 6. Nine non-prebook orders over 3 h | concede | A note in `curation_comments`: the count, the 652-minute maximum, and why they stay. The cap stays a curator option. CLEAN-11 is a Should, and the gamer found that dropping training rows over 180 min changes nothing. |
| 7. Stale and wrong text | concede | All six fixes apply as listed. The `## Review` Outcome and Main points blocks need updating once issues 2 and 3 and the Horizon decision are settled. |

**Point 4: a decision item, mildest (b); its weight shrinks under issue 3 B**
- **I agree:** this is a new decision for Myunghwan, not a fix. The booked-slot meaning is inferred, not documented (EV-7), and option (a) partly reopens issue 1, which Myunghwan settled on 2026-11-09.
- **What the critic leaves out:**
  - The evidence that the model loses on these rows is about 10.5 min against 9.75 for the promise. That is a gap of under 1 minute on 3.9% of rows.
  - Under the total target these rows carried 96-98% of the squared error. Under issue 3 B they weigh about their share of the rows (domain practitioner, finding 1).
  - So once issue 3 B is applied, the gap is an approximate fit on a small subgroup (USE-1 approximate). It is not a validity failure.
- **Ranking:** the item should sit below issues 2 and 3 and the Horizon decision. Option (b) is enough to ship.

**Point 5: rewrite the splits comment; the selection effect is bounded, not shown**
- **I agree:** the claim that "cadence and window count follow the release" is unsupported (claim 28). The comment should say:
  - the source is silent on horizon and cadence, and a daily refit is assumed;
  - the floor fixed the windows;
  - a 1-day gap would put training at about 48.7%;
  - the excluded share is 370 / 407 / 423 orders;
  - fugaku is the precedent.
- **I dispute that the gamer's last-hour numbers measure a selection effect.**
  - The 24.5-25.6 against 26.6-27.6 min means compare the last training hour (23:00-24:00) with the same hour a day earlier. They do not hold time of day fixed against the orders actually withheld.
  - A difference of the same size can come from day-to-day variation alone.
  - What bounds any selection effect is the excluded share, 0.07-0.12% of eligible rows. Probe 13 also shows no newest day outside the band of the earlier days (|z| < 3 on the mean, the median and the 90th percentile).
- **What follows:** under the amended SPLIT-10, the measurement that allows no gap is the excluded share. Quote that number. Do not present the last-hour comparison as a measured selection effect.

**Fact the critic raised**
- `group.log` is missing from the run folder. I confirm this and do not rely on it. No point on either side depends on a group probe: entities recur by design under a forward split (merchants seen 99.8-99.9%, couriers 98.5-99.1%; claim 15).

**Joint position for the mediator:**
- **Validity fixes:** issue 3 B, issue 2 B, and the LEAK-9 protocol line.
- **Curator items:** issues 2 and 3, the Horizon decision (recommend A), and the new prebook booked-time item (recommend b, ranked last).
- **Notes and text:** points 5, 6 and 7.

</details>

<details><summary>Critic (2026-11-21)</summary>

**Critic opening: meituan_food_delivery_time (meituan)**

**Position: do not ship as merged. Ship after changes 1-3; 4-7 are a curator item, notes and doc fixes.** The task is real (an ETA update at courier acceptance, first-party data, clear signal), so nothing here argues for exclusion. But the merged definition does not run, its target makes the benchmark rank the wrong thing, and it lacks the protocol line that its own test set needs.

Read: `dataset.py`, README, the record (`## Review`, Horizon block, issues 1-3), the claim, domain, precedent, blind and gamer reports, the column findings, `check.log`, `check_patched.log`, `leak.log`, `task.log`, `dtype.log`. **`group.log` is missing** from the run folder.

**1. The target ranks methods by extrapolating a known input (KNOWN issue 3; USE-5 Must)**

- **Problem:** `delivery_minutes` = elapsed (known, an input) + remaining. On prebooked orders elapsed runs to 10,293 min, so 98% of the target's variance is a column the model already has.
- **Evidence:**

  | Source | Linear / rule | Random forest | LightGBM on total | LightGBM on remaining + elapsed |
  |---|---|---|---|---|
  | panel task probe (`task.log`), RMSE | linear 10.41 | 31.16 | 62.83 | - |
  | column audit, 3 days | elapsed + mean 10.68-11.49 | - | 42.86-68.99 | 7.73-8.70 |
  | blind review, 200k sample | elapsed + median 11.4 | - | 41.4 | 8.1 |
  | task gamer, untuned | elapsed + median 10.73-11.71 | - | 51.11-74.51 | 8.56-9.90 |

  Four independent runs agree: a rule with no learning beats every tree model by 4-6x, and 96-98% of LightGBM's squared error sits on the 4% prebook rows. On non-prebook rows the two fits are close (7.7-9.2 vs 7.6-8.4).
- **Effect:** the benchmark would score extrapolation of one column on a few hundred rows, not delivery prediction. The customer's ETA is acceptance + remaining minutes either way.
- **Precedent:** every shipped ETA task (sendy, nyc/pkdd taxi, lusaka, brazilian) counts from its prediction point. The total was an AI proposal; no curator words fix it (precedent F1).
- **Remedy:** option B of issue 3: target = arrival − acceptance, `elapsed_minutes` stays an input, all prebooks stay. Re-look at the RMSE CC line afterwards, as the issue's notes say.

**2. The definition as merged does not run (KNOWN issue 2; SPLIT-15 Must)**

- **Evidence:** `check.log` raises "The newest cutoff's window ends at 2022-10-25 00:00:00, before the newest data (2022-10-25 00:23:29)". With the 62 rows dropped, `check_patched.log` has 0 errors, but reports `accepted_check_warnings_unused` for `splits_rows_unused`.
- **Effect:** no build, no check, no probe on the shipped definition.
- **Remedy:** option B (drop acceptances from 25 Oct 00:00 local, 62 rows, 0.01%), remove `accepted_check_warnings`, the 62-row sentence in `task_summary.row` and the last sentence of the splits bullet. Same as coffee_rating_prediction and kickstarter (2026-11-11, cross-dataset item A). Option A cannot stand under a Must.

**3. Test rows give away each other's outcome; no protocol line (NEW; LEAK-9 Should)**

- **Problem:** a test window is one whole day of one city's couriers. A model that reads the other test rows of the same courier (next accept time, accepts in the next 30/60 min, position at the next assignment) learns when the courier became free again, which is the delivery.
- **Evidence (task gamer, LightGBM, 22/23/24 Oct):**

  | Model | RMSE |
  |---|---|
  | honest (remaining target, courier past only) | 7.715 / 8.286 / 7.454 |
  | + courier's future within the test day | 7.065 / 7.610 / 6.756 |
  | gain | 0.65 / 0.68 / 0.70 (8-9%) |
  | ref: fetch time, a post-acceptance field | 6.314 / 6.830 / 6.183 |

  The gain is consistent on 3 of 3 days, larger than the courier-load gain the domain practitioner measured (0.13-0.20), and about half of what a known post-acceptance field gives. The gamer found no column drop that closes it without losing the legitimate courier history; `courier_id` and `accepted_at` are the channel.
- **Rule:** LEAK-9 as amended 2026-11-05: an evaluation leak is fixed by a protocol line the benchmark checks. `dataset.py` has none (no "other test rows" text anywhere). Precedents: duolingo_spaced_repetition_recall, frempl_french_motor_personal_line, medical_facility_operational_data, fremtpl2.
- **Remedy:** a `Potential leak, kept on purpose:` bullet in `curation_comments` with the numbers above, and the protocol sentence in `splits_comment`: each test row is predicted from the training rows and its own features only; no feature or model step may use other test rows; a method that reads them is called out and not benchmarked. No data change.

**4. Prebooked orders lose their booked delivery time (NEW; USE-6 Must, EV-7)**

- **Problem:** issue 1 dropped `estimate_arrived_time` as a platform forecast. On prebooked orders it is very likely the slot the customer booked at checkout, known at placement, not a forecast.
- **Evidence (domain practitioner):** on prebooks, promise − acceptance correlates 0.854 with the remaining time; as a bare predictor it scores 9.75 min RMSE, the shipped-input model about 10.5. The promise is constant across an order's waybills (column audit: 0 orders vary).
- **Limit:** that the field is the booked slot is inferred from the data, not documented (EV-7), and it partly reverses Myunghwan's 2026-11-09 choice. So this is a decision, not a fix.
- **Remedy:** a new decision item for Myunghwan: (a) keep "promise − acceptance" as an input for `is_prebook = 1` rows only, or (b) keep the exclusion and say in `fit_reason` that prebooked rows lack their booked time. Mildest: (b).

**5. The split filter replaces a gap without the reason written down (NEW in part; SPLIT-10, SPLIT-12 Should)**

- **Problem:** `splits_comment` says "Cadence and window count follow the eight-day operational release", which no source states (claim auditor 28, untested). It does not say why the filter replaces the 1-day gap the ETA siblings use.
- **Evidence:** a 1-day gap would push 22 Oct's training to about 48.7%, below SPLIT-14's floor (Horizon block). The filter drops 370/407/423 orders (0.07-0.12%); the gamer measured a small selection effect: the last training hour's mean target is 24.5-25.6 min vs 26.6-27.6 a day earlier (slow late orders are the ones held back). Footnote [^x21h4] paraphrases SPLIT-10 as "gap or filter"; the amended rule allows no gap only on a measurement.
- **Remedy:** rewrite `splits_comment` per the Horizon notes for A: the source is silent on horizon and cadence (daily refit assumed), the floor fixed the windows, the gap's cost, the excluded share and its selection effect; cite fugaku as precedent.

**6. Nine non-prebook orders over 3 hours remaining (NEW, minor; CLEAN-11 Should)**

- **Evidence (precedent F4):** 42 orders over 3 h remaining, 33 of them prebooks; 9 non-prebook, 2 over 6 h (max 652 min). lusaka, nyc and pkdd drop trips over 3 h as not closed in the app (Lennart, 2026-10-26 / 11-05).
- **Effect:** under RMSE on option B, one 300-min error weighs about as much as 1,000 typical rows (estimate). The gamer found dropping training rows over 180 min changes nothing, so this is about scoring, not fitting.
- **Remedy:** a note in `curation_comments` stating the count and why they stay, or a decision item if the curator wants the family's cap. Not a reason to hold the dataset.

**7. Stale and wrong text (quality; EV-2 Must for the facts)**

- `known`: "district" → "business area of the accepted waybill" (supplement 2.6: overlaps, also order type; `da_id` follows the accepting courier in 1,963 orders).
- "structural zero event times" → only grab, fetch, arrive times and courier coordinates are 0 on rejected rows; placement, push, dispatch are real.
- "redundant dt" → `dt` is the source cohort date, differs from local creation date for 1,758 orders.
- 2026-11-21 Assessment: 14 of the 213 pre-17-Oct placements are not prebooked ("mostly prebooked").
- Metric note: one sentence that RMSE scores the mean remaining time, not the padded customer ETA (domain practitioner finding 3; MET-8 fallback, no rule breach).
- `## Review` Outcome and Main points say nothing is open; issues 2, 3 and the Horizon decision are open.

**Not argued:** the licence (CC BY-NC plus a permission request) is a note under EV-4, not a reason (lucas_topsoil precedent). Missing courier load is an engineered feature the source cannot give row by row; the task is real without it.

</details>

<details><summary>Critic rebuttal (2026-11-21)</summary>

**Critic rebuttal: meituan_food_delivery_time (meituan)**

The advocate and I agree on the verdict: ship after issue 2 B, issue 3 B and a LEAK-9 protocol line, with notes. The disagreements are two points of fact and one on point 6.

| Advocate point | Reply | Why |
|---|---|---|
| 1. Real task, signal, no data leak | **Concede, with two corrections** | (a) "26 of 28 claims held or were wording-only" is generous: claim 19 (the definition does not run), 25 (the metric is refuted in effect) and 26 (stale "nothing open") are substantive, and 27-28 are untested. (b) `check_patched.log` is clean only on a patched copy (issue 2 B applied). It also shows `accepted_check_warnings_unused` as an info line, which needs removing. Neither changes the verdict. |
| 2. Issue 3 B | **Concede** | Same evidence, same remedy (USE-5 Must; precedent F1). |
| 3. Issue 2 B | **Concede** | Same remedy (SPLIT-15 Must; coffee_rating and kickstarter, 2026-11-11). |
| 4. Split sound | **Concede the design; dispute "documentation only, no censoring"** | Probe 13's own reading says it "does not show which labels a model refit at a window's start would have known (SPLIT-10)". The probe also shows p50 z = +3.8 for one newest period. The gamer measured the filter's selection effect: the last training hour's mean target is 24.5-25.6 min, against 26.6-27.6 a day earlier. Small (0.07-0.12% of rows), but the amended SPLIT-10 allows no gap only on a measurement, so the splits comment must state that effect, not only the excluded counts. This is still a text change, not a design change. |
| 5. LEAK-9 protocol line | **Concede** | We agree on the rule, the remedy and on not coarsening `accepted_at`. loan_default_prediction_imperial_college is the closest precedent (same pattern: next row of a hidden entity in the same temporal test window). |
| 6. Missing prebook booked time: a `fit_reason` note | **Dispute in part** | (a) Issue 1 asked about forecasts with unverified snapshot timing. A booked slot is a customer request known at checkout, not a forecast, and issue 1 never separated the two. So Myunghwan has not decided it. It needs its own decision item (one decision per issue), with the note as the mildest option. Under USE-6 (Must) an input known at the prediction point is legitimate. (b) "Costs little after issue 3 B" is a score argument. Whether the task matches what the actor has does not depend on how much the score moves. On those rows the model (about 10.5) still loses to the bare slot (9.75). (c) **Factual error:** "meal-ready estimate worth 0.63-0.76 RMSE" is the gamer's "honest+src" gain from **both** the promise and the meal-ready estimate together. Nobody measured the meal-ready estimate alone. |
| 7. Licence, metric, doc fixes, long tail | **Concede** | Same list. One addition: the 9 non-prebook rows over 3 h are noted with their count and the family's 3-hour cap (lusaka, nyc, pkdd) as the contrast, so the curator can choose the cap. |

**Net:** ship after issue 2 B, issue 3 B, the LEAK-9 protocol line and the doc fixes. One new decision item goes to Myunghwan: the booked slot of prebooked orders as an input. The splits comment states the filter's measured selection effect.

</details>

<details><summary>Claim audit (2026-11-21)</summary>

**Claim auditor: meituan_food_delivery_time (meituan)**

**What I ran**

- The definition's own `_load_raw` and `_clean`, on the raw CSV in the run folder. Two runs. Scripts and logs are in the run folder. Note: the first run has an index-alignment bug in its baseline columns; the second replaces it.
- **How I worked around the split error.** `_make_splits` still raises on this branch: "The newest cutoff's window ends at 2022-10-25 00:00:00, before the newest data (2022-10-25 00:23:29)". I rebuilt the three windows by hand with the definition's own filters:
  - train = accepted before midnight and delivered before midnight;
  - test = accepted on that day;
  - the 62 rows from 25 October are in no window.
- I extracted the text of the background document, the October 2024 supplement and Wang et al. 2025 with pypdf (installed into the run folder).
- I read the panel outputs: `check.log` (it fails with the split error) and `check_patched.log` (0 errors, after the 62 rows are dropped). I also read `leak.log` and `task.log`; both ran on the patched frame of 568,483 rows.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 654,343 attempts for 568,546 orders, exactly one accepted attempt per order | curation bullet 2 | count the raw rows | holds | 654,343 / 568,546; at most 1 accepted per order; every order has one | PROV |
| 2 | Rejected attempts have "structural zero event times" | curation bullet 2 | zero share per column on rejected rows | holds, wording too broad | grab, fetch and arrive times and the grab coordinates are 0 on 100% of rejected rows; placement, push and dispatch times are never 0 (supplement 2.4 lists only grab/fetch/arrive and the courier coordinates) | EV-2 |
| 3 | One accepted order has no arrival label, which leaves 568,545 rows | curation bullet 2, decision 1 | count | holds | 1 accepted row has `arrive_time` = 0 (the same row has `dispatch_time` = 0); 568,545 rows | - |
| 4 | Target = total minutes from placement to arrival | `predicted` | recompute from raw | holds | maximum difference 0.0 | USE-5 (issue 3 is open) |
| 5 | `grab_lat`/`grab_lng` are the courier's position at acceptance, per Wang 2025, correcting the 2024 document | curation bullet 3, `known` | read both documents | holds | 2024 Table 2: "when the waybill is assigned"; Wang 2025 Table A.2: "Courier latitude when accepting order" | USE-3 |
| 6 | "district" (`da_id`) | `known` | supplement 2.6 | refuted in wording (KNOWN, column audit) | "associated with geographic locations and other factors such as order type ... may have geographically overlapped areas"; 20.3% of accepted rows have a `da_id` other than the courier's most common one that day | EV-2 |
| 7 | The source `is_weekend` flag describes order creation, so it is recomputed from acceptance | curation bullet 8 | compare the flag with three dates | holds | the flag equals weekend-of-creation-date on 100% of rows, weekend-of-acceptance on 99.88%, weekend-of-`dt` on 99.89% | - |
| 8 | Timestamps converted to China local time (UTC+8) | curation bullet 8 | dispatch checkpoints in local time | holds | the checkpoints fall at 11:25, 11:27 and 11:30 local each day, the "noon peak" of Wang 2025 | - |
| 9 | Dispatch snapshots cover only three noon checkpoints a day | curation bullet 10 | `dispatch_rider` times | holds | 24 checkpoints, 3 per day, all 11:25-11:30 | - |
| 10 | The supplement documents a wave-start indexing defect | curation bullet 10 | supplement 2.2 | holds | "may be problematic due to incorrect indexing" | - |
| 11 | Both platform forecasts and their derivatives are excluded | `known`, curation bullet 4 | frame columns | holds | the frame has 15 features plus the target; none is built from `estimate_*`; `delivered_at` leaves the frame | USE-6 |
| 12 | Every observed training event happens before the test window's midnight; arrival is the latest of the six clocks | splits comment, curation bullet 9 | maximum of all six clocks on the training rows, including the order's rejected waybills | holds | latest accepted-row event per fold: 23:59:47, 23:59:53, 23:59:56 on the day before; latest rejected-waybill event 23:45-23:48; the assertion in `_clean` passes | SPLIT-9, SPLIT-10 |
| 13 | Train/test sizes, and 370/407/423 unfinished orders excluded | README splits table, decision 2 | hand-built windows | holds | 500,764/67,349; 423,008/77,719; 345,355/77,637; 370/407/423 excluded | SPLIT-10 |
| 14 | Each train side holds at least half the rows; 22-24 Oct are the last three complete days | splits comment | training share | holds | 88.1% / 74.4% / 60.7%; 25 Oct holds only 62 rows | SPLIT-14 |
| 15 | Merchants and couriers recur | `split` | seen fractions | holds | merchants 99.8-99.9% seen, couriers 98.5-99.1% (decision table reproduced) | SPLIT-13 |
| 16 | No row is a copy across the split | implied | hash of the 15 features, train against test | holds | 0 copies in every fold (leak probe: 0.0%); 4 rows share all features within the frame (2 conflicting, info) | LEAK |
| 17 | Recorded-promise RMSE 12.14/11.79/11.76; elapsed + training-mean remaining 10.68/11.49/11.01 | decision 2 | recompute | holds | identical to 4 decimal places | - |
| 18 | 4,962 merchants, 4,901 couriers, 22,181 prebooked | decision 1 | count; Wang 2025 | holds | Wang: 4,962 merchants, 4,955 couriers, of whom 54 never accepted, which leaves 4,901; 23 districts | - |
| 19 | Row: Oct 17-24 cohorts plus 62 acceptances after midnight on 25 Oct | `row`, accepted warning | count | the count holds; the definition does not run (KNOWN, issue 2) | 62 rows, 00:00-00:23; `check.log` raises the SPLIT-15 error; `check_patched.log` then reports `accepted_check_warnings_unused` | SPLIT-15 |
| 20 | Collection facts: acceptances run to 25 Oct 00:23; some prebooked placements go back to 11 Oct | assessment 2026-11-21 | minimum placement time | holds, incomplete | earliest placement 11 Oct 21:29; 213 orders were placed before 17 Oct, 199 of them prebooked and **14 not prebooked** | EV-2 |
| 21 | `fit_reason`: "the challenge names delivery timing prediction" | `fit_reason` | background, Sample Question 4 | holds | "predict courier delivery processes ... like precise timings for order pick-up and delivery" | USE-1 |
| 22 | `fit_reason`: the promise has "unverified snapshot timing" | `fit_reason`, curation bullet 5 | does the promise vary across an order's waybills? | holds; the evidence leans one way | the promise is constant per order across all orders with several waybills (column audit: 0 orders vary), while the meal-ready estimate varies in 8,794 orders. That fits a promise fixed at or before the first dispatch. It does not prove the timing, and it changes nothing now that the promise is not an input. | EV-7 |
| 23 | Metric: fallback, because no source prescribes one | `metric.reason` | search the background, the supplement and Wang 2025 for RMSE, MAE, MAPE, "evaluat", "metric", "accura" | holds | no predictive scoring metric anywhere; "evaluates" refers only to the matching-degree score; no leaderboard | MET-1, MET-11 |
| 24 | RMSE is computable on our folds | MET-2 | `metric.resolve("regression")`, then `score` on each fold | holds | no scoring columns needed; 67,349-77,719 test units per fold; RMSE of the training mean 82.3/71.9/93.1; elapsed + mean 10.68/11.49/11.01 | MET-2 |
| 25 | RMSE on the total target measures the ETA task | MET-2, MET-3 (implied) | probe family ranking | **refuted in effect** (KNOWN, issue 3; new evidence) | task probe: linear 10.41, random forest 31.16, LightGBM 62.83, single feature (`elapsed_minutes`) 57.25. The declared target ranks the families by whether they can extrapolate the known elapsed time, not by how well they predict delivery. | USE-5, MET-1 |
| 26 | Record "Main points": "No further curator decision remains" | `## Review` | open issues | refuted (stale) | issues 2 and 3 and the Horizon decision (2026-11-21) are open | - |
| 27 | Previous-panel model numbers (residual LightGBM 8.42-9.52; isolated learner 7.32/8.21/7.70) | assessments 2026-11-09 | - | untested | no refit; the column audit's residual LightGBM gives 7.73/8.70/8.33 with other settings, so the spread does not contradict them | - |
| 28 | "Cadence and window count follow the eight-day release, not model scores" | splits comment | - | untested (KNOWN, Horizon) | the source states no cadence; the Horizon block asks for the splits comment to say so | SPLIT-12 |

**Refuted or untested claims, ranked**

1. **The metric on the total target (claim 25, KNOWN, issue 3; the evidence is NEW).**
   - The panel's task probe ranks linear (RMSE 10.4) far ahead of random forest (31.2) and LightGBM (62.8).
   - The trees lose because they cannot extrapolate `elapsed_minutes` on prebooked orders (elapsed time up to 10,293 minutes).
   - This shows the ranking issue 3 predicts, on the panel's own probe.
   - Mildest remedy: option B of issue 3, remaining minutes as the target; RMSE in minutes stays.
2. **The definition does not run (claim 19, KNOWN, issue 2).**
   - With the 62 rows dropped (the patched check), `accepted_check_warnings_unused` appears.
   - Option B's notes already say to remove the accepted warning and the 62-row sentence.
3. **"district" (claim 6, KNOWN, column audit doc fix).**
   - Supplement 2.6 says `da_id` also reflects order type and that areas overlap.
   - Remedy: "business area of the accepted waybill".
4. **"Structural zero event times" (claim 2, NEW, wording).**
   - Only the grab, fetch and arrive times and the grab coordinates are 0 on rejected rows. Placement, push and dispatch times are real.
   - Remedy: "Rejected attempts have zero grab, fetch and arrival times and zero courier coordinates (supplement 2.4)."
5. **Collection-facts assessment (claim 20, NEW, minor).**
   - 14 of the 213 pre-17-October placements are not prebooked.
   - Remedy: "some placements, mostly prebooked, go back to 11 Oct".
6. **Stale "Main points" (claim 26, NEW, editorial).**
   - The Outcome and Main points blocks still say that nothing is open.
   - Remedy: update them when issues 2 and 3 are settled.

Every other claim in task_summary, the curation notes, the splits comment, the decisions and the metric block held when tested. None of the tests showed a leak, a copy across the split or a training event after the cutoff.

</details>

<details><summary>Domain practitioner (2026-11-21)</summary>

**Domain practitioner: meituan_food_delivery_time**

I am the ETA team at the platform. When a courier accepts an order, I update the arrival time the customer sees, and dispatch uses the same estimate to plan the courier's route.

**Fit: direct for ordinary orders, approximate for prebooked ones.** The row, the moment and the inputs match an ETA update at acceptance. For prebooked orders, though, the model does not get the delivery time the customer booked, and that time drives my ETA.

**Metric: partly.** RMSE in minutes is a fair score for the expected remaining time. It does not score the ETA I show the customer, where a late ETA costs more than an early one. On the total target as shipped, RMSE mostly measures how well a model adds back the elapsed time on prebooked orders (issue 3).

**What I tested**

I ran one CPU job on the raw waybill CSV with the shipped selection: accepted attempts with an arrival.
- Remaining time after acceptance, split by the prebook flag.
- The recorded promise against the actual remaining time.
- An as-of courier load: the orders the same courier had accepted earlier and not yet delivered, or not yet picked up, at this acceptance time. It uses only events before the acceptance time.
- LightGBM (500 trees, 127 leaves) on the remaining-time target, in the definition's three windows (24, 23 and 22 October; training only on orders delivered before midnight). One run without the load features, one with them, and the recorded promise as a reference.

Script and log are in the run folder (`load.py`, `1401911.log`).

The `dataset check` and probe outputs this round are missing: the run folder the run folder held only `precedent/` when I looked.

**Answers as the actor**

**1. Do I have these inputs at acceptance?**

- **Inputs I have:** all 15 shipped inputs. These are the merchant, the accepting courier, the business area, the coordinates, the courier's position at acceptance, the prebook flag, the acceptance time, the elapsed time and the push and dispatch delays.
- **Inputs I would always have but the data lacks:**
  1. **The booked delivery time of a prebooked order (NEW, finding 1).** The customer picked it at checkout.
  2. **The courier's current load (NEW, finding 2):** how many orders the courier already carries and how many are not yet picked up. Meituan's own ETA features include area-level uncollected orders and capacity load.
  3. **The promise shown at checkout (KNOWN, issue 1, resolved B).** It is constant across an order's attempts, which fits a value fixed at placement. Under USE-6 I would use it as an input. Myunghwan chose the forecast-free task for safety, and I do not reopen that.
  4. **Weather and the merchant's live backlog.** The source does not publish them, and there is no remedy.
- **Nothing in the shipped inputs comes from after acceptance.**

**2. Is the target what I act on?**

No. I act on the remaining minutes: ETA = acceptance time + remaining time.

The total target adds the elapsed time, which I already know. For prebooked orders the elapsed time runs up to 10,293 minutes. This is KNOWN as issue 3, and I support option B (USE-5).

I want a number of minutes, and for the screen I want a padded quantile, not the mean (see question 5).

**3. Does one row match one decision, and is the test what I would face?**

Yes. One accepted order is one ETA update.

The test is the next day, in the same city, with the same couriers and merchants recurring. That is what a daily refit meets (USE-10). New cities and seasons are not tested; this is KNOWN from the Horizon block.

**4. Would I use this model?**

For ordinary orders, yes. A learner without the platform forecasts is clearly better than the recorded promise on the mean error:

| Test day | Inputs | RMSE | MAE | RMSE non-prebook | Within ±5 min | More than 10 min late |
|---|---|---|---|---|---|---|
| 24 Oct | shipped inputs (remaining target) | 7.19 | 5.49 | 7.02 | 54.8% | 7.9% |
| 24 Oct | + courier load | 7.06 | 5.37 | 6.87 | 56.0% | 7.6% |
| 24 Oct | recorded promise | 12.14 | 9.81 | 12.21 | 27.8% | 1.2% |
| 23 Oct | shipped inputs | 8.12 | 5.85 | 7.80 | 52.0% | 10.6% |
| 23 Oct | + courier load | 7.95 | 5.68 | 7.61 | 53.7% | 9.9% |
| 23 Oct | recorded promise | 11.79 | 9.35 | 11.82 | 30.9% | 1.9% |
| 22 Oct | shipped inputs | 7.78 | 5.75 | 7.39 | 53.1% | 9.5% |
| 22 Oct | + courier load | 7.59 | 5.58 | 7.18 | 54.5% | 8.6% |
| 22 Oct | recorded promise | 11.76 | 9.47 | 11.81 | 29.8% | 1.5% |

What would make me distrust it:
- It is late by more than 10 minutes on 8-11% of orders, against 1-2% for the promise.
- It has no booked time for prebooked orders.
- Its training covers eight days of one city.

**Findings**

**1. Prebooked orders lack their booked delivery time (NEW; USE-3, USE-6, USE-8)**

**Evidence:**

| | not prebooked | prebooked |
|---|---|---|
| rows | 546,364 | 22,181 |
| remaining time after acceptance (mean / p99) | 25.1 / 55.0 min | 40.2 / 73.6 min |
| elapsed time at acceptance (mean / p99) | 4.5 / 23.2 min | 139.3 / 1,372.4 min |
| promise minus acceptance against remaining time (correlation) | – | 0.854 |
| promise as a predictor of remaining time (RMSE) | 11.89 min | 9.75 min |

- **What the numbers show:** after acceptance, a prebooked order is an ordinary 40-minute delivery. Its long total time is the wait before acceptance.
- **The promise is the booked time.** On prebooked orders, the promise tracks the remaining time closely, so for these orders it is almost certainly the slot the customer booked, not a platform forecast.
- **The model loses on these orders.** From the all-row and non-prebook RMSEs on 24 October, the model's error on prebooked orders is about 10.5 min. The bare promise gets 9.75 min.
- **Why it matters:** the booked time is known at placement. It is the customer's request, not a platform forecast. Issue 1 dropped it together with the forecasts, and the record never separates the two.
- **Effect:** 3.9% of rows. Under the total target (issue 3, option A) these rows carry 96-98% of the squared error. Under option B they weigh about as much as their share of rows.
- **Expert change:** for prebooked rows only, keep "booked time minus acceptance" (the promise, used only where `is_prebook = 1`) as an input. Otherwise state in `fit_reason` that the booked time is missing. This is a curator decision, because it partly reverses issue 1's choice. Whether the promise of a prebooked order is the booked slot is inferred from the data, not documented.

**2. Courier load at acceptance is missing and cannot be rebuilt from one row (NEW; USE-6, minor)**

**Evidence:** the mean remaining time rises steadily with the courier's open orders, from 0 to 5 open orders:

| Courier's open orders at acceptance | Orders | Mean remaining time (min) |
|---|---|---|
| 0 | 197,618 | 23.2 |
| 1 | 179,056 | 24.3 |
| 2 | 95,562 | 26.7 |
| 3 | 44,201 | 29.2 |
| 4 | 18,808 | 31.3 |
| 5 | 6,970 | 33.1 |

- **Spread:** the median courier has 1 open order, and the 99th percentile has 5.
- **Gain from adding it:** RMSE drops by 0.13-0.20 min (about 2%) on each test day, and every metric in the table above improves.
- **Why it matters:** every platform uses this input. It needs other orders' events up to the acceptance time, so a row-level model cannot compute it from the shipped columns.
- **Weight:** an added, engineered feature, so the minimal-preprocessing practice argues against it. I rank it low: the task is real without it.

**3. RMSE scores the mean, but the ETA shown to the customer is an asymmetric decision (NEW as a metric argument; MET-1, MET-8)**

- **Evidence:** the recorded promise is early by 8.2 min on average and late by more than 10 min on 1-2% of orders. The unbiased learner is late by more than 10 min on 8-11%.
- **Platform practice:** Meituan's published ETA work trains with an asymmetric loss that penalises late predictions more (slopes 1.2 early and 1.8 late, per a summary of the Meituan tech blog; I could not open the original post).
- **What I would choose:** the source has no metric, and RMSE is the fallback under MET-8, so this is no rule violation. For the customer ETA I would choose by MAE together with the late rate, or by a quantile (pinball) loss. RMSE fits the dispatch use, the expected completion time. I would keep RMSE and add a sentence to the metric note saying that it scores the mean remaining time, not the padded customer promise. The earlier record already calls MAE and calibration diagnostics.

**4. Target: remaining minutes, not total minutes (KNOWN, issue 3)**

I support option B. The customer's ETA is the acceptance time plus the remaining minutes. With option B, RMSE in minutes scores the part I do not know.

**5. Promise excluded as an input (KNOWN, issue 1, resolved)**

At acceptance I would have it. The promise is constant across an order's attempts, which points to a value fixed at placement. I leave the decision as resolved and note only finding 1's carve-out for prebooked orders.

**Gaps ranked by how much they change the task**

1. **Total target instead of remaining time (issue 3).** It changes what the score measures.
2. **No booked time for prebooked orders (finding 1).** It affects 3.9% of rows; on those rows the model is worse than the platform's booked slot.
3. **Mean-error metric against an asymmetric customer ETA (finding 3).** It is a framing note, not a change.
4. **No courier load (finding 2).** It costs about 2% RMSE.
5. **One city and eight days, no weather (known).** Generalisation is limited, and there is no remedy.

**Sources**

- Record `curation/records/meituan_food_delivery_time.md`, plus `dataset.py` and `README.md` in the worktree.
- Column findings in the run folder.
- Rules in `use_case.md` (USE-3, USE-5, USE-6, USE-8, USE-10) and `metrics.md` (MET-1, MET-8).
- [到达时间预测两则: Uber 和美团](https://shiina18.github.io/machine%20learning/2022/03/03/predict-eta): Meituan's ETA features, including area uncollected orders and capacity load, and merchant backlog.
- [Deep Learning-Based ETA Estimation in Meituan's Delivery System](https://besthub.dev/articles/deep-learning-based-eta-estimation-in-meituan-s-delivery-system-9795f127a7ca): the asymmetric late-penalising loss. This is a summary of the Meituan tech blog post 深度学习在美团配送ETA预估中的探索与实践 (2019); the original link did not open.
- [Uber DeepETA](https://www.uber.com/en-US/blog/deepeta-how-uber-predicts-arrival-times/): MAE as the production ETA metric, and residual post-processing.

</details>

<details><summary>Precedent check (2026-11-21)</summary>

**Precedent check: meituan_food_delivery_time (PR #59 re-check, 2026-11-21)**

**What I did**
- Ran the decision register (5,933 decisions, 43 flags). Output: the run folder. No flag names this dataset. The relevant flags are general ones: `amendment_due` on SPLIT-10 (exceptions on 11 datasets) and on SPLIT-14, and `opposite_outcomes` on USE-5.
- Compared every decision of the definition, issues 2 and 3, and the Horizon block with the ETA and delivery siblings (sendy, nyc/pkdd taxi, 2024_lusaka, brazilian_ecommerce, delivery_eta_1m, medical_facility), the cross-dataset item on short newest periods, and the Cases tables of use_case.md, splits.md, cleaning_features.md and evidence.md.
- Ran one CPU job on the raw data to count long durations. Script and log are in `.../precedent/`.
- **Missing panel outputs:** the run folder contains only my `precedent/` folder. There is no check.log, README_check.md, leak/, task/, dtype/ or group.log, so I could not read them.

**Verdict per decision**

| # | Decision | Status | Closest precedents |
|---|---|---|---|
| 1 | Prediction point at courier acceptance; elapsed, dispatch and push delays and the courier position as inputs (USE-3, USE-6) | consistent | sendy (inputs: placement, confirmation and pickup times; prediction at pickup) |
| 2 | Both platform forecasts excluded (forecast-free; 2026-11-09, Myunghwan) | departs from USE-6's default, **with a stated reason** | brazilian_ecommerce keeps Olist's promise (2026-10-15). 2_month_survival keeps physician estimates out (2026-10-26, Lennart). |
| 3 | Total target since placement (issue 3, open) | **departs, no curator reason** | sendy, nyc/pkdd taxi, lusaka and brazilian all count from the prediction point. Counter-case: medical_facility. |
| 4 | Prebooks kept; durations not clipped (CLEAN-11) | consistent for prebooks. Weak open point on the longest non-prebook rows. | lusaka, nyc and pkdd drop trips over 3 h as not closed in the app (2026-11-05, 2026-10-26, Lennart) |
| 5 | Delivered-before-midnight filter in place of a fixed gap (SPLIT-10) | departs from the ETA siblings' 1-day gap, **with an evident reason not yet written down** | fugaku (filter only, 2026-11-03, Myunghwan). nyc, pkdd and lusaka use a 1-day gap. |
| 6 | One-day windows on 22-24 October, walking back from the newest (SPLIT-12, SPLIT-14, SPLIT-15, Horizon block) | consistent | SPLIT-15 accepts "a history too short for others". The target count is 3 (above 250k units, SPLIT-33). |
| 7 | 62 acceptances on 25 October kept outside the windows (issue 2, open) | A is **not reasonable under the ranking** now (it breaks SPLIT-15, a Must). B follows precedent. | coffee_rating_prediction and kickstarter cut their partial newest period (2026-11-11, Lennart, cross-dataset item A). lusaka keeps a 70-row partial day inside its last window. |
| 8 | RMSE on raw minutes, fallback (MET-1, MET-8, CLEAN-16) | consistent | lusaka "ok keep minutes", "as the other RMSE-scored ETA datasets" (2026-11-04, Lennart) |
| 9 | Merchant and courier ids as categorical inputs, recurring across windows | consistent | sendy (rider and customer recur, kept) |
| 10 | Licence CC BY-NC 4.0 plus a permission request, kept as a note (EV-4) | consistent | lucas_topsoil (2026-09-23, Lennart). The 11-08 panel called it a "release blocker"; EV-4 makes it a note only. |
| 11 | Not a duplicate of food_delivery_time or the other delivery-time tasks (PROV-4, PROV-7) | consistent | food_delivery_time was retired as AHDS (2026-11-05, Andrej), so it does not compete. meituan_courier_order_acceptance is a different task. |

**Findings**

**F1 (KNOWN, issue 3): the total target departs from every ETA precedent; B follows them**
Every shipped ETA definition counts the target from its prediction point, with the earlier events as inputs:

| Dataset | Prediction point | Target | Earlier events |
|---|---|---|---|
| sendy_logistics_challenge | pickup | seconds from pickup to arrival | placement, confirmation and pickup times are inputs |
| nyc_taxi_trip_duration_1m, pkdd_15_taxi_trip_time_prediction_ii_1m, 2024_lusaka | trip start | trip time from start | none |
| brazilian_ecommerce | purchase | days from purchase | none |
| **meituan (A)** | **acceptance** | **minutes since placement**, elapsed up to 10,293 min | elapsed is an input and also part of the target |

- **Counter-case:** medical_facility_operational_data predicts at check-in. Its target is the delay against the scheduled time, and `minutes_early` is an input (2026-11-05, Lennart). So that target also contains a known offset.
- **What sets medical_facility apart:**
  - It is the source's own target (Crowley et al.).
  - The offset is minutes, not days.
  - Meituan's source defines no target. The total was the AI's proposal (Assessment 2026-11-08: "Exact implementation details remain agent proposals").
- **History:** the 11-08 panel already raised this ("Total target includes a known elapsed component", gamer item 1). The mediator kept the total, which was an AI decision. Myunghwan's quoted words fix only the prediction point. His 11-09 inclusion approval covered the definition as a whole, not the target. So choosing B reverses no explicit curator ruling.
- **Consistency:** B is consistent with precedent. A is a departure with no fact that sets it apart. **USE-5 (Must)**, sendy.
- If B is chosen, the metric CC (RMSE in minutes, 2026-11-09) needs a new look, as the issue's notes say. This is not drift.

**F2 (KNOWN, issue 2): option A now breaks a Must; B follows the cross-dataset precedent**
- Myunghwan approved A on 2026-11-09. SPLIT-15 was amended on 2026-11-10 to require that the newest window is always tested. This is a rule change after the decision, not drift.
- Under the current Must, A cannot stand: no higher-ranked principle overrides it, and the definition errors.
- **B** matches the 2026-11-11 cross-dataset ruling (Lennart, A): coffee_rating_prediction drops its 2 reviews of October 2023, consistent with kickstarter's cut of the last 60 days.
- **C** has a sibling precedent: 2024_lusaka keeps a 70-row partial final day inside its last window. The record measured that this moves RMSE by 0.002. So C is not without precedent. It differs in two ways:
  - lusaka's window ends where the data ends.
  - Meituan's tail would make the newest window 24 h 23 min long.
- **Fact for the curator:** the 62 rows belong to the 24 October source cohort (`dt`). Under B they leave the frame; under C they are scored with their cohort.

**F3 (NEW, minor; Horizon block and splits comment): the no-gap choice needs its distinguishing fact written down**
- **Precedents:** the three closest ETA precedents (nyc 2016, pkdd, 2024_lusaka) all use a 1-day gap, although their delays are minutes to hours. Meituan uses a filter (delivered before midnight) and no gap. That is fugaku's design (2026-11-03, Myunghwan), which is listed as an exception.
- **Distinguishing fact, evident but not written down:** a 1-day gap before the 22 October window would leave training only up to 20 October. That is the 48.7% the Horizon block quotes for 21 October, below SPLIT-14's floor. With 8 days, the gap would cost a window.
- **Under the amended SPLIT-10, measurement decides.** The filter excludes 370/407/423 orders (0.07-0.12%), so any selection of fast orders at the cut is bounded at that share.
- **Wording:** footnote [^x21h4] paraphrases SPLIT-10 as "a gap ... **or** training only on rows whose outcome is known". The rule says both ("with a gap"). The amendment allows no gap only on measurement.
- **Suggested fix:** the splits comment names both facts: the 1-day gap's cost under the floor, and the excluded share. It cites fugaku as the precedent and the taxi/lusaka 1-day gaps as the contrast.
- This follows the amended rule. No reflection prompt is needed. The register's `amendment_due` on SPLIT-10 (11 datasets) should not count this case as a new exception if the measurement is written down.

**F4 (NEW, minor; CLEAN-11 and the 3-hour cap of the ETA family)**
- **Precedent:** lusaka, nyc and pkdd drop trips over 3 hours as "not closed in the app" (CLEAN-11 then CLEAN-15; 2026-11-05 and 2026-10-26, Lennart). Meituan keeps every duration ("Do not clip").
- **Counts from that run, 568,545 labeled orders:**

  | Remaining time after acceptance | Orders | Of which prebooks |
  |---|---|---|
  | over 2 h | 71 | 53 |
  | over 3 h | 42 | 33 |
  | over 6 h | 10 | 8 |
  | max | 652 min | |

- **Prebooks are set apart:** a courier can accept a prebook hours before its slot, so those rows are real.
- **The open part is the 9 non-prebook orders with more than 3 h remaining (2 over 6 h).** They are the same kind of row the family dropped as not closed in the app.
- **Effect:** tiny on row count. Under RMSE each such row adds about as much squared error as about 1,000 typical rows (300² against 8²). That is an estimate, not measured.
- **Recommendation:** add a note to the definition, or a decision item if the curator wants the family's rule applied. Low priority.

**F5 (KNOWN, resolved issue 1; consistency note only)**
- Excluding both forecasts departs from USE-6's default ("dropping it changes the task") and from brazilian_ecommerce.
- **Distinguishing fact, already recorded:** the meal-ready forecast differs across attempts for 8,794 orders, and no issuance timestamps exist (LEAK-10, EV-7). Olist's promise is fixed at checkout.
- The 11-09 Assessment instead names 2_month_survival as the precedent. That precedent rests on the source framing the physician estimate as a comparator. The Meituan source does not frame its promise that way, so 2_month_survival is the weaker analogy. The timing uncertainty is the fact that carries the departure, and curation_comments already says so.
- Reasonable as decided. This is the only exception of its kind, so no amendment is due.

**Doc points from the column audit (not precedent questions, listed for completeness)**
- "district" should read "business area of the accepted waybill" (da_id follows the accepting courier in 1,963 orders).
- "redundant dt" is refuted: dt is the source's cohort date and differs from the local creation date for 1,758 orders.

</details>

<details><summary>Blind review (2026-11-21)</summary>

**Blind review: Meituan food delivery time (`delivery_minutes`)**

**Verdict: include with changes.** It is a real ETA task on real operational data with clear signal. But the target, as built, runs from order creation, so its tail is mostly the already-known wait `elapsed_minutes`. That turns RMSE into a test of copying one column, and the licence forbids redistribution without permission.

**Concerns, most serious first**

**1. The target includes a part that is already known, and that part decides the score**
- `delivery_minutes` is order creation to arrival, and the features describe the moment of acceptance. In the data, `delivery_minutes >= elapsed_minutes` on every row (smallest difference 1.53 min). So the target is `elapsed_minutes` (known) plus the remaining time (the part actually to be predicted).
- Pre-booked orders (3.9%) make up the tail. Their `delivery_minutes` has a median of 80.6, a 90th percentile of 410 and a maximum of 8,208 minutes (5.7 days). Their remaining time, though, has a median of 38.5 and a 90th percentile of 52, just like normal orders. The whole tail is `elapsed_minutes`.
- LightGBM on 3 daily windows (train on the days before; test on 2022-10-22, -23 and -24), using the 200k sample:

| model | RMSE all | R² all | RMSE non-prebook | R² non-prebook |
|---|---|---|---|---|
| mean | 73.0 | 0.00 | 13.6 | -0.19 |
| `elapsed` + median remaining (no learning) | **11.4** | **0.975** | 10.6 | 0.27 |
| linear regression, 4 features | 9.2 | 0.984 | 8.8 | 0.50 |
| LightGBM on `delivery_minutes` | **41.4** | **0.678** | 7.7 | 0.61 |
| LightGBM on remaining time, plus `elapsed` | 8.1 | 0.987 | 7.6 | 0.63 |

- Over the whole set, a rule with no learning beats a tuned GBM by about 4x on RMSE. The GBM loses only because it cannot carry the additive `elapsed` term into the multi-day prebook tail. On normal orders the GBM is the best model. So on this target the method ranking measures extrapolation of one known column across a few hundred extreme rows, not delivery-time prediction. `elapsed_minutes` takes 62% of the GBM's gain importance.
- **Change:** make the target the remaining time, `arrive_time − grab_time`. Keep `elapsed_minutes` as a feature. On that target the GBM reaches R² 0.49 against a median baseline (RMSE 8.1 vs 11.4): real signal, not trivial. If you want to keep the creation-to-arrival framing, at least drop the prebook orders or cap the time to acceptance, and say so.

**2. Licence: redistribution is not allowed without permission**
- License.txt in the repo: "CC BY-NC 4.0 … We reiterate that without permission, the distribution of this dataset to third parties is not allowed, and this dataset is intended for non-commercial use only". It also asks for an acknowledgement ("This research was supported by data provided by Meituan.").
- A benchmark that ships a derived table to users is distributing a derivative. **Change:** get written permission from Meituan, or ship only a loader that points users to the GitHub download. Also record the NC restriction and the acknowledgement.

**3. Feature choice at the prediction point**
- At acceptance the source also has `estimate_arrived_time` (the promised delivery time) and `estimate_meal_prepare_time` (the estimated meal-ready time). Both are known before acceptance, and both are absent here. Dropping the promised time is defensible, because it is Meituan's own ETA model and would turn the task into "correct Meituan's ETA". Dropping the estimated meal-ready time throws away a legitimate, likely strong input: waiting at the restaurant is a large part of delivery time. **Change:** add the estimated meal-ready time as a lead time (minutes from acceptance). I could not measure its value because the column is not in the clean room.
- The courier's current load (orders on hand when accepting) is the main driver in this domain, and it is missing. It can be rebuilt legitimately from earlier accepts by the same courier, but only with the full table and the wave file. This is a known limit, not a defect.

**4. Rows are not independent; check how the split relates to couriers**
- Couriers bundle orders. 154 sample rows share the restaurant, the recipient coordinates, the courier and the acceptance second (one customer's split orders), and their targets differ by a median of 1.5 min. 4,806 couriers appear on a median of 6 of the 8 days, so the same couriers are in train and test. That is fine under a forward-in-time split, because the platform knows its couriers. Within a test day, bundled rows are correlated, which only affects variance.
- Only 8 days (2022-10-17 to 10-24), one city area. The weekly cycle is seen once, so each test window has at most one earlier day of the same weekday.

**5. Smaller data points**
- Coordinates are integer degrees ×1e6, shifted for privacy ("uniformly shifted but not scaled"; supplementary document §2.1). Distances survive, absolute positions do not. Fine.
- `da_id` overlaps geographically ("associated with geographic locations and other factors such as order type", §2.6). It is fine as a categorical, but `poi_id`, `courier_id` and `da_id` are stored as int64 and should be categorical or ID types. Removing the ID columns barely changes the GBM (RMSE on non-prebook rows 7.76 vs 7.73).
- `is_weekend` matches the weekday exactly. Timestamps are on whole seconds. No missing values. The 568,483 rows match the 654,343 waybills minus rejected ones (rejected waybills have zero grab/arrive times, §2.4), which is plausible.
- Among non-prebook rows, 12 have `delivery_minutes` > 180 (max 597) and 57 have `elapsed_minutes` > 60. These are plausible operational outliers; leave them in.
- No training weight is named in `task.md`.

**What I could not check**
- The exact test windows and how the split is cut. I assumed the last 3 days as 3 expanding daily windows.
- Whether `accepted_at` is passed to models as a feature.
- The full 568k rows: I used the 200k sample.
- The preparation code, and whether the waybill rows of re-dispatched orders are handled as I assume (the accepted waybill is kept, with `elapsed` measured from order creation).
- The value of the dropped estimate columns.
- The 2025 data paper (5.7 MB PDF), which I did not read. I did read the 2024 background document and the October 2024 supplementary document.

I opened no files outside the clean room except the allowed Python interpreter.

Scripts and logs: `work/baseline.py`, `work/1401930.log`. Source copies: `work/src/`.

</details>

<details><summary>Task gamer (2026-11-21)</summary>

**Task gamer: meituan_food_delivery_time (saved by the main session from the agent's hand-back; content verbatim in substance)**

Setup: 3 one-day test windows (22, 23, 24 Oct 2022), all earlier days train; untuned LightGBM (500 trees, lr 0.05, 63 leaves), all rows. "Honest" = LightGBM on remaining time (target - elapsed, elapsed added back) + hour, two distances, courier past (gap since previous accept, same shop as previous, accepts in past 30/60 min). "Honest+src" = honest + promised time and meal-ready estimate (relative to order and acceptance). Noise (random column): +0.01..+0.03 on honest; -1.9..+2.1 on raw target.

**Exploits (RMSE r2/r1/r0 = 22/23/24 Oct)**
| # | Exploit | Honest | Exploited | Gain | Deployed model has it? |
|---|---|---|---|---|---|
| 1 | Courier's future within the test day: time to next and second-next accept, accepts in next 30/60 min, next order same shop, distance from next-assignment position to this recipient and shop | 7.715/8.286/7.454 | 7.065/7.610/6.756 | 0.65/0.68/0.70 | No |
| 1a | timing only | same | 7.301/7.891/7.013 | ~0.4 | No |
| 1b | next-assignment location only | same | 7.524/8.077/7.228 | ~0.2 | No |
| 1c | 1 on top of honest+src | 6.972/7.526/6.826 | 6.338/6.926/6.176 | 0.63/0.60/0.65 | No |
| 2 | counts over train+test (per shop/courier/courier-day/address) | 7.715/8.286/7.454 | 7.673/8.255/7.369 | 0.04/0.03/0.09 (noise) | courier-day count no; harmless |
| ref | fetch time (post-acceptance, correctly excluded) | | 6.314/6.830/6.183 | 1.3-1.5 | No |

Fix for 1: none clean (no column drop removes it without the legitimate courier history). Options untested: coarsen accepted_at in test rows (e.g. 15 min); accept and document as a property of a batch test set with entity ids; sequential scoring (benchmark cannot).

**Flaws hurting an honest model**
| # | Flaw | Baseline | Honest choice |
|---|---|---|---|
| A | Target from order creation contains known elapsed (tail to 10,293 min, prebooks); trees cannot extrapolate. 484-638 rows/test day (<1%) carry 95-97% of target variance | untuned LGBM raw target 74.51/51.11/58.58 | same on remaining time 8.99/9.90/8.56; rule elapsed+median remaining 11.19/11.71/10.73 |
| B | Promised delivery time (estimate_arrived_time) and meal-ready estimate (estimate_meal_prepare_time), set before acceptance, are dropped | honest 7.715/8.286/7.454 | honest+src 6.972/7.526/6.826 (gain 0.63-0.76) |
Fix A: target = arrive - grab (or drop prebooks, unmeasured). Dropping train rows with remaining >180 min: no change.

**Found nothing**
Tied-second order (-0.008..-0.006, noise); number formats (all whole seconds); 2 full-feature duplicates, no cross-split copies; no training rows after the split (370-423 late-label rows correctly left out; small selection effect, last training hour mean 24.5-25.6 vs 26.6-27.6 a day earlier); no transforms over all rows; no weight. Source lookup works (all 568,483 rows match) — not a flaw of the task. Web: no prediction leaderboard, no leak threads.

Not checked: prebooks-dropped variant; coarsening accepted_at; dispatch-time tables (courier load); tuned models.
Files: this folder: prep.py, fit.py, 1401931.log, 14019*.log, src/.

</details>

<details><summary>Column audit (2026-11-21)</summary>

**meituan column audit — built data; 2 issues (62-row tail breaks newest-window guard; total target vs remaining); facts hold**
Doc fixes: task_summary.known "district" -> "business area of the accepted waybill"; curation_comments 3rd bullet + da_id note (follows accepting courier in 1,963 orders where it changes); "redundant dt" -> "dt (the source's cohort date; it differs from the local creation date for 1,758 orders)"; optional grab position match note (median 35 m within 30 s of dispatch snapshot).

</details>

<details><summary>Mediator</summary>

**Independent mediator**

Verdict: ship after changes, conditional on the curator's forecast-retention decision and completion of final native verification. This is an AI recommendation, not human acceptance. This report records the initial mediation; the completion addendum below supersedes its pending-verification statement.

Validity: USE-1/3/5/6 support the acceptance-time ETA task and explicit total-duration target. Forecast snapshot availability remains cannot-verify under USE-3/6, LEAK-10 and EV-7; no post-acceptance revision demonstrated. Actual splits satisfy SPLIT-1/9/14 and the label-availability intent of SPLIT-10.

Value: meaningful residual signal survives appropriate baselines and forecast removal. TP-4 supplies no Trivial finding. Initial mediation's native task review was pending; bounded LightGBM experiments are not the benchmark's tuned methods.

Quality: cleaning and semantic types appropriate. Qualify short-summary forecast wording. One unused-row warning is explained; acceptance register empty. Weighed: first-party operational source and substantial sample favor inclusion; eight days, one city and unverified forecasts limit claims. One unresolved human question.

**Routine changes**

1. Qualify task_summary.known and fit_reason (USE-3/6, LEAK-10, EV-7). Say the accepted attempt's recorded promise and meal-ready forecast have unverified snapshot timing relative to acceptance; retention assumes available by acceptance, with no issuance/revision timestamps supplied. Regenerate README. Do not describe uncertainty as resolved or automatically change direct fit.
2. Present proper baseline context and scope (TP-4, EV-2/8/9). Retain total target and minute errors. Known elapsed explains substantial variance; high total R2 is not evidence of predicting future uncertainty.

| Test day | Promise RMSE | Elapsed plus training mean remaining | Full residual model, two seeds |
|---|---:|---:|---:|
| Oct 24 | 12.141 | 10.680 | 7.159-7.181 |
| Oct 23 | 11.787 | 11.494 | 7.925-7.930 |
| Oct 22 | 11.755 | 11.014 | 7.525-7.538 |

Full-row, three-window, bounded 500-tree LightGBM results. Without forecasts: 8.403-9.527; without entity IDs: 7.498-8.461. Sensitivity is not issuance-time or leakage verification.

3. Finish and inspect final native task verification (TP-1, EV-3/7/8). At initial mediator inspection the final log/JSON were unavailable. Historical partial-Oct 25 output cannot close this check. Review final flags with their actual scope and stronger evidence; routine work, not human choice.
4. Explain unused-row warning without inventing acceptance (EV-3/7). Zero errors, one splits_rows_unused warning, one conflicting-duplicate info. Precisely 62 Oct 25 acceptances remain outside complete-day windows. Keep explanation and empty acceptance register visible. Distinct historical orders sharing inputs lie together in training; no cross-split copies.

**Human issue: retain recorded forecasts under unverified acceptance-time availability?**

The question concerns stored-snapshot provenance, not forecast meaning. Source documents describe a promise and predicted meal readiness without locating issuance/revision of accepted-row versions.

Advocate: timely forecasts are legitimate inputs under USE-6; promise invariant across attempts; changed rejected-attempt estimates precede eventual acceptance; no late accepted snapshot is demonstrated. Removing a legitimate company estimate changes the task.

Critic: meal-ready forecasts vary across 8,794 orders, accepted snapshots lack issuance history, and short summaries originally overstated availability. Forecast block materially improves prediction, so uncertainty remains prominent.

USE-3/6 are Must rules at P3; LEAK-10 Must at P4. EV-2/7 prevent treating source terminology or ablation as timing verification. No established Must violation exists to override; value cannot excuse one later found. Remedy ladder: recover timely snapshots or mask identifiable late cells, then drop inseparable unavailable field while preserving real task under USE-12.

Exact question: Accept retaining the recorded forecasts with this explicit availability uncertainty, or require logging evidence or qualification of an alternative without the unresolved fields before acceptance?

Factual resolution requires issuance/version history or an authoritative account of accepted-row snapshot meaning. More predictive ablations cannot settle it. An alternative without unresolved fields needs an explicit choice and qualification; the completed combined ablation is not authority to silently replace the definition.

**Agreed facts and reconciliation**

- Target is (arrival-placement)/60; elapsed is (acceptance-placement)/60. Subtracting known elapsed from both target and prediction leaves errors identical, although separately trained learners differ. Blind alternative of total framing plus baselines is satisfied; no target change follows from TP-6.
- 654,343 attempts, 568,546 orders each with one accepted attempt; 568,545 labels after one absent arrival; all 22,181 prebooks retained.
- Oct 24/23/22 trains 500,764/423,008/345,355, tests 67,349/77,719/77,637. Independently reconstructed memberships identical. Exclude 370/407/423 unavailable labels, zero remain; smallest train fraction 60.744%.
- Recurrence matches future operations under USE-10 and SPLIT-1/3/13, not cold-start/season/city claims.
- Definition supplies categorical IDs/flags, UTC+8, shifted-coordinate notes and temporary arrival removed before modeling. Blind omissions resolved by actual implementation under EV-2.
- Corrected date prose supersedes earlier audit wording findings. Record distinguishes acceptance task from historical creation/dispatch screening.
- Gamer confirmed zero exploits: row-order attack maps to LEAK-10/SPLIT-22 and failed; copy lookup maps to LEAK-16-21 and found none; label attack maps to LEAK-12/SPLIT-9/10 and found zero unavailable labels under correct interpretation. Residual learning is legitimate USE-6 use, not exploit. No measured attack contradicts an accepted warning or potential-leak note.
- Licence belongs release checklist under EV-4, not scientific verdict or human issue list.
- No extra mediator experiment required: independent membership tests and algebra settle accessible disputes; unavailable logging cannot be recovered with another fit.

**Precedents**

Olist supports retaining timely company promises but does not establish Meituan snapshot timing. Medical-facility elapsed-time precedent supports known elapsed inputs. ETA boundaries support measured maturity restrictions rather than copying another task's fixed gap. No rule amendment, exception or matching-precedent departure established. Provenance choice remains human.

Initially reviewed definition SHA 256 a768b61b5c5fbd7c2c385030318a76849df2fe829a219a05bbad86e10d1b75b7. Mediator changed no files, records, claims, scientific decisions or acceptance state.

**Completion addendum**

The routine documentation and verification work is resolved. Inspected updated definition SHA 256 77389f3f2763fbc124928da949e92280dc9f586801ec7ca54fe7cb8353d9112a and regenerated README: both summaries qualify forecast availability, download is commit-pinned, and operational-baseline table supplies the agreed interpretation. No target, feature or split change warranted.

Final native task probes completed all three corrected splits, 568545 rows, 17 features, no flags. The linear model reported RMSE 8.435 minutes and beats the constant baseline on every split. Untuned results complement residual experiments; high total R2 alone is not evidence of future-uncertainty resolution. No extra model rerun needed.

62-row unused-tail warning remains, accepted register empty. Transparent pending warning bookkeeping, not separate scientific question. Recommendation ship after changes, routine changes complete, one remaining human decision: accept recorded forecasts with explicit availability uncertainty, or require logging evidence/qualification without unresolved fields before acceptance? Neither timing safety nor leakage established. No human acceptance applied; mediator edited no files.


</details>

<details><summary>Claim audit</summary>

**Independent claim audit: Meituan delivery time**

Verdict: ready with noted concerns, subject to the panel and curator. No proven feature leak or split failure found. Forecast availability at acceptance remains unverified. Two date descriptions need small wording corrections. The old screening use case is historical, and must not be mistaken for the current acceptance-time task.

Validity: USE-1 and USE-5 hold for the specified accepted-order ETA update; the source supports the field meanings. USE-3/USE-6 are untested for the exact forecast snapshots. SPLIT-9/10 hold in all three current folds. Value: RMSE fallback is supported by the source search and computable on all three folds (MET-1/2/3). Promise and elapsed baselines are materially stronger than a mean predictor. Quality: cleaning and dtype claims hold; date prose needs correction. Scientific acceptance and screening approval are not applied by this review.

This initial audit examined an earlier definition, its generated README and the historical curation record. Subsequent corrections and final verification are documented in the mediator completion addendum.

Evidence shorthand:

- D: current definition and generated README in `datasets/_dev/tabarena-v0pt2/meituan_food_delivery_time/`.
- R: `curation/records/meituan_food_delivery_time.md`.
- E: independently computed `claims-evidence.json` and reproducible `claims_audit.py`.
- B/S/P: cached primary-source text in the published background, supplement and paper. These are source statements, not our measurements. B: March 2024 background Sample Question 4 and Tables 1-2. S: October 2024 supplement sections 2.2-2.5. P: Wang et al. 2025 section 3.1, appendices A.1-A.2 and introduction.

| Claim (exact phrase, or separately identified implied claim) | Source | Cheapest refutation test run | Result and evidence | Rule |
|---|---|---|---|---|
| "The delivery platform updates the customer's ETA when a courier accepts the order" | D summary use_case | Compare actor, event and decision against lifecycle and source timing question | Holds as the curated use case. B Sample Question 4 explicitly proposes prediction of pickup/delivery timings; P describes acceptance before pickup and delivery. The exact midnight refit and acceptance-time update are our task design, not a source-prescribed experiment. | USE-1/3 |
| "How many minutes after placement will this accepted food order reach the customer?" and "Total minutes from order placement to delivery, including the time already elapsed at acceptance" | D summary question/predicted | Recompute target from raw arrive minus placement, and test remaining time | Holds: explicit formula is seconds divided by 60; all labeled rows have nonnegative elapsed and remaining durations. Total median 28.5 minutes, maximum 10,336.483. Remaining time is still unknown at acceptance. | USE-5, MET-3 |
| "One accepted food order in an anonymized Chinese city, October 17-24, 2022, including prebooked orders" | D summary row, README | Count unique accepted orders and actual timestamp dates | Partly refuted: uniqueness and prebooks hold, city/anonymization are source-described. Acceptance dates include 62 rows on October 25; placement dates extend back to October 11. Oct 17-24 is the release's nominal day range, not either timestamp's literal range. | PROV-12, EV-2/7 |
| "Acceptance time, elapsed order and dispatch times, merchant and courier, district, pickup and destination coordinates, courier coordinates at acceptance ... and the prebook flag" | D summary known | Compare feature formulas and source lifecycle/dictionary | Holds for these nonforecast fields: P section 3.1 locates grab coordinates at acceptance; assignment precedes acceptance. IDs and flags are source order/assignment fields. No future fetch or arrival feature ships. | USE-3, LEAK-10 |
| "the platform's promise and meal-ready estimate" are known at prediction | D summary known/fit_reason; implied availability | Read S/P and compare forecasts among attempts sharing an order | Untested for snapshot timing. P says forecasts are associated with order ID; S says meal time is estimated readiness. Neither states the stored revision existed at acceptance. Promise has 0 varying orders across attempts; meal estimate varies for 8,794 orders. This discrepancy refutes literal invariance of the meal estimate across waybills, not availability of the accepted attempt's value. No proven leak. | USE-3/6, EV-2/6/7 |
| "Three future acceptance days, October 22-24. Each midnight refit trains on earlier accepted orders whose delivery was already recorded. Merchants and couriers can recur" | D summary split | Inspect every actual fold, reconstruct delivery time independently from shipped total minus elapsed, and count recurring IDs | Holds. Train/test sizes Oct 24 500,764/67,349; Oct 23 423,008/77,719; Oct 22 345,355/77,637. Latest training delivery on preceding day 23:59:47, 23:59:53 and 23:59:56 respectively. Seen merchants 99.79%-99.85%, couriers 98.52%-99.10%. | SPLIT-9/10/13 |
| "Select accepted waybills, omit one absent delivery label" | D summary changes | Raw counts, accepted-per-order check, filter replay | Holds: 654,343 attempts, 568,546 orders and accepted attempts; exactly one accepted attempt for every raw order. Exactly one accepted arrival equals zero. 568,545 labeled rows remain. | PROV-12, CLEAN-1 |
| "fit=direct"; "The challenge names pickup and delivery timing prediction" | D summary fit/reason | Read source question and task identity | Source timing question holds (B Sample Question 4). Direct fit is conditional on the still-unverified forecast snapshot assumption, and is an advisory judgment rather than a measured guarantee. No evidence supports declaring the task invalid. | USE-8, EV-7 |
| "Eight days in one city limit generalization" | D summary fit_reason, notes | Source scope, count recurring entities and test date ranges | Holds as a limitation: one short nominal release, only three consecutive test days, nearly all test merchants/couriers seen. No test of unseen cities or seasons is possible here. | SPLIT-1/13/18 |
| "Prebooked orders can have long known waits before acceptance" | D summary fit_reason | Count prebooks and long elapsed inputs | Holds: 22,181 prebooked rows retained; 180 labeled orders have more than 1,440 elapsed minutes before acceptance; no duration cutoff applied. The claim says can, not that every prebook has a long wait. | USE-5/6 |
| "Rejected attempts have structural zero event times" | D notes | Inspect rejected grab/fetch/arrival timestamps and grab coordinates | Holds: zero nonzero entries for all five tested fields among rejected attempts; S section 2.4 explicitly documents this convention. | PROV-12, CLEAN-4 |
| "Do not clip or log unusual durations or discard prebooked orders"; "No target-based duration filtering" | D notes | Replay row filter, inspect target formula and prebook counts | Holds: filter is accepted flag and positive arrival only; raw total duration is divided by 60 without clipping/logging. | CLEAN-1, MET-3 |
| "The latter places grab_lat and grab_lng at acceptance, correcting the earlier assignment description" | D notes | Compare B dictionary to P section 3.1 and Table A.2 | Holds as a source revision: P says courier position at order acceptance, B describes assignment. Source correction supports retention at the chosen prediction point. | PROV-13, USE-3 |
| "Coordinates stay in the source's shifted integer units; no external geocoding or spatial matching" | D notes | Inspect column selection, transformations, final dtypes and source correction | Holds in this definition: six coordinate columns copied and remain int 64. S section 2.1 describes uniform shifting, no scaling. No join or external coordinate transformation occurs. | PROV-12, CLEAN-1 |
| "estimate_arrived_time is the platform's promised arrival; estimate_meal_prepare_time is predicted meal readiness, not observed completion" | D notes | Read corrected source field meanings | Holds as source-described semantics: P section 3.1 calls the first promised delivery and the second predicted readiness; S section 2.5 corrects the older completion wording. This does not verify revision timing. | USE-6, PROV-13 |
| "These are order-level forecasts in the source"; "Exact forecast revision history is unavailable" | D notes | Compare P's order-associated statement with raw per-order variation | Source attribution holds. Treat "order-level" as associated with an order, not invariant: 8,794 orders have varying meal estimates. Revision history unverified; neither our data nor consulted documents recover it. | EV-2/7 |
| "Structural zero meal-ready estimates become missing" | D notes | Count missing transformed values and raw zero convention | Holds: 9,874 meal-ready missing values. Also one zero dispatch time becomes missing; formula correctly prevents a 1970-derived duration. | CLEAN-4 |
| "Compare with elapsed-only and promise baselines, not only a constant mean" | D notes | Score all three baselines on all three folds via library scorer | Holds as necessary context, now executed independently: table below. Promise RMSE around 12 minutes compared with mean 72-93 minutes. This does not prove triviality without the model comparison. | TP-4, EV-1/8/9 |
| "Drop CSV index, order and waybill IDs, redundant dt, acceptance indicator and future fetch time" | D notes | Inspect shipped columns | Holds: none ship. Final frame has 17 features plus target. | LEAK-10, CLEAN-6 |
| "Arrival time is used solely to exclude unavailable training labels, then dropped before modeling" | D notes | Inspect clean, split and output columns | Holds in intended predictor sense: delivered_at is removed by SplitPlan; arrival also necessarily constructs the target and excludes its one absent label. No arrival or delivered_at predictor ships. | LEAK-10, SPLIT-10 |
| "Merchant, courier and district IDs stay categorical" | D notes | Inspect container dtypes | Holds: poi_id, courier_id and da_id are category. is_prebook and recomputed is_weekend are also categorical; accepted_at is datetime. | CLEAN-2/6 |
| "No full-wave membership, wave ends or future aggregates enter" | D notes; implied no all-row fitting | Inspect data recipe and retained columns | Holds: only the raw waybill table is read, no wave fields or fitted full-row statistics are used. | LEAK-10/27 |
| "Convert Unix timestamps to naive China local time (UTC+8). Recompute weekend from acceptance time ... Keep one acceptance datetime and elapsed durations" | D notes | Inspect formulas and final dtypes | Holds mechanically: +8 hours and naive datetime 64[ns]; derived weekend from accepted_at. Source geography supports China-time interpretation; the formula is explicit rather than an unexplained inferred time axis. | CLEAN-1, SPLIT-9 |
| "The 62 acceptances after midnight October 25 stay in the frame but outside the three complete-day test windows" | D notes | Count dates and every test range | Holds: 62 Oct 25 rows and zero in any train/test; matches generated unused-row warning. These rows are not a partial 62-row evaluation fold. | SPLIT-9/18 |
| "Supporting dispatch snapshots cover only three noon checkpoints daily, not continuous workload. Completed waves contain future information and the supplement documents a wave-start indexing defect; no joins used" | D notes | Read P introduction/3.2 and S 2.2/2.3; inspect loader | Holds as source-described limitation and current code behavior. No dispatch/wave table was independently downloaded/recounted in this audit; no join occurs. | LEAK-10, EV-2 |
| "Daily midnight refits predict the next acceptance day's orders, newest window first"; "Each train side holds at least half of all labeled rows" | D splits_comment | Fold ordering, minimum train count and independent reconstructed label times | Holds: newest-to-oldest Oct 24/23/22, min train 345,355 > 568,545/2. Labels unavailable at midnight excluded: 370/407/423 respectively. | SPLIT-9/10 |
| "Use October 22-24, the final three local acceptance days" | D splits_comment | Actual acceptance day counts | Refuted wording: October 25 also has 62 acceptances. Mild fix: "the final three complete local acceptance days" and retain existing tail note. | EV-2/7 |
| "Cadence and window count follow the eight-day operational release, not model scores" | D splits_comment | Read explicit cutoffs and definition; compare source scope | Holds as declared design rationale; cutoffs are fixed, no score-driven selection code. Authorship motivation cannot be independently proven from the final code alone. | SPLIT-1/18 |
| "metric = Metric.fallback(...)"; "describe timing prediction but prescribe no single predictive scoring metric" | D metric, README metric block, R screening metric | Search and read B Sample Questions/full dictionary, S corrections, P operational paper; resolve scorer and score each fold | Holds for consulted source texts. B's operational distance/delay objectives are not a prescribed predictive leaderboard metric. No unique predictive model-selection metric is specified. Resolved rmse needs no scoring columns, row unit exists, raw minutes scale is identity, all test folds score finitely. No official RMSE claim is made. | MET-1/2/3/8/11 |
| Implied: no order is copied across a split | D recipe and temporal split | Global unique accepted order check plus cross-split full feature-row hash overlap | Holds for exact copies: unique accepted order per raw order; zero feature hashes shared between train/test in every fold. Two feature-identical rows exist in the complete frame, with conflicting labels, but do not cross these splits. This check does not establish absence of every semantic near-duplicate. | LEAK-16/21, EV-7 |
| R screening: "when an order is placed or dispatched"; "grab ... courier position come after the prediction point ... drop" | Historical R comments | Compare with final acceptance task and newer source correction | Refuted as a description of the current definition; remains a legitimate record of an earlier proposed task. Mild remedy is a new add-stage assessment explaining the prediction-point change, preserving the dated screening history. | USE-3, EV-2 |
| R screening: "568,546 real Meituan food orders"; attempts, source timing question, promise legitimacy and short windows | Historical R comments | Raw count and primary source checks above | Counts and source descriptions hold; actual labeled dataset is one row smaller. Forecast timing remains unverified rather than categorically legitimate. | PROV-12, USE-6 |
| R external sibling/duplicate judgments and "External collections: none found" | Historical R comments | No independent sibling dataset search or collection comparison in this bounded audit | Untested; not used as positive proof of this definition's uniqueness. Parent panel/provenance review must assess if needed. | PROV-4/7, EV-7 |
| R "priority 4", gap/shape/source factors and comparison to 45,451-row external dataset | Historical R comments | Raw shape/source checked; no new coverage/external dataset audit | Shape and first-party source hold; priority and external-data factual comparisons remain untested here. They are screening assessments, not acceptance evidence. | EV-4/7 |
| ZIP SHA 256 in download_description | D metadata | Independently hash cached downloaded ZIP | Holds: `38b51431a12dd7e73deb4fc750b1275067fbc29cfce2c4b4492339738c988ce2`. Live redownload, public repository creation date, licence and citation authors were not independently reverified in this role. No provenance claim beyond cached bytes is inferred. | PROV-12, EV-7 |

Independent scorer results, RMSE in minutes (not trained models):

| Test acceptance day | Rows | Train-mean prediction | Known elapsed minutes | Platform promise |
|---|---:|---:|---:|---:|
| 2022-10-24 | 67,349 | 82.310 | 27.471 | 12.141 |
| 2022-10-23 | 77,719 | 71.900 | 28.894 | 11.787 |
| 2022-10-22 | 77,637 | 93.108 | 28.234 | 11.755 |

Ranked remaining matters and mildest remedies:

1. **Untested prediction-time forecast snapshots (P3/P4, USE-3/6, EV-7).** Forecast meaning is source-supported; retention is reasonable but not proven safe by that meaning. Across-attempt variation establishes that meal-ready values are not a single immutable order constant. It does not establish a post-acceptance revision or target-derived field. Preserve an explicit uncertainty in REVIEW and seek logging/version evidence before upgrading availability to verified. The parent may compare models with/without these fields as sensitivity evidence, but scores cannot establish timestamp provenance. No automatic drop or exclusion is justified by the current evidence.
2. **Refuted timestamp-range wording (P5 documentation).** Revise summary row to call Oct 17-24 nominal release dates and mention next-day acceptance tail; revise "final three local acceptance days" to "final three complete local acceptance days". Data/splits already implement the right windows and disclose the tail.
3. **Historical record differs from final task (P3 documentation).** Add the current acceptance-time framing and correction provenance in a new assessment when the parent applies its authorized record update. Preserve the AI-unverified screening history and the separate approval state.
4. **Untested broader uniqueness, source metadata and final task-probe ranking.** This role did not search every external sibling, redownload the source, audit licensing text, or run tuned model comparisons. Existing task/leak outputs may be used by the parent with their exact current split scope. The leak probe's daily-count warning on Oct 25 describes the retained partial tail; the actual tested windows exclude it. The cached check log reports 0 errors, 1 unused-row warning (62 rows), 1 conflicting-duplicate info. Those are parent-run checks, not a claim that this role reran `dataset check`.

No recommendations to exclude the dataset. Human review is still required; none of these findings is a reservation/ownership claim, and this report does not update a record or accept a screening decision.


</details>

<details><summary>Column audit</summary>

**Independent column audit: Meituan food delivery time**

Reviewed 2026-11-08. Definition: `datasets/_dev/tabarena-v0pt2/meituan_food_delivery_time/dataset.py`, SHA 256 `2367a2d99a669858125f4008c5220ca24da4340485cc3a925aec273909258f60`, in the supplied add-dataset checkout. No scientific or repository edits. This report and dtype-probe outputs are the only audit artifacts written.

Prediction point: immediately after courier acceptance; target is total placement-to-delivery minutes, including elapsed time. This is a coherent ETA update. Review follows P3/P4/P7, USE-1/3/6, LEAK-1/2/3/6/10/12 and CLEAN-3/9/10/11/14/15. Sources inspected: local `20261107_meituan_screen_review/background.txt` Tables 1–2; `supplement.txt` sections 2.1, 2.3–2.6; `paper.txt` section 3.1 and Appendix A. These distinguish forecast target timestamps from forecast issuance timestamps. The latter are unavailable.

Loaded the final split-plan frame via `dataset_io.from_definition(..., raw=True)`: 654,343 raw attempts, 568,545 labeled accepted orders, 17 inputs plus target. `delivered_at` is absent from the final frame. The prescribed dtype probe reports three count-like flags, all rejected below using the source's identifier meanings. No confirmed leakage or cleaning defect was found. One timing/documentation question remains; it is not a demonstrated leak.

**Retained columns**

| Column | Meaning from source | Known at acceptance? | Dtype / cleaning | Verdict; rule |
|---|---|---|---|---|
| `poi_id` | Anonymized merchant identifier | Yes, order's merchant | category; 4,962 values; zero is valid ID | Fine. Count-like probe flag is false: codes identify merchants, not counts. CLEAN-3/14. |
| `courier_id` | Courier assigned to the accepted waybill | Yes, assigned and accepting courier | category; 4,901 values; zero is valid ID | Fine. Count-like flag refuted by codebook. Recurrent couriers are consistent with temporal use case. CLEAN-3/14; USE-10. |
| `da_id` | Operating area code, associated with geography and order type; areas can overlap | Yes, accepted attempt's dispatch area | category; all 23 codes 0–22 | Fine. Count-like flag refuted. Do not interpret as ordinal distance or count. Supplement 2.6; CLEAN-14. |
| `is_prebook` | Advance scheduled order flag | Yes, specified at order creation | category, exactly 0/1; 22,181 prebooked labeled orders | Fine; essential context for long elapsed and total times. CLEAN-14; USE-6. |
| `sender_lng` | Shifted merchant longitude | Yes, pickup location | int 64 numerical coordinate, no zero or missing in retained rows | Fine; preserve relative source geometry. Uniform shift prevents treating absolute values as real-world degrees without undoing anonymization. CLEAN-2/14. |
| `sender_lat` | Shifted merchant latitude | Yes | int 64 numerical coordinate, no zero/missing | Fine; CLEAN-2/14. |
| `recipient_lng` | Shifted specified destination longitude | Yes, destination of accepted order | int 64 numerical coordinate, no zero/missing | Fine; source destination, not measured courier endpoint. CLEAN-14; LEAK-10. |
| `recipient_lat` | Shifted specified destination latitude | Yes | int 64 numerical coordinate, no zero/missing | Fine; CLEAN-14; LEAK-10. |
| `grab_lng` | Courier longitude at acceptance | Yes, paper section 3.1 corrects earlier assignment wording | int 64 numeric; all structural rejected-attempt zeros disappear with accepted selection | Fine. No future endpoint. CLEAN-10/14; LEAK-10. |
| `grab_lat` | Courier latitude at acceptance | Yes, same source clarification | int 64 numeric, no retained zero/missing | Fine; CLEAN-10/14; LEAK-10. |
| `accepted_at` | `grab_time`, converted from Unix seconds to naive China local time | Exactly the prediction point | datetime 64[ns], UTC+8; 2022-10-17 00:01:00 through 2022-10-25 00:23:29 | Fine; genuine datetime, also temporal key. CLEAN-14. |
| `is_weekend` | Acceptance-day weekend flag | Yes, deterministic from acceptance clock | category, exactly 0/1; recomputed instead of copying original order-date flag | Fine. Recalculation changes 704 retained rows, consistent with a different event date. It is derivable from accepted_at, not an exact copied column. CLEAN-14; USE-3. |
| `elapsed_minutes` | `(grab_time-platform_order_time)/60` | Yes, elapsed time already observed | float 64, no missing; 0.05–10,293.47 minutes | Fine. A known part of total target is legitimate here, not a leak. Do not reject solely for target correlation. USE-6; LEAK-10. |
| `promised_minutes` | `(estimate_arrived_time-platform_order_time)/60`, platform promise relative to placement | Source calls it a promise, supported as order input | float 64; no zero/missing source forecasts; range 30–10,346.07 minutes | Fine with revision-history limit documented. All 568,546 order IDs have a single promised timestamp across attempts; all labeled promises meet source minimum of 30 minutes. USE-6. |
| `meal_ready_in_minutes` | Predicted readiness minus acceptance timestamp | Plausible attempt-time forecast; exact issuance/revision timing unverified | float 64; 9,874 zero-coded source forecasts correctly become NaN; range −10,283.12 to 35.52 minutes | Question, not confirmed leak. Negative values mean forecast readiness is already past; positive values are expected future forecast dates, not evidence of late issuance. See issue 1. USE-3/6; LEAK-6/10; CLEAN-10/11/14. |
| `dispatch_to_accept_minutes` | Elapsed time since dispatch of the accepted waybill | Yes; both events have happened | float 64; one structural zero dispatch timestamp masked; other values 0–319.77 minutes | Fine. Supplement's checkpoint reinterpretation concerns the two separate assignment-input files, not this waybill table. CLEAN-10/14; USE-3. |
| `push_to_accept_minutes` | Elapsed time since this order entered dispatch | Yes | float 64, no missing/zero source timestamp; 0.0167–10,293.12 minutes | Fine. Long durations are possible for advance orders and retries; no target-based clipping. CLEAN-11/14; USE-6. |
| `delivery_minutes` | `(arrive_time-platform_order_time)/60` | Future outcome; target only | float 64 minutes; one missing accepted arrival removed; 1.97–10,336.48 minutes | Fine. No label filtering by duration. Prebooked elapsed waits explain the largest values. CLEAN-15; USE-5. |

**Dropped fields and temporary metadata**

| Raw / temporary column | Semantics and timing | Treatment / verdict |
|---|---|---|
| `Unnamed: 0` | CSV storage row index | Dropped correctly, CLEAN-3. |
| `order_id` | Identity joining attempts of an order | Used to assert unique accepted rows, then dropped correctly; CLEAN-3, LEAK-17. Exactly one accepted attempt per raw order. Zero is an ordinary ID, not missing. |
| `waybill_id` | Dispatch-attempt identity | Dropped correctly, CLEAN-3. |
| `dt` | Source's stated creation-date partition | Dropped. It disagrees with UTC+8 platform-order date in 1,758 retained rows, so deriving event clocks from timestamps avoids treating this partition as an exact timestamp. No need to repair a discarded column. CLEAN-3/12/14. |
| raw `is_weekend` | Source's order-date weekend indicator | Replaced by acceptance-date version; source field is available earlier and is no leak. No problem in chosen derivation. |
| `is_courier_grabbed` | Whether attempt accepted | Cohort selection, then constant and dropped correctly. Accepted-only ETA update conditions on an event already observed. USE-1/3; CLEAN-5. |
| `platform_order_time` | Actual placement time | Used in elapsed duration, promise duration and label; dropped raw timestamp. No future information in elapsed calculation. |
| `order_push_time` | Actual entry into dispatch | Replaced by push-to-accept duration; all positive. Fine. |
| `dispatch_time` | Actual waybill assignment, with one absent zero among labeled orders | Replaced by duration with missing retained correctly. Fine. |
| `grab_time` | Actual acceptance | Replaced by datetime and time differences. All positive in retained data. Fine. |
| `estimate_arrived_time` | Platform promised arrival | Replaced by promised duration; not realized arrival. Fine. |
| `estimate_meal_prepare_time` | Forecast readiness, corrected by supplement 2.5 | Replaced by forecast-minus-acceptance duration, zeros masked. Question in issue 1 applies to underlying forecast as well. |
| `fetch_time` | Actual food pickup, after acceptance | Dropped correctly; unavailable at prediction and would leak, LEAK-10 Must. |
| `arrive_time` | Actual completed delivery | Used only for target and training-label availability, never input. Fine. |
| `delivered_at` | Temporary datetime from arrival | Used to exclude labels unavailable at midnight refits, then dropped by `_make_splits`. Verified absent from model frame. Fine; LEAK-12 Must. |

**Cross-checks and ranked findings**

Positive event times satisfy placement ≤ push ≤ dispatch ≤ acceptance ≤ pickup ≤ arrival in every labeled retained row; the sole zero dispatch is excluded from the corresponding inequality test and masked. No coordinate zero survives accepted selection. No positive meal-ready forecast precedes order creation. There are 102,093 negative nonmissing meal-ready-minus-acceptance values; those are not impossible readiness estimates. Meal forecast equals observed pickup on only 541 rows and is later than pickup on 251,255 rows; treating it as actual meal completion is refuted by both the supplement and observations. Max total minutes are 645.42 for on-demand orders and 10,336.48 for prebooked orders, so the latter explain the seven-day maximum without target edits.

1. **Medium, open timing question / correct factual wording (P3/P4; USE-3, USE-6; LEAK-6/10).** The definition describes the forecasts as order-level and says inputs describe the order by acceptance. The promise is constant per order, but the meal estimate is not. There are 8,794 orders with differing meal-ready values across attempts; after ignoring zero values, 8,174 orders have more than one positive forecast. Sorting positive attempts by dispatch time then waybill ID yields 8,181 changed rows: 2,490 rejected and 5,691 accepted. Every changed rejected row was dispatched before its order's eventual acceptance; the median forecast change is −720 seconds (range −2,100 to +823). These observations show attempt-specific forecast revisions can occur before acceptance and refute the claim that every order has a fixed meal forecast. They do **not** show the accepted row was updated after acceptance or outcome. Source text says this is a platform prediction and the supplement associates it with the waybill; it supplies no forecast issuance history. Mildest remedy: describe it as the meal-ready forecast recorded on the accepted attempt, preserve the timing uncertainty explicitly, and avoid claiming uniqueness or verified issuance time. If later evidence establishes late revisions, restore the snapshot available by acceptance or mask the locatable late cells; drop the field if a material late gain cannot be separated. A predictive ablation alone cannot establish issuance time or prove a leak. No blanket removal is supported by this audit.

Other within-order differences across attempts (24 platform-order timestamps, 230 push timestamps, 1,963 area IDs, 66 destination coordinate pairs) do not by themselves identify future values: accepted-attempt inputs can reflect changes before acceptance. Sender coordinates are constant within each order, though 97 merchant IDs have more than one coordinate across their orders; that is not a reason to replace observed order pickup coordinates with a global merchant coordinate.

No other ranked finding. The dtype probe's three flags all concern known categorical identifiers; no ordinal scale, measured quantity typed categorical, or unresolved missing-code error remains. This audit does not run models, accept the dataset scientifically, or settle the unobserved forecast revision process.

Probe output: `meituan_food_delivery_time.json` and `flagged.csv`.


</details>

<details><summary>Split audit</summary>

**Independent split auditor**

Verdict: right with notes; no actionable split findings. Audited definition SHA 256 2367a2d99a669858125f4008c5220ca24da4340485cc3a925aec273909258f60. Actual definition loaded independently with dataset_io; No scientific files edited.

| Test day | Train | Train fraction | Test | Unavailable arrivals excluded |
|---|---:|---:|---:|---:|
| Oct 24 | 500764 | 88.078% | 67349 | 370 |
| Oct 23 | 423008 | 74.402% | 77719 | 407 |
| Oct 22 | 345355 | 60.744% | 77637 | 423 |

Independently computed accept-before-midnight AND deliver-before-midnight train indices and calendar-day test indices exactly match every returned split. Zero overlapping train/test rows, unavailable train labels or overlapping test windows; every test day has all 24 acceptance hours. Latest train deliveries: Oct 23 23:59:47, Oct 22 23:59:53, Oct 21 23:59:56. SPLIT-9/10/14 hold. The exclusions affect 0.074%,0.096%,0.122% of otherwise eligible historical rows.

222705 distinct test orders (39.171% of all 568545) are scored. All labeled orders stay in the frame, including 62 acceptances through Oct 25 00:23:29, outside the three complete-day windows. Explicit cutoffs prevent a partial tail replacing Oct 22. Temporal evaluation matches future work with recurring entities (USE-10,SPLIT-1/3/13), not cold-start entities; no windows selected by model scores.

| Test day | Merchant seen | Courier seen | Pair seen |
|---|---:|---:|---:|
| Oct 24 | 99.853% | 98.775% | 51.762% |
| Oct 23 | 99.793% | 99.099% | 48.830% |
| Oct 22 | 99.815% | 98.524% | 44.801% |

No raw exact copies; unique waybill IDs and exactly one accepted attempt per order. Two processed feature profiles match but carry 48.5333 versus 48.5 minute labels: distinct order IDs, both Oct 21 11:21:34, together in training for all tests. Zero exact train/test feature copies with or without acceptance time. Retaining them follows measured LEAK-16 reasoning; approximate spatial similarity was not used as an invented entity key.

The sole absent accepted arrival is Oct 18, not a test day. Oct 24 has 322 deliveries after the next midnight and follow-up through Oct 25 00:44:11. Across three tests remaining-duration p 99 is 55.15-57.73 minutes; maxima 269.32-652.10. All 22181 prebooks retained. Terminal-truncation test:1047 acceptances in Oct 24 hour 23 have remaining p 50/p 90/p 99/max 21.45/34.45/49.727/74.917 minutes; earlier corresponding p 90 is 32.975-34.427, p 99 45.396-52.886, max 65.183-75.1. No observed terminal collapse. One extract cannot prove absence of unpublished orders or later outcomes: extraction freeze/revision history unknown (EV-7).

Training spans only five-seven days and tests Saturday/Sunday/Monday in one city. State seasonal/geographic limits (SPLIT-20). Source paper section 3.1 describes actual event clocks and forecasts; raw platform creation can be as early asOct 11 for prebooks despite source dt labels, without affecting acceptance splitting. Reproduction scripts supplied by reviewer: (local scratch artifact) and (local scratch artifact) preserved in this panel. Initial one-second timeout was followed by successful 8.8-second rerun.


</details>

<details><summary>Domain practitioner</summary>

**Independent domain practitioner**

Fit: direct, with an explicit unresolved forecast-timing risk. I would use this as an acceptance-time ETA refinement task. No established domain-validity failure requires changing the target or excluding prebooked orders.

At acceptance the operator knows the accepted courier, merchant, destination, acceptance location, order age, dispatch history and prebook flag. The 2025 paper section 3.1 explicitly places courier coordinates at acceptance. Pickup and arrival are future events and correctly excluded (USE-1, USE-3). Total placement-to-arrival is an exact representation of the ETA: subtracting known elapsed time gives remaining duration with identical errors (USE-5, USE-6). One accepted order matches one update. Future-day evaluation with recurring entities matches routine deployment; known deliveries at each refit respects label availability (USE-10). Eight days cannot establish seasonal or city transfer. Missing workload/route state limits inputs but does not invalidate this narrower task; completed-wave joins would introduce future information.

Independent test: promise is constant per order, meal-ready forecasts vary for 8,794 orders, initially reporting 8,168 orders varying in positive estimates. A later column audit distinguishes 8,174 orders varying after filtering to positive estimates. Do not call meal-ready estimates fixed at placement. The variation establishes revisions across attempts, not revisions after acceptance. The release lacks forecast generation/version times. Retaining accepted-row forecasts needs explicit acknowledgement of this residual uncertainty, not a claim of proven leakage. This potential timing risk alone does not change fit to approximate under USE-8.

| Acceptance day | Promise RMSE | Elapsed plus training mean remaining RMSE |
|---|---:|---:|
| Oct 22 | 11.755 | 11.014 |
| Oct 23 | 11.787 | 11.494 |
| Oct 24 | 12.141 | 10.680 |

These independently fitted baselines use labels known before midnight. Prebooked median remaining time is 38.2 minutes against 23.7 for on-demand; maximum prebooked total duration exceeds seven days. Known prebooking waits support retaining prebooks and residual baselines, not target-based trimming.

RMSE minutes is an acceptable explicit fallback (MET-1,3,5,8): background Sample Question 4 and the supplement/data paper name timing prediction without one predictive scoring metric. MAE/calibration are useful diagnostics, not a reason to invent asymmetric source costs. Sources read: original background Sample Question 4; supplement sections 2.4-2.5; 2025 paper section 3.1; independent raw CSV checks with supplied interpreter and No science files edited. True human choice: accept the documented forecast-snapshot uncertainty or request an alternative qualification.


</details>

<details><summary>Blind reviewer</summary>

**Independent blind reviewer**

Verdict: include with changes. The data supports a useful acceptance-time delivery prediction task, but the supplied target appears to include time already elapsed before prediction. That makes variance and ordinary R2 largely explainable by a known quantity. Define the target precisely, preferably evaluate remaining delivery time, and publish label-availability-aware temporal splits before inclusion.

Scope: read only task.md/data.parquet in the clean room plus the named public GitHub repository/background PDF. No surrounding project files, curation reports, skills or agent files opened. Inherited general instructions supplied no dataset evidence. DOI inaccessible. Read-only inspection; no dataset changes.

Task: plausible actor is the platform immediately after courier acceptance, refreshing customer ETA and operational planning. It is not candidate courier selection: the table describes the actually assigned and accepting courier. Public background distinguishes creation/dispatch/acceptance/arrival; meal preparation is an estimate and the earlier document describes courier coordinates at assignment. Exact derived formulas and estimate revision timing remain unverified from supplied blind inputs.

Measured:568545 rows x 18 columns, no exact duplicate rows. Acceptance spans Oct 17 00:01:00 toOct 25 00:23:29, with 62 Oct 25 rows. Target median 28.50, SD 79.63,max 10336.48 minutes. Missing meal-ready 9874(1.74%), dispatch-to-accept 1, none elsewhere.4962 merchants,4901 couriers,23 districts. Target equals promise within half second about 0.049%, not an equality shortcut.

**Ranked concerns**

1. Total target includes a known elapsed component. Correlation with elapsed 0.9904 and promise 0.9941. Total p 50/p 99/max 28.50/130.15/10336.48 minutes; remaining (total minus elapsed)24.18/56.32/652.10. Remaining SD 11.08 versus total 79.63. All 199 targets over one day are prebooks; largest has 10293.47 elapsed and 43.02 remaining. Adding total to acceptance suggests completions throughOct 30; adding remaining endsOct 25 00:46:18. Required: verify formulas and use remaining, OR explicitly frame total and require elapsed baseline. High total-target R2 is not strong prediction of future uncertainty. Do not automatically drop prebook extremes.

2. Acceptance sorting alone does not prove known training labels. Blind task.md supplies 3 windows but no boundaries,membership,validation,metric or as-of policy. Illustrative Oct 22/23/24 windows show 423/407/370 prior acceptances not complete at midnight, assuming residual is remaining. Publish exact splits, exclude labels not arrived at cutoff and apply to validation. Blind artifact does not establish whether intended splits already handle this.

3. Known elapsed distorts model comparison. Bounded diagnostics: expanding temporal training,1 daytests,LightGBM 120 trees,31 leaves,learning_rate 0.08,2 threads,categoricalIDs,acceptance hour extracted. Direct experiments conservatively excluded rows where acceptance plus FULL duration crosses cutoff. No tuning.

| Test | Rows | Median constant MAE | Elapsed+train median remaining MAE/RMSE | Direct model MAE/RMSE |
|---|---:|---:|---:|---:|
| Oct 22 |77637|14.95|8.35/11.19|7.04/68.47|
| Oct 23 |77719|14.42|8.60/11.72|6.76/42.87|
| Oct 24 |67349|14.40|8.25/10.73|6.84/55.34|

Elapsed baseline total-target R2 is 0.974-0.986. Same model on remaining with correctly matured labels:

| Test | MAE | RMSE | Remaining R2 |
|---|---:|---:|---:|
| Oct 22|5.64|7.48|0.538|
| Oct 23|5.78|7.95|0.518|
| Oct 24|5.58|7.21|0.543|

This establishes meaningful nontrivial future signal, not tuned ceiling. Use MAE/RMSE on exact defined outcome; residual R2 if used.

4. Redistribution permission before publication: source saysCC BY-NC 4.0,acknowledgment and separate third-party permission. Resolve for processed republication/commercial use; release blocker, not evidence against scientific task.

5. Semantic types/coordinates need metadata. IDs nominal despite numeric values; binary flags categorical; acceptance datetime needs timezone. Shifted integer coordinates are not ordinary geographic degrees; no geodesic formulas without verifying transformation. Durations numeric and missingness preserved.

6. Narrow horizon: about 8 days, only 0.90-1.48%test couriers and 0.15-0.21%test merchants unseen in diagnostics. Legitimate future orders in same population, no seasonal/city/cold start assurance. Do not use 62 rowOct 25 fragment as substantive day.

Inclusion conditions: exact target/feature formulas; remaining outcome OR explicit known-elapsed accounting; reproducible matured-label splits; semantic types; redistribution permissions. With these the residual task is large, real and nontrivial. Source: https://github.com/meituan/Meituan-INFORMS-TSL-Research-Challenge and its background PDF. Reviewer could not inspect withheld definition/notes/actual split memberships; parent/mediator must reconcile those evidence limits.

**Logical-type addendum**

Categorical-type objection resolved by supplied logical metadata, provided benchmark loaders honor it. The declared levels exactly match observed data:4962 merchants,4901 couriers,23 districts,2 prebooklevels,2 weekendlevels; no missing/unused levels. Integer storage is serialization, not incorrect intended semantics. Blind diagnostic models already treated all five as categories, so results need no revision. Coordinate transformation and timezone documentation remain requests within blind scope; all other concerns and include-with-changes verdict remain.


</details>

<details><summary>Task gamer</summary>

**Participant gaming probe**

Confirmed exploits: **0**. All 568,545 rows inspected, with full shipped training and test rows used; no subsampling. All reported predictions scored through `score.score`.

| RMSE / diagnostic | r 0 f 0 | r 1 f 0 | r 2 f 0 |
|---|---:|---:|---:|
| Honest direct LightGBM | 55.70723 | 38.61178 | 65.87652 |
| Honest elapsed-residual LightGBM | **6.91827** | **7.71333** | **7.23007** |
| Promised minutes alone | 12.14080 | 11.78748 | 11.75523 |
| Elapsed minutes alone | 27.47150 | 28.89413 | 28.23391 |
| Row-order-only LightGBM | 82.68092 | 72.54583 | 93.57694 |
| Exact train-feature copy matches in test | 0 | 0 | 0 |
| Training outcomes extending into test, using accepted + delivery − elapsed | 0 | 0 | 0 |

The direct and residual models both use all 17 intended inputs, timestamps converted to seconds plus hour/weekday, categorical IDs, and pairwise coordinate differences. Each LightGBM uses 180 trees, 31 leaves, learning rate .07, and two threads. The residual model predicts `delivery_minutes - elapsed_minutes` and adds the observed elapsed time back. This is an honest formulation using an intended input. Its improvement is not an exploit. The high total-duration correlations with elapsed (.9904) and promised (.9941) and heavy outliers explain why blindly fitting the total target is a weak baseline. Residual duration has median 24.18 minutes and 99 th percentile 56.32 minutes.

Tested attacks with no successful result:

- Row-position artifact: a 100-tree, 15-leaf LightGBM using only the global row index loses badly to the honest residual model on every split.
- Copy lookup: hash all intended columns and map held-out rows to training targets. There is one duplicate feature row globally, but no train/test matches on any split, so there are no usable copy predictions.
- Training-label timing: reconstructed completion under the elapsed-from-order interpretation is strictly before each test start for every training row. Treating delivery as acceptance-origin instead flags 229/255/274 rows, but that interpretation is inconsistent with the natural subtraction of elapsed and is not evidence of leakage. A conservative sensitivity run removing these flagged rows is recorded separately.

Limits: bounded tree models and cheap probes only; no exhaustive feature reverse engineering, semantic source verification, or public row lookup. Strong known inputs were treated as legitimate. No surrounding project files, other kits, curation notes, or external reports were opened. No public web was needed. Shipped files were not edited.

Artifacts: `probe.py`, `results.json`, per-split residual prediction arrays, `maturity.py`, and `maturity_results.json` (conservative timing sensitivity).

Conservative label-timing sensitivity: removing the 229/255/274 rows flagged by `accepted_at + delivery_minutes` leaves 500535/422753/345081 training rows and yields residual RMSE **6.92091 / 7.70960 / 7.24118**. Relative to retaining them, the RMSE differences are +.00264 / −.00373 / +.01111; this provides no consistent material leakage gain. Model compute took approximately 39 seconds for the main probes plus 26 seconds for sensitivity.

**Logical-type addendum**

Inspected the kit's new `logical-types.json`, `task.json` categorical metadata and `score.load()` restoration. Checked loaded values against raw Parquet: all five restored categorical columns retain identical values; other values and row index are identical. Prior models already treated `poi_id`, `courier_id` and `da_id` as categorical. The two remaining restored fields are binary `[0,1]` flags. No exploit or interpretation conclusion changes: zero confirmed exploits, and elapsed-residual improvement remains legitimate. No model reruns performed; original numerical results remain measurements of the original probe encoding, with these two flags numerical. Category handling could change individual fitted predictions slightly, so exact score invariance is not claimed.


</details>

<details><summary>Precedent checker</summary>

**Independent precedent check: Meituan delivery duration**

Observed 2026-11-08. Reviewer role: precedent checker. Checkout HEAD at review:
`9048f36a1bcf7da3687fde04b18ef79cd7a1201e`.

Verdict: the proposed acceptance-time task is consistent in principle. Proceed with
the add-dataset assessment, subject to the measured timing and split checks below.
This report is an AI recommendation, not curator acceptance of a final definition.
No dataset definition existed at the first pass, so this is not an implementation sign-off.

**Authority and approval**

The parent supplied the following session evidence: after the full Gate 1 explanation,
the user instructed the agent to run add-dataset repeatedly. That authorizes executing
the adding workflow and its review. The parent also supplied the recommended task:
predict total order-placement-to-arrival minutes at courier acceptance, using elapsed
minutes and inputs known then. I did not independently inspect the original user
transcript, and do not claim that the user separately chose each feature, timestamp,
metric, filter or split boundary. These implementation choices remain AI proposals
until reviewed under the workflow. Do not manufacture a CC line for them.

The existing Myunghwan triage claim was reported freshly verified by the parent.
It is preserved: this reviewer did not fetch, renew, change stage, release or otherwise
mutate claims. The local candidate record still contains the original unverified
screening draft; that historical text is not proof that the user withheld workflow
authorization or that every newly proposed detail is accepted.

**Decisions checked against rules and precedents**

1. USE-1, USE-3, USE-5: a platform refreshing an order's ETA when a courier accepts
   it has a real actor, moment and decision. Total elapsed duration to arrival is
   equivalent to the arrival time the actor acts on when order time is known. State
   explicitly that this updates an ETA after acceptance, rather than promising the
   initial ETA at checkout or selecting a courier before assignment. Fetch time and
   arrival time remain unavailable as features. Acceptance time can define the
   prediction point and clock features; order-to-acceptance minutes are known then.

2. USE-6, LEAK-37: the closest precedent is brazilian_ecommerce (Olist), whose
   checkout promise was retained because it predated delivery (2026-10-15). The
   platform promise and estimated meal-ready time are legitimate Meituan inputs
   when the published values are the estimates available by acceptance, rather
   than revisions recorded after it. A promised time before or after the observed
   acceptance is not itself evidence of leakage: estimates may be missed. Check
   their generation/version semantics. Medical_facility_operational_data similarly
   supports retaining an elapsed-time quantity known at the chosen prediction point.

3. USE-3, USE-6: merchant and assigned courier IDs are known at acceptance. The
   initial screening warned about courier fields because it considered order
   creation/dispatch; a later, explicit acceptance point distinguishes this case.
   The records describe courier location both as assignment-time position and as
   grab coordinates. Either an earlier assignment location or an acceptance location
   is eligible if known at acceptance, but do not label it an acceptance observation
   without source support. Availability, not the field's name or predictive power,
   decides. Reject post-acceptance trajectory information and completed-wave aggregates.

4. USE-10, SPLIT-1/3/4/6/13: future orders for the operating platform with recurring
   merchants and couriers call for a temporal split. Holding out couriers would test
   a distinct cold-start application. Keeping their IDs in this warm-start setting
   follows the rule and does not require a grouped split. Accepted waybills have
   one order each in initial-data.json (568,546 accepted rows and unique orders),
   supporting one prediction per accepted order, subject to final cleaning checks.

5. SPLIT-9/10: daily refits must use only earlier prediction rows whose arrivals
   are already known at the window start. Count late training arrivals at each
   actual boundary, check the resulting train fraction and require zero remaining
   unavailable labels. The closest cases are the taxi/cooking/router ETA tasks,
   which measured boundary overruns and used a one-day gap where needed; delivery_eta
   needed no gap because orders ended overnight. Copy the measurement, not their
   numeric gap. Olist's month gap follows its longer delay and is not a requirement
   for Meituan. A targeted as-of restriction or sufficient gap can meet the task;
   do not invoke the vehicle-loan fixed-horizon exception to retain known late
   arrivals when this source provides outcome timestamps. Do not select fast future
   prediction rows merely because their arrivals happened early. Release-end
   completeness/censoring remains a separate check.

6. SPLIT-11/12/14/15/20/21: eight source days may support at least three distinct
   daily test windows with expanding histories and >=50% train each. Prove that
   after cleaning and label-maturity restrictions; eight calendar labels alone do
   not establish it. Choose cadence from the application, not model scores. Use the
   actual prediction timestamp/local-day convention consistently; the source dt
   field and UTC timestamp dates need not have identical midnight boundaries.

7. PROV-4/5/6/7: food_delivery_time, Olist, JD.com and LaDe are not duplicates merely
   because they predict delivery time. The candidate's documented origin is Meituan's
   own waybill release, whereas food_delivery_time is the separately sourced Kaggle
   file with synthetic coordinate offsets. The courier-acceptance sibling shares
   Meituan provenance but asks whether an offer is accepted, a distinct task under
   PROV-7. No retirement, replacement or duplicate reclassification of another
   dataset follows from this add operation. Conversely, reshipping the same Meituan
   duration under another name or target scale would require duplicate scrutiny.

8. MET-1/3/8/10/11: the screening found an open research call without a unique
   duration leaderboard metric. RMSE in minutes is a defensible explicit fallback
   for an updated ETA's absolute timing error, after the source search is recorded.
   Olist later used context RMSLE on a log target because relative delivery-day
   error was the stated interpretation. That is a reason to explain Meituan's
   absolute-minute choice, not a standing rule that all durations use RMSLE.
   Choose and document modelling transform separately; any transformed target must
   declare its inverse correctly. Never pick the metric from whichever improves scores.

**Evidence and limits**

Read the checkout's AGENTS.md; both knowledge skill indexes; principles.md,
use_case.md, splits.md, metrics.md and the relevant provenance rules; the records
meituan_food_delivery_time, meituan_courier_order_acceptance, brazilian_ecommerce and
food_delivery_time; and the records/claims procedures. Paths are relative to the
checkout unless otherwise named. Rules and curator decisions are stronger evidence
than an automated register flag. No new standing rule or exception is needed for
the proposed framing.

Generated `register.json` with the supplied interpreter using
`decision_register.py --json PATH`.
The register includes historical consistency flags elsewhere, including vehicle-loan
exceptions; they are neither new Meituan failures nor authorization to alter them.
The register is a first-pass snapshot and will not include decisions added later.

Initial-data.json also shows one zero arrival, 9,874 zero meal-ready estimates,
17 zero courier IDs, 578 zero merchant IDs, 115,139 zero area IDs, and prebooked
orders with long total durations. These are prompts for source-aware cleaning,
missing-code interpretation and population/scale checks, not permission to trim
long durations by target or invent thresholds. Its extreme negative minimum follows
the zero arrival and should not be treated as genuine negative delivery time.

No direct source download, model fit, dataset check or final definition inspection
was performed by this reviewer. Timing availability and final fold maturity still
need the main agent's source and measured evidence. No scientific files or claims
were changed.

**Final consistency pass, 2026-11-08**

Reviewed the finished definition, SHA 256
`a768b61b5c5fbd7c2c385030318a76849df2fe829a219a05bbad86e10d1b75b7`,
its generated README, and the independent claims, columns, split and domain
reports in this panel. Also checked the cached 2025 source paper's acceptance
location statement and forecast-description passages. The earlier report above
is preserved as the first-pass assessment; this section supersedes its pending
implementation-inspection status.

Result: no actual remaining rule/precedent contradiction established. Recommend
presenting the final definition for human review with the unresolved forecast
snapshot timing clearly identified. This is not final scientific acceptance.

The final code implements the proposed acceptance-time total-duration task,
retains known elapsed time and prebooks, drops actual pickup/delivery inputs,
and uses delivery timestamps solely as temporary split metadata before removing
them from the model frame. The source paper explicitly places grab coordinates
at acceptance, resolving the first-pass location question. Notes now describe
meal forecasts recorded on the accepted attempt and disclose 8,794 orders with
varying meal forecasts and unknown revision history. This is consistent with
Olist's USE-6 precedent conditional on availability; the precedent does not
prove the stored Meituan snapshot existed by acceptance. Snapshot timing remains
an evidence gap, not an established leak, exception, amendment or resolved fact.
The direct-fit recommendation does not erase this uncertainty.

Explicit October 22-24 cutoffs and `delivered_at < midnight` training restrictions
match SPLIT-9/10/14. The split auditor independently matched every returned index:
train sizes 345,355, 423,008 and 500,764; at least 60.744% of all labeled rows;
423, 407 and 370 unavailable arrivals excluded; zero unavailable training labels.
This applies the taxi/order-time boundary precedent without copying Olist's
one-month gap. The README documents the 62 unscored October 25 rows; its check
summary reports no errors, one unused-row warning and one conflicting-copy info.
The two feature-identical profiles belong to distinct historical orders together
in all training sides, with no train/test exact-copy overlap according to the
independent split audit. Neither advisory flag contradicts the evaluation design.
I reviewed these audit artifacts and code; I did not rerun their measurements.

The claims/columns reports cite an earlier definition hash and flag date prose
that the current bytes have corrected: the row describes October 17-24 as source
cohorts and mentions October 25, and the split notes now say final three complete
local acceptance days. Their retained criticism of those superseded sentences
is historical, not a fresh contradiction. Their timing uncertainty remains current.

A known elapsed component is legitimate under USE-6. Total and remaining duration
are valid representations of the same ETA: with per-row known elapsed e,
`y_total - prediction_total = (y_total-e) - (prediction_total-e)`. Thus they give
identical RMSE for corresponding predictions. Independently trained nonlinear
models need not produce corresponding predictions; score equivalence does not
make a silent retraining-target change authorized. Retain the actual proposed
total target and disclose the component. The domain report supplies the needed
nontrivial comparison context: elapsed plus training mean remaining scores RMSE
11.014/11.494/10.680 minutes for October 22/23/24, against platform promise
11.755/11.787/12.141. A mean-total baseline alone would exaggerate progress.
These are baselines, not proof of benchmark value or of forecast timing safety.
The blind review's residual-target suggestion is a recommendation, not a user
decision, and does not identify a Must violation in the current target.

RMSE on raw total minutes remains a documented fallback, with no forced transfer
of Olist's relative-error interpretation. No source duplication or claim-stage
contradiction was identified. Human authorization still covers proceeding with
add-dataset; it does not establish acceptance of unresolved forecast provenance,
a new target or final shipping. No scientific files, claims, context
graph were changed by this reviewer.


</details>

<details><summary>Advocate opening</summary>

**Advocate opening: Meituan delivery duration**

Recommendation: retain this definition for human review. No established failure requires changing target, population or splits. Forecast snapshot timing remains unresolved; this does not establish final acceptance or release authorization. Reviewed definition a768b61b5c5fbd7c2c385030318a76849df2fe829a219a05bbad86e10d1b75b7, README and all seven Phase A reports.

1. Acceptance-time ETA updating is real and total-duration target explicit. USE-1/3/5/6 (Must;P3) support one accepted order, known age and future arrival. Source paper 3.1 places courier coordinates at acceptance; future pickup/arrival inputs removed. For known elapsed e, y_total-p_total=(y_total-e)-(p_total-e), so corresponding remaining predictions have identical RMSE. Independently fitted nonlinear learners need not correspond: gamer direct 55.707/38.612/65.877 versus residual 6.918/7.713/7.230. This is substantial modeling sensitivity, not target-validity failure. TP-6 distinguishes valid task from preferred version. Blind alternative allows total framing plus elapsed baselines, supplied by definition. Do not describe high total R2 as resolving future uncertainty.

2. Final splits satisfy blind request. For October 24, 23 and 22 respectively, independent checks found training sizes of 500,764 / 423,008 / 345,355 and test sizes of 67,349 / 77,719 / 77,637. Exclude 370/407/423 late labels, zero unavailable train outcomes/overlap, smallest train 60.744%. SPLIT-9/10/14 concern actual membership; final measurements outrank blind kit omissions under EV-2. Initial partial-Oct 25 native output historical; await final native rerun.

3. Snapshot timing is an evidence gap, not demonstrated leak. Source calls forecasts; promise invariant, meal-ready forecasts vary across 8,794 orders. Changed rejected estimates occur before eventual acceptance, supporting revisions before prediction but not proving issuance time of accepted snapshot. USE-3/6,LEAK-10 Must: if post-acceptance revisions established, restore/mask timely snapshots or drop unseparable field, keeping task under USE-12. None established. EV-2/3/6 prevent declaring either safety or leakage proven. Mild present remedy precise accepted-attempt wording plus human uncertainty; Olist conditional precedent not Meituan proof. Direct fit does not settle fact.

4. Raw inputs do not establish triviality. Gamer residual beats promise every fold 6.918/7.713/7.230 versus 12.141/11.787/11.755; elapsed alone 27.472/28.894/28.234 and stronger elapsed+train-mean remaining duration 10.680/11.494/11.014. Main all-three-window two 500 tree seeds full 7.159-7.181/7.925-7.930/7.525-7.538;without forecasts 8.403-8.417/9.505-9.527/8.921-8.945. Real residual signal and estimate sensitivity, not provenance/tuned ceiling. TP-4 needs raw feature matching methods fold by fold; absent. TP-1 still requires final native flag review; unfinished runs cannot be called complete.

5. Recurring entities/short horizon describe intended deployment. USE-10,SPLIT-1 choose future work with 99.79-99.85%seen merchants,98.52-99.10%seen couriers, not invented cold start.222705 test orders over 3 complete days;62 Oct 25 tailunscored. All 24 hours per test, no terminal collapse, followup beyond midnight.8 days cannot establish city/season transfer or prove no unpublished outcomes. Unused-row warning no Must failure. Corrected date prose supersedes older wording complaints (EV-2).

6. Cleaning preserves observed task.654343 attempts,568546 orders each one accepted,oneabsentarrival;568545 labels and 22181 prebooks remain. Structural zero forecasts become missing; nominal IDs categories; coordinates preserved; no completed-wave joins. One feature-conflicting pair distinct orders together in train, no exact train/testcopies. CLEAN atP 7 does not justify target trimming against P3. Gamer zeroexploits bounded, not universal immunity.

7. Licence terms belong release. RecordCC BY-NC 4.0/separatepermission and check before publication. EV-4 forbids licence as scientific verdict reason; neither proves nor disproves validity or any Must failure.

No scientific edits. Curator acceptance and snapshot uncertainty remain open; final native verification still pending at opening.


</details>

<details><summary>Critic opening</summary>

**Critic opening**

Verdict: ship after small documentation changes and a curator decision on forecast uncertainty. No exclusion supported.

1. Forecast availability asserted more strongly than verified. task_summary.known lists both as known at acceptance;fit_reason says inputs describe order by acceptance;long notes acknowledge unknown revision history. Claim,column,domainaudits agree meal-ready forecasts vary across 8,794 orders,promise constant; neither establishes issuance time. USE-3/6(Must,P3),LEAK-10(Must,P4),EV-7(Must) require supported meaning versus unverified availability. Mild remedy qualify short summaries and one REVIEW question: retain under snapshot assumption or seek logging/alternative qualification. Keep direct fit underUSE-8; uncertainty alone does not imply approximate fit. No proven leak justifies automatic removal.

2. Strongest models do not settle uncertainty. Across all three folds and two seeds, remaining-duration models scored RMSE 7.159-7.930 minutes with all inputs and 8.403-9.527 minutes without forecasts. Forecast block matters, signal survives without it;combined ablation neither isolates meal nor places revisions after acceptance. EV-2 limits evidence to tested question;EV-6 calls circumstantial such. Report scope/method sensitivity, not forecast safety or proof suspect revisions supply gain. Human judges provenance, not whether to repeat completed experiments.

3. Benchmark value requires correct baseline context. Known elapsed explains much variance. Gamerresidual 6.918/7.713/7.230 vs promise 12.141/11.787/11.755 and elapsed+mean remaining duration 10.680/11.494/11.014. High totalR 2/meanbaselinegain alone not forecasting progress. TP-4 requires proof before Trivial, absent;EV-8 needs model/split provenance. Include these baselines/residual interpretation. Retain total target; change unnecessary for honest corresponding prediction errors.

Concede other objections: final code matures training labels,evaluatesOct 22-24,retains 62 unscored tail,removes futureevents,corrects date wording. Blind lacked final definition. Recurringentities/prebooks/knownelapsed legitimate. Licensing releasechecklist underEV-4,not scientificverdict.

Routine: summary qualifications,evidencepresentation,confirm final probes. Curator: retain forecasts with snapshot uncertainty? No file edits per read-only role.


</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal**

1. Concede the short-summary qualification. `known` and `fit_reason` should distinguish source-supported forecast meanings from unverified availability of the stored snapshots at acceptance. The long notes already disclose revisions across 8,794 orders and unavailable revision history. USE-3/6 (Must, P3), LEAK-10 (Must, P4) and EV-7 (Must) support consistent wording throughout. This is a documentation repair and an explicit curator question, not an established leak or reason to exclude. Retaining `direct` does not establish snapshot safety.

2. Agree that ablations cannot settle issuance timing. Completed qualification covers all three windows and two seeds: full residual RMSE 7.159-7.930, without estimates 8.403-9.527, without entity IDs 7.498-8.461. These results establish model sensitivity and signal surviving removal of the forecast block. They neither isolate the meal estimate nor show when either forecast was recorded. EV-2 (Must) limits each measurement to its tested question. If later evidence establishes unavailable values, USE-12 (Must, P3) favors repairing the inputs while keeping the task.

3. Agree on baseline presentation and retaining the total target. Gamer residual RMSE 6.918/7.713/7.230 improves on promise 12.141/11.787/11.755 and elapsed-plus-mean-remaining 10.680/11.494/11.014. TP-4 (Must, P6) therefore supplies no Trivial finding. Corresponding total and remaining predictions have identical errors; separately trained learners can differ substantially. Report absolute-minute errors and these baselines without treating high total-target R2 as evidence of strong prediction of future uncertainty.

The remaining difference is resolved by qualifying the short summaries. Final native task probes remain pending; historical output containing the partial October 25 window cannot close that check. The curator still decides whether to retain forecasts under the documented snapshot assumption. No scientific files changed, and this rebuttal does not constitute human acceptance.


</details>

<details><summary>Critic rebuttal</summary>

**Critic rebuttal**

Concede advocate points 1, 2 and 4-7. The total target is valid, final measured splits resolve the blind reviewer's concerns, models beat appropriate baselines, and neither cleaning flags nor licensing justify scientific exclusion. The unfinished native rerun remains routine verification, not evidence of failure.

On point 3, agree that forecast timing is unverified rather than a demonstrated leak. Retention for human review is supported. My remaining objection is presentation: `known` and `fit_reason` still state acceptance-time availability without the qualification already present in longer notes. EV-7 (Must) prevents upgrading cannot-verify to pass; USE-8 allows direct fit while naming the uncertainty.

Exact mild change:

- In `known`, describe "the accepted attempt's recorded promise and meal-ready forecast; their snapshot timing relative to acceptance is unverified."
- Append to `fit_reason`: "Forecasts are retained assuming the accepted-attempt values were available by acceptance; the release provides no issuance or revision timestamps."
- Present completed ablations as sensitivity evidence, never timing verification.

Exact human question: "Accept retaining the recorded forecasts with this explicit availability uncertainty, or require logging evidence or qualification of an alternative without the unresolved fields before acceptance?"

No target, population or split change is warranted by current evidence. No science edits made.


</details>

<details><summary>Review editor</summary>

Substantively ready after presentation edits; no additional human issue needed. Lead outcome with valid task, useful operational signal and mature-label temporal splits. Lead panel with ship after changes. Explain remaining-duration models in plain language. Convert embedded headings to bold; expand compressed prose and remove execution plumbing from the portable copy while preserving run originals. Keep the single forecast-snapshot decision and actual pending acceptance. Parent applied these changes; the collector parses one issue with no field disagreements. The independent editor rechecked the outcome, issue and panel opening and found them ready for curator review, with no further edits.

</details>


<details><summary>Focused all-event claim audit</summary>

Zero new actionable findings. Independently audited all six actual event clocks, the final definition, source rows, previous qualified frame and ordered split membership. All 568,545 accepted labeled orders have arrival as their latest actual event. The explicit max-event assertion, strict midnight arrival filter and earliest-test-acceptance assertion therefore certify the complete observed training interval. Pickup and arrival are excluded from predictors, and temporary delivery metadata is removed before modeling.

Every clock of every training order is strictly before its refit boundary and earliest test acceptance; zero violations and unchanged purges of 370, 407 and 423 orders. Every train/test index and all feature/target values match the previous qualification. Numeric category storage in the kit is restored through its declared logical schema; this is not a data change. No model rerun needed.

Promise and meal-ready timestamps are forecasts of future times, not observed future events. Their issuance/revision timing remains unverified. The curator approved acceptance-time framing and the actual-event boundary, not forecast retention, warnings, final inclusion, build or commit. A clean event boundary does not prove forecast provenance.

</details>

<details><summary>Focused all-event split audit</summary>

Pass for the curator-approved acceptance-time boundary. Exact typed-frame comparison includes every value, categorical level, column, row order and index: 568,545 rows and 18 columns match the previous qualified frame. All six ordered train/test arrays match exactly. Independent raw lineage covers every accepted positive-arrival order once, without extra loss or duplication.

| Test day | Train | Test | Latest actual training event | First test acceptance | Actual-event violations |
|---|---:|---:|---|---|---:|
| October 24 | 500,764 | 67,349 | October 23 23:59:47 | October 24 00:00:04 | 0 |
| October 23 | 423,008 | 77,719 | October 22 23:59:53 | October 23 00:00:01 | 0 |
| October 22 | 345,355 | 77,637 | October 21 23:59:56 | October 22 00:00:02 | 0 |

Every one of the six source event clocks passes independently. Training fractions are 88.0782%, 74.4019% and 60.7437%; purges remain 370/407/423. Gaps before first test acceptance are 17/8/6 seconds, and the training end precedes midnight by 13/7/4 seconds. The 62-row partial-day tail remains unchanged.

Acceptance-to-delivery training and test intervals do not overlap. Literal placement-to-delivery intervals still overlap for 220/256/280 future-acceptance test orders, because some prebooked orders were placed earlier. That does not violate this prediction-time availability rule: all training observations already exist before test acceptance. Do not claim full placement-interval disjointness.

Exact typed frame and every ordered membership support reuse of previous model evidence without fitting. Forecast issuance timing and live evaluator isolation from future query rows remain unverified; neither is resolved by this split check.

</details>

<details><summary>Focused boundary mediator</summary>

Pass for this scoped correction; no scientific fix or model rerun needed. The independent claim and split audits verify all actual training events precede midnight and earliest test acceptance. Exact typed-frame and ordered-membership equality support reuse of existing scores.

The curator settled acceptance-time prediction and rejected expanding this work into a nominated-courier counterfactual task. Observed-event separation is not the same as demanding disjoint placement-to-arrival intervals for prebooked orders. The code and review use the approved acceptance boundary, so earlier placements do not invalidate it.

Forecast snapshot issue 1 remains unresolved; predicted future dates are not actual event observations. Live evaluator causal query isolation also remains unverified. No warning acceptance, final ship, build or commit approval is inferred. Original full-panel evidence stays historical; these checks cover only the explicit boundary correction.

</details>

<details><summary>Focused isolated participant boundary recheck</summary>

The isolated participant recheck found zero training completions at or after the earliest test acceptance in all three windows. Completion is reconstructed as acceptance plus total duration minus known elapsed time.

| Split | Violations | Max training completion | First test acceptance |
|---|---:|---|---|
| Newest | 0 | October 23 23:59:47 | October 24 00:00:04 |
| Middle | 0 | October 22 23:59:53 | October 23 00:00:01 |
| Oldest | 0 | October 21 23:59:56 | October 22 00:00:02 |

No missing boundary timestamps. Reconstruction has nanosecond floating-point noise, without changing the strict boundary results. No models were rerun; original model settings and scores retain their earlier scope.

</details>

<details><summary>Focused review editor</summary>

The accepted_at choice is settled, the all-observed-training-event guarantee is stated precisely, and the record judgment does not promise disjoint placement-to-arrival intervals. Forecast issue 1 remains open, and neither live evaluator isolation nor warning/final shipping acceptance is asserted. No new curator issue or scientific correction needed. The only requested edit was to trim local execution plumbing from portable focused reports while preserving full run originals; that edit was applied. Ready for curator review.

</details>

<details><summary>Focused forecast-free qualification</summary>

The primary has 568,545 accepted labeled orders and 15 features. Both platform forecast columns, their durations and missingness are excluded; replacing raw forecasts with missing or extreme values leaves the complete cleaned frame unchanged. Source cohorts, target and cutoffs are preserved; row order changes only within tied acceptance timestamps. Historical predictions were not reused.

| Test day | Forecast-free RMSE, two seeds | Recorded promise RMSE | Elapsed plus training mean remaining RMSE |
|---|---:|---:|---:|
| October 24 | 8.416–8.431 | 12.141 | 10.680 |
| October 23 | 9.498–9.517 | 11.787 | 11.494 |
| October 22 | 8.917–8.988 | 11.755 | 11.014 |

Full training sides, fixed 500-tree LightGBM, two seeds. Learn remaining minutes and add known elapsed back; errors are total-duration minute errors. Promise is an external recorded-value reference, with unverified issuance timing, not a certified prospective comparator. Forecast-assisted models remain historical sensitivity.

Fresh native leakage, raw, task, dtype and recurrence probes complete. Task probes: no flags; linear RMSE10.408, forest31.162, direct LightGBM62.834 on capped training. Known elapsed explains much total variance; residual comparisons assess future uncertainty. No exact feature copies cross splits. The incomplete October25 tail is retained but never evaluated. Nominal IDs remain categorical. Check: zero errors, one explained warning (62 unused tail rows), two extra conflicting-profile rows informational (two pairs of distinct orders with seconds-apart arrivals); no acceptance inferred.

The same source cohorts and all six actual-event boundaries pass independent checks. Query-row context is not operationally available before its own acceptance; live evaluator isolation remains unverified.

</details>

<details><summary>Focused forecast-free precedent check</summary>

**Independent precedent check — curator choice**


Closest precedent: 2_month_survival_rate_prediction, Lennart2026-10-26: objective model beside physician comparator. USE-6 does not compel every distinct task to consume a blackbox comparator. Olist and LDAPS concern forecast refinement and remain valid alternative tasks; the explicit independent framing distinguishes this choice. Medical-facility elapsed precedent supports retained known elapsed duration at acceptance. No exception, amendment, contradictory precedent or drift established. decision_register --rule USE-6 had zero flagged cases. Proceed with scoped feature change, affected qualification and focused independent review.

</details>

<details><summary>Focused forecast-free claim audit</summary>

**Independent claim audit — forecast-free revision**


| Claim | Independent test | Result | Rule |
|---|---|---|---|
| Both platform forecasts, derivatives and missingness excluded | Replace both raw columns with all missing, then extreme constants; compare complete _clean outputs | Exact equality including target and temporary split metadata; 15 inputs | USE-3/6, LEAK-10 |
| Acceptance point and total target preserved | Trace standardized rows to raw | 568545 unique labeled orders; target max difference0; acceptance mismatches0 | USE-3/5, PROV-12 |
| Every actual training event precedes refit | Test six raw event clocks in each fold | Zero violations for placement, push, dispatch, acceptance, pickup, delivery; arrival latest in every row | SPLIT-9/10 |
| Promise external only | Inspect dependencies and recompute raw test errors | No feature, target or split dependency; evidence agrees | USE-6, EV-2/7 |
| RMSE computes | Native constant-mean scorer on all folds | Finite | MET-1/2 |
| Independent ETA framing implemented | Summary, notes, code, curator words | Holds; forecast timing uncertainty retained for external comparator; feature approval is not ship/metric/warning/build acceptance | USE-1/6, EV-7 |

| Test day | Train | Test | Recorded promise RMSE | Native dummy RMSE |
|---|---:|---:|---:|---:|
| Oct24 | 500764 | 67349 | 12.140804 | 82.310145 |
| Oct23 | 423008 | 77719 | 11.787483 | 71.900442 |
| Oct22 | 345355 | 77637 | 11.755230 | 93.108383 |

Historical and current ordered frames differ within tied acceptance times (e.g. rows19/20 exchange merchants1116/578). Do not reuse old predictions by position or claim exact ordered equality. Historical forecast-assisted results retain sensitivity scope. Issue 1 now records Myunghwan’s choice and is resolved; final inclusion, metric and warning acceptance remain pending. No further fitting is necessary.

</details>

<details><summary>Focused forecast-free column audit</summary>

**Independent column audit: forecast-free Meituan**

Audited 2026-11-09. Findings requiring a definition correction: **0**. Scope is the human-selected independent ETA model immediately after courier acceptance, predicting total placement-to-delivery minutes. This is not final acceptance, build authorization, or acceptance of the unused-tail warning.


Loaded the actual definition through `dataset_io.from_definition`, using the project Python and warehouse, with all numerical The final frame has **568,545 rows, 15 predictors and one target**. The dtype probe counts 14 because its table omits datetime columns. Its three count_like flags are courier_id, poi_id and da_id: these are nominal identifiers, so categorical is correct under CLEAN-12/14. No ordinal scale needs decoding.

| Column | Meaning and availability at acceptance | Actual dtype / cleaning | Verdict and rule |
|---|---|---|---|
| poi_id | Anonymized merchant, known from order | category; 4,962 levels | Fine; USE-3/10, CLEAN-12/14 |
| courier_id | Accepting courier, known at acceptance | category; 4,901 levels | Fine; USE-3/10, CLEAN-12/14 |
| da_id | Source area/business district code; includes order-type effects and overlapping geography per supplement 2.6 | category; 23 levels | Fine; USE-3, CLEAN-12/14; do not reinterpret as disjoint geographic polygons |
| is_prebook | Order was booked in advance, known at placement | category; observed 0/1 | Fine; USE-3, CLEAN-11/14 |
| sender_lng | Merchant longitude, known from order | int64; source shifted units; no zero cells | Fine; USE-3, CLEAN-2/14 |
| sender_lat | Merchant latitude, known from order | int64; source shifted units; no zero cells | Fine; USE-3, CLEAN-2/14 |
| recipient_lng | Customer specified destination longitude, known from order | int64; source shifted units; no zero cells | Fine; USE-3, CLEAN-2/14 |
| recipient_lat | Customer specified destination latitude, known from order | int64; source shifted units; no zero cells | Fine; USE-3, CLEAN-2/14 |
| grab_lng | Courier longitude at acceptance; paper section 3.1 explicitly settles timing | int64; source shifted units; no zero cells | Fine; USE-3, LEAK-2/3, CLEAN-14 |
| grab_lat | Courier latitude at acceptance; same source timing | int64; source shifted units; no zero cells | Fine; USE-3, LEAK-2/3, CLEAN-14 |
| accepted_at | Actual grab_time converted to China local time | datetime64[ns]; UTC+8 | Fine; USE-3, CLEAN-12/14 |
| is_weekend | Weekend of acceptance, not source creation-date flag | category; observed 0/1, recomputed from accepted_at | Fine; USE-3, CLEAN-14 |
| elapsed_minutes | Acceptance minus placement | float64; 0.05 to 10,293.4667 minutes; no missing | Fine; USE-3/5, CLEAN-11/14; long prebook waits stay |
| dispatch_to_accept_minutes | Acceptance minus dispatch of accepted waybill | float64; 0 to 319.7667; one source zero dispatch becomes missing | Fine; USE-3, CLEAN-10/11/14 |
| push_to_accept_minutes | Acceptance minus actual push into dispatch system | float64; 0.0167 to 10,293.1167; no missing | Fine; USE-3, CLEAN-11/14 |
| delivery_minutes (target) | Actual delivery minus placement, only learned after delivery | float64; 1.9667 to 10,336.4833; no missing; not an input | Fine; USE-5, LEAK-12 |

Both raw estimate_arrived_time and estimate_meal_prepare_time are absent from the model frame, along with promised_minutes and meal_ready_in_minutes. Independently replacing both raw forecast columns with NaN, and then removing both raw columns entirely, leaves `_clean` output exactly identical by pandas frame equality. Feature construction, sample inclusion, missingness and split construction therefore have no forecast dependency. `_decisions` reads the raw recorded promise solely to calculate an external reference error table. It neither adds a predictor nor changes split membership. Recorded promise issuance time remains unverified. Prior forecast-assisted scores remain historical sensitivity evidence. Exclusion implements the explicit independent-prediction framing; USE-6 still permits available source estimates in a forecast-refinement framing and does not by itself establish leakage.

The source's six actual events are placement, push, dispatch, acceptance, pickup and arrival; predictions are not events. In every labeled accepted row, placement and push are no later than acceptance; positive dispatch is no later than acceptance; pickup and arrival occur later. Arrival is the maximum of all six actual clocks in every row. Pickup is excluded from predictors; delivered_at is a temporary training-availability guard removed by `_make_splits`.

Used index-traced raw lineage to independently check all six clocks for each actual split (rather than assuming source CSV row order equals the standardized frame). Latest training actual event and first test acceptance, China local:

| Test day | Latest of all six training event clocks | Earliest test acceptance |
|---|---|---|
| October 24 | October 23 23:59:47 | October 24 00:00:04 |
| October 23 | October 22 23:59:53 | October 23 00:00:01 |
| October 22 | October 21 23:59:56 | October 22 00:00:02 |

The strict training-interval boundary remains intact. No full-wave information, future aggregates or joined dispatch snapshots enter the feature table.

The check's conflicting-profile info reflects two pairs (four rows) of genuinely distinct order and waybill identities after dropping identifiers. Their recorded arrival times differ by 2 and 3 seconds respectively. This is plausible coarse-profile ambiguity, not established reposting: retain under LEAK-16/18/20 with the documented info. No row deletion is justified by this finding. The 62 after-midnight October 25 acceptance rows remain outside the three complete-day test windows; disposition of that existing warning is outside this column audit.


</details>

<details><summary>Focused forecast-free split audit</summary>

**Forecast-free primary revision: focused split audit**

Observed 2026-11-09 UTC. Verdict: right with notes. No new split issue found. The acceptance-time use case remains temporal, with recurring merchants/couriers allowed (USE-10, SPLIT-1/3/6); strict midnight label availability is satisfied (SPLIT-9/10), and all three expanding histories exceed the 50% floor (SPLIT-14). This is a focused independent split audit, not final curator approval.

The final definition has 568,545 labeled orders and 15 model features. Both forecast-derived fields, `promised_minutes` and `meal_ready_in_minutes`, leave the feature frame. The target remains total placement-to-arrival minutes, and `accepted_at` remains the temporal key. The external raw promise comparison neither supplies a feature nor defines a split.

**Measured final splits**

| Test acceptance day | Train | Train share | Test | Unfinished prior acceptances excluded | Latest training actual event | Earliest test acceptance |
|---|---:|---:|---:|---:|---|---|
| 2022-10-24 | 500,764 | 88.0782% | 67,349 | 370 | 2022-10-23 23:59:47 | 2022-10-24 00:00:04 |
| 2022-10-23 | 423,008 | 74.4019% | 77,719 | 407 | 2022-10-22 23:59:53 | 2022-10-23 00:00:01 |
| 2022-10-22 | 345,355 | 60.7437% | 77,637 | 423 | 2022-10-21 23:59:56 | 2022-10-22 00:00:02 |

For each split I independently reconstructed membership from the raw-row lineage: train acceptance before midnight and all six actual event clocks strictly before midnight; test acceptance within the next local day. The resulting ordered positions equal the actual final split arrays. There are no extra exclusions, train/test intersections or repeated test rows across windows; the distinct test union is 222,705 orders.

Each of `platform_order_time`, `order_push_time`, `dispatch_time`, `grab_time`, `fetch_time` and `arrive_time` has zero training events at or after midnight, and zero at or after the earliest test acceptance, in every window. Across all labeled rows the maximum of the six clocks equals arrival. Thus the arrival guard covers every observed training event. This establishes separation at acceptance; prebooked test orders can have placements before midnight, so it does not mean placement-to-arrival intervals are disjoint.

**Source cohort identity and changed order**

Both definitions were processed with the maintained `dataset_io.from_definition(..., raw=True)` interface, tracing source positions by index. Source positions are unique and map to unique order IDs. The frame covers exactly the accepted positive-arrival source rows: 654,343 raw attempts, 568,546 acceptances, one absent accepted arrival omitted. No additional cleaning loss or duplication occurs. Exactly 62 October 25 acceptances remain in the frame and are the only rows unused by every train/test side. They remain outside the three complete-day tests.

The saved old definition exactly reproduces the frozen qualified participant kit's data frame (values, dtypes, category metadata, columns, index and order) and all six ordered train/test position arrays. Every old/new common column is exactly equal after alignment by raw source position. Every final train/test source-order cohort is unchanged: sorting raw source positions within each side produces exact equality with the old version.

Ordered frame identity is **not** preserved. Removing features changes the content hash used to order equal acceptance timestamps; 295,619 full-frame positions map to a different raw source row. The old/new `accepted_at` series is identical position by position, proving these swaps remain within tied acceptance times.

| Test day | Train positions mapping to different raw rows | Test positions mapping to different raw rows | Ordered integer train array equal old | Ordered integer test array equal old |
|---|---:|---:|---|---|
| October 24 | 261,231 | 34,287 | No | Yes |
| October 23 | 218,533 | 42,690 | No | Yes |
| October 22 | 178,450 | 40,067 | No | Yes |

The unchanged test integer arrays are not evidence of unchanged test row order. Existing prediction vectors cannot be attached to the new frame by position. Model qualification and exploit scores must come from the new feature version, as the parent session is doing; this audit ran no models and makes no claim that old predictions verify the new task (EV-7/8).

**Duplicate note**

The final feature frame has two extra conflicting duplicate rows: four rows in two exact-feature groups with differing targets, compared with one extra row (two rows in one group) previously. This matches the current check's `dataset_conflicting_duplicate_rows` info count of 2. Exact feature hashes including acceptance datetime identify zero test rows with a copy in train on each actual split. The increase does not introduce cross-split copies. No deduplication is proposed.

</details>

<details><summary>Focused forecast-free isolated participant</summary>

**Independent isolated participant recheck**

Inspected only the revised participant kit and generic libraries. All scored models use each split's training labels and current-row predictors; no holdout tuning or future-query features.

| Total-minute RMSE | October24 | October23 | October22 |
|---|---:|---:|---:|
| Training mean total | 82.3101 | 71.9004 | 93.1084 |
| Elapsed plus train mean remaining | 10.6800 | 11.4935 | 11.0142 |
| Elapsed plus courier mean remaining | 9.9503 | 10.7116 | 10.2628 |
| Elapsed plus merchant mean remaining | 9.8406 | 10.5844 | 10.1416 |
| Fixed180-tree direct LightGBM | 54.7951 | 42.2838 | 67.6648 |
| Elapsed plus fixed180-tree remaining LightGBM | 7.3215 | 8.2094 | 7.6996 |

Both ensembles use the same fixed settings, declared categorical inputs, timestamp-derived day/hour/weekday and simple coordinate differences/distances. Distances remain shifted-source units. Remaining-time predictions add known elapsed back before native total-minute scoring. The stronger results than unengineered qualification are not an identical-settings comparison.

Target/elapsed correlation0.99037; remaining duration mean25.716, SD11.084, median24.183, 99thpercentile56.317 minutes. Known elapsed explains extreme total tails. Decomposition is lawful, not leakage; 7–8minute remaining uncertainty survives.

Chronological boundaries have zero reconstructed training arrivals at/after test start. Two duplicated predictor vectors globally; zero exact train/test copies even excluding acceptance timestamp. Partial courier/merchant/destination matches cover only0.05–0.07% of tests. Recurring IDs supply legitimate historical signal. No broad copy exploit demonstrated.

Future same-courier query rows exist for94.7–95.4% of test rows. Their use would violate the acceptance-time information contract. Immediate next-grab position matches current destination for0/0/1 rows, and gap correlation with remaining time is weakly negative. No scored model uses that context. Live evaluator whole-query visibility/isolation remains unverified: a conditional concern, not a proved flaw. No demonstrated shortcut removes future uncertainty.

</details>

<details><summary>Focused forecast-free mediator</summary>

**Judgment:** ship, pending curator approval; routine review reconciliation completed. This is an AI recommendation. Validity: approved independent ETA, no forecast dependency, strict six-event temporal boundaries. Value: meaningful remaining-time signal survives legitimate elapsed and entity baselines; no Trivial finding. Quality: no definition correction, duplicate-profile information explained, 62-row warning still unaccepted. First-party provenance and sample size favor inclusion; short single-city coverage limits generalization.

No renewed feature choice is needed. Final inclusion, fallback RMSE in minutes and explicit acceptance or disposition of the 62 retained October25 tail rows remain for Myunghwan. Recommend inclusion and retaining the explained tail. The recorded promise's snapshot timing and live evaluator query isolation remain unverified, without a demonstrated defect creating another scientific choice.

The participant's elapsed decomposition is lawful known information (USE-3/6). Historical courier/merchant means fit recurring-entity prediction (USE-10; SPLIT-1/3/13). Copy checks found no train/test lookup (LEAK-16–21), and maturity checks found no violations (LEAK-12; SPLIT-9/10). Future same-courier query context is a conditional evaluation concern (LEAK-9/10), not a scored exploit or verified live evaluator flaw. No model used it. Preserve current-row plus training-history inputs and exclude subsequent query rows/future batch aggregates.

Simple and engineered residual models use differing preprocessing; they establish feasibility, not a model ranking. Historical assisted scores stay sensitivity only. No further fit is needed. Precedents support an objective model beside a comparator; Olist/LDAPS refinement is a distinct task. No exception or amendment.

The published issue/options remain historical with the actual curator words and a closing Resolved turn, as the review format requires; the page hides it from open choices. Original reports remain preserved.

</details>

<details><summary>Focused forecast-free review editor</summary>

The cold editor found only presentation corrections: distinguish the completed scientific recommendation from pending curator acceptance, make the three remaining approvals explicit, remove a stale reconciliation statement and remove a malformed process-identity table from the portable report. These edits are applied. Preserve the original resolved issue/options and historical reports. No scientific correction or additional model checks are needed.

</details>

<details><summary>Final curator approval</summary>

**Myunghwan (2026-11-09):** "yes. agreed." This approves all three offered decisions: include the forecast-free dataset, use fallback RMSE in minutes, and retain the 62 October 25 rows outside the scored windows with the explained warning accepted.

The independent consistency check found no conflicting precedent, rule exception or amendment. The warning reason is recorded in the definition and the metric acknowledgement in the curation record. Earlier panel statements about pending approval remain historical. Data, target, features and split construction are unchanged. Scientific review is complete; build, commit and publication have not been requested.

</details>
