---
unique_name: law_school_admission_bianry
name: law-school-admission-bianry
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Ethical Issue
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '1991'
domain: education
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/43889
source_row: 820
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the workbook note "Not a predictive task" holds for this OpenML cut; the `No` stands. Counter-argument on the markers only: `Ethical Issue` has no basis under SEL-1 (nobody asked that the data not be used; a race column is no ethical bar), the reason is the target.
- Source: OpenML 43889 (2022-05-30), "obtained from the R-package fairml", from the LSAC National Longitudinal Bar Passage Study (Wightman, 1998; students entering law school in 1991). As published here: 20,800 rows x 12 columns, target `ugpagt3`: "The response variable has been changed to a binary version: Whether ugpa is greater than 3."
- Use case: none: undergraduate GPA is known before admission, so nobody predicts it from LSAT and demographics (SEL-3, SEL-8: the mirror relabelled the data into a task of its own); regime IID.
- Siblings and duplicates: no other record of the LSAC data. External collections: fairml, the fairness literature (Kusner et al. 2017 counterfactual fairness used first-year average and bar passage).
- Papers and pages: Wightman 1998, LSAC research report; OpenML page.
- Metric: none; the fallback if ever revived.
- For the curator: the original study's bar-passage outcome is a different, possibly real task (a law school deciding on academic support); it would be a new record from the LSAC source, not this cut.

OpenML d/43889, a 1991 survey of US law-school students (the well-known law-school/LSAC fairness dataset) with race as a feature. The curator flags it as a survey rather than a genuine predictive task, and it is already in TabArena Reject. It is widely used as an algorithmic-fairness benchmark with race/sensitive attributes, raising ethical-scope concerns, and it is a survey table rather than a real-world deployed prediction problem. A human could confirm the exact target (bar passage / admission), but the survey nature plus ethical sensitivity supports a No.

---

CC: "Survey among students attending law school in the U.S. in 1991. Race as feature. Not a predictive task."
