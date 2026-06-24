---
unique_name: laduma_analytics_football_league_winners_prediction_challenge
name: laduma-analytics-football-league-winners-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: Other
required_split:
- '?'
problem_type: TBD
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

A Zindi football challenge to predict league/match winners; the record has no detail, so it is unclear whether this is a per-match outcome classification (in scope) or a ranking/forecasting-of-future-results framing (out of scope). Sports outcome data is typically split across multiple match/team tables needing joins and often demands a temporal split to avoid leakage. Given the ambiguity it belongs in 2nd Tier pending inspection. A human must verify the exact target (match result vs league winner vs ranking), the temporal/grouped split needs, table structure, and size.
