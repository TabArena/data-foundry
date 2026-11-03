---
unique_name: springleaf_marketing_response
name: Springleaf Marketing Response
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
- Many features
original_source: Kaggle
year: '2015'
domain: business & marketing
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/springleaf-marketing-response
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a 2015 Kaggle competition of the consumer lender Springleaf, one row per customer with about 1,930 anonymized columns and the response to a direct-mail offer as the target, scored by ROC AUC; the company names the decision, but what the columns measure cannot be checked.
- Source: Kaggle competition "Springleaf Marketing Response" by Springleaf (Featured, enabled 2015-08-14, deadline 2015-10-19, 2,221 teams; Kaggle API). As published (Data page): "a high-dimensional dataset of anonymized customer information. Each row corresponds to one customer. The response variable is binary and labeled "target""; "The features have been anonymized to protect privacy and are comprised of a mix of continuous and categorical features", with "placeholder" values for cases such as missing values kept "to match with internal systems at Springleaf". Files: `train.csv.zip` 157 MB, `test.csv.zip` 157 MB (no labels), `sample_submission.csv.zip`; about 145,000 training rows and about 1,930 columns as participants report, not counted here.
- Use case: Springleaf's marketing team decides whom to send a direct-mail loan offer: "Determine whether to send a direct mail piece to a customer" (Kaggle API description); "Springleaf must be sure they are focusing on the customers who are likely to respond and be good candidates for their services" (Description); fit direct. Regime IID unless a mailing or account date among the columns orders the rows (then temporal, SPLIT-7); not checked.
- Siblings and duplicates: `pva_revenue_prediction_kddcup98` (`Yes`, shipped; KDD Cup 98 donors' response to a charity mailing, scored by a stand-in `roc_auc`): the same kind of task from another source and decade, no duplicate (PROV-4). No other Springleaf record. External collections: none found (searched only this repository; the session's web search budget was used up).
- Better data: found as better data for `pva_revenue_prediction_kddcup98`; no further search this round.
- Papers and pages: the competition's Description, Evaluation and Data pages (read through the Kaggle API); the example script "xgboost-example" linked from the Data page.
- Metric: "Submissions are evaluated on area under the ROC curve between the predicted probability and the observed target" (Evaluation page): `roc_auc`, the leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the columns are anonymized (`Anonymized`): what each one measures, whether it is known before the mailing, and whether a field records the response cannot be checked (LEAK-32, LEAK-38); placeholder codes for missing values can only be decoded by pattern; only the training file has labels; the row order and any date-like columns decide the regime; Kaggle's competition rules (registration) are a note, not a criterion (EV-4).
- Priority: gap 0 (business & marketing and binary are not thin), use case + (the company names the mailing decision), source 0 (a competition page that does not document the columns), shape + (about 145,000 customers, wide and mixed), risk - (anonymized features, leaks that cannot be ruled out).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `pva_revenue_prediction_kddcup98`.
- as published: customers, one row each; train.csv.zip 157 MB and test.csv.zip 157 MB (Kaggle file listing); about 145,000 training rows x about 1,930 anonymized columns as reported by participants (verify at ...; target: binary: whether the customer responds to the direct-mail offer; access: registration.
- Why: the same task as KDD Cup 98 (response to a direct-mail solicitation, one row per customer from the customer file, binary response, AUC as our stand-in metric there)
- Adds: 17 years newer and about 1.5x the rows of the KDD98 learning file (95,412); a commercial lender instead of a charity. Caveats: columns anonymized (Anonymized marker), no column descriptions; Kaggle competition rules (registration)
