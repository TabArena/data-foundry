---
unique_name: bloodsai_blood_spectroscopy_classification_challenge
name: bloodsai-blood-spectroscopy-classification-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
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

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a real non-invasive blood-test task, but raw NIR spectral bins and 60 shuffled repeat scans per sample with no sample id.
- Source: Zindi competition with bloods.ai, 2021-10-19 to 2022-02-13, $7,500; as published: `Train.csv` / `Test.csv` (and `_trimmed` versions), 170 `absorbance` columns (NIR, 900-1700 nm per the collection page), `temperature`, `humidity`, `Id`, three targets `hdl_cholesterol_human`, `cholesterol_ldl_human`, `hemoglobin(hgb)_human`, each low / ok / high; row count not seen (page could be read through the API; data needs a login).
- Use case: a person scans a fingertip with a NIR device and gets a blood-level class sent to a doctor (the source names patients, home devices and doctors); fit approximate, the label is a lab test paired to the scan; regime grouped by sample, but the source says "Each blood sample is scanned 60 times ... We have shuffled the measurements, so you won't know which measurements are from the same sample", so no group id ships.
- Siblings and duplicates: none found (soil spectral records `open_soil_spectral_library`, `africa_soil_property_prediction_challenge` are other domains). External collections: none found.
- Papers and pages: https://zindi.africa/competitions/bloodsai-blood-spectroscopy-classification-challenge (Description, Data Collection & Exporting Procedures, Data Description, Evaluation); a bloods.ai US patent is linked from the data page.
- Metric: Accuracy over the three targets (Zindi Evaluation page: "The evaluation metric for this challenge is Accuracy"), a leaderboard metric (MET-4), argmax, no threshold to fix (MET-6); inputs none beyond the class.
- Risks for /add-dataset: repeats of one sample across folds without a group id (a leak a random split cannot avoid; recovering the groups would be our own reconstruction, P4, P5); raw spectral bins lean out (SEL-15, weighed); three targets, pick one (CLEAN-18); `problem_type` Multiclass holds; `required_split` Random (IID) (AI-filled) is contradicted by the repeats and kept only until the group question is settled.
- Priority: gap - (medical not thin), use case + (actor and decision named by the host), source + (host documents collection and calibration), shape - (170 spectral bins, size unknown), risk - (hidden repeat groups).

Zindi BloodS.ai challenge to classify blood samples from spectroscopy measurements. Spectroscopy yields high-dimensional spectral intensity vectors (wavelength channels), which sit on the boundary between tabular ML and signal/spectral data where the feature ordering carries meaning, so it may not be fully representative of generic tabular ML. The task is a genuine real-world predictive classification with a clear target, which is in scope, but representativeness is the open question. A human must inspect the actual feature set (number/nature of spectral channels), sample count after cleaning, and whether standard tabular models are competitive here versus signal-specific methods.
