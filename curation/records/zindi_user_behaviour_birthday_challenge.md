---
unique_name: zindi_user_behaviour_birthday_challenge
name: zindi-user-behaviour-birthday-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: technology & internet
required_split:
- '?'
problem_type: Binary Classification
source_links:
- https://zindi.africa/competitions/zindi-user-behaviour-birthday-challenge/data
source_row: 913
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a churn-like task on Zindi's own users (active next month or not), real and binary, but masked, spread over six activity tables and framed as a user-month panel, so a forecasting-like check comes first.
- Source: Zindi's own competition "Zindi User Behaviour Birthday Challenge", 2021-09-24 to 2022-01-23 (https://zindi.africa/competitions/zindi-user-behaviour-birthday-challenge, read through Zindi's page API); as published: "a subset of Zindi user activity. All variables have been masked"; `Users.csv`, `Competitions.csv`, `CompetitionPartipation.csv`, `Submissions.csv`, `Discussions.csv`, `Comments.csv`, `VariableDefinitions.csv`, and `Train.csv` ("a summarized table of the above activities ... it is recommended you pull features from the above tables"), `Test.csv` (user, month, year); target: "1 indicates that the user was active on Zindi in that month" (entered a competition, submitted, or posted in the forums).
- Use case: "help us establish and track our performance as a data science community and platform" (Description): Zindi would target inactive users; no decision named, fit approximate; regime temporal (user-months), users recur (grouped structure).
- Siblings and duplicates: none (grep birthday, user behaviour). External collections: none found.
- Papers and pages: the competition page; no paper.
- Metric: ROC AUC ("The evaluation metric for this competition is Area Under the Curve (AUC)", Evaluation tab), a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: a user-month panel where last month's activity is the obvious predictor: the TP-10 naive-profile test decides between SEL-10 and SEL-11; activity tables to aggregate up to each prediction month (joins, LEAK on dates); masked columns.
- Priority: gap 0 (technology & internet, binary, temporal not thin), use case 0 (no decision named), source 0 (masked, a competition page), shape + (six tables with dates), risk - (forecasting-like panel, heavy joins).

This Zindi 'user behaviour birthday challenge' record has only a name and data link, with no comments describing the target. Based on the name it concerns user-behaviour modeling, which could be a legitimate classification/regression but might also be a recommendation or engagement-prediction task that is out of scope. There is too little information to decide the task type, target, modality, or size. A human must open the source to determine the target and protocol; provisionally 2nd Tier.
