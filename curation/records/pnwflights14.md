---
unique_name: pnwflights14
name: pnwflights14
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
year: '2014'
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/ismayc/pnwflights14
source_row: 1027
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Pacific Northwest 2014 flights data (analogous to the well-known nycflights13 teaching dataset), distributed as flights plus auxiliary tables (airlines/airports/weather). It supports standard tabular tasks such as flight delay classification or arrival-delay regression with a natural temporal split, and is large and real-world. Some joining and target definition is needed, and the standard departure-time leakage must be avoided. Suggest TBD -> Yes; a human must pick the non-leaking target (e.g. arrival delay) and confirm usable size after cleaning.
