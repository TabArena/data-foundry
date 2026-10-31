---
unique_name: cfpb_college_banking_agreements
name: College Deposit Product Marketing
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
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
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/college-deposit-product-marketing
- https://arxiv.org/abs/2605.12292
- '# the file itself; the student-banking page above covers the credit-card agreements only'
- https://files.consumerfinance.gov/f/documents/cfpb_college-banking-database_2020-2023.csv
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a CFPB compilation of colleges' disclosures on campus bank-account deals. The active-account count sits beside same-year costs and payments, and the source names no actor or decision.
- Source: CFPB, cfpb_college-banking-database_2020-2023.csv (https://files.consumerfinance.gov/f/documents/cfpb_college-banking-database_2020-2023.csv, header read 2026-10-31). The page STRABLE links (consumerfinance.gov, student banking, marketing agreements and data) covers only credit cards, and no CFPB landing page or codebook for this file was found (the guessed deposit-agreements page returns 404). The columns (award year, institution, issuer, total active accounts, annual mean and median account costs incurred, monetary consideration both ways, school type, OPEID, enrollment, MSI type, the cash-management disclosure, account-terms and agreement URLs, the date the CFPB accessed them) look like the disclosures the U.S. Department of Education's cash-management rules ask of institutions with Tier One or Tier Two arrangements; that is a reading, to verify. As published in STRABLE: 1,359 rows x 18 columns, 497 institutions over award years 2020-21 to 2022-23 (the year spelled two ways); target `TOTAL_ACTIVE_ACCOUNTS_` on a log scale.
- Use case: none named; a bank bidding for a campus arrangement, or a college comparing offers, estimating account uptake would be a stand-in. Fit approximate at best; regime grouped by institution (about three award years each) or temporal by award year.
- Siblings and duplicates: `cfpb_college_credit_card_agreements` (the credit-card side, CARD Act reports), `cfpb_prepaid_product_agreements` and `cfpb_terms_of_credit_card_plans` (same publisher, other data); `consumer_complaints` (CFPB, `Yes`). External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2), "College Deposit Product Marketing": "Agreements regarding deposit products offered to college students. The task is to predict associated financial metrics."
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE and `preprocess_consumer-financial-protection-bureau-college-deposit-product-marketing.py`; the CFPB's reports on college banking not found; papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (no codebook or task from the CFPB); STRABLE scores R2 for regression and AUROC for classification over all its tables (App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` with a log1p transform (MET-3, MET-8); inputs none.
- Risks for /add-dataset: the costs incurred by account holders and the consideration paid are results of the same accounts in the same award year (LEAK-10, USE-3): keep only what is known when the contract is signed; the three URL columns and the CFPB's access date are no features; institutions repeat across years (grouped split); the file's documentation is unread (PROV-2).
- Priority: gap 0 (finance, regression not thin), use case 0, source 0 (a CFPB file without a codebook found), shape 0 (1,359 rows of 497 institutions, about ten real inputs), risk - (same-year outcome columns, no decision named).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,359 rows x 18 columns incl. target (STRABLE parquet); target: TOTAL_ACTIVE_ACCOUNTS_.
- Why: Predict the number of active accounts under a college deposit-product marketing agreement
- Notes: Raw file cfpb_college-banking-database_2020-2023.csv.
