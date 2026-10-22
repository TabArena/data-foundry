---
unique_name: pollution
name: pollution
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
year: '1973'
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=542
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: 60 US metropolitan areas from a 1973 study of regression instability, an explanatory table with the workbook's "Tiny data" by Lennart and Andrej; a curator may well reject it (`Too Small`, TP-5, or `No Good Target  / Scientific Discovery`, SEL-3).
- Source: McDonald, G.C. and Schwing, R.C. (1973), "Instabilities of regression estimates relating air pollution to mortality", Technometrics 15, 463-; served by StatLib and OpenML 542 ("the pollution data so loved by writers of papers on ridge regression"); as published: 60 rows (SMSAs, 1959-1961) x 15 numeric predictors (climate, demography, HC, NOX, SO2 potentials), target `MORT` (age-adjusted mortality per 100,000).
- Use case: none the source states: the paper estimates the effect of pollution on mortality across cities, a look at the coefficients, not a decision on a new city; fit none or approximate at best; regime IID (one row per metropolitan area, no time).
- Siblings and duplicates: none found (grep McDonald, Schwing, 542); other pollution records are different data; external collections: OpenML, StatLib.
- Papers and pages: the Technometrics paper (not read); many ridge-regression papers used it.
- Metric: none found as a prediction metric (the OpenML page states none; the paper studies coefficient stability), so the fallback `rmse`.
- Risks for /add-dataset: 60 rows give about 20 test rows per fold (TP-5); the target is an observed rate, but the task is explanatory (SEL-3, USE-2).
- Priority: gap 0, use case 0, source + (a peer-reviewed paper), shape 0 (60 rows), risk - (too small, unclear decision).

OpenML dataset id 542, a classic pollution/mortality regression table with only 60 samples. Prior TabArena verdict and both Lennart and Andrej flagged it as too small for the 3-fold CV protocol. With 60 rows it cannot support reliable benchmarking. Suggest No on size grounds.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

60 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small
