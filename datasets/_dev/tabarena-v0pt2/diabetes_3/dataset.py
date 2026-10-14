"""Curated dataset definition for `diabetes_3` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary

# The file's headers and the names we give them, in the file's column order. The names spell out the authors' own
# headers in the 2002 version of the file (age sex bmi map tc ldl hdl tch tg glu y), checked in `_decisions`.
COLUMN_NAMES = {
    "AGE": "age",
    "SEX": "sex",
    "BMI": "bmi",
    "BP": "mean_arterial_pressure",
    "S1": "total_cholesterol",
    "S2": "ldl_cholesterol",
    "S3": "hdl_cholesterol",
    "S4": "total_cholesterol_hdl_ratio",
    "S5": "log_triglycerides",
    "S6": "glucose",
    "Y": "disease_progression_one_year",
}


class Diabetes3(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How far will a diabetes patient's disease progress over the next year?",
        use_case=(
            "At a patient's baseline visit, a physician predicts the disease progression one year later from routine "
            "measurements; the paper aims at accurate baseline predictions for future patients, for example to plan "
            "follow-up."
        ),
        row=("One diabetes patient at the baseline visit (442 patients; clinic, place and period not stated)."),
        predicted=(
            "A quantitative measure of disease progression one year after baseline, from 25 to 346; the source does "
            "not say what it measures."
        ),
        known=(
            "Age, sex, body mass index, mean arterial blood pressure and six blood measurements (total, LDL and HDL "
            "cholesterol, the total-to-HDL ratio, triglycerides and glucose)."
        ),
        split="Random patients, so the test data stands for new patients of the same clinic.",
        fit="direct",
        fit_reason=(
            "The features are taken at baseline and the outcome a fixed year later, as the paper describes. The "
            "measure, the clinic and the units are not documented, and the glucose values look low for diabetes "
            "patients."
        ),
    )

    # Dataset
    unique_name = "diabetes_3"
    year = "2002"
    domain = "medical & healthcare"
    source = "Other"  # published with the paper; the file is on Trevor Hastie's LARS page at Stanford (paper, Sec. 7)
    source_url = "https://doi.org/10.1214/009053604000000067"
    license = None  # none stated on the page or in the paper; lars (GPL-2) and scikit-learn (BSD-3) redistribute it
    download_description = """
        The file is `diabetes.data` on Trevor Hastie's LARS page at Stanford
        (https://hastie.su.domains/Papers/LARS/diabetes.data, formerly under web.stanford.edu/~hastie/), which the paper
        names as the place of the data (Sec. 7). That host refused connections on 2026-10-07; the Wayback Machine last
        captured it live on 2026-08-04, with the same file. We take the Wayback capture of 2021-10-21, which is
        byte-identical to the captures of 2010-08-15 and 2026-08-04 and to the copy on Dennis Boos's NCSU page.

        mkdir -p local-data-warehouse/diabetes_3
        wget -O local-data-warehouse/diabetes_3/diabetes.data "https://web.archive.org/web/20211021183551id_/https://web.stanford.edu/~hastie/Papers/LARS/diabetes.data"
        # when the Wayback Machine is offline, the NCSU copy gives the same bytes:
        # wget -O local-data-warehouse/diabetes_3/diabetes.data "https://www4.stat.ncsu.edu/~boos/var.select/diabetes.tab.txt"
        echo "af0c583c28547d76cd2db5f5c67de7e8  local-data-warehouse/diabetes_3/diabetes.data" | md5sum -c
    """
    bibtex = """
        @article{efron2004least,
          title={Least angle regression},
          author={Efron, Bradley and Hastie, Trevor and Johnstone, Iain and Tibshirani, Robert},
          journal={The Annals of Statistics},
          volume={32},
          number={2},
          pages={407--499},
          year={2004},
          doi={10.1214/009053604000000067}
        }
    """
    curation_comments = """
        We start with `diabetes.data` from Trevor Hastie's LARS page at Stanford: the unstandardised data of Efron, Hastie, Johnstone & Tibshirani (2004), 442 patients with the headers AGE, SEX, BMI, BP, S1-S6 and Y.

        - Prediction point: the baseline visit of a diabetes patient. The paper predicts disease progression one year later from ten baseline measurements (Sec. 1), so no column is dropped.
        - We use the unstandardised file, as the record asks; OpenML 44223, scikit-learn's default `load_diabetes()` and the R package lars ship the features scaled.
        - We rename the columns to what they measure, spelling out the authors' headers in the 2002 version of the file (`age sex bmi map tc ldl hdl tch tg glu y`). The data confirms them row by row (decision table): S2 is the Friedewald LDL from S1, S3 and S5 = ln(tg), S4 is S1 / S3, and the blood pressures that are not whole numbers end in .33 or .67, as mean arterial pressures do.
        - Note: `ldl_cholesterol` and `total_cholesterol_hdl_ratio` are computed from other columns; we keep them as two of the paper's ten covariates.
        - The source does not say which `sex` code (1 or 2) is which; we keep the two codes as categories.
        - Anomaly: the cholesterol ratio is given with decimals in 62 rows and the blood pressure in thirds in 42; in the other rows both are whole numbers, which may mark two recording batches. The format does not carry the target (decision table), so we keep the values as written.
        - Anomaly, cohort: the paper names no clinic, inclusion rule or units, and the data does not look like its "442 diabetes patients": read as fasting plasma glucose in mg/dL, `glucose` (58 to 124) stays below the diabetes threshold of 126. Without units the data cannot settle it; we keep the dataset, as the curators accepted its origin.
        - The target is the paper's response on its own scale (25 to 346, skewness 0.44), not logged. The paper fits it by least squares, which the default RMSE matches.
        - IID: one row per patient, no visit dates and no time trend in the file order. No missing values or duplicate rows.
        - Not trivial, despite the record's `Trivial` marker: on all 60 shipped splits, the best of least squares, ridge and a random forest (R^2 0.49) beats the best single feature (0.30) by at least 0.097.
    """

    # Task
    target = "disease_progression_one_year"
    problem_type = "regression"

    accepted_check_warnings = {
        "meta_license_unknown": (
            "Neither the LARS page nor the paper states a licence for the data. The R package lars (GPL-2) and "
            "scikit-learn (BSD-3-Clause) redistribute it under their package licences."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "diabetes.data", sep="\t")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # the file's headers are codes (S1-S6); name each column by what it measures, in the file's order
        return raw.rename(columns=COLUMN_NAMES, errors="raise")

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["sex"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        tc, ldl, hdl, ratio, log_tg, pressure = raw["S1"], raw["S2"], raw["S3"], raw["S4"], raw["S5"], raw["BP"]
        friedewald = tc - hdl - np.exp(log_tg) / 5
        ratio_whole = ratio == ratio.round(0)
        ratio_ok = np.where(ratio_whole, ratio == (tc / hdl).round(0), (ratio - (tc / hdl).round(2)).abs() <= 0.011)
        names = pd.DataFrame(
            {
                "raw column": ["S2", "S4", "BP"],
                "2002 header": ["ldl", "tch", "map"],
                "name": ["ldl_cholesterol", "total_cholesterol_hdl_ratio", "mean_arterial_pressure"],
                "check": [
                    "S2 = S1 - S3 - exp(S5) / 5 within 0.1 (Friedewald LDL, mg/dL)",
                    "S4 = S1 / S3 rounded to a whole number or to two decimals",
                    "3 x BP is a whole number within 0.015: (systolic + 2 x diastolic) / 3",
                ],
                "rows matching": [
                    int(((ldl - friedewald).abs() <= 0.1).sum()),
                    int(ratio_ok.sum()),
                    int(((3 * pressure - (3 * pressure).round(0)).abs() <= 0.015).sum()),
                ],
                "rows": [len(raw)] * 3,
            }
        )
        pressure_whole = pressure == pressure.round(0)
        formats = pd.DataFrame(
            {
                "cholesterol ratio": np.where(ratio_whole, "whole", "decimals"),
                "blood pressure": np.where(pressure_whole, "whole", "thirds"),
                "target": raw["Y"],
            }
        )
        by_format = (
            formats.groupby(["cholesterol ratio", "blood pressure"])["target"]
            .agg(rows="size", mean="mean", median="median")
            .round(1)
        )
        r2 = float(np.corrcoef((~ratio_whole).astype(int), raw["Y"])[0, 1] ** 2)
        return [
            Decision(
                "Columns named by what they measure, checked row by row",
                "The file codes its columns BP and S1-S6. The 2002 version of the same file on the LARS page carries "
                "the authors' own headers (map, tc, ldl, hdl, tch, tg, glu), which we spell out. The derived columns "
                "agree with the others: LDL is the Friedewald estimate (so S5 is the log of the triglycerides), S4 is "
                "total cholesterol over HDL, and the blood pressure is a mean arterial pressure (whole or in thirds).",
                names,
            ),
            Decision(
                "Two number formats, kept as written",
                "Some rows give the cholesterol ratio with decimals and the blood pressure in thirds, which may mark a "
                f"second recording batch. The target barely differs by format (R^2 {r2:.4f} for the ratio's format), "
                "so the format is no leak.",
                by_format,
            ),
        ]
