"""Curated dataset definition for `obesity_estimation` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class ObesityEstimation(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is a person's body mass index, judged from eating habits and lifestyle alone?",
        use_case=(
            "For example, a health app or survey estimates a person's body mass index from eating and activity "
            "habits, to flag a risk of overweight without asking for weight and height (the source aims at tools that"
            " identify obesity levels from such habits)."
        ),
        row=(
            "One respondent to a web questionnaire in Mexico, Peru or Colombia (498 people, the source's real "
            "answers); the period is not stated."
        ),
        predicted=(
            "The body mass index (weight over height squared) from the reported weight and height; mean 24.3, range "
            "13.3 to 49.5."
        ),
        known=(
            "Sex, age, family history of overweight, and answers on eating (high-calorie food, vegetables, main "
            "meals, snacking, water, alcohol, calorie counting), smoking, physical activity, screen time and usual "
            "transport."
        ),
        split="Random respondents of the same survey.",
        changes=(
            "We drop the 77% synthetic rows the source made by oversampling, and predict the body mass index instead "
            "of the obesity level built from it; we drop weight and height, which gave the level away."
        ),
        fit="approximate",
        fit_reason=(
            "A body mass index is measured with a scale and a tape in a minute, so estimating it from habits only "
            "fits a setting that cannot ask for weight and height. The respondents are web volunteers, and the habits"
            " are reported at the same time as the weight."
        ),
    )

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
        - We use only the real data, throwing away the SMOTE samples. The real answers are the first 498 rows: their class counts equal Fig. 1 of the data paper (Palechor & De la Hoz 2019), and all its Normal_Weight rows are among them. A filter on whole-number values would let in 15 synthetic rows, so we cut by position.
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
        # The first 498 rows are the source's real answers, the SMOTE rows follow (see curation_comments)
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
