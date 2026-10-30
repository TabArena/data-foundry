"""Curated dataset definition for `heart_disease` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, SplitPlan, TaskSummary

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
# The UCI codes (heart-disease.names) and their labels; `fbs` and `exang` stay 0/1 flags
LABELS = {
    "sex": {1.0: "male", 0.0: "female"},
    "cp": {1.0: "typical angina", 2.0: "atypical angina", 3.0: "non-anginal pain", 4.0: "asymptomatic"},
    "restecg": {0.0: "normal", 1.0: "ST-T wave abnormality", 2.0: "left ventricular hypertrophy"},
    "slope": {1.0: "upsloping", 2.0: "flat", 3.0: "downsloping"},
    "thal": {3.0: "normal", 6.0: "fixed defect", 7.0: "reversible defect"},
}


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "slope": ["upsloping", "flat", "downsloping"],
}


class HeartDisease(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will the angiogram of a patient at a new hospital show a narrowed coronary artery?",
        use_case=(
            "For a chest-pain patient referred for angiography, a cardiologist estimates from the history and the "
            "noninvasive tests done before it whether the angiogram will show narrowing, with a model built at other "
            "hospitals, to decide whether the angiogram is needed. Detrano et al. (1989) built their model in "
            "Cleveland and applied it at other hospitals, to spare patients an unnecessary angiogram (p. 309)."
        ),
        row=(
            "One of 796 patients examined by angiography at one of three hospitals: Cleveland Clinic (303), the "
            "Hungarian Institute of Cardiology in Budapest (294) and the VA Medical Center in Long Beach (199); "
            "exams of 1981 to 1987, donated in 1988."
        ),
        predicted=(
            "Whether the angiogram shows more than 50% narrowing in any major coronary artery (49% do; 36% to 74% by "
            "hospital)."
        ),
        known=(
            "Age, sex, chest-pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, an "
            "exercise test (peak heart rate, chest pain on exercise, the ECG's ST depression and its slope) and, "
            "mostly in Cleveland, calcium seen on fluoroscopy and a thallium scan. Not the hospital, though which "
            "tests were recorded tells the hospitals apart."
        ),
        split=(
            "Whole hospitals are held out: each split trains on two hospitals and tests on the third, so the test "
            "data stands for the patients of a hospital the model has never seen."
        ),
        changes=(
            "We merge three hospitals' files into one table and split by hospital, leave out the Swiss file (its "
            "release dropped most patients without disease), drop one Long Beach patient entered twice, and merge the "
            "four grades of disease into one class."
        ),
        fit="approximate",
        fit_reason=(
            "Every patient had been referred for angiography, as at this check, and the features come from tests done "
            "before the angiogram (30 exercise tests dated after it, likely date errors, are kept). But Cleveland ran "
            "three tests on every patient by study protocol, and two are no longer used: CT has replaced the "
            "thallium-201 scan and calcium seen on fluoroscopy."
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
        We start with the processed files of three hospitals from UCI's Heart Disease collection, the 13 variables of the Detrano et al. (1989) model and its label (p. 305; pages of Am J Cardiol 64:304-310). UCI's raw 76-attribute files hold the same 294 Hungarian, 200 Long Beach and 123 Swiss patients, so the patients the release dropped are not public.

        - Prediction point: after the referral for angiography, before the angiogram, with the history, the resting tests and the exercise test at hand. `ca` (major arteries with calcium seen on cardiac fluoroscopy, 0-3) and `thal` (exercise thallium scan) are noninvasive tests done before the angiogram (Detrano et al. 1986, PMID 3698241 and 3706156; in Cleveland by research protocol, read after the angiogram and without knowledge of its result, p. 305), so neither is read from it. In 30 patients the raw files date the angiogram before the exercise test (Cleveland 11, by 7 to 449 days; Hungary 13, by 1 to 367 days; Long Beach 6, by 7 to 15 days and one by 369), and one Long Beach angiogram is dated 1901; the codebook doubts this date field ("cmo: month of cardiac cath (sp?) (perhaps 'call')"), and the paper has every test within 6 weeks before the angiogram (p. 306). Kept: 15 of the 30 are diseased, and blanking their exercise tests leaves the linear model's ROC AUC at 0.836.
        - One study, three tasks merged: the files share the attributes, their coding and the label (though `ca` and `thal` were recorded almost only in Cleveland), and a model trained on the other two hospitals ranks a hospital's patients nearly as well as one trained there (logistic regression ROC AUC 0.880 on Cleveland, 0.898 on Hungary, 0.732 on Long Beach; trained in-site 0.905, 0.905, 0.663; TabPFN 3.5 gave 0.888, 0.906, 0.739 against 0.913, 0.914, 0.708 in the first run, not reproduced since). We concatenate the files and keep the hospital as the group column.
        - Split by hospital, the source's design generalised: Detrano et al. built their model on the Cleveland patients and "applied [it] to" the patients of the other hospitals (abstract, p. 305); here every hospital is tested once. A hospital brings its own disease rate (46% in Cleveland, 36% in Budapest, 74% in Long Beach; the paper's Table I gives 46%, 38% and 74%) and its own test habits (`ca` and `thal` recorded almost only in Cleveland, no exercise test for 53 Long Beach patients). Held out whole, a hospital is scored on its own patients only: a random split would compare patients of two hospitals in 68% of its positive-negative pairs, and the hospital's disease rate alone would reach a pooled ROC AUC of 0.65. The model is not given the hospital, but the features tell the hospitals apart (91% accuracy, 85% from which tests are missing); reweighting the training hospitals to one disease rate changes the mean ROC AUC by 0.003 or less.
        - Note: three hospitals give three splits, the case in which `covertype` (three areas) went back to a random split. Here the transfer to a new hospital is the source's design, no class drops out (51 or more patients of each class in every test fold), and resampling the patients of each held-out hospital separates 7 of 15 pairs of model families, against 4 to 5 for a random 10 x 3 split. `sepsis_prediction_1m` kept its hospitals as a feature because its use case is the known hospitals.
        - Note: the task probes flag `unstable` (standard error of the best family's mean skill 0.105 over the 3 splits). The linear model beats the class shares at every held-out hospital (ROC AUC 0.880, 0.898, 0.732); the spread is Long Beach, the hardest hospital under every split, in-site too. Kept as one atypical group, as `musk` and `pancreatic_cancer_mouse_detection` were; re-check with tuned results after the build.
        - Switzerland left out: its UCI file keeps 123 of the paper's 143 patients and only 8 of its about 27 without disease (94% diseased against 81% by the paper's Table I, 85% of 85 in Basel and 74% of 58 in Zurich; the abstract gives 84%; cholesterol 0 in every row), so its disease rate is the release's, not the hospital's, and as a held-out hospital it would be scored on 8 patients without disease.
        - Missing values: "?" becomes NaN. Cholesterol 0 (49 Long Beach rows) and resting blood pressure 0 (1 row) are impossible and become NaN. Other missing values stay: whether a test was done is known before the angiogram, and the source's model was built for patients with only some tests (352 logistic regressions, one per clinically relevant set of variables, p. 305). The test hospitals did the thallium scan for a minority (Table II: 41 patients in Long Beach, 33 in Budapest) and the paper lists no fluoroscopy among their data (p. 306), so `ca` and `thal` are missing by the hospitals' practice, not by the release. Recording differs by hospital and is not harmonised: Hungary and Long Beach leave `slope` blank when there is no ST depression (188 of the 190 blanks in Hungary), Cleveland records it (99 rows); `restecg` left ventricular hypertrophy is 49% of Cleveland's patients and 2% of Hungary's. Harmonising `slope` changes the ROC AUC by under 0.003.
        - Target: `num` (0 = no narrowing over 50%, 1-4 = disease grades; the Hungarian file holds only 0/1) becomes the binary `heart_disease_diagnosis` (Yes/No), as in the study.
        - Codes get their labels from UCI's `heart-disease.names`: `sex`; `cp` typical angina, atypical angina, non-anginal pain, asymptomatic; `restecg` normal, ST-T wave abnormality, left ventricular hypertrophy; `slope` of the peak-exercise ST segment upsloping, flat, downsloping; `thal` normal, fixed defect, reversible defect. `fbs` (fasting blood sugar over 120 mg/dl) and `exang` (angina on exercise) stay 0/1 flags. `oldpeak` is the ST depression on exercise relative to rest; one Long Beach value is negative.
        - Anomaly: the Hungarian file keeps 294 of the paper's 425 patients (36% diseased against 38%); the paper took all catheterizations of 1983 to 1987 without prior infarction or valve disease (p. 306), and how the 294 were chosen is not stated.
        - Duplicates: the Long Beach pair of equal rows is one patient entered twice (the raw file gives both the same exercise and angiogram dates and the same ten vessel readings, which no other Long Beach pair shares), so one is dropped. The Hungarian pair is two patients (exams in March and May 1986) and stays.
        - Ordinal scales (2026-10-30, CLEAN-14): 1 columns typed as ordered categories in the order of the source's
          codebook (`ORDINAL_LEVELS`).
    """

    # Task
    target = "heart_disease_diagnosis"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Detrano et al. 1989 score reliability, the mean predicted probability against the disease rate (calibration in the large) and by quintiles (p. 306), and clinical utility, the percent correctly classified over the thresholds 0.2 to 0.8 they call relevant for angiography decisions (p. 307): no single threshold, so a threshold-free metric (MET-7); UCI's heart-disease.names reports accuracy at 0.5, a default. No costs of errors: UCI's costs/ folder holds the prices of the tests, and Statlog's 5:1 heart cost matrix belongs to a later 270-row cut of the Cleveland file, not to this source. ROC AUC per held-out hospital does not score reliability. roc_auc is the binary fallback."
    )
    grouping = Grouping(
        on="hospital",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a hospital: Cleveland Clinic, the Hungarian Institute of Cardiology (Budapest) or the VA Medical Center (Long Beach). The source's question is whether a probability model carries over to other hospitals: "This model, derived from the clinical and noninvasive test results of 303 patients undergoing angiography at the Cleveland Clinic in Cleveland, Ohio, was applied to a group of 425 patients undergoing angiography at the Hungarian Institute of Cardiology in Budapest, Hungary (disease prevalence 38%); 200 patients undergoing angiography at the Veterans Administration Medical Center in Long Beach, California (disease prevalence 75%); ..." (Detrano et al. 1989, abstract). So whole hospitals are held out and the model is not told the hospital. Each row is one patient and one prediction.
        """,
    )
    splits_comment = """
        Leave one hospital out: three splits, each training on two hospitals and testing on the third (Cleveland, Hungary, then Long Beach), one repeat, since repeating a split of three groups into three folds gives the same splits. The source built its model in Cleveland and applied it at the other hospitals; leaving each hospital out in turn generalises that design so that every hospital is tested once. With three hospitals the scores are three numbers and differ by hospital (Long Beach is the hardest). Unlike `covertype`'s three areas, the transfer is the source's design and no class drops out (curation notes).
    """
    accepted_check_warnings = {
        "task_group_count_low": "Three hospitals by design: the source built its model at one hospital and applied it "
        "at the others. The fourth hospital (Switzerland) is left out because its published file kept only 8 of its about "
        "27 patients without disease.",
        "splits_dimensions_off_protocol": "Leave one hospital out gives exactly three splits. More repeats would split "
        "the same three hospitals the same way, so they would add copies, not information.",
        "groups_test_groups_few": "Testing on one unseen hospital at a time is the task. Each fold still scores 199 to "
        "303 patients one by one (smallest class: 51). The signal carries over to unseen hospitals: the linear model "
        "beats the class shares at each of the three (task probes, ROC AUC 0.880, 0.898, 0.732). Most of the "
        "variation between folds comes from Long Beach, the hardest hospital.",
        "groups_largest_share_high": "Cleveland is a real hospital, one of three, not a catch-all value. When it is the "
        "test hospital, the model trains on the other two (493 patients), where two of Cleveland's tests were rarely "
        "recorded (`ca` for 5, `thal` for 62).",
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {h: pd.read_csv(raw_dir / f, header=None, names=COLUMNS) for h, f in HOSPITALS.items()}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # One table, with the hospital each file comes from
        df = pd.concat([d.assign(hospital=h) for h, d in raw.items()], ignore_index=True)
        # Drop the one Long Beach patient entered twice (same dates and vessel readings in the raw file); the
        # Hungarian pair of equal rows is two patients and stays
        twice = df.duplicated() & df["hospital"].eq("VA Long Beach")
        assert twice.sum() == 1
        df = df[~twice].reset_index(drop=True)
        # Proxy missing values: "?" and the impossible zeros of cholesterol and resting blood pressure
        df = df.replace("?", np.nan)
        numeric = [c for c in COLUMNS if c != "num"]
        df[numeric] = df[numeric].astype(float)
        df[["chol", "trestbps"]] = df[["chol", "trestbps"]].replace(0, np.nan)
        # Restore the labels of the codes
        for col, labels in LABELS.items():
            assert df[col].dropna().isin(labels).all(), col
            df[col] = df[col].map(labels)
        # Make target: presence (grades 1-4) against absence (0) of disease
        df["heart_disease_diagnosis"] = (df["num"].astype(int) > 0).map({True: "Yes", False: "No"})
        return df.drop(columns=["num"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS, categorical=["hospital", "sex", "cp", "fbs", "restecg", "exang", "slope", "thal"]
        )

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
        no_exercise_test = df[["thalach", "exang", "oldpeak"]].isna().all(axis=1)
        by = (
            df.assign(no_exercise_test=no_exercise_test)
            .groupby("hospital", observed=True)
            .agg(
                patients=(self.target, "size"),
                disease_pct=(self.target, lambda s: s.eq("Yes").mean() * 100),
                ca_missing_pct=("ca", lambda s: s.isna().mean() * 100),
                thal_missing_pct=("thal", lambda s: s.isna().mean() * 100),
                slope_missing_pct=("slope", lambda s: s.isna().mean() * 100),
                chol_missing_pct=("chol", lambda s: s.isna().mean() * 100),
                no_exercise_test=("no_exercise_test", "sum"),
            )
        )
        return [
            Decision(
                title="Split by hospital: train on two, test on the third",
                why=(
                    "The source built its model at one hospital and applied it at the others (Detrano et al. 1989, "
                    "p. 305), and the hospitals differ in disease rate and in which tests they recorded, as a new "
                    "hospital would. Trained on the other two hospitals, logistic regression reaches ROC AUC 0.880 on "
                    "Cleveland, 0.898 on Hungary and 0.732 on Long Beach. The paper has the Cleveland model "
                    "overpredicting disease by 10 points in Budapest and 5 in Long Beach (abstract, p. 307); our models overpredict in "
                    "Hungary too but underpredict in Long Beach, mostly for its patients without an exercise test. "
                    "ROC AUC within one hospital does not score this."
                ),
                evidence=by.round(0),
            )
        ]
