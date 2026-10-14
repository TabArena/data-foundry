"""Curated dataset definition for `force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, TaskSummary, drop_columns

LABEL = "FORCE_2020_LITHOFACIES_LITHOLOGY"
"""The lithology code of the competition files."""

LITHOLOGY = {
    30000: "Sandstone",
    65030: "Sandstone/Shale",
    65000: "Shale",
    80000: "Marl",
    74000: "Dolomite",
    70000: "Limestone",
    70032: "Chalk",
    88000: "Halite",
    86000: "Anhydrite",
    99000: "Tuff",
    90000: "Coal",
    93000: "Basement",
}
"""The lithology names of the codes, from the competition's starter notebook."""

LOGS = [
    "CALI",
    "RSHA",
    "RMED",
    "RDEP",
    "RHOB",
    "GR",
    "SGR",
    "NPHI",
    "PEF",
    "DTC",
    "SP",
    "BS",
    "ROP",
    "DTS",
    "DCAL",
    "DRHO",
    "MUDWEIGHT",
    "RMIC",
    "ROPA",
    "RXO",
]
"""The wireline-log and drilling curves of the files."""

LAS_NULLS = [-999.0, -999.25, -999.9]
"""LAS null values left in some curves (RXO, SP, ROPA)."""


def las_nulls(frame: pd.DataFrame) -> pd.DataFrame:
    """Where ``frame`` holds a LAS null value; the files store them as float32 (-999.9000244, -999.2501221)."""
    values = frame.to_numpy(dtype=float)
    null = np.zeros(values.shape, dtype=bool)
    for value in LAS_NULLS:
        null |= np.isclose(values, value, rtol=0, atol=0.01)
    return pd.DataFrame(null, index=frame.index, columns=frame.columns)


class Force2020WellWellLogAndLithofaciesDatasetForMachineLearningCompetition(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Which rock type lies at each depth of a newly drilled well, judging from its well logs?"),
        use_case=(
            "After a well has been drilled and logged, a geologist interprets the rock type along the whole well from"
            " its wireline logs, its position and the official stratigraphic picks (the FORCE 2020 competition's "
            "task)."
        ),
        row="One depth sample (every 0.152 m) of one of 118 wells in the Norwegian North Sea.",
        predicted=(
            "The rock type at that depth as interpreted by hand, one of 11 classes such as shale, sandstone or "
            "limestone."
        ),
        known=(
            "The well's logs at that depth (gamma ray, resistivity, density, neutron, sonic, caliper and others, some"
            " missing), the depth and position, drilling data (bit size, mud weight, rate of penetration) and the "
            "stratigraphic group and formation; the same well's other depths may be used."
        ),
        split=("Whole wells are held out in three folds, so the test data stands for wells never interpreted."),
        changes=(
            "We pool the competition's training, open-test and blind wells and split by well across all 118; we drop "
            "the interpreter's confidence in the label and the basement class, found in one well only."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is known once a well is logged, and a held-out well is a new well. The "
            "stratigraphic picks come from the national register (NPD) rather than the interpreters, as the "
            "competition gave them."
        ),
    )

    # Dataset
    unique_name = "force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition"
    year = "2020"
    domain = "chemistry & material science"
    source = "GitHub"
    source_url = "https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition"
    license = "CC BY 4.0 (Zenodo record); the original well logs: NLOD 2.0"
    data_tags = ("Spatial",)
    download_description = """
        We download the competition files from the organisers' GitHub repository, pinned to a commit (the data files
        are unchanged since they were added on 2020-11-13). The Zenodo record (https://doi.org/10.5281/zenodo.4351156)
        archives the same 118 wells as LAS files; we do not use them.

        mkdir -p local-data-warehouse/force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition
        cd local-data-warehouse/force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition
        BASE=https://raw.githubusercontent.com/bolgebrygg/Force-2020-Machine-Learning-competition/c8d01ee92c1c8e1ecba36f96cca6ea7b689338a1/lithology_competition/data
        wget $BASE/train.zip $BASE/leaderboard_test_features.csv $BASE/leaderboard_test_target.csv $BASE/hidden_test.csv

        md5: train.zip d935a5161fb47421a07f0a51abfc3d46, leaderboard_test_features.csv b562ce84d315de526e5983bfe85aaf30,
        leaderboard_test_target.csv 50d873b9ee892ff5f0d8b8075c474482, hidden_test.csv 1ea8d4310de00f1beb7d5ba7e7006c26.
    """
    bibtex = """
        @misc{bormann2020force,
          author = {Bormann, Peter and Aursand, Peder and Dilib, Fahad and Manral, Surrender and Dischington, Peter},
          title = {{FORCE} 2020 Well well log and lithofacies dataset for machine learning competition},
          year = {2020},
          publisher = {Zenodo},
          doi = {10.5281/zenodo.4351156},
          howpublished = {\\url{https://doi.org/10.5281/zenodo.4351156}},
          note = {FORCE 2020 Machine Learning Competition, \\url{https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition}}
        }
    """
    curation_comments = """
        We start with the four files of the FORCE 2020 lithology competition on GitHub: train.zip (98 wells), leaderboard_test_features.csv with leaderboard_test_target.csv (10 open-test wells) and hidden_test.csv (10 blind wells, labels included). Each row is one depth sample (every 0.152 m) of one of 118 wells in the Norwegian North Sea.

        - Prediction point: a well has been drilled and logged, and its lithology is interpreted from the wireline logs, the NPD lithostratigraphy (GROUP, FORMATION) and the well position (GitHub readme). Every feature is known then, for every depth of the well.
        - We stack the three files (1,429,694 rows), joining the open-test features to their labels row by row after checking that both list the same WELL and DEPTH_MD.
        - Grouped cross-validation by well over all 118 wells replaces the competition's 98 / 10 / 10 split, whose blind set the organisers found too small to represent the lithologies. Neighbouring depths of a well are nearly identical, so a row-random split would let a model recognise the well (random forest log loss 0.31 on row-random folds against 0.78 on grouped folds).
        - We drop FORCE_2020_LITHOFACIES_CONFIDENCE, the interpreter's confidence in the label: it is recorded with the label and is missing for the open-test wells.
        - Target: FORCE_2020_LITHOFACIES_LITHOLOGY, mapped to the names of the starter notebook and renamed lithology. We drop the Basement class, whose 103 rows are all in well 16/4-1, so no grouped split can both train and test it; 11 classes remain.
        - Proxy missing values: the LAS null values -999.0, -999.25 and -999.9 become missing in RXO, SP and ROPA. Interpolated values and spikes stay ("slightly cleaned up and partially despiked", Zenodo), as do missing curves: only WELL, DEPT and GR are guaranteed (starter notebook).
        - WELL (the group of the split), GROUP and FORMATION are categorical.
        - Note: GROUP and FORMATION are NPD's lithostratigraphy picks, not the FORCE interpreters' (every top in the Zenodo record's NPD files has Interpreter NPD), and only 10% of the 574 group boundaries fall on a lithology change at the same sample. The competition gave them as features, so we keep them; without both the random forest's log loss rises from 0.78 to 0.84.
        - Note: 34/5-1 A and 34/5-1 S, two wellbores of one well, share no depth sample and lie 1.1-1.9 km apart where their depths overlap, so the group stays the wellbore, as in the competition.
        - Note: the task probes flag no_spread because untuned LightGBM diverges here with its default min_child_weight of 0.001 (log loss 2.77). The random forest (0.744, class shares 1.284) and the linear model (0.989) differ by 0.19 skill, so the families spread.
        - Anomaly: MUDWEIGHT is on three scales (per-well medians of 0.13-0.17, 1.08-1.80 and 156) with no unit in any LAS header; we leave it, as a conversion would rest on guessed units.
        - Anomaly: the labels are a hand interpretation; the organisers put the reachable accuracy near 80% (repository blog post, p. 9).
        - Note: we score log loss, not the competition's penalty matrix. No duplicate rows or repeated (WELL, DEPTH_MD) pairs.
    """

    # Task
    target = "lithology"
    problem_type = "multiclass_classification"
    grouping = Grouping(
        on="WELL",
        labels="per_sample",
        prediction_unit="row",
        context="all_rows",
        definition="""
            One group is a wellbore (WELL, 118 in the Norwegian North Sea); its rows are the depth samples of its logs, which DEPTH_MD orders. The use case is to interpret the lithology of a new well from its logs, and the organisers held out whole wells: "We held out 10 wells where we only provided the logs (test dataset) and 10 wells that were not provided at all to the contestants" (blog post in the repository, p. 3). Each depth sample is one prediction, scored per sample as in the competition. The whole log of a new well is known when it is interpreted, so a model may use the well's other depths: the starter notebook keeps WELL "so the data can be separated per well. This will be necessary for any 'windowed' approaches where we use non-local information in the ML features".
        """,
    )
    accepted_check_warnings = {
        "splits_test_class_missing": "Halite occurs in 4 wells (14,711 rows) and Anhydrite in 10 (1,807 rows). The "
        "grouped folds keep wells whole, and fold r0f2 tests none of them; r0f0 and r0f1 test 1 and 3 halite wells "
        "and 6 and 4 anhydrite wells, and every train side holds both classes. Log loss is defined on the classes a "
        "fold holds.",
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        train = pd.read_csv(raw_dir / "train.zip", sep=";")
        features = pd.read_csv(raw_dir / "leaderboard_test_features.csv", sep=";")
        labels = pd.read_csv(raw_dir / "leaderboard_test_target.csv", sep=";")
        # the open-test labels list the same (WELL, DEPTH_MD) in the same order as the features
        assert features["WELL"].equals(labels["WELL"])
        assert features["DEPTH_MD"].equals(labels["DEPTH_MD"])
        open_test = features.assign(**{LABEL: labels[LABEL].to_numpy()})
        hidden_test = pd.read_csv(raw_dir / "hidden_test.csv", sep=";")
        return {"train": train, "open_test": open_test, "hidden_test": hidden_test}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. Stack the training, open-test and blind wells; grouped cross-validation replaces their split
        df = pd.concat([raw["train"], raw["open_test"], raw["hidden_test"]], ignore_index=True)
        # 2. The interpreter's confidence in the label is recorded with it
        df = drop_columns(df, ["FORCE_2020_LITHOFACIES_CONFIDENCE"])
        # 3. Lithology names; Basement occurs in one well only (16/4-1, 103 rows)
        df["lithology"] = df[LABEL].map(LITHOLOGY)
        assert df["lithology"].notna().all()
        df = drop_columns(df, [LABEL])
        df = df[df["lithology"] != "Basement"]
        # 4. LAS null values are missing values
        df[LOGS] = df[LOGS].mask(las_nulls(df[LOGS]))
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["WELL", "GROUP", "FORMATION"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        stacked = pd.concat([frame.assign(file=name) for name, frame in raw.items()], ignore_index=True)
        lithology = stacked[LABEL].map(LITHOLOGY).rename("lithology")
        classes = pd.DataFrame(
            {
                "rows": lithology.value_counts(),
                "wells": stacked.groupby(lithology)["WELL"].nunique(),
            }
        ).sort_values("rows", ascending=False, kind="stable")
        files = stacked.groupby("file", sort=False).agg(rows=("WELL", "size"), wells=("WELL", "nunique"))
        null = las_nulls(stacked[LOGS])
        nulls = pd.DataFrame({"rows": null.sum(), "wells": null.groupby(stacked["WELL"]).any().sum()})
        nulls = nulls[nulls["rows"] > 0]
        return [
            Decision(
                "All 118 wells in one frame, split by well",
                "The competition's split is 98 training, 10 open-test and 10 blind wells; the organisers found the 10 "
                "blind wells too few to represent the lithologies. Grouped 3-fold cross-validation over all wells "
                "tests about 39 wells per fold.",
                files,
            ),
            Decision(
                "Basement dropped: one well",
                "A class that occurs in a single well cannot be in the train and the test side of a grouped split. "
                "All other classes occur in at least 4 wells.",
                classes,
            ),
            Decision(
                "LAS null values set to missing",
                "The values -999.0, -999.25 and -999.9 (stored as float32) are the null values of the LAS format, "
                "not readings.",
                nulls,
            ),
        ]
