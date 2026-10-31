---
unique_name: lahman_mlb_salaries
name: Lahman Baseball Database, Salaries table joined with the prior season's Batting statistics
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Website
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://sabr.org/lahman-database/
- https://search.r-project.org/CRAN/refmans/Lahman/html/Salaries.html
- https://cran.r-project.org/package=Lahman
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the salary task of `baseball_hitter` on 26,428 player-seasons of 1985-2016 instead of 263 hitters of one year, from a documented source; but salaries follow contract status and multi-year deals more than last season's statistics, and the table stops in 2016.
- Source: the Lahman Baseball Database (SABR, https://sabr.org/lahman-database/); Salaries table (R package Lahman, 2022 version): "A data frame with 26428 observations on the following 5 variables" (yearID, teamID, lgID, playerID, salary); "There is no real coverage of player's salaries until 1985", and the package vignette "Team Payroll and the World Series" says additions to the table were discontinued after 2016 (read in a search snippet). It joins on playerID and yearID to Batting, Pitching and Fielding (the prior season's statistics) and People (birth year, debut date).
- Use case: a front office or a player's agent sets or argues a salary from the player's record (salary arbitration compares the statistics of comparable players); the source names no use; fit approximate, because a salary of year t was often fixed by a contract signed years earlier and pre-arbitration players earn near the minimum whatever they did. Regime temporal by season (32 seasons, a drifting market), with players repeated across seasons.
- Siblings and duplicates: `baseball_hitter` (StatLib Hitters, 263 hitters, 1987 salaries; Lennart `TBD -> 2nd Tier`, `Outdated`: "Very old and likely outdated task"); `nba_player_stats_salaries_2000_2025` (another sport's salaries, a candidate of this run). Lahman is another source, not a duplicate (PROV-4); `lahman_hall_of_fame` and `lahman_team_seasons_runs` use other tables (PROV-7). External collections: none found.
- Better data: found as better data for `baseball_hitter`; no further search this round.
- Papers and pages: the Lahman documentation and its payroll vignette; no paper that defines the prediction task was read.
- Metric: none found (the SABR page, the R documentation), so the fallback `rmse`; a salary's error is relative to its size, which may argue for `rmsle` on dollars by context (MET-11, the diamonds precedent), the curator's call; inputs none.
- Risks for /add-dataset: features only from seasons before the salary year (same-season statistics are not known when the salary is set; LEAK); contract status (service time, free agency, multi-year deals) is not in the data and only partly derivable from the debut date; nominal dollars over 32 seasons (a year feature or deflation, MET-3); joins across four tables and players traded mid-season (several team rows per year); pitchers and hitters need different statistics.
- Priority: gap 0 (domain Other, regression and temporal are not thin), use case 0 (none named), source + (a maintained, documented database), shape + (26,428 player-seasons over 32 seasons), risk - (contract mechanics outside the data, joins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `baseball_hitter`.
- as published: Salaries: 26,428 player-seasons x 5 columns (yearID, teamID, lgID, playerID, salary), 1985-2016; joins on playerID/yearID to Batting, Pitching, Fielding and People (birth year, debut) for ...; target: Player's annual salary (USD) for the season; access: open (CSV/SQL/Access download; earlier releases CC BY-SA 3.0).
- Why: Same task as the StatLib Hitters data (1987 opening-day salary of 263 hitters from 1986 and career statistics, Sports Illustrated + Baseball Encyclopedia): salary from prior-season and career batting statistics
- Adds: About 100 times the rows (26,428 player-seasons vs 263), 32 seasons instead of one (a temporal split by year is possible), pitchers too; traceable maintained source. Caveat: no salaries after 2016, and salary is in nominal dollars (needs a year feature or deflation)
