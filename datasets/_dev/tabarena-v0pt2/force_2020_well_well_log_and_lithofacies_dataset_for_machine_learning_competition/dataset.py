"""Curated dataset definition for `force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    TaskSummary,
    drop_columns,
)

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

PENALTY_LABELS = [
    "Sandstone",
    "Sandstone/Shale",
    "Shale",
    "Marl",
    "Dolomite",
    "Limestone",
    "Chalk",
    "Halite",
    "Anhydrite",
    "Tuff",
    "Coal",
]
"""The lithologies in the order of the starter notebook's ``lithology_numbers``, without Basement."""

PENALTY_MATRIX = [
    [0.0, 2.0, 3.5, 3.0, 3.75, 3.5, 3.5, 4.0, 4.0, 2.5, 3.875],
    [2.0, 0.0, 2.375, 2.75, 4.0, 3.75, 3.75, 3.875, 4.0, 3.0, 3.75],
    [3.5, 2.375, 0.0, 2.0, 3.5, 3.5, 3.75, 4.0, 4.0, 2.75, 3.25],
    [3.0, 2.75, 2.0, 0.0, 2.5, 2.0, 2.25, 4.0, 4.0, 3.375, 3.75],
    [3.75, 4.0, 3.5, 2.5, 0.0, 2.625, 2.875, 3.75, 3.25, 3.0, 4.0],
    [3.5, 3.75, 3.5, 2.0, 2.625, 0.0, 1.375, 4.0, 3.75, 3.5, 4.0],
    [3.5, 3.75, 3.75, 2.25, 2.875, 1.375, 0.0, 4.0, 3.75, 3.125, 4.0],
    [4.0, 3.875, 4.0, 4.0, 3.75, 4.0, 4.0, 0.0, 2.75, 3.75, 3.75],
    [4.0, 4.0, 4.0, 4.0, 3.25, 3.75, 3.75, 2.75, 0.0, 4.0, 4.0],
    [2.5, 3.0, 2.75, 3.375, 3.0, 3.5, 3.125, 3.75, 4.0, 0.0, 2.5],
    [3.875, 3.75, 3.25, 3.75, 4.0, 4.0, 4.0, 3.75, 4.0, 2.5, 0.0],
]
"""The competition's penalty A[true, predicted] (penalty_matrix.npy), the 11 x 11 sub-matrix without Basement."""

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

SENTINEL_FLOOR = -900.0
"""Log values below this are the LAS null values (-999.0, -999.25, -999.9) or interpolation ramps from them."""

NON_NEGATIVE = ["RSHA", "RMED", "RDEP", "RMIC", "RXO", "GR", "SGR", "ROP", "ROPA"]
"""Resistivity, gamma-ray and penetration-rate curves, which cannot be negative."""

DCAL_MAX = 100.0
"""A differential caliper (hole diameter minus bit size, inches) above this is impossible."""

DRHO_HOLDS_DENSITY = ["36/7-3", "31/4-10"]
"""Wells whose DRHO curve holds a bulk density (equal to RHOB in 36/7-3), not a density correction."""


def impossible_values(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Where the log curves of ``frame`` hold no reading, by reason; each value is a boolean frame over ``LOGS``."""
    logs = frame[LOGS]
    none = pd.DataFrame(False, index=frame.index, columns=LOGS)
    negative, dcal, drho = none.copy(), none.copy(), none.copy()
    negative[NON_NEGATIVE] = logs[NON_NEGATIVE] < 0
    dcal["DCAL"] = logs["DCAL"] > DCAL_MAX
    drho["DRHO"] = frame["WELL"].isin(DRHO_HOLDS_DENSITY) & logs["DRHO"].notna()
    return {
        "below -900 (LAS null or ramp)": logs < SENTINEL_FLOOR,
        "negative": negative & ~(logs < SENTINEL_FLOOR),
        f"DCAL above {DCAL_MAX:g}": dcal,
        "DRHO holds a density": drho & ~(logs < SENTINEL_FLOOR),
    }


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
            "competition gave them. The known gap: the interpreters also drew on mud logs, completion logs and "
            "in-house data that the model does not get, which the organisers say caps the reachable accuracy near "
            "80%."
        ),
    )

    # Dataset
    unique_name = "force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition"
    year = "2020"
    domain = "environmental science & climate"
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
        - Grouped cross-validation by well over all 118 wells replaces the competition's 98 / 10 / 10 split, whose blind set the organisers found too small to represent the lithologies (see the splits comment). Neighbouring depths of a well are nearly identical, so a row-random split would let a model recognise the well (a random forest of 150 trees on every 10th depth sample: log loss 0.315 on row-random folds against 0.763 on the grouped folds, 3 folds each).
        - We drop FORCE_2020_LITHOFACIES_CONFIDENCE, the interpreter's confidence in the label: it is recorded with the label and is missing for the open-test wells.
        - Target: FORCE_2020_LITHOFACIES_LITHOLOGY, mapped to the names of the starter notebook and renamed lithology. We drop the Basement class, whose 103 rows are all in well 16/4-1, so no grouped split can both train and test it; 11 classes remain.
        - Proxy missing values: values below -900 in the 20 log curves become missing. They are the LAS null values -999.0, -999.25 and -999.9 (in RXO, SP and ROPA) and interpolation ramps from them (RXO -995.9 and -968.1, ROPA -965.9 and -948.9, DRHO -7,429.3). Z_LOC is not masked: it is the true vertical depth, below -900 m on most rows.
        - Impossible values become missing: negative readings of the resistivity, gamma-ray and penetration-rate curves (RMED 7, RXO 131, SGR 39, ROP 52 and ROPA 20 rows; SGR down to -778) and DCAL above 100 inches (2 rows, one of 10,006.8).
        - DRHO becomes missing in two wells where it holds another curve: in 36/7-3 it equals RHOB on all 3,474 rows, in 31/4-10 it is a bulk density (median 2.38 g/cm3, 2,208 rows); a density correction is normally within about 0.2 g/cm3. We mask by well, not by a threshold: |DRHO| > 1 would also take 3,339 rows of 28 other wells (median -1.16), unusual bad-hole readings that stay.
        - Interpolated values and spikes otherwise stay ("slightly cleaned up and partially despiked", Zenodo), as do missing curves: only WELL, DEPT and GR are guaranteed (starter notebook).
        - WELL (the group of the split), GROUP and FORMATION are categorical.
        - Note: GROUP and FORMATION are NPD's lithostratigraphy picks, not the FORCE interpreters' (every top in the Zenodo record's NPD files has Interpreter NPD; the deepest top above each sample reproduces GROUP on 100% and FORMATION on 99.95% of the rows). They are not independent of the label: lithostratigraphic units are defined by their rock, the labels and the NPD tops draw on the same post-well material (completion and mud logs), 14,709 of 14,711 Halite rows lie in the Zechstein group, four formation names state a lithology ("Intra ... Fm. Sst.", "Ran Sst Mb."; 0.66% of the rows), and within 0.76 m (NPD's whole-metre rounding) 65.7% of group and 62.8% of formation boundaries sit on a lithology change, against 23.4% of random samples (4x). The competition gave them as features, so we keep them; without both, a random forest's log loss rises from 0.764 to 0.809 (100 trees, 200k training rows per grouped fold). Whether NPD's picks exist when a newly drilled well is first interpreted is not settled: the interpreter would then have the operator's own tops.
        - Note: 34/5-1 A and 34/5-1 S, two wellbores of one well, share 2,273 measured depths but no identical readings and lie 1.5-1.9 km apart at equal measured depth, so the group stays the wellbore, as in the competition; both are in one fold of the shipped splits.
        - Note: the task probes show a real signal that the model families spread over: random forest log loss 0.742, untuned LightGBM 0.872, the linear model 0.886, the class shares 1.288 (3 grouped folds). Before the impossible values were masked, untuned LightGBM diverged (2.68) and the probes flagged no_spread.
        - Anomaly: MUDWEIGHT is on three scales (per-well medians of 0.13-0.17 in 19 wells, 1.08-1.80 in 9 and 156 in 16/10-2) with no unit in the competition files; we leave it, as a conversion would rest on guessed units. Other curves have wells on another scale: ROP in 25/6-2 (median 17,778 against 0.6-150 elsewhere, 2,925 rows), SGR in 34/12-1 and 35/11-15 S (medians about 0.01 against 46-106, 8,731 rows) and ROPA in 34/4-10 R (median 0.099 against 10-82). The scale is constant within a well.
        - Anomaly: the labels are a hand interpretation; the organisers put the reachable accuracy near 80% (repository blog post, p. 9).
        - Metric: the competition's penalty matrix scores the hard labels (the spec); the top three teams trained on multiclass log loss (technical retrospective in the repository, p. 3-4).
        - No duplicate rows or repeated (WELL, DEPTH_MD) pairs.
    """

    # Task
    target = "lithology"
    problem_type = "multiclass_classification"
    metric = Metric.source(
        "cost_matrix",
        original="penalty matrix score S = -(1/N) sum_i A[y_true_i, y_pred_i]",
        reference=(
            "FORCE 2020 starter notebook, https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition/blob/"
            "master/lithology_competition/data/starter_notebook.ipynb"
        ),
        params={"labels": PENALTY_LABELS, "matrix": PENALTY_MATRIX},
        definition=(
            "mean over depth samples of the competition's penalty A[true, predicted] on hard labels (the competition's "
            "score is its negative); 11 x 11 sub-matrix of penalty_matrix.npy after Basement was dropped, symmetric, "
            "zero diagonal, order of the starter notebook's lithology_numbers"
        ),
    )
    grouping = Grouping(
        on="WELL",
        labels="per_sample",
        prediction_unit="row",
        context="all_rows",
        definition="""
            One group is a wellbore (WELL, 118 in the Norwegian North Sea); its rows are the depth samples of its logs, which DEPTH_MD orders. The use case is to interpret the lithology of a new well from its logs, and the organisers held out whole wells: "We held out 10 wells where we only provided the logs (test dataset) and 10 wells that were not provided at all to the contestants" (blog post in the repository, p. 3). Each depth sample is one prediction, scored per sample as in the competition. The whole log of a new well is known when it is interpreted, so a model may use the well's other depths: the starter notebook keeps WELL "so the data can be separated per well. This will be necessary for any 'windowed' approaches where we use non-local information in the ML features".
        """,
    )
    splits_comment = """
        Grouped 3-fold cross-validation by well over all 118 wells (37 to 41 whole wells per test fold, one repeat) replaces the competition's 98 training, 10 open-test and 10 blind wells: the organisers found the blind set too small to represent the lithologies ("With hindsight we should have chosen a larger blind dataset", blog post, p. 3). Test wells have drilled neighbours, as the competition's held-out wells had (14 of its 20 share a licence block with a training well): the median distance from a test well to the nearest training well is 8 km and 55-76% share a licence block, so the score stands for new wells in explored areas, not frontier wells (random forest log loss 0.763 grouped by well, 0.814 by licence block, 1.015 by quadrant). Halite (4 wells) and Anhydrite (10) are absent from one test fold.
    """
    accepted_check_warnings = {
        "splits_test_class_missing": "Halite occurs in 4 wells (14,711 rows) and Anhydrite in 10 (1,807 rows). The "
        "grouped folds keep wells whole, and fold r0f2 tests none of them; r0f0 and r0f1 test 1 and 3 halite wells "
        "and 6 and 4 anhydrite wells, and every train side holds both classes. The mean penalty is defined on the "
        "classes a fold holds.",
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
        # 4. LAS null values, their interpolation ramps and impossible readings are missing values
        masks = impossible_values(df)
        df[LOGS] = df[LOGS].mask(np.logical_or.reduce([mask.to_numpy() for mask in masks.values()]))
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
        masks = impossible_values(stacked[lithology != "Basement"])
        masked = pd.DataFrame({reason: mask.sum() for reason, mask in masks.items()})
        masked = masked[masked.sum(axis=1) > 0]
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
                "LAS null values and impossible readings set to missing",
                "Values below -900 are the LAS null values -999.0, -999.25 and -999.9 (stored as float32) or "
                "interpolation ramps from them. Resistivity, gamma ray and penetration rate cannot be negative, a "
                "differential caliper above 100 inches is impossible, and DRHO holds a bulk density in 36/7-3 and "
                "31/4-10. Rows masked per curve and reason (Basement rows dropped):",
                masked,
            ),
        ]
