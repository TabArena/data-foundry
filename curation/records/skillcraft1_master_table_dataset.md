---
unique_name: skillcraft1_master_table_dataset
name: SkillCraft1 Master Table Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
- Not Representative
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2013'
domain: Other
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5161N
source_row: 810
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's doubt (CC: "Unclear target / predictive task"; TabArena Reject) is kept and the verdict `TBD -> 2nd Tier` left as it is; priority 1. A counter-argument on the use case and the grouping for the curator.
- Source: UCI 272 (doi 10.24432/C5161N), Thompson, Blair, Chen and Henrey (2013), "Video game telemetry as a critical tool in the study of complex skill learning", PLoS ONE 8(9): e75129. As published: 3,395 rows, `GameID` ("Unique ID number for each game"), the target `LeagueIndex` (Bronze to Professional, coded 1-8, ordinal), self-reported Age, HoursPerWeek, TotalHours, and 15 per-timestamp telemetry rates (APM, hotkey use, perception-action cycles, action latency, units made); all numeric.
- Use case: the paper studies how skill differs across leagues (a discovery aim). A decision that fits is placement: a matchmaking service assigns a new player a league from their play; that use case is written by the curation, not the source (USE-1, fit approximate). Regime IID: the CC fears several games per player, but the paper says "From each respondent we gathered a replay file" and "we have only a single game from each participant" (3,360 players, 55 professionals from public sources), so no player group can leak a league.
- Siblings and duplicates: none among the records. External collections: not checked.
- Metric: the paper fits pairwise two-league conditional inference forests and reports a "classification rate" per pair against a baseline (e.g. Bronze-Gold 82.32% vs 77.81%), accuracy with no costs, a habit (MET-5, MET-6), so the fallback.
- **Counter-argument (AI):** the target is clear (the league the ladder assigned) and the grouping concern does not hold (one game per player), so this is an IID ordinal task with a plausible placement use case; what stays open is the use case, which the source does not state. Note that Professional players (league 8) lack the self-reported fields. The curator has the call.
- Priority: gap - (domain Other, regression), use case - (curation-written), source + (paper and UCI page), shape - (3,395 rows but all numeric, no structure), risk - (the curator's unclear-task doubt; the use case is ours).


UCI SkillCraft1 (Thompson et al. 2013): StarCraft II telemetry aggregated into per-game engineered tabular features, with LeagueIndex (player skill league) as the usual target, already a TabArena Reject / 2nd-Tier. The curator notes the data is grouped by player (a player's league could leak across their games), the predictive task/target is somewhat unclear, and temporal nature needs checking. It is engineered tabular data so it is not raw non-tabular modality, but the leakage/grouping concerns make it borderline; a human must verify the grouping/leakage handling, the precise target, and whether a grouped split makes it a sound predictive task.

---

CC: "Game data, transformed to tabular with movement data. Samples are games - task is to predict in which league a game is (skill level). Likely grouped data (users are likely always in the same league which would be the target). I don't see what the task is. Also would need data analysis to determine the temporal nature. Groups of players could leak their league. 

Unclear target / predictive task"

## Reference

Thompson et al. (2013)
