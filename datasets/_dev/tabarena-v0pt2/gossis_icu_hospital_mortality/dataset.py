"""Curated dataset definition for `gossis_icu_hospital_mortality` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    TaskSummary,
    decode,
    drop_columns,
)

# The ordinal scales, lowest level first, from the source's codebook (as in wids_diabetes_mellitus, the same GOSSIS
# columns).
ORDINAL_LEVELS = {
    "gcs_eyes_apache": ["none", "to pain", "to speech", "spontaneous"],
    "gcs_motor_apache": ["none", "extension", "abnormal flexion", "withdrawal", "localises pain", "obeys commands"],
    "gcs_verbal_apache": ["none", "incomprehensible sounds", "inappropriate words", "confused", "oriented"],
}

# The codebook's words for the Glasgow Coma Scale codes (CLEAN-12).
CODE_LABELS = {
    "gcs_eyes_apache": {"1": "none", "2": "to pain", "3": "to speech", "4": "spontaneous"},
    "gcs_motor_apache": {
        "1": "none",
        "2": "extension",
        "3": "abnormal flexion",
        "4": "withdrawal",
        "5": "localises pain",
        "6": "obeys commands",
    },
    "gcs_verbal_apache": {
        "1": "none",
        "2": "incomprehensible sounds",
        "3": "inappropriate words",
        "4": "confused",
        "5": "oriented",
    },
}


class GossisIcuHospitalMortality(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a patient admitted to intensive care die before leaving the hospital?",
        use_case=(
            "At the end of the first day in the ICU, a severity score estimates each patient's risk of dying in "
            "hospital, as APACHE does, for risk adjustment and for comparing ICUs and hospitals (WiDS Datathon 2020, "
            "MIT's GOSSIS initiative)."
        ),
        row=(
            "One ICU stay at one of 147 US hospitals in MIT's GOSSIS data (91,713 stays with a label; one year, not "
            "dated)."
        ),
        predicted="Whether the patient died during this hospital stay; 8.6% did.",
        known=(
            "Age, sex, ethnicity, height, weight and BMI, how and why the patient was admitted, the days in hospital "
            "before the ICU, chronic conditions, the vital signs and lab values of the first hour and day, and the "
            "worst first-day values of the APACHE score."
        ),
        split="Whole hospitals are held out, so the test data stands for hospitals the score has not seen.",
        changes=(
            "APACHE IVa's two death probabilities are dropped (another model's prediction of the target), as are "
            "the identifiers and the ICU id."
        ),
        fit="direct",
        fit_reason=(
            "Every feature is recorded in the first 24 hours of the stay and the label comes at discharge, which is "
            "the set-up of APACHE and GOSSIS; the source's own test hospitals were mostly not in its training data."
        ),
    )

    # Dataset
    unique_name = "gossis_icu_hospital_mortality"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/widsdatathon2020",
            # Kaggle states the data terms only on the rules tab, behind the competition's acceptance; the copy on PhysioNet
            # (https://physionet.org/content/widsdatathon2020/1.0.0/) is credentialed, under the PhysioNet Restricted Health
            # Data License 1.5.0 (the Review, issue on the licence).
            license="Kaggle Competition Rules",
            year="2020",
            bibtex=r"""
                @misc{Lee2020WiDSDatathon2020,
                  author = {Meredith Lee and Jesse Raffa and Marzyeh Ghassemi and Tom Pollard and Sharada Kalanidhi and Omar Badawi and Karen Matthys and Leo Anthony Celi},
                  title  = {{WiDS} (Women in Data Science) Datathon 2020: {ICU} Mortality Prediction (version 1.0.0)},
                  year   = {2020},
                  publisher = {PhysioNet},
                  doi    = {10.13026/vc0e-th79},
                  howpublished = {\url{https://www.kaggle.com/competitions/widsdatathon2020}},
                  note   = {Kaggle competition}
                }
            """,
        ),
    )
    data_tags = ("ForcedGroupedFromTemporal",)
    download_description = """
        We download the data from Kaggle (the competition's rules must be accepted first). The same files are on
        PhysioNet (credentialed access, https://doi.org/10.13026/vc0e-th79).

        kaggle competitions download -c widsdatathon2020 && unzip widsdatathon2020.zip && rm widsdatathon2020.zip
        mkdir -p local-data-warehouse/gossis_icu_hospital_mortality && mv training_v2.csv "WiDS Datathon 2020 Dictionary.csv" local-data-warehouse/gossis_icu_hospital_mortality/
    """
    curation_comments = """
        We start with training_v2.csv of the WiDS Datathon 2020 on Kaggle (91,713 labelled ICU stays); unlabeled.csv
        has no labels and stays out.

        - Prediction point: the end of the first 24 hours in the ICU; every feature is a first-hour or first-day value,
          an admission fact or a chronic condition, and the label is death before hospital discharge.
        - Built in place of wids_diabetes_mellitus (2026-11-11, the curator's mark on its issue 1, c): the same GOSSIS
          cohort, with a target nobody knows at 24 hours. 130,127 of WiDS 2021's 130,157 rows are rows of the WiDS 2020
          files, 90,998 of them in this labelled file.
        - APACHE IVa's `apache_4a_hospital_death_prob` and `apache_4a_icu_death_prob` are dropped (CLEAN-6): another
          model's prediction of the target (in-hospital death) and of a narrower one (ICU death), computed from the
          same first-day values; kept, the task would be to recalibrate APACHE. They are not fit on this table, so no
          leak in the sense of LEAK-27, and they stay the reference: ROC AUC 0.863 on the 81,395 rows where they are
          computed (-1 in 2,371 rows, missing in 7,947).
        - Dropped identifiers: `encounter_id` and `patient_id` (one per row: no patient repeats), `icu_id` (nested in
          the hospital: each ICU belongs to one hospital, so under the hospital split every test value is unseen).
          `hospital_id` is the group column, never a feature.
        - `readmission_status` is constant (0 in every row, although 560 stays have the stay type `readmit`) and
          dropped; `icu_stay_type` stays.
        - Three exact copies are dropped: `paco2_for_ph_apache` (= `paco2_apache`), `h1_inr_max` and `h1_inr_min`
          (= the day-one INR), as in wids_diabetes_mellitus.
        - Clipped values ship as published: GOSSIS clipped many columns at fixed bounds (BMI at 14.84 and 67.81, weight
          at 38.6 and 186 kg, height at 137.2 and 195.59 cm, 420 to 460 rows at each; age is top-coded at 89). The 1,756
          rows whose BMI differs from weight over height squared by more than 0.01 all have BMI, weight or height at a
          bound, so the BMI is not impossible and is not set missing (unlike wids_diabetes_mellitus): those rows die at
          12.9% against 8.6%, and missing values would mark them (kept on Andrej's mark, 2026-11-11). No age 0 occurs
          here.
        - Time basis: ForcedGroupedFromTemporal: ICU stays of one year (eICU, 2014-2015), released without a date or an
          order (no signal in the file order, encounter_id or patient_id); the split holds out hospitals, and a later
          period of stays, which a dated release would allow, is not tested.
        - Anomaly: `pre_icu_los_days` is negative in 778 rows (median -0.30 days, 647 above -1 day): a registration lag
          in eICU (hospital admission recorded after the ICU admission); kept, as missing values would mark the same
          rows (2026-11-11, Andrej).
        - Anomaly: `apache_2_bodysystem` holds "Undefined diagnoses" (3,768 rows) and "Undefined Diagnoses" (346); kept
          apart, since they map to different APACHE III body systems (the first to Cardiovascular, 2,948, and
          Musculoskeletal/Skin, 820; the second only to Musculoskeletal/Skin).
        - Glasgow Coma Scale codes carry the codebook's words, as ordered categories (`CODE_LABELS`, `ORDINAL_LEVELS`;
          CLEAN-12, CLEAN-14); the diagnosis codes `apache_2_diagnosis` and `apache_3j_diagnosis` are codes, kept as
          strings.
        - The target (CLEAN-25): `hospital_death` ships as words, "Yes" (died, the event, sorting second) and "No".
        - Repeat patients: `patient_id` is one per row (91,713 ids, the same range as `encounter_id`), so repeat
          patients cannot be found; eICU holds about 1.4 stays per patient. The hospital split keeps a patient's stays
          at one hospital in one fold; only stays admitted from another hospital (2.6%) could cross. No two rows share
          hospital, age, sex, ethnicity, height, weight and three first-day vitals.
        - Hospital fingerprint: the features name the hospital for 82.8% of the stays of the 20 largest hospitals (the
          split auditor's check), yet `hospital_id` as a feature adds nothing (ROC AUC 0.902 with it, 0.903 without,
          random splits) and the grouped split scores 0.901 against 0.903 random: case mix, not the site, carries
          the outcome.
    """

    # Task
    target = "hospital_death"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="Area Under the Receiver Operating Characteristic Curve",
        reference="https://www.kaggle.com/competitions/widsdatathon2020/overview/evaluation",
        definition="AUC between the predicted probability of hospital_death and the observed label",
    )
    grouping = Grouping(
        on="hospital_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a hospital (147 US hospitals, 2 to 4,333 stays each). A severity score is used to compare and adjust for risk across hospitals, including ones its developers never saw, and the WiDS 2020 organisers held out hospitals: 57 of the 66 hospitals of their test file are not in the training file. Each stay is one prediction, made from that stay's first day alone.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "training_v2.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = drop_columns(
            raw,
            [
                "encounter_id",  # identifier, one per row
                "patient_id",  # identifier, one per row
                "icu_id",  # nested in hospital_id: unseen in every test fold
                "readmission_status",  # constant
                "apache_4a_hospital_death_prob",  # APACHE IVa's prediction of the target (CLEAN-6)
                "apache_4a_icu_death_prob",  # APACHE IVa's prediction of ICU death (CLEAN-6)
                # exact copies of another column
                "paco2_for_ph_apache",
                "h1_inr_max",
                "h1_inr_min",
            ],
        )
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "hospital_id",
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
                "ventilated_apache",
                "aids",
                "cirrhosis",
                "diabetes_mellitus",
                "hepatic_failure",
                "immunosuppression",
                "leukemia",
                "lymphoma",
                "solid_tumor_with_metastasis",
                "apache_3j_bodysystem",
                "apache_2_bodysystem",
            ],
            string=[
                # codes for admission diagnoses
                "apache_2_diagnosis",
                "apache_3j_diagnosis",
            ],
        )
