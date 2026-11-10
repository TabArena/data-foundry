---
unique_name: xuetangx_mooc_dropout
name: XuetangX MOOC dropout prediction (Understanding Dropouts in MOOCs, AAAI 2019; KDD Cup 2015)
checked_by:
- Myunghwan
data_foundry_status:
- 'DF: Suspended'
suggestion: TBD -> 2nd Tier
priority: 4
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- Revisit later
original_source: Website
year: '2019'
domain: education
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://ojs.aaai.org/index.php/AAAI/article/view/3825
- http://moocdata.cn/data/user-activity
- http://moocdata.cn/challenges/kdd-cup-2015
- https://biendata.com/competition/kddcup2015/
- https://www.kaggle.com/datasets/ramspimatiz7gmailcom/mooc-dataset-dropout-dataset
- https://www.kaggle.com/datasets/sst2023/kdd-cup-2015
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: XuetangX's course-dropout data from the platform team's AAAI 2019 paper, whose model was deployed to send retention messages, with the KDD Cup 2015 cut of the same platform; a large learning-analytics task in a thin domain, but the features have to be built from about 6 GB of event logs and the first publisher's download links are dead.
- Source: Feng, Tang, Liu, Zhang and Guan, "Understanding Dropouts in MOOCs", AAAI 2019 (read from the authors' PDF, keg.cs.tsinghua.edu.cn); data on moocdata.cn ("These files are the datasets used in the paper"): tracking logs 2015-08 to 2017-08; the "Dropout prediction dataset" (`train_log.csv`, `test_log.csv` with enroll_id, username, course_id, session_id, action, object, time; `train_truth.csv`, `test_truth.csv` with 1 dropout, 0 not); `user_info.csv` (gender, education, birth year); `course_info.csv` (start, end, course type, category); and the KDD Cup 2015 data. Table 2: 467,113 instructor-paced and 218,274 self-paced enrollments (372,088 and 205,988 dropouts) in 698 and 515 courses; Table 1 (KDD Cup): 200,904 enrollments, 159,223 dropouts, 112,448 users, 39 courses. Dropout: no activity in the 10 days after a 35-day history (paper) or a 30-day history (KDD Cup, "set to 30 days and 10 days respectively by the competition organizers"). The prediction dataset's rows were not counted (its truth files on the Kaggle mirror suggest about 200,000 enrollments, a subset of Table 2).
- Use case: the platform, a fixed time after a learner starts a course, decides whether its assistant sends a retention message (section "From Prediction to Online Intervention": "If a user's dropout probability is greater than a threshold, XiaoMu would send the user an intervention message", with an A/B test of three strategies). Fit direct. Regime temporal by course start, or grouped by course; users recur across courses; how the authors split train and test is not stated in what was read.
- Siblings and duplicates: `open_university_learning_analytics_dataset` (`Yes`, BeyondArena; the Open University's course outcomes, another platform and country, PROV-7); `upv_university_student_dropout`, `chile_school_dropout_mineduc` and `predict_students_dropout_and_academic_success` are degree or school dropout, other tasks. The KDD Cup 2015 data and the AAAI data are two cuts of one platform's logs with the same label (PROV-6): one record, and the curator picks one (the AAAI cut is larger and has user and course context). External collections: none found.
- Better data: found by the gap scout for education; no further search this round.
- Papers and pages: Feng et al. 2019 (code at github.com/wzfhaha/dropout_prediction); the KDD Cup 2015 page on moocdata.cn ("predict whether a user will drop a course within next 10 days based on his or her prior activities"; 821 teams per the paper); biendata's competition page could not be reached.
- Metric: Feng et al., Experiments: "The evaluation metrics include Area Under the ROC Curve (AUC) and F1 Score (F1)" (Table 4: CFIN 90.07 AUC and 92.27 F1 on KDD Cup, 86.40 and 90.92 on XuetangX), two side by side, so the fallback (MET-5); the KDD Cup 2015 leaderboard scored AUC per the record's earlier assessment (not re-read: biendata unreachable), the source metric for that cut (MET-4). Either way `roc_auc`; the deployed threshold is not given (MET-6); inputs none.
- Risks for /add-dataset: features are aggregates of the history window's logs (about 4.2 GB train and 1.9 GB test logs on the mirror), and every window must end at the history cut, since the label comes from the next 10 days of the same logs (LEAK-10); the first publisher's links (lfs.aminer.cn) redirect to the aminer.cn home page and the Kaggle mirrors are by unknown uploaders with licence "unknown": `ramspimatiz7gmailcom/mooc-dataset-dropout-dataset` (2025) has the four prediction files but neither `user_info.csv` nor `course_info.csv`, `sst2023/kdd-cup-2015` (2023) has the KDD Cup files; check them against the paper's counts (PROV-8, PROV-15); many enrollments per user and per course (grouping); dropout is 80% and 94% of enrollments, so the positive class is the majority.
- Priority: gap + (education has 3 accepted), use case + (deployed interventions, named in the paper), source + (the platform team's paper and data page), shape + (hundreds of thousands of enrollments, user and course groups, a time order), risk - (log aggregation; dead first-publisher links and mirrors without the context files).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for education.
- as published: Paper Table 2: 467,113 instructor-paced + 218,274 self-paced course enrollments (dropout 80% / 94%), 698 + 515 courses, 2015-08 to 2017-08 logs; KDD Cup 2015 subset (Table 1): 200,904 enrollments, ...; target: dropout: no activity on the course in the 10 days after a 30-day (KDD Cup) or 35-day (paper) history window; access: open (the first publisher's download links on lfs.aminer.cn now redirect to the aminer.cn home page; the same files are mirrored on Kaggle; the KDD Cup copy on biendata needs a login).
- Why: a real competition and paper on a task still done on every MOOC platform, with a deployed use and a metric (AUC, F1; the KDD Cup scored AUC); groups by course and user and a time order by course start
- Adds: a second, much larger learning-analytics dropout task next to open_university_learning_analytics_dataset, from another platform and country; mixed features once the logs are aggregated (activity counts, demographics, course category)

CC (2026-11-06, Myunghwan): Proceed to add-dataset qualification, explicitly requested after the screening explanation. Pursue the larger AAAI XuetangX release first; verify actual release coverage, prediction-time inputs and evaluation before final inclusion. No build or commit is authorized.

**Assessment (AI, 2026-11-07):** review panel (full): recommend shipping only after explicit curator acceptance of an approximate released-label task; disputed: source-window alignment and actual label maturity remain unverified (USE-5/8, LEAK-10, SPLIT-9/10); for the curator: issue 1. The acquired copy has 225,642 enrollments, 247 courses and 31 predictors; original-publisher byte equivalence and cohort selection are unverified. Native checks 0 errors, 1 unknown-license warning; model probes show signal but no-spread lacks tuned evidence. Full eleven-role panel includes the cold-editor check recorded in the final review. Priority 4: gap + (education), use case + (source retention contact), source + (platform paper/code), shape + (measured temporal interaction table), risk - (source clock/copy gaps and log aggregation).

**Assessment (AI, 2026-11-07):** review panel (focused): existing candidate rechecked and ready for the same final curator choice; disputed: actual source-window alignment and label availability remain unverified (USE-5/8, LEAK-10, SPLIT-9/10); for the curator: issue 1 unchanged. Fresh raw hashes, preserved labels, exact frame/scorer/splits and native 27-check result (0 errors, 1 license warning) confirm reuse of the dated probes and full panel; zero new model fits. Claim audit, mediation and cold editor found no new substantive issue. Priority 4: gap + (education), use case + (source retention contact), source + (platform paper/code), shape + (verified temporal interaction table), risk - (unchanged source-clock/copy gaps).

CC (2026-11-08, Myunghwan): Hold XuetangX. Good dataset, but we do not aggregate by default. Raw records are individual activities while the supplied dropout label belongs to a learner-course enrollment; constructing one tabular sample per enrollment requires aggregation and additional task design. This is not straightforward enough to pursue now. Defer inclusion; this is not a scientific rejection or a finding of demonstrated leakage.

**Assessment (AI, 2026-11-08):** Applied the curator's case-specific hold as `TBD -> 2nd Tier` / `DF: Suspended`, retaining the existing wrangling marker, priority and all exploratory definition/evidence. The earlier screening approval and panel recommendations remain history, superseded for current inclusion by this hold. Issue 1's source timing remains unaccepted, not resolved. The later checks found feasible identity-disjoint windows and a plausible inclusive-day explanation, not a curator-approved tabular representation. Suggested reopening: explicit curator reconsideration of a straightforward source-defined task table or expressly accepted aggregation design; this is operational guidance, not an additional quoted curator condition.

**Assessment (AI, 2026-11-08):** Draft-PR decision-only publication: the exploratory enrollment-aggregation definition, generated card, full panel and measurements are preserved locally, not included as an added dataset in this PR. No source activity row is treated as an independent labeled sample. The candidate remains held; no timing approximation or scientific inclusion is accepted. The official active claim was released and its mirror cleared on 2026-11-08.
