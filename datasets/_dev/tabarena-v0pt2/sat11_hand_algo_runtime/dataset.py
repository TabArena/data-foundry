"""Curated dataset definition for `sat11_hand_algo_runtime` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, anonymize_ids


class Sat11HandAlgoRuntime(AbstractCuratedDataset):
    # Dataset
    unique_name = "sat11_hand_algo_runtime"
    year = "2011"
    domain = "technology & internet"
    source = "ASlib"
    source_url = "https://github.com/coseal/aslib_data/tree/master/SAT11-HAND-ALGO"
    license = "GPLv3"
    download_description = """
        wget https://raw.githubusercontent.com/coseal/aslib_data/refs/heads/master/SAT11-HAND-ALGO/feature_values.arff && wget https://raw.githubusercontent.com/coseal/aslib_data/refs/heads/master/SAT11-HAND-ALGO/algorithm_feature_values.arff && wget https://raw.githubusercontent.com/coseal/aslib_data/refs/heads/master/SAT11-HAND-ALGO/algorithm_runs.arff && mkdir -p local-data-warehouse/sat11_hand_algo_runtime && mv feature_values.arff algorithm_feature_values.arff algorithm_runs.arff local-data-warehouse/sat11_hand_algo_runtime/
    """
    bibtex = """
        @inproceedings{xu-sat12a,
          author    = {L. Xu and F. Hutter and H. Hoos and K. Leyton-Brown},
          title     = {Evaluating Component Solver Contributions to Portfolio-Based Algorithm Selectors},
          pages     = {228-241},
          crossref  = {sat12}
        }
        @Proceedings{sat12,
          editor =         {A. Cimatti and R. Sebastiani},
          title =         {Proceedings of the Fifteenth International Conference on Theory and Applications of Satisfiability Testing (SAT'12)},
          booktitle = {Proceedings of the Fifteenth International Conference on Theory and Applications of Satisfiability Testing (SAT'12)},
          publisher =         springer,
          series =         lncs,
          volume =         7317,
          year =         2012
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

        - Algorithm selection can be solved with many methods (pairwise classification, hierarchical regression, multi-label, ...). We follow the concept from Pulatov et al. (https://proceedings.mlr.press/v188/pulatov22a.html) and learn one single, unified regression model that goes from (instance_features, algorithm_features) -> runtime.
        - The description says 'If features are "?", the instance was solved during feature computation.' but from the status file we can see that no task was presovled. So it is unclear what this is referring to. We believe that in all cases we have nan values for features, it is a case of the feature running into a memout, timeout, or crash as stated by the description.
        - The runtimes are right-censored: every run was stopped at the cutoff of 5,000 s, and a timeout is stored as a runtime of 5,000 s (the slowest finished run took 4,996 s, so `runtime == log(5000)` marks a timeout). A regression model and RMSE take that cutoff as the exact runtime, which biases predictions down (Hutter et al. 2014, section 9). We drop the 112 of 296 instances on which all 10 algorithms time out (1,120 rows): their labels are only lower bounds, and they cannot change which algorithm is selected (every choice costs the same; the single-best to virtual-best PAR10 gap is the same with or without them). We keep the 666 timeouts of the other 184 instances at the cutoff: selecting the fastest algorithm needs every algorithm's outcome, and the cutoff keeps the order within an instance (every finished run is faster) and is enough to compute PAR10.
        - A survival task type (a censoring indicator, a censoring-aware loss and metric) could use every run, including the 112 dropped instances, as survival-based algorithm selectors do (for example Run2Survive, Tornede et al. 2020). The raw files keep them; TabArena has no such task type yet.
        - We log scale the target.
        - We drop duplicated columns and remove features that leak the target or are not relevant for the predictive task.
    """

    # Task
    target = "runtime"
    problem_type = "regression"
    grouping = Grouping(
        on="instance_id",
        labels="per_sample",
        prediction_unit="group",
        aggregation="select_min",
        context="all_rows",
        definition="""
            One group is a SAT instance; its rows are the runs of the 10 candidate algorithms on it, described by instance and algorithm features, with the log runtime as the target. The use case is algorithm selection: predict every algorithm's runtime on a new instance and run the one predicted fastest (ASlib, Bischl et al. 2016; one model for all algorithms as in Pulatov et al. 2022), scored by the selected algorithm's true runtime (PAR10, or the share of the gap between the single best and the virtual best solver that is closed). The split holds out instances as ASlib's folds do; the instances also come in families, which the split does not separate.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        def load_arff(path) -> pd.DataFrame:
            with open(path, encoding="utf-8") as f:
                data = arff.load(f)
            df = pd.DataFrame(data["data"], columns=[a[0] for a in data["attributes"]])
            return df

        df_features = load_arff(raw_dir / "feature_values.arff")
        df_algo_features = load_arff(raw_dir / "algorithm_feature_values.arff")
        df_algo_runs = load_arff(raw_dir / "algorithm_runs.arff")
        return {"df_features": df_features, "df_algo_features": df_algo_features, "df_algo_runs": df_algo_runs}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df_features, df_algo_features, df_algo_runs = raw["df_features"], raw["df_algo_features"], raw["df_algo_runs"]
        # Drop algorithms that for which we do not have features
        df_algo_runs = df_algo_runs[df_algo_runs["algorithm"].isin(df_algo_features["algorithm"].unique())]
        # Drop instances that no algorithm solves: all their runtimes are the censored cutoff
        solved = df_algo_runs.loc[df_algo_runs["runstatus"] == "ok", "instance_id"].unique()
        df_algo_runs = df_algo_runs[df_algo_runs["instance_id"].isin(solved)]
        # Merge
        df = df_algo_runs.merge(df_features, on="instance_id", how="left").merge(
            df_algo_features, on="algorithm", how="left"
        )
        # Sanitize ID
        # Create mapping: molecule -> random string id
        # stable anonymous ids (random uuid4 ids changed the data on every run)
        df["instance_id"] = anonymize_ids(df["instance_id"])
        # Drop features
        df = df.drop(
            columns=[
                # Data has no repetitions
                "repetition_x",
                "repetition_y",
                "repetition",
                # We want to only rely on algorithm meta features not names.
                "algorithm",
                # Leaks target
                "runstatus",
                # Duplicated columns
                "clustering_min",
                "edge_ta",
                "edge_to",
                "edge_tl",
                "edge_da",
                "edge_do",
                "edge_dl",
                "edge_as",
                "edge_aa",
                "edge_ao",
                "edge_al",
                "edge_ot",
                "edge_oa",
                "edge_ol",
                "edge_lt",
                "edge_la",
                "edge_ll",
                "degree_min",
                "path_min",
                "VCG_VAR_mean",
                "edge_at",
            ]
        )
        df["runtime"] = np.log(df["runtime"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "instance_id",
            ],
        )
