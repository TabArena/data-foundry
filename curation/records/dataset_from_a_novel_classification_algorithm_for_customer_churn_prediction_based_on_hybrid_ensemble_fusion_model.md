---
unique_name: dataset_from_a_novel_classification_algorithm_for_customer_churn_prediction_based_on_hybrid_ensemble_fusion_model
name: Dataset from A novel classification algorithm for customer churn prediction based on hybrid Ensemble-Fusion model
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Data Requested
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2024'
domain: business & marketing
required_split:
- Random (IID)
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.nature.com/articles/s41598-024-71168-x
source_row: 877
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a private company churn table (2015-2022) that the paper barely describes; the data is "available on request" and was requested on 07/03/2026.
- Source: He and Ding (2024), "A novel classification algorithm for customer churn prediction based on hybrid Ensemble-Fusion model", Scientific Reports (doi:10.1038/s41598-024-71168-x, PMC11364882). The data: "a private dataset of the customer production line system of the Company from 2015 to 2022 is used, where 80% of the data is used for training and 20% of the data is used for testing" (Experiments); "Data is available on request from the author (Chenggang He)" (Data availability). Rows, columns, the target's definition and the industry are not stated.
- Use case: "facilitate the enterprises to take actions quickly and efficiently to retain customers", predicting "whether customers will churn in the following months" (Introduction, Fig. 2 text); actor a company's retention team, fit direct if the data matches; regime likely temporal (seven years of records, churn in the following months), not the paper's random 80/20; `required_split` left as is until the data is seen.
- Siblings and duplicates: the other churn-paper records (`dataset_from_feature_selection_based_dynamic_transfer_ensemble_model_for_customer_churn_prediction`, `dataset_from_research_model_of_churn_prediction_based_on_customer_segmentation_and_misclassification_cost_in_the_context_of_big_data`) are other companies' data; a private table cannot duplicate a public churn set. External collections: none.
- Papers and pages: the paper; its predecessor He et al. 2021 (ICTAI) on an "intelligent machine learning system" may use the same data.
- Metric: accuracy, AUC and F1 reported side by side, none named as the criterion, so the fallback `roc_auc` (MET-5, MET-8).
- Risks for /add-dataset: no access (`Data Requested`, no answer recorded); unknown features and churn definition (USE-5); the paper says the collected data had "no labels to mark customer churn" before cleaning, so the label is the authors' construction.
- Priority: gap - (business, binary), use case + (retention named), source - (the paper does not describe the table), shape - (unknown), risk 0.

Dataset underlying a 2024 Nature Scientific Reports paper on customer churn prediction via a hybrid ensemble-fusion model; churn is a standard real-world tabular binary-classification task. The record notes the data was formally requested from the authors on 07/03/2026, so it is not yet in hand and may be one of the common public telecom-churn sets (potential duplicate risk). It maps well to the in-scope criteria if the data is original and obtainable. A human must confirm the data arrives, verify it is not a re-upload of an existing TabArena churn set, and check size/target.

---

Data Requested on 07/03/2026 by Lennart

## Reference

https://www.nature.com/articles/s41598-024-71168-x
