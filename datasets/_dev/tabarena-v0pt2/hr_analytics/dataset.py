"""Curated dataset definition for `hr_analytics` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, drop_columns

RAW_FILE = "train_jqd04QH.csv"
"""The hackathon's train file: 18,359 enrollees with labels, 2,425 of them looking for a job change."""


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "education_level": ["Primary School", "High School", "Graduate", "Masters", "Phd"],
    "experience": [
        "<1",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        ">20",
    ],  # open-ended
    "company_size": ["<10", "10/49", "50-99", "100-500", "500-999", "1000-4999", "5000-9999", "10000+"],  # open-ended
    "last_new_job": ["never", "1", "2", "3", "4", ">4"],  # open-ended
}


class HrAnalytics(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a person who signed up for a data-science training looking for a new job?",
        use_case=(
            "A training institute for data science that also recruits for its clients wants to know which of the "
            "people signing up for its trainings are really looking for a new job, before it puts them in touch with "
            "clients hiring data scientists (the contest's framing)."
        ),
        row=(
            "One person enrolled in the institute's trainings, from an Analytics Vidhya hackathon of July 2018 (18,359"
            " enrollees); institute, place and period not stated."
        ),
        predicted=(
            "Whether the enrollee is looking for a job change (13.21% are); how and when this was recorded is not "
            "stated."
        ),
        known=(
            "City (coded) and its development index, gender, education level and field, university enrolment, years "
            "of experience and whether it is relevant, current employer's size and type, years between the previous "
            "and the current job, and training hours completed."
        ),
        split="Random enrollees, so the test data stands for other enrollees of the same trainings.",
        changes=(
            "We use the hackathon's own train file instead of Kaggle's 2020 copy, which adds 2,623 rows of the "
            "hackathon's unlabelled test file, all labelled as looking for a job change."
        ),
        fit="approximate",
        fit_reason=(
            "The label has no stated source or timing (a stated intention or an actual search), and training hours "
            "completed are only known some time after sign-up. The use case is plausible, but the data does not show "
            "when each fact was recorded."
        ),
    )

    # Dataset
    unique_name = "hr_analytics"
    year = "2018"
    domain = "business & marketing"
    source = "Other"  # Analytics Vidhya's DataHack hackathon Student DataFest 2018: The Data Supremacy, 6-22 July 2018
    source_url = "https://www.analyticsvidhya.com/datahack/contest/the-data-supremacy"
    license = None  # neither contest page states one; Kaggle's 2020 copy is marked CC0 by its uploader
    data_tags = ("Spatial",)
    download_description = """
        We download the train file of Analytics Vidhya's Student DataFest 2018: The Data Supremacy (DataHack, 6 to 22
        July 2018) from the link on the contest page; the page of JanataHack: HR Analytics (May 2020) links the same
        file. The contest's test file (test_GYi4Gz5.csv, 15,021 enrollees) has no labels and is not used.
        train_jqd04QH.csv: md5 17c9aca783a7f53040e7498c20be5729,
        sha256 591b300fcc58356f4b142f4b978ad42168f0a76663596d086a9592ccbb3a946c

        mkdir -p local-data-warehouse/hr_analytics && cd local-data-warehouse/hr_analytics
        curl -fLO https://datahack-prod.s3.amazonaws.com/train_file/train_jqd04QH.csv
    """
    bibtex = r"""
        @misc{analyticsvidhya2018datasupremacy,
          author = {{Analytics Vidhya}},
          title = {Student DataFest 2018: The Data Supremacy},
          year = {2018},
          howpublished = {\url{https://www.analyticsvidhya.com/datahack/contest/the-data-supremacy}},
          note = {DataHack hackathon, 6--22 July 2018; the files ran again as JanataHack: HR Analytics in May 2020.
                  Kaggle's 2020 copy (HR Analytics: Job Change of Data Scientists) adds rows of the unlabelled test
                  file, all labelled 1}
        }
    """
    curation_comments = """
        We start with train_jqd04QH.csv, the train file of Analytics Vidhya's Student DataFest 2018: The Data
        Supremacy (DataHack, July 2018). The same files ran again as JanataHack: HR Analytics (May 2020).

        - Source: the record links Kaggle's "HR Analytics: Job Change of Data Scientists" (arashnic, 2020). Its
          `aug_train.csv` is 16,535 rows of this file (labels unchanged) plus 2,623 rows of the contest's unlabelled
          test file, all labelled 1. We use the contest's file instead (Lennart, 2026-10-14).
        - Why: the added labels look made up. 89% of city_21's test rows became positives against 27% in this file,
          and a model trained on this file separates the added rows from the other test rows with ROC AUC 0.93. They
          lift a quick model's CV ROC AUC from 0.66 to 0.80 (record, 2026-10-14).
        - Prediction point: sign-up for the training. The contest asks for "the probability of an enrollee to look for
          a new job" from "the current credentials/demographics/experience"; how and when the label was recorded is
          not stated.
        - We drop `enrollee_id`, unique per row; JanataHack's rules forbid it as a feature.
        - `training_hours` is the training completed, so it is known only some time after sign-up. Kept, as in the
          contest.
        - Features as published: city and the answers stay categories, including `experience`, `company_size` and
          `last_new_job` (values such as "<1", ">20", "10/49", "never"). The target is renamed `LookingForJobChange`
          and maps 0/1 to No/Yes.
        - Missing values stay missing (company type 27%, company size 26%, gender 22%, major 15%).
        - Duplicates: without the ID, 45 rows repeat an earlier row and 17 feature vectors carry both labels. They
          belong to different enrollees and stay.
        - IID split: one row per enrollee and no dates.
        - Note: the task probes flag `no_spread` (ROC AUC LightGBM 0.625, linear 0.622, random forest 0.619; LightGBM
          +0.012 over random forest, paired SE 0.006). We keep the task: a real signal with a low ceiling (Lennart,
          2026-10-14).
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 4 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`); 1 hold a state outside the scale, placed by the
          curator's rule (missing when the column has no other missing value, else the lowest level; a state that is
          simply not on the scale, such as Other, is missing).
    """

    # Task
    target = "LookingForJobChange"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC-ROC",
        reference="https://www.analyticsvidhya.com/datahack/contest/the-data-supremacy (also https://www.analyticsvidhya.com/datahack/contest/janatahack-hr-analytics)",
        definition="Area under the ROC curve on the probability that an enrollee looks for a job change.",
    )
    accepted_check_warnings = {
        "meta_license_unknown": (
            "Neither contest page (The Data Supremacy, 2018; JanataHack: HR Analytics, 2020) states a licence: they "
            'give participation rules only ("Use of external dataset is not allowed for creating model", "In case of '
            "any dispute, decision of Analytics Vidhya shall be final\") and link the site's general Terms & "
            "Conditions. Kaggle's 2020 copy is marked CC0 by its uploader, who did not make the data."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # the enrollee ID is unique per row; JanataHack's rules forbid it as a feature
        df = drop_columns(raw, ["enrollee_id"])
        # data dictionary: "0 - Not looking for job change, 1 - Looking for a job change"
        df = df.rename(columns={"target": self.target})
        df[self.target] = df[self.target].map({1: "Yes", 0: "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "city",
                "gender",
                "relevent_experience",
                "enrolled_university",
                "education_level",
                "major_discipline",
                "experience",
                "company_size",
                "company_type",
                "last_new_job",
            ],
        )
