"""Curated dataset definition for `heart_disease_hungary` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class HeartDiseaseHungary(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a patient examined for heart disease have narrowed coronary arteries?",
        use_case=(
            "For example, a cardiologist decides from routine and exercise-test results whether a patient needs "
            "coronary angiography, the invasive test that gives the diagnosis."
        ),
        row=(
            "One patient examined for coronary artery disease at the Hungarian Institute of Cardiology in Budapest "
            "(294 patients; published 1988, period not stated)."
        ),
        predicted=("Whether angiography shows more than 50% narrowing in any major coronary vessel (36% do)."),
        known=(
            "Age, sex, chest-pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, and "
            "the exercise test (maximum heart rate, angina, ST depression and, often missing, its slope); the "
            "fluoroscopy and thallium-scan results are missing for nearly all patients."
        ),
        split=("Random patients, so the test data stands for new patients of the same clinic and period."),
        changes="We merge the four disease grades into disease or none, as the original study did.",
        fit="direct",
        fit_reason=(
            "All features come from tests done before angiography, whose result is the label, as when deciding whom "
            "to refer. The data is small and old."
        ),
    )

    # Dataset
    unique_name = "heart_disease_hungary"
    year = "1988"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C52P4X"
    license = "CC BY 4.0"
    download_description = """
        Get the UCI data.

        wget https://archive.ics.uci.edu/static/public/45/heart+disease.zip && unzip heart+disease.zip processed.hungarian.data && rm heart+disease.zip && mkdir -p local-data-warehouse/heart_disease_hungary && mv processed.hungarian.data local-data-warehouse/heart_disease_hungary/
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
        - We make the target binary (0=no heart disease, 1=heart disease). This follows the original study in attempting to distinguish presence (values 1,2,3,4) from absence (value 0).
        - The data has one naturally occurring duplicate, which we do not drop.
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
        df = pd.read_csv(raw_dir / "processed.hungarian.data", header=None, names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.replace("?", np.nan)
        df[["ca", "trestbps", "thalach", "chol"]] = df[["ca", "trestbps", "thalach", "chol"]].astype(float)
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
