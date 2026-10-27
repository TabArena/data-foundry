---
unique_name: customer_retention_in_the_media_industry_datathon
name: customer-retention-in-the-media-industry-datathon
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Kaggle
domain: business & marketing
required_split:
- Temporal (NON-IID)
- '?'
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/customer-retention-in-the-media-industry-datathon/overview
- https://www.kaggle.com/competitions/customer-retention-datathon-amsterdam-edition
- https://www.kaggle.com/competitions/kkbox-churn-prediction-challenge
source_row: 1043
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: the files look like a re-use of KKBox's WSDM Cup 2018 churn
data, a strong real churn task; the record should probably take KKBox as its source (PROV-8).
- Source: two Kaggle community datathons (June 2024 and an Amsterdam edition, October 2024, "using Google Cloud
  Platform"), the same five files each: `members.csv` (427,921,437 bytes), `transactions.csv`, `user_logs.csv`,
  `train_data.csv`, `kaggle_test_data.csv`. These names and the members size match KKBox's Churn Prediction Challenge
  (Kaggle, WSDM Cup, launched 2017-09-18: `members_v3`, `transactions`, `user_logs`, `train`), so the first publication
  is most likely KKBox 2017 (unverified: the datathon pages render no text and its files need an accepted entry).
- Use case: KKBox's retention team predicts whether a subscriber renews within 30 days after the subscription expires
  (KKBox page; labeller script `WSDMChurnLabeller.scala` published); fit direct. Regime temporal (KKBox labels users
  by expiry month: train February, test March 2017).
- Siblings and duplicates: no KKBox record in `curation/records/`; the two datathons share one file set (one record is
  right). External collections: none found.
- Papers and pages: Kaggle kkbox-churn-prediction-challenge (WSDM 2018 Cup); solutions on GitHub (e.g. WSDM_2018).
- Metric: the datathons score ROC AUC (Kaggle API `evaluationMetric`), KKBox scored log loss (Kaggle API). The
  original task's metric is log loss (MET-1, MET-4); inputs none.
- Risks for /add-dataset: heavy joins (user_logs 1.4 GB, transactions with dates after the cut-off must be filtered:
  LEAK), a label leak was reported in KKBox v1 and the labels were re-issued (train_v2), and the datathon may have relabelled or
  subsampled; confirm the source before choosing which files to use.
- Priority: gap 0, use case +, source + (KKBox, WSDM Cup), shape + (millions of users, temporal), risk - (joins,
  known label leak in v1).

Kaggle datathon (media-industry customer retention / churn), a genuine real-world predictive task that is a natural binary churn classification. Churn challenges typically supply multiple tables (subscription, activity, demographics) needing a join, and a temporal split is often the intended protocol. This fits the in-scope tabular criteria well, but I have not verified the dataset is downloadable, its size, the exact target, or whether the two linked competitions share data. A human must confirm data availability, the precise target column, table layout, and split regime.
