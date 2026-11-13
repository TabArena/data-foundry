"""Curated dataset definition for `sdss_17` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    Splits,
    TaskSummary,
    Temporal,
)

# The first day of each test window, newest first: 2019 and 2020 form one window (1 January 2019 to the end of the data,
# 24 March 2020), then the calendar years 2018 to 2012 (2026-11-12, Andrej).
WINDOW_STARTS = tuple(pd.Timestamp(f"{year}-01-01") for year in range(2019, 2011, -1))


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
            "The sky position, the brightness in five colour bands (u, g, r, i, z) from the survey's images and the "
            "camera column that took them. The date of the spectrum orders the split but is no model input: it "
            "arrives with the class."
        ),
        split=(
            "Later spectra: each year from 2012 to 2018, and January 2019 to March 2020 together, is predicted by a "
            "model trained on every spectrum taken before it, as the survey's classifier would be refit at each data "
            "release and used on the objects observed next."
        ),
        changes=(
            "We drop the redshift, fitted together with the class from the spectrum, and the plate and fibre, which "
            "record how the object was chosen for spectroscopy; the task is to classify from the images alone. We "
            "split by the year of the spectrum instead of at random, 2019 and 2020 in one window, and the date is no "
            "model input."
        ),
        fit="approximate",
        fit_reason=(
            "The features exist before a spectrum, but every row is an object the survey's targeting programmes "
            "already picked by its colours for a spectrum, so the mix of classes and colours is not that of the "
            "objects one would classify without one. Each programme picked its own kind of object, so the class mix "
            "of later years differs (quasars 15% of the spectra in 2010-2013, 31-46% from 2014)."
        ),
    )

    # Dataset
    unique_name = "sdss_17"
    domain = "physics & astronomy"
    sources = (
        Source(
            role="publication",
            platform="Other",  # SDSS Data Release 17; the Kaggle file is a cut of it
            url="https://www.sdss4.org/dr17/",
            license="Public Domain",  # SDSS data are public; the Kaggle cut says Data files © Original Authors
            year="2021",
            bibtex="""
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
            """,
        ),
        Source(
            role="copy",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/fedesoriano/stellar-classification-dataset-sdss17",
            license="Data files © Original Authors",
            name="the Kaggle cut we download",
        ),
    )
    download_description = """
        We download the data from Kaggle.

        mkdir -p local-data-warehouse/sdss_17/ && cd local-data-warehouse/sdss_17 && kaggle datasets download fedesoriano/stellar-classification-dataset-sdss17 && cd ../../ && unzip local-data-warehouse/sdss_17/stellar-classification-dataset-sdss17.zip -d local-data-warehouse/sdss_17 && rm local-data-warehouse/sdss_17/stellar-classification-dataset-sdss17.zip
    """
    curation_comments = """
        - We renamed the target feature.
        - We drop duplicate objects by sky position ("alpha", "delta"). The Kaggle CSV stores "obj_ID" as a rounded float, so deduplicating on it removed 21,947 distinct objects; by position there is a single object observed on two plates.
        - We dropped several (ID-like) meta-features that seem to be not part of the predictive task.
        - We drop "redshift". The SDSS pipeline fits the class and the redshift in the same step, and stars are only fitted within +-1200 km/s (Bolton et al. 2012, Sec. 3.1), so |redshift| <= 0.0041 identifies stars almost perfectly. The task is therefore photometric: classify an object from its position and u, g, r, i, z magnitudes.
        - "u", "g", "r", "i", "z" are the SDSS model magnitudes (equal to "MODELMAG" in the DR17 spectrum files), photometry from the survey's images. The spectra are not in the file: they set the label, class and redshift being two outputs of one template fit (Bolton et al. 2012). The spectra can be recovered from the DR17 archive by plate, night and fibre, but a spectral task would ask a model to redo the fit that gives its own label, so the task stays photometric (2026-11-11, Andrej).
        - We drop "plate" and "fiber_ID". A plate is one spectroscopic pointing (one or two nights, so it duplicates the observation date) designed for one targeting program, so it encodes how the object was pre-selected from photometry rather than what it is: 11% of rows sit on plates that are at least 99% one class, and plate and fiber alone give OvR ROC AUC 0.80. A new object has no plate before it is targeted, and the fiber number is only a slot on the plate. Adding both to the photometry also makes LightGBM worse (log loss 0.334 -> 0.404).
        - We set the sentinel -9999 (one row in u, g and z) to missing.
        - Split by the year of the spectrum instead of at random (2026-11-11, Andrej). Every row is a spectrum taken
          on a dated night (the raw file's "MJD", now the time column "date") through a plate drilled for one
          targeting programme, and the programmes changed what they observed: quasars are 3-11% of each year's
          spectra in 2000-2009, 14-16% in 2010-2013 and 31-46% from 2014 on. A classifier in use is trained on the
          spectra taken so far and labels objects the survey has not yet observed, so it has neither the test
          object's plate-mates nor the later programmes, which the random split gave it. Log loss on the 99,999
          objects, lower is better (untuned LightGBM with 500 trees, logistic regression, TabPFN 3.5 on 10,000
          training rows and up to 5,000 test rows, the sky position alone through the 50 nearest objects):

          | Split | Class shares | Position alone | Logistic regression | LightGBM, magnitudes only | LightGBM, as shipped | TabPFN 3.5 |
          |---|---|---|---|---|---|---|
          | random objects, 3 x 3 folds | 0.955 | 0.791 | 0.656 | 0.353 | 0.331 | 0.294 |
          | by plate, 3 x 3 folds | 0.956 | 0.901 | 0.657 | 0.354 | 0.338 | 0.292 |
          | by sky cell of 10 degrees, 3 x 3 folds | 0.957 | 0.992 | 0.663 | 0.357 | 0.354 | 0.301 |
          | by year, 9 windows 2012-2020 | 1.121 | 1.169 | 0.755 | 0.491 | 0.506 | 0.439 |

          The LightGBM columns of the last row leave the date out, as the shipped task does; logistic regression and
          TabPFN had it (untuned LightGBM with the date scores 0.540 against 0.506 without). The year row was
          measured on nine windows, 2019 and 2020 apart; the shipped split merges the two into one window (eight
          windows, `splits_comment`; 2026-11-12, Andrej), on which LightGBM's mean is 0.485, lower only because the
          2020 window alone is hard.

          On the same rows, the 48,743 spectra of 2012-2020, LightGBM scores 0.391 out of fold under the random split
          and 0.506 by year; on 2014 alone, the first eBOSS year, 0.441 against 0.530. Trained on a random draw of the
          other years (later ones included, as many rows), its loss on 2014 falls from 0.530 to 0.470 and on 2016 from
          0.501 to 0.444: part of what the random split buys is the later programmes. The sky position shows the same
          from the other side: added to the five magnitudes it lowers LightGBM's loss under the random split (0.353 to
          0.331) and raises it by year (0.491 to 0.506), because it teaches the sky footprints of past programmes. A
          split by plate or by sky cell removes the test object's plate-mates but still trains on later programmes,
          and the cell size sets the score (0.345 at 5 degrees, 0.373 at 20).
        - We keep "MJD" out of the features and bring it back only as the time column "date": a pointing id or an
          observation date encodes the pre-selection, not what the object is. The date orders and splits the rows
          and is no model input (`Temporal(..., feature=False)`, `feature_columns` leaves it out): the prediction
          point is an object imaged but not yet observed spectroscopically, and the date of its spectrum arrives
          with its class (2026-11-12, Andrej).
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

    # Splits: calendar-year windows with 2019 and 2020 merged (`_make_splits`); declared windows have one length
    temporal = Temporal(
        on="date",
        horizon=1,
        horizon_unit="years",
        feature=False,  # the date of the spectrum arrives with the class: no model input (2026-11-12, Andrej)
    )
    splits_comment = """
        Eight windows, newest first: 1 January 2019 to 24 March 2020, then the calendar years 2018 to 2012; each
        trains on every spectrum taken before it, as a classifier refit at each yearly data release (DR8, January
        2011, to DR16, December 2019) would. No gap: the pipeline's class comes with the spectrum, and a public user
        waits for the next release, which the one-year windows already stand in for.

        The windows train on 51.3% (2012) to 98.9% (2019-2020) of the 99,999 objects and hold 11,044, 9,843, 5,849,
        3,364, 4,873, 5,989, 6,705 and 1,076 spectra. The sizes follow DR17, of which the file holds 1.6% to 2.4% a
        year: BOSS used all the dark time until June 2014, eBOSS half of it until it ended on 1 March 2019,
        and 2020 holds only 7 eFEDS plates of X-ray sources (and 1 reverberation-mapping plate), observed before the
        observatory closed for COVID-19 on 24 March 2020. A 2020 window alone (141 spectra, 8 plates, one programme)
        gave untuned LightGBM's log loss a standard error of 0.083 against 0.008 to 0.025 in the other years, and 77%
        of the noise of the nine-window mean (standard error 0.0105). Merged with 2019 (1,076 spectra, 72 plates) the
        newest window's standard error is 0.024 and that of the eight-window mean 0.0056; every spectrum stays tested,
        the eFEDS ones included, and the newest window spans 15 months (2026-11-12, Andrej).

        The year also holds out the test object's plate, which the random split did not: 0 to 5 plates per window
        were also observed before it, at most 90 test rows (0.9% of the 2013 window).
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/star_classification.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "ObjectType"
        df = df.rename(columns={"class": target_feature})
        df = df.drop_duplicates(subset=["alpha", "delta"])
        df = df.replace(-9999, np.nan)
        # The night the spectrum was taken, as a date: the split's time column, never a pre-selection id (2026-11-11, Andrej).
        df["date"] = pd.to_datetime(df["MJD"], unit="D", origin=pd.Timestamp("1858-11-17"))
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
                "MJD",  # observation date, now the time column "date"
                "redshift",  # fitted together with the class by the spectroscopic pipeline
                "plate",  # spectroscopic pointing: observation date and targeting program
                "fiber_ID",  # slot on the plate
            ]
        )
        return df

    def _make_splits(self, df: pd.DataFrame) -> Splits:
        """The windows of `WINDOW_STARTS`, newest first, each training on every spectrum taken before its start."""
        dates = df["date"]  # the frame arrives sorted by date with a RangeIndex
        positions = np.arange(len(df))
        splits: Splits = {}
        end = None
        for start in WINDOW_STARTS:
            test = (dates >= start) & (dates < end) if end is not None else dates >= start
            train = dates < start
            splits[len(splits)] = {0: (positions[train.to_numpy()].tolist(), positions[test.to_numpy()].tolist())}
            end = start
        return splits

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # cam_col names which of the six camera columns took the image: a code, not a quantity (point 4, 2026-10-31)
        return FeatureTypes(categorical=["cam_col"], datetime=["date"])
