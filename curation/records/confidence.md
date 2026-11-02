---
unique_name: confidence
name: confidence
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
original_source: Other
year: '?'
domain: Other
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/confidence/metadata.yaml
- https://www.openml.org/d/468
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the workbook verdict (Tiny data; Lennart and Andrej: too small) stands, priority 1;
recommend `No` with `Too Small` and `No Good Target / Scientific Discovery` (TP-5, SEL-3); the curator has the call.
- Source: StatLib, consumer-confidence items given by Gordon Bechtel (Univ. of Florida) with permission of the Conference
  Board and the Michigan Survey Research Center, "1992 DATA" (OpenML 468, "Source: Unknown - Date unknown"); PMLB copies
  it. As published: 72 rows x 3 numeric features `P`, `N`, `O` (share of pessimistic, neutral, optimistic answers) and
  the target `ITEM`, which of six survey questions (business conditions, jobs, family income, 6 or 12 months ahead) the
  row is; 12 rows per item. OpenML 1015 is a binarised version (60/12). The record's old `Regression` was wrong:
  PMLB and OpenML serve a 6-class classification (`problem_type` corrected, it was AI-filled).
- Use case: none. Telling which survey question produced a month's answer shares is no decision anyone makes; the table
  is a survey summary (SEL-3). Regime would be IID at best; the 12 rows per item are likely the months of 1992 (temporal).
- Siblings and duplicates: none in `curation/records/` besides the PMLB/OpenML copies named here.
- Papers and pages: no paper found; OpenML 468 description, PMLB metadata (empty description).
- Metric: none found (OpenML, PMLB, StatLib text); the fallback.
- Risks for /add-dataset: 72 rows, 12 per class (TP-5); no target a decision fits (SEL-3).
- Priority: gap 0, use case -, source - (anonymous StatLib note), shape - (72 x 3).

PMLB 'confidence' dataset with only 72 samples. Both the prior TabArena verdict and the two named reviewers (Lennart, Andrej) flagged it as too small, and 72 rows is far below what the benchmark's CV protocol can support. There is no path to making this representative at that size. Reject on size; no further verification needed.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

72 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small
