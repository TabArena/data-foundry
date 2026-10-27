---
unique_name: sleuth_ex1714
name: sleuth_ex1714
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target / Scientific Discovery
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
- https://www.openml.org/search?type=data&id=659
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: the proposed fast reject (SEL-3 (with SEL-8; Lennart and Andrej's 'too small' supports, TP-5)) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`No Good Target / Scientific Discovery`, SEL-3): a textbook table from a civil-rights inquiry into insurance redlining, 47 Chicago zip codes; no predictive task, and the OpenML target `income` was picked by default.
- Source: Ramsey and Schafer, The Statistical Sleuth (2nd ed., Duxbury 2002), exercise 17.14 (R package Sleuth2, `ex1714`); the data from Andrews and Herzberg, Data (1985): Illinois Department of Insurance counts of homeowner policies by zip code, December 1977 to February 1978, fire and theft from 1975. As published: 47 x 8 (Zip, Fire, Theft, Age, Income, Race, Vol, Invol). OpenML 659 (StatLib upload) sets `income` as target with "CLASSINDEX: none specific".
- Use case: none. Sleuth2: "In the 1970's the U.S. Commission on Civil Rights investigated charges that insurance companies were attempting to redefine Chicago 'neighborhoods' in order to cancel existing homeowner insurance policies or refuse to issue new ones": the question is whether involuntary (FAIR plan) policies relate to the minority share after adjusting for fire, theft and housing age, an inference on 47 areas (SEL-3, SEL-8). Median family income per zip code as a target has no actor.
- Siblings and duplicates: the same data is faraway's `chredlin` (no record); `sleuth_case2002`, `sleuth_ex1605`, `sleuth_case1202` are other Sleuth tables (Lennart kept sleuth_case2002 as `TBD -> 2nd Tier`, `Outdated`). External collections: OpenML 659.
- Metric: none (a regression exercise in a textbook).
- The workbook notes (TabArena "Tiny data"; Lennart and Andrej: "too small") agree on dropping it; size alone would be TP-5, the target decides here.
- Reject check (AI, 2026-10-22): does not stand. The SEL-3 reading is sound (Sleuth2: "the U.S. Commission on Civil Rights investigated charges that insurance companies were attempting to redefine Chicago 'neighborhoods'", https://search.r-project.org/CRAN/refmans/Sleuth2/html/ex1714.html; OpenML 659 "CLASSINDEX: none specific", https://www.openml.org/d/659). But the curator's precedent goes the other way: Lennart kept sleuth_case2002 at TBD -> 2nd Tier although he called it "a real study but for scientific discovery", and today's run left the sibling Sleuth tables (sleuth_ex1605, sleuth_case1202) at TBD -> 2nd Tier, priority 1, with the same SEL-3 counter-argument. A No here alone would be inconsistent; size alone is not a reason (TP-5), and the record had already been moved off No by the size policy.
- For /add-dataset: TBD -> 2nd Tier, priority 1. Treat it like sleuth_ex1605/sleuth_case1202: put the SEL-3 counter-argument (no actor predicts zip-level income; Invol is the inference response) in the record for the curator to settle the Sleuth family in one decision; if it is added, choose a target with a use case (not OpenML's default `income`), and check TP-5 on 47 rows.

OpenML 659, a Sleuth statistics-textbook dataset with only 47 samples, far too small for the benchmark's 3-fold CV protocol. The TabArena curation verdict and two reviewers (Lennart, Andrej) already agree it is too small. It is excluded on size; it is one of a family of tiny Sleuth textbook tables.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

47 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small

Highly related to `sleuth_case2002` (Sleuth textbook datasets).
