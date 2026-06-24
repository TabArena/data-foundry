---
unique_name: bloodsai_blood_spectroscopy_classification_challenge
name: bloodsai-blood-spectroscopy-classification-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/bloodsai-blood-spectroscopy-classification-challenge/data
source_row: 914
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi BloodS.ai challenge to classify blood samples from spectroscopy measurements. Spectroscopy yields high-dimensional spectral intensity vectors (wavelength channels), which sit on the boundary between tabular ML and signal/spectral data where the feature ordering carries meaning, so it may not be fully representative of generic tabular ML. The task is a genuine real-world predictive classification with a clear target, which is in scope, but representativeness is the open question. A human must inspect the actual feature set (number/nature of spectral channels), sample count after cleaning, and whether standard tabular models are competitive here versus signal-specific methods.
