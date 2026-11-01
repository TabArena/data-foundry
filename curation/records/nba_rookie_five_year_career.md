---
unique_name: nba_rookie_five_year_career
name: 'NBA Stats (1947-present): regular-season player and team data scraped from Basketball-Reference'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: Kaggle
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats
- https://www.basketball-reference.com/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a maintained compilation of Basketball-Reference's season and career tables from which the rookie five-year-career task of `basketball_c` can be rebuilt with every NBA rookie (4,897 players debuting through 2021, 2,291 of them with a span of five seasons or more), but the target is ours to build and the source states no task.
- Source: Kaggle upload by Sumitro Datta (`sumitrodatta`), "NBA Stats (1947-present)" (dataset id 1177523, CC0, updated monthly, files of 2026-04-13; first version date not read), "Regular Season Data from Basketball-Reference", built by the uploader's own scraping "in the mold of Lahman's Baseball Database" (Kaggle description). As published: 20 CSV files: player totals, per game, per 36 minutes, per 100 possessions, advanced, play by play and shooting (from 1997), season info, career info, award shares, all-star selections, end-of-season teams, draft pick history and team tables; player ids are Basketball-Reference slugs. `Player Career Info.csv` (read as a preview): 5,416 players with `from`, `to`, `debut`, height, weight, birth date, colleges and `hof`.
- Use case: none stated by the source (a statistics archive). The decision a five-year-career prediction fits is a team's call on a rookie-scale contract's option years after the first season (our reading); fit approximate (the span from `from` to `to` is not seasons played, and careers continue abroad). Regime temporal by debut season.
- Siblings and duplicates: `basketball_c` (`No`, `Data Quality Issue`: the Coursera rookie set, "Data problems and missing source information") is the record this was found for; `nba_draft` (`TBD -> 2nd Tier`) is another source; `nba_players_2016_2019` (`No`) and `nba_player_stats_salaries_2000_2025` (this run) also draw on Basketball-Reference, with other tasks (PROV-7). External collections: none among the records.
- Better data: found as better data for `basketball_c`; no further search this run.
- Papers and pages: the Kaggle page; Basketball-Reference's glossary for the statistics; no paper.
- Metric: none found (Kaggle page, the `basketball_c` record); the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: the target is built (`No Good Target (yet)` until the curator fixes the definition: span or seasons played, NBA only); rookies of the last five seasons have no outcome yet and go (SPLIT-9); only rookie-season statistics are features, since later seasons tell the career length (USE-3); joins of the season tables on player slug and season, with the combined rows of traded players to deduplicate; ABA and BAA seasons to exclude or flag; Sports Reference's terms on scraping (EV-4, noted only).
- Priority: gap 0 (binary, temporal not thin), use case 0 (none stated), source 0 (a documented compilation of a reference site, no publisher's paper), shape + (about 4,900 rookies, dozens of statistics, a time axis), risk - (a target to build, censoring, table joins): 1.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `basketball_c`.
- as published: 20 CSV files, including Player Totals (4.5 MB), Player Per Game, Advanced, Player Season Info and Player Career Info (first and last season per player), Draft Pick History; NBA 1950-present, BAA ...; target: Built: career of at least 5 seasons (from Player Career Info), predicted from the rookie season's statistics, as in the record; access: open (Kaggle download, login).
- Why: Same target and features as the record's Coursera/data.world rookie set (1,340 rookies 1980s-2015, rookie-season box score, 5-year career flag), which was rejected for data errors and an unclear source
- Adds: Every rookie since 1947 (several thousand), from a named primary source (Basketball-Reference player slugs as IDs), maintained to 2026, with advanced stats and draft position; the target must be built and recent rookies (debut after 2021) are censored. Caveats: a scrape (no licence stated on Kaggle; Sports ...
