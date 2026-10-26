---
unique_name: adult
name: adult
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
- No Good Target / Scientific Discovery
- Outdated
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '1996'
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5XW20
- https://www.openml.org/search?type=data&id=1590
source_row: 804
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's `No` (CC line, TabArena Reject) stands on SEL-3 and USE grounds; one counter-argument on a marker: `Duplicate` does not fit.
- Source: UCI Adult (doi 10.24432/C5XW20), donated in 1996 by Ronny Kohavi and Barry Becker, extracted by Becker from the 1994 Census database; 48,842 rows x 14 features (train 32,561, test 16,281), the target income above 50K dollars; first used in Kohavi (KDD 1996), see Reference.
- Use case: none fits, as the CC says: no actor decides on whether income exceeds 50K, and the data was not collected for that decision (SEL-3; `No Good Target / Scientific Discovery`). `Outdated`: 1994 data; Ding et al. (NeurIPS 2021, "Retiring Adult") rebuilt the task on American Community Survey data (Folktables, ACSIncome), for which no record exists.
- Siblings and duplicates: `census_income` (KDD 1994-95 CPS, 300k rows, `TBD -> 2nd Tier`, AI) is another extract of the same survey programme, not a copy of Adult, and Adult is the first publication; `income_prediction_challenge_for_azubian` and `predictive_insights_youth_income_prediction_challenge` are other populations. External collections: TabSTAR, OpenML 1590.
- Metric: Kohavi 1996 reports accuracy (error rate) only, a habit (MET-6), so the fallback had it shipped.
- Ethics: race and sex are features (noted by the curator); no objection from subjects or creators found (SEL-1 not triggered on the source's words).
- **Counter-argument (AI):** `Duplicate` (PROV-4 to PROV-7) needs a recorded original that Adult copies; none exists, and the OpenML link is Adult itself. Suggest dropping the marker, or naming the dataset it duplicates; the verdict does not depend on it. The curator has the call.

The classic 1996 UCI/Census 'Adult' income (>50K) dataset, already tagged 'TabArena Reject' and '2nd Tier / Scientific Discovery'. It is hugely overused/duplicated across benchmarks, derived from a 1994 census extract, and curators note the >50K target was never a real operational task (ethical concerns around race as a feature). While it is representative tabular data, it is not a meaningful real predictive task and is explicitly a prior reject. No additional verification is needed to keep it out.

---

CC: "determine whether a person makes over 50K a year from Census data. Not a meaningful task. Potential ethical issues from including race as a feature. Can be understood as a real gap-filling task or from the IRS to detect if someone entered fraudulent information? Is representative of tabular data in general, but does not represent a meaningful task. One can think of a meaningful task with this, but it was not originally used or collected for such a task; but label is wrong, higher/lower 50k is not relevant in such settings"

## Reference

Ron Kohavi, "Scaling Up the Accuracy of Naive-Bayes Classifiers: a Decision-Tree Hybrid", Proceedings of the Second International Conference on Knowledge Discovery and Data Mining, 1996
