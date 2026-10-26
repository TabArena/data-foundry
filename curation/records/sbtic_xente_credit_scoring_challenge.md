---
unique_name: sbtic_xente_credit_scoring_challenge
name: sbtic-xente-credit-scoring-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2019'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/sbtic-xente-credit-scoring-challenge/data
- https://zindi.africa/competitions/xente-credit-scoring-challenge
source_row: 930
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: predict whether a Xente pay-later loan defaults from the customer's e-commerce transactions and the loan's fields; a real credit decision with a chronological split, but small and with columns known only after repayment.
- Source: the Standard Bank Tech Impact Challenge: Xente Credit Scoring Challenge on Zindi (2019-08-30 at the SBTIC finals, reopened as a points challenge until 2019-12-01, 695 participants), data from Xente (Uganda). As published: "approximately 2,665 unique e-commerce transactions that occurred between 21 September 2018 and 17 July 2019. During this period, 1,631 loans were issued"; "The data have been split into a test and training set. This was done chronologically" (Train 21 Sep 2018 to 31 Mar 2019, Test 31 Mar to 17 Jul 2019); columns CustomerId, TransactionStartTime, Value, Amount, ProviderId, ProductId, ProductCategory, ChannelId, TransactionStatus, IssuedDateLoan, AmountLoan, LoanId, PaidOnDate, IsFinalPayBack, InvestorId, DueDate, PayBackId, ThirdPartyId, IsThirdPartyConfirmed, target IsDefaulted ("Exceeded agreed payback time"); a second table `unlinked_masked_final.csv` (2.4 MB) of transactions not linked to loans.
- Use case: Xente decides on a loan at application, "to refine their credit decision processes, and ... assess the creditworthiness of new and existing clients" (the page); fit direct once the post-outcome columns are dropped; regime temporal because the source split by time and a lender scores future applicants.
- Siblings and duplicates: `xente-credit-scoring-challenge` (DSN AI+ Unilorin private hackathon, 2020-11; its Zindi parent is this competition and its files have the same sizes: Train.csv 642,190, Test.csv 207,046, unlinked 2,444,377 bytes), already in this record's `source_links`; `xente_fraud_detection_challenge` and `xente_purchase_prediction_challenge` are other Xente data and tasks.
- Papers and pages: https://zindi.africa/competitions/sbtic-xente-credit-scoring-challenge.
- Metric: `roc_auc` (Zindi Evaluation: "The evaluation metric for this challenge is the Area Under the Curve (AUC)"), a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: PaidOnDate, IsFinalPayBack, PayBackId and ThirdPartyId are known only after repayment (LEAK, drop; Test.csv lacks some loan columns, per the page); rows are transactions and payback installments, while the unit is the loan (dedupe to one row per loan); the number of defaults may be small for three temporal windows (TP-5, TP-9); joining the unlinked transactions as customer history.
- Priority: gap 0, use case +, source +, shape + (borderline), risk -.

Zindi Xente credit scoring challenge, predicting loan default/repayment from financial-transaction and loan features, which is a canonical real-world tabular binary classification task in finance. Credit scoring is well-suited to the benchmark with a clear target and adequate data, though it may require a temporal split since lending data is time-ordered. A human must verify whether the original data is a single table or transactions to be aggregated/joined, the exact target definition, size, and the appropriate split regime, plus the Zindi data license.
