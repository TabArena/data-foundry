---
unique_name: law_school_admission_bianry
name: law-school-admission-bianry
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Ethical Issue
tags:
- 2nd Tier / Scientfic Discovery
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

OpenML d/43889, a 1991 survey of US law-school students (the well-known law-school/LSAC fairness dataset) with race as a feature. The curator flags it as a survey rather than a genuine predictive task, and it is already in TabArena Reject. It is widely used as an algorithmic-fairness benchmark with race/sensitive attributes, raising ethical-scope concerns, and it is a survey table rather than a real-world deployed prediction problem. A human could confirm the exact target (bar passage / admission), but the survey nature plus ethical sensitivity supports a No.

---

CC: "Survey among students attending law school in the U.S. in 1991. Race as feature. Not a predictive task."
