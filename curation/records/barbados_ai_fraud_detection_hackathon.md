---
unique_name: barbados_ai_fraud_detection_hackathon
name: barbados-ai-fraud-detection-hackathon
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
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/barbados-ai-fraud-detection-hackathon/data
source_row: 943
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a re-run of the Xente fraud data, recorded as `xente_fraud_detection_challenge`.
- Source: Zindi, "Barbados AI Fraud Detection Hackathon", one day, 2025-05-10; the Zindi API gives its `parent` as `xente-fraud-dection-hackathon` (2020), itself a copy of the Xente Fraud Detection Challenge (2019-05-20, Uganda, ~140,000 transactions), which `xente_fraud_detection_challenge` lists in its `source_links`.
- As published: "anonymized transaction data", "a sample of approximately 140,000 transactions that occurred between 15 November 2018 and 15 March 2019": the same sentence, size and dates as the Xente Data Description; the Barbados framing is new, the data is not (PROV-5: confirmed by the parent link and the identical description).
- Siblings and duplicates: `xente_fraud_detection_challenge` (AI `TBD -> Yes`, unverified) carries the task; its first publication is the 2019 Xente challenge (PROV-8).
- Metric: F1 (Zindi Evaluation page), the same as Xente's.
- Reject check (AI, 2026-10-22): stands. Zindi API: parent = xente-fraud-dection-hackathon, whose parent is xente-fraud-detection-challenge (2019). The files are byte-identical in size: Train 17,071,505 / Test 7,951,537 / SampleSubmission 1,045,033 bytes in both; Variable_Definitions 977 in both. The Data Description has the same '140,000 transactions ... 15 November 2018 and 15 March 2019' sentence. The task is kept in xente_fraud_detection_challenge (PROV-4, PROV-8).

Zindi Barbados AI fraud-detection hackathon with no comments in the record, but the name strongly implies a transaction/fraud binary classification task, which is a representative real-world tabular ML problem. Fraud datasets typically have a clear binary target and tabular transaction features. The lack of detail means this is provisional. A human must open the Zindi page to confirm the target, feature modality, cleaned size, class imbalance, and the appropriate (likely temporal) split.
