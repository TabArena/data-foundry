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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the datathon's labelled table is 946,686 users with is_churn, plus 24,274 test users without public labels, so it is not a 2-million-row table. The "millions" are the members (about 6.8 million) and the listening log rows (about 18.4 million). The files match the v2 release of KKBox's churn challenge (WSDM Cup 2018). The call stands at priority 3 with KKBox as the source (PROV-8).
- As published: both datathons ship the same five files, with the same byte sizes (Kaggle API file listing): https://www.kaggle.com/competitions/customer-retention-in-the-media-industry-datathon (files of 2024-07-01) and https://www.kaggle.com/competitions/customer-retention-datathon-amsterdam-edition (files of 2024-10-17). The files: members.csv 427,921,437 bytes, transactions.csv 115,394,513, user_logs.csv 1,431,465,728, train_data.csv 44,494,256 and kaggle_test_data.csv 1,092,335. Downloads need an accepted entry (the API answered "You must accept this competition's rules before you'll be able to download files"), so columns and rows were not read. The event was Endava's "joint datathon hosted with Google Cloud" at Google's Warsaw office on 4 June (https://info.endava.com/enhancing-customer-retention-in-the-media-industry-datathon), with no data source named. The KKBox challenge (https://www.kaggle.com/competitions/kkbox-churn-prediction-challenge, 2017) ships train.csv, train_v2.csv, members_v3.csv, transactions.csv, transactions_v2.csv, user_logs.csv, user_logs_v2.csv, sample_submission_v2.csv and WSDMChurnLabeller.scala (Kaggle API). No official row count was found. A public project (https://github.com/aatmanpandya/music-subscription-churn) gives train 993K, train_v2 971K, members_v3 6.8M, transactions 21.5M, transactions_v2 1.4M, user_logs 392M (30 GB) and user_logs_v2 18.4M rows; others give train_v2 as 970,960 users with 8.99% churn.
- The task's table: train_data.csv has 946,686 rows and kaggle_test_data.csv 24,274, computed from the byte sizes under KKBox's layout: a 44-character msno, "msno,is_churn" lines of 47 bytes, "msno" lines of 45 bytes, plus the header. Both sizes divide exactly, and 946,686 + 24,274 = 970,960, the user count of KKBox's train_v2 (March 2017 expiries). So the datathon is KKBox's v2 release with train_v2 split into a train and a hidden test, and by size members.csv, transactions.csv and user_logs.csv are members_v3, transactions_v2 and user_logs_v2. The unit is a user whose subscription expires in the label month. The inputs are ours to build: member attributes, transaction aggregates and daily listening aggregates, about 20 to 40 features after aggregation (estimated). KKBox labels two months: train (February 2017, about 993K users) and train_v2 (March 2017, 970,960), about 1.96 million user-months together, with users repeated. The April 2017 test labels were never released. More months would need our own labels from the transactions with KKBox's labeller script.
- Access: Kaggle login and acceptance of the competition rules, for the datathons and for KKBox; no licence text was read (the competition pages render no text here). KKBox's files are 7z archives: user_logs.csv.7z 7,136,060,375 bytes (the 30 GB log), transactions.csv.7z 707,508,779, user_logs_v2.csv.7z 685,951,221, members_v3.csv.7z 242,308,558, the rest under 50 MB each.
- Changes the call: the size. The labelled table is under one million users for the datathon and under two million user-months for KKBox's two labelled months, so the record does not belong in the 2-million-row list. The source: the datathon re-releases KKBox's v2 files with the train labels split off (PROV-8: the first publication is KKBox 2017), and the datathon's hidden test labels are public in KKBox's train_v2. Building from KKBox adds a second labelled month (February 2017) for a temporal split. The screening's point stands that transactions and logs run past many users' expiry and need a cut at each user's expiry (LEAK). Priority 3 stands under KKBox. Moving the record's name and links to KKBox is the curator's call.
- Not checked: the datathon's columns, row counts and any relabelling (the files sit behind the rules; the counts above are computed from byte sizes); official KKBox row counts (taken from public projects, not from Kaggle); the licence terms of either competition.
