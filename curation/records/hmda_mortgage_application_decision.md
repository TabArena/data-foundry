---
unique_name: hmda_mortgage_application_decision
name: HMDA Snapshot National Loan-Level Dataset (Home Mortgage Disclosure Act loan/application register)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: finance
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://ffiec.cfpb.gov/data-publication/snapshot-national-loan-level-dataset
- https://www.consumerfinance.gov/archive/newsroom/ffiec-publishes-2023-data-on-mortgage-lending/
- https://www.consumerfinance.gov/about-us/newsroom/ffiec-publishes-2023-data-on-mortgage-lending/
- https://www.consumerfinance.gov/data-research/hmda/historic-data/
- https://www.stlouisfed.org/publications/review/2026/may/determinants-of-mortgage-denial
- https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the regulator's loan-level register of US mortgage applications, about 10 million a year with the lender's action, a strong source for an approve-or-deny task; no source names a predictive use, post-decision fields must go, and `hmda_mortgage_denial` records the same data.
- Source: the Home Mortgage Disclosure Act loan/application register, published yearly by the FFIEC and the CFPB as the Snapshot National Loan-Level Dataset (ffiec.cfpb.gov/data-publication); the expanded fields (debt-to-income and combined LTV, applicant age, AUS, credit-score model) start with the 2018 data. "The 2023 data include information on 10 million home loan applications, a decrease from the 14.3 million reported in 2022", from 5,113 reporting institutions (CFPB newsroom). As published: one row per application or purchased loan, about 99 fields (LAR data fields page): `action_taken` (1 originated, 2 approved not accepted, 3 denied, 4 withdrawn, 5 closed as incomplete, 6 purchased, 7-8 preapproval requests), loan type, purpose, amount, term, property value (rounded to $10,000), income, DTI and age in bins, race, ethnicity and sex fields, census tract with the Census Bureau's tract fields, the lender's LEI, denial reasons; no credit score (only the scoring model used). One file per year.
- Use case: none named by the source: HMDA is published to monitor lending, and the St. Louis Fed Review (May 2026) studies "over 30 million home purchase mortgage applications from 2018-2024" to explain denials, with no predictive metric. The framing would be ours (an applicant or broker estimating the odds of denial before applying, or an examiner's expected decision for a lender), so fit approximate. Regime temporal by `activity_year` (a model is fit on past years and used on new applications).
- Siblings and duplicates: `hmda_mortgage_denial` (a candidate of this run, batch screen_63, not screened yet) names the same FFIEC public LAR with the same denied-or-approved target: one of the two is a `Duplicate` (PROV-4), for the main session to settle. Other sources of a credit decision: `credit_approval` (`Yes (Disagreement)`), `japanese_credit_screening` (`No`), `loan_predication` (`TBD -> 2nd Tier`), `loan_approval_prediction_dataset` (`TBD -> 2nd Tier`), `loan_prediction_problem_dataset` (`No`), `banking_marketing_leads_conversion_data` (`TBD -> 2nd Tier`); `sleuth_ex1714` (`TBD -> 2nd Tier`, redlining by ZIP code). External collections: none of our vocabulary.
- Better data: found as better data for `banking_marketing_leads_conversion_data`, `credit_approval`, `japanese_credit_screening`, `loan_approval_prediction_dataset`, `loan_predication` and `loan_prediction_problem_dataset`, a related task next to `sleuth_ex1714`; no further search this round.
- Papers and pages: the FFIEC data-publication pages and the LAR data fields; the CFPB's yearly data releases; the St. Louis Fed Review, "Determinants of mortgage denial" (2026).
- Metric: none found (FFIEC publication pages, the CFPB newsroom, the St. Louis Fed Review: denial rates and percentage-point gaps, no prediction scored), so the fallback `roc_auc` (MET-8). Inputs none.
- Risks for /add-dataset: fields set at or after the decision: denial reasons, and the pricing fields (interest rate, rate spread, total loan costs, points and fees, origination charges, lender credits, HOEPA status) that are reported for originated or approved loans and missing for denials, plus purchaser type (LEAK; to confirm on the data); which actions form the classes (denied against originated and approved-not-accepted; withdrawn, incomplete, purchased and preapproval rows out); a sample of one year or state for size; race, ethnicity, sex and age are protected attributes, an ethics call for the curator whether they stay as features (SEL-1 is not failed by the source's words; HMDA exists to monitor them); the lender (LEI) is a strong feature and a grouping key.
- Priority: gap 0 (finance and binary not thin), use case 0 (the source names monitoring, not a prediction), source + (federal regulator, field definitions), shape + (millions of rows a year, mixed types, years for a temporal split), risk - (post-decision fields to drop, and a second record of the same data).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `banking_marketing_leads_conversion_data`, `credit_approval`, `japanese_credit_screening`, `loan_approval_prediction_dataset`, `loan_predication`, `loan_prediction_problem_dataset`; a related task next to `sleuth_ex1714`.
- as published: Mortgage applications; about 10 million applications in the 2023 snapshot from 5,113 institutions (14.3 million in 2022); dozens of columns (action taken, loan amount, income, property value, ...; target: action_taken (originated / denied), i.e. whether an application is denied; access: open.
- Why: The redlining question of sleuth_ex1714 measured on mortgages, per application rather than per ZIP: a federal source, a predictive target, millions of units each year. | same target as credit_approval (a lender's approve/deny decision on a consumer credit application) and as the leads record (approval/conversion of a ...
- Adds: Its own task in the same domain (lending access); notes for screening: race, ethnicity and sex are reported fields (a fairness and ethics point for the curator), no credit score in the public file, a sample of one year or one state would be needed. | real, named population and traceable regulator release instead of ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same HMDA data and target (`hmda_mortgage_denial`; PROV-4). The curator keeps one, or both as distinct tasks.
