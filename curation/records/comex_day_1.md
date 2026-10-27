---
unique_name: comex_day_1
name: comex-day-1
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: finance
required_split:
- '?'
problem_type: TBD
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/comex-day-1
source_row: 977
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): "COMEX Vehicle Insurance Claim Challenge", a one-day private Zindi re-run of `autoinland_vehicle_insurance_claim_challenge` on the same AutoInland policies.
- Source: Zindi competition `comex-day-1` (read through the Zindi API; the web page refused the connection): title "COMEX Vehicle Insurance Claim Challenge", 22 May 2023, 09:30 to 18:30, Oman, "This challenge is COMEX participants", 3 participants; restricted, secret code required. Its description, data description and files (Train.csv, Test.csv, VariableDefinitions.csv, NigerianStateNames.csv, starter notebooks) are word for word those of the AutoInland Vehicle Insurance Claim Challenge (Zindi, 2021-03-26): "The data describes ~12,000 policies sold by AutoInland for car insurance"; target: "if a customer will submit a claim within 3 months from their first transaction"; metric F1 in both.
- Siblings and duplicates: `autoinland_vehicle_insurance_claim_challenge` (AI `TBD -> Yes`, which already lists four other re-runs: the-smart-cube-hackathon, women-in-data-2022, indabax-ghana-autoinland-vehicle-insurance-claim, vehicle-insurance-claim-hackathon) is the first publication; add the comex-day-1 link there. `axa_vehicle_insurance_claim_challenge` (UmojaHack Nigeria) may be the same data again; check it when AutoInland is added.
- The old markers `Missing source information` and `TBD` go: the source is AutoInland via Zindi, and the record's domain (finance) would be insurance.
- Reject check (AI, 2026-10-22): stands. Zindi API (api.zindi.world/v1/competitions/comex-day-1): 'COMEX Vehicle Insurance Claim Challenge', 22 May 2023, 3 participants, 'This challenge is COMEX participants.'; Data Description 'The data describes ~12,000 policies sold by AutoInland for car insurance', same file list (incl. NigerianStateNames.csv) and error_metric f1 as autoinland-vehicle-insurance-claim-challenge (2021). Same source, same task (PROV-4); keep autoinland_vehicle_insurance_claim_challenge (TBD -> Yes).

Zindi 'comex-day-1' competition with no comments or description in the record, so there is too little information to judge confidently. The name suggests a COMEX commodity-exchange financial dataset, which would raise a real risk that the task is price prediction/forecasting (out of scope) rather than a fixed IID tabular classification/regression. Per guidance I do not reject solely for sparse info, but the likely financial-price framing keeps it below first tier. A human must read the Zindi competition page to determine the actual target, whether it is forecasting versus a fixed task, the feature types, and the data size.
