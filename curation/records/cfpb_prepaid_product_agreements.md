---
unique_name: cfpb_prepaid_product_agreements
name: Prepaid Financial Product
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
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.consumerfinance.gov/data-research/prepaid-accounts/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/prepaid-financial-product
- https://arxiv.org/abs/2605.12292
- https://www.consumerfinance.gov/data-research/prepaid-accounts/download-agreements/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the CFPB's register of prepaid account agreements. STRABLE's target is whether an agreement was withdrawn by the download date, a status no named actor predicts, read over a window shared by all rows.
- Source: CFPB, Prepaid Account Agreements: "The Prepaid Rule requires prepaid account issuers to submit their prepaid account agreements to the CFPB", also when "a previously submitted agreement is no longer offered" (https://www.consumerfinance.gov/data-research/prepaid-accounts/); the download holds "all prepaid product agreement files and their supporting metadata". As published in STRABLE (prepaid_metadata_recent_agreements.csv; parquet previewed 2026-10-31): 3,336 rows x 13 columns, one agreement per row, submitted (`created_date`) 2019-2024 with effective dates back to 2013; target `current_status`, Active 2,639 and Withdrawn 697; STRABLE dropped `withdrawal_date` as a leak. The STRABLE paper's text says "The task is to predict fee structures"; its config predicts the status.
- Use case: none named; who acts on a prediction that an issuer stops offering a prepaid product is unclear (USE-1). Fit none as published; regime temporal by submission date.
- Siblings and duplicates: `cfpb_college_banking_agreements`, `cfpb_college_credit_card_agreements`, `cfpb_terms_of_credit_card_plans`, `consumer_complaints` (CFPB, `Yes`): same publisher, other data. External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2), "Prepaid Financial Product": "Information on prepaid financial products and terms. The task is to predict fee structures."
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the CFPB pages above; STRABLE and `preprocess_consumer-financial-protection-bureau-Prepaid-Financial-Product.py`; papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (a register, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (App. D.1), a benchmark's habit, not the source's. So the fallback, `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: the status is read at the download date, a window all rows share (SEL-6): Withdrawn is 22% of the 2019 submissions (344 of 1,586) and 2% of the 2024 ones (9 of 466); the raw metadata's `withdrawal_date` would allow a fixed horizon after submission; `path` and `direct_download` repeat issuer, product and date; `product_id` and `agreement_id` are ids; the fee schedules the paper names sit in the agreement PDFs (heavy wrangling).
- Priority: gap 0 (finance, binary not thin), use case 0, source + (CFPB, a register required by the Prepaid Rule), shape + (3,336 agreements, mixed, dated), risk - (a status over a shared window with no decision named).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 3,336 rows x 13 columns incl. target (STRABLE parquet); target: current_status.
- Why: Predict the current status of a prepaid account agreement
- Notes: Raw file prepaid_metadata_recent_agreements.csv (CFPB). Paper says 'fee structures'; config target is current_status (binary).
