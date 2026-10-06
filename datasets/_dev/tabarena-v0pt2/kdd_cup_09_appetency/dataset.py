"""Curated dataset definition for `kdd_cup_09_appetency` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class KddCup09Appetency(AbstractCuratedDataset):
    # Dataset
    unique_name = "kdd_cup_09_appetency"
    year = "2008"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://kdd.org/kdd-cup/view/kdd-cup-2009/Data"
    license = "Public Domain"
    download_description = """
        We download the data and the labels from the KDD challenge website:

        mkdir -p local-data-warehouse/kdd_cup_09_appetency && wget -P local-data-warehouse/kdd_cup_09_appetency https://kdd.org/cupfiles/KDDCupData/2009/orange_small_train.data.zip && unzip local-data-warehouse/kdd_cup_09_appetency/orange_small_train.data.zip -d local-data-warehouse/kdd_cup_09_appetency/ && rm local-data-warehouse/kdd_cup_09_appetency/orange_small_train.data.zip && wget -P local-data-warehouse/kdd_cup_09_appetency https://kdd.org/cupfiles/KDDCupData/2009/orange_small_train_appetency.labels
    """
    bibtex = r"""
        @inproceedings{guyon2009analysis,
          title={Analysis of the kdd cup 2009: Fast scoring on a large orange customer database},
          author={Guyon, Isabelle and Lemaire, Vincent and Boull{\'e}, Marc and Dror, Gideon and Vogel, David},
          booktitle={KDD-Cup 2009 Competition},
          pages={1--22},
          year={2009},
          organization={PMLR}
        }
    """
    curation_comments = """
        - We use the small training data from the original data (230 features).
        - We use appetency as label.
        - We dropped empty columns: "Var8", "Var15", "Var20", "Var31", "Var32", "Var39", "Var42", "Var48", "Var52", "Var55", "Var79", "Var141", "Var167", "Var169", "Var175", "Var185", "Var209", "Var230".
        - Anomaly: the feature names and categorical feature values have no semantic meaning.
        - Anomaly: this dataset has many missing values.
    """

    # Task
    target = "Appetency"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "orange_small_train.data", sep="\t")
        df_y = pd.read_csv(raw_dir / "orange_small_train_appetency.labels", header=None)
        return {"df": df, "df_y": df_y}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, df_y = raw["df"], raw["df_y"]
        target_feature = "Appetency"
        df[target_feature] = df_y[0]
        empty_cols = [
            "Var8",
            "Var15",
            "Var20",
            "Var31",
            "Var32",
            "Var39",
            "Var42",
            "Var48",
            "Var52",
            "Var55",
            "Var79",
            "Var141",
            "Var167",
            "Var169",
            "Var175",
            "Var185",
            "Var209",
            "Var230",
        ]
        df.drop(columns=empty_cols, inplace=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Var192",
                "Var193",
                "Var194",
                "Var195",
                "Var196",
                "Var197",
                "Var198",
                "Var199",
                "Var200",
                "Var201",
                "Var202",
                "Var203",
                "Var204",
                "Var205",
                "Var206",
                "Var207",
                "Var208",
                "Var210",
                "Var211",
                "Var212",
                "Var214",
                "Var216",
                "Var217",
                "Var218",
                "Var219",
                "Var220",
                "Var222",
                "Var223",
                "Var225",
                "Var226",
                "Var227",
                "Var228",
                "Var229",
                "Var191",
                "Var213",
                "Var215",
                "Var221",
                "Var224",
            ],
        )
