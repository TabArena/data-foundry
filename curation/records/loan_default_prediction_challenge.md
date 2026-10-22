---
unique_name: loan_default_prediction_challenge
name: loan-default-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2018'
domain: finance
required_split:
- '?'
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/loan-default-prediction-challenge/data
- https://zindi.africa/competitions/data-science-nigeria-challenge-1-loan-default-prediction
source_row: 898
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: SuperLender's repeat-loan default at application, a direct credit decision; the record's link is a 2022 rerun of Data Science Nigeria's Challenge 1.
- Source: SuperLender data first released in Zindi's "Data Science Nigeria Challenge #1: Loan Default Prediction" (start 2018-10-11, https://zindi.africa/competitions/data-science-nigeria-challenge-1-loan-default-prediction); the record's link is the AfroPavo Analytics internship rerun (2022-03-15 to 2022-04-16), whose API names the DSN challenge as its parent. As published: three tables per split, `traindemographics.csv`, `trainperf.csv` (the repeat loan to score, target `good_bad_flag`, "good = settled loan on time; bad = did not settled loan on time"), `trainprevloans.csv` (the customer's earlier loans), joined on `customerid`. Rows not checked (Zindi data needs a login).
- Use case: "These two fundamental drivers need to be determined at the point of each application to allow the credit grantor to make a calculated decision ... if an applicant should get a loan, and if so - what the size, price and tenure of the offer will be" (description page); fit direct; regime temporal (`approveddate`, `creationdate` ship; one repeat loan per customer, so grouping adds nothing).
- Siblings and duplicates: no other record of the SuperLender data (grep: superlender, data science nigeria); other credit-default records (zimnat_loan_default_predictio, african_credit_scoring_challenge, lt_vehicle_loan_default_prediction) are other lenders. External collections: none found.
- Papers and pages: the two competition pages; no paper.
- Metric: error rate, "the percentage of loans you predict incorrectly" (Evaluation page of both competitions), the leaderboard metric (MET-4); hard labels at 0.5 with no costs stated, so a candidate for overruling under MET-4 and MET-6 once probed; inputs none.
- Risks for /add-dataset: `trainprevloans` holds `closeddate` and `firstrepaiddate`, known only for loans closed before the application date: filter by date (LEAK); `totaldue` and `termdays` are offer terms set with the decision (USE); aggregation of previous loans (joins); exact birthdate and GPS coordinates to coarsen (personal data).
- Priority: gap - (finance, binary, temporal not thin), use case + (actor and decision named), source + (the page documents every column), shape + (mixed types and dates; the row count not checked), risk - (three tables to join, post-application dates).

A Zindi loan-default competition where the task is predicting whether a loan was good or bad, a classic real-world tabular binary classification problem in credit risk. This maps well to the benchmark criteria: genuine predictive task, clear target, finance domain. The record lacks size and split details, so it cannot be confirmed Yes outright. A human must verify dataset size after cleaning, the exact target definition, absence of leakage, and whether a temporal/grouped split (by applicant or time) is warranted, but it is a plausible Yes.

---

Predict if a loan was good or bad
