"""Curated dataset definition for `heart_disease_va_long_beach` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class HeartDiseaseVaLongBeach(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a patient with suspected heart disease have narrowed coronary arteries?",
        use_case=(
            "For example, after the exercise test, a cardiologist estimates whether a patient has coronary artery "
            "disease, to decide on coronary angiography; the source built a probability algorithm for this diagnosis "
            "(Detrano et al. 1989)."
        ),
        row=(
            "One patient examined for coronary artery disease at the Veterans Administration Medical Center in Long "
            "Beach, California (200 patients; period not stated)."
        ),
        predicted=(
            "Whether the angiogram shows coronary artery disease, a narrowing of more than 50% in a major vessel; "
            "74.5% of these patients have it."
        ),
        known=(
            "Age, sex, chest-pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG and the"
            " exercise test (maximum heart rate, angina during exercise, ST depression and its slope); fluoroscopy "
            "and thallium-scan results are missing for most patients."
        ),
        split="Random patients of the same hospital.",
        changes="We merge the four grades of disease into present or absent, as the study does.",
        fit="direct",
        fit_reason=(
            "The features come from the examination and the noninvasive tests done before angiography, and the label "
            "is the angiogram. The sample is small, and the share with disease is high, as among patients sent to "
            "angiography."
        ),
    )

    # Dataset
    unique_name = "heart_disease_va_long_beach"
    year = "1988"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C52P4X"
    license = "CC BY 4.0"
    download_description = """
        Get the UCI data.

        wget https://archive.ics.uci.edu/static/public/45/heart+disease.zip && unzip heart+disease.zip processed.va.data && rm heart+disease.zip && mkdir -p local-data-warehouse/heart_disease_va_long_beach && mv processed.va.data local-data-warehouse/heart_disease_va_long_beach/
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
        - Proxy missing values: cholesterol is 0 in 49 of 200 rows and resting blood pressure in 1, both impossible and undocumented (the names file lists only -9); the zeros sit in one block of records (1984-85 exercise tests) and do not relate to the label (75.5% disease against 73.6%), so they become missing.
        - We make the target binary (0=no heart disease, 1=heart disease). This follows the original study in attempting to distinguish presence (values 1,2,3,4) from absence (value 0).
        - The dataset has one naturally occurring duplicate, which we do not drop.
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
        df = pd.read_csv(raw_dir / "processed.va.data", header=None, names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.replace("?", np.nan)
        df[["ca", "trestbps", "thalach", "oldpeak", "chol"]] = df[
            ["ca", "trestbps", "thalach", "oldpeak", "chol"]
        ].astype(float)
        # Proxy missing values: a cholesterol or resting blood pressure of 0 is impossible (an undocumented missing code)
        df[["chol", "trestbps"]] = df[["chol", "trestbps"]].replace(0, np.nan)
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
