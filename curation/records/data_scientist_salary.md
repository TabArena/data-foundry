---
unique_name: data_scientist_salary
name: data_scientist_salary
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
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

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a real 2018-2019 MachineHack task (salary band of an Indian data-science job posting), but every feature is a string and the job description is the main signal, so it sits at the edge of SEL-12.
- Source: MachineHack hackathon "Predict The Data Scientists Salary In India" (2018-2019; "a classification hackathon", Analytics India Magazine, 2019-01-24, https://analyticsindiamag.com/deep-tech/machinehack-winners-how-industry-mavericks-predicted-data-scientists-salary-and-won-big); used in Shi et al. 2021, "Benchmarking multimodal AutoML for tabular data with text fields" (arXiv:2111.02705), and uploaded to OpenML 46664 from that paper (2025-02-19). As published on OpenML: 15,841 rows (the competition train file had 19,802), 6 string features (`experience`, `job_description`, `job_desig`, `job_type`, `key_skills`, `location`), target `salary` with 6 bands, majority class 22.8%, 15,520 missing values.
- Use case: estimate the salary band of a posting from its text, skills and location (a job seeker or recruiter, not named by the source); fit approximate; regime IID (no posting date ships).
- Siblings and duplicates: no other record of this data (grep: 46664, salary in india). External collections: Shi et al. 2021 multimodal benchmark, TabSTAR.
- Papers and pages: the MachineHack page (not readable without login), Shi et al. 2021.
- Metric: none found (the MachineHack evaluation page could not be read; the AIM article names none; Shi et al. report accuracy for all classification sets, a habit), so the fallback `log_loss` (MET-8).
- Risks for /add-dataset: text-dominated (SEL-12, `NLP (Text)`): judge whether tabular models are competitive; the curator's note that descriptions are cut after the first blurb (as published, so a note rather than repairable damage, CLEAN); `experience` as a range string to parse; salary bands are ordered (a regression on band midpoints is not what the source asked).
- Priority: gap - (technology, multiclass, IID not thin), use case - (no actor named), source + (benchmark paper and OpenML description), shape + (about 16k rows, 6 features), risk - (text-dominated).

MachineHack 'Predict the Data Scientist's Salary in India' hackathon (OpenML id 46664), framing salary as a multiclass classification rather than regression. The curator flags that the free-text job-description fields are truncated to the first blurb, a data-quality defect, and that the task is dominated by string preprocessing, pushing it toward an NLP-heavy rather than representative tabular problem. It is a real-ish task but with notable caveats. A human should verify how much signal survives the text truncation, the post-cleaning size, and whether it is representative tabular ML or text-dominated; 2nd Tier for now.

---

Text descriptions are cut off after the first blurb! No full sentences? Salary prediction as a classification instead of a regression task. Otherwise seems like a real-ish task but mostly for string preprocessing
