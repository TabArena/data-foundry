---
unique_name: dont_overfit_by_uofk_fmsi
name: dont-overfit-by-uofk-fmsi
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Too Small
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/dont-overfit-by-uofk-fmsi/data
source_row: 971
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi 'Don't Overfit' competition (UofK FMSI), modeled on the well-known Kaggle 'Don't Overfit!' challenges, which deliberately provide a tiny training set with many anonymized continuous features to stress-test overfitting. Such datasets are typically very small and often artificial/anonymized, putting them at risk under criterion 4B (artificial) and 'Too Small'. They can still be interesting tabular benchmarks but are unrepresentative edge cases. A human must verify the training-set size, whether features are real or synthetic/anonymized, and the target before any promotion; 2nd Tier at most.
