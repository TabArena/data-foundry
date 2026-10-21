---
unique_name: rosbank1
name: rosbank1
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
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

## Reference

Booster
