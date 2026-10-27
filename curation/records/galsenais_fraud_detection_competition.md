---
unique_name: galsenais_fraud_detection_competition
name: galsenais-fraud-detection-competition
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
source_links:
- https://zindi.africa/competitions/galsenais-fraud-detection-competition/data
source_row: 942
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a 2025 re-run of the Xente Fraud Detection Challenge on the same Xente transaction sample, recorded as `xente_fraud_detection_challenge`.
- Source: Zindi hackathon "GalsenAI's Fraud Detection Competition" (GalsenAI and AI Hub Senegal, 2025-03-19 to 2025-04-27, secret code); the Zindi API lists as its parent the 2020 "Xente Fraud Dection Hackathon", itself a re-run of the 2019 "Xente Fraud Detection Challenge".
- Deciding words: the data page repeats the 2019 challenge word for word: "Xente is an e-commerce and financial service app serving 10,000+ customers in Uganda. This dataset includes a sample of approximately 140,000 transactions that occurred between 15 November 2018 and 15 March 2019", with the same files (training.csv "Transactions from 15 November 2018 to 13 February 2019", test.csv "from 13 February 2019 to 14 March 2019", Xente_Variable_Definitions.csv) and the same subtitle "Accurately classify the fraudulent transactions from Xente's e-commerce platform" (https://zindi.africa/competitions/galsenais-fraud-detection-competition, https://zindi.africa/competitions/xente-fraud-detection-challenge).
- Canonical: `xente_fraud_detection_challenge` (`TBD -> Yes`, its `source_links` already list the 2020 hackathon and other re-runs); this link can be added there.
- Metric: F1 (the same as the 2019 challenge).
- Reject check (AI, 2026-10-22): stands. PROV-4/PROV-5 (Must), source confirmed. Zindi API: parent = xente-fraud-dection-hackathon (the 2020 re-run of the 2019 xente-fraud-detection-challenge). The data page repeats "a sample of approximately 140,000 transactions that occurred between 15 November 2018 and 15 March 2019". The file list and file descriptions are identical (training.csv "Transactions from 15 November 2018 to 13 February 2019", test.csv "from 13 February 2019 to 14 March 2019", Xente_Variable_Definitions.csv). It is the same fraud task with the same metric, so not distinct under PROV-7. Canonical: xente_fraud_detection_challenge (TBD -> Yes); add this link to its source_links. https://zindi.africa/competitions/galsenais-fraud-detection-competition

Zindi fraud-detection competition with no comments in the record. Fraud detection is a classic, highly representative tabular binary-classification task with a clear target (fraud vs. legitimate), so it is a plausible Yes. Unknowns include dataset size, whether a temporal/grouped split is required (transaction data often is), and whether the data is real or synthetically generated for the competition. A human should verify the target, the split regime, and data provenance before finalizing.
