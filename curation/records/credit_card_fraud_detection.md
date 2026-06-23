---
unique_name: credit_card_fraud_detection
name: Credit Card Fraud Detection
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Data Quality Issue
tags:
- Non-IID (Temporal)
collections:
- New - IST
source_links:
- https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/data
source_row: 56
type_adapter_id: curation-record-v1
---

# Credit Card Fraud Detection

## Comments

"result of a PCA transformation. Unfortunately, due to confidentiality issues, we cannot provide the original features and more background information about the data. Features V1, V2, … V28 are the principal components obtained with PCA"

Thus, we know that any train test split would simulate transductive learning. This kind of transductive learning would be impossible for some the test splits 

Domain expert: "Given the PCA transformation applied across the full time horizon, it is not an ideal setup for benchmarking"
