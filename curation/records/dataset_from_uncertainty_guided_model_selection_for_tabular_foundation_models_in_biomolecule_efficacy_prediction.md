---
unique_name: dataset_from_uncertainty_guided_model_selection_for_tabular_foundation_models_in_biomolecule_efficacy_prediction
name: Dataset from Uncertainty-Guided Model Selection for Tabular Foundation Models in Biomolecule Efficacy Prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- Data Requested
tags:
- New IID
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2025'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://arxiv.org/abs/2510.02476
source_row: 865
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Dataset(s) from a 2025 arXiv paper on tabular foundation models for biomolecule efficacy prediction; this is a genuine tabular predictive task (efficacy regression/classification on molecular descriptor features) and explicitly relevant to tabular ML. The record notes the data was preprocessed from prior work, was requested on 14/03/2026, and could possibly be reconstructed manually. Risks: the features may be derived/transformed descriptors, and a grouped (by scaffold/assay) split may be required. A human must verify data availability, that the features are not lossy/irreversible transforms, the exact target, and the appropriate split.

---

Their data could be used; it is from another work and has been preprocessed.

Lennart: requested their versions of the dataset for benchmarking on 14/03/2026. But we could also likely reproduce one/some of their data state manually
