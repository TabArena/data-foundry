---
unique_name: lahman_team_seasons_runs
name: Lahman Baseball Database, Teams table (version 2025)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- 2nd Tier / Scientific Discovery
original_source: Website
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://sabr.org/lahman-database/
- https://search.r-project.org/CRAN/refmans/Lahman/html/Teams.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the runs-scored regression of `moneyball` from its documented upstream (every MLB team season to 2025, raw counts instead of three rates), but runs scored against the same season's batting counts is close to an accounting identity, an explanation rather than a prediction someone acts on.
- Source: the Lahman Baseball Database (SABR, https://sabr.org/lahman-database/, version 2025 covering 1871-2025); Teams table (R package Lahman, 2020 version): 3,015 rows x 48 columns: yearID, lgID, teamID, franchID, divID, Rank, G, Ghome, W, L, DivWin, WCWin, LgWin, WSWin, R, AB, H, X2B, X3B, HR, BB, SO, SB, CS, HBP, SF, RA, ER, ERA, CG, SHO, SV, IPouts, HA, HRA, BBA, SOA, E, DP, FP, name, park, attendance, BPF, PPF and three team-id columns; version 2025 adds five seasons (not counted).
- Use case: the source states none. The Moneyball use (estimate the runs a roster will score from its players' rates before the season) needs the players' prior-season rates, which this table does not hold; with same-season counts the target is explained, not predicted (USE-2, SEL-3). Fit approximate at best; regime temporal by season if kept.
- Siblings and duplicates: `moneyball` (AI `TBD -> 2nd Tier`, priority 1, `No Good Target / Scientific Discovery`; Kaggle and OpenML 41021 from The Analytics Edge, 1,232 team seasons of 1962-2012 "gathered from baseball-reference.com"): the same quantity from another source (PROV-4), not a duplicate; the marker is carried over to treat like cases alike. `lahman_hall_of_fame` and `lahman_mlb_salaries` use other tables (PROV-7). External collections: none found.
- Better data: found as better data for `moneyball`; no further search this round.
- Papers and pages: the Lahman documentation; the sabermetric run estimators (Runs Created, linear weights) fit team runs from these counts almost exactly (general knowledge, not read), which is the `Trivial` worry.
- Metric: none found (the SABR page, the R documentation), so the fallback `rmse`; inputs none.
- Risks for /add-dataset: W, L, Rank, the title flags, RA, ER, ERA and attendance are same-season outcomes (LEAK); R is near-linear in the batting counts (TP-4 to probe; the CC on `moneyball`: "Linear model best in TabRepo"); 19th-century leagues and short seasons (1981, 1994, 2020) change the scale (filter, or a per-game target); about 3,100 rows.
- Priority: gap 0 (domain Other), use case 0 (none), source + (a documented database), shape + (about 3,100 team seasons over 150 years, temporal), risk - (a same-season identity, leaks).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `moneyball`.
- as published: Team seasons; Teams has 48 columns and 3,015 rows in the 2020 version (1871-2020); version 2025 covers 1871-2025, so roughly 3,100 team seasons (not counted). CSV, SQL and Access downloads.; target: R (runs scored by the team in the season), the same as Moneyball's RS; access: open.
- Why: The same target and features of the same kind: AB, H, 2B, 3B, HR, BB, SO, SB, CS, HBP, SF, from which OBP, SLG and BA follow, plus RA, W, L, league and park.
- Adds: About 2.5 times the team seasons (all of MLB history to 2025 against 1962-2012), 13 more recent seasons, the raw counts instead of three rates, a maintained source with a data dictionary. The same-season leak and near-linearity risks of the record stay.
