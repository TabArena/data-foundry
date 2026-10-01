"""Curated dataset definition for `asp_potassco_classification` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, anonymize_ids


class AspPotasscoClassification(AbstractCuratedDataset):
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

        - We treat it as a multiclass classification task to solve the algorithm selection task as in the OpenML version (https://openml.org/d/41705).
        - We drop all cases where no algorithm was able to finish before the timeout as these are essentially random labels.
        - We resole the instance ID to a task ID by mapping the instance ID back to the source task based on their naming convention. From our understanding, the data contains multiple instance from the same solver task, differing only in seed or task configurations. We want to avoid having samples from the same task in both train and test set, as this would leak what algorithms are best for this task, and since in real-world you might not have samples from your new task. Thus, we treat the data as a grouped task, where we aim to generalize the predicting the best algorithm to new tasks across a set of instances of this task.
    """

    # Task
    target = "algorithm"
    problem_type = "multiclass_classification"
    group_on = "task_id"
    group_labels = "per_sample"

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
        # Only keep instances for which we have meaningful labels
        df_algo_runs = df_algo_runs[df_algo_runs["runstatus"] == "ok"]
        # Reduce to best algorithm per instance
        df_algo_runs = df_algo_runs.loc[
            df_algo_runs.groupby("instance_id")["runtime"].idxmin(), ["instance_id", "algorithm"]
        ].reset_index(drop=True)
        # Merge
        df = df_algo_runs.merge(df_features, on="instance_id", how="left")
        # Map instance ID to group ID
        df["task_id"] = df["instance_id"].str.rsplit("/", n=1).str[0]
        # stable anonymous ids (random uuid4 ids changed the data on every run)
        df["task_id"] = anonymize_ids(df["task_id"])
        df = df.drop(
            columns=[
                "instance_id",
                # Duplicated columns
                "Frac_Removed_Nogood-1",
                "Frac_Removed_Nogood-2",
            ]
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "task_id",
            ],
        )
