"""Curated dataset definition for `wids_diabetes_mellitus` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class WidsDiabetesMellitus(AbstractCuratedDataset):
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
        new_clipped_features = []
        for f in clipped_features:
            min_val = df[f].min()
            max_val = df[f].max()
            clip_f = f + "_clipped"
            new_clipped_features.append(clip_f)
            df[clip_f] = (df[f] == min_val) | (df[f] == max_val)
        as_cat_type = [
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
            "diabetes_mellitus",
        ] + new_clipped_features
        as_string_type = [
            # Codes for medical terms
            "apache_2_diagnosis",
            "apache_3j_diagnosis",
        ]
        for c in as_string_type:
            nan_mask = df[c].isna()
            df.loc[nan_mask, c] = np.nan
            df[c] = df[c].astype("string")
        df[as_cat_type] = df[as_cat_type].astype("category")
        return df
