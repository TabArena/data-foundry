---
unique_name: cps88wages
name: cps88wages
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 4
decision_markers:
- Outdated
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
original_source: Other
year: '1988'
domain: social science
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/44984
- unclear maybe https://www.icpsr.umich.edu/web/ICPSR/studies/4377
source_row: 807
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 4: a real, documented CPS wage table, but built for
econometric specification testing, not for a decision (the curator's CC line and the TabArena reject point the same way).
- Source: March 1988 Current Population Survey (US Census Bureau), sample drawn by Bierens & Ginther (Empirical Economics
  26, 2001) for testing quantile-regression models; distributed as `CPS1988` in the R package AER and as OpenML 44984.
  As published: 28,155 men aged 18-70 x 7 columns: `wage` (target, deflated to 1992 dollars), `education`, `experience`
  (potential), `ethnicity` (cauc/afam), `smsa`, `region`, `parttime`. One table.
- Use case: no actor named by the source; the paper estimates a (median) wage equation, a returns-to-schooling question
  (USE-2). A use case the curation could write (an HR salary benchmark) would be approximate at best and uses 1988 data.
  Regime IID (one cross-section, one survey month).
- Siblings and duplicates: `census_income` (CPS 1994/95, income threshold, also `TabArena Reject`, TBD -> 2nd Tier) is a
  different survey year and task; no duplicate of this extract found. External collections: TabArena Reject, TabSTAR.
- Papers and pages: Bierens & Ginther 2001; OpenML 44984 ("The goal is to estimate the wage using information about
  working individuals"); the original page http://www.personal.psu.edu/hxb11/MEDIAN.HTM (offline).
- Metric: none found as a prediction metric (OpenML page, AER docs; the paper tests model specifications), so the
  fallback (RMSE on log wage would be the econometric habit).
- Risks for /add-dataset: few features (6), `ethnicity` as a sensitive input (the CC line); `Outdated` stays.
- Priority: gap + (social science thin), use case -, source + (paper, CPS documentation), shape + (28k rows, mixed types).

CPS 1988 wages dataset: predict (log) wage from census/survey demographic features. It is a genuine real-world tabular regression with a clear target, but it is outdated (1988) and is already in the TabArena Reject and TabSTAR collections, with a curation note questioning whether predicting wage from sensitive demographic features is desirable. These outdatedness and sensitivity concerns argue against first-tier inclusion rather than against task validity. A human should weigh the ethical/sensitive-feature angle, the age of the data, and whether a fresher CPS extract is preferable, plus confirm the row count.

---

CC: "predict wage based on census/survey data. again census data that is outdated, unclear if the task of predicting the wage based on the selected sensitive features makes sense"

## Reference

Bierens, Herman J., and Donna K. Ginther. "Integrated conditional moment testing of quantile regression models." Empirical Economics 26 (2001): 307-324.
