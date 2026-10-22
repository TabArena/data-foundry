---
unique_name: health_insurance
name: health_insurance
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Outdated
- No Good Target (yet)
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '1993'
domain: social science
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/44993
- March 1993 CPS
source_row: 808
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the `No` (TabArena workbook reject, the CC above) holds: the source is an econometric estimate of a causal effect, not a prediction a decision uses (SEL-3, USE-1). Counter-point for the curator: social science is thin in the benchmark (1 accepted), but a thin domain does not make a task (the priority factors never override a Must).
- Source: Olson, C. A. (1998), "A comparison of parametric and semiparametric estimates of the effect of spousal health insurance coverage on weekly hours worked by wives", Journal of Applied Econometrics 13(5):543-565, on the March 1993 Current Population Survey; distributed as `HI` in the R package Ecdat; OpenML 44993 (`health_insurance`, v3, uploaded 2022-12-22): 22,272 married women x 12 features, target `whrswk` (hours worked per week by the wife), with `wght` a "sampling weight (should be ignored)".
- Use case: none; the paper asks how much spousal coverage changes wives' labour supply (an effect estimate); nobody decides on a predicted weekly hours figure. Regime would be IID (one cross-section).
- Siblings and duplicates: none among the records (checked by name, OpenML id, Olson, spousal). External collections: TabSTAR (as recorded).
- Metric: none for prediction (the paper compares estimators of an effect).
- Risks: `year` holds 1993, the survey year; by PROV-9 the first publication of this table is the 1998 paper and its data archive (not changed: a human-verdict record).
- Priority: none (verdict `No`).

OpenML dataset derived from the March 1993 CPS, used in an econometrics study estimating the effect of spousal health-insurance coverage on weekly hours worked by wives. The curation comment notes the target (predicting work hours of married wives in 1993) is outdated, not a genuine predictive task, and confounded by income. It is already in TabArena Reject. It fails on outdatedness and lack of a meaningful, non-confounded predictive target. No.

---

CC: "predicting the work hours from health insurance data? very weird task; Outdated, as predicting work hours of married wifes from 1993 is not representative. Also not a predictive task. not a predictive task as far as I can tell, also the study sounds confounded by income"

## Reference

Olson, Craig A. "A comparison of parametric and semiparametric estimates of the effect of spousal health insurance coverage on weekly hours worked by wives." Journal of Applied Econometrics 13.5 (1998): 543-565.
