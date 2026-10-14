"""Curated dataset definition for `stroke_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

RAW_FILE = "train_ajEneEa.csv"
"""The contest's training file: 43,400 patients, 783 of them with a stroke."""

KAGGLE_STROKES = 249
KAGGLE_OTHERS = 4_861
"""fedesoriano's Kaggle file holds the first 249 stroke rows and the first 4,861 other rows of the training file."""

AGE_BANDS = [0, 40, 60, 70, 83]
AGE_LABELS = ["under 40", "40-59", "60-69", "70-82"]


class StrokePrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Has a patient had a stroke, judged from a few facts of the health record?",
        use_case=(
            "For example, a hospital chain screens its patients' records for a high stroke risk, to offer prevention;"
            " the contest asked whether a patient has had a stroke."
        ),
        row=(
            "One patient record of a hospital chain, from the McKinsey Analytics Online Hackathon of 2018 (43,400 "
            "patients; place and period not stated)."
        ),
        predicted=("Whether the patient has had a stroke (1.8%), at a time not stated, before or after the record."),
        known=(
            "Age, sex, high blood pressure, heart disease, average blood glucose, smoking status, whether ever "
            "married, work type and urban or rural residence."
        ),
        split="Random patients.",
        changes=(
            "We use the contest's whole training file instead of the Kaggle cut, and drop the body-mass index, whose "
            "missing values follow a stroke."
        ),
        fit="approximate",
        fit_reason=(
            "The record has no dates, so the label is a stroke at any time rather than within a fixed time after the "
            "record, and some facts may be recorded after it. Marriage, work type and residence look generated: they "
            "carry nothing beyond age."
        ),
    )

    # Dataset
    unique_name = "stroke_prediction"
    year = "2018"
    domain = "medical & healthcare"
    source = "Other"  # the McKinsey Analytics Online Hackathon on Analytics Vidhya's DataHack, 2018-04-14
    source_url = "https://www.analyticsvidhya.com/datahack/contest/mckinsey-analytics-online-hackathon/"
    license = "None stated on the contest page; the identical Mendeley Data copy is CC BY-NC 3.0"
    download_description = """
        We download the training file of the McKinsey Analytics Online Hackathon (Analytics Vidhya DataHack,
        2018-04-14) from the link on the contest page. The contest's test file (test_v2akXPA.csv, 18,601 patients)
        has no labels and is not used.
        train_ajEneEa.csv: sha256 540986aebc2cc8a9a6c907df5ea4fdf93e8b5e3dabacdd727337363757b539aa

        mkdir -p local-data-warehouse/stroke_prediction && cd local-data-warehouse/stroke_prediction
        wget https://datahack-prod.s3.amazonaws.com/train_file/train_ajEneEa.csv

        The same file, byte for byte, is dataset.csv inside dataset.rar of Liu, Fan and Wu's Mendeley Data deposit
        (doi:10.17632/x8ygrw87jw.1), should the contest link stop working:
        wget -O dataset.rar https://data.mendeley.com/public-files/datasets/x8ygrw87jw/files/ed922255-74f5-40c7-97ff-2fa1bbb385e4/file_downloaded
        7z e dataset.rar  # or: bsdtar -xf dataset.rar, or: unrar e dataset.rar
        mv dataset.csv train_ajEneEa.csv && rm dataset.rar
        Without a RAR tool, the same with Python (tested on 2026-10-06, gives the sha256 above):
        uv run --no-project --with unrar-cffi python -c "from unrar.cffi import rarfile; open('train_ajEneEa.csv', 'wb').write(rarfile.RarFile('dataset.rar').read('dataset.csv'))" && rm dataset.rar
    """
    bibtex = r"""
        @misc{mckinsey2018healthcare,
          author = {{McKinsey \& Company} and {Analytics Vidhya}},
          title = {McKinsey Analytics Online Hackathon - Healthcare Analytics},
          year = {2018},
          howpublished = {\url{https://www.analyticsvidhya.com/datahack/contest/mckinsey-analytics-online-hackathon/}},
          note = {24-hour contest on Analytics Vidhya DataHack, 14 April 2018: stroke prediction for a chain of hospitals}
        }
        @misc{liu2019stroke,
          author = {Liu, Tianyu and Fan, Wenhui and Wu, Cheng},
          title = {Data for: A hybrid machine learning approach to cerebral stroke prediction based on imbalanced medical-datasets},
          year = {2019},
          publisher = {Mendeley Data},
          doi = {10.17632/x8ygrw87jw.1},
          note = {Version 1; the data of Liu et al., Artificial Intelligence in Medicine 101:101723, 2019}
        }
    """
    curation_comments = """
        We start with train_ajEneEa.csv, the training file of the McKinsey Analytics Online Hackathon - Healthcare Analytics (Analytics Vidhya DataHack, 2018-04-14).

        - Prediction point: a patient's record in a hospital chain's health records. The file has no dates and the label is "0 - no stroke, 1 - suffered stroke" (data dictionary), so the task is the contest's: estimate from the record, written before or after a stroke, whether the patient has had one.
        - Source: the record links fedesoriano's Kaggle "Stroke Prediction Dataset", a cut of this file (its first 249 stroke rows and first 4,861 others). We use the whole file: 8.5 times the rows and 3.1 times the strokes, at the contest's stroke share (first decision table).
        - Partly generated or altered: Residence_type, ever_married and work_type carry nothing beyond age. For adults, a logistic regression on 1-year ages gains nothing from them (likelihood-ratio p = 0.47 for Residence_type, 0.39 for ever_married, 0.68 to 0.88 for the work types, against 7e-145 for sex), where real survey data (BRFSS 2015) show the dependence. Women and men are married alike at every age (third decision table). The glucose level has no value below 55.00 and a spike at 65. We found no statement of how the file was made. We keep the columns as published: the three add nothing to a model (regularised LightGBM ROC AUC 0.850 with and without them), and dropping them is the option if the dataset stays.
        - Leak, dropped: bmi. A missing BMI follows the stroke: with all other columns fixed, a stroke multiplies the odds of a missing BMI by 3.69 (95% CI 2.99 to 4.57; second decision table). A likely reason is a record made at the stroke admission, where no one weighed the patient. The BMI values add nothing beyond the missingness (ROC AUC 0.847 without the column, 0.846 with the missing values drawn at random), so the whole column goes.
        - We drop the Patient ID (`id`), unique per row.
        - Features as published: hypertension and heart_disease stay 0/1; gender, ever_married, work_type, Residence_type and smoking_status are categories. The target maps 0/1 to No/Yes.
        - Missing values: smoking_status is blank for 30.6% of the rows, all children under 10 among them. It is missing independently of the stroke (odds ratio 0.96), so it stays missing (the Kaggle cut writes "Unknown").
        - Anomaly: ages under 2 are years plus 0.08 per month, and ages 78 to 82 hold more patients per year than 70 to 77, as if older ages were folded in. Kept as published.
        - Duplicates: without bmi, 62 rows repeat an earlier row, none with a stroke; each pair differs in BMI in the raw file, so they are different patients and stay.
        - IID split: one row per patient, and a model is used for new patients. The contest also scored ROC AUC.
        - Note: age alone scores ROC AUC 0.840 and a regularised LightGBM 0.850, above age on 9 of 9 splits; no task-probe flag.
    """

    # Task
    target = "stroke"
    problem_type = "binary_classification"
    accepted_check_warnings = {
        "dataset_pure_feature_value": (
            "work_type = children holds the 6,156 patients aged 0.08 to 16 with that work type; 2 of them had a "
            "stroke (0.03%, against 1.8% overall). Strokes are rare in children: an age effect, not a leak."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # the Patient ID is unique per row and says nothing about the label; a missing BMI follows the stroke
        # (curation_comments, Leak), and the BMI values add nothing beyond the missingness
        df = drop_columns(df, ["id", "bmi"])
        # data dictionary: "0 - no stroke, 1 - suffered stroke"
        df[self.target] = df[self.target].map({0: "No", 1: "Yes"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["gender", "ever_married", "work_type", "Residence_type", "smoking_status"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        def summary(frame: pd.DataFrame) -> dict[str, float]:
            stroke = frame["stroke"].eq(1)
            no_bmi = frame["bmi"].isna()
            return {
                "rows": len(frame),
                "strokes": int(stroke.sum()),
                "stroke share (%)": round(100 * stroke.mean(), 2),
                "rows without BMI": int(no_bmi.sum()),
                "strokes without BMI": int((stroke & no_bmi).sum()),
                "rows without smoking status": int(frame["smoking_status"].isna().sum()),
            }

        stroke = raw["stroke"].eq(1)
        kaggle = pd.concat([raw[stroke].head(KAGGLE_STROKES), raw[~stroke].head(KAGGLE_OTHERS)])
        versions = pd.DataFrame(
            [summary(raw), summary(kaggle)],
            index=[
                "Contest training file (shipped)",
                "fedesoriano's Kaggle cut: its first 249 strokes and first 4,861 others",
            ],
        )

        # BMI missingness by age band: strokes, and patients without a stroke with and without a comorbidity
        frame = pd.DataFrame(
            {
                "age band": pd.cut(raw["age"], AGE_BANDS, right=False, labels=AGE_LABELS),
                "no_bmi": raw["bmi"].isna(),
                "stroke": stroke,
                "comorbid": raw["hypertension"].eq(1) | raw["heart_disease"].eq(1),
            }
        )
        band = frame.groupby("age band", observed=True)

        def missing_share(mask: pd.Series) -> pd.Series:
            return (100 * frame.loc[mask, "no_bmi"].groupby(frame.loc[mask, "age band"], observed=True).mean()).round(1)

        bmi = pd.DataFrame(
            {
                "patients": band.size(),
                "strokes": band["stroke"].sum(),
                "BMI missing, strokes (%)": missing_share(frame["stroke"]),
                "BMI missing, no stroke, hypertension or heart disease (%)": missing_share(
                    ~frame["stroke"] & frame["comorbid"]
                ),
                "BMI missing, no stroke, neither (%)": missing_share(~frame["stroke"] & ~frame["comorbid"]),
            }
        )

        # the three columns that carry nothing beyond age: shares by age band and sex, adults
        adults = df[df["gender"].isin(["Female", "Male"]) & df["age"].ge(20)]
        bands = pd.cut(adults["age"], [20, 25, 30, 35, 45, 55, 65], right=False)
        rows = {}
        for (interval, sex), group in adults.groupby([bands, adults["gender"]], observed=True):
            rows[(f"{interval.left:.0f}-{interval.right - 1:.0f}", str(sex))] = {
                "patients": len(group),
                "ever married (%)": round(100 * group["ever_married"].eq("Yes").mean(), 1),
                "self-employed (%)": round(100 * group["work_type"].eq("Self-employed").mean(), 1),
                "government job (%)": round(100 * group["work_type"].eq("Govt_job").mean(), 1),
                "urban (%)": round(100 * group["Residence_type"].eq("Urban").mean(), 1),
            }
        columns = pd.DataFrame.from_dict(rows, orient="index").rename_axis(["age", "gender"])
        return [
            Decision(
                "The contest's training file, not the Kaggle cut",
                "The record links fedesoriano's Kaggle file, a cut of this file (curation_comments, Source); the "
                "whole file has 8.5 times the rows and 3.1 times the strokes, at the contest's stroke share.",
                versions,
            ),
            Decision(
                "bmi dropped: a missing BMI follows the stroke",
                "In every age band, 16.5% to 20.8% of the strokes have no BMI, against 9.3% to 14.5% of the patients "
                "without a stroke but with hypertension or heart disease and 1.6% to 3.6% of the others. With age, sex, "
                "the comorbidities, glucose, smoking and the other columns fixed, a stroke multiplies the odds of a "
                "missing BMI by 3.7 (curation_comments, Leak).",
                bmi,
            ),
            Decision(
                "Residence_type, ever_married and work_type kept as published, though they carry nothing beyond age",
                "Women and men are married alike and hold the same work types at every age, and about half of every "
                "group is urban; in BRFSS 2015, 53.8% of women and 40.3% of men aged 25-29 were ever married "
                "(curation_comments, Partly generated). The three columns add nothing to a model; dropping them is "
                "the option if the dataset stays.",
                columns,
            ),
        ]
