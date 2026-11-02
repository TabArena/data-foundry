---
unique_name: indabax_nigeria_23
name: indabax-nigeria-23
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
year: '2023'
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/indabax-nigeria-23/data
source_row: 980
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4, PROV-5): IndabaX Nigeria 2023 re-runs the STEG electricity and gas fraud challenge with the same files; duplicate of `fraud_detection_in_electricity_and_gas_consumption`.
- Source: Zindi, "An application of a classification problem - Fraud Detection" (2023-06-01 to 2023-06-10, IndabaX Nigeria with Thomas Adewumi University, 67 participants). As published: "The data provided by STEG is composed of two files" (client data and billing history since 2005), target fraud 1 / 0; files train.zip 64,178,074 B, test.zip 27,696,276 B, SampleSubmission.csv 2,153,008 B.
- Use case: STEG flags clients for meter-fraud inspection.
- Siblings and duplicates: `fraud_detection_in_electricity_and_gas_consumption` (`Yes`, Lennart); `indabax_drc_2022` (Lennart, 2026-10-12: No, `Duplicate` on the same file sizes, 61.2 MB / 26.4 MB / 2.1 MB); same files as `indabax_mali_2023`.
- Metric: AUC (Zindi Evaluation page: "The metric used for this challenge is AUC").
- Note for the canonical record: add this link to its re-run list.
- Reject check (AI, 2026-10-22): stands. Zindi API: the same three STEG files byte for byte (64,178,074 / 27,696,276 / 2,153,008 B) as the canonical STEG challenge and the indabax_drc_2022 precedent (curator No, Duplicate); 'The data provided by STEG is composed of two files'. https://zindi.africa/competitions/indabax-nigeria-23

IndabaX Nigeria 2023 is a Zindi hackathon with no task description in the record; target, modality, and size are unknown. IndabaX hackathons are commonly genuine tabular prediction tasks, so missing info alone is not grounds to reject. A human must inspect the Zindi page for the actual target, confirm it is tabular (not image/text/NLP), and check size and split regime.
