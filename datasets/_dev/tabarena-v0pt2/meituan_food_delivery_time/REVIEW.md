# meituan_food_delivery_time

**Outcome:** added. The focused panel recommends inclusion of the forecast-free acceptance-time ETA task: valid inputs and temporal boundaries, useful remaining-time prediction, and no required definition correction. First-party operational provenance and substantial samples favor inclusion; eight days in one city limit generalization. Myunghwan approved inclusion, fallback RMSE in minutes and retaining the 62 unused tail rows on November 9, 2026. Scientific review is complete; a build has not been requested.

**Main points:** All scientific decisions are approved: the forecast-free 15-feature task, root mean squared error in minutes and the explained warning for 62 retained but unused October 25 rows. No further curator decision remains for this review.

**Record judgment:** Each row is an accepted order; predict total placement-to-delivery minutes immediately after acceptance. Known elapsed time, courier/merchant/district, shifted coordinates, prebook flag, acceptance time and dispatch/push delays are inputs. Both platform forecasts are excluded. Three future-day windows retain the same source cohorts, with every actual training event before midnight and earliest test acceptance; 370/407/423 unfinished training orders are excluded. Removing features changes tie ordering, so old predictions cannot be reused by position. Fresh qualification uses the revised frame. Recorded-promise timing and live evaluator isolation from future query rows remain unverified; neither is certified by these data checks.

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

**Review panel:** ship (focused mediator); Myunghwan approved final inclusion, the declared metric and the explained unused-tail warning on November 9, 2026. Routine reconciliation is complete. Independent claim, column, split, precedent and isolated participant reviews find no required definition correction or demonstrated exploit. Issue 1 and the final approvals are resolved; earlier pending statements in the reports below record their historical review state. The original full panel and boundary reports below are historical: their 17-feature counts, forecast-retention question and positional evidence reuse do not describe the revised primary.

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
- E: independently computed `panel/claims-evidence.json` and reproducible `panel/claims_audit.py`.
- B/S/P: cached primary-source text in warehouse `_runs/20261107_meituan_screen_review/{background,supplement,paper}.txt`. These are source statements, not our measurements. B: March 2024 background Sample Question 4 and Tables 1-2. S: October 2024 supplement sections 2.2-2.5. P: Wang et al. 2025 section 3.1, appendices A.1-A.2 and introduction.

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

Probe output: `panel/dtypes/meituan_food_delivery_time.json` and `panel/dtypes/flagged.csv`. All Python processes used the supplied interpreter, warehouse and OMP/MKL/OPENBLAS/POLARS thread caps of 2.


</details>

<details><summary>Split audit</summary>

**Independent split auditor**

Verdict: right with notes; no actionable split findings. Audited definition SHA 256 2367a2d99a669858125f4008c5220ca24da4340485cc3a925aec273909258f60. Actual definition loaded independently with dataset_io; thread caps 2. No scientific files edited.

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

RMSE minutes is an acceptable explicit fallback (MET-1,3,5,8): background Sample Question 4 and the supplement/data paper name timing prediction without one predictive scoring metric. MAE/calibration are useful diagnostics, not a reason to invent asymmetric source costs. Sources read: original background Sample Question 4; supplement sections 2.4-2.5; 2025 paper section 3.1; independent raw CSV checks with supplied interpreter and thread caps 2. No science files edited. True human choice: accept the documented forecast-snapshot uncertainty or request an alternative qualification.


</details>

<details><summary>Blind reviewer</summary>

**Independent blind reviewer**

Verdict: include with changes. The data supports a useful acceptance-time delivery prediction task, but the supplied target appears to include time already elapsed before prediction. That makes variance and ordinary R2 largely explainable by a known quantity. Define the target precisely, preferably evaluate remaining delivery time, and publish label-availability-aware temporal splits before inclusion.

Scope: read only task.md/data.parquet in the clean room plus the named public GitHub repository/background PDF. No surrounding project files, curation reports, skills or agent files opened. Generic workspace instructions were in inherited context, supplied no dataset evidence and were not used. DOI inaccessible. Read-only inspection; numerical libraries made temporary caches. No packages installed, agents spawned or dataset changes.

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

Limits: bounded tree models and cheap probes only; no exhaustive feature reverse engineering, semantic source verification, or public row lookup. Strong known inputs were treated as legitimate. No surrounding project files, other kits, curation notes, or external reports were opened. A process diagnostic printed only this task's shell/sandbox process text; none was used as benchmark evidence. No public web was needed. Shipped files were not edited.

Artifacts: `work/probe.py`, `work/results.json`, per-split residual prediction arrays, `work/maturity.py`, and `work/maturity_results.json` (conservative timing sensitivity).

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

Generated `panel/register.json` with the supplied interpreter using
`decision_register.py --json PATH` and OMP/MKL/OPENBLAS/POLARS thread caps of 2.
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
a new target or final shipping. No scientific files, claims, controller or context
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



Loaded the actual definition through `dataset_io.from_definition`, using the project Python and warehouse, with all numerical thread caps 2. The final frame has **568,545 rows, 15 predictors and one target**. The dtype probe counts 14 because its table omits datetime columns. Its three count_like flags are courier_id, poi_id and da_id: these are nominal identifiers, so categorical is correct under CLEAN-12/14. No ordinal scale needs decoding.

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

Bridge startup inspection: latest recorded selected sync captured 2026-11-06 04:50:46Z, installed 04:51:27Z, over 3 days old; selected receipt files intact. Current peer changes remain unknown; no remote freshness or transfer is claimed. Findings here come from current local files and raw data.

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
