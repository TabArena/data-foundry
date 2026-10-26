---
unique_name: dataset_from_research_model_of_churn_prediction_based_on_customer_segmentation_and_misclassification_cost_in_the_context_of_big_data
name: Dataset from Research Model of Churn Prediction Based on Customer Segmentation and Misclassification Cost in the Context of Big Data
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Data Requested
tags:
- '?'
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2015'
domain: business & marketing
required_split:
- Random (IID)
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- http://dx.doi.org/10.4236/jcc.2015.36009
- https://www.scirp.org/journal/PaperDownload.aspx?paperID=56907
source_row: 796
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 3: a large real Chinese telecom churn snapshot (about 1M customers, 25 attributes, 2.8% churn) with a clear retention use case, but private: no data availability statement, requested on 07/03/2026.
- Source: Liu and Zhuang (2015), "Research Model of Churn Prediction Based on Customer Segmentation and Misclassification Cost in the Context of Big Data", Journal of Computer and Communications 3, 87-93 (doi:10.4236/jcc.2015.36009, open access, CC BY). Sec. 3.1: "we select customer consumption listings from November 2014 to January 2015 and churn data for February 2015 as our model data. This data contains a total of 1,048,575 records and 25 customer attributes like customer ID, costs, traffic, voice package information etc."; Sec. 3.2: 1,016,610 records after removing abnormal ones, "including 27,925 customer churn records" (2.8%), 19 attributes kept.
- Use case: "Companies are able to previously recognize the consumers who are ... move toward a competitor by churn prediction, then, take appropriate marketing campaigns to maintain and retain these customers" (Sec. 1); actor the operator's retention team, moment end of January 2015, decision whom to target; fit direct; regime IID (one snapshot, one row per customer).
- Siblings and duplicates: no other record of this data; the other churn-paper records are other companies. External collections: none.
- Papers and pages: the paper only.
- Metric: "accuracy and coverage" (coverage is the churn recall) on a 3:1 resampled set with an unstated misclassification cost (Sec. 3.3), threshold metrics without a fixed threshold or cost (MET-6), so the fallback `roc_auc` (MET-8).
- Risks for /add-dataset: no access (`Data Requested`); 1,048,575 is the Excel row limit (2^20 - 1), so the table the authors had was likely cut at export: a selective sample (PROV-6, `Not Representative`) to ask about; the K-means segment is the authors' construction (not a feature to ship as given).
- Priority: gap - (business, binary, IID), use case + (retention named, direct), source + (the paper documents window, size and churn rate), shape + (1M rows, 25 attributes), risk - (the Excel cut).

Dataset behind a 2015 JCC paper on churn prediction using customer segmentation and misclassification cost; churn is an in-scope real-world tabular binary-classification task. The data was requested from the authors on 07/03/2026 and is not yet available, and older churn papers frequently use the widely-circulated public telecom-churn data (duplicate risk). It plausibly fits the criteria pending data delivery. A human must confirm the data is obtainable, original (not a re-upload of an existing TabArena/UCI churn set), and check its size and target.

---

Data Requested on 07/03/2026 by Lennart
