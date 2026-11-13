---
unique_name: online_shoppers_purchasing_intention_dataset
name: Online Shoppers Purchasing Intention Dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
tags:
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
original_source: UCI
year: '2018'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5F88Q
notebook_path: datasets/beyond_iid/old_iid/online_shoppers_purchasing_intention_dataset/online_shoppers_purchasing_intention_dataset.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/online_shoppers_purchasing_intention_dataset/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Shopping prediction (also like a recommender system task); special preprocessing to avoid impact of time; sloved with an LSTM; 

available on OpenML

Click stream data. Study title is Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM - so original data was time-series or at least temporal. dataset consists of feature vectors belonging to 12,330 sessions. 

The dataset was formed so that each session would belong to a different user in a 1-year period to avoid any tendency to a specific campaign, special day, user profile, or period. Although there is a temporal component, the task is conceptualized s.t. the samples are iid. However, I am unsure whether the task is conceptualized correctly regarding the delayed target prediction. The features and the target should have a delay - otherwise it is meaningless to predict a purchase after it already happened

Potential issue: Temporal Task?

Lennart: very likely a temporal task and maybe even grouped

Andrej: temporal task, but the features used for the tabular task are time-invariant. If the task was conceptualized correctly, a temporal split is not needed

CC (2026-10-01, Lennart): Leak audit: kept `PageValues`, dropped the February-May sessions instead (12,330 -> 6,875 rows).
- `PageValues` is meant as a historical Google Analytics page metric, "stored in the application database ... and updated automatically at regular intervals", averaged over the pages a session visits (Sakar et al. 2019, Sec. 2.1 and Sec. 3). Used that way it is a valid real-time feature.
- But the data has two regimes. February-May (5,455 rows): all 560 buyers have PageValues > 0, PageValues alone gives AUC 0.974 (LightGBM 0.981, 0.823 without it). June-December (6,875 rows): 370 of 1,348 buyers (27%) have PageValues = 0, PageValues alone gives AUC 0.814 (LightGBM 0.875, 0.739 without it). Most likely the page-value table was computed over the early period, so the early buyers' own purchases credited their pages; the later values behave like the intended historical metric. A change in site tracking could leave a similar pattern, so this is not proven.
- `SpecialDay` is non-zero only in February and May and is dropped as constant.
- Split: IID (required_split set to Random (IID)): each session belongs to a different user sampled over one year (Sec. 2.1) and only the month is known, so a temporal split would mainly test extrapolation to unseen months.

**Assessment (AI, 2026-10-19):** open since the leak audit of 2026-10-01: 40 exact duplicate rows remain after the February-May sessions were dropped. To decide in the next pass: drop them as collection copies (with the share in the notes) or keep them as natural repeats.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Sakar et al. 2019 report accuracy, TPR, TNR and F1 (F1 stressed over accuracy, full text paywalled); no fixed threshold or costs. Original rejected: F1. roc_auc is the binary fallback.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `Month` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `ga_merchandise_store_sessions` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (True means revenue).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship: the page-value leak is handled by keeping June-December, methods separate on the source task, and the 40 repeated rows are natural one-page bounces of different users (keep). Priority 2: gap 0, use case 0, source 1, shape 1, risk -1.

CC (2026-11-11, Andrej): the 40 repeated one-page visits stay as natural repeats of different users (review page, issue 1 A, agreeing with the answer of 2026-11-06), with a note; this closes the Assessment of 2026-10-19. Random split kept as forced from temporal (issue 2 A): `ForcedIIDFromTemporal` and a `Time basis:` line (only December can train on half; testing December costs 0.009 ROC AUC for LightGBM). Issue 3 (finished-visit rows as a stand-in for the in-visit decision) parked.

CC (2026-11-13, Andrej): collection fact `Target: Later` (Review issue 4, B): whether the visit ends in a purchase, which closes the session the features describe, so it arrives after the features; the forced tag and the split stay.

## Review

**Outcome:** added. The AI recommends shipping it as defined; one small point is open (issue 1, the 40 repeated
visits, recommended kept). Reviewed on 2026-11-04 without a panel, from the evidence already gathered (the record, the
leak audit of 2026-10-01, model runs on the TabArena v0.1 task of the same source, which hold all 12,330
visits) and one check on the v0.2 rows. The data are Sakar et al.'s (2019) Google Analytics visits to one online shop
(UCI 468): one row per visit, each by a different user over one year, with page counts and times, the pages' bounce,
exit and value figures from the shop's analytics, month, visitor type and technical codes; the target is whether the
visit ended in a purchase. v0.2 keeps June to December (6,875 visits, 20% buy). Validity: a real use case (the shop
decides during a visit whether to show an offer), with an approximate fit, since each row summarises the finished
visit; the page-value leak is handled by the cut: in February, March and May every buyer has `PageValues` above zero
and that column alone gives ROC AUC 0.974, while on the kept months 27% of buyers have 0 and it gives 0.814, as a
historical page metric would (not provable from the data). Value: on the v0.1 task the benchmark methods spread (1-AUC
0.060 for the best foundation models, 0.065 for tuned gradient boosting, 0.082 to 0.087 for logistic regression);
not measured on the v0.2 rows. Quality: 40 repeated rows (issue 1); our experiments found that the page times mix
whole seconds with exact fractions, a detail of how the analytics summed them that is worth about 0.3% of the best
model's error, no action. Weighed: a documented source and a real decision +, methods separate +, the page-value fix
rests on a cut that cannot be proven -, a summary of the finished visit -, better data found
(`ga_merchandise_store_sessions`, not screened yet) -.

**Main points:** issues 1 and 2 settled on 2026-11-11 (repeats kept with a note; random split forced from temporal
with its `Time basis:` line). Parked: the finished-visit rows as a stand-in for the in-visit decision (3).

**Record judgment:** valid, ship. The cut of February to May, the IID split and the dropped `SpecialDay` are
Lennart's decisions of 2026-10-01; the open point the Assessment of 2026-10-19 left for "the next pass" is issue 1.
The data-scouting run of 2026-10-30/31 found `ga_merchandise_store_sessions` (Google's GA360 export, about 70 times the
sessions, with hit-level timing that would allow a prediction point inside the visit) as better data for the same
task; it is screened in its own record and does not change this verdict. The record has no `domain` or
`problem_type` field; the definition's values (business & marketing, binary classification) can be filled in without
a mark.

**Issues for Andrej:**

1. **Keep the 40 repeated visits?**

   * **Problem:**
     - 40 of the 6,875 rows (0.6%) repeat another row in every column; with the rows they repeat, 69 rows are involved.
     - All 69 are visits that opened one product page (two pages in 2 rows), spent no recorded time, bounced, had no page value and did not buy.
     - Drop the repeats as copies, or keep them as different users who did the same short visit?
   * **Background:** the source built the data so that "each session would belong to a different user in a 1-year
     period" (Sakar et al. 2019, as quoted in the record). With 16 columns, of which the visit-level ones are all
     zero or fixed for a one-page bounce, different users with the same month, browser, region, traffic source and
     visitor type give identical rows. Duplicates need a decision each time[^1a]; few features and plausible repeats
     are natural and stay[^1b].
   * **Experiments:** the v0.2 rows rebuilt from the shipped container (June to December, `SpecialDay` dropped; Slurm
     job 1344881): 40 repeats, 69 rows in repeat groups, all labelled No, all with 0 administrative and informational
     pages, 1 product page (67 rows) or 2 (2 rows), 0 seconds, bounce and exit rate 0.2, page value 0.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 6,875 rows; a note names the repeats | the shop does meet many identical one-page bounces | an identical row can sit in train and test |
     | B | Drop the repeats | 6,835 rows | no identical row across the split | removes real visitors the shop meets |

   * **Recommendation:** A: the repeats are the commonest visit a shop sees, by different users, and all carry the
     same label, so they inflate nothing a real deployment would not meet. **Decision:** keep (A) or drop (B)?

   **Notes for the AI:** on A, add a curation note ("40 rows repeat another: one-page product visits with no time, a
   bounce and no page value, all without purchase; different users per Sakar et al. 2019, kept as natural
   repeats") and a `CC (2026-11-04, Andrej):` line closing the Assessment of 2026-10-19; on B, `df.drop_duplicates()`
   after dropping `SpecialDay`, re-run `dataset check`.

   [^1a]: **LEAK-16** (Must): duplicate rows need a decision every time.
   [^1b]: **LEAK-18** (Should): many degrees of freedom and an exact match is a collection artefact, dropped; few
     features and plausible repeats are natural, kept with a note.

   **Answer (AI, 2026-11-06):**

   * **Verdict:** natural, coarse rows: the repeats are different users whose short visits look the same, so they
     stay with the random split (A), and the note gives the overlap (0.7% to 0.9% of test rows have an identical row
     in training)[^1e1].
     - Link at chance: 239 of the 6,875 visits are the same one-page product bounce, and 39 of the 40 repeats are
       among them. Giving each visit the visitor details (month, operating system, browser, region, traffic source,
       visitor type, weekend) of a random other visit yields 37 repeats (28 to 45 in 200 shuffles; 43 within the
       month) against 40 observed; with every column independent, 21.
     - The label goes with the visit, not the link: all 69 rows are no purchase, as are 238 of the 239 bounces.
     - No order: no user id, each visit a different user per the source, and the month the only time.
   * **Recommendation:** unchanged, A.

   [^1e1]: **LEAK-41** (Must; draft PR #62): repeats of a unit the data does not record get one verdict; natural when
     the look-alikes are distinct units (a coarse profile): the random split stays and the notes give the share of
     test rows with a look-alike in training. **LEAK-42** (Should; draft PR #62): three tests set the verdict: a link
     above a chance rate that keeps the data's structure, a label that travels with the link beyond what the shared
     features predict, and an order.

   **Resolved (2026-11-11, Andrej):** A (ok, on the answer of 2026-11-06): the 40 repeats stay; a curation note
   names them as natural repeats of different users, with the chance link (37 expected against 40) and the share of
   test rows with an identical row in training (0.7% to 0.9%); a `CC` line closes the Assessment of 2026-10-19. Text
   only, no `dataset check`.

2. **Split by time, or keep the random split as forced by too few months?**

   * **Problem:**
     - The month of every visit is in the data (June to December of one year) and the shop scores later visits, but
       only December can be a test window that trains on at least half of the visits (June to November, 75%), while
       November would train on 31%, so the three windows the rules ask for do not exist.
     - The rules allow no temporal split with fewer than three windows, so the random split stays as forced from
       temporal, the tag for too few periods, with its cost measured on the one valid window[^2a].
     - Keep the random split as forced, or test on December alone?
   * **Background:** the purchase share rises from 10.1% in June to 25.4% in November and falls to 12.5% in December;
     visits per month run from 288 (June) to 2,998 (November). Inside a month the file order is not the order of days:
     weekend and weekday visits alternate as often as in a shuffled file (November 1,143 runs against 1,165 expected,
     December 612 against 578), so no finer window can be built. Every visit is a different user, so no entity can be
     held out across the months either.
   * **Experiments:** the 6,875 shipped visits and 16 features, untuned LightGBM and logistic regression (one-hot
     categories), ROC AUC (Slurm job 1365898):
     - Shipped random split (3 x 3): LightGBM 0.868 (0.863 to 0.873), logistic regression 0.839.
     - December trained on June to November: LightGBM 0.890, logistic regression 0.881.
     - Same December visits and same training size (December in 3 folds, 3 seeds; June to November only against visits
       drawn from all months, other December visits included): LightGBM 0.889 against 0.898 (-0.009, lower on 8 of 9
       folds), logistic regression 0.880 against 0.878 (+0.002, higher on 4 of 9). November, below the floor, loses
       0.034 and 0.030.
   * **Effect on the task:** the random split lets a model learn a month's purchase level from other visits of the same
     month; on December that is worth about 0.01 ROC AUC to LightGBM and nothing to logistic regression.
   * **Consistency:** follows distribution_transformers_at_cauca_department, whose two label years give one window: it
     ships IID with the cost measured on that window (0.648 trained on 2019 against 0.639 on random folds)[^2b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, forced from temporal (implemented) | 3 x 3 random folds; the definition gets the tag `ForcedIIDFromTemporal` and a `Time basis:` line: the month is in the data, only December can train on half, and testing December costs 0.009 ROC AUC (LightGBM) at equal training size | the rules' answer when three windows do not exist; 9 folds over all months | the folds mix months whose purchase share runs from 10% to 25% |
     | B | December as the one test window | train on June to November (5,148 visits), test on December (1,727) | tests later visits, as the shop meets them | one window where the rules ask for three; a single holiday month decides the score |

   * **Recommendation:** A: the release cannot give three windows, the rules do not allow fewer, and on the one valid
     window the random split gains little (0.009 for LightGBM, nothing for logistic regression). **Decision:** A or B?

   **Notes for the AI:** on A, `data_tags = ("ForcedIIDFromTemporal",)`; the curation bullet "We keep the IID split:
   each session belongs to a different user ..." becomes `- Time basis: ForcedIIDFromTemporal: the visit month
   (June to December of one year) is in the data and the shop scores later visits; not split by month, because only
   December can train on half of the visits (June to November, 75%; November would train on 31%) and the file order
   within a month is not the order of days, so three windows do not exist; testing December on June to November costs
   0.009 ROC AUC at equal training size (untuned LightGBM 0.889 against 0.898; logistic regression +0.002).` The frame
   has no date column, so no warning to accept. On B, a month index (June 1 to December 7, the year is not in the data)
   as the time column, `Temporal(on="month_index", splits=TemporalSplits(window=1, unit="unique", n_windows=1),
   horizon=1, horizon_unit="months")`, `accepted_check_warnings` for `splits_too_few` with the reason, `split` and
   `splits_comment` rewritten, record `required_split` Temporal. Under either option the record gets the tags
   `Samples: Over Time` and `Time: Dated`. Results: Slurm job 1365898.

   [^2a]: **SPLIT-14** (Must): a temporal task has at least 3 windows, none training on less than half of the data; a
     task that cannot meet it ships in the closest regime, tagged as forced from temporal (SPLIT-8; IID:
     `ForcedIIDFromTemporal`). **SPLIT-32** (Should): how the data was collected is information for the split; the
     record's collection facts and, where one fits, the definition's use-case prototype with its `Time basis:` line.
   [^2b]: SPLIT-8 case: distribution_transformers_at_cauca_department, two label years, one year IID, ROC AUC 0.648
     trained on 2019 and tested on 2020 against 0.639 on the random folds (2026-10-21, Lennart).

   **Resolved (2026-11-11, Andrej):** A (ok): `data_tags = ("ForcedIIDFromTemporal",)`; the bullet "We keep the IID
   split: ..." became the drafted `- Time basis: ForcedIIDFromTemporal: ...` line (ending with what the split cannot
   test: later months and the shift in purchase share between months). The record already had `Samples: Over Time` and
   `Time: Dated`. Splits unchanged, so no `dataset check`.

3. **Each row summarises the finished visit, purchase included: keep it as an approximate stand-in for the in-visit decision?**

   * **Problem:**
     - The shop decides during a visit whether to show an offer, but every page count, duration and page figure in a row covers the whole visit, the pages after that moment and the purchase itself included, so part of each row arrives after the prediction point[^3a].
     - On the kept months nothing in the summary spells out the purchase: no page type marks the buyers (ROC AUC 0.55 to 0.68 for each count, duration, bounce and exit rate alone; `PageValues` 0.81, kept by Lennart), and buyers range from one-page visits (17 viewed two pages or fewer) to long ones.
     - Keep the finished-visit rows with the gap the fit names, or retire them for data that allows a prediction point inside the visit?
   * **Background:**
     - The purchase share rises with the visit's length: 2.9% of one-page visits bought, 7.1% of three-page visits, 14.3% of six to ten pages and 24.9% of more than twenty, so the late part of a row is mostly the visit's length, which a shop sees growing during the visit.
     - The record's first triage note asked the same ("it is meaningless to predict a purchase after it already happened"); Lennart's leak audit of 2026-10-01 settled the page values by the cut of February to May, not the summary.
     - The data scouting found `ga_merchandise_store_sessions` (Google's GA360 export, hit-level timing), screened in its own record, which could cut each visit at a prediction point inside it.
   * **Effect on the task:** models score sessions whose counts are final, while a deployed model sees them part-way; the ranking a model learns from final lengths would be applied to shorter, unfinished ones, so the score overstates the in-visit task by an amount no field of this release can measure.
   * **Consistency:** the rule retires a task whose features summarise a window that ends at the outcome when no common prediction point can be rebuilt, as for iranian_churn, whose usage window ends at churn and gives ROC AUC 0.986[^3a]; the fact that sets this one apart is that its summary does not mark the outcome: without `PageValues` LightGBM reaches 0.739 on these months (Lennart's audit of 2026-10-01), and no field alone passes 0.68.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, approximate fit (implemented) | the rows as they are; `fit_reason` names the finished visit | the source's own task and features; no field spells out the purchase | part of each row comes after the decision; the size of that gap cannot be measured here |
     | B | Retire for in-visit data | `No (Retired)` once `ga_merchandise_store_sessions` ships with a prediction point inside the visit | the use case's own timing | depends on another dataset not yet added; loses a documented source the benchmark has run since v0.1 |

   * **Recommendation:** A: the summary carries the visit's length, not a mark of the purchase, and the fit already names the gap; revisit when the hit-level data ships[^3b]. **Decision:** keep (A) or retire for in-visit data (B)?

   **Notes for the AI:** on A, close with a `CC` line in the record that answers the first note (the counts and durations do not mark the buyers; the gap is named in `fit_reason`); no definition change. On B, record `No (Retired)` with the reason, the folder removed once the GA360 dataset ships, a CHANGELOG entry.

   [^3a]: **USE-3** (Must): name the prediction point; a value that did not exist then is a leak, including a feature computed over a window that ends at the outcome. **LEAK-10** (Must): a feature holds only what existed at the prediction point; when the features summarise a window that ends at the outcome and no common prediction point can be rebuilt, retire.
   [^3b]: **USE-8** (Must): an approximate fit is a stand-in with a known gap, named as such in `fit_reason`. **LEAK-11** (Should): a value measured after the outcome that weakens the signal stays, with a note.

   **Deferred (2026-11-11):** parked on Andrej's mark ("We will get back to that.").

4. **Record `Target: Later`?**

   * **Problem:**
     - The record names no `Target:` fact, which reads as a target measured with the features.
     - The label is whether the visit ends in a purchase, which closes the session the features describe: it arrives after the features, and the forced tag already treats the use case as forward.
   * **Background:** asked on 2026-11-13 together with `CrossSectional`, which was dropped the same day; the fact stays useful, since the `Target:` facts decide between `DelayedTarget` and a forced tag and start the leak checks.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave as is (implemented) | no `Target:` fact | no change | the record contradicts the label's timing |
     | B | Record `Target: Later` | the record gains the fact; tag and split stay | the record says when the label arrives; the facts guard can check it | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, add `Target: Later` to the record with a CC line; the definition does not change.

   **Andrej (2026-11-13, change):** Option B: Record Target: Later.

   **Resolved (2026-11-13, Andrej):** B. The record has `Target: Later`; the forced tag and the split stay.

## Reference

Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM recurrent neural networks
By C. O. Sakar, S. Polat, Mete Katircioglu, Yomi Kastro. 2019

Published in Neural computing & applications (Print)
