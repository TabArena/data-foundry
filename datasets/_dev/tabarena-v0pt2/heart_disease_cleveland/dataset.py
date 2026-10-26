"""Curated dataset definition for `heart_disease_cleveland` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class HeartDiseaseCleveland(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a patient with suspected heart disease have narrowed coronary arteries?",
        use_case=(
            "A cardiologist estimates a patient's chance of coronary artery disease from history and non-invasive "
            "tests, to decide on a coronary angiography (Detrano et al. 1989)."
        ),
        row=(
            "One of 303 patients of the Cleveland Clinic whose coronary arteries were examined by angiography (data "
            "donated in 1988)."
        ),
        predicted=(
            "Whether the angiography shows a narrowing of more than 50% of the diameter in any major vessel (46% do)."
        ),
        known=(
            "Age, sex, chest-pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, an "
            "exercise test (peak heart rate, chest pain on exercise, the ECG's ST depression and its slope), the "
            "number of major coronary arteries with calcium seen on cardiac fluoroscopy (0-3) and an exercise "
            "thallium scan."
        ),
        split=("Random patients, so the test data stands for new patients of the same clinic and years."),
        changes=("We merge the four grades of disease into one class, as the experiments on this data do."),
        fit="direct",
        fit_reason=(
            "The features come from history and tests that precede the angiography setting the label, including the "
            "fluoroscopy and the thallium scan, noninvasive tests done before it (Detrano et al. 1986). The patients "
            "are 303 of one clinic, 1988 or earlier."
        ),
    )

    # Dataset
    unique_name = "heart_disease_cleveland"
    year = "1988"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C52P4X"
    license = "CC BY 4.0"
    download_description = """
        Get the UCI data.

        wget https://archive.ics.uci.edu/static/public/45/heart+disease.zip && unzip heart+disease.zip processed.cleveland.data && rm heart+disease.zip && mkdir -p local-data-warehouse/heart_disease_cleveland && mv processed.cleveland.data local-data-warehouse/heart_disease_cleveland/
    """
    bibtex = """
        @article{detrano1989international,
          title={International application of a new probability algorithm for the diagnosis of coronary artery disease},
          author={Detrano, Robert and Janosi, Andras and Steinbrunn, Walter and Pfisterer, Matthias and Schmid, Johann-Jakob and Sandhu, Sarbjit and Guppy, Kern H and Lee, Stella and Froelicher, Victor},
          journal={The American journal of cardiology},
          volume={64},
          number={5},
          pages={304--310},
          year={1989},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        We start with the processed version and the subset of 14 attributes used in the study and clinical practice.

        - We encode missing values as np.nan instead of "?".
        - The vessel count `ca` is the number of major coronary arteries with calcium seen on cardiac cinefluoroscopy and `thal` an exercise thallium scan, both noninvasive tests before the angiography that sets the label (Detrano et al. 1986, PMID 3698241 and 3706156). Our data reproduces those papers' sensitivity and specificity (`ca` at least 1: 66.7% and 80.7%), so neither is read from the angiogram.
        - We make the target binary (0=no heart disease, 1=heart disease). This follows the original study in attempting to distinguish presence (values 1,2,3,4) from absence (value 0).
    """

    # Task
    target = "heart_disease_diagnosis"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Detrano et al. 1989 score reliability (calibration in the large) and clinical utility (percent correctly classified): two criteria, one of them about probabilities; no threshold or costs for the hard call. Original rejected: percent correctly classified. roc_auc is the binary fallback."
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "age",
            "sex",
            "cp",
            "trestbps",
            "chol",
            "fbs",
            "restecg",
            "thalach",
            "exang",
            "oldpeak",
            "slope",
            "ca",
            "thal",
            "num",
        ]
        df = pd.read_csv(raw_dir / "processed.cleveland.data", header=None, names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.replace("?", np.nan)
        df["ca"] = df["ca"].astype(float)
        # Make target
        df["heart_disease_diagnosis"] = (df["num"] > 0).astype(int)
        df = df.drop(columns=["num"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "thal",
                "slope",
                "exang",
                "restecg",
                "fbs",
                "cp",
                "sex",
            ],
        )
