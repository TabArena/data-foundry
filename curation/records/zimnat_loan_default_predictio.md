---
unique_name: zimnat_loan_default_predictio
name: Zimnat Loan Default Predictio
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2020'
domain: finance
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/umojahack-zimbabwe/data
- https://zindi.africa/competitions/umojahack-zimbabwe
source_row: 1018
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 1: a real lender's loan table with an overdue flag; in scope, but the flag is a status at an unknown snapshot over loans already running, so the prediction point needs work.
- Source: Zindi private hackathon "UmojaHack Zimbabwe: Zimnat Loan Default Prediction", 2020-10-17 (https://zindi.africa/competitions/umojahack-zimbabwe, read through Zindi's page API); as published: "a sample dataset of over 12,000 loans, many of them with money overdue"; "Each row in the dataset corresponds to a loan ... information about the loan (starting dates, maturity date, amount, interest rate etc) as well as some information on the customer"; target `Target`, "1 indicates that the loan has an unpaid payment due, a 0 indicates that all is well"; Train.csv, Test.csv, VariableDescription.csv. Rows and columns not counted (login).
- Use case: "Your challenge is to predict which loans will end in a missed payment" so the lender can "manage that risk"; fit approximate (no decision moment named; if the loans are scored at origination, the columns must be the application fields only); regime temporal by start date (to confirm from the columns).
- Siblings and duplicates: no other record of this data (grep zimnat: `zimnat_insurance_recommendation_challenge` and `the_zimnat_insurance_assurance_challenge` are other Zimnat tasks); other default records (`loan_default_prediction_challenge`, `african_credit_scoring_challenge`) are other lenders. External collections: none found.
- Papers and pages: the competition page; no paper.
- Metric: ROC AUC ("The evaluation metric for this competition is the Area Under the ROC curve (AUC) ... This will allow the clients to set thresholds to their own needs", Evaluation tab): a deliberate leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the overdue status is measured at one unstated date while loans have different ages and maturities, so loan age drives the label (SEL-6 to weigh, USE); columns set after origination (balance, days overdue, payments) would leak (LEAK); confirm the start dates for a temporal split.
- Priority: gap 0 (finance, binary not thin), use case 0 (no decision moment), source 0 (a hackathon page; the variable file not read), shape + (12,000 loans, dates and amounts), risk - (snapshot label, possible post-origination columns).

Zimnat loan default prediction (UmojaHack Zimbabwe, Zindi) asks to predict which customers will default on a loan, a clean binary classification with a clear target and standard credit/customer tabular features. This is a representative real-world finance task. As a UmojaHack/hackathon dataset it may be modest in size and could carry imbalance. A human must verify row count after cleaning, the exact target and feature set, and the appropriate split; provisionally Yes.

---

Predict which customers will default on a loan
