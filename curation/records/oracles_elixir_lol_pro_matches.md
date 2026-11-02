---
unique_name: oracles_elixir_lol_pro_matches
name: Oracle's Elixir League of Legends professional match data (yearly files)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Website
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://oracleselixir.com/tools/downloads
- https://www.kaggle.com/datasets/barthetur/league-of-legends-2024-competitive-game-dataset
- https://www.kaggle.com/datasets/lauffing/oracles-elixir-league-of-legends-pro-play-data
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: every official professional League of Legends game of a season, with the gold, experience, CS and kill state at 10 and 15 minutes and the result; a traceable, dated version of the task of `league_of_legends_diamond_games_first_15_minutes`, with no published task or decision behind it.
- Source: Oracle's Elixir (Tim Sevenhuysen), yearly match-data files compiled from Riot's official esports match data (the scout's account; oracleselixir.com returned 403 here, so the years offered, the definitions page and the terms were not read). As published (preview of the Kaggle mirror barthetur/league-of-legends-2024-competitive-game-dataset, its 2024 file as of 2024-02-13, read 2026-10-31): 12,276 rows x 123 columns, 1,023 games from 1 January to mid-February 2024, 12 rows per game (five players and one team row per side, `position` top/jng/mid/bot/sup/team); columns `gameid`, `datacompleteness` (complete 10,020 rows, partial 2,244, reparse 12), `url`, `league`, `year`, `split`, `playoffs`, `date`, `game`, `patch`, `side`, player and team ids, `champion`, `ban1` to `ban5`, `gamelength`, `result`, end-of-game totals (kills, dragons, barons, towers, gold, damage, vision), and the snapshots `goldat10`, `xpat10`, `csat10`, `killsat10` and so on with their `opp_` and `diff` versions at 10 and 15 minutes. The second mirror (lauffing) holds 2020-2024 xlsx files of about 25 MB each.
- Use case: an in-play bookmaker or a bettor prices the match winner at the 15-minute mark, or a team analyst judges how decisive an early lead is (the scout's; Oracle's Elixir names no decision, so the use case is ours); fit approximate; regime temporal, because games are dated and the game changes with each patch; teams recur, so grouping by team is a question inside the temporal task.
- Siblings and duplicates: `league_of_legends_diamond_games_first_15_minutes` (Lennart `TBD -> Yes` with `AHDS`: "Technically real data, but not a real predictive task", "akin to predicting NFL or other sport game things") is ranked solo-queue play, another source and population, not a duplicate (PROV-4); the curator's doubt about the task applies here too. No other esports record (grep: oracle, esport, league_of_legends). External collections: none found.
- Better data: found as better data for `league_of_legends_diamond_games_first_15_minutes`; no further search this round.
- Papers and pages: the two Kaggle mirrors; no paper read (the web search budget was used up).
- Metric: none found (no competition or paper defines the task; the Kaggle pages read, the site blocked), so the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: one row per game, not per player or team: pair the two team rows or keep one side, so a game never sits on both sides of a split (LEAK-16 to LEAK-21); keep only what is known at minute 15 (the 10 and 15 minute snapshots, picks, bans, side, league, patch, date) and drop `gamelength`, the end-of-game totals and the `first*` objectives that can fall after minute 15 (LEAK-10); rows marked `partial` (18% of the preview) may lack the snapshots; the terms of use are unread (the Kaggle mirror says CC BY-NC-SA 4.0; noted only, EV-4).
- Priority: gap 0, use case 0 (ours), source + (a named compiler with game ids and match URLs), shape + (about 1,000 games in six weeks of 2024, several seasons, dated), risk - (the curator's open doubt on the task, leaky end-of-game columns, partial rows).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `league_of_legends_diamond_games_first_15_minutes`.
- as published: every official competitive LoL game of a year, 12 rows per game (10 players, 2 teams), over 100 columns including goldat10/15, xpat10/15, csat10/15, golddiffat10/15, xpdiffat10/15, killsat15 and the ...; target: result (team won the game), from the early-game state at 10 or 15 minutes; access: open.
- Why: The same target (which side wins) and the same kind of features (gold, experience, CS, kills and objectives at minute 15) as the record's 48,651 diamond ranked games. Here they come from a named, maintained compiler instead of an untraced Kaggle scrape.
- Adds: Traceable provenance and a real decision (live betting markets on pro esports), more than ten seasons with date, patch and league for a temporal or league-grouped split, and the at-10 and at-15 snapshots. Trade-offs: professional play, not ranked solo queue, so fewer games per year than the record's 48,651. The terms ...
