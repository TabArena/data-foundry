"""Curated dataset definition for `sdss_17` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


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
        - We drop duplicate objects by sky position ("alpha", "delta"). The Kaggle CSV stores "obj_ID" as a rounded float, so deduplicating on it removed 21,947 distinct objects; by position there is a single object observed on two plates.
        - We dropped several (ID-like) meta-features that seem to be not part of the predictive task.
        - We drop "redshift". The SDSS pipeline fits the class and the redshift in the same step, and stars are only fitted within +-1200 km/s (Bolton et al. 2012, Sec. 3.1), so |redshift| <= 0.0041 identifies stars almost perfectly. The task is therefore photometric: classify an object from its position and u, g, r, i, z magnitudes.
        - We drop "plate" and "fiber_ID". A plate is one spectroscopic pointing (one or two nights, so it duplicates the dropped MJD) designed for one targeting program, so it encodes how the object was pre-selected from photometry rather than what it is: 11% of rows sit on plates that are at least 99% one class, and plate and fiber alone give OvR ROC AUC 0.80. A new object has no plate before it is targeted, and the fiber number is only a slot on the plate. Adding both to the photometry also makes LightGBM worse (log loss 0.334 -> 0.404).
        - We set the sentinel -9999 (one row in u, g and z) to missing.
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
        df = df.drop_duplicates(subset=["alpha", "delta"])
        df = df.replace(-9999, np.nan)
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
                "redshift",  # fitted together with the class by the spectroscopic pipeline
                "plate",  # spectroscopic pointing: observation date and targeting program
                "fiber_ID",  # slot on the plate
            ]
        )
        return df
