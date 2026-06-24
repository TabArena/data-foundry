---
unique_name: elusage
name: elusage
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
year: '?'
domain: Other
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=228
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

OpenML 'elusage' is a tiny dataset of 55 samples (electricity usage vs. month/temperature). The record already records a TabArena verdict of 'Tiny data' with two reviewers (Lennart, Andrej) independently calling it too small for 3-fold CV. It is far below any reasonable size threshold for a stable benchmark task. Excluded as Too Small; nothing further to verify.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

55 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small
