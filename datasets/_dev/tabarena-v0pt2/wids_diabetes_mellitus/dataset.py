"""Curated dataset definition for `wids_diabetes_mellitus` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class WidsDiabetesMellitus(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a patient admitted to intensive care have diabetes?",
        use_case=(
            "In the first day of an ICU stay, when the patient's verified medical history is often not at hand, the "
            "care team estimates whether the patient has diabetes, to inform treatment (WiDS Datathon 2021)."
        ),
        row=(
            "One admission to an intensive care unit of 204 hospitals in MIT's GOSSIS data (127,358 admissions; "
            "period not stated)."
        ),
        predicted="Whether the patient has been diagnosed with diabetes mellitus; 21.6% have.",
        known=(
            "Age, sex, ethnicity, height, weight and BMI, how and why the patient was admitted, other chronic "
            "conditions, the vital signs and lab values of the first hour and day, the worst first-day values of a "
            "standard severity score, and the hospital and unit."
        ),
        split=("Random admissions, so the test data stands for new patients of the same hospitals and units."),
        fit="direct",
        fit_reason=(
            "Everything the model sees is recorded within the first day in the ICU, and the label is a condition the "
            "patient already has but the team may not know of. The test patients come from the same hospitals as the "
            "training ones."
        ),
    )

    # Dataset
    unique_name = "wids_diabetes_mellitus"
    year = "2021"
    domain = "medical & healthcare"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/widsdatathon2021"
    license = "Kaggle Competition Rules"
    download_description = """
        We download the data from Kaggle.

        kaggle competitions download -c widsdatathon2021 -f TrainingWiDS2021.csv && unzip TrainingWiDS2021.csv.zip &&  rm TrainingWiDS2021.csv.zip
        mkdir -p local-data-warehouse/wids_diabetes_mellitus && mv TrainingWiDS2021.csv local-data-warehouse/wids_diabetes_mellitus/
    """
    bibtex = r"""
        @misc{Matthys2021WiDSDatathon2021,
          author = {Karen Matthys and Meredith Lee and Neha Goel and Sharada Kalanidhi and Valerie and Vani M.},
          title  = {WiDS Datathon 2021},
          year   = {2021},
          howpublished = {\url{https://kaggle.com/competitions/widsdatathon2021}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the Kaggle dataset.

        - Data from the prior year's hackathon (2020) also used the very similar data but with older data and different splits. But it seems the feature engineering was transferable across years.
        - We drop encounter_id as it is an identifier with no temporal information, and from the competition there seems to be no temporal or index-based leakage.
        - We follow the top solutions and use normal random splits, instead of stratifying by hospital_id or ICU ID. Moreover, with the data for which we have labels, we have an even larger overlap for hospital_id and ICU ID even more than the train-test split on Kaggle. Lastly, we do not need to decode the hospital_ID based on the ICU ID.
        - A hospital can have multiple ICUs, so there is a strong co-correlation between hospital_id and ICU ID, but it is not identical.
        - We drop rows with age=0, as these seems to be 30 faulty entries (patients have a large height at age 0).
        - Kaggle experts found that several features were likely clipped to a min/max value based on investigating the histograms of the data. We noticed this too. Following the experts, we add a flag for these features indicating if the value was clipped or not.
        - Several Kaggle experts also re-computed the BMI. We also noticed that for 2770 rows, the BMI did not match the real BMI based on the weight and height. We drop all of these cases, as it is unclear to us what the cause of this error is. Given the small fraction, there is either a data entry error, or some values got corrected manually.
        - We found and dropped three duplicated columns that provided no new information.
        - We keep medical codes as string, as these could be more meaningfully decoded.
    """

    # Task
    target = "diabetes_mellitus"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="Area Under the ROC Curve (AUC)",
        reference="https://www.kaggle.com/competitions/widsdatathon2021/overview/evaluation",
        definition="AUC between the predicted probability of diabetes_mellitus and the observed label",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "TrainingWiDS2021.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(
            columns=[
                "Unnamed: 0",  # Saving artifact
                "encounter_id",  # Identifier, no temporal information
                "readmission_status",  # Constant
                # Duplicated columns (no new information)
                "paco2_for_ph_apache",
                "h1_inr_max",
                "h1_inr_min",
            ]
        )
        df = df[df["age"] != 0]  # Drop rows with age=0 (faulty entries)
        # Drop cases with faulty BMI calculations
        df["bmi_new"] = df["weight"] / ((df["height"] / 100) ** 2)
        bmi_wrong_mask = (df["bmi"].round(2) != df["bmi_new"].round(2)) & ~df["bmi"].isna()
        df = df[~bmi_wrong_mask]
        df = df.drop(columns=["bmi_new"])
        # add min/max flags for features that were clipped
        clipped_features = [
            "d1_sysbp_min",
            "d1_sysbp_max",
            "d1_heartrate_min",
            "d1_heartrate_max",
            "d1_diasbp_min",
            "d1_diasbp_max",
            "heart_rate_apache",
        ]
        for f in clipped_features:
            min_val = df[f].min()
            max_val = df[f].max()
            clip_f = f + "_clipped"
            df[clip_f] = (df[f] == min_val) | (df[f] == max_val)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "hospital_id",
                "icu_id",
                "elective_surgery",
                "ethnicity",
                "gender",
                "hospital_admit_source",
                "icu_admit_source",
                "icu_stay_type",
                "icu_type",
                "apache_post_operative",
                "arf_apache",
                "intubated_apache",
                "gcs_unable_apache",
                # We keep medical scales as int (as they are ordinal in nature)
                "ventilated_apache",
                "aids",
                "cirrhosis",
                "hepatic_failure",
                "immunosuppression",
                "leukemia",
                "lymphoma",
                "solid_tumor_with_metastasis",
                *[c for c in df.columns if c.endswith("_clipped")],
            ],
            string=[
                # Codes for medical terms
                "apache_2_diagnosis",
                "apache_3j_diagnosis",
            ],
        )
