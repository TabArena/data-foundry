---
unique_name: sendy_logistics_challenge
name: sendy-logistics-challenge
checked_by:
- Myunghwan
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 2
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
- 'Entities: Recur'
- 'Features: Read Later'
collections:
- New (BeyondArena)
original_source: Zindi
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/sendy-logistics-challenge/data
v2_path: datasets/_dev/tabarena-v0pt2/sendy_logistics_challenge/dataset.py
source_row: 929
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: predict the time from pickup to arrival of a Sendy motorbike delivery in Nairobi from the order, its timestamps up to pickup, distance, weather and rider metrics; a real ETA task with a named user, but no month or year in the data.
- Source: Zindi, "Sendy Logistics Challenge" (2019-08-23 to 2019-11-25, 2,201 participants, $7,000), hosted by Sendy and insight2impact. As published: Train.csv (4.1 MB), Test.csv (1.2 MB), Riders.csv, VariableDefinitions.csv; "a subset of over 20,000 orders and only includes direct orders (i.e. Sendy 'express' orders) with bikes in Nairobi. All data in this subset have been fully anonymized while preserving the distribution", with weather added; columns Order No, User Id, Vehicle Type, Platform Type, Personal or Business, day of month / weekday / time for placement, confirmation, arrival at pickup and pickup, Distance (KM), Temperature, Precipitation, pickup and destination lat/long, Rider Id; Arrival at Delivery times only in Train; target "Time from Pickup to Arrival" in seconds.
- Use case: Sendy tells the customer an arrival time when the rider picks up the package, and plans scheduling ("enhance customer communication ... improved resource management and planning for order scheduling"); fit direct at pickup; regime: a temporal task by nature, but the release has only day of month and weekday, no month or year ("Placement - Day of Month i.e 1-31"), so the windows SPLIT-14 asks for cannot be built and it ships IID, forced from temporal (SPLIT-8). The AI-filled `required_split` `Temporal (NON-IID)` is changed to `Random (IID)` for that reason.
- Siblings and duplicates: `sendy_logistics_challenge_2` (the Zindi Mentorship #2 and EDSA 2020 re-runs, both with this competition as parent and the same file sizes; proposed `Duplicate` in this batch); `delivery_rider_response_challenge_by_galsenai` (IndabaX Senegal 2021, Sendy rider matching, AI `No`, another task). External collections: none found.
- Papers and pages: https://zindi.africa/competitions/sendy-logistics-challenge (winners linked from the page, not read).
- Metric: `rmse` on seconds (Zindi Evaluation: "The error metric for this competition is the Root Mean Squared Error"), a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: Riders.csv holds rider aggregates (number of orders, age on platform, average rating, number of ratings), probably taken at extraction time over all orders (LEAK check); drop the Arrival at Delivery columns; rider-marked times give many near-zero or implausible targets (known from the competition, to verify; CLEAN, not a reason to drop rows silently); join the rider table on Rider Id.
- Priority: gap 0, use case +, source +, shape +, risk - (rider aggregates, noisy target, forced IID).

Zindi Sendy logistics challenge to predict delivery ETA for parcel/motorbike deliveries in Nairobi, a genuine real-world tabular regression task with order, rider, and location features. This is a strong fit for the benchmark, though it likely involves joining multiple provided tables (orders + riders) and may need a temporal split since deliveries are time-ordered. A human must confirm the target (ETA/duration), table structure to be joined, size, split regime, and license; note potential overlap with the 'sendy_logistics_challenge_2' record.

**CC (2026-10-29, Myunghwan):** Pursue add-dataset for Sendy delivery duration at pickup. Use timestamped orders and exclude undated changing rider summaries, including counts, ratings and tenure. The later clarification permits joining verified static rider attributes by Rider ID; this supersedes the earlier blanket exclusion of Riders.csv. Eligibility requires actual field semantics, availability at pickup and a join that preserves order rows. Exclude arrival-at-delivery outcome fields from predictors. This is screening approval, not final inclusion. Split and full data qualification remain pending. The source's seconds/RMSE task is the starting proposal. No build or commit requested.

**Assessment (AI, 2026-10-29):** Added for curator review, not final shipment. Official archive has 21,201 labelled Nairobi delivery orders; definition retains all rows and 19 predictors, scored by original RMSE in seconds. All labels equal recorded arrival-minus-pickup clocks; 547 (2.58%) are <=10 seconds and 740 (3.49%) <=60 seconds, so physical-ETA fit is approximate. No eligible static rider attributes exist: counts, tenure and ratings are excluded; no rider-table join. Destination-arrival fields, unique order ID, constant vehicle and four duplicated calendar fields are removed. The recorded target, provisional source-distance retention and forced random split await curator decisions. No complete chronology was recovered; future dates would trigger chronological evaluation and label-availability checks. Native five-fold diagnostic RMSE is 767.02 versus dummy 988.29 seconds, with no task flags; leakage and hidden-group probes show no identified copying shortcut. On the first native repeat, full/no-distance RMSE is 761.52/789.63 seconds; distance timing remains unverified, not proven leakage. The panel recommends conditional inclusion, with conservative distance omission unless retention is justified. This assessment supersedes historical direct-fit, mandatory rider-join and final-IID language; screening Yes remains pursuit authority only. Priority 2: gap 0 (no thin domain/type/regime), use case 0 (real source ETA purpose but approximate fit), source + (original codebook), shape + (21,201 rows and mixed inputs), risk - (recorded-label and feature-timing uncertainty).

**Assessment (AI, 2026-10-29, placement-time revision):** Qualified the curator-requested total-duration task on all 21,201 labelled completed express orders with 13 placement-time inputs. Excluded later events, rider identity and undated rider summaries; source distance remains provisional. The recorded total avoids pickup-marking errors but is not verified physical arrival; retain source rows pending curator disposition. Native first-five-fold RF RMSE 2017.72 seconds versus dummy 2227.52; all 26 checks pass and fresh probes show no flags. First-repeat pooled L2 RMSE/MAE 2133.11/1158.59 seconds; two multi-day orders contribute 39.31% of squared versus 1.06% of absolute error. A focused independent recheck supports inclusion subject to recorded-label, distance, same-release split and scoring choices; recommends MAE if average absolute ETA miss is the intended objective. Current RMSE is a stand-in for the revised target, not the original contest task. This supersedes pickup-task numerical/feature claims without changing the historical curator inputs or assigning shipment. Priority 2: gap 0 (no thin domain/type/regime), use case 0 (real ETA purpose, approximate recorded outcome), source + (original codebook), shape + (21,201 rows, mixed inputs), risk - (timing and label uncertainty).

CC (2026-10-29, Myunghwan): Approved excluding total placement-to-arrival durations above 24 hours and straight-line endpoint average speeds above 100 km/h. Retain equality and keep the original pickup-short cases unless these total-duration rules exclude them. The restricted benchmark covers ordinary completed deliveries; eligibility is outcome-conditioned. Source distance, random split and metric remain open; no ship/build authorization.

CC (2026-10-29, Myunghwan, distance): "I don't think the definitioin matters too much as far as it is consistent." Applied as retention of source Distance (KM) after empirical consistency checks, not certification of its acquisition time. Filtered Train/Test medians 8/8 km and correlations to endpoint distance 0.9524/0.9532 support a shared distance-like meaning; repeated-route variability and exact as-of remain documented. Revisit if actual later-only provenance emerges.

CC (2026-10-29, Myunghwan, split): "is the order No looking ordered? we can check. we don't need exact "time cutoff" but sequence based cut off is fine. in the worst case, accept the random split but with limited value" Across all 28,269 original Train/Test orders, numeric Order No sorting has day/weekday adjacency 0.669% versus random 0.693%; clocks lack forward progression. No supported chronological sequence was found. Applied the authorized fallback: repeated random same-release folds with limited generalization value, not a future-period or historical-label-maturity test.

CC (2026-10-29, Myunghwan, metric): Stick to the original eval metric Applied RMSE on raw total-duration seconds; no target transformation.

**Assessment (AI, 2026-10-29, approved-filter recheck):** Current task retains 21,199 rows and 13 placement-time predictors; two >24-hour rows and zero >100 km/h rows excluded by curator decision. Source distance retained after consistency audit, with as-of unverified. Native 26 checks pass; fresh first-five-fold LGBM mean RMSE1531.58 versus dummy1808.66 with no task flags; leak and hidden-group checks find no demonstrated shortcut. Independent membership, boundary, column, split and scorer audits pass. Fixed-model pooled first-three-fold RMSE1546.32/MAE1128.95; fold RMSE1563.93/1565.66/1508.68; longest1% of retained labels18.31% squared error. These replace the earlier all-row current-performance claims. Outcome-conditioned eligibility, recorded-arrival uncertainty and temporal optimism remain disclosed. All four add-stage choices are settled; ready for final review-added judgment after final consistency verification. No final curator ship, build or commit. Priority 2: gap0, use case0 (approximate recorded and restricted ETA), source+ (original source/codebook), shape+ (21,199 mixed-feature rows), risk- (documented provenance and temporal limitations).

CC (2026-10-29, Myunghwan): "yes, ship" — accepted the final Sendy placement-to-recorded-arrival definition after review-added-datasets. Retain 21,199 rows and 13 predictors; exclude total durations >24 hours and straight-line average speeds >100 km/h; retain source distance with undocumented as-of noted; retain RMSE in seconds and random same-release evaluation after numeric Order No failed the sequence check. Pickup, arrival-at-pickup and confirmation times are not predictors; pickup timestamps do not enter the target. Calendar fragments contradict a single-month release if accurate; same-month interpretation is only within each order, not across the dataset. Outcome-conditioned population, recorded-event uncertainty and limited future-generalization value are acknowledged. Ready for a separately requested build/commit; neither is authorized by this verdict.

CC (2026-11-04, Lennart): `Distance (KM)` stays as implemented (Review issue 2), with a `Potential leak, kept on purpose:` note under LEAK-38 quoting the dictionary's "Distance covered". The declared metric (RMSE in seconds) is checked as declared.

CC (2026-11-04, Lennart): the task is the source's, pickup to arrival at pickup ("yes switch to the source task please"), scored by the competition's RMSE, with the rider id and the earlier clocks as inputs. The two multi-day orders are ordinary rows under it ("these might become normal rows again"), so the duration and speed filter of 2026-10-29 and its exception to CLEAN-11 are withdrawn: 21,201 rows. The 547 pickup legs of 10 s or less stay as the source's labels (CLEAN-11).

**Assessment (AI, 2026-11-04):** under the pickup task, Order_No_2800 and Order_No_3530 have pickup legs at the 87th and 70th percentile (2,640 and 1,854 s, about 15 km/h by the source distance). No leg exceeds 3 h; 834 legs are faster than 100 km/h in a straight line, 546 of them the short legs of the late pickup mark. Riders.csv stays out: every rider's `No_Of_Orders` is at least their orders in Train plus Test. `dataset check` passes.

CC (2026-11-04, Lennart): the placement and confirmation weekdays are numbers (CLEAN-14, a cycle).

CC (2026-11-04, Lennart): the fit stays approximate under the forced-IID split, as beMTPL97, freMTPL2 and the other forced-IID definitions ("(b)").

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; its issues came from the light static review of the PR #33 page and the research behind each mark, and all are settled.

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes, then a rebuild on the curator's ask (USE-5 holds, the label being exact from the logged pickup mark; `Distance (KM)` tested under EV-1 and passes; a weak leak across rows, +3.4 RMSE, kept with a note; SPLIT-8 holds at a measured cost of 1.3 s; MET-1 to MET-4 hold; the notes now give these numbers); disputed: USE-5 and CLEAN-11 on the 547 late-marked legs (11.5 RMSE for a model trained without them), P5 on the stale build; for the curator: issues 4-7. Priority 2: gap 0, use case 0, source +, shape +, risk - (use case: Sendy's own ETA decision, but the fit is approximate; source: Zindi page with a codebook; shape: 21,201 orders, 19 mixed inputs; risk: the late-marked labels, issue 4, leave the target partly unclear).

CC (2026-11-05, Lennart): the precipitation blanks stay missing, with the note on their likely meaning (Review issue 6, A; CLEAN-10).

CC (2026-11-05, Lennart): no rebuild now; the container is rebuilt with the release, and until then no text claims probes on the new one (issue 7, A).

CC (2026-11-05, Lennart): the declared metric (RMSE, the source's) is checked and stays as declared.

CC (2026-11-05, Lennart): the 740 pickup legs of 60 s or less leave (Review issue 4, B, agreeing with the AI's answer; CLEAN-11's clause for a row whose target the source names as not the task's quantity), with the winners' page: the rider "forgot to mark that he took the order and did it just before it was delivered" (https://zindi.world/learn/meet-the-winners-of-the-sendy-logisitics-challenge). No one acts on the ETA of a leg marked at the destination, since the customer already has the parcel, so a deployed team leaves these legs out of training and does not judge its model on them; the late tap shows in the inputs (a median wait at the pickup of 1,505 s on legs of 10 s or less against 475 s on legs over 120 s). This supersedes the keep of 2026-11-04; 20,461 orders remain.

CC (2026-11-05, Lennart): `Distance (KM)` is labelled "tested: not measured between the rider's two taps; a GPS total recorded after delivery not excluded" (issue 5, A as choice (a) of the consistency check), and the untested part is named in `fit_reason` as a kept risk (USE-8, as kick and homesite); LEAK-38 names it among the kept fields. It replaces the `Potential leak, kept on purpose` label of 2026-11-04.

**Assessment (AI, 2026-11-05):** after the drop of issue 4: 20,461 orders and 922 riders on random 3x3 folds (6,820-6,821 test rows; 99.1-99.4% of test orders have a rider seen in training); `dataset check` 0 errors, 0 warnings; leak probes: all features R² 0.392 (Distance alone 0.348), no exact copies across the split, and probe 19 flags the removed rows as the cut on the label. LightGBM on the shipped folds: RMSE 742.8 s on the first repeat (766.6 without Distance); over the nine splits the wait feature gains 3.2 (8.5 before), training only on legs of 100 s or more costs 0.2 (11.5 before), the rider's later orders that day gain 4.2 (3.4 before), and holding out calendar days or month classes costs 2.1 and 1.1 s. The same scripts on the rows before the drop give 764.2 and 787.2 s on the first repeat, not the 761.3 and 789.6 the notes quoted, so those two old figures do not reproduce exactly.

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask. The claim stays until the PR that takes it to `main` sets `DF: Yes`.

## Review

**Outcome:** added. Sendy's 21,201 labelled Nairobi express orders from the Zindi challenge, as the source's own task:
the seconds from the rider's pickup mark to arrival at the destination, predicted at pickup, scored by the source's
RMSE in seconds, on random folds forced from temporal. The review panel recommends shipping after the note edits made
in this pass and a rebuild on your ask. Validity: USE-1 and USE-8 hold (fit approximate); USE-5 holds by the
mediator's reading and is disputed by the critic for the late-marked legs (issue 4); LEAK-10 and LEAK-16 hold;
`Distance (KM)` was tested under EV-1: it is not measured between the rider's two marks, and a GPS total recorded
after delivery is not ruled out (issue 5: which label its note takes); a weak leak across rows is kept with a note
(LEAK-30 tension row); USE-7 holds for two orders that end 89-90 m from their pickup (anonymised coordinates, source
distance 3-4 km; note added). This departs from your 100 m radius for Lusaka of the same day; the mediator would drop
both orders if you disagree. SPLIT-4 and SPLIT-8 hold, the forced-IID cost measured at 1.3 s RMSE. Value: MET-1 to
MET-4 hold, every fold scorable; LightGBM 752-762 s against 987 s for the mean. Quality: CLEAN-11 keep of the short
legs (issue 4), CLEAN-10 meaning of blank precipitation (issue 6), CLEAN-14 holds. Weighed: the source's own task and
real deliveries (+) against the late-mark labels, which are worth 12 s of RMSE (-). For you: issue 4 (a disputed
Must), then 5, 7 and 6.

**Main points:** Keep the 547 late-marked pickup legs or drop them (4)? Call `Distance (KM)` tested rather than a
potential leak (5)? Rebuild, since the container is the superseded placement task (7)? Fill blank precipitation with
0 (6)?

**Record judgment:** valid. The 2026-11-04 CC lines replace Myunghwan's placement task of 2026-10-29 and his "yes,
ship", which `suggestion: 'Yes'` and `claimed_by: Myunghwan` still carry. The record's line 70 ("no panel ran")
becomes false and is replaced by the panel line when this file closes. One CC line of 2026-11-04 reads "pickup to
arrival at pickup" where it means "at destination"; it is yours, so it is left for you to fix.

**Issues for Lennart:**

4. **Keep the 547 pickup legs of 10 s or less, or drop the late-marked legs?**

   * **Problem:**
     - The label is the pickup leg, the seconds from the rider's pickup mark in the app to the arrival mark, and riders
       often make the pickup mark only at the destination, so the label is a few seconds although the parcel travelled
       kilometres: 547 legs of 10 s or less (2.6%), 740 of 60 s or less, 822 of 120 s or less.
     - On those rows the customer already has the parcel when the pickup is marked, so no arrival estimate rests on
       them, and the task partly scores spotting the late mark.
     - Keeping them is disputed under the rule that the label is the quantity the actor acts on[^label] and the
       cleaning rule on which rows stay[^clean], and departs from the taxi precedents (consistency check).
   * **Background:** The winners' page says the rider "forgot to mark that he took the order and did it just before it
     was delivered" ([winners](https://zindi.world/learn/meet-the-winners-of-the-sendy-logisitics-challenge)); two
     winners built outlier classifiers for these rows. Now all 21,201 rows are kept (your call of 2026-11-04); the
     anomaly note gives the numbers below, and the task summary says that the 2.6% of labels of 10 s or less reward
     spotting a late mark rather than estimating a trip.
   * **Experiments:**

     | Measure (LightGBM) | Value |
     |---|---|
     | Share of the squared error, legs of 10 s or less (first repeat) | 4.6% |
     | RMSE on all legs / on the other legs (first repeat) | 761.3 / 749.3 s |
     | Trained only on legs of 100 s or more, as a deployed ETA model would be (9 splits) | loses 11.5 (744.2-755.7) |
     | Feature "wait from arrival at pickup to the pickup mark" (nine splits) | gains 8.5 (4.8-12.1 per split) |

   * **Consistency:** nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m dropped trips under 30 s
     (pkdd also above 120 km/h), delivery_eta_1m and cooking_time_1m times under 1 min, also against the competitions'
     own labels, so "the source's labels" alone does not set Sendy apart. The facts that do: the short legs are real
     deliveries (median 2.64 km in a straight line, none within 100 m); the late mark shows in the inputs (median wait
     1,505 s against 475 s on legs over 120 s), while nyc's broken clocks and pkdd's GPS jumps did not; Zindi applied no
     filter, where TabReD did for delivery_eta and cooking_time.
   * **Panel:** The critic reads the rule on the label's quantity[^label] as failing these labels ("a label checked and
     found to be another quantity than the one the actor acts on still fails"), and an exception to the cleaning
     rule[^clean] cannot answer a Must. The mediator and the advocate hold the label rule met: no system observes the
     physical pickup, the app fires on the rider's tap, and the label is exactly the destination clock minus the tap
     clock in every row (asserted in the code), so the error sits in an input that the wait shows. Then the cleaning
     rule's default (keep) applies, and its clause "a row whose target the source names as not the task's quantity may
     leave, with the source's words" permits a drop without requiring one.
   * **Unknown:** What would settle it: the host's own statement (VariableDefinitions.csv or the forum) that these
     marks are errors.
   * **Option details:** B and C drop the late-marked legs under the cleaning rule's source-words clause[^clean],
     quoting the winners' page, with a cut at 60 or 120 s, where the long wait before the pickup mark still shows; a cut
     at 30 s or 120 km/h leaves late marks in (of the 803 legs above 120 km/h, only 80 are longer than 60 s). Cost: 740
     or 822 rows, a departure from the task the source scored, and a cut that rests on the label.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | all rows; a Cases row | the source's task; real deliveries | 2.6% score a late mark |
     | B | Drop legs of 60 s or less | 740 rows leave | late marks out | not the scored task; a cut on the label |
     | C | Drop legs of 120 s or less | 822 rows leave | late marks out | not the scored task; a cut on the label |

   * **Recommendation:** A (mediator): keep, and record the distinguishing facts as a Cases row (kind `applied`) of the
     cleaning rule[^clean]. **Decision:** A, B or C?

   **Notes for the AI:** on A, write the CLEAN-11 Cases row (kind `applied`) with the facts under Consistency. On B or
   C, drop under CLEAN-11's source-words clause, quoting the winners' page.

   [^label]: **USE-5** (Must, disputed).
   [^clean]: **CLEAN-11** (Should); its clause "a row whose target the source names as not the task's quantity may
     leave, with the source's words". A CLEAN-11 exception cannot answer USE-5, a Must.

   **Lennart (2026-11-05, discuss):** IT seems here, however, that one could argue that a good preprocessing would
   remove these for the deployed model, no? or would we argue that we would observe these in real-world at predict time
   and need to be robust to them?

   **Answer (AI, 2026-11-05):** Both are true, at different steps, and they point the same way. The rows do occur at
   prediction time: the rider taps pickup at the destination, the app computes an ETA, and the inputs show the late tap
   (a median wait of 1,505 s from arrival at the pickup to the tap, against 475 s on other legs). But no one acts on
   that ETA, because the customer already has the parcel. So a deployed team would leave these legs out of training, as
   your first reading says, and would not judge its model on them, since a wrong ETA there costs nothing. Robustness to
   them would matter only if a decision rested on those predictions, and none does.

   The benchmark today does the opposite on both counts: it trains and scores on them. 4.6% of the squared error comes
   from spotting the late tap, and a model trained only on legs of 100 s or more, as a deployed one would be, loses 11.5
   s RMSE for it.

   This leans to B: drop the legs of 60 s or less (740 rows) under the cleaning rule's clause for rows the source names
   as not the task's quantity, quoting the winners' page. C (120 s, 822 rows) also catches late taps that take a little
   longer, at the cost of more real short legs. The cost of either is a departure from the task Zindi scored. If you
   agree, mark Change to B (or C).

   **Lennart (2026-11-05, discuss):** Agree.

   **Resolved (2026-11-05, Lennart):** B. The 740 legs of 60 s or less leave (547 of 10 s or less, 193 of 11-60 s;
   guarded), under the cleaning rule's clause for rows the source names as not the task's quantity, quoting the winners'
   page: 20,461 orders. LightGBM RMSE (first repeat) 742.8; a model trained only on legs of 100 s or more now costs 0.2
   instead of 11.5. The 82 legs of 61-120 s stay, some of them late marks too (median wait 1,358 s), named in
   `fit_reason`. A CLEAN-11 Cases row; `dataset check` clean.

5. **`Distance (KM)`: call it tested rather than a potential leak kept on purpose?**

   * **Problem:**
     - Your 2026-11-04 call kept `Distance (KM)` with a `Potential leak, kept on purpose:` note, since the page does not
       say whether it is the distance priced at booking or the distance travelled.
     - The panel tested the timing: it is not measured between the rider's two marks, though a GPS total recorded
       after delivery is not excluded.
     - The choice is the note's label and `fit_reason`, with no change to data or scores (the column lowers RMSE from
       789.6 to 761.5 s).
   * **Experiments:** 1,708 of the 2,094 routes that occur more than once with the same pickup and destination
     coordinates carry the same km and 275 of the other 386 differ by 1 km; within a route, Distance does not track the
     label (correlation 0.012-0.015); the legs marked at the destination carry the full route distance (median 5 km).
     So it is not measured between the two marks. A GPS total recorded after delivery is not excluded (partial
     correlation 0.159 with the label given the straight line, which a road distance would also give)[^tested].
   * **Background:** The rule for a potential leak kept on purpose covers only fields whose timing cannot be
     tested[^untestable]. The note keeps your label and now gives these measurements. `fit_reason` does not name
     Distance, so as it stands the definition does not meet the rule as the kick and homesite rows apply it: a potential
     leak kept on purpose is named in `fit_reason`[^fit]. Either A or B fixes this. Without an answer, B is applied
     before the rebuild.
   * **Panel:** A is the mediator's, B the critic's condition.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Relabel "tested, not a leak" | the note relabelled | matches the test | a GPS total not excluded |
     | B | Keep the label, add to `fit_reason` | names Distance as a kept risk | as kick and homesite | none found |
     | C | As now (implemented) | label kept, `fit_reason` silent | none found | fails the `fit_reason` rule |

   * **Recommendation:** A (mediator); then `fit_reason` needs no clause. **Decision:** A or B?

   [^untestable]: **LEAK-38** (Should): covers only fields whose timing cannot be tested.
   [^tested]: **EV-1**.
   [^fit]: **USE-8** (Must): a potential leak kept on purpose is named in `fit_reason`, as the kick and homesite Cases
     rows of USE-8 ask.

   **Lennart (2026-11-05, change):** Option A: Relabel "tested, not a leak".

   **Consistency check (AI, 2026-11-05):** "tested, not a leak" says more than the test shows: the distance is not
   measured between the rider's two taps, but a GPS total recorded after delivery is not excluded (partial correlation
   0.159 given the straight line). kick and homesite, with an untested part left, keep it named in `fit_reason`. Which
   do you want?
   - (a) label it "tested: not measured between the taps; a GPS total recorded after delivery not excluded", and name
     that part in `fit_reason`;
   - (b) A as marked;
   - (c) B: keep the current label and add Distance to `fit_reason`.

   Give the letter in the note; nothing is applied until then.

   **Lennart (2026-11-05, change):** Reply (a): label it "tested: not measured between the taps; a GPS total recorded
   after delivery not excluded", and name … Option A: Relabel "tested, not a leak".

   **Resolved (2026-11-05, Lennart):** (a). `Distance (KM)` is labelled "tested: not measured between the rider's two
   taps; a GPS total recorded after delivery not excluded", kept under LEAK-38 as amended today and named in
   `fit_reason`. It lowers RMSE from 766.6 to 742.8.

7. **Rebuild before shipping?**

   * **Problem:**
     - The container in the warehouse was built on 2026-10-29 for the superseded placement task (21,199 rows, 13
       inputs).
     - The README already describes the new definition (21,201 rows, 19 inputs), but its build block points at that
       container and carries `build_stale: true`.
     - Builds happen on your ask[^faithful].
   * **Background:** Every number in this panel comes from the definition's own frame.
   * **Panel:** The critic holds that "ship after the note edits" is not reachable until the rebuild; the advocate
     concedes it as a precondition, not a defect.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | With the release (implemented) | the 2026-10-29 container stays | none found | no probe saw the new one |
     | B | Rebuild now | `dataset check` and the probes on the new one | rows and splits changed | none found |

   * **Recommendation:** B, rebuild now, since the rows and splits changed and no probe has seen the new container.
     **Decision:** A (with the release rebuild) or B (ask for the rebuild now)?

   [^faithful]: **P5** (faithful data); builds happen on the curator's ask.

   **Resolved (2026-11-05, Lennart):** A. No rebuild now; the container is rebuilt with the release.

6. **Fill blank precipitation with 0 where a temperature exists?**

   * **Problem:**
     - `Precipitation in millimeters` is blank in 20,649 of 21,201 rows, and none of the 552 recorded values is 0
       (0.1-99.1 mm).
     - Every row without a temperature also lacks precipitation, so a blank beside a temperature most likely means no
       rain[^missing].
   * **Background:** Against: in 121 of the 172 hour blocks with rain, some orders carry a value and others are blank
     (anonymisation jitter or months merged by day and weekday).
   * **Experiments:** The fill changes RMSE from 760.5 to 761.4 s, so nothing measurable.
   * **Unknown:** What would settle it: VariableDefinitions.csv (not in the warehouse).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the blanks (implemented) | missing, a note on their meaning | no assumed meaning | none found |
     | B | Fill 0 | 0 where a temperature exists | the likely meaning | a meaning the source does not state |

   * **Recommendation:** A, keep the blanks, with the note: the fill changes nothing measurable and assumes a meaning
     the source does not state. **Decision:** A (keep the blanks) or B (fill 0)?

   [^missing]: **CLEAN-10** (Should).

   **Resolved (2026-11-05, Lennart):** A. The blanks stay missing, with the note on their likely meaning.

**Review panel:** ship after changes, then a rebuild on your ask (mediator). Tier full, second pass after your PR #33
review: twelve reports (claim, column and split auditors, domain practitioner, blind reviewer, task gamer, precedent
checker, advocate and critic with one rebuttal each, mediator). Claims: 45; 38 hold (three of them with a wording or
note fix), 1 refuted (the Distance timing is testable and passes; note updated), 6 untested (they need Test.csv and
Riders.csv; now phrased as the 2026-10-29 audit's). Blind review: include with small changes; its main concern the
near-zero labels. Task gamer: the best exploit is features from the same rider's later orders that day, +3.4 RMSE
against a noise spread of 0.3 (noted, kept as weak); the pickup-wait feature gains 8.5 by spotting late marks (issue
4). Agreed: no exclusion; the split and its measured cost; the metric; the note edits (Distance, the leak across
rows, the split cost, the two orders 89-90 m apart, precipitation, the untested claims). Disputed: USE-5 on the
late-marked legs (issue 4); whether the stale build blocks shipping (issue 7). Back to you because they revisit your
2026-11-04 calls: the Distance label (issue 5) and the short legs (issue 4). In the mediator's report, issues 1-4 are
issues 4, 5, 6 and 7 here; the other reports number their own points.

<details><summary>Mediator</summary>

**Mediator report: `sendy_logistics_challenge` (second pass, 2026-11-04)**

**Recommendation**

```text
Verdict: ship after changes, then a rebuild on the curator's ask, with `dataset check` and the probes re-run on the
new container (README `build_stale: true`, built 2026-10-29 for the superseded placement task; P5).
Validity: USE-1 holds; USE-5 holds (the label is exact from the logged pickup mark, which is the system's trigger);
USE-8 holds (approximate: rider marks plus forced IID; fit_reason must name the kept cross-row leak); USE-7 holds
(the two orders 89-90 m apart have a source distance of 3-4 km; coordinates are anonymised; note needed);
LEAK-10 and LEAK-16 hold; Distance (KM) was tested under EV-1 and is not a leak, so LEAK-38 no longer applies;
weak cross-row leak (+3.4 RMSE) kept with a note (LEAK-30 tension row); SPLIT-4 holds; SPLIT-8 holds, cost
measured (1.3 s).
Value: MET-1 to MET-4 hold (Zindi RMSE in seconds, all 9 folds scorable); TP: skill 0.24, R² about 0.40.
Quality: CLEAN-11 default (keep) applied to the late-marked legs; CLEAN-10 note on precipitation blanks; CLEAN-14 holds.
Weighed: source task +, real deliveries +, label artefact weight (12 s RMSE) -.
For the curator: issue 1, answer consistency check 1 on the short legs.
```

**Changes to make now (no decision needed)**

1. **`Distance (KM)` note (EV-1, LEAK-38 scope).** Replace "the page does not say which" with what was measured. My run:
   - 1,708 of the 2,094 repeated identical routes (82%) carry the same integer km. Of the 386 that vary, 275 differ by only 1 km.
   - Within routes, Distance does not track the label: r = 0.013, 0.015 and 0.012 for all legs, legs >60 s and legs >100 s.
   - The 547 late-marked legs carry the full route distance (median 5 km, residual −0.013 km).
   - A distance travelled by GPS would vary on almost every repeat and grow with the trip time, so this behaves like a route distance. LEAK-38 covers only fields whose timing cannot be tested, so the field is tested and passes. No `fit_reason` clause is needed for it. Relabelling Lennart's 2026-11-04 "kept on purpose" wording is issue 2.
2. **Cross-row leak note and `fit_reason` (LEAK-30 tension row, USE-8 Must).** Add a `Potential leak, kept on purpose:` bullet. Features built from the same rider's next order that day gain 3.4 RMSE (noise ±0.3, positive on 8 of 9 splits). Only a participant who builds features across rows can use it. Add one clause to `fit_reason` naming it as kept.
3. **`splits_comment` and `task_summary.split` (SPLIT-8 Must: the cost against the nearest windows).**
   - Weekday minus day mod 7 gives 7 month classes that cannot be put in order. Holding one out gives RMSE 750.1, against 748.8 for random folds of the same size. Holding out calendar days gives 755.1, against 752.5 on the shipped split.
   - "no month or year" becomes "no month order or year".
4. **USE-7 line in `curation_comments`.** Order_No_20080 and Order_No_7111 end 89-90 m from pickup, but the source distance is 3 and 4 km and the coordinates are anonymised. So the destination input exists and the rows stay. Name the fact that sets them apart from Lusaka, nyc and pkdd.
5. **Late-mark weight in `task_summary.predicted` and the anomaly bullet (USE-8 wording, writing.md).** State these numbers while the keep stands:
   - Late-marked legs are 4.6% of the squared error.
   - Without them, RMSE goes from 761.3 to 749.3.
   - A model trained only on legs of 100 s or more loses 11.5 RMSE (744.2 → 755.7).
   - An explicit pickup-wait feature gains 8.5 (4.8-12.1).
   - The late-mark signature reaches past 10 s. Median pickup wait: 1,505 s at ≤10 s, 1,337 s at 11-60 s, 1,358 s at 61-120 s, against 475 s above 120 s (my run).
6. **Precipitation (CLEAN-10, Should).** Add a note: none of the 552 recorded values is 0, so a blank with a temperature most likely means no rain. The fill itself is issue 3.
7. **Untested claims (EV-2).** The 99.4% of test riders seen in Train, `No_Of_Orders` ≥ Train+Test orders, and the 28,269-order adjacency need Test.csv and Riders.csv, which are not in the warehouse. Phrase them as "per the 2026-10-29 audit", or fetch the two files and re-run the counts.
8. **Record hygiene.**
   - Line 62 reads "pickup to arrival at pickup" where it should say "at destination". It is Lennart's CC line, so he may prefer to fix it himself.
   - Line 70 ("no panel ran") is now false.
   - `claimed_by: Myunghwan`, and his "yes, ship" refers to the superseded definition.
   - The `source_links` zindi.africa URL 301-redirects to zindi.world (cosmetic).

**Needs the curator, ranked**

**1. P3/P7, the 547 legs of 10 s or less (740 of 60 s or less, about 822 of 120 s or less) are kept. Consistency check 1.**
- **Effect:** the largest validity-adjacent effect measured. The task partly scores detecting mis-marks (11.5 and 8.5 RMSE, see change 5).
- **Settled by rank: no Must forces a drop.**
  - The critic rests on USE-5 (Must). That reading holds only if the prediction point is the physical pickup.
  - No input and no deployed system observes the physical pickup. The app fires on the tap, and the label is exactly destination clock minus tap clock in every row (asserted in `_clean`).
  - USE-5 fails a label that is "another quantity". Here it is the same quantity, and the error sits in an input (the late tap) that is visible in the wait.
  - With USE-5 holding, CLEAN-11's default is to keep. Its source-words clause permits a drop ("may"); it does not require one. Keeping is therefore not an exception to CLEAN-11, and the critic's "a Must has no exceptions" does not bite.
- **Left to the curator (a weighing):** whether to use the permissive drop, and how to answer the precedent departure.
- **Best evidence to keep (advocate):**
  - These are real deliveries: median straight line 2.64 km, none within 100 m.
  - nyc's under-30 s trips were "not rides" (a USE-7-like cut). pkdd's GPS jumps and nyc's over-3 h clocks were invisible in the inputs. delivery_eta and cooking_time copied TabReD's own filter. Zindi applied no filter.
- **Best evidence to drop (critic, task gamer, blind reviewer):**
  - No ETA decision depends on a tap made at the destination.
  - A deployment-style model is penalised by 11.5 RMSE.
  - The winners page quotes the mis-mark.
  - A cut at 30 s or 120 km/h would leave some late marks in: of the 803 legs above 120 km/h, only 80 are longer than 60 s.
- **Decision needed:**
  - (a) keep, recording the fact above as a CLEAN-11 Cases row (kind `applied`) with change 5; or
  - (b) drop under CLEAN-11's source-words clause, quoting the winners page, with a cut that follows the wait signature (about ≤60-120 s), not only ≤30 s.
- **What would settle it:** the host's own statement in VariableDefinitions.csv or the forum on whether these marks are errors.
- **Mediator's lean:** (a), as already decided on 2026-11-04, now with the distinguishing fact written down.

**2. P4, Distance (KM): relabel the note.** Lennart's 2026-11-04 CC asked for a `Potential leak, kept on purpose:` note. The measurements in change 1 take it outside LEAK-38's scope.
- **Decision needed:** confirm the note as "tested, not a leak" (no `fit_reason` clause needed), or keep the label and add a `fit_reason` clause (USE-8).

**3. P7, CLEAN-10: fill precipitation blanks with 0 where a temperature exists?**
- The fill changes RMSE from 760.5 to 761.4, i.e. nothing.
- For: no zeros among the 552 values. Against: 121 of the 172 hour blocks with rain mix values and blanks.
- **Settles it:** VariableDefinitions.csv.

**4. House rule, rebuild.** Builds happen only on the curator's ask. Shipping needs the rebuild and probes on the new container.

**Agreed facts**

- **Frame:** 21,201 rows, 19 inputs, no row dropped. Label = destination clock − pickup clock in every row; day delta is 0.
- **Clock order:** 0 rows break placement ≤ confirmation ≤ arrival at pickup ≤ pickup, except 5 confirmations that precede placement by 1-42 s. The arrival-at-destination fields are dropped.
- **Copies:** 0 exact copies across the split. 547 legs ≤10 s (2.58%), 740 ≤60 s. Longest leg 7,883 s.
- **Metric:** Zindi's RMSE in seconds. Every fold is scorable (dummy RMSE 964.7-1,006.0).
- **Split:** no time order can be built. `Order No` adjacency is 0.669% against 0.693% at random. Forced-IID cost 1.3 s.
- **Riders:** 99.2-99.4% of test orders have a rider seen in training. Rider hold-out gives 791.0, a cold start the use case does not have.
- **Distance:** the between-marks reading is refuted (r 0.012-0.015, full distance on late legs). Alone it gives R² 0.34.
- **Precipitation:** 20,649 blank, 552 recorded, 0 zeros.
- **Late marks:** pickup wait median 1,505 s on the late legs against about 480 s on the rest.
- **Task gamer, rider's next order:** new exploit, not in the notes. Rule: LEAK-30 tension row (weak transductive) and the SPLIT-8 cost. Gain 3.4. Remedy: change 2.
- **Task gamer, pickup wait:** known mechanism (the anomaly bullet), but the note gives no number. Rule: USE-5/CLEAN-11. Gain 8.5, which the note lacks. Goes into change 5 and issue 1.
- **Task gamer, honest-model flaw:** loses 11.5 RMSE. Issue 1.

**Consistency with precedent**

- **nyc/pkdd/delivery_eta/cooking_time short-trip drops:** departure, with a distinguishing fact (real deliveries; error visible in the inputs; no source filter). Issue 1.
- **USE-7 100 m radius (nyc, pkdd, Lusaka 2026-11-04):** departure, with a fact (anonymised coordinates; source distance 3-4 km). Change 4. If the curator disagrees, drop both orders as in Lusaka.
- **Lusaka "actual traveled distance" dropped (LEAK-10):** consistent. Sendy's field is now measured as a near-deterministic route distance.
- **LEAK-38 scope:** watch item only. medical_facility applied it to a named field the same day. Sendy no longer counts as such a case after change 1.
- **Consistent:**
  - fit approximate, as all 20 `ForcedIIDFromTemporal` definitions;
  - MET-4 (zillow_prize, Lusaka RMSE);
  - SPLIT-8 (account_debt_south_africa, mobile_churn);
  - CLEAN-14 weekdays as numbers (rossmann);
  - Riders.csv out (LEAK-10; kick, expresso).
- **Drift and amendments:** none, and no amendment due.

</details>

<details><summary>Claim audit</summary>

**Focus question.** `focus.md` asks for nothing beyond the standard panel. In short: no Must is refuted. All 45 claims and the declared metric survive the tests that could have refuted them, except four quality-level points about wording and notes. Six claims could not be tested here.

The frame and splits were rebuilt from the definition, with `to_container()` in memory and nothing saved.

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1, 4 | Pickup-to-arrival seconds; 2.6% ≤10 s | task_summary, cc | Count on the frame | holds | 547 (2.58%) ≤10 s, 740 ≤60 s; min 1, max 7,883; 0 above 3 h; 0 negative | CLEAN-11 |
| 3, 9 | 21,201 rows, no row dropped | ts, cc | Rows in vs out | holds | 21,201 raw, 21,201 out; 19 features | CLEAN-11 |
| 11 | Label = destination clock − pickup clock | cc | Recompute (also asserted in `_clean`) | holds | Day delta pickup→destination is 0 in every row; the assert passes | USE-5 |
| 4, 17 | Late pickup marks make the near-zero labels (winners page) | ts, cc | Read the winners page; compare the gap between arrival at pickup and pickup | holds | 2nd place: "the rider forgot to mark that he took the order". Gap median 1,505 s on ≤10 s legs vs 480 s on the rest | USE-5, EV-2 |
| 5, 12 | Every input is known at pickup | ts, cc (implied) | Clock order, plus the Distance test below | holds | 0 rows with arrival at pickup before confirmation, pickup before arrival at pickup, or destination before pickup. The arrival-at-destination fields are dropped | USE-3, LEAK-10 |
| 13 | Arrival-at-pickup and pickup weekdays (and days) copy the confirmation's | cc | Equality test | holds | Equal in all rows, for both day and weekday | CLEAN |
| 14a | 924 riders | cc | nunique | holds | 924 riders, 3,186 users | — |
| 14b | 99.4% of Test.csv orders have a rider seen in Train | cc | Needs Test.csv | **untested** | Test.csv is not in the warehouse | SPLIT-4 |
| 15 | `Order No` unique; `Vehicle Type` constant | cc | Check both | holds | Order No unique; Vehicle Type only `Bike` | CLEAN |
| 16 | Riders.csv not as-of (`No_Of_Orders` ≥ Train+Test orders) | ts, cc | Needs Riders.csv and Test.csv | **untested** (supported by the source) | Zindi data page: "No of Orders the rider has delivered", "Age: days since first order"; no as-of date | LEAK-10 |
| 18 | Orders 2800 and 3530 waited 22.7 h and 49.1 h; legs 2,640 s and 1,854 s (87th and 70th percentile) | cc, record | Recompute | holds | 22.7/49.1 h; 2,640/1,854 s; percentiles 0.873/0.695; distances 11/8 km | CLEAN-11 |
| 19 | Five confirmation clocks precede placement by 1-42 s | cc | Count | holds | 5 rows: 26, 42, 1, 13, 12 s | CLEAN-11 |
| 20a | Distance tracks the straight line (r 0.952) | cc | Haversine | holds | r = 0.9524; Distance is an integer number of km | — |
| 20b | Distance lowers RMSE 789.6 → 761.5 (first repeat) | cc | LightGBM (400 trees), repeat 0 | holds | 787.2 → 764.2 | LEAK-38 |
| 20c | Distance timing "cannot be told" ("the page does not say which") | cc | **Conditional test (EV-1):** on repeated identical routes, does Distance move with the trip? | **refuted: the timing is testable, and the test clears it** | 10,397 rows on 2,094 repeated routes. On the 2,731 rows whose route has more than one Distance value, the within-route deviation of Distance vs that of the label gives r = 0.013. The 190 routes holding both ≤10 s legs and normal legs give the same Distance (deviation −0.001 vs 0.000 km). A distance recorded along the trip would be about 0 on late-marked legs and grow with detours | LEAK-38 (covers only untestable timing), LEAK-10, EV-1 |
| 21a | Weather is at placement, measured every 3 h | cc | Zindi data page; constancy within clock blocks | holds (source) / not visible in the data | Page: "Temperature at the time of order placement … (measured every three hours)". In the data, 1-h blocks of one date hold 5.65 distinct temperatures on average, with no step at any of the five clocks (the anonymisation is the likely cause). Harmless at pickup in any case | EV-2 |
| 21b | Missing weather stays missing | cc | Distribution of the observed precipitation values | holds as implemented; **the meaning is unstated** | 20,649 rows missing, 552 present, minimum 0.1, **zero exact zeros**: a missing value almost surely means "no rain" | CLEAN-10 (Should) |
| 22, 33 | Metric: the source's RMSE in seconds, no transform | metric, cc | Fetched the Zindi page | holds | "The error metric for this competition is the Root Mean Squared Error"; submission column "Time from Pickup to Arrival", "time in seconds" | MET-1, MET-3, MET-4 |
| MET-2 | Computable on every fold | metric | `scorer(container)` with a dummy (train mean) on all 9 folds | holds | 7,067 test rows per fold; dummy RMSE 964.7-1,006.0, equal to a hand-computed RMSE; 165-208 legs ≤10 s per fold; no scoring columns needed | MET-2 |
| 6, 24, 27 | Random 3×3 folds; forced IID from temporal | ts, sc | Read the splits; day vs weekday | holds | 9 splits of 14,134/7,067. Every day of month carries 6.84 weekdays on average, so the data spans several months with no month or year column | SPLIT-8 |
| 25, 26 | `Order No` holds no chronology (0.669% vs 0.693%) | sc | Re-ran on Train only (Test.csv absent) | holds (Train part) | Adjacency of day+weekday: 0.627% sorted vs 0.731% shuffled | SPLIT-7, SPLIT-8 |
| implied | No row is a copy across the split | — | Exact duplicates on all raw columns except `Order No` | holds | 0 copies (the probe also found 0.0%) | LEAK-16 |
| implied | The target is the real-world target | ts fit | Short legs' share of the squared error; a late-mark feature | holds, as `approximate` | Short legs are 4.6% of LightGBM's squared error. The engineered gap feature cuts RMSE 764.2 → 756.2, so the task partly rewards spotting late marks, as the competition did | USE-5, USE-8 |
| 2, 8 | Use case; fit approximate | ts | Zindi page | holds | Page: predict "delivery time from pickup to arrival at the final destination" | USE-1, USE-8 |
| 10 | Replaces placement-to-arrival task | cc | Record CC line of 2026-11-04 | holds; **record wording error** | The CC line reads "pickup to arrival **at pickup**"; it should say "at destination" | writing |
| 23, 30 | Test.csv has 7,068 unlabelled orders; source facts | cc, record | Needs Test.csv | **untested** | Not in the warehouse; the data page confirms Test.csv lacks the target columns | PROV-1 |
| 32 | Sibling `_2` is a duplicate | record | Read the sibling's record | holds (by the record) | `sendy_logistics_challenge_2`: `No`, `Duplicate`, PROV-4 (Mentorship #2 / EDSA re-runs); data not re-compared | PROV-4 |
| PROV | Record (zindi.africa) vs definition (zindi.world) | checklist | Fetched the old URL | holds (cosmetic) | zindi.africa returns 301 to zindi.world: the same page | PROV-1 |
| 28 | `dataset check` clean | report | prep check.txt | holds | 0 errors, 0 warnings; `build_stale: true` | — |
| 29, 31, 34-45 | Screening and older record lines | record | Compared with the definition | holds, as superseded | The 2026-10-29 lines (13 predictors, 21,199 rows, filter, "yes, ship" for the placement task) are overruled by the 2026-11-04 CC lines (the newer curator decision wins) | Precedence |

**Refuted, ranked by `principles.md`**

1. **P4, Should (LEAK-38): claim 20c.** The note calls `Distance (KM)` a "Potential leak, kept on purpose" because its timing cannot be tested. It can be, and the conditional test finds no trip signal: within-route r = 0.013 (n = 2,731), and late-marked legs carry the full route distance (190 routes). LEAK-38 covers only fields whose timing cannot be tested. So the right label is "tested, not a leak", not "kept on purpose".
   * **What it changes:** no data or score change. The verdict on Distance moves from an accepted risk to a measured pass.
   * **Mildest remedy:** reword the curation note to give the measurement. Drop "Potential leak, kept on purpose" and "Revisit if a source shows…", or keep the note with these numbers added.
2. **P7, Should (CLEAN-10, meaning of a missing value): claim 21b.** No precipitation value is 0.0. Of 21,201 rows, 20,649 are missing and the 552 present ones run from 0.1 to 99.1, so a missing value encodes "no rain". Shipping NaN is lossless for trees but undocumented.
   * **Mildest remedy:** a note saying a missing precipitation means no recorded rain (0 mm). Optionally fill 0, a curator call.
3. **Writing: claim 10, in the record.** The 2026-11-04 CC line says "pickup to arrival at pickup" instead of "at destination".
   * **Mildest remedy:** a one-word fix in the record.
4. **Quality (not a refutation): claim 21a.** "Measured every three hours" is the source's wording, but no 3-hour step shows in the data: 5.65 distinct temperatures per 1-h block of one date. Nothing to change. Optionally add "(as the source says; anonymised values vary within an hour)".

**Untested, ranked**

1. **P4: claims 14b (99.4% of test riders seen in Train) and 16 (`No_Of_Orders` ≥ Train+Test orders).** Both need Test.csv and Riders.csv, which are not in the warehouse.
   * **What it changes:** only the wording of the evidence. The exclusion is still supported by the source's own definition ("delivered", "days since first order", no as-of date), and Rider Id already enters as a categorical.
   * **Remedy:** download Test.csv and Riders.csv into the warehouse (the definition already asks to keep them) and re-run both counts, or phrase both as "per the 2026-10-29 audit".
2. **P5: claims 23 and 26 (Train+Test part) and 30.** These are the Test.csv size and the adjacency over 28,269 orders. My Train-only rerun agrees in direction (0.627% vs 0.731%).
   * **Remedy:** same as above.
3. **P5: sibling `_2` duplicate (32).** Accepted on the record's provenance (PROV-4), with no data comparison.
   * **Remedy:** none needed unless that record is reopened.

**Verdict for the curator.** Validity: USE-3, USE-5 (approximate fit, late marks documented), LEAK-10 and LEAK-16 hold; SPLIT-8 holds. LEAK-38 is the wrong rule for Distance: the field was tested and cleared under EV-1, so change the note's wording only. Value: MET-1 to MET-4 hold, with RMSE in seconds confirmed on the Zindi page and every fold scorable; TP: LightGBM skill +0.40. Quality: the meaning of missing precipitation is undocumented (CLEAN-10, Should). Ready, after the note edits. `build_stale` remains the curator's call to rebuild.

</details>

<details><summary>Column audit</summary>

**Column audit: sendy_logistics_challenge (column-auditor, second pass, 2026-11-04)**

**Answer to focus.md.** The focus file asks nothing beyond the standard panel. No column of the shipped frame needs to leave and none is miscleaned. The one open timing risk is `Distance (KM)` under LEAK-38. It now has a partial decisive test (problem 1), and that test points away from a trip measurement between the rider's marks. I have one cleaning question for the curator (problem 3).

I loaded the frame through `dataset_io.from_definition`: the definition's own frame, 21,201 rows × 20 columns. No container was used, because the README's build is stale. I re-ran the dtype probe, and it flags one column: `Platform Type`, as `numeric_levels`. Prediction point: the rider has marked the pickup.

**Column table**

| Column | Meaning (codebook, as summarised in the record) | Known at pickup? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| User Id | customer id (3,186 levels) | yes, at placement | category; an id code | fine | CLEAN-14, USE-10 |
| Rider Id | rider who confirmed the order (924 levels) | yes, at confirmation | category | fine | CLEAN-14, USE-10 |
| Platform Type | platform used to place the order, "4 types", no words per level | yes | category, codes 1-4 (3: 18,054; 1: 2,147; 2: 980; 4: 20). The probe's `numeric_levels` flag is answered: this is a code with no words, so a category is correct | fine | CLEAN-12, CLEAN-14 |
| Personal or Business | customer type | yes | category, 2 levels | fine | CLEAN-14 |
| Placement - Day of Month | day of month of the order | yes | int, 1-31; a cycle, so a number | fine | CLEAN-14 |
| Placement - Weekday (Mo = 1) | weekday of the order | yes | int, 1-7; a cycle | fine | CLEAN-14 |
| Confirmation - Day of Month | day of the rider's confirmation | yes | int; equals placement's in 21,199 rows and differs in 2, so it is not an exact copy | fine | CLEAN-5 |
| Confirmation - Weekday (Mo = 1) | weekday of the confirmation | yes | int; differs from placement's in 2 rows | fine | CLEAN-5, CLEAN-14 |
| Distance (KM) | "distance from Pickup to Destination" | timing undocumented; measured below | int, 1-49 | kept leak risk, now narrowed (problem 1) | LEAK-38, LEAK-37 |
| Temperature | °C at placement, measured every 3 h | yes | float, 11.2-32.1; 4,366 missing. Missingness does not follow the outcome (mean label 1,523 vs 1,566 s) and is spread over all hours. Values are jittered, probably by the anonymisation: up to 5 distinct values within one hour block | fine | CLEAN-10, LEAK-10 |
| Precipitation in millimeters | mm at placement, measured every 3 h | yes | float, 0.1-99.1; 20,649 missing (97.4%) and no zeros | question (problem 3) | CLEAN-10, CLEAN-12 |
| Pickup Lat / Pickup Long | pickup address | yes, at placement | float. These are address coordinates, not the GPS position at the pickup mark: on the 547 late-marked legs the median straight-line distance is still 2.64 km | fine | LEAK-10 |
| Destination Lat / Destination Long | destination address | yes, at placement | float | fine | — |
| Placement - Seconds after midnight | clock parsed from `h:mm:ss AM/PM` | yes | int32, 436-82,021; a cycle. With the day columns it is lossless | fine | CLEAN-12, CLEAN-14 |
| Confirmation - Seconds after midnight | same parsing | yes | int32. In 5 rows it precedes placement by 1-42 s, which is documented and kept | fine | CLEAN-11 |
| Arrival at Pickup - Seconds after midnight | same parsing | yes | int32; it is never earlier than confirmation (0 rows). Its day and weekday equal confirmation's in every row, which `_clean` asserts | fine (problem 2) | CLEAN-5 |
| Pickup - Seconds after midnight | the pickup mark, which is the prediction point | yes, by definition | int32; it is later than arrival at pickup in every row (0 rows earlier or equal) | fine (problem 2) | — |
| Time from Pickup to Arrival (target) | seconds from the pickup mark to the arrival mark | — | int, 1-7,883; asserted to equal the clock difference in every row; no transform, matching the source's RMSE | fine; 547 legs of 10 s or less kept by the curator's call | CLEAN-11, MET-4 |

Dropped raw columns, all correctly:
- `Order No`: a unique id with no chronology (CLEAN-3).
- `Vehicle Type`: constant (CLEAN-5).
- The 4 copies of day and weekday for arrival at pickup and pickup, asserted equal to confirmation's (CLEAN-5).
- The 3 arrival-at-destination fields, which make the label (LEAK-10).
- Riders.csv, which was never joined because it is not as-of (LEAK-10).

**Problems, ranked by principles.md**

**1. P4, LEAK-38 (Should) against LEAK-37/USE-6: `Distance (KM)`. Kept leak risk, narrowed by a new test. Remedy: keep it and update the note.**

The late pickup mark gives a natural experiment. On the 547 legs of 10 s or less, the rider marked pickup at the destination. If `Distance (KM)` were tracked between the pickup mark and the arrival mark, those legs would show about 0-1 km. They do not:

| | Late-marked legs (≤10 s, n = 547) | All other legs (n = 20,461) |
|---|---|---|
| Distance, median / mean | 5 / 6.6 km | 8 / 9.6 km |
| Ratio to straight-line distance | 1.59 | 1.47 |
| Correlation with straight-line distance | 0.958 | 0.952 (all rows) |
| Residual on a quadratic in straight-line distance | −0.013 km | +0.0003 km |

So it is not a distance measured between the two marks. It behaves like a route distance between the two addresses, which can be computed from coordinates known at placement.

It does not rule out a GPS total of the whole trip measured after delivery. The partial correlation of the distance residual with the label, given straight-line distance, is 0.159, and both a road-routing distance and a travelled distance would produce that.

The mildest remedy: keep the column and add this measurement to the `Potential leak, kept on purpose:` bullet as EV-1 evidence ("the between-marks reading is refuted; a post-delivery GPS total is not excluded"). No change to the data. The curator decides whether this already meets the note's "revisit" condition.

**2. P4, LEAK-1/LEAK-10: the late-mark artefact can be read from the inputs. Fine, with an optional note.**

The pickup wait (pickup clock minus arrival-at-pickup clock) separates the late-marked legs:
- Median wait is 1,505 s on legs of 10 s or less, against 476 s on the others.
- The share of legs of 10 s or less rises from 0.0% when the wait is 60 s or less to 14.8% when it is over an hour.

These inputs exist at the mark, so this is not a leak under the stated prediction point, and its measured weight is negligible. With LightGBM on repeat 0 (3 folds):

| Variant | RMSE | Mean prediction on legs ≤10 s |
|---|---|---|
| All features | 760.5 | 841 |
| Without the arrival-at-pickup clock | 760.7 | 847 |
| Without the arrival-at-pickup and pickup clocks | 760.8 | 851 |

The legs of 10 s or less are 4.6% of the squared error. No action is needed. One sentence in the label-anomaly bullet would be enough if the curator wants it.

**3. P7, CLEAN-10/CLEAN-12 (Should): does a blank `Precipitation in millimeters` mean 0 mm? Question for the curator.**

Evidence that a blank means no rain:
- None of the 552 recorded values is 0; the smallest is 0.1.
- Whenever temperature is missing, precipitation is missing too (all 4,366 rows), which marks the rows with no weather reading at all.
- 16,283 rows have a temperature but no precipitation, which suggests a blank there means no rain.

Evidence against:
- In 121 of the 172 day/weekday/hour blocks that have any precipitation, some orders carry a value and others are blank.
- That mix could come from the anonymisation jitter, or from (day, weekday) pairs that recur across months. The data cannot settle it.

Filling 0 where a temperature exists changes nothing measurable (RMSE 761.4 against 760.5). The mildest remedy is no change to the data, plus a note in the weather bullet: "blank precipitation with a temperature most likely means none recorded (no zeros in the 552 values)". The curator may choose the fill if VariableDefinitions.csv or the winners' write-ups confirm it; the file is not in the warehouse, so I could not check.

The heavy values (35 rows above 40 mm, up to 99.1) cluster on four calendar days, from 08:00 to 10:00, with matching temperatures. They are real events, not a sentinel. Keep them.

**4. P4, SPLIT-8: forced IID. Already accepted, no new action.**

Day-of-month and weekday together, plus the jittered weather, place each order on a calendar day. With random folds, orders from the same day sit on both sides of the split, so the score includes that day's shared conditions. This is part of the optimism the `ForcedIIDFromTemporal` tag and the fit "approximate" already cover.

**Judgment record**

Verdict: no column change required.

Validity:
- LEAK-10 holds for all 19 inputs.
- LEAK-38 is kept, and its mechanism is narrowed (problem 1).
- LEAK-1 holds: the late-mark wait is known at the mark and weighs nothing (problem 2).
- SPLIT-8 is accepted.

Quality:
- CLEAN-14 holds for all dtypes, including `Platform Type` as a code, the weekdays and clocks as cycles, and the ids as categories.
- CLEAN-5 holds for the drops.
- CLEAN-10 has one open question (precipitation blanks).

For the curator:
- Issue 1: update the `Distance (KM)` note with the late-mark test.
- Issue 3: add a note on precipitation blanks, or fill 0 if the source confirms it.

</details>

<details><summary>Split audit</summary>

**Verdict: the split is right, with notes.** Three repeats of three random folds, tagged `ForcedIIDFromTemporal` under SPLIT-8, fit the use case. I found no problem that needs a re-split.

**Answer to `focus.md`.** The focus file asks nothing beyond the standard panel. On the one split point it lists, forced IID from temporal under SPLIT-8: it holds, and I have now measured its cost. The data does carry a partial month code that the definition does not mention. It cannot be put in time order, and holding out by it costs nothing (750.1 against 748.8 s RMSE).

**Regime against the use case (P3, P4)**
- **The use case.** Sendy gives an arrival time once the rider has the parcel, and plans the rider's next orders from it. That is a stream of orders over time, made for riders and customers it already knows. So the natural regime is temporal, with known entities (USE-10).
- **Riders and customers are known at pickup.** Under SPLIT-4 they are features, not groups.
  - On the shipped folds, 99.2–99.4% of test orders have a rider seen in training. That matches the unverifiable claim of 99.4% for Zindi's `Test.csv`, which suggests Zindi's own test file was a random draw from the same period.
  - 88.8–89.5% of test orders have a customer seen in training.
- **No time order exists.**
  - There is no time column, and `Order No` holds no order: 0.669% day/weekday adjacency against 0.693% at random. I did not re-run this; it is in the record.
  - SPLIT-14 needs at least 3 windows, which cannot be built, so SPLIT-8 applies. The closest regime that keeps every row is IID.
- **Grouped splits are not called for.** The hidden-group probe has no hits, and no column is an entity that new orders would lack (SPLIT-29 and SPLIT-30 do not trigger). Near copies are 0.2% of rows, in pairs only. Exact copies are 0%.
- **Not applicable under IID:** the label delay (legs of at most 7,883 s), the gap and SPLIT-9.

**What I measured**
I loaded the frame through `dataset_io.from_definition`, with no build. Runs used LightGBM with 400 trees, learning rate 0.03 and 2 threads. Skill here means 1 − RMSE / dummy RMSE, which is why it is lower than the probe's R² of 0.398.

| Split | RMSE (s) | sd | Dummy | Skill |
|---|---|---|---|---|
| Shipped random 3×3 | 752.5 | 16.6 | 987.2 | 0.238 |
| Random 7-fold (same size as the period hold-out) | 748.8 | 8.4 | 987.2 | 0.241 |
| **Period hold-out: 7 month classes, leave one out** | **750.1** | 42.7 | 977.2 | 0.233 |
| Calendar-day groups (month class × day), 3-fold | 755.1 | 5.1 | 987.2 | 0.235 |
| Customer (`User Id`) groups, 3-fold | 765.1 | 5.3 | 987.2 | 0.225 |
| Rider (`Rider Id`) groups, 3-fold | 791.0 | 2.5 | 988.4 | 0.200 |

**Problems, ranked by `principles.md`**

**1. P4, SPLIT-8 (Must, met): the splits comment says the release has no month, but it carries a month class. Severity: a note.**
- **What the data shows.**
  - Placement weekday minus day of month, mod 7, is the weekday each month started on.
  - All 7 values occur, with 1,121 to 4,857 rows each. Every class covers all days 1–31, with the expected weekend dips.
  - Each class is one or more calendar months that started on the same weekday.
- **It cannot be put in time order.** Day 31 is absent in class 3 and nearly absent in class 4 (2 rows), so those are mostly 30-day months. Fitting runs of consecutive months to that pattern, several runs fit equally well. Examples are 2017-01 to 2017-11 and 2018-04 to 2019-02. Some classes are thinly filled at the month end (class 5 has 4 orders on day 30), which points to an extract that starts or ends mid-month.
- **So SPLIT-14's windows still cannot be built,** and the forced-IID call stands.
- **SPLIT-8's measured cost.** SPLIT-8 asks for the cost against valid windows where the data has any. There are no valid windows, but leaving out one month class tests unseen calendar months:
  - RMSE 750.1 against 748.8 under random folds of the same size, a gap of 1.3 s.
  - Per class, 95.6–99.1% of test orders still have a seen rider.
  - Holding out whole calendar days costs 2.6 s against the shipped split (755.1 against 752.5), so same-day orders on both sides do not inflate the score.
- **Mildest remedy:** no re-split. Add one sentence to `splits_comment`: the day of month and weekday give a month class that cannot be ordered; holding out one class gives RMSE 750.1 against 748.8 at random; revisit if dates are recovered. Optionally reword "no month or year" in `task_summary.split` to "no month order or year".

**2. P4, SPLIT-4 and USE-10 (Must, met): riders and customers recur on both sides. Severity: none, the split is right.**
- Holding out riders costs 38.5 s (791.0 against 752.5; skill 0.200 against 0.238). Holding out customers costs 12.6 s.
- These gaps measure a cold start, which is not the use case: dispatch knows the rider at pickup. The gap size never decides (SPLIT-4, SPLIT-30), and the probe's rider gap of 0.026 is not a hit.
- **Remedy:** none. If the curator wants a "new rider" variant, it is a SPLIT-31 candidate, not a fix.

**3. P4, SPLIT-19 and SPLIT-5 (Should): the source's own split cannot be followed.**
- Zindi's test labels are not released, and `Test.csv` is not in the warehouse.
- Indirectly, the 99.2–99.4% seen-rider share under random folds matches the claimed 99.4% for Zindi's test file. Random folds over the training file are therefore the closest available copy of the source's split.
- **Remedy:** none. A curator with access could confirm this from `Test.csv`.

**Not checked**
- The sibling `sendy_logistics_challenge_2`.
- The Zindi pages, which would need web access.
- `Test.csv` and `Riders.csv`, which are not in the warehouse.

Judgment record: SPLIT-1, -4, -8, -14, -29 and -30 hold, and USE-10 holds (a known entity). SPLIT-8's measured cost is now available (1.3 s RMSE) and should be written into `splits_comment`.

</details>

<details><summary>Domain practitioner</summary>

**Focus answer.** `focus.md` sets no question beyond the standard panel. The answer to it: as the Sendy dispatcher, I would use this task, and it holds up as the source's own ETA-at-pickup task. Fit is **approximate**, and that is the right call. The metric scores my decision: **yes**, with one caveat noted below.

**Fit: approximate (USE-8)**
It is the source's own decision: at pickup, an ETA for the customer and for planning the rider's next jobs (Zindi: "enhance customer communication… resource management and planning for order scheduling"). It is made at the right moment with inputs known then. Two things keep it approximate. The label is the rider's own app marks, and some of them are wrong. And random folds over one release stand in for next month's orders. I agree with Lennart's 2026-11-04 call: forced IID (SPLIT-8) keeps it approximate, as in beMTPL97 and freMTPL2. USE-9 does not apply, because no other use case would make the random split direct.

**Answers in the actor's voice**
1. **Inputs at pickup.** I have every shipped input when the rider marks the pickup: the customer, the rider, platform, all clocks up to pickup, coordinates and weather. `Distance (KM)` is most likely the route distance I quote at booking. Press reports say Sendy prices upfront from route distance. The column is integer km, and its median ratio to the straight-line distance is 1.48, which is a typical road-to-straight ratio (my run). If so, it is a legitimate USE-6 input and not a leak. The LEAK-38 note stays honest, but my evidence leans toward "known at placement". **Missing, though I would always have it:** a routing engine's travel time (the 2nd-place winner added ArcGIS fastest and shortest route times), the calendar date (month, holidays, school terms) and live traffic. I also lack as-of rider history (tenure, rolling speed); `Rider Id` partly stands in for it.
2. **Target.** I act on this quantity directly: the seconds from pickup to arrival. For planning, I want a point estimate that is the conditional mean, because the legs of a rider's schedule add up. For the customer message I would rather have a median or an upper quantile. It is not a proxy, apart from the mis-marked rows (gap 2).
3. **Row and test.** One row is one order, which is one ETA I issue. In production, 94.1% of test rows have a rider seen at least 5 times in training (fold 0, my run), and the record says 99.4% of the Zindi test orders have a seen rider. So "known rider" matches what I face (USE-10). What the test does not represent is next month. Day of month spans about 7 weekdays per value, so the release covers many months. Dropping both day-of-month columns changes RMSE from 761.3 to 762.0, so shared days do not inflate IID scores.
4. **Would I use it?** Yes, as a baseline. Out-of-fold LightGBM (repeat 0) gives RMSE 761.3 against a dummy 987.2, and MAE 523.9 against 732.1 for a median guess. That is about a 9-minute mean miss on a 23-minute median leg. I would trust it more with a routing-engine time as an input and a forward-in-time check. I would distrust it for the late-mark riders (gap 2).
5. **Metric.** See below.

**Gaps, ranked by how much they change the task**
1. **No forward-in-time test (SPLIT-8, forced IID).** I deploy on next month's orders, with new riders, rain seasons and route changes. Random folds cannot show drift. The release has no month or year, and `Order No` holds no order: 0.669% adjacency against 0.693% at random. This is the main reason the fit is approximate, and it cannot be fixed from this release.
2. **Label noise from late pickup marks (USE-5, CLEAN-11).** 547 legs are 10 s or less (2.6%) and 740 are 60 s or less (3.5%). The winners describe these as riders who "forgot to mark that he took the order and did it just before it was delivered". Two winners built separate outlier classifiers for them. On these rows, by the time the rider marks the pickup the customer already has the parcel, so no ETA decision depends on them. Scoring them rewards spotting forgetful riders. I measured the effect as small:
   - The 60 s-or-less rows carry 6.5% of the squared error while being 3.5% of the rows.
   - RMSE is 749.3 on the other rows against 761.3 on all rows.
   - `Rider Id` carries the habit: without the IDs, RMSE goes from 761.3 to 769.5, and the mean prediction on the 10 s-or-less legs rises from 850 to 1,040.

   Keeping them as source labels (CLEAN-11) is acceptable. A USE-7 cut like the one in nyc_taxi and pkdd is not available, because here the cut would rest on the label, not on an input.
3. **No routing-engine ETA among the inputs (USE-6).** In practice my model would refine a Google or OSRM travel time, and the winners rebuilt one from ArcGIS. Without it the task is "learn Nairobi travel times from 21k orders". It is still a real task, just a harder one than the deployed version. The release has no such column, so this goes in the notes only.
4. **`Distance (KM)` timing (LEAK-38).** It is worth 28 s of RMSE (789.3 without it, 761.3 with it). The pricing evidence makes this a likely USE-6 input rather than a leak. The comment could cite that evidence. One wording point: USE-8 asks that a potential leak kept on purpose be named as kept in `fit_reason`, and the current `fit_reason` does not mention it.
5. **Weather at placement, not at pickup.** For a multi-day confirmation this lags by up to 49 h. That affects two rows and does not matter.

**What a domain expert would change**
- In `fit_reason`, add one clause naming `Distance (KM)` as a potential leak kept on purpose (USE-8 wording). Optionally cite the upfront distance pricing in the LEAK-38 comment as evidence for "known at placement".
- In `task_summary.predicted` or the notes, state that on the late-marked legs the parcel had already arrived when pickup was marked, so they test the detection of mis-marking, not an ETA. Use the numbers above. No row change is needed.
- Nothing more to do in this release. A routing-time input and real dates would need a new source.
- Record hygiene only: the record's `source_links` points to zindi.africa, which now 301-redirects to the zindi.world URL the definition uses.

**Metric: yes (MET-1, MET-4)**
RMSE in seconds per order is Zindi's leaderboard metric ("The error metric for this competition is the Root Mean Squared Error"), so MET-4 says to declare it. It scores the unit I act on, one order's ETA, in the scale I act on (MET-3: seconds, no transform). It elicits the conditional mean, which is what I need for planning rider schedules, where leg times add up. The tail does not make it fragile: the top 1% of rows carry 21.4% of the squared error, and the late-mark rows only 6.5%. MET-6 to MET-9 concern classification thresholds and do not apply.

If I chose without the source's lead, I would use MAE for the customer-facing message. It equals the average miss a customer feels and is less sensitive to the forgetful-rider rows. But MET-4 holds, because I have no evidence that RMSE is biased or wrong for this use case, and the 2024 Lusaka ETA precedent kept RMSE ("ok keep minutes"). So: keep RMSE.

**Sources**
- `dataset.py`, `README.md`, the record, the panel's prep report, claims list and decision register (precedents: lusaka, nyc_taxi, pkdd, brazilian_ecommerce)
- My runs (scripts in the run folder; LightGBM, shipped splits, repeat 0)
- [Zindi competition page](https://zindi.world/competitions/sendy-logistics-challenge): target, use, RMSE
- [Zindi winners page](https://zindi.world/learn/meet-the-winners-of-the-sendy-logisitics-challenge): late marks, outlier classifiers, ArcGIS route times, Poisson/Tweedie losses
- [Nation: How Sendy is using machine learning](https://nation.africa/kenya/business/technology/how-sendy-is-using-machine-learning-to-transform-logistics-3445770) and [Disrupt Africa 2016](https://disrupt-africa.com/2016/04/13/kenyan-e-courier-startup-sendy-expands-to-kisumu/): price quoted upfront from distance (as summarised by search; not read in full)

Rules cited: USE-5, USE-6, USE-7, USE-8, USE-9, USE-10, SPLIT-8, CLEAN-11, LEAK-38, MET-1, MET-3, MET-4.

</details>

<details><summary>Blind review</summary>

**Verdict:** Include with small changes. This is a real, non-trivial last-mile ETA regression on real courier orders. I found no target leak: the "Arrival at Destination" timestamps have been dropped. But about 3.5% of the targets are clearly rider-logging artifacts, and a few columns need small type and missing-value fixes.

**What the task is.** Sendy, a Nairobi logistics platform, predicts how long a bike courier will take from pickup to drop-off. The source states the target is "Time in seconds between 'Pickup' and 'Arrival at Destination'". The data "only includes direct orders (i.e. Sendy 'express' orders) with bikes in Nairobi" and is "fully anonymized while preserving the distribution". The prediction is made once the parcel is picked up, and it drives the ETA shown to customers and dispatch planning. That is a real use. The table matches the Zindi Train.csv: 21,201 rows. `Order No` and the constant `Vehicle Type` (Bike) are gone, and so are the "Arrival at Destination" day, weekday and time, which the source says are missing in the test set.

**Concerns, most serious first**

1. **Target noise from riders tapping "delivered" right after pickup.**
   - Evidence:
     - 522 rows have a target under 10 s and 740 rows under 60 s. The 1% quantile is 3 s and the minimum is 1 s.
     - Those 740 rows cover 1–26 km (median 5 km).
     - 793 rows imply speeds above 200 km/h.
     - In these rows the wait between arrival at pickup and pickup is much longer: median 1,480 s, against 476 s for the other rows. This fits riders logging "Pickup" late and then confirming delivery at once.
     - The rows come from 250 riders. Some riders produce them over and over: Rider_Id_515 has 39, Rider_Id_39 has 34, and 11 riders have more than half of their orders under 60 s.
   - Why it matters: under RMSE these mislabels weigh heavily. Part of the noise can be learned from the rider ID and the pickup-wait pattern, so the benchmark partly rewards modelling logging habits rather than travel time.
   - Change: either drop rows with target < 60 s (or with implied speed > 80 km/h), or keep them and say so in the metadata. I lean towards removing them. If they stay, describe the task as "as-logged ETA".

2. **`Precipitation in millimeters` is 97.4% missing (20,649 of 21,201).** The values present run from 0.1 to 99.1, with no zeros. So NaN almost certainly means "no rain recorded", i.e. 0, not "unknown". Change: fill with 0, or add a rain indicator. As it stands, models that treat NaN as unknown get a misleading signal. `Temperature` is 20.6% missing (4,366 rows). That looks like genuine missingness (the source says it is measured every three hours), so leaving it as NaN is fine.

3. **The rider table was not merged.** Riders.csv (No of Orders, Age, Average Rating, No of Ratings) is part of the public source. These are snapshot aggregates, probably taken at the end of the data period, so they could leak a little future information. Leaving them out is defensible. It should still be documented, because the original task includes them.

4. **Type and encoding issues.**
   - `Platform Type` is stored as int64 but is a nominal code (1–4). Code 4 has only 20 rows. It should be categorical.
   - `User Id` has 3,186 levels and `Rider Id` has 924, both stored as categoricals. That is fine.
   - Placement and Confirmation "Day of Month" and "Weekday" are near-duplicates (they differ in 2 rows). Harmless, but redundant.
   - Month and year are absent in the source. So "Day of Month" is a cyclic feature and not a timeline.

5. **The split.** The source has no month or year, so a time-ordered split cannot be built. A random IID split is therefore the only option, and it is acceptable.
   - Riders and users repeat across folds: on average 23 orders per rider, and the top user has 645 orders. That matches deployment, where the same riders and clients keep using the platform.
   - With rider-grouped CV, R² falls from 0.41 to 0.36. The rider ID helps, but the score is not driven by memorising riders.
   - There are no duplicate rows, even after excluding the IDs and the target.

**Signal and difficulty** (LightGBM with defaults, 5-fold CV)

| Features | Result |
|---|---|
| All features | RMSE 757 against a target std of 987; R² 0.41 |
| Distance alone | R² 0.34 |
| Distance + coordinates | R² 0.38 |
| No IDs | R² 0.39 |

- Feature importance by gain: Distance, then Rider Id, User Id and the coordinates.
- The task is noisy but not trivial. The ID categoricals and the geography leave room to separate methods.
- 21k rows is plenty to score on.
- The Zindi leaderboard reported RMSEs in a similar range, around 700–750. I remember this rather than having checked it.

**Leakage check.** Placement, Confirmation, Arrival at Pickup and Pickup times all fall at or before pickup; their order holds in 99.97% of rows. All of them are known when the ETA is requested at pickup. Weather is recorded at placement. Distance is the planned pickup-to-destination distance, so it is known in advance. I found no post-outcome column.

**What I could not check**
- The full VariableDefinitions.csv text and the leaderboard numbers: I only saw a summary of the data page, not the files.
- Whether the "Distance (KM)" column is planned or actually travelled. The source says "distance from pickup to destination", so I take it as planned.
- Whether the Zindi test labels (never released) share the near-zero artifact.
- The real date range of the orders.

</details>

<details><summary>Task gamer</summary>

**Verdict:** this task can barely be gamed. The only real leak, the same rider's next order on the same day, improves RMSE by about 3.4, against a noise spread of about ±0.3. The bigger issue is in the labels: about 3.7% of targets are under 100 s because riders logged the pickup only when they delivered, and the delay between arriving at pickup and logging it gives these rows away.

Honest baseline (untuned LightGBM on `features()`): mean RMSE **762.41** over the 9 splits (731.7–782.3). Adding a column of random numbers, 3 seeds: 762.09–762.88.

Better honest model ("honest+": time gaps between the logged events, straight-line distance, time since the rider's previous pickup today, light tuning): mean **744.21** (708.1–762.7). With a random column, 3 seeds: 743.88–744.41.

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Same rider's next order that day: its arrival-at-pickup, confirmation, placement and pickup times minus this order's pickup, plus the rider's order count for the day | seq, combo | 762.41 / 744.21 | 759.08 / 740.77 | 3.3 / 3.4 (−0.2 to 7.0) | No. The rider's later orders do not exist yet at pickup. | Drop rows, or split by rider-day, so a rider's later orders are not visible in the features |
| 2 | Pickup-wait as a detector of fake short targets: wait = pickup time − arrival-at-pickup time | wait | 762.41 | 753.94 | 8.5 (4.8–12.1) | Yes as a timestamp. No in meaning: for these rows the "pickup" click happened at delivery. | See the label flaw below |

**1. Rider's next order.** For 28% of rows the same rider has a later order on the same day (rider and day matched on day of month plus weekday). The next order's arrival at pickup falls after this order's arrival for 95% of rows, so it is a loose upper bound. Its correlation with the target is only 0.08. That is why the gain is small: 3.4 on honest+, about 10× the noise spread, positive in 8 of 9 splits. The mildest fix is to compute nothing across rows. The kit has no such features, so the leak only exists if a participant builds it. A rider-day group split would close it.

**2. Short targets and pickup-wait.** One prize winner said these rows come from riders who "forgot to mark that he took the order and did it just before it was delivered". The data agrees: for targets under 100 s the median wait is 1,478 s, against 476 s for other rows. Adding `wait` cuts RMSE on these rows from 1,037 to 913, and on the other rows only from 750 to 747. A model triggered at the logged pickup click would see the same wait, so as a feature it is available. What it actually predicts, though, is a recording error and not a delivery time.

**Flaw that hurts an honest model**

| What is wrong | Honest choice | Baseline score | Honest-choice score | Fix to the task |
|---|---|---|---|---|
| 3.7% of labels (787 rows) are 1–99 s logging artefacts, and they stay in the test folds | Train on rows with target ≥ 100 s only | 744.21 (honest+) | 755.67 (worse) | Drop or flag targets under about 100 s, or under about 60 s/km, in both train and test |

A deployed ETA model would drop or relabel these rows. Here that loses 11.5 RMSE, because the test folds score against the artefacts. The benchmark therefore rewards modelling the logging error: the two-model "outlier classifier × regressor" designs in the winning write-ups, and the `wait` feature. Removing those rows from the data, or at least from the test side, is the mildest fix.

**Attacks that found nothing**
- **Formats:** latitude decimal counts (4–7) have no clear link to short targets: 2.7–5.3% across the populated decimal counts, against 3.7% overall. Temperature always has one decimal. Missing temperature: 4.8% short vs 3.4%. Missing precipitation (97% of rows): 3.8% vs 2.0%. Weak and plausible, no recording split.
- **Order and ids:** target against row position r = 0.0001; next-row autocorrelation 0.006.
- **Copies:** no duplicated feature rows. Same rider, day and pickup second: 1 pair. Same user, day and placement second: 1 pair.
- **Neighbour labels from training rows**: previous order's label when it ended before this pickup, 762.47; next order's label, 762.94; mean label of the same user/day/destination group, 761.92. All within noise of 762.41.
- **Previous-pickup gap, rider's order rank and count for the day:** 762.11 / 762.28, both noise.
- **Transforms over all rows, train-vs-test drift:** there are no scaled or rank columns, and the split is random rows, so neither applies.

**Honest signal, not exploits**
- Time gaps between logged events and straight-line distance: 762.4 → 750.4. Removing User and Rider Id from honest+ costs 14.3 (744.2 → 758.6); rider identity is known at pickup.
- The winners also used target encoding, Poisson or Tweedie loss and ArcGIS route times. I did not replicate these.

**Could not check**
- The Zindi source files need a login, so I could not compare the kit with them. I infer that the "Arrival at Destination" columns (the target's source) and the Riders.csv attributes were dropped; neither appears in the kit. I did not test looking rows up in the published file.
- The data covers more than one month and only day of month and weekday are given, so my rider-day key may merge different dates. The real calendar date would settle this.
- I did not read the forum threads beyond the winners' blog.

Sources: [Meet the winners](https://zindi.africa/learn/meet-the-winners-of-the-sendy-logisitics-challenge), [competition page](https://zindi.africa/competitions/sendy-logistics-challenge), [discussion 599](https://zindi.africa/competitions/sendy-logistics-challenge/discussions/599).

</details>

<details><summary>Precedent check</summary>

**Precedent check: `sendy_logistics_challenge` (second pass, 2026-11-04)**

**What focus.md asks.** It names no question beyond the standard panel. The direct answer: the 2026-11-04 decisions follow precedent. Two of them should go back to Lennart. The 547 near-zero pickup legs are kept, which departs from the taxi ETA filters, and the stated reason does not quite separate the cases. Two orders that end within 100 m of their pickup are kept, which departs from USE-7 with no reason given. The register has no flag on any `sendy` decision. Nothing found would break a higher-ranked Must.

---

**1. CLEAN-11: the 547 legs of 10 s or less are kept (Lennart, 2026-11-04). Departs, with a stated reason that is incomplete.**

- **Closest precedents:**
  - `nyc_taxi_trip_duration_1m` drops trips under 30 s as "not rides" and trips over 3 h as broken clocks (panel 2026-10-20, shipped 2026-10-22).
  - `pkdd_15_taxi_trip_time_prediction_ii_1m` drops trips under 30 s, and trips whose straight line runs faster than 120 km/h as a GPS jump (2026-10-26).
  - `delivery_eta_1m` and `cooking_time_1m` drop times under 1 min, as TabReD's preprocessing does.
  - `qsar_tid_11`: an impossible target is set missing and the row leaves (2026-10-21).
- **Sendy in numbers (my run on Train.csv):** 547 legs of 10 s or less, 677 under 30 s, 803 faster than 120 km/h and 834 faster than 100 km/h, all kept.
- **What the stated reason covers.** "The source's labels" separates Sendy from the TabReD pair: TabReD itself dropped those rows, Zindi did not. It does not separate Sendy from nyc. Kaggle scored nyc's under-30 s and over-3 h trips too, and they were still dropped.
- **Facts that do set Sendy apart (measured here):**
  - The short legs are real deliveries, not non-rides. Their median straight line is 2.64 km and none ends within 100 m.
  - The late mark shows in the inputs. Pickup clock minus arrival-at-pickup clock has a median of 1,505 s on the short legs against 480 s on the rest. So the label matches the pickup clock the model sees.
  - nyc's broken over-3 h clocks could not be seen from the inputs.

> **Consistency check (AI, 2026-11-04):** your call on sendy_logistics_challenge (547 legs of 10 s or less and 834 legs above 100 km/h kept as the source's labels, CLEAN-11) differs from nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m (2026-10-20/26: under 30 s dropped, over 3 h dropped as broken clocks, over 120 km/h dropped as GPS jumps), whose labels were also the competitions' labels. What sets Sendy apart?
> (a) The short legs are real deliveries (median 2.64 km in a straight line, none within 100 m), and the late pickup mark shows in the inputs (pickup minus arrival-at-pickup has a median of 1,505 s against 480 s). So the label is the app's recorded quantity, consistent with the clocks the model sees. Record this as the distinguishing fact under CLEAN-11 (a Cases row of kind `exception`);
> (b) treat Sendy like nyc and pkdd (drop the legs under 30 s or above a speed cap);
> (c) reopen nyc's over-3 h clock filter to match Sendy;
> (d) change CLEAN-11 (an amendment on recorded app marks against physical durations).

**2. USE-7 (Must): two orders end within 100 m of their pickup and stay. Departs, with no reason given.**

- **Precedents:**
  - nyc and pkdd: the 100 m radius (Lennart, 2026-10-26, the Cases row of USE-7).
  - `2024_lusaka_mobility_prediction_hackathon`: Lennart applied the same radius the same day, 2026-11-04 ("drop them, this is not a relevant prediction goal here imo").
- **The two Sendy orders:**

  | Order | Straight line | Source `Distance (KM)` | Pickup leg |
  |---|---|---|---|
  | Order_No_20080 | 0.089 km | 3 km | 1,309 s |
  | Order_No_7111 | 0.090 km | 4 km | 620 s |

  Neither the definition nor the record mentions them.
- **Why this is likely not a real USE-7 breach:** the source distance of 3-4 km says these parcels had a destination elsewhere, and the release's coordinates are anonymised. The destination input exists but is distorted. The effect is 0.009% of rows.

> **Consistency check (AI, 2026-11-04):** sendy_logistics_challenge keeps Order_No_20080 and Order_No_7111 (endpoints 89-90 m apart), while nyc_taxi_trip_duration_1m and pkdd_15 (2026-10-26) and 2024_lusaka_mobility_prediction_hackathon (2026-11-04) drop trips that end within 100 m (USE-7). What sets them apart?
> (a) Sendy's coordinates are anonymised, and the source distance (3 and 4 km) shows a destination away from the pickup. The input the ETA acts on exists, so the rows are task rows; add a line to `curation_comments`;
> (b) drop them as in the taxi tasks;
> (c) reopen the 100 m radius for anonymised coordinates;
> (d) amend USE-7's Cases row to say the radius applies to unmasked coordinates.

**3. LEAK-38: `Distance (KM)` kept with a `Potential leak, kept on purpose:` note (Lennart, 2026-11-04). Consistent, with a stated reason. The rule's scope wording lags behind its use.**

- **Pair with Lusaka:** Lusaka's "actual traveled distance" was dropped under LEAK-10 (Myunghwan, 2026-10-29). The source states it is measured over the completed trip, and Lusaka has a separate straight-line distance. Sendy's dictionary is ambiguous ("Distance covered ... from Pickup to Destination"), and the note says so. That is a fact which sets the two apart.
- **New evidence for keeping it (EV-1, my run):** I looked at the 386 exact repeated routes whose `Distance (KM)` varies (2,601 rows, legs over 60 s). Within a route, the change in distance does not track the target (r = 0.015, against 0.037 for the placement-to-pickup time). A distance actually travelled would make a detour lengthen the time. This argues against the distance-travelled reading, but only weakly: the distances are integer km and the coordinates are anonymised. It could go into the note as the "numbers" part.
- **Scope wording.** LEAK-38's text covers "Anonymised fields". `Distance (KM)` is a named field, and so is `ExpectedDelayNextExam` (medical_facility_operational_data, Lennart, the same day, LEAK-38). These are applications beyond the literal wording, not recorded exceptions. Rewording the scope to "anonymised or named fields whose timing cannot be tested" would turn this into a deliberate change. It is not yet the third case, but worth raising.
- **Tensions table:** the weak-transductive-leak row (sf_permit_time, home_credit) is about a different mechanism. Nothing contradicts this decision.

**4. The switch to the source's pickup task, which withdraws Myunghwan's duration and speed filter of 2026-10-29 and its exception to CLEAN-11 (Lennart, 2026-11-04). Consistent.**

- By the precedence rule, the newer curator decision beats the older one, and the line names what it withdraws.
- The exception was never entered in `cleaning_features.md`: no `sendy` appears anywhere in `.claude/skills`. So there is no Cases row to retract.
- The prediction point at pickup with the source's target matches the source-task rule (USE-5; zillow_prize).
- Note only: `claimed_by` is still Myunghwan, and his "yes, ship" line refers to the superseded definition.

**5. CLEAN-14: the placement and confirmation weekdays as numbers (Lennart, 2026-11-04). Consistent.**

- This is the cycle row of the CLEAN-12 table: a weekday or hour of a cycle ships as a number.
- Same treatment in rossmann_store_sales `DayOfWeek` and in Lennart's cycle rule of 2026-11-01, applied in 5g_energy_consumption, bad_customer_detection, miami_housing and mobile_churn.
- Dropping the arrival-at-pickup and pickup day and weekday as copies is guarded in `_clean`.

**6. Fit stays `approximate` under forced IID (Lennart, 2026-11-04, "(b)"). Consistent.** All 20 `ForcedIIDFromTemporal` definitions in the working copy have `fit="approximate"`, including beMTPL97, freMTPL2 and the ETA sibling food_delivery_time. Nyc, pkdd and Lusaka are approximate for their own reasons.

**7. SPLIT-8: forced IID from temporal (Myunghwan, 2026-10-29; carried into the 2026-11-04 task). Consistent.**

- The release has no month or year. The `Order No` sequence test gives 0.669% adjacency against 0.693% at random, so it holds no chronology.
- `splits_comment` says what full dates would change and to rebuild if a later release has them, as the Must asks.
- Precedents: account_debt_south_africa (2026-10-12), mobile_churn and the churn snapshots (2026-10-21), food_delivery_time.

**8. MET-4: the competition's RMSE in seconds, no transform (Myunghwan, 2026-10-29; re-checked by Lennart, 2026-11-04). Consistent.**

- It is the competition's metric (zillow_prize `mae` row).
- Nyc and pkdd use RMSLE with `log1p` only because their sources did.
- Lusaka kept RMSE in minutes the same day "as the other RMSE-scored ETA datasets".

**9. Riders.csv excluded. Consistent.** The timing is measured: every rider's `No_Of_Orders` is at least their orders in Train plus Test. LEAK-38 as amended on 2026-10-22 sends a measured mechanism to LEAK-10 and a drop (kick, expresso_churn_prediction). `Rider Id` and `User Id` as IID categoricals follow the related-entities note under LEAK-38 (SPLIT-31; amazon_employee_access, bank_marketing). The hidden-group gaps are small (+0.026 and +0.019).

**10. Not decisions, house consistency only:**

- Source link: the record has zindi.africa, the definition zindi.world. The repository itself is split: records 161 africa against 2 world, definitions 7 against 5. No rule decides it.
- `sendy_logistics_challenge_2` stays `No` with `Duplicate` (PROV-6/7). Not re-compared.

**Drift and amendments due:**

- **No drift.** Lennart's CLEAN-11 calls on 2026-11-04 (airqo zeros set missing with the rows kept, protein_model impossible values set missing, Sendy legs kept) all keep rows. The one drop that day (Lusaka) was under USE-7.
- **No amendment due.** No third exception of a kind on any rule Sendy touches. The register's amendment-due flags (CLEAN-19, SPLIT-10) and its drift flag on scaling over all rows (which lists the ETA siblings delivery_eta, maps_router_eta and cooking_time) do not involve Sendy.
- **Watch:** the LEAK-38 scope wording, with named fields in medical_facility and Sendy (item 3).

</details>

<details><summary>Advocate</summary>

**Opening brief for shipping `sendy_logistics_challenge` as defined (pickup to arrival, 21,201 rows, RMSE in seconds, 3×3 random folds)**

My case: no Must fails. The real problems the agents found are a Should departure on the short legs, two writing gaps and one undocumented missing-value meaning. Each is fixed with a note, and none needs a change to the data, the split or the metric.

**1. It is a real task: the source's own decision, made at the source's own moment (P3; USE-1, USE-5, USE-8, all Must, all met).**
- Evidence:
  - The Zindi page asks to predict the "delivery time from pickup to arrival at the final destination", and the target is "Time from Pickup to Arrival", in seconds.
  - `_clean` asserts that the label equals the destination clock minus the pickup clock in every row. The claim auditor confirmed the day delta is 0 in all rows.
  - The domain practitioner, as the Sendy dispatcher, would use the task.
  - The blind reviewer, working without our notes, also called it "a real, non-trivial last-mile ETA regression".
- `fit="approximate"` names both known gaps: the riders' own marks, and random folds standing in for future orders. All 20 `ForcedIIDFromTemporal` definitions use the same fit (beMTPL97, freMTPL2, food_delivery_time).
- Why it ranks first: P3 is the highest-ranked principle in play, and every agent agrees it holds.

**2. Every input is known at pickup. `Distance (KM)` is now measured as not a leak, so it is no longer an accepted risk (P4; LEAK-10 Must holds, LEAK-16 Must holds, EV-1).**
- Clock order: 0 rows break placement ≤ confirmation ≤ arrival at pickup ≤ pickup (5 confirmations precede placement by 1-42 s; documented). The 3 arrival-at-destination fields are dropped. Riders.csv stays out because the source defines its counts as "delivered" totals with no as-of date. Exact copies across the split: 0.
- `Distance (KM)`: three independent conditional tests each find no signal from the trip itself.
  - Within repeated routes, a change in Distance does not track a change in the label: r = 0.013 (n = 2,731; claim auditor) and r = 0.015 (n = 2,601; precedent checker).
  - On the 547 late-marked legs, the rider marked pickup at the destination. A between-marks distance would be about 0 there. Instead those legs carry the full route distance: median 5 km, ratio to straight line 1.59, residual −0.013 km.
  - The practitioner adds a supporting source: Sendy quotes prices upfront from distance.
- Concession: the column auditor is right that the data cannot rule out a GPS total recorded after delivery (partial r = 0.159 with the label, which a road distance would also give).
- Mildest remedy: reword the note so it reports the measurements. Fix 1 changes the note, not the data. LEAK-38 (Should) covers only fields whose timing cannot be tested, and EV-1 outranks it as procedure.

**3. The split follows the application, and its cost is now measured (P4; SPLIT-8 Must met, SPLIT-4, USE-10).**
- No time order can be built:
  - There is no month or year column.
  - `Order No` holds no chronology: 0.669% day/weekday adjacency against 0.693% at random, and 0.627% against 0.731% on Train alone.
  - The 7 "month classes" the split auditor found cannot be put in order.
- What forced IID costs:
  - Holding out one month class gives RMSE 750.1 against 748.8 under random folds of the same size.
  - Holding out calendar days gives 755.1 against 752.5.
  - So same-period orders on both sides of the split do not inflate the score.
- Riders and customers recur because dispatch knows them at pickup. 99.2-99.4% of test orders have a rider seen in training, which matches the 99.4% claimed for Zindi's own test file. The rider-group gap (791.0) measures a cold start, which is not this use case, and SPLIT-4 says gap size never decides.
- Mildest remedy: add one sentence to `splits_comment` with the 750.1/748.8 numbers (fix 2). No re-split.

**4. The task is worth benchmarking, with the source's metric, and every fold can be scored (P6; MET-1 to MET-4, TP).**
- The page says "The error metric for this competition is the Root Mean Squared Error", in seconds, with no transform (MET-3, MET-4).
- `scorer(container)` works on all 9 folds: 7,067 test rows each, and the dummy RMSE of 964.7-1,006.0 matches a hand computation.
- There is signal without triviality: LightGBM 752-762 against a dummy of 987 (R² about 0.40). Distance alone gives R² 0.34.
- Precedent: Lusaka kept RMSE the same day "as the other RMSE-scored ETA datasets".

**5. The 547 legs of 10 s or less stay. This departs from nyc/pkdd, and a fact sets it apart (P7; CLEAN-11 Should; USE-5).** This answers the strongest objections: the blind reviewer and the task gamer want them dropped, and the precedent checker raised a consistency check.
- What the rows are:
  - Real deliveries, not non-rides: median straight line 2.64 km, and none ends within 100 m.
  - CLEAN-11 says values that are only unusual stay, and a row leaves only when it is no task row or a copy.
- What sets Sendy apart from nyc: the late mark is visible in the inputs. The pickup wait has a median of 1,505 s on these legs against 480 s on the rest. nyc's broken clocks were not visible.
- The label is correct relative to the shipped prediction point, which is the logged pickup mark. On these rows, arrival really did follow the mark within seconds.
- The practitioner points out that a USE-7 cut is not available, because it would rest on the label, not on an input.
- The weight is small: 4.6% of the squared error, and RMSE moves 761.3 to 749.3 without these rows.
- Concession: the task gamer is right that a model which ignores the artefacts scores worse (744.2 → 755.7) and that the task partly rewards spotting late marks. That is also what the competition scored, and the winners built outlier classifiers for exactly this.
- Mildest remedy: answer the consistency check with option (a), an exception to CLEAN-11 with the 2.64 km and 1,505 s facts, serving P3 (the source's own task). Add one sentence to `task_summary.predicted` saying these legs test the detection of late marks (fix 3). Dropping test rows by their label would be the stronger remedy, and nothing in a higher rank demands it.

**6. The other real problems are notes, not reasons to hold (P7, USE-7, writing).**
- **Precipitation blanks (CLEAN-10, Should).** There are 0 zeros among the 552 recorded values, so a blank most likely means no rain. Filling 0 gives RMSE 761.4 against 760.5, a fix that changes nothing measurable. Remedy: one line in the weather bullet. Filling 0 stays optional, the curator's call.
- **The two orders ending 89-90 m from pickup (USE-7, Must).** USE-7 targets rows that lack the input the prediction acts on, and these do not. The source distance (3 and 4 km) shows a real destination; only the coordinates are anonymised. This is not a breach. Remedy: option (a), one line in `curation_comments`.
- **Writing.**
  - The record's CC line says "arrival at pickup" where it should say "at destination".
  - `fit_reason` could name `Distance (KM)`. Since the kick amendment a kept leak no longer drives the fit, and point 2 makes it "tested, not a leak", so this is optional.
  - zindi.africa 301-redirects to zindi.world, so the link is cosmetic.

**7. The remaining exploit and the untested claims do not break any rule.**
- **The task gamer's "rider's next order" feature.**
  - It gains 3.4 RMSE, and only for a participant who builds features across rows; the kit has none.
  - It is a weak transductive leak. The tension row for weak transductive leaks says to keep it with a note.
  - The proposed rider-day split cannot be built cleanly, because the day key merges different months. The split auditor's calendar-day hold-out cost only 2.6 s anyway.
- **Untested claims (99.4% rider overlap, `No_Of_Orders`, Test.csv size).** These need Test.csv and Riders.csv, which are not in the warehouse. They change wording only, and the shipped folds reproduce 99.2-99.4%. Remedy: download those files and re-run the counts, or phrase the claims as "per the 2026-10-29 audit".
- **Build state.** `dataset check` reports 0 errors and 0 warnings. `build_stale` is the curator's call to rebuild.

**Judgment record**
- **Verdict:** ship after note edits.
- **Validity:** USE-1, USE-5 and USE-8 hold (fit approximate). LEAK-10 and LEAK-16 hold. LEAK-38 is replaced by a measured pass under EV-1. SPLIT-4 and SPLIT-8 hold, and SPLIT-8's cost is measured at 1.3 s. USE-7 holds once the anonymised-coordinate note is added.
- **Value:** MET-1 to MET-4 hold, and all folds can be scored.
- **Quality:** CLEAN-11 exception (fact: real deliveries with the late mark visible in the inputs). CLEAN-10 gets a note.
- **For the curator:** answer the two consistency checks with (a). Rebuilding is your call.

</details>

<details><summary>Critic</summary>

**Opposing brief: `sendy_logistics_challenge`. It should ship only after the changes below.**

I do not argue for exclusion. The task is the source's own ETA-at-pickup task, and it is real. But the definition as it stands scores a non-task skill on part of the test rows. The container that would ship is also stale. The rest are text fixes.

**1. About 3.5% of the labels are not the quantity the actor acts on. P3, USE-5 (Must); CLEAN-11 (Should); precedent.**
- **Problem.** There are 547 legs of 10 s or less, 740 of 60 s or less and 787 under 100 s. On these legs the rider marked the pickup on arrival. The source's winners page says the rider "forgot to mark that he took the order and did it just before it was delivered". When that mark is made, the customer already has the parcel, so no ETA decision rests on these rows. USE-5 says: "A label checked and found to be another quantity than the one the actor acts on still fails." These labels have been checked.
- **Effect on the task.**
  - Training only on legs of 100 s or more, which is what a deployed model would do, costs 11.5 RMSE: 744.2 rises to 755.7 (task-gamer). The test folds score against the artefacts.
  - The pickup-wait feature, which detects the mis-marks, gains 8.5 RMSE (task-gamer). Its median is 1,505 s on these legs against 480 s on the rest (column-auditor).
  - The legs of 60 s or less are 3.5% of the rows but carry 6.5% of the squared error (practitioner).
  - So the benchmark rewards the winners' "outlier classifier" designs, not travel-time skill.
- **Precedent.** nyc_taxi and pkdd_15 drop trips under 30 s and over 120 km/h; delivery_eta and cooking_time drop times under 1 min. Their labels were also the competitions' scored labels, so "the source's labels" does not set Sendy apart (precedent-checker, consistency check 1).
- **Answer to the practitioner's objection that the cut rests on the label.** CLEAN-11 itself allows it: "A row whose target the source names as not the task's quantity may leave, with the source's words." nyc's under-30 s cut also rests on the label.
- **Remedy (fix the definition).** Drop legs under 30 s and legs whose straight line runs faster than 120 km/h, as in pkdd. That is 677 and 803 rows, overlapping. Quote the winners page and write a CLEAN-11 Cases row. If the curator keeps the rows, the consistency check needs an answer with a fact that holds up under USE-5, not only "source's labels". Note that a Must has no exceptions.

**2. The build is stale, so what would ship is not this definition. P5 (faithful data); house rule.**
- **Evidence.** The README front matter has `build_stale: true` and `built_at: 2026-10-29`, from git `b58e9ac`. That is before Lennart's 2026-11-04 switch to the pickup task, the weekday typing and the end of the row filter.
- **Remedy.** Rebuild when the curator asks for it, then re-run `dataset check` and the probes on the new container. No ship before that.

**3. `Distance (KM)` is filed under the wrong rule, and the fit does not name the kept risk. P4, LEAK-38 (Should); USE-8 (Must, wording).**
- **The rule's scope.** LEAK-38 "covers only fields whose timing cannot be tested". Here the timing was tested (EV-1):
  - Within repeated routes, the change in Distance does not track the label: r = 0.013 on 2,731 rows (claim-auditor) and r = 0.015 (precedent-checker).
  - Late-marked legs carry the full route distance: median 5 km, residual −0.013 km (column-auditor).
  - So the reading "measured between the two marks" is refuted. A post-delivery GPS total is not excluded (partial r = 0.159).
- **USE-8.** The note says the leak is "kept on purpose", but `fit_reason` does not name it. The kick and homesite Cases rows ask for that.
- **Remedy (a note).** Rewrite the bullet with these measurements: "tested, the between-marks reading refuted; post-delivery total not excluded". If it stays a kept potential leak, add one clause to `fit_reason`.

**4. A participant can build a cross-row leak from the rider's later orders. P4, by analogy with LEAK-30's weak transductive leak (Should when weak).**
- **Evidence.** From the same rider's next order that day, a participant can build features (its clocks minus this pickup, and the day's order count) that a deployed model would not have. They gain 3.4 RMSE against a noise spread of ±0.3, and are positive on 8 of 9 splits (task-gamer).
- **Why no re-split.** It is weak. The rider-day key is ambiguous without a month, and holding out calendar days costs only 2.6 s (split-auditor).
- **Remedy.** A `Potential leak, kept on purpose:` note with these numbers.

**5. The split text is factually wrong about the month. P4, SPLIT-8 (Must, met; documentation).**
- **Evidence.** Placement weekday minus day of month, mod 7, gives seven month classes. They cannot be put in time order, so SPLIT-14 still cannot be met.
- **Measured cost.** Holding out one class gives RMSE 750.1 against 748.8 at random (split-auditor).
- **Remedy.** One sentence in `splits_comment` with this cost. Change "no month or year" in `task_summary.split` to "no month order or year".

**6. Two orders end within 100 m of their pickup and the definition says nothing about them. P3, USE-7 (Must); precedent.**
- **Evidence.**
  - Order_No_20080 and Order_No_7111 end 89 m and 90 m from their pickup.
  - nyc, pkdd and Lusaka (the same day) drop such rows.
  - The source distance (3 and 4 km) and the anonymised coordinates make a real breach unlikely.
- **Remedy (a note).** A `curation_comments` line under the precedent-checker's option (a). No drop.

**7. Quality and record hygiene. P7, CLEAN-10 (Should); EV; writing. Not a reason to hold the task.**
- **Precipitation.** 20,649 values are missing, and none of the 552 recorded values is 0. A blank therefore most likely means no rain. Add a note, or fill 0 where a temperature exists (that changes RMSE from 760.5 to 761.4, so nothing).
- **Unverifiable claims.** Three facts in the definition depend on files missing from the warehouse (Test.csv, Riders.csv): 99.4% of test riders seen in training, `No_Of_Orders` at least the Train+Test orders, and the 28,269-order adjacency test. Fetch the files, or phrase these as "per the 2026-10-29 audit".
- **Record.**
  - The 2026-11-04 CC line says "arrival at pickup"; it should say "at destination".
  - `claimed_by` is still Myunghwan, and his "yes, ship" refers to the superseded definition.

**Judgment record**
- **Verdict:** ship after changes.
- **Validity:**
  - USE-5 is triggered on 3.5% of the labels; fix with the pkdd cut (issue 1).
  - USE-7 holds with a note.
  - LEAK-10 holds.
  - LEAK-38 is the wrong rule for Distance; reword the note (issue 3).
  - A weak cross-row leak is kept with a note (issue 4).
  - SPLIT-8 holds; the cost goes into the text (issue 5).
  - P5: rebuild before shipping (issue 2).
- **Value:** MET-1 to MET-4 hold; skill 0.24.
- **Quality:** CLEAN-10 note.
- **For the curator:** issue 1 is the open decision: drop as nyc and pkdd do, or a stated fact that sets Sendy apart under USE-5.

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal for `sendy_logistics_challenge`**

The critic and I agree on most of this. Points 3 to 7 are notes or record edits, and on those I concede and adopt the critic's remedies. Point 2 is a real precondition, and I concede it as one. The only real dispute is point 1, the 547 short legs. There I hold that USE-5 is met, and that the critic's drop is a curator's option, not a Must.

**1. Short legs: USE-5 triggered on 3.5% of the labels. Disputed. The facts the critic cites are true.**

- **USE-5 holds.** The prediction point is the logged pickup mark. A deployed model cannot see when the parcel was physically picked up; it fires on the rider's click. On these 547 rows the click came at the destination. The true remaining time from the trigger to arrival really was seconds, and that is exactly the label. So the label is the same quantity the system acts on, measured from the same mark the model sees.
- **This is unlike the USE-5 Cases.** In corporate_credit_rating, 17% of the labels were a different rating. In xente, a 0 meant "not reviewed". The test the critic quotes ("checked and found to be another quantity") fails here: the label was checked, and it equals destination clock minus pickup clock in every row (`_clean` asserts this; the day delta is 0).
- **What the critic has found is input error, not label error.** The rider's pickup mark is late. That late mark is visible in the inputs: the median pickup wait is 1,505 s on these legs against 480 s on the rest. A visible input error is a matter of quality (P7, CLEAN-11), not validity.
- **CLEAN-11's clause is permissive and needs the source's words.** It says "may leave, with the source's words". The quote comes from the 2nd-place winner on Zindi's blog. It is not from Sendy's or Zindi's data page, which defines the target with no filter and kept these rows in Train.csv. So the clause allows a drop but does not require one, and the default of CLEAN-11 ("values that are only unusual stay") applies.
- **The precedents do not carry over.**
  - nyc's under-30 s trips were "not rides". Sendy's legs are real deliveries: median 2.64 km straight line, none within 100 m.
  - nyc's over-3 h clocks and pkdd's GPS jumps could not be seen in the inputs. Sendy's late mark can.
  - delivery_eta and cooking_time copied TabReD's own filter. Zindi applied none.
  - pkdd's 120 km/h cap rests on exact GPS. Sendy's straight lines come from anonymised coordinates, which makes a speed cap here an unreliable cut.
- **Concessions.**
  - The practitioner's objection that "the cut rests on the label" is wrong: nyc's cut did too. I withdraw it from my opening point 5.
  - The task gamer's finding stands. A model trained the way it would be deployed loses 11.5 RMSE (744.2 → 755.7), and the wait feature gains 8.5. The task partly scores the detection of mis-marks. That has to be written into `task_summary.predicted` and the notes with these numbers (fix 3), and the CLEAN-11 Cases row should cite the test.
- **Remedy.** Option (a): an exception to CLEAN-11 with the facts above, serving P3 (the source's own task, as the source scored it). The exception is to a Should, not a Must, so the critic's "a Must has no exceptions" does not apply as long as USE-5 holds. If the curator reads USE-5 the critic's way, the critic's drop is the right rung of the remedy ladder (fix the definition), not exclusion. I would not contest that call: the weight is 4.6% of the squared error, and RMSE moves 761.3 → 749.3.

**2. Stale build (P5). Conceded.**
- What is stale is the container, not the definition. README: `built_at` 2026-10-29, `git_sha` b58e9ac, `build_stale: true`. Every agent measured the frame from the definition itself (`dataset_io.from_definition`), so the panel's numbers describe what will ship.
- `rebuild.md` puts the build on the curator's ask or before the collection is released. So the verdict becomes "ship after the release rebuild". Rows and splits changed (21,199 → 21,201), so the step-6 probe sweep and `dataset check` have to run on the new container. This is a precondition, not a defect.

**3. `Distance (KM)`: wrong rule, and `fit_reason` does not name the kept risk. Conceded, and it matches my fix 1.**
- The note should report the tests: r = 0.013 (n = 2,731) and r = 0.015 (n = 2,601) within repeated routes, and the full route distance on late-marked legs (residual −0.013 km).
- A post-delivery GPS total is still not excluded (partial r = 0.159). So a residual risk remains, and USE-8 (Must, on wording) asks for one clause in `fit_reason` naming it as kept. I drop "optional" from my opening point 6. This is a text fix with no change to the data.

**4. Rider's-next-order cross-row leak. Conceded. Same remedy as my opening point 7.**
- Add a `Potential leak, kept on purpose:` note: +3.4 RMSE against ±0.3 noise, positive on 8 of 9 splits, available only to a participant who builds cross-row features.
- Under USE-8, `fit_reason` names it too, in the same clause as Distance. No re-split: the rider-day key merges months, and holding out calendar days costs 2.6 s.

**5. Split text about the month. Conceded. Same as my fix 2.**
- One sentence in `splits_comment`: 7 month classes that cannot be ordered; holding one out gives 750.1 against 748.8 at random.
- In `task_summary.split`, change "no month or year" to "no month order or year".

**6. The two orders ending 89-90 m from pickup. Agreed. Option (a), one line in `curation_comments`.**
- USE-7 holds: the source distance (3 and 4 km) shows a real destination.
- Lusaka dropped such trips the same day, so the line should say the difference: Sendy's coordinates are anonymised.

**7. Quality and record. Conceded.**
- Precipitation: a note that a blank with a temperature most likely means no rain (none of the 552 recorded values is 0). Filling 0 stays optional (761.4 against 760.5).
- Unverifiable claims: phrase them as "per the 2026-10-29 audit", or fetch Test.csv and Riders.csv and re-run the counts.
- Record:
  - Line 62 says "arrival at pickup"; it should say "at destination".
  - `claimed_by` still names Myunghwan. His "yes, ship" is superseded by the 2026-11-04 CC lines (the newer decision wins), but the record should say so.
- One new fact from the record: line 70 says "review panel (none): no panel ran". That becomes false once this panel is recorded, and needs updating.

**Updated judgment record**
- **Verdict:** ship after the note edits and the release rebuild (with `dataset check` and the probes re-run on the new container).
- **Validity:**
  - USE-1, USE-5 and USE-8 hold (fit approximate). `fit_reason` gets one clause naming the kept risks: Distance's post-delivery reading and the weak cross-row leak.
  - LEAK-10 and LEAK-16 hold. Distance is tested under EV-1, with the residual risk named.
  - SPLIT-4 and SPLIT-8 hold; SPLIT-8's cost of 1.3 s goes into the text.
  - USE-7 holds, with the anonymised-coordinate note.
  - P5: rebuild before release.
- **Value:** MET-1 to MET-4 hold; all 9 folds can be scored; skill 0.24.
- **Quality:**
  - CLEAN-11 exception for the short legs (real deliveries, late mark visible in the inputs, label exact from the logged mark), plus the 11.5 RMSE cost to a deployed-style model stated in `task_summary`.
  - CLEAN-10 note on precipitation blanks.
- **For the curator:** consistency check 1 is the one open call. I recommend (a), and (b) is acceptable. Check 2: (a).

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal (critic): `sendy_logistics_challenge`**

I accept most of the advocate's points: 2 (with one correction), 3, 4, 6 and the leak and untested-claims parts of 7. I dispute two things. Point 5, together with the USE-5 part of point 1, is where we disagree on substance. The build state in point 7 is the other.

**Advocate 1 (real task; USE-1, USE-5 and USE-8 met).** Partly conceded, partly disputed.
- **Conceded.** USE-1 holds. The task is the source's ETA at pickup, and `fit="approximate"` is right for the riders' marks and forced IID, as in the 20 `ForcedIIDFromTemporal` definitions.
- **Disputed: "every agent agrees P3 holds".** Three agents flag the short legs:
  - The blind reviewer leans to removing them.
  - The task-gamer asks to drop or flag them in both train and test.
  - The practitioner says that on these rows "no ETA decision depends on them".
- **Disputed: USE-5 holds on every row.** USE-5 (Must) ends: "A label checked and found to be another quantity than the one the actor acts on still fails." Here the check has been done. The source's own winners page says the rider "forgot to mark that he took the order and did it just before it was delivered". The record itself says riders "mark the pickup late, when they arrive" (dataset.py, line 85-86). On these rows the label is the gap between two taps at the destination, not the pickup-to-arrival time the dispatcher acts on.

**Advocate 5 (keep the 547 legs; CLEAN-11 exception).** Disputed. This is the open decision.
- **Wrong rule.** The advocate answers with an exception to CLEAN-11, which is a Should. The failure is under USE-5, a Must. principles.md, line 130: "A Must has no exceptions: only a higher-ranked Must overrides it." P3 does not override USE-5, because USE-5 is how P3 is applied. MET-4 (the source's metric) is a lower-ranked value rule and does not override it either.
- **The facts point the other way.**
  - "Real deliveries, median 2.64 km straight line": a 2.64 km bike trip cannot take 10 s or less. This fact shows the label is wrong, not that it is valid.
  - "The late mark is visible in the inputs": that makes the error learnable, not right. The task-gamer measured it. The wait feature gains 8.5 RMSE (4.8-12.1 per split), almost all of it on these rows (1,037 → 913, against 750 → 747 on the rest). The benchmark scores the detection of recording errors.
  - "The label is correct relative to the logged pickup mark": the actor's prediction point is the real pickup, not the late tap. On these rows the parcel has already arrived when the tap happens.
- **The weight is not small next to what we already document.**
  - Dropping the rows moves RMSE from 761.3 to 749.3: 12 s.
  - A deployed-style model trained on legs of 100 s or more loses 11.5 RMSE (744.2 → 755.7).
  - The advocate wants SPLIT-8's 1.3 s and the cross-row leak's 3.4 s written down. This effect is 4-9 times larger and is the largest validity effect any agent measured.
- **"Dropping test rows by their label."** nyc and pkdd do exactly that (under 30 s), and CLEAN-11 allows it: "A row whose target the source names as not the task's quantity may leave, with the source's words." The source's words exist: the host's own winners page. I accept the practitioner's point that USE-7 is not the path. The cut rests on USE-5 and CLEAN-11's source-words clause, not on USE-7.
- **Remedy (unchanged, fix the definition).** Drop legs under 30 s (677 rows) and legs whose straight line runs faster than 120 km/h (803 rows, overlapping), as pkdd does. Quote the winners page and add a CLEAN-11 Cases row.
  - If the curator keeps the rows, the record needs a fact that shows these labels are the actor's quantity (USE-5). The fact the advocate offers is a CLEAN-11 exception and does not answer USE-5.
  - Lennart's 2026-11-04 line keeps the legs "as the source's labels (CLEAN-11)". It cites only the Should and does not address USE-5.

**Advocate 2 (`Distance (KM)`).** Mostly conceded, with one correction.
- **Conceded.** EV-1 tested the timing: r = 0.013 (n = 2,731) and r = 0.015 (n = 2,601), and the late-marked legs carry the full route distance (residual −0.013 km). LEAK-38 "covers only fields whose timing cannot be tested", so a reworded note is the remedy.
- **Correction.** "Measured as not a leak" overstates the evidence. The column-auditor found that a GPS total recorded after delivery is not excluded (partial r = 0.159).
- **Remedy.**
  - If the note ends as "tested, between-marks reading refuted", no `fit_reason` clause is needed.
  - If it stays `Potential leak, kept on purpose:` (Lennart's 2026-11-04 line 60), `fit_reason` must name it, per the kick and homesite rows of USE-8.

**Advocate 3 (split).** Conceded. The remedy is the same as my point 5: one sentence in `splits_comment` (750.1 vs 748.8), and "no month order or year" in `task_summary.split`.

**Advocate 4 (metric, MET-1 to MET-4).** Conceded.

**Advocate 6 (precipitation, the 89-90 m orders, writing).** Conceded.
- Precipitation gets a CLEAN-10 note; the fill is optional (760.5 vs 761.4).
- The two orders get option (a), one `curation_comments` line.
- Writing: the record's line 62 says "arrival at pickup" and should say "at destination".
- One addition: `claimed_by` and Myunghwan's "yes, ship" refer to the superseded definition. Record line 70 also says "no panel ran ... all settled", which this pass now overtakes.

**Advocate 7 (cross-row leak, untested claims, build).** The first two are conceded; the build state is disputed.
- **Conceded.**
  - The rider's-next-order leak gets a `Potential leak, kept on purpose:` note with 3.4 RMSE (±0.3, 8 of 9 splits). We agree on the remedy.
  - The untested claims are phrased "per the 2026-10-29 audit", or the files are fetched.
- **Disputed: build state.** "`dataset check` 0 errors" does not make the container shippable.
  - The README shows `build_stale: true`, `built_at: 2026-10-29` and `git_sha: b58e9ac`.
  - That build predates every 2026-11-04 decision: the pickup task, 21,201 rows instead of 21,199, the weekday typing and the end of the filter.
  - What would ship today is the superseded placement task. That fails P5 (faithful data), so this is a precondition for shipping, not optional.
  - Remedy: rebuild when the curator asks, then re-run `dataset check` and the probes. "Ship after note edits" is therefore not reachable as written.

**Where we stand**
- **Agreed:** no exclusion, and the note edits (Distance, split cost, precipitation, the 89-90 m orders, the cross-row leak, record wording).
- **Open for the curator, ranked:**
  1. USE-5 (Must) on the 677 to 803 artefact legs. Drop them as nyc and pkdd do, or record a fact that they are the actor's quantity. A CLEAN-11 exception does not answer a Must.
  2. P5: rebuild before shipping.
- **Verdict:** ship after changes, not after notes only.

</details>
