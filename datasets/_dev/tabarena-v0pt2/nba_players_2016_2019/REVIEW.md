# nba_players_2016_2019

**Outcome:** added. One row per NBA player and season (2016-17 to 2018-19), target the All-Star score (regression),
grouped by player; the 2017-18 and 2018-19 scores are recomputed with the NBA's formula. Ship with concerns: the
season statistics run past the January vote (issue 3).

**Main points:** The target is recomputed and matches the NBA's official scores in all 958 matched rows. The season
statistics run past the vote, so the prediction point is the season's end.

**Record fields that disagree with the definition:**

- `domain`: record `Other`, definition `social science`.

**Record judgment:** valid with concerns: the shipped target is inconsistent across seasons (issue 1), the split
(issue 2), the feature window (issue 3) and stale pageview values (issue 7).

**Issues for Lennart:**

1. **Target fixed for 2017-18 and 2018-19 (accept the recomputation?).** The NBA's own tables now confirm it.
   - Evidence: in these seasons the shipped `Score` adds the cell's ballot size plus one (113-147) to the player and
     media rank of every player without votes in that category. A cell is season x conference x ballot position.
     - The rule reproduces all 972 shipped values.
     - In the 2017-18 West frontcourt the ballot's last player (Amile Jefferson, fan rank 146) is not in the file.
       There the constant is the file's largest fan rank plus two.
   - The file's own `PRank`/`MRank` are the NBA's ranks.
     - Recomputed from them, the two seasons equal the official weighted scores for all 958 file rows that my parse
       matched by name (the verifier: 960 of 960). The shipped `Score` matches 28.
     - Official sources: pr.nba.com 2018 and 2019 result pages and PDFs, formula "(Fan Rank * 2 + Player Rank + Media
       Rank)/4".
   - 2016-17 follows the formula for all 436 rows, with one rank per cell for players without votes. The NBA
     published only separate fan, player and media lists for 2017 (official.nba.com).
   - The shift raises 921 of 972 scores by 28.2-73.6 points. Mean shipped score by season: 42.4 / 93.6 / 87.1.
   - Models trained on 2016-17 score R² -0.95 to -1.07 on the shipped 2017-18 values, and 0.68-0.73 on the recomputed
     ones.
   - Implemented: 2017-18 and 2018-19 recomputed with the formula from the file's ranks, rounded to one decimal as the
     source rounds 2016-17. The official values are quarters, and the rounding moves them by at most 0.05.
     2016-17 values kept.
   - Alternatives:
     - (a) The shipped `Score` as is: R² ~0.77 with `season` as a feature, but the target's scale differs by season.
     - (b) Only 2017-18 and 2018-19 with the shipped values (972 rows).

2. **Split: grouped by player, or IID?**
   - The real use is a new season with mostly known players, i.e. a temporal split by season. Three seasons cannot
     give three windows with half the rows in training; only 2018-19 has that.
   - Implemented: grouped by the source's `Player_ID`.
     - The source itself kept one season per player "for a problem of indipendent observations".
     - Players recur: 295 in 3 seasons, 158 in 2, 207 in 1. A player's score carries over (Spearman 0.78 / 0.80
       between consecutive seasons).
   - Numbers, untuned 3 x 3 folds, random against grouped:
     - LightGBM 0.769 / 0.751, random forest 0.715 / 0.695, ridge 0.716 / 0.700.
     - The newest season held out (the real use): 0.747 / 0.737 / 0.697.
     - The source's last-season subset (660 rows, IID): 0.66-0.71.
   - Alternative: IID on all rows (warm start). A test player's other seasons, later ones included, would then be in
     training. Your hidden-group rule says the split follows who the new rows are, and here they are mostly known
     players; I chose grouped because a random split also trains on the future.

3. **The statistics cover the whole season, past the vote (option (a) implemented; (b) is your call).**
   - 25 of the 34 features (games, games started, minutes and the 22 other per-game statistics) are whole-season
     values. The regular season ends in April and the vote closes in mid-January.
     - By the vote's close a player had played a median 54% of the season's games.
     - `team` is the end-of-season team: of the 87 rows with a team of the other conference, 82 moved after the
       vote's close, 4 before it, and 1 had not played before it.
   - It is a mismatch, not a leak. The same statistics as of the vote's close predict better.
     - Grouped 5 x 3 folds, R² at the close against the whole season: LightGBM 0.772 against 0.741 (paired -0.031,
       SE 0.004); random forest 0.694 against 0.684 (-0.010, SE 0.002); ridge 0.703 against 0.684 (-0.019,
       SE 0.004).
     - The shipped features give 0.742, the same as the rebuilt full-season ones.
   - Implemented (a): the stated prediction point is now the end of the regular season. The task explains the January
     vote from the season, and every feature is known at that point. The numbers above are in the first
     `curation_comments` bullet.
   - Alternative (b): rebuild the 25 statistics and `team` as of the vote's close from box scores, as a second raw
     input. The stated point would then be the vote and the task the real forecast.
     - The verifier's box scores: Kaggle `nathanlauga/nba-games` (`games.csv`, `games_details.csv`). It covers 2004
       to December 2020 and was scraped from stats.nba.com through the `nba_api` endpoints; its licence is
       "unknown".
     - 1,397 of 1,408 rows match by name; 43 rows have no game before the vote.
     - The vote-close dates it used (16 Jan 2017, 15 Jan 2018, 21 Jan 2019) are not stated on the NBA result
       pages; I did not confirm them.

4. **Target choice.** Implemented the source's goal, the All-Star score. Other targets in the file:
   - `Play` (played in the All-Star Game): 73 positives, 19-28 per grouped test fold. LightGBM AUC 0.973, and
     points per game alone 0.966: close to one feature.
   - log `Salary` (the uploader's suggested alternative, 1,346 rows): grouped R² 0.632. A salary is set by contracts
     signed before the season.

6. **Metadata choices.**
   - `year = "2019"`: the Kaggle upload; the data covers 2016-17 to 2018-19.
   - Licence noted: CC0 on Kaggle; the merged Social Power NBA data, which gives the 2016 pageviews, is
     CC BY-NC-SA 4.0.

7. **Stale pageview values (mask the copies?).**
   - 185 rows of 2017-18 (123) and 2018-19 (62) repeat an earlier season's `mean_views` of the same player, and 7 more
     later-season rows hold a 366-day (2016) mean: 192 of 856 later-season values.
     - Example: Carmelo Anthony's rows hold the 2016 mean, 4,679, in all three seasons. The Wikimedia API gives 6,292
       for
       2017 and 6,145 for 2018.
   - Several of the 120 rows under 20 views a day count a redirect title instead of the article. Example:
     T.J. McConnell has 2.8 a day for `T.J._McConnell` against 287 for `T._J._McConnell` in 2016.
   - No value is later than the vote, so none leaks.
   - Implemented: kept as shipped, and the comment bullet rewritten to say so.
   - Alternative: mask the 185 exact copies. A copy is a value equal to an earlier season's value of the same player;
     masking is deterministic from the raw file. Grouped LightGBM R² changes by -0.005 (SE 0.003); dropping the
     column changes it by -0.038 (SE 0.004). The redirect rows cannot be told apart in the file.
