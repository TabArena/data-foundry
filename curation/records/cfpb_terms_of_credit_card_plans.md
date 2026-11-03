---
unique_name: cfpb_terms_of_credit_card_plans
name: Terms CC Plans
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
collections:
- STRABLE
original_source: GOV Website
year: '1990'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.consumerfinance.gov/data-research/credit-card-data/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/terms-cc-plans
- https://arxiv.org/abs/2605.12292
- https://www.consumerfinance.gov/data-research/credit-card-data/terms-credit-card-plans-survey/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the CFPB's twice-yearly survey of credit card plans since 1990, with each plan's APR as a price to predict from its terms. The data is real and documented, but the use case is a stand-in and the APR's main drivers (the index level, the credit tier) are thin in the legacy file.
- Source: CFPB, Terms of Credit Card Plans (TCCP) survey: data "first collected in 1990 as part of The Fair Credit and Charge Card Disclosure Act of 1988"; the CFPB "collects and makes public data on credit cards from over 150 issuers" every six months; redesigned in 2023 to collect "more details on the credit cards that issuers offer", such as "Purchase APR good: Median APR at origination for consumers with credit scores from 620-719" (data dictionary). The waves from 1990 to June 2022 are on data.consumerfinance.gov, the later ones are xlsx files (https://www.consumerfinance.gov/data-research/credit-card-data/terms-credit-card-plans-survey/). As published in STRABLE ('TCCP Surveys.csv'; parquet previewed 2026-10-31): 9,486 rows x 12 columns, one plan per issuer and survey date, 64 survey dates from 1990 to 2022; target `APR` (0.14 to 36, mean 14.8); inputs survey date, institution, plan name, availability, location, index (V/F), variable rate index, grace period, annual fee, late fee (74% missing), consumer telephone number.
- Use case: an issuer setting a new plan's APR against the market, or a comparison service or regulator flagging plans priced high for their terms; the source publishes the survey for transparency and names no prediction. Fit approximate; regime temporal (survey waves; the APR level follows the prime rate).
- Siblings and duplicates: `cfpb_college_credit_card_agreements`, `cfpb_college_banking_agreements`, `cfpb_prepaid_product_agreements`, `consumer_complaints` (CFPB): same publisher, other data; precedent for a product's price from its attributes: `wine_world_cost` (`Yes`). External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2), "Terms CC Plans": "Terms and conditions for various credit card plans. The task is to predict interest rates."
- Better data: a candidate of the benchmark STRABLE; no further search this round. The source's own waves since 2023 (redesigned survey, APR by credit tier) are a later version of the same source: see the risks.
- Papers and pages: the TCCP page and data dictionary; STRABLE and `preprocess_consumer-financial-protection-bureau-terms-cc-plans.py`; papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (a survey, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` (MET-8); inputs none.
- Risks for /add-dataset: a variable APR is the index rate at the survey date plus a margin the file does not hold, so a temporal split meets new rate levels (SPLIT-6), and whether to add the prime rate at the survey date (external data) is a call; the 2023+ waves are a version with credit-tier APRs and more fields (PROV-6: which one enters); `Telephone Number for Consumers` and `Plan Name` (a PDF file name) are near-ids; institutions repeat across waves.
- Priority: gap 0 (finance, regression and temporal not thin), use case 0 (a stand-in), source + (CFPB survey since 1990 with a data dictionary), shape + (9,486 plan-waves over 32 years, mixed), risk - (the APR's drivers missing from the legacy file; a redesigned version to choose).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 9,486 rows x 12 columns incl. target (STRABLE parquet); target: APR.
- Why: Predict the APR of a credit card plan from its terms
- Notes: Raw file 'TCCP Surveys.csv' (CFPB Terms of Credit Card Plans survey).
