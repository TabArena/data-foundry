"""Curated dataset definition for `obesity_estimation` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class ObesityEstimation(AbstractCuratedDataset):
    # Dataset
    unique_name = "obesity_estimation"
    year = "2019"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5H31Z"
    license = "CC BY 4.0"
    download_description = """
        wget https://archive.ics.uci.edu/static/public/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition.zip && unzip estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition.zip && rm estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition.zip
        mkdir -p local-data-warehouse/obesity_estimation && mv *.csv local-data-warehouse/obesity_estimation/
    """
    bibtex = """
        @article{palechor2019dataset,
            title={Dataset for estimation of obesity levels based on eating habits and physical condition in individuals from Colombia, Peru and Mexico},
            author={Palechor, Fabio Mendoza and De la Hoz Manotas, Alexis},
            journal={Data in brief},
            volume={25},
            pages={104344},
            year={2019},
            publisher={Elsevier}
        }
    """
    curation_comments = """
        - We use only the real data, throwing away the SMOTE samples.
        - We make the task a regression task, re-creating the body mass values underlying the discretized obesity levels, and drop weight and height which leak the target partially. Thus, we create a regression task of estimating the body mass of individuals based on their eating habits and other questions from the questionnaire. The original task is trivial to solve due to the leak and thus not interesting.
    """

    # Task
    target = "BodyMass"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "ObesityDataSet_raw_and_data_sinthetic.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Filter to only real data (real data is int and not float values, see original .csv file)
        df = df.iloc[:498]
        # Creat real target
        df["BodyMass"] = df["Weight"] / (df["Height"] ** 2)
        df = df.drop(columns=["Height", "Weight", "NObeyesdad"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Gender",
                "family_history_with_overweight",
                "FAVC",
                "FCVC",
                "CAEC",
                "SMOKE",
                "SCC",
                "CALC",
                "MTRANS",
                "CH2O",
                "FAF",
                "TUE",
                "NCP",
            ],
        )
