---
unique_name: rosbank1
name: rosbank1
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
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

## Reference

Booster
