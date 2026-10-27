---
unique_name: laduma_analytics_football_league_winners_prediction_challenge
name: laduma-analytics-football-league-winners-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/laduma-analytics-football-league-winners-prediction-challenge/data
source_row: 903
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a match-outcome classification of one masked league, a few hundred games, with in-match event tables that may hold the result.
- Source: Zindi competition with Laduma Analytics and Layer, 2022-06-06 to 2022-09-04, a rerun of the #ZindiWeekendz hackathon of 2022-06-03 (accuracy); as published: "collected over 3 years, following 23 teams in an African country. The player and team's names have been masked", event data (shots, passes, tackles, dribbles with X/Y), `Train.csv`, `Test.csv`, `train_game_statistics.csv`, `test_game_statistics.csv`; "The train set is two seasons and the test one season". Target: home win / lose / draw. Rows not checked (Zindi data needs a login).
- Use case: "predict the outcome of a football match, based on historical match and player data", for Laduma Analytics "to widen the types of services they offer"; no decision named, fit approximate; regime temporal (the source splits by season).
- Siblings and duplicates: `zindi_weekendz_laduma_analytics_football_league_winners_prediction_challenge` is the same data in the weekend hackathon (22 teams, accuracy), first published three days earlier: keep one record (PROV-4, PROV-8); other sport records: fifa, football_manager_important_matches, profb. External collections: none found.
- Papers and pages: competition page (https://zindi.africa/competitions/laduma-analytics-football-league-winners-prediction-challenge); no paper.
- Metric: log loss over the three outcomes, the leaderboard metric ("The evaluation metric for this challenge is the Log Loss", Evaluation page): deliberate (MET-4); inputs none.
- Risks for /add-dataset: the per-game statistics of the test games are in-match events (goals among the shots), so the outcome may be read off the match itself rather than predicted before kick-off (LEAK, USE); event tables to aggregate to one row per game (joins); a few hundred games over three seasons (TP-5, TP-9).
- Priority: gap - (sport, under Other), use case - (no decision named), source - (a competition page, masked data, no codebook found), shape - (few hundred games, event joins), risk - (in-match statistics).

A Zindi football challenge to predict league/match winners; the record has no detail, so it is unclear whether this is a per-match outcome classification (in scope) or a ranking/forecasting-of-future-results framing (out of scope). Sports outcome data is typically split across multiple match/team tables needing joins and often demands a temporal split to avoid leakage. Given the ambiguity it belongs in 2nd Tier pending inspection. A human must verify the exact target (match result vs league winner vs ranking), the temporal/grouped split needs, table structure, and size.
