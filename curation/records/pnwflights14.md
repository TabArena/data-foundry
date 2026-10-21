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

**Assessment (AI, 2026-10-21):** aeolus (BTS on-time flights 2016-2024 with hourly weather at both airports, a temporal task in the TabArena v0.2 working copy as `aeolus_1m`) covers US flight delays, and pnwflights14 ends at the same BTS on-time table (aeolus review panel, precedent check, 2026-10-20). When this record is processed, judge it against aeolus under PROV-6: a second flight-delay task, or a duplicate of aeolus (a cut of one source without a distinct task), as for airlines and airlines_depdelay_10m.
