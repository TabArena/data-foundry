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
source_row: 745
type_adapter_id: curation-record-v1
---

# IEEE-CIS_Fraud_Detection

## Comments

CC: "Very nice fraud detection dataset (the best one I know). Requires temporal split - although the competition winners used grouped split (by month)"

"The TransactionDT feature is a timedelta from a given reference datetime (not an actual timestamp)."

" discussed the benefits of classifying clients (credit cards) instead of transactions in Kaggle's Fraud competition" -> need to make group structure part of the data by finding UIDs as well

Note: Possible data quality issue: The data is also grouped, but the group identifier is not explicitly given

## Reference

Addison Howard, Bernadette Bouchon-Meunier, IEEE CIS, inversion, John Lei, Lynn@Vesta, Marcus2010, and Prof. Hussein Abbass. IEEE-CIS Fraud Detection. https://kaggle.com/competitions/ieee-fraud-detection, 2019. Kaggle.
