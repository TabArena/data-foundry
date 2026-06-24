---
unique_name: lowbwt
name: BNG
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Missing source information
tags:
- AI-Filled (Verify)
year: '?'
domain: medical & healthcare
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=1193
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

OpenML id 1193, a low-birth-weight dataset. The TabArena curation verdict and reviewer comments converge on tiny data (the original has only 189 samples) plus concerns that this version is a simulated BNG/data-stream variant lacking source information. Both the tiny original size and the simulated/missing-provenance status are disqualifying under the criteria. The 'BNG' name suggests a Bayesian-Network-Generator synthetic expansion. A human could confirm whether any usable real version exists, but the existing TabArena reject verdict supports a No.

**Update (policy):** removed the "Too Small" marker — size is not a rejection reason (decided post-Data Foundry); this record stays No on its other ground(s).

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

see above - Original dataset has only 189 samples

Potential issue: simulated, missing source information, data streams

Lennart: simulated data streams without source information

Andrej: too small
