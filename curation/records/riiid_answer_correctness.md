---
unique_name: riiid_answer_correctness
name: Riiid Answer Correctness Prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Kaggle
year: '2020'
domain: education
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/riiid-test-answer-prediction
- https://github.com/riiid/ednet
- https://arxiv.org/abs/1912.03072
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: Riiid's Kaggle competition (2020-21, ROC AUC) on whether a student of its tutoring app answers the next question correctly, about 100 million logged interactions; a large education task with a deliberate metric, but a knowledge-tracing log whose signal sits in user and question ids and the answer history, the setting in which `assistments` stays `2nd Tier`.
- Source: Kaggle featured competition "Riiid Answer Correctness Prediction" ("Track knowledge states of 1M+ students in the wild"), by Riiid Labs, launched 2020-10-05, closed 2021-01-07, 3,406 teams, USD 100,000 (Kaggle API). Files (Kaggle API): `train.csv` (5.85 GB), `questions.csv` (296 KB), `lectures.csv` (10 KB), `example_test.csv`, and the `riiideducation` time-series API that served the hidden test in order. The row and student counts in the Assessment below (about 101 million interactions, about 394,000 students) and the column list (timestamp, user_id, content_id, content_type_id, task_container_id, user_answer, answered_correctly, prior_question_elapsed_time, prior_question_had_explanation) were not read here. Related release: EdNet (Choi et al., AIED 2020, arXiv 1912.03072; 784,309 students, 131,441,538 interactions over more than two years of the Santa app, CC BY-NC 4.0), the same company's earlier public log of the same app; whether the competition rows overlap it is unknown (PROV-6 question).
- Use case: the tutoring app picks the next question or lecture from the student's estimated knowledge state, predicted as the chance of a correct answer; Riiid's own aim as a company, fit approximate (the competition page's wording was not read; Kaggle pages do not render). Regime temporal with users as groups: the hidden test was served in time order through the time-series API, and is commonly described as continuing known users' histories and adding new users (not read here).
- Siblings and duplicates: `assistments` (`TBD -> 2nd Tier`, `No Good Target / Scientific Discovery`, `Time-series (Classification)`: a 2012-13 knowledge-tracing log in TableShift, with per-attempt columns known only after the answer), for which this was found; `duolingo_spaced_repetition_recall` (unscreened, recall of words in Duolingo lessons). Another source, not a duplicate (PROV-4). External collections: none found.
- Better data: found as better data for `assistments`; no further search this round.
- Papers and pages: the competition (Kaggle API metadata and file list); EdNet (arXiv 1912.03072). The top solutions (sequence transformers over the answer history and gradient boosting on engineered history features, as commonly reported) were not read.
- Metric: `roc_auc` from the source: the competition's evaluation metric is "Area Under Receiver Operating Characteristic Curve" (Kaggle API `evaluationMetric`), a leaderboard choice (MET-4); inputs none.
- Risks for /add-dataset: the raw table holds ids, a timestamp, the question's container and two lagged columns, so every useful feature is built from the user's earlier answers and the question's success rate; LEAK-34 allows a known entity's own history under a temporal split, but TP-10's second leg asks whether the top solutions were tabular models on point-in-time features and not lags of the target, and the field's tool is a sequence model (`Time-series (Classification)`), with the user-by-question structure of a recommender (SEL-9 to weigh); `user_answer` is the answer itself and goes (LEAK-10); lectures are rows without a target (USE-7); 100 million rows need a cap and a per-user time order; the competition rules govern use of the data (a note, EV-4).
- Priority: gap + (education is thin, 3 accepted), use case 0 (the company's aim, not read from the page), source + (a featured competition with a stated metric), shape + (about 100 million interactions with user and time structure), risk - (a sequence-model task whose features are lags of the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `assistments`.
- as published: train.csv 5.8 GB, about 101 million interactions (question answers and lecture views) of about 394,000 students (counts as commonly cited, not read); questions.csv (13.5k questions with skill tags), ...; target: answered_correctly (0/1) for the next question of a student; access: registration (Kaggle competition rules); EdNet open under CC BY-NC 4.0.
- Why: Same task as assistments in TableShift (is the next answer correct, knowledge tracing), same unit (a student's answer to a question)
- Adds: About 40 times more rows and 2017-2019 data against 2012-13; the competition columns are known before the answer by design (prior_question_elapsed_time and prior_question_had_explanation lag one step), unlike assistments' attempt_count, hint_count and ms_first_response; a deliberate leaderboard metric (ROC AUC). Same ...
