---
unique_name: churn_telco_nigeria
name: CHURN_TELCO_NIGERIA
checked_by:
- Lennart
suggestion: 'Yes'
decision_markers:
- Trivial
tags:
- New IID
collections:
- TabSTAR
original_source: Kaggle
year: '2018'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=44230
- https://www.kaggle.com/competitions/dsntelecomschurn2018/data
source_row: 675
type_adapter_id: curation-record-v1
---

## Comments

100% accuracy possible? 50/50 churn rate.

The discussion and state of the competition is a bit hard to parse. I would say yes for now and we can test if the train data is trivial later.

**Assessment (AI, 2026-10-07):** Duplicate of churn_telco_south_asia. TRAIN.csv and TEST.csv are the 2,000 rows of the SATO 2015 file (kaggle.com/datasets/mahreen/sato2015): every row matches on the nine numeric columns, all 1,400 train labels agree, and the competitor networks are renamed one to one (ufone → Uxaa, ptcl → PQza, ...). The 100% scores come from DSN's cut: TEST holds the actives with total spend 1,282-3,491 and the churners with 226-604, so "spend < 1000 → churned" is perfect, and TRAIN keeps 340 rows in those bands with the opposite labels only. On the 2,000 SATO rows the task is not trivial (30 splits: random forest AUC 0.815, best single feature 0.681). Suggest No + Duplicate; ship the SATO file as churn_telco_south_asia.

## Reference

Kaggle / Broken Website
