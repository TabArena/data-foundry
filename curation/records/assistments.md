---
unique_name: assistments
name: ASSISTments
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
- Time-series (Classification)
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Temporal)
- Non-IID (Grouped)
- AI-Filled (Verify)
collections:
- TableShift
year: '2013'
domain: education
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/nicolaswattiez/skillbuilder-data-2009-2010
- https://new.assistments.org/
- https://tableshift.org/datasets.html#assistments
source_row: 853
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

ASSISTments skill-builder data (2009-2010), used in TableShift/Gardner for knowledge-tracing / affect-to-outcome prediction. The record itself flags an 'unclear predictive task' and uncertainty over whether grouped, temporal, or custom split is correct, and existing tags mark it 2nd Tier / Scientific Discovery. It is a real education dataset but the target definition and split regime are genuinely ambiguous (student-grouped, sequence/time-ordered logs). A human must pin down the exact target (e.g. end-of-year outcome vs next-correct), the correct split, and possibly recreate the table before it can be a Yes.

---

CC: ""Unsure, but might be this dataset: https://www.kaggle.com/datasets/nicolaswattiez/skillbuilder-data-2009-2010. Gardner uses grouped split - unsure whether that was right for the task as temporal or custom with a few new groups might be required.

Also an unclear predictive task""

Need to check the splits correctly and maybe recreate the data

## Reference

Pardos, Z.A., Baker, R.S.J.d., San Pedro, M.O.C.Z., Gowda, S.M., Gowda, S.M. (2013) Affective states and state tests: Investigating how affect throughout the school year predicts end of year learning outcomes. Proceedings of the 3rd International Conference on Learning Analytics and Knowledge, 117-124
