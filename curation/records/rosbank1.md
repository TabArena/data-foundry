---
unique_name: rosbank1
name: rosbank1
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
tags:
- Free Text (Short)
- '?'
- Review Prio 1 (Atlas)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
- Dated Event Log
collections:
- New (BeyondArena)
original_source: Other
year: '2018'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://boosters.pro/championship/rosbank1/data
- https://huggingface.co/datasets/pytorch-lifestream/rosbank-churn
v2_path: datasets/_dev/tabarena-v0pt2/rosbank1/dataset.py
source_row: 643
type_adapter_id: curation-record-v1
---

## Comments

"predict customer churn after a card is used for a discounted rate, and predict the spending volume over the next three months for customers who continue to use the card." ROC AUC / RMSE
"For both tasks, participants are given a single dataset containing customer transaction history for three months of discounted use of a banking product. Task 1: In the first task, you will solve a binary classification problem—predicting customer churn. Task 2: In the second task, you will need to predict the volume of transactions via a POS terminal over the next three months of product use."


Same datasets, different targets. Need to decide for one that we deem better

Might be streaming event data (?), need to figure out when looking at the data

**Assessment (AI, 2026-10-07):** The two targets are one signal: target_flag is 1 exactly when target_sum > 0 ("Значение 0 соответствует отказу", the task text), so churn means no POS purchase in the three months after the grace period. One transaction sequence and one label per client make one row per client a fixed task, not streaming data (CoLES, arXiv 2002.08232, Tables 6-7: aggregates 0.825 AUC, sequence models 0.817-0.843). The competition ran 27 April to 28 May 2018 (boosters.pro API) and the transactions end on 2 April 2018; periods ending in March 2018 churn 24 of 36, so periods ending from January 2018 are dropped as censored. Defined as churn, temporal with a three-month label gap. No licence stated.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case -, source +, shape +, no known risk. Bank-card churn from transaction sequences, temporal, but small test windows (63-515 clients) cannot separate model families.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; the curator decides the target (churn only), the feature set against alfa_battle_2_0_task_2 (CLEAN-19) and the mixed currencies (CLEAN-21). Applied in the definition: the label timing rests on the measured March 2018 anomaly and an unpublished label window (a test found no calendar-window effect in channel type1), the period-end upper bound and the 107 of 479 post-period buyers who churned (no leak), the test windows' intake drop and season, the currency shares, and refreshed `no_spread` numbers. Corrections to the assessment of 2026-10-07: "Значение 0 соответствует отказу" is from a participant notebook (kianya/rosbank-competition), not the task text, and so is the reading of `channel_type` as the acquisition channel; in CoLES Table 6 the aggregates (0.825) are level with the supervised sequence model (0.817) and above CPC, RTD and SOP (0.782 to 0.802), but below CoLES embeddings fed to LightGBM (0.843). Priority 2: gap 0, use case 0, source 0, shape +, risk 0 (no thin domain, type or regime; the retention use is our framing, the source names only churn prediction; the source publishes no column descriptions or label window; no open issue raises a leak or an unclear target, as the panel settled the label timing).

CC (2026-10-21, Lennart): on CLEAN-19: "Okay, we here the case is that we want to take the best of both, or a reasonable combination, and not a union. so here we take the best for alfa as it is the top-solution etc, does that make sense?" (CLEAN-19, amended). The CoLES aggregates are a published baseline; the open question (Review issue 5) is now whether a 2018 top solution's features are better, else CoLES stays.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC - Area Under the ROC Curve (task 1, churn); task 2 POS spend used RMSE (https://boosters.pro/api/champ/champ?champname=rosbank1 (metric: 'AUC', checked 2026-10-21)).

CC (2026-10-26, Lennart): issue 1: churn only, no second folder for the spend target (PROV-6: a swapped target of the same rows is a duplicate).

CC (2026-10-26, Lennart): issue 8: "ok keep the temporal split as is" (SPLIT-1, SPLIT-9).

CC (2026-10-26, Lennart): issue 7, option (c): amounts are converted to rubles at the Bank of Russia's official daily rate ("try to fix this"; CLEAN-21, the measuring body's conversion).

**Assessment (AI, 2026-10-26):** issue 7 applied. amount is converted at the Bank of Russia's rate in force on the transaction's day (XML_dynamic series of the 30 currencies it quoted then, downloaded 2026-10-26, pinned by checksum in download_description). The currency codes have no codebook; the conversion confirms the ISO 4217 numeric reading (810 and 643 rubles): converted, the median POS purchase of every currency with 30 or more lies between 355 and 3,346 rubles, against 500 in rubles and 8 to 671,000 units before. The 1,466 transactions (0.3%, 184 clients) in 27 currencies the Bank did not quote on their day (baht, dirham, lari, kuna, rupiah, dong and smaller ones; Hong Kong dollars before April 2017) keep their counts and leave the amount statistics. std_amount_trx_CASH_ADV became constant (one kept client with two cash advances in a quoted currency) and is dropped. dataset check: 0 errors, 0 warnings. Issue 5: a search found the 1st place of task 1 (Kirill Khrylchenko, private AUC 0.8747) published with code (github.com/KhrylchenkoKirill/rosbank); the comparison with the CoLES features on our windows is running.

**Assessment (AI, 2026-10-26):** issue 5 compared. Khrylchenko's (1st place, task 1) feature blocks rebuilt from his code on our transactions in rubles (his own CV on the rebuild matches his notebooks: time 0.848 against 0.852, money 0.831 against 0.830). Untuned LightGBM, ROC AUC over the three windows: CoLES 0.855, his full set 0.882 (2,320 columns), CoLES plus his time and MCC-time blocks 0.893 (+.038 ± .016), CoLES plus his time block alone +.045; the gain comes from the October window (515 clients, about 4 SE). His repository has no licence; no code copied. Recommendation on the page: CoLES plus his time block (CLEAN-19, a reasonable combination).

CC (2026-10-26, Lennart): issue 5, option (c): CoLES plus the time block of the 1st place (Khrylchenko) (CLEAN-19, a reasonable combination).

**Assessment (AI, 2026-10-26):** issue 5 applied: `time_features`, our rewrite of the 1st place's time block (no code copied; his repository has no licence): for all transactions, each category, money in and money out, the span, spread, position and gaps of the active days, the same over the last active month, active days per month and the quarter of the last month; 349 columns after dropping copies. Untuned LightGBM on the three windows: CoLES 0.857, with the time block 0.896 (+0.038; October +0.051); 300 trees 0.853 against 0.891. dataset check: 0 errors, 0 warnings.

**Assessment (AI, 2026-10-26):** probes on the definition with the time features: task probes LightGBM 0.891, random forest 0.883, linear 0.823, no flag (the earlier `no_spread` is gone: LightGBM leads linear by 0.136, paired SE 0.042). Leak probes: the strongest single feature is `time_pos_span` (0.853 alone), the span of the client's POS activity, i.e. recency, the signal of the 1st place's best block; the file holds no transactions from the label window (LEAK-10, 2026-10-20), and dropping the feature changes the probe's model from 0.878 to 0.889, so no single column carries the task. No open issue left.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `sber_mbd_product_propensity` (TBD -> 2nd Tier, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Lennart): accepted `time_newest_period_short` with its reason (cross-dataset item "What to do with a newest period that holds far fewer rows than the periods before it?", A).

**Assessment (AI, 2026-11-11):** the periods ending in November and December 2017 hold 123 and 63 clients against 416 to 524 a month from May to October.

CC (2026-11-17, Andrej): the declared split (temporal on `period_end`, windows of 1 month, windows while training keeps 50% of the rows (3 in the build), gap 3 months) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-20, Andrej): split kept (Review issue 1, A as implemented): the three monthly windows, the reason in the splits comment.

## Review

**Outcome:** added. Reopened on 2026-11-19 by the split check: the definition ships fewer windows than the target count for its size, without the reason in its splits comment.

**Main points:** Which window layout (issue 1).

**Issues for Andrej:**

1. **Windows: 3 of the target's 9; which layout?**

   * **Problem:**
     - With one-month windows and the three-month label gap, only three months train on half the clients or more: September 2017 trains on 44.5%. The target an IID split of 4,791 clients would get is 9[^split33][^split15].

       | Test window | Clients | Churned | Train | Train share |
       |---|---|---|---|---|
       | December 2017 | 63 | 23 | 3,566 | 74.4% |
       | November 2017 | 123 | 49 | 3,078 | 64.2% |
       | October 2017 | 515 | 179 | 2,559 | 53.4% |

     - What the source fixes: the label covers "the next three months" after the period, so the three-month gap stays. What is assumed: the monthly refit; `splits_comment` says "refit, for example every month", and the source is silent on the cadence.
     - The two newest windows are the thin tail of the client intake (123 and 63 clients against 416 to 524 a month from May to October; accepted by Lennart on 2026-11-11), and every test label window spans the New Year, which no training label window does.
     - Shorter calendar windows do not help on their own: the newest half month (16 to 30 December) and the newest two weeks hold 25 and 23 clients, under the 33 a test window needs[^split14].
     - Overlapping windows are not needed: B reaches the target without them (one-month windows every 10 days would give 8 at half or more).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three monthly windows (implemented), the reason in `splits_comment` | 3 windows, train 53.4% to 74.4%, test 63 to 515 clients, 23 to 179 churned | the monthly refit as assumed; nothing to rebuild | 6 short of the target; two of the three windows are the thin tail |
     | B | Nine windows of equal size, at half the data or more | about 100 clients each by `period_end`, 19 September to 30 December 2017, cut at day boundaries; train 50.1% to 70.7%, test 77 to 111, 30 to 43 churned | reaches the target; equal test sizes; no window under half | windows of 4 to 41 days, not the monthly refit; neighbouring windows train on sides 1 to 3 points apart, so they test nearly one model; a custom `_make_splits` |
     | C | Monthly windows down to 30% (the curator's exception) | 6 windows, December back to July 2017; September, August and July train on 44.5%, 35.8% and 32.6%; test 63 to 524, 23 to 216 churned | keeps the monthly cadence; adds 1,531 clients of the regular intake and label windows that end before the New Year, which the newest three lack | three windows under half need your sign-off; 3 short of the target |
     | D | Nine windows of equal size, down to 30% | about 250 clients each, 28 June to 30 December 2017; train 30.1% to 62.5%, test 248 to 263, 89 to 116 churned | reaches the target with larger, equal windows | 5 windows under half; windows of 12 days to 2 months; the newest window spans November and December |

   * **Recommendation:** C: it keeps the cadence the use case assumes and adds the periods the thin newest windows lack, which is what the curator's exception is for. **Decision:** A, B, C or D?

   **Notes for the AI:** on A, add to `splits_comment`: "Three windows, against the 9 an IID split of 4,791 clients would get: with one-month windows and the three-month label gap, September 2017 would train on 44.5% of the clients (the date of your decision, Andrej)." On C: `TemporalSplits(window=1, unit="months", gap=LABEL_MONTHS, min_train_fraction=0.3)`, `splits_train_under_half` accepted for July to September 2017 with the reason, the window table in `splits_comment` (the "fourth window" sentence goes), `splits_rows_unused` re-worded (the September clients are tested), `task_summary.split`. B and D need a custom `_make_splits` (windows of equal client counts on `period_end`, each training on the clients whose period ended three months before the window starts). Then `dataset check` on Slurm, a CHANGELOG entry and a CC line. The record has no Review section yet; this is its first issue.

   **Andrej (2026-11-20, ok):** As implemented (A).

   **Resolved (2026-11-20, Andrej):** A, as implemented: the three monthly windows, the reason in the splits comment. Not rebuilt.

   [^split14]: **SPLIT-14** (Must): at least 3 windows; every window trains on at least half the data, lower only as the curator's exception down to 30%; every test window holds at least 33 scored units.

   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others): the number of windows aims at the count an IID split would get; the use case sets the window length, step and gap, which are never shortened to reach the count; fewer are accepted, never under 3, with the target, the count reached and what stops more windows in the splits comment; overlapping windows are only offered.

   [^split33]: **SPLIT-33** (Should): an IID or grouped split gets 3-fold cross-validation with 20, 10, 3 or 1 repeats by the units on its train side; SPLIT-15 aims a temporal split at the same count, here 9.

## Reference

Booster
