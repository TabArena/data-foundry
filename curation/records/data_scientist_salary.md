---
unique_name: data_scientist_salary
name: data_scientist_salary
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
- NLP (Text)
tags:
- Free Text (Short)
- New IID
- AI-Filled (Verify)
collections:
- TabSTAR
domain: technology & internet
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46664&sort=runs&status=active
- https://machinehack.com/hackathons/predict_the_data_scientists_salary_in_india_hackathon / openml_id=46664
source_row: 856
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

MachineHack 'Predict the Data Scientist's Salary in India' hackathon (OpenML id 46664), framing salary as a multiclass classification rather than regression. The curator flags that the free-text job-description fields are truncated to the first blurb, a data-quality defect, and that the task is dominated by string preprocessing, pushing it toward an NLP-heavy rather than representative tabular problem. It is a real-ish task but with notable caveats. A human should verify how much signal survives the text truncation, the post-cleaning size, and whether it is representative tabular ML or text-dominated; 2nd Tier for now.

---

Text descriptions are cut off after the first blurb! No full sentences? Salary prediction as a classification instead of a regression task. Otherwise seems like a real-ish task but mostly for string preprocessing
