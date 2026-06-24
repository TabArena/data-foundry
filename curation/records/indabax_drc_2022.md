---
unique_name: indabax_drc_2022
name: indabax-drc-2022
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/indabax-drc-2022
- https://zindi.africa/competitions/instadeep-fraud-detection-in-electricity-and-gas-consumption-challenge
- https://zindi.africa/competitions/indabax-cameroon-2021-2
source_row: 997
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

IndabaX DRC 2022 reuses the well-known STEG fraud-detection task (fraud in electricity and gas consumption), a real-world binary classification on client + billing/invoice tabular records. It is a legitimate predictive tabular task, but the original data is typically split across a client table and an invoice/transaction table that must be aggregated/joined, so wrangling is required. The fraud-detection STEG data is a known reused source, so duplication versus the original Zindi fraud challenge should be checked. A human must verify the join/aggregation, final size, label balance, and whether it duplicates the InstaDeep/STEG fraud dataset.

---

Fraud Detection in Electricity and Gas Consumption
