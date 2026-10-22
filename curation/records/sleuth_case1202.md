---
unique_name: sleuth_case1202
name: sleuth_case1202
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
- https://www.openml.org/search?type=data&id=706
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the workbook verdict ("Tiny data"; Lennart and Andrej: too small) and the current `TBD -> 2nd Tier` are left as they are; priority 1. A counter-argument on the reason.
- Source: The Statistical Sleuth (Ramsey and Schafer, Duxbury 1997), Case Study 12.2, via StatLib (lib.stat.cmu.edu/datasets, 1997) and OpenML 706 (2014). 93 rows x 7 columns (bsal, sal77, fsex, senior, age, educ, exper): the Harris Trust and Savings Bank employees in a sex-discrimination case (the book's study of beginning salaries by sex). OpenML's default target `exper` (prior experience) is an arbitrary column.
- Use case: none: the source asks whether women were paid less at hire, a discovery question; no actor predicts an employee's prior experience, and predicting salary from sex would encode the bias under study (SEL-3, USE-2).
- Siblings and duplicates: `sleuth_case2002`, `sleuth_ex1605`, `sleuth_ex1714` (the same book); Lennart kept `sleuth_case2002` at `TBD -> 2nd Tier` as "a real study but for scientific discovery". External collections: OpenML.
- Metric: none (a textbook regression analysis); the fallback.
- **Counter-argument (AI):** the stronger reason is SEL-3 (`No Good Target  / Scientific Discovery`), not size: under TP-5 a 93-row regression is a tiny-data task, not `Too Small` by itself. By SEL-3 the verdict would be `No`; treated like `sleuth_case2002` it stays `TBD -> 2nd Tier`. The curator has the call.
- Priority: gap -, use case -, source + (textbook, StatLib), shape - (93 rows), risk - (arbitrary target).


OpenML 706, a Sleuth statistics-textbook dataset with only 93 samples, far too small for the benchmark's 3-fold CV protocol. The TabArena curation verdict and two reviewers (Lennart, Andrej) already agree it is too small. It is excluded on size; it is one of a family of tiny Sleuth textbook tables.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

93 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small

Highly related to `sleuth_case2002` (Sleuth textbook datasets).
