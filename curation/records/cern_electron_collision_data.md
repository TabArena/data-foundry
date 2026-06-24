---
unique_name: cern_electron_collision_data
name: CERN Electron Collision Data
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Not Representative
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: physics & astronomy
problem_type: Other
original_data_state: One Table
source_links:
- https://opendata.cern.ch/record/304
- https://www.kaggle.com/datasets/fedesoriano/cern-electron-collision-data
source_row: 831
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

CERN Open Data dielectron collision events: each row gives the kinematic measurements (energy, momentum components, etc.) of two electrons. There is no natural supervised predictive target; the commonly used 'target' (invariant mass) is a deterministic algebraic function of the input columns, which would be trivial/leaky, and the dataset is fundamentally physics scientific-discovery data rather than a representative tabular ML task. A human could confirm no meaningful non-deterministic target exists, but it should be rejected as scientific-discovery.

---

Unsure if the same problem as Higgs (or Higgs-like datasets).
