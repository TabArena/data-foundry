---
unique_name: dlix_botswana
name: dlix-botswana
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
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/dlix-botswana/data
source_row: 947
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a re-run of the Income Prediction Challenge for Azubian, which `income_prediction_challenge_for_azubian` already records.
- Source: Zindi "DLIx Botswana Challenge" (Deep Learning IndabaX Botswana 2025), from 31 July 2025 (https://zindi.africa/competitions/dlix-botswana); the Zindi API names its parent `income-prediction-challenge-for-azubian` (7 November 2022), and both ship the same files (Train.csv 68,209,849 bytes, Test.csv 28,207,389, VariableDefinitions.csv 1,674, SampleSubmission.csv 1,257,026) and the same text ("~200 000 individuals in train and ~100 000 individuals in the test file", "predict if an individual earns above 50 000 of a specific currency").
- Siblings and duplicates: `income_prediction_challenge_for_azubian` (TBD -> Yes, AI unverified; links the Azubian page and umojahack-india-2022) carries this dataset; it is the record to screen. Whether that data is itself a re-upload of a census extract is its question, not this record's.
- Metric: F1 (Zindi), the same as the parent.
- Previous markers `TBD` and `Missing source information` replaced by `Duplicate`.
- Reject check (AI, 2026-10-22): stands. Zindi API (api.zindi.world/v1/competitions/dlix-botswana) names parent income-prediction-challenge-for-azubian; Train.csv 68,209,849 and Test.csv 28,207,389 bytes are identical to the parent's; income_prediction_challenge_for_azubian carries it (its own parent is umojahack-india-2022, for that record's year). PROV-4/PROV-5.

Zindi 'dlix-botswana' competition with no description or metadata in the record; task, target, domain, data modality, and size are all unknown. The 'DLIX' (Deep Learning IndabaX) naming raises the possibility of a non-tabular image/text task, but that is unconfirmed. Too little information to decide, and that alone is not grounds for rejection. A human must inspect the competition to establish modality, task, target, size, and split.
