---
unique_name: happyforce_employee_churn
name: Daily Happiness and Employee Turnover (Happyforce app data)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2017'
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1145/3110025.3110132
- https://www.kaggle.com/datasets/harriken/employeeturnover
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: real employee turnover in 37 client companies of an engagement app, with a published churn model; the features are app logs that need a prediction date, and the label is a "no longer exists" flag.
- Source: Berengueres et al., "Happiness, an inside job? Turnover prediction using likeability, engagement and relative happiness", ASONAM 2017 (doi 10.1145/3110025.3110132); data from myhappyforce.com, released on Kaggle by J. Berengueres (harriken/employeeturnover, files dated 2019-09-20, DbCL-1.0; the card asks to cite Bebenroth and Berengueres 2020, IJHRDM 20(1):61-74). As published: four tables, `churn.csv` (323 KB), `votes.csv` (13 MB; a vote is the answer to "How happy are you at work today?" on four icons), `comments_clean_anonimized.csv` (16 MB), `commentInteractions.csv` (22 MB, likes and dislikes). `churn.csv` previewed: 4,847 rows (`employee`, `companyAlias`, `numVotes`, `lastParticipationDate`, `stillExists`), 4,806 distinct employee-company pairs, 37 companies, 1,174 rows with `stillExists` false, last participation from 2014 to 2017. The card: "The churn table contains when an employee churned (quit or was fired)"; "Out of 4,356 employees, 2,638 employees commented at least once".
- Use case: the HR team of a client company flags employees at risk of leaving and acts on retention; the card says "we developed a model that predicts which employees will churn" and states the goal "to help companies understand the causes so they can reduce the turnover rate". Fit approximate (engagement in one app; no pay, role or tenure). Regime grouped by company (37) or temporal on the participation dates, decided with the prediction point.
- Siblings and duplicates: `ibm_hr_analytics_employee_attrition_performance_employee_ibm_attrition` (`No`, AHDS: "This is a fictional data set created by IBM data scientists."); `wns_hr_employee_promotion` (another HR target); no other Happyforce record (`grep -il happyforce/harriken`). External collections: none found.
- Better data: found as better data for `ibm_hr_analytics_employee_attrition_performance_employee_ibm_attrition`; no further search this round.
- Papers and pages: the ASONAM 2017 paper (not read here: the full text sits in the ACM library and behind a Dropbox link on the card); the Kaggle card and its starter scripts (R "how-many-unlikes-it-takes-to-get-fired"; github.com/orioli/e3).
- Metric: the card reports "Precision@50 = 80% out of a test set with 116 churns, sample size N=2k", a headline number with k fixed for one test set (MET-5: a headline is not by itself a deliberate choice; under MET-7 k would have to be scaled to each fold). The paper's evaluation section was not read, so the fallback `roc_auc` until it is (MET-8). Inputs none.
- Risks for /add-dataset: the only churn date is the last participation, so features must stop at a prediction date before it, or the vote count and the recency of the last vote give the label away (LEAK, USE); `stillExists` false may also mark an account removed for other reasons (to check in the paper); four relational tables to aggregate per employee (`Needs extensive data wrangling`); 41 duplicated employee-company rows; the comments are free text, left out or reduced to counts.
- Priority: gap 0 (business and binary not thin), use case + (the card names the churn prediction and what it is for), source + (a peer-reviewed paper on a named app's data, documented on the card), shape + (4,847 employees in 37 companies, daily votes over about three years), risk - (the label timing and the prediction point must be built from logs).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ibm_hr_analytics_employee_attrition_performance_employee_ibm_attrition`.
- as published: 4,356 employees of the app's client companies; four tables: churn.csv (when an employee churned), votes.csv (daily happiness votes), comments_clean_anonimized.csv, commentInteractions.csv (likes, ...; target: employee churn (quit or was fired) from the churn table; access: open.
- Why: the same target and use case as the IBM record (will this employee leave), real and traceable to a peer-reviewed paper with a named data source; the satisfaction signal (daily happiness votes) is of the kind of the IBM satisfaction scores
- Adds: real employees instead of a fictional IBM table, about 3x the employees (4,356 vs 1,470). Caveats: relational logs that must be aggregated per employee up to a prediction date (needs extensive wrangling), features are app engagement rather than HR records (no pay, role, tenure), the label mixes quits and dismissals, ...
