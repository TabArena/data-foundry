---
unique_name: porto_seguro
name: porto-seguro
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Anonymized
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
notebook_path: datasets/beyond_iid/new_iid/porto_seguro/porto_seguro.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/porto_seguro/dataset.py
source_row: 646
type_adapter_id: curation-record-v1
---

## Comments

CC: "Data from Kaggle competition. Some ordinal features, definitely interesting. Top solutions applied some interesting feature engineering. We do not know much about the features given, but from what we know about the task it might be suitable to use random splits as the task likely has been designed time-invariant as the targets are always the ground truth of what happened in the future.; -1 maps to nan, needs preprocessing. While some information are missing, it is more likely than not that a random split is appropriate enough; need to make missing values to nans!"

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric `normalized_gini_coefficient` replaced by the default `roc_auc`: for a binary target the normalized Gini is 2 x ROC AUC - 1, so both rank models the same, and a listed name is scored downstream while an unlisted one falls back to the default. The notes name the Gini. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — the competition's normalized Gini coefficient, 2 x AUC - 1 for a binary target, which ranks models the same as ROC AUC (Kaggle evaluation page).

## Reference

Addison Howard, Adriano Moala, and Walter Reade. Porto Seguro’s Safe Driver Prediction. https://kaggle.com/competitions/porto-seguro-safe-driver-prediction, 2017. Kaggle.
