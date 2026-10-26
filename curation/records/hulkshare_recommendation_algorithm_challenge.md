---
unique_name: hulkshare_recommendation_algorithm_challenge
name: hulkshare-recommendation-algorithm-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: technology & internet
required_split:
- Custom
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/hulkshare-recommendation-algorithm-challenge/discussions
source_row: 899
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: the proposed fast reject (SEL-9) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9): a recommendation challenge; the model scores songs so that "HulkShare [can] rank its songs and recommend the best content".
- Source: Zindi, Hulkshare Recommendation Algorithm Challenge (2022-02-03 to 2022-05-01, 516 participants), data by Hulkshare Limited. As published: Train.csv (10 MB) and Test.csv keyed by song `Vid` and `Session_id`, plus ~9 GB of per-session listening frames (each song cut into 1,000 frames; play, pause, skip, rewind) and a play-count file; target: whether the song has a high likes-to-views ratio.
- Use case: Zindi: "How does a platform recommend good content without input from a user"; the decision is the ranking of songs for recommendation; the Zindi problem type is "Collaborative Filtering".
- Siblings and duplicates: none among `curation/records/`; external collections: none found.
- Papers and pages: the Zindi page (via the API); winners' write-ups not read.
- Metric: RMSE on the target (Zindi Evaluation page), a leaderboard metric.
- Also: the release is raw session logs that need heavy aggregation (`Needs extensive data wrangling`).
- Reject check (AI, 2026-10-22): does not stand. The task is not user-item recommendation. The unit is one song (Vid), the target is that song's observed likes-to-views ratio, scored by RMSE, and the features are its aggregated listening sessions: "predicts whether the song has a high number of likes to views (listens) since the song was uploaded" (Zindi Data Description, https://zindi.africa/competitions/hulkshare-recommendation-algorithm-challenge). There are no user-item pairs and no ranking metric. Downstream ranking is the use of the prediction, as in many in-scope tasks, so SEL-9 rests on the competition's title and its 'Collaborative Filtering' tag, not on how the prediction is made.
- For /add-dataset: TBD -> 2nd Tier, priority 2. The add stage must check: (1) the time window. If likes and views are counted over the same 6 months as the frames, it may be a look-back (SEL-6) or a target leak through Num_sessions (views are the target's denominator, LEAK). (2) Whether the target is a continuous ratio or a 0/1 high-ratio flag. (3) The licence: Zindi rules say the data is 'sole property of Zindi and the competition host' with no redistribution (house rules on shipping). (4) The wrangling: 9 GB of per-session frames to aggregate per song (`Needs extensive data wrangling`). (5) Download access (login).

Zindi 'recommendation algorithm' challenge whose task is to predict whether a streamed song is liked from viewing patterns. This is a music-recommendation / implicit-feedback task, which is out of scope (RecSys/ranking). The record also notes gigabytes of raw data requiring heavy feature engineering. It fails the out-of-scope-task criterion and is impractical without extensive wrangling. No.

---

predict if a song on a streaming platform is liked by looking at viewing patterns

Gigabytes of raw data - requires a lot of feature engineering
