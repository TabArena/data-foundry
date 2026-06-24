---
unique_name: turkiye_student_evaluation
name: Turkiye Student Evaluation
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
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

UCI Turkiye Student Evaluation: ~5820 course evaluations with 28 Likert survey items plus instructor/course/attendance fields. As the CC comment notes, most features were collected in the same post-course survey as any plausible target, making it a scientific-discovery / no-clear-supervised-target dataset (it is commonly used for clustering, not prediction). It is also clustered/grouped by instructor and course. Given the lack of a meaningful, non-leaky predictive target, this should be rejected; a human could confirm there is no defensible target.

---

CC: "Scores from 5000 students related to courses; contains multiple instructors and courses and thus is clustered data

Many features were collected after the target in a survey after the course ended. Hence, this is a scientific discovery task
"
