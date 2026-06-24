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

OpenML dataset derived from the March 1993 CPS, used in an econometrics study estimating the effect of spousal health-insurance coverage on weekly hours worked by wives. The curation comment notes the target (predicting work hours of married wives in 1993) is outdated, not a genuine predictive task, and confounded by income. It is already in TabArena Reject. It fails on outdatedness and lack of a meaningful, non-confounded predictive target. No.

---

CC: "predicting the work hours from health insurance data? very weird task; Outdated, as predicting work hours of married wifes from 1993 is not representative. Also not a predictive task. not a predictive task as far as I can tell, also the study sounds confounded by income"

## Reference

Olson, Craig A. "A comparison of parametric and semiparametric estimates of the effect of spousal health insurance coverage on weekly hours worked by wives." Journal of Applied Econometrics 13.5 (1998): 543-565.
