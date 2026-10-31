---
unique_name: duolingo_spaced_repetition_recall
name: Duolingo spaced repetition learning traces (Settles and Meeder, ACL 2016)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2016'
domain: education
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.18653/v1/P16-1174
- https://doi.org/10.7910/DVN/N8XJME
- https://github.com/duolingo/halflife-regression
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 12.9 million Duolingo student-word practice traces (two weeks of 2013) with the share recalled in the session as the target, from the paper of the half-life regression model Duolingo deployed to schedule practice; education is thin, but the signal is weak (best MAE 0.128 against 0.175 for a constant) and the features are few.
- Source: Settles and Meeder, "A Trainable Spaced Repetition Model for Language Learning", ACL 2016 (doi 10.18653/v1/P16-1174); data on Harvard Dataverse (doi 10.7910/DVN/N8XJME, a 361 MB gzipped CSV), code on GitHub duolingo/halflife-regression (MIT licence for the code; the scout notes CC BY-NC 4.0 for the data, not checked). As published: "two weeks of Duolingo log data, containing 12.9 million student-word lesson and practice session traces" (Sec. 4.1); 12 columns `p_recall`, `timestamp`, `delta` (seconds since the word was last practised), `user_id`, `learning_language`, `ui_language`, `lexeme_id`, `lexeme_string`, `history_seen`, `history_correct`, `session_seen`, `session_correct` (README).
- Use case: the app predicts the probability that a learner recalls each word, which drives the strength meters and the choice of words to practise (Sec. 4.1: "Since the strength meters in Duolingo's interface are based on model predictions, we use MAE"; "Since our model is used to prioritize words for practice, we use AUC"); the paper deployed the model in "the production system" in two controlled user experiments (Sec. 4). Fit direct. Regime temporal: "using the first 90% for training and remaining 10% for testing" (Sec. 4.1), with learners on both sides of the cut.
- Siblings and duplicates: `assistments` (`TBD -> 2nd Tier`, knowledge tracing with per-attempt leaks) and `riiid_answer_correctness` (unscreened, next-answer correctness on EdNet): learner models on other platforms, no duplicate (searched Duolingo, spaced repetition, knowledge tracing). External collections: none found.
- Better data: from the gap scout for education; no further search this round.
- Papers and pages: the ACL paper (text read, Secs. 3 and 4, Table 2); the Dataverse record; the GitHub README (`evaluation.r` computes MAE, AUC and Spearman correlation).
- Metric: the paper reports MAE, AUC and the half-life correlation "for a comprehensive comparison" (Sec. 4.1, Table 2), three with a reason each and no single criterion, so the fallback `rmse` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: `p_recall` is `session_correct` / `session_seen`, so both go (LEAK); the target is a share of a few exercises, mostly 1 (training mean 0.859, Table 2); a weak signal (the best AUC 0.538, Table 2; TP-2, keep if real); `lexeme_id` has a high cardinality and `lexeme_string` is a morphological tag string; 12.9M rows need a cap; data from 2013; the decision is a prioritisation of words, which the curator may read as ranking (SEL-9), while the task as published is a per-word recall regression.
- Priority: gap + (education), use case + (the paper names the deployed uses), source + (ACL paper, Dataverse and code), shape + (12.9M traces, categorical and numeric, temporal, learners), risk - (a weak signal and few features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for education.
- as published: about 13 million student-word lesson traces x 12 columns: p_recall, timestamp, delta since last practice, user_id, learning and UI language, lexeme id and tag, history_seen, history_correct, ...; target: p_recall, the share of exercises in the session where the word was recalled correctly (session_seen and session_correct are its inputs and must be dropped); access: open.
- Why: a documented, open dataset of a company's deployed model, with the paper's metrics (MAE, AUC)
- Adds: a large learning-analytics regression task grouped by user with a time order; few features, and close to knowledge tracing (see the assistments record, kept as 2nd Tier), so a weaker hit
