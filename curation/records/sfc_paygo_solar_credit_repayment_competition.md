---
unique_name: sfc_paygo_solar_credit_repayment_competition
name: sfc-paygo-solar-credit-repayment-competition
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/sfc-paygo-solar-credit-repayment-competition/data
- https://zindi.africa/competitions/sfc-paygo-solar-credit-repayment-competition
source_row: 910
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a real PAYGo solar loan book (~37,000 contracts), but the task as published is the next six monthly payments of each contract from its payment history, a forecasting-like panel that has to pass TP-10.
- Source: Zindi competition "SFC PAYGo Solar Credit Repayment Competition", host Solar Frontier Capital (an impact investor financing PAYGo solar distributors), 6 June to 29 August 2021, $5,000, 1,072 participants (https://zindi.africa/competitions/sfc-paygo-solar-credit-repayment-competition, read through the Zindi API). As published: "a dataset consisting of over ~37000 PAYGo SHS contracts"; Train.csv "contains the target (next 6 months to predict)", Test.csv the same without target columns, metadata.csv "some extra features", VariablesDefinition.txt (a codebook, not read: download needs a login). The target is six monthly amounts per contract (submission rows `ID x m1` ... `ID x m6`).
- Use case: the page says "predict the next six months of payments for different customers. This will allow PAYGo distributors to provide appropriate services and customer support"; the data description frames it as credit scoring ("predicts PAYGo SHS contract repayments or defaults"). Actor: the distributor or its financier, at a cut-off date, projecting each running contract's collections (or default). Fit approximate: the shipped target is a monthly payment series, not a default label; a contract-level target (sum over six months, or fully paid vs defaulted) is a re-framing to decide at /add-dataset. Regime temporal (one cut-off date; the future months are later than all features).
- Siblings and duplicates: `sfc_paygo_solar_credit_repayment_hackathon` is the 3-day hackathon of 4-6 June 2021 on "over ~3000 PAYGo SHS contracts"; this page calls it "the hackathon which was a subset of this dataset", so the hackathon is the duplicate (proposed `No`, PROV-6) and this record is the one to keep. No other PAYGo record. External collections: none found.
- Papers and pages: no paper; no top-solution write-up found (web search). Discussions report contracts with payments above the contract value (~168) and transaction months past the cut-off in the hackathon data (threads 6401, 6924, 6994; organiser replies not readable).
- Metric: RMSE over the contract-month rows (Evaluation page: "The error metric for this competition is the Root Mean Squared Error"), a leaderboard metric, deliberate (MET-4); inputs: none beyond the target rows (MET-1).
- Risks for /add-dataset: SEL-10 / TP-10: the inputs likely include the contract's own past payments (discussions cite transaction dates and payment histories; the codebook was not read), a lag of the target series, which TP-10 leg 2 forbids; the task is in scope only if it is re-targeted at contract level or passes the naive-profile test. Join of metadata.csv to Train by ID; multi-output target (six months); payments above contract value. `problem_type` was `Binary Classification` (AI-filled); the source scores a regression (RMSE on amounts), so it is now `Regression`; a default label would be our re-framing. License: Zindi rules forbid redistribution (no criterion, EV-4).
- Priority: gap - (finance and temporal not thin), use case - (the source's actor and decision are vague, fit approximate), source + (host named, codebook shipped), shape + (~37,000 contracts, mixed contract metadata, temporal), risk - (forecasting-like target, SEL-10/TP-10).


Zindi SFC PAYGo solar credit repayment competition, predicting whether pay-as-you-go solar customers will repay/make payments, a genuine real-world tabular credit-scoring task in finance/fintech. This is a good fit with a clear repayment target and likely customer + payment-history tables, though it probably needs a temporal split and may require joining tables. A human must confirm the exact target (default vs payment amount, classification vs regression), table structure, size, split, and license; note likely overlap with the 'hackathon' variant.
