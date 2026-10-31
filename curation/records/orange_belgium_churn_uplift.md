---
unique_name: orange_belgium_churn_uplift
name: 'A churn prediction dataset from the telecom sector: a new benchmark for uplift modeling (Orange Belgium churn-uplift dataset)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
original_source: OpenML
year: '2023'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://arxiv.org/abs/2312.07206
- https://www.openml.org/search?type=data&id=45580
- https://github.com/TheoVerhelst/Churn-Uplift-Dataset-Paper
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 11,896 high-risk Orange Belgium subscribers of three 2020 retention campaigns, churn within two months, published as an uplift benchmark with anonymized features; real operator data with a stated label window, approximate as a plain churn task.
- Source: Verhelst, Mercier, Shrestha and Bontempi (Machine Learning Group, ULB, with Orange Belgium), "A churn prediction dataset from the telecom sector: a new benchmark for uplift modeling", ECML PKDD 2023 Workshop on Uplift Modeling and Causal ML (arXiv 2312.07206, December 2023, HTML read); the data first on OpenML 45580 `churn-uplift-mlg` (uploaded 2023-07-06 by the MLG, collection date 09-2020, target `y`, CC BY-NC-ND): "Anonymized dataset of churn and uplift modeling from a series of marketing campaigns in 2020 by a telecom company". As published (Sec. 2-3): "11,896 samples and 178 features" on demographics, usage and subscription; three campaigns "conducted between September and December 2020"; each month a model scored churn risk, "the riskiest customers were selected", a random subset kept as control and the rest called with an offer or a tariff recommendation (treatment rate 75.74%, Table 1); "The churn outcome is determined in a two-month window following the campaign".
- Use case: Orange Belgium's retention team decides each month which high-risk customers the call centre contacts (Sec. 2). For the source this is an uplift decision (who changes behaviour when called); as churn classification with the treatment flag as an input, the fit is approximate. Regime IID (the paper uses 3-fold cross-validation repeated 10 times, Sec. 5; whether the campaign month ships is not stated).
- Siblings and duplicates: the telco churn records it was found for: `churn_telco_south_asia` (`Yes`), `mobile_churn` (`Yes`, `Missing source information`), `iranian_churn` (`No (Retired)`), `churn` (`No (Retired)`, AHDS), `ibm_telco_customer_churn` (`No`, AHDS) and two paper records with private data; `orange_telecom_s_churn_dataset` (`No`, `Duplicate`) is the KDD Cup 2009 Orange data, another release. Randomized-campaign precedent: `hillstrom_email_campaign` (AI `TBD -> Yes`, priority 3, the arm kept as a feature, the uplift framing noted). No other record of this data (grep: 45580, churn-uplift, 2312.07206). External collections: none found.
- Better data: found as better data for `churn`, `churn_telco_south_asia`, `dataset_from_feature_selection_based_dynamic_transfer_ensemble_model_for_customer_churn_prediction`, `dataset_from_research_model_of_churn_prediction_based_on_customer_segmentation_and_misclassification_cost_in_the_context_of_big_data`, `ibm_telco_customer_churn`, `iranian_churn` and `mobile_churn`; no further search this round.
- Papers and pages: the paper above and its repository (github.com/TheoVerhelst/Churn-Uplift-Dataset-Paper).
- Metric: the source scores uplift by the area under the uplift curve (AUUC, Sec. 4-6), which needs the treatment flag as a scoring column (MET-2); it reports no churn-classification metric, so for churn the fallback `roc_auc` (MET-8). The framing is the curator's call.
- Risks for /add-dataset: `Anonymized`: "a Principal Component Analysis (PCA) projection of the numerical features" and "All categorical features and their levels are anonymized by giving them generic names" (Sec. 3), so what a column measures and when it was known cannot be checked; the PCA was fit over all rows, a weak transductive leak (LEAK-30); the treatment flag ships as a feature or the task is cut to the control group (about 2,890 customers); about 3.5% churn (about 410 positives); the rows are only customers Orange's model rated high-risk, which matches the campaign decision but not churn scoring of the whole customer base.
- Priority: gap 0, use case 0 (the source's decision is uplift; the churn fit approximate), source + (paper, named operator, stated label window), shape + (11,896 x 178), risk - (anonymized PCA features, uplift as the original task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `churn`, `churn_telco_south_asia`, `dataset_from_feature_selection_based_dynamic_transfer_ensemble_model_for_customer_churn_prediction`, `dataset_from_research_model_of_churn_prediction_based_on_customer_segmentation_and_misclassification_cost_in_the_context_of_big_data`, `ibm_telco_customer_churn`, `iranian_churn`, `mobile_churn`.
- as published: 11,896 customers x 178 features (OpenML 45580 'churn-uplift-mlg': 180 columns with target y and the treatment flag; uploaded 2023-07-06, collection date 09-2020); response rate 3.6% control, 3.4% ...; target: churn: the customer terminates the subscription within the two months after the campaign; access: open.
- Why: Same target and use case as the telco records: an operator's subscribers, churn in a fixed window after a scoring date, from demographic, usage and subscription features known at scoring | operator churn with a fixed scoring date and a stated label window, features known at scoring: the timing iranian_churn lacked ...
- Adds: About 6x the rows of churn_telco_south_asia (2,000) and 2020 rather than 2015 data, a named operator and a stated label window (the question churn_telco_south_asia cannot settle); open, against the two Chinese telecom records whose data is private and requested (it is newer than both, but smaller than the ...
