---
unique_name: strikes
name: strikes
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '1999'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/770
- https://lib.stat.cmu.edu/datasets/
- https://www.openml.org/d/549
source_row: 800
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's `No` stands: a country-year macro panel analysed to compare explanatory models, with no decision that a prediction would serve.
- Source: Bruce Western, StatLib 1999 (OpenML 549, uploaded 2014): "annual observations on the level of strike volume (days lost due to industrial disputes per 1000 wage salary earners), and their covariates in 18 OECD countries from 1951-1985"; 625 rows x 7 columns (country, year, strike volume, unemployment, inflation, social-democratic parliamentary representation, a time-invariant union-centralization measure); "analyzed in ... 'Vague Theory and Model Uncertainty in Macrosociology'" (Sociological Methodology).
- Use case: none named; the paper is about model uncertainty in explaining strike volume, not about predicting it. A real prediction would be next year's strike volume per country, which is forecasting (SEL-10); the same-year covariates make it an explanation exercise (SEL-3). Regime if kept: temporal or grouped by country.
- Siblings and duplicates: OpenML 770 is "Binarized version of the original data set ... computing the mean" (a derived copy, same record). External collections: TabSTAR; TabArena Reject.
- Papers and pages: https://www.openml.org/d/549, https://lib.stat.cmu.edu/datasets/; Western 1996/1999 paper not read.
- Metric: none found (OpenML and StatLib descriptions); the fallback would apply.
- Counter-argument: none found; the marker matches the curator's reason ("Rather interpretability than predictive task"). 625 rows over 18 countries would also be small for a grouped split.

The OpenML 'strikes' regression dataset (volume of strikes by country/year, 1951-1985) from a macrosociology study. It is already in the TabArena Reject collection; the curator notes it is an interpretability rather than predictive task, is small, and needs group/time-based splits. The dataset is tiny and tied to a sociological modeling exercise, not representative real-world tabular prediction. Recommend reject, consistent with prior curation.

**Update (policy):** removed the "Too Small" marker — size is not a rejection reason (decided post-Data Foundry); this record stays No on its other ground(s).

---

CC: "Regression. Rather interpretability than predictive task. temporal (collection 1951-1985); requires group-based or time-based splits"

## Reference

Vague Theory and Model Uncertainty in Macrosociology," which is to appear in Sociological Methodology
