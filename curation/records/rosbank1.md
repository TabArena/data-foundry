---
unique_name: rosbank1
name: rosbank1
checked_by:
- Lennart
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
- '?'
problem_type: TBD
original_data_state: One Table
source_links:
- https://boosters.pro/championship/rosbank1/data
- https://huggingface.co/datasets/pytorch-lifestream/rosbank-churn
source_row: 643
type_adapter_id: curation-record-v1
---

## Comments

"predict customer churn after a card is used for a discounted rate, and predict the spending volume over the next three months for customers who continue to use the card." ROC AUC / RMSE
"For both tasks, participants are given a single dataset containing customer transaction history for three months of discounted use of a banking product. Task 1: In the first task, you will solve a binary classification problem—predicting customer churn. Task 2: In the second task, you will need to predict the volume of transactions via a POS terminal over the next three months of product use."


Same datasets, different targets. Need to decide for one that we deem better

Might be streaming event data (?), need to figure out when looking at the data

## Reference

Booster
