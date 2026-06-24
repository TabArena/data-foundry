---
unique_name: cps88wages
name: cps88wages
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Outdated
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
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

CPS 1988 wages dataset: predict (log) wage from census/survey demographic features. It is a genuine real-world tabular regression with a clear target, but it is outdated (1988) and is already in the TabArena Reject and TabSTAR collections, with a curation note questioning whether predicting wage from sensitive demographic features is desirable. These outdatedness and sensitivity concerns argue against first-tier inclusion rather than against task validity. A human should weigh the ethical/sensitive-feature angle, the age of the data, and whether a fresher CPS extract is preferable, plus confirm the row count.

---

CC: "predict wage based on census/survey data. again census data that is outdated, unclear if the task of predicting the wage based on the selected sensitive features makes sense"

## Reference

Bierens, Herman J., and Donna K. Ginther. "Integrated conditional moment testing of quantile regression models." Empirical Economics 26 (2001): 307-324.
