"""Curated dataset definition for `sat11_hand_algo_runtime` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import arff
import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, anonymize_ids


class Sat11HandAlgoRuntime(AbstractCuratedDataset):
    # Dataset
    unique_name = "sat11_hand_algo_runtime"
    year = "2011"
    domain = "technology & internet"
    source = "ASlib"
    source_url = "https://github.com/coseal/aslib_data/tree/master/SAT11-HAND"
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
        - This regression task is special as it contains censored regression values (capped to some max value) and the model needs to learn this.
        - We log scale the target.
        - We drop duplicated columns and remove features that leak the target or are not relevant for the predictive task.
    """

    # Task
    target = "runtime"
    problem_type = "regression"
    group_on = "instance_id"
    group_labels = "per_sample"

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
