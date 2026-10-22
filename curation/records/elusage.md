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

**Assessment (AI, 2026-10-22):** the workbook verdict stands: "Tiny data", "Lennart: too small", "Andrej: too small"; recommend restoring `No` with `Too Small` (and noting `No Good Target  / Scientific Discovery`); the curator has the call. The current `TBD -> 2nd Tier` came from an AI "policy" note, not from a curator.
- Source: OpenML 228 (uploaded 2014), "Dataset from Smoothing Methods in Statistics (ftp stat.cmu.edu/datasets) Simonoff, J.S. (1996)", the same book as `quake` (Lennart: `No`, Scientific Discovery). As published: 55 rows, 3 columns, target `average_electricity_usage` (monthly household electricity use against month and average temperature), no missing values.
- Use case: none stated; a textbook smoothing example. A utility forecasting its load would use a series (SEL-10), not 55 monthly rows; fit none.
- Siblings and duplicates: `quake` (same book, `No`); no copy found. External collections: OpenML only.
- Metric: none found (OpenML description, the book's citation); the fallback would be `rmse`.
- Risks: TP-5 (55 rows, about 18 per test fold), no task (SEL-3); `year` `?` would be 1996 (PROV-9).
- No priority set: the human verdict is a reject.


OpenML 'elusage' is a tiny dataset of 55 samples (electricity usage vs. month/temperature). The record already records a TabArena verdict of 'Tiny data' with two reviewers (Lennart, Andrej) independently calling it too small for 3-fold CV. It is far below any reasonable size threshold for a stable benchmark task. Excluded as Too Small; nothing further to verify.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

55 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small
