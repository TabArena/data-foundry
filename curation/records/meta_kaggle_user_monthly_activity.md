---
unique_name: meta_kaggle_user_monthly_activity
name: Meta Kaggle (Kaggle's public data on competitions, users, submissions, discussions)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Kaggle
domain: technology & internet
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/kaggle/meta-kaggle
- https://www.kaggle.com/datasets/kaggle/meta-kaggle-code
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: Kaggle's own daily dump of its public activity tables (users, competitions, teams, submissions, forums, notebooks), published for exploration; the monthly-activity target of `zindi_user_behaviour_birthday_challenge` would be ours to build, on a user-month panel that may reduce to each user's last month.
- Source: Kaggle, "Meta Kaggle" (kaggle/meta-kaggle, dataset id 9, updated daily; Apache 2.0 since August 2023, CC BY-NC-SA before): "Kaggle's public data on competitions, users, submission scores, code, and more", "derived from Kaggle's SQL database"; "This data is not a complete dump of our database. Rows, columns, and tables have been filtered out and transformed" (data card, read through the Kaggle API). As published: CSV tables of users, competitions, teams and memberships, submissions, forum topics and messages, notebooks and versions, datasets, achievements and followers, from 2010 on, 14.7 GB (the run's file listing, 2026-10-30); companion Meta Kaggle for Code. No target; `year` left empty (first release not dated).
- Use case: the parent's: at the start of a month the platform flags users likely to be inactive, for re-engagement, from their past activity. The source names no prediction ("Explore our public data", data card); fit approximate. Regime temporal (user-months), users recur.
- Siblings and duplicates: `zindi_user_behaviour_birthday_challenge` (`TBD -> 2nd Tier`, priority 1; Zindi's masked subset of its own platform, another source); no Meta Kaggle record (grep meta-kaggle). External collections: none found.
- Better data: found as better data for `zindi_user_behaviour_birthday_challenge`.
- Papers and pages: the data card; no paper predicting user activity from it found (one web search).
- Metric: none for this data; the Zindi challenge scored AUC on its own target, a stand-in here (MET-11), and the fallback is the same `roc_auc`.
- Risks for /add-dataset: the target and the user-month rows are ours (SEL-3, marker `No Good Target (yet)`); a forecasting-like panel: run TP-10 against each user's last month first (SEL-10, SEL-11); the undocumented filtering (deleted or private activity missing would look like inactivity); joins over 14.7 GB; user names and display names go.
- Priority: gap 0 (technology & internet, binary, temporal not thin), use case 0, source + (the platform's own release and data card), shape + (millions of users, dated tables), risk - (a target to build, a forecasting-like panel).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `zindi_user_behaviour_birthday_challenge`.
- as published: a set of activity tables, 14.7 GB in all (Kaggle API listing, 2026-10-30): Users.csv 2.7 GB (more than 10 million users already in 2022), Competitions.csv, Teams.csv 0.8 GB, TeamMemberships.csv 0.44 ...; target: not published: whether a user is active in a given month (joins a competition, submits, posts in the forums), to be built from the dated activity tables ...; access: open (Kaggle download with a free account), Apache 2.0.
- Why: same task as zindi_user_behaviour_birthday_challenge: monthly activity of members of a data-science competition platform from their own activity history, on the same table design (Users, Competitions, participation, Submissions, Discussions, Comments) that Zindi masked and released as a subset
- Adds: orders of magnitude more users and 16 years instead of a masked Zindi subset of about two years; unmasked, documented columns with real dates; the platform's own maintained release under Apache 2.0 instead of competition files under Zindi's no-redistribution rules. Caveats: the monthly target and the per-user ...
