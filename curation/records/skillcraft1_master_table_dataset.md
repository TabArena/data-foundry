---
unique_name: skillcraft1_master_table_dataset
name: SkillCraft1 Master Table Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
- Not Representative
tags:
- 2nd Tier / Scientfic Discovery
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

UCI SkillCraft1 (Thompson et al. 2013): StarCraft II telemetry aggregated into per-game engineered tabular features, with LeagueIndex (player skill league) as the usual target, already a TabArena Reject / 2nd-Tier. The curator notes the data is grouped by player (a player's league could leak across their games), the predictive task/target is somewhat unclear, and temporal nature needs checking. It is engineered tabular data so it is not raw non-tabular modality, but the leakage/grouping concerns make it borderline; a human must verify the grouping/leakage handling, the precise target, and whether a grouped split makes it a sound predictive task.

---

CC: "Game data, transformed to tabular with movement data. Samples are games - task is to predict in which league a game is (skill level). Likely grouped data (users are likely always in the same league which would be the target). I don't see what the task is. Also would need data analysis to determine the temporal nature. Groups of players could leak their league. 

Unclear target / predictive task"

## Reference

Thompson et al. (2013)
