---
unique_name: nflverse_nfl_games_spreads
name: nflverse games / schedules table (games.csv with spread, total and moneyline per NFL game)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
original_source: Github
original_data_state: One Table
source_links:
- https://github.com/nflverse/nfldata/blob/master/data/games.csv
- https://github.com/nflverse/nfldata/blob/master/DATASETS.md
- https://cloud.r-project.org/web/packages/nflreadr/vignettes/dictionary_schedules.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a maintained table of every NFL game since 1999 (about 7,300 played, by the season schedules) with the spread, total and odds; a larger and documented stand-in for `chscase_foot`, but the margin against the market's line is close to noise by design, and the spread alone may match any model.
- Source: the nflverse `nfldata` repository (github.com/nflverse/nfldata, data/games.csv; first release year not found), documented in its DATASETS.md and in the nflreadr schedules dictionary. As published (header and last rows previewed, 2.19 MB): one row per game, 46 columns, seasons 1999 to the 2026 schedule (unplayed games have empty scores); `result`, "The number of points the home team scored minus the number of points the visiting team scored", "convenient for evaluating against the spread bets"; `spread_line` positive when the home team is favoured; `total_line`, moneylines and spread odds (empty in the 1999 rows), rest days, division game, roof, surface, temperature, wind, starting quarterbacks, coaches, referee and stadium. Neither page states a licence or where the lines come from.
- Use case: a bettor (or a sportsbook trader) decides before kick-off whether to bet a side against the spread; the dictionary's "evaluating against the spread bets" is the only hint, so the fit is approximate; regime temporal by season.
- Siblings and duplicates: `chscase_foot` (`TBD -> 2nd Tier`, priority 1; 526 games of 1989-91 from Chatterjee, Handcock and Simonoff's casebook, "Betting on professional football") and `profb` (`No`, SEL-3; StatLib scores and spreads of 1989-91 published for questions, not prediction): other sources and seasons, no duplicate. External collections: none found.
- Better data: found as better data for `chscase_foot`; no further search this round.
- Papers and pages: DATASETS.md; the nflreadr dictionary (cloud.r-project.org/web/packages/nflreadr/vignettes/dictionary_schedules.html).
- Metric: none found (DATASETS.md, the dictionary), so the fallback: `rmse` on the margin, or `roc_auc` on covering (MET-1, MET-8); a bettor acts on a hard pick against the odds, but the source fixes no threshold or cost (MET-6, MET-7); inputs none.
- Risks for /add-dataset: TP-4, the market's spread is the best public predictor of the margin, so one feature may match every model (`Trivial`), and against the spread the outcome is near a coin flip (TP-2 at best); drop every post-game column (scores, `total`, `overtime`; LEAK-10); the lines and starting quarterbacks are known only shortly before kick-off, so the prediction point decides which go in; where the lines come from is unstated (PROV-2); whether a betting task belongs in the benchmark is for the curator to weigh.
- Priority: gap 0, use case 0 (a hint, no actor named), source 0 (a community repository with a dictionary, the lines' origin unstated), shape + (about 7,300 games, mixed types, seasons), risk - (likely trivial through the spread).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `chscase_foot`.
- as published: NFL games, one row each, 46 columns, seasons 1999 to the current schedule; file 2.19 MB, roughly 7,000 played games (estimated from the file size, not counted).; target: result (home score minus away score; 'used to evaluate spread bets'), or whether the home team covers spread_line; access: open.
- Why: The same task as chscase_foot (NFL games, the result against the point spread, 1989-91) with features of the same kind known before kick-off: spread_line, total_line, moneylines, rest days, division game, roof, surface, temperature, wind, starting QBs, coaches. The StatLib sibling profb (same seasons, record verdict ...
- Adds: About 13 times the games (roughly 7,000 against 526), 26 seasons up to now instead of three seasons of 1989-91, the line and the odds as columns, maintained and documented (nflreadr dictionary). Risk unchanged: against the spread the outcome is near-noise by market design, so the margin (result) with the spread as a ...
