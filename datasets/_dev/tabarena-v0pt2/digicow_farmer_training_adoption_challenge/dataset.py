"""Curated dataset definition for `digicow_farmer_training_adoption_challenge` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import ast
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Temporal, TemporalSplits, drop_columns

TARGET = "adopted_within_07_days"
"""The challenge's main target: adoption within 7 days of the training (most of the leaderboard weight)."""

LATER_TARGETS = ["adopted_within_90_days", "adopted_within_120_days"]
"""The challenge's two other targets; each contains the 7-day label (7 <= 90 <= 120 in every row)."""

FLAG_ONLY_TRAINERS = ["TRA_szrwyfzz", "TRA_hyodnntj"]
"""The two trainers whose rows carry `has_topic_trained_on` = 1 mostly for adopters (curation comments)."""

WINDOWS = TemporalSplits(window=4, unit="months", n_windows=9, min_train_fraction=0.5)
"""Four-month test windows walking back from December 2025; the 50% train floor stops after four (splits comment)."""


def stored_day(raw: pd.DataFrame) -> pd.Series:
    """The training date as Train.csv stores it: `YYYY-MM-DD` with the day of the training in the month field."""
    return pd.to_datetime(raw["training_day"], format="%Y-%m-%d")


def true_day(raw: pd.DataFrame) -> pd.Series:
    """The training date with day and month swapped back (curation comments)."""
    stored = stored_day(raw)
    return pd.to_datetime(pd.DataFrame({"year": stored.dt.year, "month": stored.dt.day, "day": stored.dt.month}))


def trainer_text(cell: str) -> str:
    """`['TRA_a', 'TRA_b']` -> `TRA_a, TRA_b` (one trainer in all but 3 rows)."""
    return ", ".join(ast.literal_eval(cell))


def topics_text(cell: str) -> str:
    """`[['A', 'B'], ['C']]` -> `A; B | C`: the topics of each session of the training day, sessions split by `|`."""
    return " | ".join("; ".join(session) for session in ast.literal_eval(cell))


class DigicowFarmerTrainingAdoptionChallenge(AbstractCuratedDataset):
    # Dataset
    unique_name = "digicow_farmer_training_adoption_challenge"
    year = "2026"
    domain = "environmental science & climate"
    source = "Zindi"
    source_url = "https://zindi.africa/competitions/digicow-farmer-training-adoption-challenge"
    license = "Zindi Competition Rules"
    data_tags = ("Spatial",)
    download_description = """
        The Zindi data page needs a login. The Zindi API lists the files of the final data release
        (https://api.zindi.world/v1/competitions/digicow-farmer-training-adoption-challenge, field `datafiles`; the
        zip's manifest is dated 2026-02-10T12:40:23): Train.csv 3,239,613 bytes, Test.csv 1,254,202, Prior.csv
        7,454,788, dataset_data_dictionary.csv 880. Two participant copies hold exactly these files: the Kaggle
        dataset laban102/digicow-farmer-training-adoption-dataset (uploaded 2026-02-13, with the Zindi manifest) and
        the 9th-place solution repository on GitHub; their files are byte-identical (same git blob hashes). We download
        the two files the definition reads from the GitHub commit, which pins them.

        mkdir -p local-data-warehouse/digicow_farmer_training_adoption_challenge
        cd local-data-warehouse/digicow_farmer_training_adoption_challenge
        BASE=https://raw.githubusercontent.com/AgbajeAyomipo/DigiCow-Farmer-Training-Adoption-Challenge-9th-place-solution/b736cc8255b4d68b39241cb0fec02563f957ab56/data
        wget $BASE/Train.csv $BASE/dataset_data_dictionary.csv

        Alternative (the same bytes): uvx --from kaggle==2.2.2 kaggle datasets download
        laban102/digicow-farmer-training-adoption-dataset, then unzip Train.csv and dataset_data_dictionary.csv.

        sha256 (2026-10-07): Train.csv 4977559dc82378b23a846b15ada8ce54714cb319ed38d1f829b2f63e05b72ac4,
        dataset_data_dictionary.csv 13f730ecb97836abd3fbd6f905ddf7e4c353f213d7eedfb4eacad238816beb11.
    """
    bibtex = r"""
        @misc{Zindi2026DigiCowFarmerTrainingAdoption,
          author = {{Zindi} and {DigiCow Africa} and {Digital Africa}},
          title = {DigiCow Farmer Training Adoption Challenge},
          year = {2026},
          howpublished = {\url{https://zindi.africa/competitions/digicow-farmer-training-adoption-challenge}},
          note = {Zindi competition, 2026-01-28 to 2026-03-01}
        }
    """
    curation_comments = """
        We start with Train.csv of the Zindi DigiCow Farmer Training Adoption Challenge (final release, 2026-02-10): 13,536 labelled rows, one per farmer.

        - Recommendation (2026-10-07): retire, suggestion `No` with the markers `Too Small` and `Data Quality Issue`; the folder stays for Lennart's decision (last two bullets). Revisit if DigiCow documents when and for which trainers adoption was followed up.
        - Prediction point: the end of a farmer's training day, when DigiCow knows the farmer's profile, the trainer and the topics of the day's sessions.
        - We use the final release, from which the host removed the counts over later trainings after leak reports; Test.csv has no labels.
        - Dates: `training_day` is stored with the day in the month field. We swap them back; then Sundays are rare and 42.7% of a group's date gaps are whole weeks (first decision). The day is never above 12, so the release holds days 1-12 of each month only.
        - We do not use Prior.csv: in true dates 20.3% of its rows for Train.csv farmers come after the farmer's Train.csv row, so history features built from it would see later outcomes.
        - Target: `adopted_within_07_days`, the challenge's main target. We drop `adopted_within_90_days` and `adopted_within_120_days`: later outcomes that contain the 7-day label in every row.
        - We drop `has_topic_trained_on`: for the trainers TRA_szrwyfzz and TRA_hyodnntj it goes with the adoption, and within one session the flagged farmers hold all the 7-day adopters (second decision). The drop is incomplete, since `topics_list` predicts the flag with ROC AUC 0.87 in these trainers' rows. Dropping both or keeping both is Lennart's call.
        - We drop `ID` (row id) and `farmer_name` (one row per farmer). `trainer` (a list of ids) and `topics_list` are written as text, topics joined by "; " within a session and sessions by " | ". Gender, registration, age band, group, county, subcounty, ward and trainer are categoricals; `belong_to_cooperative` stays 0/1.
        - Duplicates, kept: 6,590 rows (48.7%) repeat another row, but each is a different farmer of the same session and recorded profile. Copies share the training day, so they fall in the same test window.
        - Label recording (Data Quality Issue): a 0 mixes "did not adopt" with "not recorded". The share of 120-day adopters who adopted within 7 days is 0% for the trainings of August-October 2024 and 45%, 64% and 95% for November 2024, December 2024 and February 2025 (third decision), and TRA_gertumxc's farmers of March-July 2025 never adopted at any horizon (fourth decision). The trainer and location columns, the leak probes' strongest single features, carry this recording.
        - Anomaly: one row per farmer is the challenge's construction (the farmer's latest training in stored-date order); the selection uses dates, not labels.
        - Too Small: the test windows hold 9, 5, 19 and 103 adopters from 1, 1, 2 and 7 trainers, and shorter windows leave a window without any adopter (fifth decision). A random split, folds grouped by `group_name` or leaving one trainer out do not fix this (NEW_DATASETS_ISSUES.md).
    """

    # Task
    target = TARGET
    problem_type = "binary_classification"

    # Splits: 4-month windows of true training dates (splits comment)
    temporal = Temporal(on="training_day", splits=WINDOWS)
    splits_comment = """
        DigiCow scores a farmer at the end of the training day and refits on trainings whose 7-day outcome is known. Trainings fall on days 1-12 of a month only, so with windows that start on the first of a month the newest training on a train side is at least 19 days old in every window (17 after a February) and its 7-day label is known: no gap is needed. Test windows of 4 calendar months walk back from December 2025, newest first, while the train side holds at least half of the rows; train is all earlier data. That gives 4 windows: September-December 2025 (718 rows, 9 adopters), May-August 2025 (773 rows, 5), January-April 2025 (727 rows, 19; no training in January) and September-December 2024 (4,264 rows, 103), the last trained on 7,054 rows with 17 adopters. Adopters arrive in waves (curation comments), so shorter windows leave a window without any adopter (with 3-month windows, April-June 2025 has none): 4 months is the shortest calendar window for which every window holds adopters, and the 50% floor ends the walk back at September 2024, short of the 9 splits an IID task of this size would get. The windows' adopters come from 3, 3, 8 and 52 sessions and 1, 1, 2 and 7 trainers: too few units to compare methods (curation comments, Too Small; recommended for retirement).
    """
    accepted_check_warnings = {
        "dataset_duplicate_rows": "6,590 rows repeat another row: each row is a different farmer (13,536 distinct "
        "farmer_name values), trained in the same session with the same recorded profile. Copies share the training "
        "day, so they always fall in the same window (2026-10-07).",
        "dataset_pure_feature_value": "The values are three trainers and the counties, subcounty and ward they mainly "
        "serve: TRA_ubcgvofe 0 adopters in 1,456 rows, TRA_suiifsur 2 in 2,190, TRA_gertumxc 11 in 3,049. They mark "
        "where adoption was not recorded (curation comments, Label recording): the Data Quality Issue for which the "
        "dataset is recommended for retirement. Accepted only so that the folder checks clean for Lennart's decision "
        "(2026-10-07).",
        "splits_test_minority_few": "The two newest windows hold 9 and 5 adopters, all trained by TRA_rkvyofbh in 3 "
        "sessions each; shorter windows leave a window without any adopter. This is the Too Small for which the dataset "
        "is recommended for retirement. Accepted only so that the folder checks clean for Lennart's decision "
        "(2026-10-07).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv", dtype=str)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # The stored date holds the day in the month field: swap them back
        df["training_day"] = true_day(raw).dt.strftime("%Y-%m-%d")
        df["trainer"] = df["trainer"].map(trainer_text)
        df["topics_list"] = df["topics_list"].map(topics_text)
        df["belong_to_cooperative"] = df["belong_to_cooperative"].astype(int)
        df[TARGET] = df[TARGET].map({"1": "Yes", "0": "No"})
        return drop_columns(
            df,
            [
                "ID",  # row id
                "farmer_name",  # one row per farmer: an id
                "has_topic_trained_on",  # recorded with the adoption for two trainers (curation comments)
                *LATER_TARGETS,  # each contains the 7-day label
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["gender", "registration", "age", "group_name", "county", "subcounty", "ward", "trainer"],
            string=["topics_list"],
            datetime={"training_day": "%Y-%m-%d"},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        stored, true = stored_day(raw), true_day(raw)
        labels = raw[[TARGET, *LATER_TARGETS]].astype(int)

        # 1. The stored date has the day in the month field: weekdays and weekly group rhythms appear only swapped back
        def date_profile(dates: pd.Series) -> dict[str, object]:
            sessions = pd.DataFrame({"group": raw["group_name"], "date": dates}).drop_duplicates()
            gaps = sessions.sort_values(["group", "date"], kind="stable").groupby("group")["date"].diff().dt.days
            gaps = gaps.dropna()
            weekday = dates.dt.dayofweek
            return {
                "rows on a Saturday": round(float((weekday == 5).mean()), 3),
                "rows on a Sunday": round(float((weekday == 6).mean()), 3),
                "group date gaps": len(gaps),
                "gaps that are whole weeks": round(float((gaps % 7 == 0).mean()), 3),
                "largest day of the month": int(dates.dt.day.max()),
            }

        swap = pd.DataFrame({"as stored": date_profile(stored), "day and month swapped": date_profile(true)}).T

        # 2. has_topic_trained_on is recorded with the adoption for two trainers
        trainer = raw["trainer"].map(trainer_text)
        flag = raw["has_topic_trained_on"].astype(int)
        topic = (
            pd.DataFrame(
                {
                    "trainer": trainer,
                    "flag": flag,
                    "adopted 7 days": labels[TARGET],
                    "adopted 120 days": labels["adopted_within_120_days"],
                }
            )
            .groupby(["trainer", "flag"])
            .agg(
                rows=("flag", "size"),
                adopted_7_days=("adopted 7 days", "sum"),
                adopted_120_days=("adopted 120 days", "sum"),
            )
        )
        topic = topic[topic["rows"] >= 20]

        # 3. Adoptions arrive in waves: label classes by month of the (true) training date
        timing = pd.DataFrame(
            {
                "month": true.dt.strftime("%Y-%m"),
                "within 7 days": labels[TARGET],
                "day 8 to 90": labels["adopted_within_90_days"] - labels[TARGET],
                "day 91 to 120": labels["adopted_within_120_days"] - labels["adopted_within_90_days"],
            }
        )
        waves = timing.groupby("month").agg(
            rows=("month", "size"),
            adopted_within_7_days=("within 7 days", "sum"),
            adopted_day_8_to_90=("day 8 to 90", "sum"),
            adopted_day_91_to_120=("day 91 to 120", "sum"),
        )
        adopters = waves[["adopted_within_7_days", "adopted_day_8_to_90", "adopted_day_91_to_120"]].sum(axis=1)
        waves["share_within_7_days"] = (waves["adopted_within_7_days"] / adopters.where(adopters > 0)).round(2)

        # 4. The label is adoption as recorded: adopters by trainer and period (true dates)
        period = pd.cut(
            true,
            pd.to_datetime(["2024-01-01", "2024-11-01", "2025-01-01", "2026-01-01"]),
            right=False,
            labels=["Mar-Oct 2024", "Nov-Dec 2024", "2025"],
        )
        recorded = (
            pd.DataFrame(
                {
                    "trainer": trainer,
                    "period": period,
                    "adopted 7 days": labels[TARGET],
                    "adopted 120 days": labels["adopted_within_120_days"],
                }
            )
            .groupby(["trainer", "period"], observed=True)
            .agg(
                rows=("period", "size"),
                adopted_7_days=("adopted 7 days", "sum"),
                adopted_120_days=("adopted 120 days", "sum"),
            )
        )
        recorded = recorded[recorded["rows"] >= 20]

        # 5. The test windows, with the sessions and trainers of their adopters
        y = df[TARGET] == "Yes"
        session = df["training_day"].astype(str) + df["group_name"].astype(str) + df["trainer"].astype(str)
        rows = []
        for i, folds in self.make_splits(df).splits.items():
            train, test = folds[0]
            dates = df["training_day"].iloc[test]
            rows.append(
                {
                    "window": i,
                    "first day": dates.min().date(),
                    "last day": dates.max().date(),
                    "test rows": len(test),
                    "test adopters": int(y.iloc[test].sum()),
                    "adopter sessions": session.iloc[test][y.iloc[test].to_numpy()].nunique(),
                    "adopter trainers": df["trainer"].iloc[test][y.iloc[test].to_numpy()].nunique(),
                    "train rows": len(train),
                    "train adopters": int(y.iloc[train].sum()),
                }
            )
        windows = pd.DataFrame(rows).set_index("window")

        return [
            Decision(
                "training_day is stored with day and month swapped; we swap them back",
                "As stored, Sundays are as common as weekdays and a group's training dates are whole weeks apart no "
                "more often than chance; swapped back, Sundays are rare and 42.7% of the gaps are whole weeks, as for "
                "groups meeting on a fixed weekday. The day is never above 12, so the release holds days 1-12 only.",
                swap,
            ),
            Decision(
                "has_topic_trained_on is dropped: it goes with the adoption for two trainers",
                "For TRA_szrwyfzz and TRA_hyodnntj the flag is 1 on 221 of 4,195 rows, which hold all their adopters "
                "(71% adopted within 120 days); within one session only the adopters tend to carry it. For the other "
                "trainers it is 1 on almost every row. The drop is incomplete: topics_list predicts the flag with ROC "
                "AUC 0.87 in these trainers' rows (curation comments).",
                topic,
            ),
            Decision(
                "Adoptions are recorded in waves",
                "By month of the (swapped-back) training date, 1 of the 95 adopters trained in August-October 2024 "
                "adopted within 7 days, against 33 of 45, 69 of 77 and 19 of 19 for November 2024, December 2024 and "
                "February 2025: 36 of the 38 August adopters adopted on days 91-120, 40 of the 57 of September-October "
                "on days 8-90, all pointing at adoptions recorded around December 2024. A delay set by farmers' "
                "behaviour cannot jump like this between neighbouring months. 10 of the 21 months have no 7-day adopter.",
                waves,
            ),
            Decision(
                "The label is adoption as recorded: a 0 mixes 'did not adopt' with 'not recorded'",
                "Adopters appear only for some trainers and periods. TRA_gertumxc's farmers adopted within 120 days in "
                "the trainings of August-December 2024 and never in 2025, although the 2025 windows closed before the "
                "release; TRA_ubcgvofe and TRA_suiifsur record almost no adoption. This is the Data Quality Issue for "
                "which the dataset is recommended for retirement (curation comments).",
                recorded,
            ),
            Decision(
                "Test windows: 4 calendar months, newest first",
                "The shortest calendar windows for which every window holds adopters; the train side keeps at least "
                "half of the rows. The adopters of the two newest windows come from one trainer and 3 sessions each: "
                "Too Small.",
                windows,
            ),
        ]
