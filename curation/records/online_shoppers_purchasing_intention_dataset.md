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
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Fixed Delay'
- Dated Event Log
original_source: UCI
year: '2018'
collection_period: Unknown
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
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

**Assessment (AI, 2026-11-04):** reviewed for BeyondArena v0.2, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship: the page-value leak is handled by keeping June-December, methods separate on the source task, and the 40 repeated rows are natural one-page bounces of different users (keep). Priority 2: gap 0, use case 0, source 1, shape 1, risk -1.

CC (2026-11-11, Andrej): the 40 repeated one-page visits stay as natural repeats of different users (Review issue 1, A, agreeing with the answer of 2026-11-06), with a note; this closes the Assessment of 2026-10-19. Random split kept as forced from temporal (issue 2 A): `ForcedIIDFromTemporal` and a `Time basis:` line (only December can train on half; testing December costs 0.009 ROC AUC for LightGBM). Issue 3 (finished-visit rows as a stand-in for the in-visit decision) parked.

CC (2026-11-13, Andrej): collection fact `Target: Later` (Review issue 4, B): whether the visit ends in a purchase, which closes the session the features describe, so it arrives after the features; the forced tag and the split stay.

CC (2026-11-19, Andrej): leave one month out, `ForcedGroupedFromTemporal` (Review issue 6, C): the relation is measured not flat (November), so whole months are held out, each once; `Month` is the group, no input.

CC (2026-11-20, Andrej): the finished-visit rows stay as an approximate stand-in for the in-visit decision (Review issue 3, A). This answers the first triage note ("it is meaningless to predict a purchase after it already happened"): on the kept months no count, duration, bounce or exit rate marks the buyers (ROC AUC 0.55 to 0.68 each; LightGBM 0.739 without `PageValues`), and `fit_reason` names the gap: each row summarises the finished visit, while the shop acts during it.

**Assessment (AI, 2026-11-23):** does leave one month out flatter the score by training on later months? No. For each
test month from August to December, two training sides of equal size (90% of the visits before the test month) score
all of that month's visits: one drawn from the earlier months only, as a forward deployment has, and one drawn from all
other months, earlier and later, as the shipped folds have. 10 draws each; ROC AUC, gap = all other months − earlier
months only, ± SE:

| Test month | Train size | LightGBM | Random forest | Logistic regression | TabPFN |
|---|---|---|---|---|---|
| August | 648 | -0.008 ± 0.006 | -0.024 ± 0.003 | -0.007 ± 0.010 | -0.041 ± 0.006 |
| September | 1,037 | -0.029 ± 0.007 | -0.018 ± 0.005 | -0.033 ± 0.006 | -0.025 ± 0.005 |
| October | 1,440 | +0.001 ± 0.005 | -0.008 ± 0.002 | -0.027 ± 0.005 | -0.014 ± 0.002 |
| November | 1,935 | +0.010 ± 0.003 | +0.006 ± 0.002 | -0.003 ± 0.005 | +0.004 ± 0.001 |
| December | 4,633 | +0.002 ± 0.001 | +0.000 ± 0.001 | -0.001 ± 0.001 | -0.001 ± 0.001 |
| Mean | | -0.005 | -0.009 | -0.014 | -0.015 |

Later months help only November, by +0.004 to +0.010; elsewhere they cost as much or more. The `Time basis:` line
now says the test months are unseen, not later, and gives this result.

## Review

**Outcome:** added. The AI recommends shipping it as defined; all issues are settled (the 40 repeated visits kept,
issue 1). Reviewed on 2026-11-04 without a panel, from the evidence already gathered (the record, the
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

**Main points:** Better-data check (2026-11-25, issue 7): Keep online_shoppers until a session record built from Google's GA360 sample of the Merchandise Store replaces it: that sample is readable here, has 45 times the usable visits over 12 months, and its hits let each visit be cut at a prediction point inside it, which removes the finished-visit gap of issue 3 and allows a forward split by month; the other event logs checked are weaker. Earlier: issue 1 settled on 2026-11-11 (repeats kept with a note); issue 4 on 2026-11-13 (`Target: Later`);
issue 6 on 2026-11-19 (leave one month out, `ForcedGroupedFromTemporal`, `Month` the group and no input), which
replaces the random split forced from temporal of issue 2 (2026-11-11); issue 3 on 2026-11-20 (the finished-visit
rows stay as an approximate stand-in, the gap named in `fit_reason`). Nothing open.

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
   * **Experiments:** the v0.2 rows rebuilt from the shipped container (June to December, `SpecialDay` dropped): 40
     repeats, 69 rows in repeat groups, all labelled No, all with 0 administrative and informational
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

   [^1e1]: **LEAK-41** (Must): repeats of a unit the data does not record get one verdict; natural when
     the look-alikes are distinct units (a coarse profile): the random split stays and the notes give the share of
     test rows with a look-alike in training. **LEAK-42** (Should): three tests set the verdict: a link
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
     categories), ROC AUC:
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
   `Samples: Over Time` and `Time: Dated`.

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

   Parked on 2026-11-11 on Andrej's mark ("We will get back to that."); reopened on 2026-11-20 (Andrej). **Decision:** keep (A) or retire for in-visit data (B)?

   **Resolved (2026-11-20, Andrej):** A (ok), as implemented: the finished-visit rows stay as an approximate stand-in, with the gap named in `fit_reason`. No definition change.

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

6. **Hold out whole months instead of random visits?**

   * **Problem:**
     - The visits carry their month (June to December), and the stationary-relation test found the relation not flat: a model trained on earlier months does clearly worse on November than one trained on November itself, and the purchase share moves from 10% in June to 25% in November.
     - Since 2026-11-17 the forced step holds out whole periods before it falls back to random[^s8]; your call of 2026-11-11 kept random when only random or windows were on the table.
     - Seven months are enough periods under either option of the cross-dataset item on the period count.
   * **Experiments:** stationary-relation test of 2026-11-18 (v2; the v3 re-run with the stronger comparison model confirms it: not flat), ROC AUC gap of the forward model ± one SD.

     | Month tested | LightGBM | Kumo-Tabular | Floor | Verdict |
     |---|---|---|---|---|
     | November | +0.054 ± 0.007 | +0.039 ± 0.004 | 0.003-0.004 | not flat |
     | October | -0.003 ± 0.006 | +0.001 ± 0.006 | 0.004 | flat |
     | December | -0.012 ± 0.004 | +0.003 ± 0.001 | 0.004 | flat |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 3 x 3 random folds over visits, `ForcedIIDFromTemporal` (implemented) | No change | No rebuild | Hides the November shift; skips the forced step's first remedy |
     | B | 3-fold CV over whole months, `ForcedGroupedFromTemporal` | The month is the group; the Time basis line gives the test | Tests a change between months, the shift a temporal split would test | Folds of unequal size (November holds 44% of the visits); trains on later months too |

   * **Recommendation:** B, because the relation is measured not flat and the data holds seven months to hold out. **Decision:** A or B?

   **Notes for the AI:** `Grouping(on="Month")`; decide with the curator whether `Month` stays an input (a held-out month is a level the model has not seen); one session per user, so no unit constraint; add a splits_comment; tree: online_shoppers leaves the departures.

   [^s8]: **SPLIT-8** (Must, amended 2026-11-17): "The closest regime holds out whole periods where the data has an order with at least two periods to hold out ... Without such periods it is grouped by the entity when an entity has several rows and the use case meets new entities ..., and IID otherwise."

   **Answer (AI, 2026-11-18):** reassessed with the new forced step (the interchangeable question first; measured not flat leads to whole periods or Too Small) and the pooled flat verdict.

   - The v3 test confirms not flat (November, and the purchase share moves 2.5-fold), so the branch is "measured not flat", whose only splits are whole periods or Too Small: A (random) is now outside every leaf.
   - Seven months give enough groupings for 3 repeats, so the leaf is `ForcedGroupedFromTemporal` (periods, measured not flat). Recommendation unchanged: B.

   **Andrej (2026-11-19, discuss):** Why do you suggest three fold CV although the target would rather be 9 folds and we could do CV over all months?

   **Answer (AI, 2026-11-19):** B is 9 splits, the target: three repeats of 3-fold CV over the seven months, each repeat grouping the months differently. CV over all months is a new option C: each month held out once, 7 splits.

   | Month | Visits | Train share when held out alone |
   |---|---|---|
   | June | 288 | 96% |
   | July | 432 | 94% |
   | August | 433 | 94% |
   | September | 448 | 93% |
   | October | 549 | 92% |
   | November | 2,998 | 56% |
   | December | 1,727 | 75% |

   (6,875 visits; February, March and May are left out by the definition.)

   * **B (3 x 3 over months):** 9 splits; each fold holds two or three months. November is 44% of the visits, so a fold holding November with December tests 69% of the data and trains on 31%; folds are of very unequal size, and the months in a fold change by repeat.
   * **C (leave one month out):** 7 splits, two under the target; each month is tested exactly once on all other months, train 56% to 96%, test 288 to 2,998 visits; no random grouping. The November shift the test found shows in one split of its own.

   | | Option | Splits | Train share | Test visits |
   |---|---|---|---|---|
   | B | 3 x 3-fold CV over whole months | 9 | about 31% to 96%, by grouping | 288 to 4,725 |
   | C | Leave one month out | 7 | 56% to 96% | 288 to 2,998 |

   **Recommendation:** C: every month tested once on all others, no fold under half the data; 7 is the most whole months allow. **Decision:** A, B or C?

   **Andrej (2026-11-19, discuss):** Reply (C): Leave one month out, but this would still be ForcedGrouped

   **Resolved (2026-11-19, Andrej):** C, tagged `ForcedGroupedFromTemporal`: seven folds, each month held out once and trained on all others (June 95.8% ... November 56.4%, December 74.9%); `Month` is the group and no input (a held-out month would be an unseen level); a `Time basis:` line gives the not-flat test. `dataset check`: 0 errors; `task_group_count_low`, `splits_dimensions_off_protocol` and `groups_test_groups_few` accepted with this decision, and `groups_largest_share_high` (November 44% of the visits) accepted as a real month: for you to confirm. Not rebuilt.

7. **Keep online_shoppers until a GA360 session record (cut at the 3rd pageview, split by month) replaces it, or keep it as it is?**

   * **Problem:**
     - Google's GA360 sample (903,653 visits, 2016-08-01 to 2017-08-01) cut at each visit's 3rd pageview gives 306,997 visits (3.7% buy) whose features end before any checkout step, and on it untuned LightGBM reaches ROC AUC 0.874 against 0.856 for logistic regression when trained on earlier months and tested on the next.
     - The same visits with their finished-visit totals added score 0.977, so the gap issue 3 accepted but could not measure is large in a store's own export; online_shoppers holds only finished-visit rows (6,875 visits, June to December, split by leaving one month out).
     - Keep online_shoppers until a GA360 session record replaces it, keep it as it is, keep both, or retire it now?
   * **Background:**
     - Current state: 6,875 visits of one shop (Sakar et al. 2019, UCI 468), June to December of one year, 16 features, 20% buy; split by leaving one month out (`ForcedGroupedFromTemporal`, issue 6), `Target: Later` (issue 4), repeats kept (issue 1). Issue 3 (2026-11-20) kept the finished-visit rows as an approximate stand-in, "revisit when the hit-level data ships". Nothing else is open.
     - `online_shoppers_purchase_intention` is the same table (OpenML 45560: 12,330 visits, 1,908 buyers, Sakar et al. as source, as in UCI 468), already `No` as `Duplicate`; not a candidate.
     - `google_analytics_customer_revenue_prediction` (`Yes`, priority 2) uses the same GA360 sessions for another task: each customer's revenue in a later window. Kaggle's v1 train.csv has the same 903,653 sessions as the BigQuery sample, without hits; v2 (train_v2 25.4 GB, test_v2 7.6 GB, August 2016 to October 2018) adds hits and 15 months, not downloaded here.
     - Candidates (the in-visit cut is the same for all: a visit enters at its 3rd page or item view, provided no checkout or purchase came earlier; the label is a purchase later in the visit):

       | Candidate | Visits (all → at the cut) | Buy rate at the cut | What it adds | Split it allows | Access, licence | Concerns | Verdict |
       |---|---|---|---|---|---|---|---|
       | GA360 sample, Google Merchandise Store (BigQuery `google_analytics_sample`, = `ga_merchandise_store_sessions`) | 903,653 → 306,997 (714,167 users) | 3.7% (11,415 buyers) | hit-level timeline, page paths, product views and cart adds before the cut; traffic source, device, country, visit number | 12 months by date: forward windows, each training on at least 70% | BigQuery, Google account needed; read here with the project's service account (about 0.3 GB scanned; GA4 about 1.2 GB); no licence stated, all users have viewer access | an obfuscated demo export; the session task and the prediction point are ours to define; 33% of cut visits belong to users with several | better |
       | GA4 sample, same store (BigQuery `ga4_obfuscated_sample_ecommerce`) | 360,129 → 107,670 | 4.5% (4,822) | event names (item views, cart adds, promotions, scrolls) | 3 months only (Nov 2020 to Jan 2021): ten-day windows | BigQuery, as above | 3 months; LightGBM below logistic regression | not better: shorter and does not separate methods |
       | YooChoose, RecSys Challenge 2015 (Kaggle mirror) | 9,249,729 → 4,417,474 | 8.2% | item, category and timestamp per click; the challenge's own task (will the session buy) | 6 months (Apr to Sep 2014) | Kaggle; CC BY-NC-ND 4.0 | no page type, device or source: AUC 0.63 at the cut | not better: features too thin for a tabular task |
       | REES46 cosmetics shop (Kaggle; the multi-category store of the same platform, 14.7 GB for two months, not downloaded) | 4,535,941 → 685,450 | 10.0% | product, brand, price, cart and remove events | 5 months (Oct 2019 to Feb 2020) | Kaggle; free use with attribution | 39,205 of 155,617 buying sessions (25%) hold no view: purchases are often logged under a session of their own, so the session label is broken | not better: label artefact |
       | Retailrocket (Kaggle) | 1,761,675 (sessionised by 30-minute gaps; no session id) → 157,394 | 3.1% | view, add-to-cart, transaction per item | 4.5 months (May to Sep 2015) | Kaggle; CC BY-NC-SA 4.0 | no session id; 9,463 of 14,297 buying sessions fall out at the cut (transactions without 3 views) | not better: sessions are reconstructed and most buyers lost |
       | Diginetica, CIKM Cup 2016 | not read | about 18,025 purchases over 5 months (paper) | views, queries, products | dates | Google Drive behind the CodaLab page; no licence found | no device or source | not checked on files; smaller than GA360 |

   * **Effect on the task:** none on this definition. The replacement keeps the use case (show an offer during a visit) and adds what issue 3 found missing: features that end at a prediction point inside the visit, and a forward split by month instead of one forced from temporal. It changes the shop (Google's merchandise store in place of a Turkish one) and the features (hit-level counts in place of the analytics' page-type figures; no `PageValues`).
   * **Experiments:** run on 2026-11-25. GA360 and GA4 read from BigQuery the same day (queries in the scripts folder); YooChoose, REES46 cosmetics and Retailrocket downloaded from Kaggle the same day. Untuned LightGBM (500 trees, learning rate 0.05, 31 leaves) against logistic regression (one-hot categories, log-scaled counts); ROC AUC; every window trained on all earlier data. online_shoppers on its shipped split (leave one month out).

     | Data | Rows | Split | LightGBM | Logistic regression | Gap |
     |---|---|---|---|---|---|
     | online_shoppers, finished visit (shipped) | 6,875 | 7 months, each held out | 0.843 (0.788 to 0.895) | 0.832 (0.781 to 0.886) | +0.011 |
     | GA360, cut at 3rd pageview | 306,997 | May, June, July 2017 | 0.874 (0.866 to 0.884) | 0.856 (0.848 to 0.864) | +0.018 |
     | GA4, cut at 3rd pageview | 107,670 | three ten-day windows of Jan 2021 | 0.712 (0.672 to 0.734) | 0.727 (0.721 to 0.732) | -0.015 |
     | REES46 cosmetics, cut at 3rd view | 400,000 of 685,450 | three windows of Jan-Feb 2020 | 0.756 | 0.720 | +0.036 |
     | Retailrocket, cut at 3rd view | 157,394 | three windows of Aug-Sep 2015 | 0.769 | 0.761 | +0.008 |
     | YooChoose, cut at 3rd click | 400,000 of 4,417,474 | three windows of Aug-Sep 2014 | 0.627 | 0.595 | +0.032 |

     - The finished-visit gap, measured where the hits allow it (same rows, same windows, the visit's final totals added):

     | Data | LightGBM at the cut | LightGBM with final totals | Best single final total |
     |---|---|---|---|
     | GA360 | 0.874 | 0.977 | final pageviews alone 0.932 |
     | GA4 | 0.712 | 0.973 | |
     | REES46 cosmetics | 0.756 | 0.926 | |
     | Retailrocket | 0.769 | 0.964 | |
     | YooChoose (buys in a separate file) | 0.627 | 0.745 | |

     - GA360 per month at the cut: 21,930 to 30,721 visits and a buy rate of 2.9% to 4.5%; 4 buyers had fewer than 3 pageviews and 133 reached a checkout step before the 3rd, so the cut keeps 11,415 of 11,552 buyers (98.8%). Country is set for 99.9% of rows (61% United States).
     - Scripts and results: the run's evidence folder (scripts/ga360_cut.sql, ga4_cut.sql, derive.py, baseline.py; results_*.csv; derived/*_stats.json).
   * **Consistency:** fiat_500 and body_density_prediction take the same decision in this batch (keep until the better record is added, then retire as replaced); all follow the pattern that a better dataset is its own record and the old one keeps the verdict its own data earn[^better]. Issue 3 named this replacement as the reason to revisit; option B is that revisit.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | online_shoppers ships; no replacement planned | keeps the verdict its own data earn; nothing to build | finished-visit rows whose gap is large in a comparable export; a forced split on 7 months |
     | B | Keep until a GA360 session record replaces it | a new record for GA360 visits cut at the 3rd pageview, split forward by month; online_shoppers retired as replaced once it is accepted | a prediction point inside the visit; 45 times the visits; 12 months for a forward split; methods separate | an obfuscated demo export and a task we define; BigQuery needs a Google account (Kaggle v2 is the 33 GB alternative); waits for the new record |
     | C | Keep both | as B, and online_shoppers stays | two shops for the same use case | one use case twice, the older one with the finished-visit gap |
     | D | Retire now | No (Retired), folder removed | no finished-visit stand-in | no session purchase task until the GA360 record is added |

   * **Recommendation:** B: GA360 is the only candidate that is larger, dated over a full year and rich enough in features (0.874 at the cut, methods separate by 0.018), and it answers issue 3 directly; online_shoppers stays valid until the replacement is checked and accepted[^valid]. **Decision:** A, B, C or D?

   **Notes for the AI:** On B: a dated CC line in online_shoppers' record naming `ga_merchandise_store_sessions` as the replacement; when that record is accepted, online_shoppers becomes No (Retired), folder removed, CHANGELOG entry. Build `ga_merchandise_store_sessions` from `bigquery-public-data.google_analytics_sample.ga_sessions_*` with the run's evidence folder (pipe the SQL into `bq query --use_legacy_sql=false --format=csv --max_rows=2000000` through stdin: a leading `--` comment breaks the argument form); drop rows with `funnel_before_cut`, never ship `fin_*`, `sid` or `uid`. Questions for that record's own review: the prediction point (3rd pageview here; a time cut is the alternative), whether visits of returning users across the cutoff stay (the shop knows its returning visitors; visit number is a feature[^entity]), the month windows, and its overlap with `google_analytics_customer_revenue_prediction` (same sessions, a user-level revenue task; both can stand as different tasks, or one record holds both). If BigQuery is not to be used, Kaggle `ga-customer-revenue-prediction` train_v2.csv/test_v2.csv carry the hits as JSON (33 GB, competition rules non-commercial; not checked here whether its hits are complete). On C: as B without the retirement. On D: No (Retired), folder removed, CHANGELOG entry.

   [^better]: Pattern "Small or dated, and the task is still done today": a larger or newer public dataset with the same target and use case is its own record; the old record is not rejected automatically and keeps the verdict its own data earn until the curator decides.
   [^valid]: Keep two questions apart (TP-6): is the task valid, and is it the best version? A valid task stays.
   [^entity]: SPLIT-13: an entity that recurs across the cutoff is part of the task when the model predicts for known entities, and a question when the use case is a new entity.

## Reference

Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM recurrent neural networks
By C. O. Sakar, S. Polat, Mete Katircioglu, Yomi Kastro. 2019

Published in Neural computing & applications (Print)
