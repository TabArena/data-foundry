---
unique_name: indabax_tanzania_mobile_banking_prediction_challenge
name: indabax-tanzania-mobile-banking-prediction-challenge
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
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/indabax-tanzania-mobile-banking-prediction-challenge
source_row: 1000
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a private IndabaX Tanzania 2021 hackathon (21 to 23 June 2021) re-running the iX Mobile Banking Prediction Challenge (17 May to 13 June 2021).
- Source: https://zindi.africa/competitions/indabax-tanzania-mobile-banking-prediction-challenge; the Zindi API lists Train.csv 11,296,855 bytes, Test.csv 4,748,025 bytes, SampleSubmission.csv 604,211 bytes and VariableDefinitions.csv 2,231 bytes, byte for byte the sizes of `ix_mobile_banking_prediction_challenge`, with the same description ("predict if individuals across Africa and around the world use mobile or internet banking"), the same data description ("~100 000 and the test contains ~45 000 survey responses") and the same metric (AUC).
- Siblings and duplicates: the first publication is `ix_mobile_banking_prediction_challenge` (screened `TBD -> 2nd Tier`, 2026-10-22); this record ends at the same source (PROV-4, PROV-8).
- Metric: ROC AUC, Zindi Evaluation page.
- Reject check (AI, 2026-10-22): stands. Zindi API: parent 'ix-mobile-banking-prediction-challenge' (17 May to 13 Jun 2021, run first), with identical files: Train.csv 11,296,855, Test.csv 4,748,025, SampleSubmission.csv 604,211, VariableDefinitions.csv 2,231 B. https://zindi.africa/competitions/indabax-tanzania-mobile-banking-prediction-challenge

IndabaX Tanzania mobile-banking challenge asks to predict who uses mobile banking, a financial-inclusion binary classification on survey/demographic tabular features (FinScope-style). This is a genuine real-world predictive tabular task fitting the IID criterion. Plausible Yes, but mobile-banking/financial-inclusion data can be survey-derived and overlaps with other Zindi financial-inclusion challenges. A human must verify size, the target, whether it duplicates the financial-inclusion-in-Africa dataset, and that features are not aggregate/survey-only weighting issues.

---

predict who uses mobile banking
