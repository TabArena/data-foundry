---
unique_name: rosbank1
name: rosbank1
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
tags:
- Free Text (Short)
- '?'
- Review Prio 1 (Atlas)
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

CC (2026-10-21, Lennart): on CLEAN-19: "Okay, we here the case is that we want to take the best of both, or a reasonable combination, and not a union. so here we take the best for alfa as it is the top-solution etc, does that make sense?" (CLEAN-19, amended). The CoLES aggregates are a published baseline; the open question (REVIEW.md issue 5) is now whether a 2018 top solution's features are better, else CoLES stays.

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

## Reference

Booster
