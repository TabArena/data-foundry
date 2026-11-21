"""Curated dataset definition for `body_density_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Metric, Source, TaskSummary


class BodyDensityPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What is a man's body density, and so his body fat, judging from tape measurements, age, weight and height?"
        ),
        use_case=(
            "A gym or clinic estimates a person's body density, and from it the body fat, from simple measurements "
            "instead of weighing the person under water (the curator's notes)."
        ),
        row=("One of 252 men measured for a study of body-composition equations (Penrose et al. 1985)."),
        predicted=(
            "Body density measured by underwater weighing; the body-fat percentage follows from it by a fixed formula."
        ),
        known=(
            "Age, weight, height and ten circumferences (neck, chest, abdomen, hip, thigh, knee, ankle, biceps, "
            "forearm and wrist)."
        ),
        split="Random men, so the test data stands for new men like those of the study.",
        changes="We drop the body-fat percentage, which is computed from the density.",
        fit="direct",
        fit_reason=(
            "The features are the cheap measurements the use case has, and the label is the costly test they replace."
            " The sample is small and narrow: 252 men of one study published in 1985."
        ),
    )

    # Dataset
    unique_name = "body_density_prediction"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="Other",  # StatLib (Johnson's bodyfat file); later copies on OpenML and Kaggle
            url="https://lib.stat.cmu.edu/datasets/bodyfat",
            license="Free to distribute and use for non-commercial purposes (Dr. A. Garth Fisher's permission, in the StatLib file)",
            year="1995",
            bibtex=r"""
                @article{penrose1985generalized,
                  title={Generalized body composition prediction equation for men using simple measurement techniques},
                  author={Penrose, Keith W and Nelson, Arnold G and Fisher, Arnold Garth},
                  journal={Medicine \& Science in Sports \& Exercise},
                  volume={17},
                  number={2},
                  pages={189},
                  year={1985},
                  publisher={Ovid Technologies (Wolters Kluwer Health)}
                }
            """,
        ),
        Source(
            role="copy",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/fedesoriano/body-fat-prediction-dataset",
            license="Data files © Original Authors",
            name="the Kaggle copy we download",
        ),
        Source(
            role="copy",
            platform="OpenML",
            url="https://www.openml.org/d/560",
            license="Public",
            year="2014",
            name="OpenML 560",
        ),
    )
    data_tags = ("Timeless",)
    download_description = """
        We download the data from Kaggle.

        kaggle datasets download fedesoriano/body-fat-prediction-dataset && unzip body-fat-prediction-dataset.zip && rm body-fat-prediction-dataset.zip
        mkdir -p local-data-warehouse/body_density_prediction && mv bodyfat.csv local-data-warehouse/body_density_prediction/
    """
    curation_comments = """
        We start with the data from Kaggle.

        - Note, the task is not about bodyfat prediction as this is determined by a deterministic formula. Instead, the task is to estimate the density (which can be used to get the body fat via the deterministic formula). However, density requires a test. So we aim to predict from data the density such that we can skip this test. Which can make a lot of sense, if the test is too expensive as it requires underwater weighing.
        - Time basis: Timeless: each man was measured once (tape, scale and underwater weighing in one study at BYU,
          before 1985), so density and features describe the same body at one time; no date or order is recorded, and
          the derivation block of the first 143 cases does not differ from the rest. Not tested: bodies measured in
          another study, such as women or today's gym and clinic clients.
    """

    # Task
    target = "Density"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="standard error of estimate (SEE) of the prediction equation, with R / R^2",
        reference="Penrose, Nelson & Fisher 1985, Med Sci Sports Exerc 17(2):189; Johnson 1996, 'Fitting Percentage of Body Fat to Simple Body Measurements', Journal of Statistics Education 4(1) (StatLib bodyfat)",
        definition="root mean squared error of the predicted body density (g/cm3)",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "bodyfat.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Bodyfat leaks the density
        df = df.drop(columns=["BodyFat"])
        return df
