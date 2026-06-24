---
unique_name: mimic_iv
name: MIMIC-IV
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
- Ethical Issue
tags:
- '?'
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: medical & healthcare
required_split:
- '?'
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://physionet.org/content/mimiciv/
source_row: 798
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

MIMIC-IV is the large PhysioNet critical-care relational database (many tables to be joined), supporting real clinical prediction tasks like mortality or readmission. It is a genuine real-world source but requires credentialed access (DUA), substantial wrangling to derive a fixed tabular task, and has patient-privacy/ethical access constraints. The curator is unsure which version/task to use or whether it is even feasible. This is not a drop-in dataset, so TBD -> 2nd Tier. A human must decide the specific cohort/target, handle the credentialing and licensing, define the join/feature pipeline, and choose a patient-grouped split.

---

Another MIMIC dataset. Need to figure out which version(s) to use and how, or if even possible.
