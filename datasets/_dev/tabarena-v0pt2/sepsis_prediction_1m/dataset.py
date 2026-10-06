"""Curated dataset definition for `sepsis_prediction_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping


class SepsisPrediction1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "sepsis_prediction_1m"
    version_of = "sepsis_prediction"
    version_comment = """
        We sub-sample the frame to 1.5M rows by whole patients (stratified on the target) and use grouped 3-fold cross-validation, so every fold trains on about 1M and tests on about 500k rows (v2 split protocol).
    """
    year = "2019"
    domain = "medical & healthcare"
    source = "Other"
    source_url = "https://www.kaggle.com/datasets/salikhussaini49/prediction-of-sepsis"  # alt https://physionet.org/content/challenge-2019/1.0.0/
    license = "ODC Open Database License"  # CC BY-NC-SA 4.0 on Kaggle...
    data_tags = ("Non-IID", "Grouped")
    download_description = """
        We download the data from Kaggle as the link for the data from the original PhysioNet challenge seems to be down.

        kaggle datasets download -d salikhussaini49/prediction-of-sepsis && unzip prediction-of-sepsis.zip all_files && rm prediction-of-sepsis.zip
        mkdir -p local-data-warehouse/sepsis_prediction && mv all_files local-data-warehouse/sepsis_prediction/
    """
    bibtex = """
        @article{reyna2020early,
          title={Early prediction of sepsis from clinical data: the PhysioNet/Computing in Cardiology Challenge 2019},
          author={Reyna, Matthew A and Josef, Christopher S and Jeter, Russell and Shashikumar, Supreeth P and Westover, M Brandon and Nemati, Shamim and Clifford, Gari D and Sharma, Ashish},
          journal={Critical care medicine},
          volume={48},
          number={2},
          pages={210--217},
          year={2020},
          publisher={LWW}
        }
    """
    curation_comments = """
        We start with all files from Kaggle.

        The original data has one file per user that was already preprocessed to one .csv file by the competition creators. Here we start with the preprocessed single .csv file. The data is non-IID in nature based on the groups of patients from different hospitals. The data is grouped per patient ("Patient_ID"), and each patient's rows are the hours of one ICU stay. We simulate a snapshot early warning for patients not seen in training: at every hour, predict whether sepsis follows within the next 6 hours from that hour's measurements only. The model is trained once on the training patients and not refit with a new patient's data, and no prediction uses the patient's other hours. (The PhysioNet 2019 challenge also allowed the patient's earlier hours; causal history features built in `_clean` would be the upgrade to that setting.) One prediction per patient from the whole stay is not a valid alternative: all 2,932 septic records end at most 9 hours after their first positive hour, so the record length gives the outcome away.
        In the original competition, one had to predict for unseen patients from the existing hospitals and also for a new hidden hospital. In the public data, we only have two hospitals, (A) and (B). Given the limited data, we decide not to simulate a domain shift as we could not "train" for domain shift. Thus, we simulate only a normal grouped non-IID scenario. That is, we use all patients from both hospitals for training and testing, but ensure that the splits are grouped by patient ID. Thus, we simulate what would happen if someone trains a model on data from two hospitals and uses this to predict for other patients from these hospitals. This decision is also amplified by the large gap in performance for the unseen hospital in the competition (Report, Table 3), clearly pointing to a domain shift that is out-of-scope for this task. Note, we do not have temporal information of the order of patients, thus, we cannot simulate to only predict for patients "from the future". We believe this does not introduce any data leakage for this dataset.

        - Patients with an ID larger than 100_000 are from hospital (B), while patients with an ID smaller than 100_000 are from hospital (A). We add this indicator into our data and then reset the Patient_IDs to be continuous increasing integers.
        - The data consists of a lot of missing values due to missing measurements.
        - Note, hour is a reset time index per patient. ICULOS is similar, but with an offset. We keep both as this can show that we have truncated data for a patient.
        - We reverse the ordinal encoding of Gender.
        - We mark features as categorical where appropriate.
        - For each patient, we predict the sepsis status over time. So it is more or less a transformed survival task (also in the original challenge).
        - Prediction point and scoring: each row is one patient-hour with only that hour's measurements, and SepsisLabel is 1 from 6 hours before sepsis onset onward, so the task is "sepsis within the next 6 hours" at every hour. No row encodes the time left in the stay. The leak risk lies in the evaluation: the test set holds complete patient records, and septic records end shortly after onset, so a method that looks at a patient's later rows (record length, last Hour/ICULOS) learns the outcome. Each hour is predicted from its own row only: no feature may combine a patient's rows (record length, last Hour/ICULOS, aggregates over the stay). Scoring uses the PhysioNet 2019 utility per patient over its ordered hours, not independent rows. Patient_ID is group metadata, not a model feature.
    """

    # Task
    target = "SepsisLabel"
    problem_type = "binary_classification"
    metric = "PhysioNet2019UtilityFunction"  # https://github.com/physionetchallenges/evaluation-2019/blob/master/evaluate_sepsis_score.py
    grouping = Grouping(
        on="Patient_ID",
        labels="per_sample",
        time_on="Hour",
        prediction_unit="row",
        context="none",
        definition="""
            One group is an ICU stay; its rows are its hourly records. The PhysioNet/Computing in Cardiology Challenge 2019 predicts sepsis 6 hours ahead "at each hour of a patient's clinical record" for unseen patients and scores a utility per patient over its ordered hours. We use the snapshot form: each hour is one prediction, made from its own row only (no feature combines a patient's rows), and the challenge utility per patient is the score. The challenge also allowed the patient's earlier hours, a possible upgrade with causal history features.
        """,
    )

    # Splits
    subsample_to_budget = True
    accepted_check_warnings = {
        "splits_rows_never_tested": "The v2 protocol caps each test fold at 500k rows; the grouped folds of the 1.5M-row "
        "frame overshoot by whole groups, so 3,371 rows (0.2%) are trimmed from a test fold (2026-10-01).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "all_files" / "Dataset.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Add Hospital Indicator
        df["Hospital"] = "Hospital_A"
        df.loc[df["Patient_ID"] > 100_000, "Hospital"] = "Hospital_B"
        # Reset Patient IDs to be continuous (after remapping, IDs higher than 20k are from Hospital B)
        codes, _ = pd.factorize(df["Patient_ID"])
        df["Patient_ID"] = codes
        df["Gender"] = df["Gender"].replace({0: "Female", 1: "Male"})
        df = df.drop(columns=["Unnamed: 0"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Hospital",
                "Patient_ID",
                "Gender",
                "Unit1",
                "Unit2",
            ],
        )
