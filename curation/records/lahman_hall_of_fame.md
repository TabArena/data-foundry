---
unique_name: lahman_hall_of_fame
name: Lahman Baseball Database (version 2025), HallOfFame table joined with People/Batting/Pitching/Fielding career statistics
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
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://sabr.org/lahman-database/
- https://search.r-project.org/CRAN/refmans/Lahman/html/HallOfFame.html
- https://cran.r-project.org/package=Lahman
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a traceable, maintained source for the Hall-of-Fame task of `baseball` (every ballot since 1936, with the election year), but no decision rests on the prediction, and the ballot rows carry the vote counts that decide the label.
- Source: the Lahman Baseball Database, created by Sean Lahman (free online since the mid-1990s), now published by SABR (https://sabr.org/lahman-database/: version 2025, released 2026-01-02, "complete major league batting and pitching statistics back to 1871"; CSV, SQL and Access downloads; annual updates by Bryan Walko). As published (R package Lahman, 2022 version): HallOfFame is "A data frame with 4323 observations on the following 9 variables": playerID, yearID ("Year of ballot"), votedBy (BBWAA or a committee), ballots, needed, votes, inducted (Y/N), category (Player, Manager, Pioneer/Executive, Umpire), needed_note; it joins on playerID to People, Batting, Pitching, Fielding, Awards and AllstarFull.
- Use case: someone forecasts whether a candidate is elected on a ballot from his career record (an analyst, the memorabilia market); the source names no actor or decision, and the vote is itself the decision, so the fit is approximate. Regime temporal by ballot year (the CC on `baseball` asks for the date); players repeat across ballots (up to 10-15 years on the BBWAA ballot), so a split by election year keeps a player's earlier ballots in training.
- Siblings and duplicates: `baseball` (OpenML 185, Simonoff 2003, 1,340 players; Lennart `TBD -> 2nd Tier`, `Missing source information`: "very imbalanced ... date information could also be relevant ... task might be trivial or better modeled by deterministic rules"): the same task from another source (PROV-4), not a duplicate. `lahman_mlb_salaries` and `lahman_team_seasons_runs` take other tables of the same database for other tasks (PROV-7). External collections: none found (the web search budget was used up).
- Better data: found as better data for `baseball`; no further search this round.
- Papers and pages: the Lahman documentation (R refman pages HallOfFame, Salaries, Teams); Hall-of-Fame prediction papers in the Journal of Quantitative Analysis in Sports (Young et al. 2008, a neural network; Freiman 2010, random forests; Mills and Salaga 2011, tree ensembles), cited from memory, not opened.
- Metric: none found (the SABR page, the R documentation; the JQAS papers not read), so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: `votes`, `ballots`, `needed` and `needed_note` are the vote that decides `inducted` and never become features (LEAK); the unit must be fixed, per ballot or per player (USE-5); committee elections of long-retired players (`votedBy`) and the non-player categories are other processes to filter; career statistics must be cut at the ballot year; factors that drive votes (the steroid era, the character clause) are outside the data; a few inductees per year among dozens of candidates, and milestone rules (3,000 hits, 500 home runs) are the CC's `Trivial` worry to probe (TP-4).
- Priority: gap 0 (domain Other is never thin), use case 0 (no actor named), source + (a maintained database with documentation), shape + (4,323 dated ballot rows with joined career statistics), risk - (outcome columns on the ballot rows, joins across tables, repeated players).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `baseball`.
- as published: HallOfFame: 4,323 ballot rows x 9 columns (playerID, yearID, votedBy, ballots, needed, votes, inducted, category) in the 2022 version, elections since 1936; career stats from the ...; target: Inducted into the Hall of Fame (Y/N), per player or per ballot; access: open (CSV/SQL/Access download; earlier releases CC BY-SA 3.0, check the 2025 readme).
- Why: Same target (Hall of Fame membership) and the same kind of features (career batting/fielding statistics) as OpenML 185 (Simonoff 2003, 1,340 players); different source, so its own record, not a version
- Adds: Covers every candidate and election through the latest release (vs a 2003 snapshot), adds pitchers, ballot year (a temporal split by election year, which the record's comment asks for) and vote shares; traceable, maintained publisher (the record is marked 'Missing source information'). scout_01 proposed the Teams ...
