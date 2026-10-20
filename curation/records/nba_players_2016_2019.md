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

## Reference

Kaggle
