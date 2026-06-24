---
unique_name: sfc_paygo_solar_credit_repayment_competition
name: sfc-paygo-solar-credit-repayment-competition
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/sfc-paygo-solar-credit-repayment-competition/data
source_row: 910
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi SFC PAYGo solar credit repayment competition, predicting whether pay-as-you-go solar customers will repay/make payments, a genuine real-world tabular credit-scoring task in finance/fintech. This is a good fit with a clear repayment target and likely customer + payment-history tables, though it probably needs a temporal split and may require joining tables. A human must confirm the exact target (default vs payment amount, classification vs regression), table structure, size, split, and license; note likely overlap with the 'hackathon' variant.
