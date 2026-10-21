"""Curated dataset definition for `heart_disease` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, SplitPlan, TaskSummary

COLUMNS = [
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
# The hospitals of Detrano et al. (1989), in the order of the test folds. Switzerland is left out (curation notes).
HOSPITALS = {
    "Cleveland": "processed.cleveland.data",
    "Hungary": "processed.hungarian.data",
    "VA Long Beach": "processed.va.data",
}


class HeartDisease(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will the angiogram of a patient at a new hospital show a narrowed coronary artery?",
        use_case=(
            "A cardiologist estimates a chest-pain patient's chance of coronary artery disease from the history and "
            "noninvasive tests with a model built at other hospitals, to decide whether the patient needs angiography, "
            "as Detrano et al. (1989) applied their Cleveland model in Budapest, Long Beach and Switzerland."
        ),
        row=(
            "One of 797 patients examined by angiography at one of three hospitals: Cleveland Clinic (303), the "
            "Hungarian Institute of Cardiology in Budapest (294) and the VA Medical Center in Long Beach (200); "
            "exams of the 1980s, donated in 1988."
        ),
        predicted=(
            "Whether the angiogram shows more than 50% narrowing in any major coronary artery (49% do; 36% to 75% by "
            "hospital)."
        ),
        known=(
            "Age, sex, chest-pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, an "
            "exercise test (peak heart rate, chest pain on exercise, the ECG's ST depression and its slope) and, "
            "mostly in Cleveland, calcium seen on fluoroscopy and a thallium scan. Not the hospital."
        ),
        split=(
            "Whole hospitals are held out: each split trains on two hospitals and tests on the third, so the test "
            "data stands for the patients of a hospital the model has never seen."
        ),
        changes=(
            "We merge three hospitals' files into one table and split by hospital, leave out the Swiss file (its "
            "release dropped most patients without disease), and merge the four grades of disease into one class."
        ),
        fit="approximate",
        fit_reason=(
            "The features come from tests done before the angiogram that sets the label, and a held-out hospital "
            "is a new one with its own disease rate and test habits. But every patient had already been sent to "
            "angiography, so the data shows referred patients, not those a referral is decided for."
        ),
    )

    # Dataset
    unique_name = "heart_disease"
    year = "1988"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C52P4X"
    license = "CC BY 4.0"
    download_description = """
        Get the UCI data (the processed files of the three hospitals).

        mkdir -p local-data-warehouse/heart_disease && cd local-data-warehouse/heart_disease && wget https://archive.ics.uci.edu/static/public/45/heart+disease.zip && unzip heart+disease.zip processed.cleveland.data processed.hungarian.data processed.va.data && rm heart+disease.zip
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
        We start with the processed files of three hospitals from UCI's Heart Disease collection, the 14 attributes used in the study.

        - Prediction point: before the angiogram, with the history, the resting tests and the exercise test at hand. `ca` (major arteries with calcium seen on cardiac fluoroscopy, 0-3) and `thal` (exercise thallium scan) are noninvasive tests done before the angiogram (Detrano et al. 1986, PMID 3698241 and 3706156), so neither is read from it.
        - One study, three tasks merged: the files share the protocol, attributes and label, and a model trained on two hospitals ranks the third's patients nearly as well as one trained there (TabPFN 3.5 ROC AUC 0.888 on Cleveland, 0.906 on Hungary, 0.739 on Long Beach; trained in-site 0.913, 0.914, 0.708). We concatenate the files and keep the hospital as the group column.
        - Split by hospital, as in the source: Detrano et al. (1989) derived their model on the Cleveland patients and "applied [it] to" the other hospitals' patients (abstract). A hospital that uses a model built elsewhere brings its own disease rate (36% in Budapest, 46% in Cleveland, 75% in Long Beach, as in the paper) and its own test habits (`ca` and `thal` recorded almost only in Cleveland, no exercise test for 53 Long Beach patients). Held out whole, a hospital is scored on its own patients only. A random split would mix the hospitals in every test fold, and 68% of its positive-negative pairs would compare patients of two hospitals, a comparison no clinician makes. The model is not given the hospital: a new one is unknown.
        - Note: the task probes flag `unstable` (the standard error of the best model family's mean skill is 0.094 over the 3 splits). The signal is there at every held-out hospital: the linear model beats the class shares on 3 of 3 (mean ROC AUC 0.838). The spread is between hospitals, Long Beach being the hardest (TabPFN 3.5: 0.888 Cleveland, 0.906 Hungary, 0.739 Long Beach). Kept, as `consumer_complaints_1m` and `apistox` were with 3 and 4 windows.
        - Switzerland left out: its UCI file keeps 123 of the paper's 143 patients and only 8 of its 23 without disease (94% diseased against the paper's 84%), so its disease rate is the release's, not the hospital's, and as a held-out hospital it would be scored on 8 patients without disease.
        - Missing values: "?" becomes NaN. Cholesterol 0 (49 Long Beach rows) and resting blood pressure 0 (1 row) are impossible and become NaN. Other missing values stay: whether a test was done is known before the angiogram. In Hungary `slope` is missing exactly when there is no ST depression.
        - Target: `num` (0 = no narrowing over 50%, 1-4 = disease grades; the Hungarian file holds only 0/1) becomes the binary `heart_disease_diagnosis`, as in the study.
        - Codes are kept as in UCI: `sex` 1 = male; `cp` 1 typical angina, 2 atypical angina, 3 non-anginal pain, 4 asymptomatic; `fbs` 1 = fasting blood sugar over 120 mg/dl; `restecg` 0 normal, 1 ST-T wave abnormality, 2 left ventricular hypertrophy; `exang` 1 = angina on exercise; `oldpeak` ST depression on exercise relative to rest; `slope` of the peak-exercise ST segment, 1 up, 2 flat, 3 down; `thal` 3 normal, 6 fixed defect, 7 reversible defect.
        - Anomaly: the Hungarian file keeps 294 of the paper's 425 patients (36% diseased against 38%), selection not stated. 6 Long Beach angiograms are dated 7 to 15 days (one 369 days) before the exercise test in the raw file; kept. One Long Beach `oldpeak` is negative.
        - Duplicates: two rows repeat another row of the same hospital (one Hungarian, one Long Beach); with 13 coarse attributes these are plausible patients, kept.
    """

    # Task
    target = "heart_disease_diagnosis"
    problem_type = "binary_classification"
    grouping = Grouping(
        on="hospital",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a hospital: Cleveland Clinic, the Hungarian Institute of Cardiology (Budapest) or the VA Medical Center (Long Beach). The source's question is whether a probability model carries over to other hospitals: "This model, derived from the clinical and noninvasive test results of 303 patients undergoing angiography at the Cleveland Clinic in Cleveland, Ohio, was applied to a group of 425 patients undergoing angiography at the Hungarian Institute of Cardiology in Budapest, Hungary (disease prevalence 38%); 200 patients undergoing angiography at the Veterans Administration Medical Center in Long Beach, California (disease prevalence 75%)" (Detrano et al. 1989, abstract). So whole hospitals are held out and the model is not told the hospital. Each row is one patient and one prediction.
        """,
    )
    splits_comment = """
        Leave one hospital out: three splits, each training on two hospitals and testing on the third (Cleveland, Hungary, then Long Beach), one repeat, since repeating a split of three groups into three folds gives the same splits. This follows the source, which built its model at one hospital and tested it at the others; with three hospitals the scores are three numbers and differ by hospital (Long Beach is the hardest).
    """
    accepted_check_warnings = {
        "task_group_count_low": "Three hospitals by design: the source built its model at one hospital and applied it "
        "at the others. The fourth hospital (Switzerland) is left out because its published file kept only 8 of its 23 "
        "patients without disease.",
        "splits_dimensions_off_protocol": "Leave one hospital out gives exactly three splits. More repeats would split "
        "the same three hospitals the same way, so they would add copies, not information.",
        "groups_test_groups_few": "Testing on one unseen hospital at a time is the task. Each fold still scores 200 to "
        "303 patients one by one (smallest class: 51). The signal carries over to unseen hospitals: the linear model "
        "beats the class shares on all three (task probes), and logistic regression reaches ROC AUC 0.868 on held-out "
        "hospitals (group probes, 2026-10-21). Most of the variation between folds comes from Long Beach, the hardest "
        "hospital.",
        "groups_largest_share_high": "Cleveland is a real hospital, one of three, not a catch-all value. When it is the "
        "test hospital, the model trains on the other two (494 patients), where two of Cleveland's tests were almost "
        "never recorded.",
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {h: pd.read_csv(raw_dir / f, header=None, names=COLUMNS) for h, f in HOSPITALS.items()}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # One table, with the hospital each file comes from
        df = pd.concat([d.assign(hospital=h) for h, d in raw.items()], ignore_index=True)
        # Proxy missing values: "?" and the impossible zeros of cholesterol and resting blood pressure
        df = df.replace("?", np.nan)
        numeric = [c for c in COLUMNS if c != "num"]
        df[numeric] = df[numeric].astype(float)
        df[["chol", "trestbps"]] = df[["chol", "trestbps"]].replace(0, np.nan)
        # Make target: presence (grades 1-4) against absence (0) of disease
        df["heart_disease_diagnosis"] = (df["num"].astype(int) > 0).astype(int)
        return df.drop(columns=["num"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["hospital", "sex", "cp", "fbs", "restecg", "exang", "slope", "thal"])

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # Leave one hospital out, one repeat: fold i tests on the i-th hospital and trains on the other two
        hospital = df["hospital"].astype(str).to_numpy()
        splits = {
            0: {
                i: (np.flatnonzero(hospital != h).tolist(), np.flatnonzero(hospital == h).tolist())
                for i, h in enumerate(HOSPITALS)
            }
        }
        return SplitPlan(splits=splits)

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        by = df.groupby("hospital", observed=True).agg(
            patients=(self.target, "size"),
            disease_pct=(self.target, lambda s: (s.astype(int) == 1).mean() * 100),
            ca_missing_pct=("ca", lambda s: s.isna().mean() * 100),
            thal_missing_pct=("thal", lambda s: s.isna().mean() * 100),
            slope_missing_pct=("slope", lambda s: s.isna().mean() * 100),
            chol_missing_pct=("chol", lambda s: s.isna().mean() * 100),
            exercise_test_missing_pct=("oldpeak", lambda s: s.isna().mean() * 100),
        )
        return [
            Decision(
                title="Split by hospital: train on two, test on the third",
                why=(
                    "The source built its model at one hospital and applied it at the others (Detrano et al. 1989), "
                    "and the hospitals differ in disease rate and in which tests they recorded, as a new hospital "
                    "would. Trained on two hospitals, TabPFN 3.5 reaches ROC AUC 0.888 on Cleveland, 0.906 on "
                    "Hungary and 0.739 on Long Beach (LR 0.879, 0.903, 0.693), and its mean predicted probability is "
                    "off where the disease rate differs (46% against 36% in Hungary, 62% against 75% in Long Beach), "
                    "the source's own finding."
                ),
                evidence=by.round(0),
            )
        ]
