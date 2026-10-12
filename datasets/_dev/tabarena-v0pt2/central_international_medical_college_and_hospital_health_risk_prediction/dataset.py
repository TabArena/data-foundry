"""Curated dataset definition for `central_international_medical_college_and_hospital_health_risk_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, drop_columns

RAW_FILE = "Health_Risk_Dataset.csv"
"""The only file of version 1 (the only version) of the Kaggle dataset."""

CONSCIOUSNESS = {"A": "Alert", "C": "Confusion", "V": "Verbal", "P": "Pain response", "U": "Unresponsive"}
"""The data card's words for the level-of-consciousness codes (NEWS2's ACVPU scale)."""

CLASSES = ["Normal", "Low", "Medium", "High"]
"""The four risk levels, from the lowest."""


def news2_points(raw: pd.DataFrame, *, scale2_points_on_air: bool) -> pd.DataFrame:
    """Points of each NEWS2 parameter (Royal College of Physicians 2017, Chart 1), for the decision evidence only.

    Args:
        raw: The raw frame, with its original column names and consciousness codes.
        scale2_points_on_air: Give the SpO2 scale-2 points for a saturation of 93% or more on air too. Chart 1 gives
            them only on oxygen ("≥93 on air" scores 0).
    """
    rr = raw["Respiratory_Rate"]
    spo2 = raw["Oxygen_Saturation"]
    sbp = raw["Systolic_BP"]
    pulse = raw["Heart_Rate"]
    temp = raw["Temperature"]
    on_oxygen = raw["On_Oxygen"].eq(1).to_numpy()
    scale1 = np.select([spo2 <= 91, spo2 <= 93, spo2 <= 95], [3, 2, 1], 0)
    scale2_low = np.select([spo2 <= 83, spo2 <= 85, spo2 <= 87], [3, 2, 1], 0)
    scale2_high = np.select([spo2 <= 92, spo2 <= 94, spo2 <= 96], [0, 1, 2], 3)
    if not scale2_points_on_air:
        scale2_high = np.where(on_oxygen, scale2_high, 0)
    scale2 = np.where(spo2 <= 87, scale2_low, scale2_high)
    return pd.DataFrame(
        {
            "respiration": np.select([rr <= 8, rr <= 11, rr <= 20, rr <= 24], [3, 1, 0, 2], 3),
            "spo2": np.where(raw["O2_Scale"].eq(2).to_numpy(), scale2, scale1),
            "air_or_oxygen": np.where(on_oxygen, 2, 0),
            "systolic_bp": np.select([sbp <= 90, sbp <= 100, sbp <= 110, sbp <= 219], [3, 2, 1, 0], 3),
            "pulse": np.select([pulse <= 40, pulse <= 50, pulse <= 90, pulse <= 110, pulse <= 130], [3, 1, 0, 1, 2], 3),
            "consciousness": np.where(raw["Consciousness"].eq("A").to_numpy(), 0, 3),
            "temperature": np.select([temp <= 35.0, temp <= 36.0, temp <= 38.0, temp <= 39.0], [3, 1, 0, 1], 2),
        },
        index=raw.index,
    )


def news2_band(points: pd.DataFrame) -> pd.Series:
    """The NEWS2 response band (RCP 2017, Chart 4) in the label's words.

    Total 0 is Normal, 1-4 Low, a score of 3 in a single parameter or a total of 5-6 Medium, 7 or more High.
    """
    total = points.sum(axis=1)
    red = points.drop(columns="air_or_oxygen").eq(3).any(axis=1)
    band = np.select([total >= 7, total >= 5, red, total >= 1], ["High", "Medium", "Medium", "Low"], "Normal")
    return pd.Series(band, index=points.index)


class CentralInternationalMedicalCollegeAndHospitalHealthRiskPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "central_international_medical_college_and_hospital_health_risk_prediction"
    year = "2025"
    domain = "medical & healthcare"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/ludocielbeckett/health-risk-prediction-anonymized-real-data"
    license = "Apache 2.0"
    download_description = """
        We download version 1 (the only version, 2025-08-24) of the Kaggle dataset; its zip holds one file.
        Health_Risk_Dataset.csv: sha256 def34f7c98d3c580be348052856ef494b8ffb690684af3fc5546eb94edee0cec

        mkdir -p local-data-warehouse/central_international_medical_college_and_hospital_health_risk_prediction
        cd local-data-warehouse/central_international_medical_college_and_hospital_health_risk_prediction
        kaggle datasets download ludocielbeckett/health-risk-prediction-anonymized-real-data/1
        unzip health-risk-prediction-anonymized-real-data.zip && rm health-risk-prediction-anonymized-real-data.zip
    """
    bibtex = r"""
        @misc{alam2025healthrisk,
          author = {Alam, Rakibul},
          title = {Health Risk Prediction (Anonymized Real Data)},
          year = {2025},
          howpublished = {\url{https://www.kaggle.com/datasets/ludocielbeckett/health-risk-prediction-anonymized-real-data}},
          note = {Kaggle dataset; the uploader names Central International Medical College and Hospital, Dhaka, as the source}
        }
    """
    curation_comments = """
        We start with Health_Risk_Dataset.csv (1,000 rows), the only file of the Kaggle dataset "Health Risk Prediction (Anonymized Real Data)" (Rakibul Alam, 2025). The uploader says it holds patients of the ICU and the medical ward of Central International Medical College and Hospital, Dhaka; the data card says nothing about how the risk levels were assigned.

        - Prediction point: a bedside observation round in the ICU or a medical ward. A nurse has just measured the seven NEWS2 parameters, and the model assigns the patient's risk level from them; all eight features are those measurements.
        - Anomaly: the target is the NEWS2 band of the features (Royal College of Physicians 2017, NEWS2 Charts 1, 2 and 4). Risk_Level equals the band in 1,000 of 1,000 rows when the scale-2 points for an SpO2 of 93% or more are given on air too, and in 987 rows with Chart 1's "on oxygen" condition (first decision). The label is a lookup of the features, not an outcome, so models only have to learn the score's thresholds. Whether the dataset stays (criterion 4C, Trivial) is the curator's call.
        - Anomaly: the vital signs look drawn per class. Patient_ID numbers the rows in blocks of the label (second decision), and within a class the vitals behave like independent draws, while across the classes they move together (third decision). The values also lack the terminal-digit preference of charted observations. This points to generated data (criterion 4B) but is circumstantial; the label rule is the decisive finding.
        - Dropped Patient_ID: one identifier per row, numbered in blocks of the label, so it would give the label away.
        - Consciousness gets the data card's words for its codes (Alert, Confusion, Verbal, Pain response, Unresponsive) as a category. O2_Scale (1 or 2, the SpO2 scale in use) and On_Oxygen (0 on air, 1 on supplemental oxygen) stay numeric.
        - IID split: each row is a different patient, and the file holds no time, ward or visit information.
        - The task probes flag `solved` (macro ROC AUC 0.996-0.997). It is a lookup, not a leak: the NEWS2 band is right on every row, and the source has no earlier stage to fall back to, as all eight features are measured together. The generated-data probe's `rule_leaves` flag follows from the same threshold rule.
        - No duplicate rows and no missing values.
    """

    # Task
    target = "Risk_Level"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # one id per row, numbered in blocks of the label: it would give the label away
        df = drop_columns(df, ["Patient_ID"])
        df["Consciousness"] = df["Consciousness"].map(CONSCIOUSNESS)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["Consciousness"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        label = raw["Risk_Level"]
        on_air_too = news2_band(news2_points(raw, scale2_points_on_air=True))
        chart = news2_band(news2_points(raw, scale2_points_on_air=False))
        rule = pd.DataFrame(
            {
                "rows": label.value_counts(),
                "NEWS2 band equal, scale-2 points also on air": label[on_air_too.eq(label)].value_counts(),
                "NEWS2 band equal, scale-2 points only on oxygen (Chart 1)": label[chart.eq(label)].value_counts(),
            }
        ).reindex(CLASSES)
        rule.loc["all"] = rule.sum()

        number = raw["Patient_ID"].str[1:].astype("int64")
        blocks = number.groupby(label).agg(["min", "max", "count"]).reindex(CLASSES)
        blocks.columns = ["first Patient_ID number", "last Patient_ID number", "rows"]

        dependence = {}
        for level in CLASSES:
            part = raw[label.eq(level)]
            spo2 = part["Oxygen_Saturation"]
            alert = part["Consciousness"].eq("A")
            dependence[level] = {
                "rows": len(part),
                "Spearman pulse vs temperature": part["Heart_Rate"].rank().corr(part["Temperature"].rank()),
                "SpO2 on air": spo2[part["On_Oxygen"].eq(0)].mean(),
                "SpO2 on oxygen": spo2[part["On_Oxygen"].eq(1)].mean(),
                "SpO2 on scale 1": spo2[part["O2_Scale"].eq(1)].mean(),
                "SpO2 on scale 2": spo2[part["O2_Scale"].eq(2)].mean(),
                "pulse, alert": part.loc[alert, "Heart_Rate"].mean(),
                "pulse, not alert": part.loc[~alert, "Heart_Rate"].mean(),
            }
        dependence = pd.DataFrame.from_dict(dependence, orient="index").round(2)
        dependence.index.name = "Risk_Level"
        del df
        return [
            Decision(
                "The label is the NEWS2 band of the features",
                "NEWS2 (Royal College of Physicians 2017) scores each of seven parameters 0-3 (Chart 1) and sets the "
                "response by the total and by a score of 3 in a single parameter (Charts 2 and 4). Computed from the "
                "features, that band equals Risk_Level in every row when the SpO2 scale-2 points are given on air too, "
                "and in 987 rows with the chart's on-oxygen condition: the label is a lookup, not an outcome.",
                rule,
            ),
            Decision(
                "Patient_ID dropped: numbered in blocks of the label",
                "Each class holds one consecutive range of ids, so the id alone gives the label. Its order within a "
                "class is unrelated to the NEWS2 total (Spearman 0.00-0.03).",
                blocks,
            ),
            Decision(
                "The vital signs do not depend on each other within a class",
                "Within each class the vitals behave like independent draws: pulse is unrelated to temperature, SpO2 "
                "is the same on air and on oxygen and on both SpO2 scales, and the patients who are not alert have "
                "the pulse of the alert ones, while across classes every vital moves with the label (pairwise "
                "Spearman |r| 0.59-0.68). With the id blocks this points to values drawn per class. It is "
                "circumstantial; the label rule is the decisive finding.",
                dependence,
            ),
        ]
