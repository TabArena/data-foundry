---
unique_name: home_credit_default_stability
name: Homecredit Default
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2024'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability
- https://github.com/yandex-research/tabred/tree/main/preprocessing#homecredit-default-stability-homecredit-20
notebook_path: datasets/beyond_iid/temporal/home_credit_default_stability/home_credit_default_stability_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/home_credit_default_stability_1m/dataset.py
source_row: 710
type_adapter_id: curation-record-v1
---

## Comments

Follow the preprocessing from TabRed as well. Verify that TabRed preprocessing gets similar feature sets to top solutions

Kaggle solutions used IID CV splits. There is also a problem with metric hacking on the Kaggle submissions.

TabRed uses 4/5 month as time horizon

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric stays the default `roc_auc`: the competition scored "Home Credit 2023 - Gini Stability" (Kaggle API), the mean weekly Gini with a penalty for a falling trend and for the spread around it; it needs the week of each row and is no listed metric, and ROC AUC is the per-week score it is built from (definitions.md, Field mapping, rule 4). The notes now name the original. Needs a rebuild to reach the container (notes only).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: isbidproduct_1095L (boolean) and 5 aggregates that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: isbidproduct_1095L (explicit). Reverted: posfpd10lastmonth_333P, posfpd30lastmonth_3976960P, posfstqpd30lastmonth_3976962P, mean_contaddr_smempladdr_334L, mean_safeguarantyflag_411L (aggregates) stay numeric.

## Reference

Daniel Herman, Tomas Jelinek, Walter Reade, Maggie Demkin, and Addison Howard. Home Credit - Credit Risk Model Stability. https://kaggle.com/competitions/home-credit-credit-risk-model-stability, 2024. Kaggle.
