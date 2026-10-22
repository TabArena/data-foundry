---
unique_name: cern_electron_collision_data
name: CERN Electron Collision Data
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Trivial
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

**Screening (AI, 2026-10-22):** `No` (`No Good Target  / Scientific Discovery`, SEL-3; `Trivial`, SEL-5): a CMS outreach sample of real dielectron events with no label; the only target-like column, the invariant mass, is computed from the other columns.
- Source: CERN Open Data Portal record 304, Thomas McCauley, published 2014 (data 2010), CC0, doi 10.7483/OPENDATA.CMS.PCSW.AHVG: "100k dielectron events in the invariant mass range 2-110 GeV for use in outreach and education", "not suitable for a full physics analysis". Columns: Run, Event, and per electron E, px, py, pz, pt, eta, phi, Q; M, "The invariant mass of two electrons (GeV)". Kaggle copy by fedesoriano (2020) repeats the CERN text and defines no task.
- Use case: none; there is no outcome or annotation per event, and M = sqrt((E1+E2)^2 - |p1+p2|^2) is the definition of the invariant mass from the row's own four-vectors, so a regression on M is a formula (SEL-5, TP-4). Events were also selected on M (2-110 GeV).
- Siblings and duplicates: `cern_proton_collision_dataset` (same uploader, same verdict proposed); `higgs`, `hepmass`, `susy` are simulations (Lennart `No` on `higgs`, SEL-16) and a different case: this is real data without a label. The human note "Unsure if the same problem as Higgs": it is not simulated, but it has no target.
- Metric: none (no task is defined anywhere).
- Physics is a thin domain; the gap does not create a target.
- Reject check (AI, 2026-10-22): stands. CERN record 304 (https://opendata.cern.ch/record/304): '100k dielectron events ... for use in outreach and education', 'not suitable for a full physics analysis'; no outcome or annotation per event, and M is the invariant mass of the row's own two four-vectors (SEL-3, SEL-5).

CERN Open Data dielectron collision events: each row gives the kinematic measurements (energy, momentum components, etc.) of two electrons. There is no natural supervised predictive target; the commonly used 'target' (invariant mass) is a deterministic algebraic function of the input columns, which would be trivial/leaky, and the dataset is fundamentally physics scientific-discovery data rather than a representative tabular ML task. A human could confirm no meaningful non-deterministic target exists, but it should be rejected as scientific-discovery.

---

Unsure if the same problem as Higgs (or Higgs-like datasets).
