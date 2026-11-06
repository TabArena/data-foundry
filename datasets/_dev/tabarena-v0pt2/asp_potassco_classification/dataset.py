"""Curated dataset definition for `asp_potassco_classification` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    ScoringColumn,
    TaskSummary,
    anonymize_ids,
)


class AspPotasscoClassification(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How long will each of 11 configurations of the solver clasp take on a logic-programming problem of a kind"
            " not seen before?"
        ),
        use_case=(
            "Algorithm selection: a user of answer set programming (a way to state and solve search problems in logic)"
            " predicts the runtime of each configuration on a new problem instance and runs the one predicted fastest,"
            " as the selector claspfolio 2 does (ASlib, Bischl et al. 2016); here for a kind of problem not seen before."
        ),
        row=(
            "One run of one of 11 clasp configurations on one instance of the Potassco benchmark set, stopped at 600 "
            "seconds (1,212 instances from 96 problem classes that at least one configuration solved, 13,332 runs; "
            "ASlib, 2014)."
        ),
        predicted=(
            "The run's time in seconds, on a log scale; a run stopped at the 600-second limit counts as 600 (1,963 "
            "runs, on 38% of the instances)."
        ),
        known=(
            "The configuration's name, statistics of the instance's program (numbers of rules, atoms and constraints "
            "of each kind) and of a few short probing runs of the solver (choices, conflicts, learnt constraints, "
            "backjumps)."
        ),
        split=(
            "Whole problem classes are held out (32 of the 96 in each test fold), so the test data stands for a kind of "
            "problem never seen in training, as for a user with a new encoding."
        ),
        changes=(
            "We drop instances that no configuration solved within the time limit, and hold out whole problem classes"
            " where claspfolio 2 and ASlib split instances at random. ASlib adds the cost of computing the features to"
            " the selected runtime; we leave it out, as it is the same whichever configuration is picked."
        ),
        fit="approximate",
        fit_reason=(
            "The features exist before solving, a held-out class matches a new encoding, and the score is the time "
            "the user loses with the pick, timeouts included. But instances that no configuration solved are dropped,"
            " which a user cannot know in advance."
        ),
    )

    # Dataset
    unique_name = "asp_potassco_classification"
    year = "2014"
    domain = "technology & internet"
    source = "ASlib"
    source_url = "https://github.com/coseal/aslib_data/tree/master/ASP-POTASSCO"
    license = "GPLv3"
    download_description = r"""
        wget https://raw.githubusercontent.com/coseal/aslib_data/refs/heads/master/ASP-POTASSCO/algorithm_runs.arff \
        && wget https://raw.githubusercontent.com/coseal/aslib_data/refs/heads/master/ASP-POTASSCO/feature_values.arff \
        && mkdir -p local-data-warehouse/asp_potassco_classification \
        && mv feature_values.arff algorithm_runs.arff local-data-warehouse/asp_potassco_classification/
    """
    bibtex = """
        @article{hoos2014claspfolio,
          title={claspfolio 2: Advances in algorithm selection for answer set programming},
          author={Hoos, Holger and Lindauer, Marius and Schaub, Torsten},
          journal={Theory and Practice of Logic Programming},
          volume={14},
          number={4-5},
          pages={569--585},
          year={2014},
          publisher={Cambridge University Press}
        }
        @article{bischl_aslib_2016,
        	title = {{ASlib}: {A} {Benchmark} {Library} for {Algorithm} {Selection}},
        	number = {237},
        	journal = {Artificial Intelligence Journal (AIJ)},
        	author = {Bischl, Bernd and Kerschke, Pascal and Kotthoff, Lars and Lindauer, Marius and Malitsky, Yuri and Fréchette, Alexandre and Hoos, Holger H. and Hutter, Frank and Leyton-Brown, Kevin and Tierney, Kevin and Vanschoren, Joaquin},
        	year = {2016},
        	pages = {41--58}
        }
    """
    curation_comments = """
        We get the data from ASlib and merge them into one file.

        - Task (Andrej, 2026-11-04): runtime regression with one row per instance and configuration, as sat11_hand_algo_runtime. A selector in use learns from the full table of runs, every configuration on every training instance, timeouts included, and the user loses time mostly to timeouts (96% of the single best configuration's PAR10 comes from them). Until then the task was multiclass classification of the fastest configuration, as in the OpenML version (https://openml.org/d/41705), scored by log loss as a stand-in for PAR10; that label counted a pick 0.05 s slower as wrong as a timeout (for 62% of the instances the second-best configuration is within 1 s of the best) and no model saw a runtime or a timeout. On the 30 splits of the classification definition, always running the configuration most often fastest in training gives a PAR10 of 611 s, the best pick per instance 21 s; untuned LightGBM trained this way picks at 646 s.
        - We drop all instances that no configuration solved before the 600 s timeout (all their runtimes are the censored limit, and every choice costs the same). We keep the 1,963 timeouts of the other 1,212 instances at the limit of 600 s (every finished run took at most 599.7 s): selecting the fastest configuration needs every configuration's outcome, and the limit keeps the order within an instance and is enough to compute PAR10.
        - Timeouts stay at the recorded 600 s in the target (Andrej, 2026-11-06): it is the value ASlib records, and how to
          treat a censored run is left to the models; the scoring, ASlib's PAR10, charges a timeout ten times the limit.
          Counting timeouts at that charge (6,000 s) in the target moved the picks only within noise here (better with
          LightGBM and linear models, worse with a random forest and TabPFN).
        - We log scale the target. The configuration's name (`algorithm`) is a categorical feature: the scenario publishes no configuration features.
        - The instance id is anonymised and ships as a scoring column only: the metric picks per instance the configuration with the lowest predicted runtime. Never a feature.
        - We resolve the instance ID to a problem class (`task_id`) from its path: the instance path without the file name, for example `ASP-Comp-2011-Lparse/26-Solitaire`. A class holds different instances of one problem (here, Solitaire puzzles), and the best configuration depends on the class, which the instance features fingerprint. claspfolio 2 and ASlib split the instances at random, so their test instances come from known classes; we hold out whole classes instead, to predict the runtimes on a problem class not seen in training (the `definition` of the grouping).
        - Metric: ASlib's PAR10 of the configuration predicted fastest per instance. ASlib adds the feature costs (`feature_costs.arff`) to the selected runtime; they are the same whichever configuration is picked, so we leave them out.
        - To do: rename the dataset (it is no longer a classification task) once the BeyondArena v0.2 review page is done; its marks are stored under the current name.
    """

    # Task
    target = "runtime"
    problem_type = "regression"
    metric = Metric.source(
        "par_k",
        original="PAR10 (penalized average runtime, factor 10) of the selected configuration (ASlib)",
        reference=(
            "Bischl et al. 2016, ASlib: A benchmark library for algorithm selection, Artificial Intelligence "
            "237:41-58; https://github.com/coseal/aslib_data/tree/master/ASP-POTASSCO (cutoff 600 s)"
        ),
        definition=(
            "per instance select the configuration with the lowest predicted runtime; its true runtime in seconds"
            " (exp of the log target), a timeout (runtime >= 600 x (1 - 1e-4)) counted as 6,000 s; mean over "
            "instances. ASlib's feature costs are left out: they are the same whichever configuration is picked."
        ),
        params={"cutoff": 600, "k": 10, "timeout_rel_tol": 0.0001},
        inputs={"group": "instance_id"},
        target_transform="log",
    )
    scoring_columns = (
        ScoringColumn(
            column="instance_id",
            role="group",
            used_by="par_k",
            description=(
                "the anonymised instance (11 rows each, one per configuration); the metric picks per instance the "
                "configuration with the lowest predicted runtime and averages the picks' true runtimes."
            ),
        ),
    )
    grouping = Grouping(
        on="task_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a problem class of the Potassco ASP benchmark set (96 classes with 1 to 134 instances); its rows are the runs of the 11 clasp configurations on its instances, with the log runtime as the target. The use case is algorithm selection: predict every configuration's runtime on a new instance and run the one predicted fastest (ASlib, Bischl et al. 2016), scored per instance by the selected configuration's true runtime (PAR10) through the instance id, a scoring column. claspfolio 2 (Hoos et al. 2014) and ASlib split the instances at random; holding out whole problem classes is our choice and asks for a configuration on a problem class not seen in training.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        def load_arff(path) -> pd.DataFrame:
            with open(path, encoding="utf-8") as f:
                data = arff.load(f)
            df = pd.DataFrame(data["data"], columns=[a[0] for a in data["attributes"]])
            return df

        df_features = load_arff(raw_dir / "feature_values.arff").drop(columns=["repetition"])
        df_algo_runs = load_arff(raw_dir / "algorithm_runs.arff")
        return {"df_features": df_features, "df_algo_runs": df_algo_runs}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df_features, df_algo_runs = raw["df_features"], raw["df_algo_runs"]
        # Drop instances that no configuration solves: all their runtimes are the censored cutoff
        solved = df_algo_runs.loc[df_algo_runs["runstatus"] == "ok", "instance_id"].unique()
        df_algo_runs = df_algo_runs[df_algo_runs["instance_id"].isin(solved)].copy()
        # A run that did not finish counts as the 600 s limit (ASlib stores timeouts at 600 s already)
        df_algo_runs.loc[df_algo_runs["runstatus"] != "ok", "runtime"] = 600.0
        df_algo_runs = df_algo_runs[["instance_id", "algorithm", "runtime"]]
        # Merge
        df = df_algo_runs.merge(df_features, on="instance_id", how="left")
        # Map instance ID to group ID
        df["task_id"] = df["instance_id"].str.rsplit("/", n=1).str[0]
        # stable anonymous ids (random uuid4 ids changed the data on every run)
        df["task_id"] = anonymize_ids(df["task_id"])
        df["instance_id"] = anonymize_ids(df["instance_id"])
        df = df.drop(
            columns=[
                # Duplicated columns
                "Frac_Removed_Nogood-1",
                "Frac_Removed_Nogood-2",
            ]
        )
        df["runtime"] = np.log(df["runtime"])
        return df.reset_index(drop=True)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "task_id",
                "instance_id",  # scoring column only, never a feature
                "algorithm",  # the configuration's name; the scenario publishes no configuration features
                "Tight",  # whether the program is tight: a yes/no flag (CLEAN-14)
            ],
        )
