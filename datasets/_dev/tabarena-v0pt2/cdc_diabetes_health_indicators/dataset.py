"""Curated dataset definition for `cdc_diabetes_health_indicators` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary

RAW_FILE = "diabetes_012_health_indicators_BRFSS2015.csv"
"""Teboul's three-class file; the two binary files of the same Kaggle dataset are not used."""

LABELS = {0: "No diabetes", 1: "Prediabetes", 2: "Diabetes"}
"""Diabetes_012 as Teboul's notebook codes BRFSS DIABETE3: 2 and 3 to 0, 4 to 1, 1 to 2 (7 and 9 removed)."""


class CdcDiabetesHealthIndicators(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Has this adult been told they have diabetes or prediabetes, judging from their other answers to a health"
            " survey?"
        ),
        use_case=(
            "A screening questionnaire, as the notes set it: for example, a health service decides from a few survey "
            "answers which adults to send for a diabetes blood test."
        ),
        row=(
            "One adult interviewed in the CDC's 2015 BRFSS health survey who answered all 22 selected questions "
            "(253,680 of 441,456 respondents, unweighted)."
        ),
        predicted=(
            "Which answer the adult gave: diabetes (13.9%), prediabetes (1.8%) or neither (84.2%). Diabetes only "
            "during pregnancy counts as neither, and prediabetes holds only those who volunteered it."
        ),
        known=(
            "21 other answers: blood pressure, cholesterol and its last check, body-mass index, smoking, stroke, "
            "heart disease, exercise, fruit and vegetables, heavy drinking, health cover and cost barriers, general, "
            "mental and physical health, difficulty walking, sex, age group, education and income."
        ),
        split="Random respondents of the same survey year, standing for new respondents.",
        fit="approximate",
        fit_reason=(
            "The label is a diagnosis received a median of 10 years before the interview, so the answers mostly "
            "describe life after it, not the undiagnosed adults a screening looks for. Without the answers most "
            "affected, the ROC AUC of diabetes against the rest drops by at most 0.0014."
        ),
    )

    # Dataset
    unique_name = "cdc_diabetes_health_indicators"
    year = "2016"
    domain = "medical & healthcare"
    source = "GOV Website"  # the CDC's BRFSS 2015 survey; we download a Kaggle cut of it
    source_url = "https://www.cdc.gov/brfss/annual_data/annual_2015.html"
    license = "CC0: Public Domain"
    download_description = """
        We download Alex Teboul's Kaggle dataset (one version, files of 2021-11-08, CC0) and keep the three-class
        file; the two binary files of the zip are not used. The file is a cut of the CDC's BRFSS 2015 survey data
        (https://www.cdc.gov/brfss/annual_data/annual_2015.html), made with Teboul's public notebook from the CDC's
        2015 file.
        diabetes_012_health_indicators_BRFSS2015.csv: sha256 a971809d0786d2d7d7f6070f83dfe8af9d860ea33a79e0e2701c8a49f78f9861

        mkdir -p local-data-warehouse/cdc_diabetes_health_indicators && cd local-data-warehouse/cdc_diabetes_health_indicators
        kaggle datasets download alexteboul/diabetes-health-indicators-dataset
        unzip diabetes-health-indicators-dataset.zip diabetes_012_health_indicators_BRFSS2015.csv && rm diabetes-health-indicators-dataset.zip
    """
    bibtex = r"""
        @misc{teboul2021diabetes,
          author = {Teboul, Alex},
          title = {Diabetes Health Indicators Dataset},
          year = {2021},
          howpublished = {\url{https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset}},
          note = {Kaggle dataset; a cleaned subset of the CDC Behavioral Risk Factor Surveillance System (BRFSS) 2015}
        }
    """
    curation_comments = """
        We start with diabetes_012_health_indicators_BRFSS2015.csv from Alex Teboul's Kaggle dataset, a cut of the CDC's BRFSS 2015 survey made with his public notebook; we use it as published, as the record decided.

        - Prediction point: a screening questionnaire. From the other answers of the same BRFSS interview, the model estimates whether the adult has been told they have diabetes or prediabetes.
        - The label is a lifetime diagnosis (a median of 10 years before the interview), so the answers about the present mostly describe life after it. We keep every answer, as Xie et al. 2019 do on BRFSS 2014: without the care-contact, lifestyle or complication answers the ROC AUC of diabetes against the rest drops by at most 0.0014 from 0.829.
        - Target: the three classes of Diabetes_012, renamed Diabetes with readable labels. No diabetes includes diabetes only during pregnancy, and Diabetes is any type.
        - Note: Prediabetes holds only the respondents who volunteered "pre-diabetes" to the diabetes question; where the pre-diabetes module was asked, 14% to 23% of the respondents told they have prediabetes are in the class. The class still carries a weak signal (one-vs-rest ROC AUC 0.700), so the record's three classes stay (first decision table).
        - Cohort: Teboul's notebook keeps the 253,680 of 441,456 respondents who answered all 22 selected questions, which the record accepts. The cholesterol question is not asked of respondents never checked, so none is kept, and CholCheck = 0 means the last check was five or more years ago. The diabetes share moves from 13.0% to 13.9%.
        - Features: the 21 answers as published; yes/no flags stay 0/1 and the ordinal codes (GenHlth, Age, Education, Income) stay numeric, as their order is their meaning. We cast the file's floats to integers and map Sex to Female/Male (categorical).
        - Duplicates: we keep the 23,899 rows that repeat an earlier row (decision table). They are different respondents (state and sequence number are unique in the raw file) with the same answers to 21 coarse questions.
        - Note: the notebook does not select the survey weights, so the rows are the unweighted sample.
        - Anomaly: 599 rows have a BMI of 70 or more (self-reported height and weight); we keep them.
        - IID split: each row is a different adult of one survey wave, and a model is used for new respondents.
        - Licence: CC0 on Kaggle; BRFSS data are public-domain CDC material.
    """

    # Task
    target = "Diabetes"
    problem_type = "multiclass_classification"
    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Each row is a different BRFSS respondent (state and sequence number are unique in the raw survey file); "
            "identical answers to 21 coarse questions are expected and kept (curation_comments, Duplicates)."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # the file stores every value as a float; all are whole numbers without missing values
        features = [c for c in df.columns if c != "Diabetes_012"]
        df[features] = df[features].astype("int64")
        df["Sex"] = df["Sex"].map({0: "Female", 1: "Male"})
        # the three-class label (the record's choice) with readable names
        df = df.rename(columns={"Diabetes_012": self.target})
        df[self.target] = df[self.target].astype("int64").map(LABELS)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["Sex"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        label = raw["Diabetes_012"].astype("int64")
        adult30 = raw["Age"].ge(3)  # age bands 1 and 2 are 18-24 and 25-29
        versions = pd.DataFrame(
            {
                "No diabetes": [
                    int(label.eq(0).sum()),
                    int(label.le(1).sum()),
                    int((label.eq(0) & adult30).sum()),
                ],
                "Prediabetes": [int(label.eq(1).sum()), 0, 0],
                "Diabetes": [
                    int(label.eq(2).sum()),
                    int(label.eq(2).sum()),
                    int((label.eq(2) & adult30).sum()),
                ],
            },
            index=[
                "Three classes (shipped; Teboul's Diabetes_012)",
                "Binary, prediabetes as no diabetes (Teboul's binary files, UCI 891)",
                "Binary, prediabetes and ages below 30 left out (Xie et al. 2019)",
            ],
        )
        versions["rows"] = versions.sum(axis=1)

        features = [c for c in df.columns if c != self.target]
        repeats = df.duplicated(keep="first")
        vectors = df.groupby(features, sort=False, observed=True)[self.target].transform("nunique")
        duplicates = pd.DataFrame(
            {
                "rows": df[self.target].value_counts(sort=False),
                "repeat an earlier row": df.loc[repeats, self.target].value_counts(sort=False),
                "in a feature vector with several labels": df.loc[vectors.gt(1), self.target].value_counts(sort=False),
            }
        ).reindex(list(LABELS.values()))
        duplicates.loc["all"] = duplicates.sum()
        return [
            Decision(
                "Three-class target, as the record decided",
                "The record keeps prediabetes as its own class. The other versions in use, built from the same file: "
                "Teboul's binary files, and Xie et al. 2019 (Methods, Data analysis: \"Respondents younger than 30 "
                'years were excluded [...] as were respondents with prediabetes").',
                versions,
            ),
            Decision(
                "Duplicate rows kept",
                "Each row is a different respondent; identical answers to 21 coarse questions are expected, also "
                "with different labels.",
                duplicates,
            ),
        ]
