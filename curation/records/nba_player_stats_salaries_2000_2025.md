---
unique_name: nba_player_stats_salaries_2000_2025
name: NBA Player Stats and Salaries 2000-2025
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2025'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ratin21/nba-player-stats-and-salaries-2000-2025
- https://github.com/edwinjeon/NBA-Salary-Prediction
- https://www.basketball-reference.com
- https://hoopshype.com/salaries/players/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: real per-game statistics with each season's pay for 10,473 player-seasons 2000-2025, but a season's pay was mostly fixed by a contract signed before that season's statistics existed, so the table supports a look back more than a pay decision.
- Source: Kaggle upload `ratin21`, "NBA Player Stats and Salaries 2000-2025" (dataset id 7580884, file of 2025-06-03, CC0), built by the author's script in github.com/edwinjeon/NBA-Salary-Prediction (created 2025-05-13; "Full scrapping script can be found at my GitHub Repository"), statistics from Basketball-Reference and salaries from HoopsHype (the record's links). As published: one CSV, 10,473 rows x 31 columns (`Player`, `Salary`, `Year`, `Pos`, `Age`, `Team`, games, minutes and per-game box-score statistics; counted on the repository's copy of the file), 117 to 540 player-seasons a year and few before 2006 (153 in 2000, 117 in 2005).
- Use case: the repository's aim is to "predict NBA player salaries for 2025-2026 season based on traditional per-game statistics" and to "explore how traditional stats correlate to player compensation"; no actor or decision. The decision that exists, a front office pricing a free agent's next contract from past statistics, needs contract signings (year, length, value) rather than season pay; fit approximate at best. Regime temporal by season or grouped by player.
- Siblings and duplicates: `nba_2k20_player_dataset` (`No`, `AHDS`: game ratings) is the record this was found for; the pay precedents are `baseball_hitter` (`TBD -> 2nd Tier`), `fifa` (`No`) and `lahman_mlb_salaries` (this run); `nba_players_2016_2019` (`No`) and `nba_draft` (`TBD -> 2nd Tier`) are other NBA tables. No other record names this upload. External collections: none among the records.
- Better data: found as better data for `nba_2k20_player_dataset`; no further search this run.
- Papers and pages: the Kaggle page and the GitHub README; no paper.
- Metric: none found (Kaggle page, README); the fallback `rmse`, the target likely shipped as log salary (MET-3, MET-8); inputs none.
- Risks for /add-dataset: the label's timing: a season's pay comes from an earlier contract while the features describe the same season (USE-3; lag the statistics a season at least); rookie-scale and minimum salaries follow the collective bargaining agreement's scales by draft slot and experience (SEL-5 for those rows); prorated pay of short contracts moves with games played (a 6-game player paid 73,153 in 2025); nominal dollars under a rising salary cap (a year feature or the cap share); thin salary coverage before 2006; player names as the only identifier.
- Priority: gap 0 (sports, regression, temporal not thin), use case 0 (none named), source 0 (a student's scrape of two sites, script public), shape + (10,473 rows, 31 columns with position and team), risk - (the label's timing and the pay scales): 1.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `nba_2k20_player_dataset`.
- as published: player-seasons 1999-2000 to 2024-25 (26 seasons), per-game stats (PTS, AST, REB, STL, BLK, age, position, team) and salary in USD, one CSV of 1.46 MB, CC0; rows not counted; target: season salary (USD); access: open.
- Why: the 2k20 table pairs real salaries with game ratings; this is the same salary target with real performance statistics in place of the game's ratings (fits only if the record's target is salary, not the 2k rating)
- Adds: real features, 26 seasons instead of one game edition, a grouped (player) or temporal split; weak precedent: fifa (No) and baseball_hitter (2nd Tier) for player pay tasks, and contract timing makes salary partly lagged
