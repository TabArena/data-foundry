---
unique_name: ieee_fraud_detection
name: IEEE-CIS_Fraud_Detection
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Data Quality Issue
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: Kaggle
year: '2019'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/ieee-fraud-detection
notebook_path: datasets/beyond_iid/temporal/ieee_fraud_detection/ieee_fraud_detection.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/ieee_fraud_detection/dataset.py
source_row: 745
type_adapter_id: curation-record-v1
---

## Comments

CC: "Very nice fraud detection dataset (the best one I know). Requires temporal split - although the competition winners used grouped split (by month)"

"The TransactionDT feature is a timedelta from a given reference datetime (not an actual timestamp)."

" discussed the benefits of classifying clients (credit cards) instead of transactions in Kaggle's Fraud competition" -> need to make group structure part of the data by finding UIDs as well

Note: Possible data quality issue: The data is also grouped, but the group identifier is not explicitly given

CC (2026-10-01, Lennart): Leak audit, kept as is. The engineered `uid` (card1 + addr1 + D1 anchor, from the 1st-place Kaggle solution) carries labels across the temporal split: the host labels a chargeback card and its later linked transactions as fraud, so test rows whose uid had fraud in train are about 95% fraud (15-17% of test rows have a uid seen in train). This is legitimate history under the host's labelling rule, not a leak, and it is worth little: dropping uid moves LightGBM AUC by -0.007 to -0.001 (0.911 -> 0.903 on split 0, 0.908 -> 0.907 on split 1), and dropping uid plus the row-ID/time proxies (TransactionID, day, date) gives 0.906. The Data Quality Issue marker (uid is not given by the host) stays.

## Reference

Addison Howard, Bernadette Bouchon-Meunier, IEEE CIS, inversion, John Lei, Lynn@Vesta, Marcus2010, and Prof. Hussein Abbass. IEEE-CIS Fraud Detection. https://kaggle.com/competitions/ieee-fraud-detection, 2019. Kaggle.
