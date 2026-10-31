---
unique_name: cfpb_college_credit_card_agreements
name: College Credit Card Marketing
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: finance
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.consumerfinance.gov/data-research/student-banking/marketing-agreements-and-data/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/college-creditcard-marketing
- https://arxiv.org/abs/2605.12292
- https://files.consumerfinance.gov/f/documents/cfpb_college-credit-card-data-release_2009-2024.csv
- https://files.consumerfinance.gov/f/documents/cfpb_college-credit-card-data-guide_2025-12.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the CFPB's yearly reports of card issuers' marketing agreements with colleges, 2009-2024, a documented collection. The target (payments to the college) is reported in the same year as the open and new accounts that drive it, and no decision is named.
- Source: CFPB, college credit card agreements: under the CARD Act of 2009 "the CFPB collects information each year from card issuers that have agreements with colleges or affiliated organizations such as alumni associations, sororities, fraternities, and foundations" (consumerfinance.gov, college credit card pages); combined file cfpb_college-credit-card-data-release_2009-2024.csv with a data guide (December 2025; its text could not be extracted here) and yearly agreement PDFs; "2019 marketing agreements may include omissions due to the Bureau's COVID-19 regulatory flexibility statement". As published in STRABLE: 6,283 rows x 13 columns, one row per agreement and reporting year (1,045 rows in 2009 falling to 131 in 2024), 2,098 institution-issuer pairs; target `PAYMENTS_BY_ISSUER` on a log scale, 15.5% zeros. The STRABLE paper says the task is "to predict the number of open accounts"; its config predicts the payments.
- Use case: none named; a college or alumni association negotiating an affinity-card agreement estimating what the issuer will pay would be a stand-in. Fit approximate; regime grouped by agreement or temporal by reporting year.
- Siblings and duplicates: `cfpb_college_banking_agreements` (campus deposit accounts, a CFPB compilation), `cfpb_prepaid_product_agreements`, `cfpb_terms_of_credit_card_plans`, `consumer_complaints` (CFPB, `Yes`): same publisher, other data. External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2), "College Credit Card Marketing": "Marketing agreements between credit card issuers and universities. The task is to predict the number of open accounts."
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the CFPB's yearly college credit card reports to Congress (not read); STRABLE and `preprocess_consumer-financial-protection-bureau-college-creditcard-marketing.py`; papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the CFPB publishes reports, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` with the transform the target needs (MET-3, MET-8); inputs none.
- Risks for /add-dataset: `TOTAL_OPEN_ACCOUNTS_AS_OF_END_OF_REPORTING_YEAR` and `NEW_ACCOUNTS_OPENED_IN_REPORTING_YEAR` are results of the same year as the payments (Spearman 0.73 between open accounts and the target in the preview), so they fit only a look back (LEAK-10, USE-3); which of payments and open accounts is the target (USE-5); the same agreement repeats yearly (grouped or temporal split); the payments follow from contract terms that are only in the PDFs (heavy wrangling to use them); a byte-order mark in the first column's name.
- Priority: gap 0 (finance, regression not thin), use case 0, source + (CFPB, a collection by law with a data guide), shape + (6,283 agreement-years over 16 years, a panel), risk - (same-year outcome columns, the target disputed between paper and config).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 6,283 rows x 13 columns incl. target (STRABLE parquet); target: PAYMENTS_BY_ISSUER.
- Why: Predict the payments a card issuer makes to a college under a credit card marketing agreement
- Notes: Raw file cfpb_college-credit-card-data-release_2009-2024.csv. Paper says 'number of open accounts'; config target is PAYMENTS_BY_ISSUER.
