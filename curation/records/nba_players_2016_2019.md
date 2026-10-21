---
unique_name: nba_players_2016_2019
name: NBA PLAYERS 2016-2019
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Tiny Data
collections:
- TabSTAR
original_source: Kaggle
year: '2019'
domain: Other
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/davra98/nba-players-20162019
- https://www.openml.org/search?type=data&id=43653&sort=runs&status=active
v2_path: datasets/_dev/tabarena-v0pt2/nba_players_2016_2019/dataset.py
source_row: 789
type_adapter_id: curation-record-v1
---

## Comments

Contains: https://www.kaggle.com/datasets/noahgift/social-power-nba

"Fake IID" by using only the last season for each player

Need to figure out which split / subset of the data to use

**Assessment (AI, 2026-10-07):** Valid; added as a grouped regression (`datasets/_dev/tabarena-v0pt2/nba_players_2016_2019/`). Target: the source's All-Star score, 0.5 fan rank + 0.25 player rank + 0.25 media rank (data card; the NBA's formula). In 2017-18 and 2018-19 the shipped `Score` adds the ballot size plus one (113-147) to the rank of every player without player or media votes. Recomputed from the file's ranks, those seasons equal the NBA's official weighted scores (pr.nba.com result tables, all 958 matched rows). Split: grouped by player (660 players, 295 in all three seasons). The statistics cover the whole season, past the January vote. TabSTAR's target `Rk` is basketball-reference's alphabetical row number.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap + (domain social science), use case -, source -, shape +, no known risk. Grouped social-science regression with the target repaired to match official NBA scores; a stand-in task with season-long features past the vote.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes, and the changes are in the definition: the prediction point stated as the vote's close with the end-of-season statistics and `team` kept under LEAK-11 (both measured to weaken the signal), last season's score added as `prev_score` (grouped R^2 0.744 to 0.760), the grouped split named a fallback from temporal, the 185 stale pageview copies masked, and a note that the score ranks the whole ballot. The earlier assessment's "no known risk" is wrong: the prediction point and the split are stand-ins (fit approximate). Open for the curator: the split and the "too few periods" amendment, the target over the whole ballot, box-score statistics, the pageview re-pull. Priority 3: gap + (domain social science), use case - (the actor is our example, fit approximate), source - (a student upload on Kaggle, no paper), shape +, risk 0 (no leak shown; the open issues are weighing calls and a repairable column).

CC (2026-10-21, Lennart): option (a) of the cross-dataset item on tasks with too few periods: the closest regime that keeps the rows, tagged as forced from temporal, with the cost measured against the valid windows (SPLIT-8 amended).

**Assessment (AI, 2026-10-21):** tagged `ForcedGroupedFromTemporal`. Cost: the one valid window (train 2016-18, test 2018-19) scores untuned LightGBM R^2 0.745 against 0.744 grouped (0.766 against 0.760 with prev_score), same order of model families. REVIEW.md issue 2 settled.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — A Kaggle dataset upload with no task or metric; the All-Star score target is our construction from the NBA's weighting of the fan, player and media vote ranks, so no source metric exists; a continuous score gives rmse.

## Reference

Kaggle
