---
unique_name: porto_seguro
name: porto-seguro
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2017'
domain: insurance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/porto-seguro-safe-driver-prediction
source_row: 646
type_adapter_id: curation-record-v1
---

# porto-seguro

## Comments

CC: "Data from Kaggle competition. Some ordinal features, definitely interesting. Top solutions applied some interesting feature engineering. We do not know much about the features given, but from what we know about the task it might be suitable to use random splits as the task likely has been designed time-invariant as the targets are always the ground truth of what happened in the future.; -1 maps to nan, needs preprocessing. While some information are missing, it is more likely than not that a random split is appropriate enough; need to make missing values to nans!"

## Reference

Addison Howard, Adriano Moala, and Walter Reade. Porto Seguro’s Safe Driver Prediction. https://kaggle.com/competitions/porto-seguro-safe-driver-prediction, 2017. Kaggle.
