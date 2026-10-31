"""Curated dataset definition for `sdss_17` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class Sdss17(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a sky object a galaxy, a star or a quasar, judging from its images alone?",
        use_case=(
            "For example, an astronomer classifies objects that have images but no spectrum, to choose targets for "
            "spectroscopy or to build catalogues."
        ),
        row=(
            "One object with a spectrum in the Sloan Digital Sky Survey's Data Release 17 (99,999 objects of a "
            "100,000-object sample shared on Kaggle)."
        ),
        predicted=(
            "The class the survey's spectroscopic pipeline assigned: galaxy (59.44%), star (21.59%) or quasar (18.96%)."
        ),
        known=(
            "The sky position, the brightness in five colour bands (u, g, r, i, z) from the survey's images, and the "
            "camera column that took them."
        ),
        split=("Random objects, so the test data stands for other objects chosen for spectra in the same way."),
        changes=(
            "We drop the redshift, fitted together with the class from the spectrum, and the plate and fibre, which "
            "record how the object was chosen for spectroscopy; the task is to classify from the images alone."
        ),
        fit="approximate",
        fit_reason=(
            "The features exist before a spectrum, but every row is an object the survey's targeting programmes "
            "already picked by its colours for a spectrum, so the mix of classes and colours is not that of the "
            "objects one would classify without one."
        ),
    )

    # Dataset
    unique_name = "sdss_17"
    year = "2021"
    domain = "physics & astronomy"
    source = "Other"  # SDSS Data Release 17; the Kaggle file is a cut of it
    source_url = "https://www.sdss4.org/dr17/"
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
    metric = Metric.fallback(
        reason=(
            "SDSS DR17 (Abdurro'uf et al. 2022) is a data release with no prediction task or metric; the "
            "Kaggle 'Stellar Classification Dataset - SDSS17' is a dataset page, not a competition, with no "
            "evaluation metric. Our task (photometric classification, redshift/plate/fiber dropped) also "
            "differs from the SDSS pipeline's spectroscopic classification."
        ),
    )

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

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # cam_col names which of the six camera columns took the image: a code, not a quantity (point 4, 2026-10-31)
        return FeatureTypes(categorical=["cam_col"])
