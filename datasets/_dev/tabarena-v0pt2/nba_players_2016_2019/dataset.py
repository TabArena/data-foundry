"""Curated dataset definition for `nba_players_2016_2019` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    TaskSummary,
    anonymize_ids,
    drop_columns,
)

TARGET = "all_star_score"

SHIFTED_SEASONS = ("2017-18", "2018-19")
"""Seasons whose shipped `Score` adds the ballot size plus one to the rank of players without votes."""

VOTE_COLUMNS = ["Fvot", "FRank", "Pvot", "PRank", "Mvot", "MRank"]
"""Fan, player and media votes and their ranks: the components of the score."""

# The file's names are R's `make.names` forms of basketball-reference's glossary (`X3P.` is 3P%): source -> ours.
RENAME = {
    "Player_ID": "player_id",
    "Pos1": "position",
    "Pos2": "second_position",
    "Age": "age",
    "Tm": "team",
    "G": "games",
    "GS": "games_started",
    "MP": "minutes_per_game",
    "FG": "field_goals_per_game",
    "FGA": "field_goal_attempts_per_game",
    "FG.": "field_goal_pct",
    "X3P": "three_pointers_per_game",
    "X3PA": "three_point_attempts_per_game",
    "X3P.": "three_point_pct",
    "X2P": "two_pointers_per_game",
    "X2PA": "two_point_attempts_per_game",
    "X2P.": "two_point_pct",
    "eFG.": "effective_field_goal_pct",
    "FT": "free_throws_per_game",
    "FTA": "free_throw_attempts_per_game",
    "FT.": "free_throw_pct",
    "ORB": "offensive_rebounds_per_game",
    "DRB": "defensive_rebounds_per_game",
    "TRB": "total_rebounds_per_game",
    "AST": "assists_per_game",
    "STL": "steals_per_game",
    "BLK": "blocks_per_game",
    "TOV": "turnovers_per_game",
    "PF": "personal_fouls_per_game",
    "PTS": "points_per_game",
    "Salary": "salary",
    "mean_views": "wikipedia_daily_views",
    "Season": "season",
    "Conference": "conference",
    "Role": "ballot_position",
    "Score": TARGET,
}


def documented_score(df: pd.DataFrame) -> pd.Series:
    """The score as the data card defines it: 0.5 x fan rank + 0.25 x player rank + 0.25 x media rank.

    Rounded to one decimal, half to even, as the source rounds its 2016-17 values.
    """
    return (0.5 * df["FRank"] + 0.25 * df["PRank"] + 0.25 * df["MRank"]).round(1)


def next_season(season: pd.Series) -> pd.Series:
    """The label of the season after (`2016-17` -> `2017-18`)."""
    start = season.str[:4].astype(int) + 1
    return start.astype(str) + "-" + (start + 1).astype(str).str[2:]


def repeats_earlier_season(df: pd.DataFrame, key: str, season: str, value: str) -> pd.Series:
    """True where `value` equals the value of the same `key` in an earlier season (a stale copy)."""
    rows = df[[key, season, value]].reset_index()
    earlier = df[[key, season, value]].dropna(subset=[value])
    pairs = rows.merge(earlier, on=[key, value], suffixes=("", "_earlier"))
    stale = pairs.loc[pairs[f"{season}_earlier"] < pairs[season], "index"]
    return pd.Series(df.index.isin(stale), index=df.index)


def last_name_order(names: pd.Series) -> pd.Series:
    """Position of each name when sorted by last name, then first name (basketball-reference's table order)."""
    parts = names.str.split(" ", n=1)
    key = parts.str[1].fillna("") + " " + parts.str[0]
    return key.str.lower().rank(method="first")


class NbaPlayers20162019(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How high will an NBA player rank in a season's All-Star vote, given his season?",
        use_case=(
            "For example, when the All-Star vote opens and before the NBA publishes the first fan returns, a team's "
            "marketing staff estimates where its players will rank from their statistics, salary, popularity and last "
            "season's vote, to decide whom to campaign for."
        ),
        row="One NBA player in one regular season, 2016-17 to 2018-19 (1,408 rows of 660 players).",
        predicted=(
            "The player's All-Star score for the season, half his rank in the fan vote plus a quarter each of his "
            "ranks in the player and media votes, within his season, conference and ballot position; lower is better. "
            "It ranks the whole ballot, so most of the error comes from players far below the 2 or 3 starters."
        ),
        known=(
            "The prediction point is the vote's close in mid-January. Known then: age, position, conference, ballot "
            "position, salary, last season's score and Wikipedia page views of the calendar year the season starts. "
            "The statistics (games, minutes, points, rebounds, assists, shooting) and the team are end-of-season "
            "values, which predict the score less well than values at the vote's close."
        ),
        split=(
            "Whole players are held out with all their seasons. Held-out players are mostly veterans whose other "
            "seasons are hidden, not new players. The real use, a new season of mostly known players, needs a split "
            "by season, which three seasons cannot give; the grouped split is the fallback and scored the same as "
            "holding out the newest season."
        ),
        changes=(
            "We recompute the score of 2017-18 and 2018-19 with the NBA's formula, as the shipped one penalised "
            "players without player or media votes; drop the votes and ranks behind it and whether the player played "
            "in the game; add last season's score; and blank the page views that repeat an earlier season's value."
        ),
        fit="approximate",
        fit_reason=(
            "The vote closes in mid-January, but 25 of the 35 features are the whole season's; statistics as of the "
            "vote's close predict better (R^2 0.772 against 0.741). The fan returns the NBA publishes during the vote "
            "are missing, and last season's score is missing for 2016-17. Held-out players stand in for a new season "
            "of mostly known players."
        ),
    )

    # Dataset
    unique_name = "nba_players_2016_2019"
    year = "2019"
    domain = "social science"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/davra98/nba-players-20162019"
    license = "CC0-1.0 (Kaggle data card)"
    data_tags = ("ForcedGroupedFromTemporal",)
    download_description = """
        We download the only file of the Kaggle dataset, nba_final.csv (1,408 rows, 45 columns, dated 2019-12-04;
        sha256 06455e5a0b3efebfc9257e7e71d687bc1aad3558d14b73bb186872d85d310eb5).

        kaggle datasets download davra98/nba-players-20162019 && unzip nba-players-20162019.zip && rm nba-players-20162019.zip
        mkdir -p local-data-warehouse/nba_players_2016_2019 && mv nba_final.csv local-data-warehouse/nba_players_2016_2019/

        OpenML 43653 (https://data.openml.org/datasets/0004/43653/dataset_43653.pq) holds the same rows and columns;
        only 51 player names lost their non-ASCII letters there (the names are dropped).
    """
    bibtex = r"""
        @misc{davra2019nbaplayers,
          author = {davra98},
          title = {{NBA} {PLAYERS} 2016-2019: Some stats of {NBA} players},
          year = {2019},
          howpublished = {\url{https://www.kaggle.com/datasets/davra98/nba-players-20162019}},
          note = {Kaggle dataset}
        }
    """
    curation_comments = """
        We start with nba_final.csv, the only file of the Kaggle dataset "NBA PLAYERS 2016-2019" (davra98): one row per NBA player and season, 2016-17 to 2018-19 (1,408 rows, 660 players), with season statistics, salary, Wikipedia pageviews and All-Star votes.

        - Prediction point: the close of the All-Star vote (mid-January; 25 Dec to 21 Jan in 2019, starters public on 24 Jan). The 25 season statistics (`games`, `games_started` and the per-game values) and `team` are measured at the end of the regular season, after the outcome, and kept (LEAK-11): they weaken the signal. The same statistics as of the vote's close, rebuilt from box scores, predict the score better (grouped LightGBM R^2 0.772 against 0.741, paired SE 0.004, 5 x 3 folds).
        - Target: `all_star_score` (`Score`). Within each season, conference and ballot position the players are ranked by their fan, player and media votes, and the score is 0.5 x fan rank + 0.25 x player rank + 0.25 x media rank (data card; the NBA's own rule). Lower is better. The score ranks the whole ballot (92-140 players per cell): 92% of rows score above 10 and carry 77% of its variance, so RMSE is driven by non-contenders. A label is relative to its cell, and the cell (season, conference, ballot position) is in the features.
        - Target fixed for 2017-18 and 2018-19 (`documented_score`): the shipped `Score` adds the ballot size plus one to the player and media rank of players without such votes, which makes the seasons incomparable. We recompute both seasons with the formula from the file's own ranks, rounded to one decimal as the source rounds 2016-17; they then equal the NBA's official scores for all 958 rows matched by name (decision table). 2016-17 follows the formula and keeps its values; its unranked players get the same rank (players voted in the cell plus one), so the three seasons share one scale (mean target 42.4 / 45.8 / 44.7).
        - Added `prev_score`: the player's score of the season before, public before the vote opens (USE-10: the previous outcome of a known player). It is missing for all of 2016-17 (436 rows) and for players without a row in the previous season; the missing values come from the design and say nothing about the player. It stays on the same side of every grouped split as its row. Grouped LightGBM R^2 0.744 -> 0.760 (SE 0.004).
        - Dropped: the votes and ranks the score is computed from (`Fvot`, `FRank`, `Pvot`, `PRank`, `Mvot`, `MRank`); `Play` (played in the game, decided after the vote); `Rk` (basketball-reference's alphabetical row number; decision table); `Player.x` (the name).
        - `Player_ID` becomes the group column `player_id`, anonymized.
        - Grouped by player, a fallback from the temporal split the use case implies: most players appear in several seasons, and a player's score carries over (decision table). A split by season needs three test windows with half the rows or more before each, and of three seasons only 2018-19 has that (66%). Tagged ForcedGroupedFromTemporal (SPLIT-8, Lennart, 2026-10-21): the one valid window (train 2016-18, test 2018-19) scores untuned LightGBM R^2 0.745 against 0.744 grouped (0.766 against 0.760 with `prev_score`), with the same order of model families, so the grouped split under-rates real use by about 0.01.
        - Renamed: the per-game statistics after basketball-reference's glossary; `conference` `Est` to `East`; `ballot_position` `Back` and `Front` to `guard` and `frontcourt`. `season` is a category.
        - `team` is the team at the end of the season, of the other conference in 87 rows (82 of them traded after the vote). Kept under LEAK-11: masking the team on those 87 rows raises grouped R^2 0.744 -> 0.751 (paired +0.007, SE 0.0015), so the post-vote value weakens the signal. Trades within a conference are not measured.
        - `wikipedia_daily_views` (`mean_views`) is the mean daily pageviews over the calendar year in which the season starts, before the vote (checked against the Wikimedia API to 2 decimals). 185 rows of the later seasons repeat an earlier season's value of the same player, a stale merge: masked (`repeats_earlier_season`; grouped R^2 -0.005, SE 0.003). Left as shipped: 7 later-season rows that hold a 2016 mean without being an exact copy, and rows that count a redirect title instead of the article (undercounts the file cannot tell apart).
        - Missing values stay missing (`salary`, `wikipedia_daily_views`, the shooting percentages of players without an attempt). No duplicate rows.
        - Note: TabSTAR (via OpenML 43653) takes the alphabetical `Rk` as its target and keeps the vote columns as features, so that version has no task.
        - Note: the merged pageviews of noahgift/social-power-nba are CC BY-NC-SA 4.0.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    grouping = Grouping(
        on="player_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a player (basketball-reference's player id), with one row per season he played in 2016-17 to 2018-19 (660 players, 1 to 3 rows). The source treats a player's seasons as dependent: "for a problem of indipendent observations we took only the last seasons' observation for each player" (Kaggle data card, Context). A model predicts a player's All-Star score of a season from that season's statistics, salary and popularity; holding out players keeps all seasons of a test player out of training, including his later ones, which a model applied to a new season cannot have seen. Each row is one prediction, made from that row alone.
        """,
    )

    # One string without code indentation: `splits_comment` is stored as written (it is not dedented).
    splits_comment = (
        "Grouped 3-fold cross-validation by player with the recommended repeats: all seasons of a player stay on one "
        "side, so no split trains on a test player's other seasons. This is a fallback from temporal: the real use, "
        "a new season with mostly known players, is a temporal split by season, but of three seasons only the newest "
        "has half the rows or more before it, and the protocol needs three such windows. Holding out players scored "
        "close to holding out the newest season (untuned LightGBM R^2, 3 x 3 folds: 0.751 against 0.747; a rerun on "
        "the shipped splits: 0.744 against 0.745), with the same order of model families; a random split scored "
        "0.769 (rerun 0.759)."
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "nba_final.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # Target: in 2017-18 and 2018-19 the shipped score shifts the rank of players without player or media votes
        # by the ballot size plus one; recompute it with the documented formula from the file's own (official) ranks.
        shifted = df["Season"].isin(SHIFTED_SEASONS)
        assert df.loc[shifted, ["FRank", "PRank", "MRank"]].notna().all().all()
        df["Score"] = df["Score"].mask(shifted, documented_score(df))
        # Last season's score of the same player, public before the vote opens (USE-10); missing for 2016-17 and for
        # players without a row in the season before.
        last = df[["Player_ID", "Season", "Score"]].rename(columns={"Score": "prev_score"})
        last["Season"] = next_season(last["Season"])
        df = df.merge(last, on=["Player_ID", "Season"], how="left", validate="1:1")
        # Pageviews: mask the exact copies of an earlier season's value of the same player (stale merges).
        df["mean_views"] = df["mean_views"].mask(repeats_earlier_season(df, "Player_ID", "Season", "mean_views"))
        # The votes and ranks are the score's components; `Play` follows from the vote; `Rk` is the alphabetical
        # row number of basketball-reference's table; `Player.x` is the name.
        df = drop_columns(df, ["Rk", "Player.x", *VOTE_COLUMNS, "Play"])
        df = df.rename(columns=RENAME)
        # The group column: hide the names in basketball-reference's ids (`jamesle01`).
        df["player_id"] = anonymize_ids(df["player_id"])
        df["conference"] = df["conference"].map({"Est": "East", "West": "West"})
        df["ballot_position"] = df["ballot_position"].map({"Back": "guard", "Front": "frontcourt"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "player_id",
                "position",
                "second_position",
                "team",
                "season",
                "conference",
                "ballot_position",
            ],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        ranked = raw[["FRank", "PRank", "MRank"]].notna().all(axis=1)
        matches = (raw["Score"] - documented_score(raw)).abs() < 0.051
        no_votes = raw["Pvot"].fillna(0).eq(0) | raw["Mvot"].fillna(0).eq(0)
        target_fix = pd.DataFrame(
            {
                "rows": raw.groupby("Season").size(),
                "rows with all three ranks": ranked.groupby(raw["Season"]).sum(),
                "of these, shipped score = documented formula": (ranked & matches).groupby(raw["Season"]).sum(),
                "rows without player or media votes": no_votes.groupby(raw["Season"]).sum(),
                "mean shipped score": raw.groupby("Season")["Score"].mean().round(1),
                "mean target": df.groupby("season", observed=True)[TARGET].mean().round(1),
            }
        )
        target_fix.index.name = "season"

        seasons = df.groupby("player_id", observed=True)["season"].nunique()
        wide = df.pivot_table(index="player_id", columns="season", values=TARGET, observed=True)
        persistence = pd.DataFrame(
            {
                "value": [
                    int((seasons == 3).sum()),
                    int((seasons == 2).sum()),
                    int((seasons == 1).sum()),
                    round(wide["2016-17"].corr(wide["2017-18"], method="spearman"), 3),
                    round(wide["2017-18"].corr(wide["2018-19"], method="spearman"), 3),
                ]
            },
            index=[
                "players in 3 seasons",
                "players in 2 seasons",
                "players in 1 season",
                "Spearman of a player's target, 2016-17 vs 2017-18",
                "Spearman of a player's target, 2017-18 vs 2018-19",
            ],
        )

        alphabetical = pd.Series(
            {
                season: round(group["Rk"].corr(last_name_order(group["Player.x"]), method="spearman"), 4)
                for season, group in raw.groupby("Season")
            },
            name="Spearman of Rk with the last-name order",
        )
        alphabetical.index.name = "season"
        return [
            Decision(
                "Target recomputed for 2017-18 and 2018-19 with the documented formula",
                "The shipped score of these seasons adds the ballot size plus one to the rank of players without "
                "player or media votes, which the data card's formula and the file's own ranks do not. Recomputed, "
                "the two seasons equal the NBA's official weighted scores (pr.nba.com 2018 and 2019 result tables) "
                "for all 958 file rows matched by name; the shipped score matches 28. 2016-17 follows the formula "
                "and keeps its values.",
                target_fix,
            ),
            Decision(
                "Grouped by player",
                "Most players appear in several seasons and their score carries over; the source kept one season "
                "per player for independence. A temporal split by season cannot be built from three seasons.",
                persistence,
            ),
            Decision(
                "`Rk` dropped: basketball-reference's alphabetical row number",
                "TabSTAR used `Rk` as the target ('NBA All-Star Rank'), but it orders the players by last name.",
                alphabetical,
            ),
        ]
