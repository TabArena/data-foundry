"""Curated dataset definition for `sdss_17` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class Sdss17(AbstractCuratedDataset):
    # Dataset
    unique_name = "sdss_17"
    year = "2022"
    domain = "physics & astronomy"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/fedesoriano/stellar-classification-dataset-sdss17"
    license = "Public Domain"  # On Kaggle it says Data files © Original Authors which is under public domain.
    download_description = """
        We download the data from Kaggle.

        mkdir -p local-data-warehouse/sdss_17/ && cd local-data-warehouse/sdss_17 && kaggle datasets download fedesoriano/stellar-classification-dataset-sdss17 && cd ../../ && unzip local-data-warehouse/sdss_17/stellar-classification-dataset-sdss17.zip -d local-data-warehouse/sdss_17 && rm local-data-warehouse/sdss_17/stellar-classification-dataset-sdss17.zip
    """
    bibtex = """
        @article{accetta2022seventeenth,
          title={The seventeenth data release of the Sloan Digital Sky Surveys: Complete release of MaNGA, MaStar, and APOGEE-2 data},
          author={Accetta, Katherine and Aerts, Conny and Aguirre, Victor Silva and Ahumada, Romina and Ajgaonkar, Nikhil and Ak, N Filiz and Alam, Shadab and Prieto, Carlos Allende and Almeida, Andres and Anders, Friedrich and others},
          journal={The Astrophysical Journal Supplement Series},
          volume={259},
          number={2},
          pages={35},
          year={2022},
          publisher={IOP Publishing}
        }
    """
    curation_comments = """
        - We renamed the target feature.
        - We dropped duplicates based on "obj_ID" to avoid target leakage from subgroups.
        - We dropped several (ID-like) meta-features that seem to be not part of the predictive task.
    """

    # Task
    target = "ObjectType"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/star_classification.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "ObjectType"
        df = df.rename(columns={"class": target_feature})
        df = df.drop_duplicates(subset=["obj_ID"])
        # Note: the following is from a very naive domain knowledge perspective
        # and should be checked with domain experts. But otherwise, the predictive task
        # might leak. So we are better safe than sorry.
        df = df.drop(
            columns=[
                "obj_ID",  # should not be predictive, also has duplicates?
                "spec_obj_ID",  # ID
                "run_ID",  # should not be predictive but might indicate confounding noise
                "rerun_ID",  # constant
                "field_ID",  # might indicate clusters/subgroups of data?
                "MJD",  # date of observation, should not be predictive?
            ]
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "plate",
                "fiber_ID",
            ],
        )
