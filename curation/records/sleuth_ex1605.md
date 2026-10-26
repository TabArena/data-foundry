---
unique_name: sleuth_ex1605
name: sleuth_ex1605
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
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
- https://www.openml.org/search?type=data&id=687
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the workbook verdict ("Tiny data"; Lennart and Andrej: too small) and the current `TBD -> 2nd Tier` are left as they are; priority 1. A counter-argument on the reason.
- Source: The Statistical Sleuth (Ramsey and Schafer), Exercise 16.5, via StatLib (1997) and OpenML 687 (2014); the data is "a subset from an observational, longitudinal, study on adopted children", Skodak and Skeels (1949) (Sleuth3 R documentation, https://search.r-project.org/CRAN/refmans/Sleuth3/html/ex1605.html). 62 rows x 6 columns: FMED (adoptive mother's years of education), TMIQ (biological mother's IQ), the child's IQ at ages 2, 4, 8 and 13; OpenML's target `Age13IQ`.
- Use case: none: the exercise asks "whether child's intelligence related to intelligence of the biological mother and the intelligence of the adoptive mother", a discovery question on a 1949 cohort; no actor decides on a predicted IQ at 13 (SEL-3, USE-2; `Outdated` would also apply).
- Siblings and duplicates: `sleuth_case1202`, `sleuth_case2002` (Lennart: "a real study but for scientific discovery", `TBD -> 2nd Tier`), `sleuth_ex1714`. External collections: OpenML.
- Metric: none; the fallback.
- **Counter-argument (AI):** the stronger reason is SEL-3 (`No Good Target / Scientific Discovery`), not size alone; with 62 rows the size is borderline as well (TP-5 counts the spread per test fold). Treated like `sleuth_case2002` it stays `TBD -> 2nd Tier`. The curator has the call.
- Priority: gap -, use case -, source + (textbook, StatLib, the 1949 study), shape - (62 rows), risk - (target picked by the uploader).


OpenML 687, a Sleuth statistics-textbook dataset with only 62 samples, far too small for the benchmark's 3-fold CV protocol. The TabArena curation verdict and two reviewers (Lennart, Andrej) already agree it is too small. It is excluded on size; it is one of a family of tiny Sleuth textbook tables.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

62 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small

Highly related to `sleuth_case2002` (Sleuth textbook datasets).
