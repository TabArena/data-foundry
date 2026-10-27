---
unique_name: turkiye_student_evaluation
name: Turkiye Student Evaluation
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
year: '2013'
domain: education
required_split:
- Grouped (NON-IID)
problem_type: Other
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5S02S
source_row: 811
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** agrees with the curator's `No` (CC line; `TabArena Reject`): no target that a decision needs.
- Source: UCI 262, donated 2013-08-31 by Ernest Fokoue and Necla Gunduz: "a total 5820 evaluation scores provided by students from Gazi University in Ankara (Turkey)", "28 course specific questions and additional 5 attributes": `instr` (3 instructors), `class` (13 courses), `repeat`, `attendance` (0-4), `difficulty` (1-5), Q1-Q28 Likert 1-5. UCI lists "Classification, Clustering" and names no target; no paper.
- Use case: none. Every column is answered by the student in the one post-course form, so predicting `difficulty`, `attendance` or the instructor from the other answers is a look at the survey, not a decision (SEL-3, SEL-7: answers of the same interview); the record's CC says the same. Regime would be grouped by instructor and course (only 3 and 13).
- Siblings and duplicates: none among `curation/records/` (grep Turkiye, student evaluation).
- Metric: none found (UCI page), so the fallback would apply.
- Counterpoint checked: education is thin (3 accepted), so a target here would fill a gap, but no candidate column is observed after or apart from the survey, so the gap does not change the verdict. The marker `No Good Target / Scientific Discovery` fits; `problem_type` `Other` matches.

UCI Turkiye Student Evaluation: ~5820 course evaluations with 28 Likert survey items plus instructor/course/attendance fields. As the CC comment notes, most features were collected in the same post-course survey as any plausible target, making it a scientific-discovery / no-clear-supervised-target dataset (it is commonly used for clustering, not prediction). It is also clustered/grouped by instructor and course. Given the lack of a meaningful, non-leaky predictive target, this should be rejected; a human could confirm there is no defensible target.

---

CC: "Scores from 5000 students related to courses; contains multiple instructors and courses and thus is clustered data

Many features were collected after the target in a survey after the course ended. Hence, this is a scientific discovery task
"
