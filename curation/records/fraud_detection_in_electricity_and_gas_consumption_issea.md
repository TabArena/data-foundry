---
unique_name: fraud_detection_in_electricity_and_gas_consumption_issea
name: fraud-detection-in-electricity-and-gas-consumption-issea
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- Review Prio 1 (Atlas)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2020'
domain: industry & manufacturing
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/fraud-detection-in-electricity-and-gas-consumption-issea/data
source_row: 988
type_adapter_id: curation-record-v1
---

# fraud-detection-in-electricity-and-gas-consumption-issea

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

STEG (Société Tunisienne de l'Électricité et du Gaz) electricity & gas consumption fraud detection (Zindi / ISSEA). Real utility billing data: a client table plus an invoice/consumption-history table (~4.5M invoice rows over ~135K clients) to be joined; the target (fraud) is one binary label per client, so the natural split is grouped by client. Invoices carry dates, so a temporal element exists too — worth checking whether a temporal or grouped split better mirrors the real task. Real, sizeable, clear predictive task → looks worth pursuing for the 1M–10M-row benchmark, pending a data inspection.
