---
unique_name: assistments
name: ASSISTments
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
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
- https://sites.google.com/site/assistmentsdata/datasets/2012-13-school-data-with-affect
source_row: 853
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 3: TableShift defines a target (next answer correct, held-out schools), but it is a knowledge-tracing log where most per-attempt columns are known only after the answer, and the curator's CC calls the task unclear.
- Source: ASSISTments (Heffernan's group, WPI), the 2012-13 school-year data with affect predictions, on the ASSISTments data site; as published: one problem log per row (user, problem, assignment, skill, start/end time, `correct`, `attempt_count`, `hint_count`, `first_action`, `ms_first_response`, averaged affect predictions); TableShift reports 2,667,776 rows. The Kaggle link in the record is the 2009-2010 skill-builder set, a different year: TableShift says "We use the open-source ASSISTments 2012-2013 dataset".
- Use case: the tutor (or teacher) deciding whether a student has mastered a skill or needs another problem; TableShift: "the process of deploying ASSISTments at a new school"; fit approximate (the source's own decision is a mastery rule, sequence models are the field's tool); regime grouped by school (TableShift: about 700 training schools, 10 held out) or temporal by student history.
- Siblings and duplicates: none in `curation/records/`; external collections: TableShift (`assistments`), knowledge-tracing benchmarks (ASSIST2012 in DKT, SAKT and pyKT).
- Papers and pages: Feng, Heffernan, Koedinger (2009), UMUAI 19:243-266 (the platform); Wang, Heffernan, Heffernan (2015), LAK (the affect detectors); Pardos et al. (2013), LAK (the record's reference); Gardner, Popovic, Schmidt (2023), TableShift, NeurIPS D&B.
- Metric: none deliberate found; TableShift reports accuracy (in-domain and out-of-domain) for every task, a habit (MET-6), and knowledge tracing reports AUC; so the fallback `roc_auc`.
- Risks for /add-dataset: `attempt_count`, `hint_count`, `bottom_hint`, `first_action`, `ms_first_response`, `end_time` describe the same attempt and leak `correct` (LEAK); the affect columns are detector outputs over the same clip; the target needs binarising (the site: "1 = correct, <1 = Incorrect"); 2.7M rows of a sequence (`Time-series (Classification)` stays as a concern); the old `No Good Target  / Scientific Discovery` marker stays until the curator settles the task.
- Priority: gap + (education and grouped regime thin), use case - (approximate), source + (ASSISTments documents the columns), shape + (2.7M rows, mixed types, grouped), risk - (leaking per-attempt columns, unclear target).

ASSISTments skill-builder data (2009-2010), used in TableShift/Gardner for knowledge-tracing / affect-to-outcome prediction. The record itself flags an 'unclear predictive task' and uncertainty over whether grouped, temporal, or custom split is correct, and existing tags mark it 2nd Tier / Scientific Discovery. It is a real education dataset but the target definition and split regime are genuinely ambiguous (student-grouped, sequence/time-ordered logs). A human must pin down the exact target (e.g. end-of-year outcome vs next-correct), the correct split, and possibly recreate the table before it can be a Yes.

---

CC: ""Unsure, but might be this dataset: https://www.kaggle.com/datasets/nicolaswattiez/skillbuilder-data-2009-2010. Gardner uses grouped split - unsure whether that was right for the task as temporal or custom with a few new groups might be required.

Also an unclear predictive task""

Need to check the splits correctly and maybe recreate the data

## Reference

Pardos, Z.A., Baker, R.S.J.d., San Pedro, M.O.C.Z., Gowda, S.M., Gowda, S.M. (2013) Affective states and state tests: Investigating how affect throughout the school year predicts end of year learning outcomes. Proceedings of the 3rd International Conference on Learning Analytics and Knowledge, 117-124
