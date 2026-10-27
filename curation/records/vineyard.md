---
unique_name: vineyard
name: vineyard
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
year: '?'
domain: biology & life sciences
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=192
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the workbook verdict (Tiny data; Lennart and Andrej: too small) stands, priority 1; recommend `No` with `Too Small` (TP-5); the curator has the call.
- Source: OpenML 192 (uploaded 2014): "Dataset from Smoothing Methods in Statistics (ftp stat.cmu.edu/datasets)", Simonoff, J.S. (1996), Springer; "Source: Unknown". As published: 52 rows x 4 numeric columns, `row_number`, `lugs_1989`, `lugs_1990` and the target `lugs_1991` (grape harvest in lugs per vineyard row).
- Use case: a grower's yield of a row in 1991 from the two previous harvests: the target is the next value of each row's own series (close to SEL-10 forecasting, SEL-11 only with more years); a textbook smoothing example, not a decision. Regime would be temporal, with only one target year.
- Siblings and duplicates: none in `curation/records/`; OpenML and the CMU StatLib archive carry it.
- Papers and pages: Simonoff (1996), as an example for smoothing.
- Metric: none found (OpenML page), so the fallback (rmse).
- Risks for /add-dataset: 52 rows, about 17 per test fold (TP-5); the features are lags of the target.
- Priority: gap 0, use case 0 (none), source - (a textbook example, source unknown on OpenML), shape - (52 x 3), risk - (lagged target).

The OpenML 'vineyard' dataset (id 192) has only 52 samples. The TabArena curation verdict and reviewers (Lennart, Andrej) all mark it as too small for reliable 3-fold CV evaluation. It fails the adequate-size criterion and should be rejected as Too Small; no further verification needed.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

52 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small
