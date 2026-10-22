---
unique_name: indabax_mali_2023
name: indabax-mali-2023
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
- https://zindi.africa/competitions/indabax-mali-2023/data
source_row: 981
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4, PROV-5): a private re-run of the STEG electricity and gas fraud challenge with the same files; duplicate of `fraud_detection_in_electricity_and_gas_consumption`.
- Source: Zindi, IndabaX Mali 2023 (2023-07-15 to 2023-07-17, RobotsMali and GDSC ENI-ABT, 12 participants). As published: "Les données fournies par STEG consistent en deux fichiers" (Client_train / Invoice_train, Client_test / Invoice_test), target fraud 1 / 0 per client; files train.zip 64,178,074 B, test.zip 27,696,276 B, SampleSubmission.csv 2,153,008 B.
- Use case: STEG flags clients for meter-fraud inspection; regime grouped by client in the canonical record.
- Siblings and duplicates: `fraud_detection_in_electricity_and_gas_consumption` (`Yes`, WIP (DF), Lennart; lists seven Zindi re-runs); `indabax_drc_2022` (Lennart, 2026-10-12: No, `Duplicate`, "the same STEG files (train.zip 61.2 MB, test.zip 26.4 MB, SampleSubmission.csv 2.1 MB)"); 64,178,074 B = 61.2 MiB and 27,696,276 B = 26.4 MiB. Same files as `indabax_nigeria_23`.
- Metric: AUC (Zindi Evaluation page: "l'erreur Area Under the Curve").
- Note for the canonical record: add this link to its re-run list.
- Reject check (AI, 2026-10-22): stands. Zindi API: train.zip 64,178,074 B, test.zip 27,696,276 B and SampleSubmission.csv 2,153,008 B, byte for byte the files of fraud-detection-in-electricity-and-gas-consumption-challenge and indabax-drc-2022 (curator No, Duplicate, 2026-10-12); the page says 'Les données fournies par STEG consistent en deux fichiers'. https://zindi.africa/competitions/indabax-mali-2023

IndabaX Mali 2023 is a Zindi educational hackathon with no comments or task description in the record, so the target, modality, and size are unknown. Most IndabaX hackathons are real-world tabular classification/regression tasks, so it should not be rejected on missing info alone. A human must open the Zindi page to determine the actual prediction task, modality (rule out image/text), size after cleaning, and split regime before a final verdict.
