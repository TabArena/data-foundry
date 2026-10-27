---
unique_name: zindi_weekendz_laduma_analytics_football_league_winners_prediction_challenge
name: zindi-weekendz-laduma-analytics-football-league-winners-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Too Small
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
source_links:
- https://zindi.africa/competitions/zindi-weekendz-laduma-analytics-football-league-winners-prediction-challenge/data
source_row: 989
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: the first release of the Laduma Analytics match-outcome data, the same task as the later rerun `laduma_analytics_football_league_winners_prediction_challenge`; small, built from in-match events, and to be kept in one record only.
- Source: #ZindiWeekendz hackathon "Laduma Analytics Football League Winners Prediction Challenge" with Laduma Analytics and Layer, 2022-06-03 to 2022-06-05 (https://zindi.africa/competitions/zindi-weekendz-laduma-analytics-football-league-winners-prediction-challenge, read through Zindi's page API); as published: "collected over 3 years, following 22 teams in an African country. The player and team's names have been masked"; event data ("shots, passes, tackles, and dribbles ... X and Y coordinates"); "The train set is two seasons and the test one season"; `Train.csv`, `Test.csv`, `game_statistics.csv`, `VariableDefinitions.csv`; target per `Game_ID`: Home Win, Draw, Away Win.
- Use case: "predict the outcome of a football match, based on historical match and player data ... useful to Laduma Analytics to widen the types of services they offer"; no decision named, fit approximate; regime temporal (the source splits by season).
- Siblings and duplicates: `laduma_analytics_football_league_winners_prediction_challenge` (the rerun of 2022-06-06 to 2022-09-04, log loss, "23 teams", separate train and test game statistics; `TBD -> 2nd Tier`, priority 1): the same publisher and data, so keep one record (PROV-4); this page is the first publication (PROV-8), the rerun has the deliberate log-loss metric and the clearer files; the curator picks. Other sport records: fifa, football_manager_important_matches, profb. External collections: none found.
- Papers and pages: the competition page; no paper.
- Metric: accuracy ("The evaluation metric for this challenge is Accuracy", Evaluation tab) on hard labels; the rerun moved to log loss, which MET-8 would prefer; inputs none.
- Risks for /add-dataset: `game_statistics.csv` holds the match's own events (shots, goals), so the outcome may be read off the game rather than predicted before kick-off (LEAK, USE); event tables to aggregate per game (joins); about three seasons of one league, a few hundred games (TP-5, TP-9).
- Priority: gap 0 (sport, under Other), use case 0 (no decision), source 0 (masked, a weekend hackathon), shape - (few hundred games), risk - (in-match statistics, duplicate with the rerun).

This Zindi Weekendz challenge asks to predict football league match/winners outcomes, a sports-results prediction task. It could be framed as a genuine classification (win/draw/loss) but Zindi Weekendz datasets are typically very small and the task usually requires a temporal split since matches occur in sequence. The record provides no size, features, or exact target. A human must inspect dataset size, the target definition, and the split regime; provisionally 2nd Tier given likely small size.
