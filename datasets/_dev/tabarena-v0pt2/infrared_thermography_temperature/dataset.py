"""Curated dataset definition for `infrared_thermography_temperature` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary

FACIAL = (
    "Max1R13_",
    "Max1L13_",
    "aveAllR13_",
    "aveAllL13_",
    "T_RC",
    "T_RC_Dry",
    "T_RC_Wet",
    "T_RC_Max",
    "T_LC",
    "T_LC_Dry",
    "T_LC_Wet",
    "T_LC_Max",
    "RCC",
    "LCC",
    "canthiMax",
    "canthi4Max",
    "T_FHCC",
    "T_FHRC",
    "T_FHLC",
    "T_FHBC",
    "T_FHTC",
    "T_FH_Max",
    "T_FHC_Max",
    "T_Max",
    "T_OR",
    "T_OR_Max",
)
"""The 26 facial temperatures of one imaging round (PhysioNet `_Table1.pdf`); the file appends the round number."""


def image_columns(round_: int) -> list[str]:
    """The blackbody offset and the 26 facial temperatures of one imaging round, as the file names them."""
    return [f"T_offset{round_}", *(f"{name}{round_}" for name in FACIAL)]


ROUND_1 = tuple(image_columns(1))
"""The columns of the first imaging round: the features, named as in the file."""

SAME_MEASUREMENT = ("170208-03", "180228-01")
"""Two subject codes, a year apart, that hold one measurement: rounds 1-3 of both cameras agree within 0.02 °C."""


def day_effect(values: pd.Series, day: pd.Series) -> dict[str, float]:
    """How much of a quantity lies between measurement days.

    The share of its variance between the day means (eta squared), the same share with shuffled days (mean of 1,000
    seeded shuffles), the permutation p-value, and the intraclass correlation ICC(1) of one-way ANOVA.
    """
    keep = values.notna().to_numpy()
    v = values.to_numpy(dtype=float)[keep]
    groups = pd.factorize(day.to_numpy()[keep])[0]
    total = ((v - v.mean()) ** 2).sum()

    def between(g: np.ndarray) -> float:
        sizes = np.bincount(g)
        means = np.bincount(g, weights=v) / sizes
        return float((sizes * (means - v.mean()) ** 2).sum() / total)

    rng = np.random.default_rng(0)
    observed = between(groups)
    shuffled = np.array([between(rng.permutation(groups)) for _ in range(1000)])
    n, n_days = len(v), groups.max() + 1
    sizes = np.bincount(groups)
    ms_between = observed * total / (n_days - 1)
    ms_within = (1 - observed) * total / (n - n_days)
    k0 = (n - (sizes**2).sum() / n) / (n_days - 1)
    return {
        "share between days": observed,
        "same with shuffled days": shuffled.mean(),
        "permutation p": (1 + (shuffled >= observed).sum()) / (1 + len(shuffled)),
        "ICC": (ms_between - ms_within) / (ms_between + (k0 - 1) * ms_within),
    }


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Age": ["18-20", "21-25", "21-30", "26-30", "31-40", "41-50", "51-60", ">60"],  # open-ended
}


class InfraredThermographyTemperature(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is a person's oral temperature, estimated from one thermal image of the face?",
        use_case=(
            "At a clinic's triage station, after a person has rested 15 minutes in the room and answered a short "
            "intake, a thermal camera images the face once and estimates the oral temperature, to decide whether to "
            "measure by mouth; a maker of such cameras fits the same mapping to calibrate a device."
        ),
        row=(
            "One person imaged once and measured by mouth in an FDA study of infrared fever screening at the "
            "University of Maryland Health Center, College Park, from November 2016 to May 2018, mostly students "
            "(1,001 people)."
        ),
        predicted=(
            "The oral temperature, the mean of two thermometer readings in monitor mode, in °C; the typical spread is"
            " about 0.5 °C."
        ),
        known=(
            "The first image's temperatures at 26 places of the face and the camera's reference offset; the room "
            "temperature and humidity, the distance to the camera and the time of day, which the station records; "
            "and the sex, age group, ethnicity and whether cosmetics are worn, which the person states at intake."
        ),
        split=(
            "Random people, so the test data stands for new people screened with the same set-up; people measured on "
            "the same day fall on both sides. The set-up changed between the two study years (two locations, the "
            "distance shortened from about 0.8 to 0.6 m), and a calibration fitted on the first year over-predicts "
            "the second by about 0.08 °C."
        ),
        changes=(
            "We keep only the first image, taken before the thermometer, and drop the 17 people without a complete "
            "first image, whose next image was taken after it. We drop the fast-mode oral reading, a second "
            "measurement of the target."
        ),
        fit="direct",
        fit_reason=(
            "The station has the camera's readings, the room sensors and the intake answers when the image is "
            "taken, and the oral reading is its reference. Both papers call the conditions a best case (15 minutes of "
            "rest, key points partly placed by hand, blurred images excluded), and the task covers one university "
            "clinic's cameras, rooms and people (87% aged 18 to 25)."
        ),
    )

    # Dataset
    unique_name = "infrared_thermography_temperature"
    year = "2023"
    domain = "medical & healthcare"
    source = "Other"
    source_url = "https://doi.org/10.13026/3bhc-9065"
    license = "CC0 1.0"
    download_description = """
        We download the FLIR camera file of version 1.0.0 from PhysioNet and check it against the release's SHA256SUMS.txt.

        mkdir -p local-data-warehouse/infrared_thermography_temperature && cd local-data-warehouse/infrared_thermography_temperature
        wget https://physionet.org/files/face-oral-temp-data/1.0.0/FLIR_groups1and2.csv https://physionet.org/files/face-oral-temp-data/1.0.0/SHA256SUMS.txt
        grep FLIR_groups1and2.csv SHA256SUMS.txt | sha256sum -c -
    """
    bibtex = """
        @misc{wang2023facial,
          author = {Wang, Quanzeng and Zhou, Yangling and Ghassemi, Pejman and Chenna, Dwith and Chen, Michelle and Casamento, Jon and Pfefer, Joshua and Mcbride, David},
          title = {Facial and oral temperature data from a large set of human subject volunteers (version 1.0.0)},
          howpublished = {PhysioNet},
          year = {2023},
          doi = {10.13026/3bhc-9065},
          url = {https://doi.org/10.13026/3bhc-9065}
        }
        @article{wang2022infrared,
          author = {Wang, Quanzeng and Zhou, Yangling and Ghassemi, Pejman and McBride, David and Casamento, Jon P. and Pfefer, T. Joshua},
          title = {Infrared Thermography for Measuring Elevated Body Temperature: Clinical Accuracy, Calibration, and Evaluation},
          journal = {Sensors},
          volume = {22},
          number = {1},
          pages = {215},
          year = {2022},
          doi = {10.3390/s22010215}
        }
    """
    curation_comments = """
        We start with FLIR_groups1and2.csv from PhysioNet (version 1.0.0): 1,020 subjects of an FDA fever-screening study, each with four rounds of facial temperatures, two oral readings, demographics and the room conditions.

        - Prediction point: at a clinic's triage station, after 15 minutes of rest in the room, the camera images a person once and the oral temperature is estimated from that image (facial temperatures, blackbody offset), the room readings and distance the station records, the time of day and what the person states at intake.
        - We keep round 1 (`T_offset1` and the 26 facial temperatures) and drop rounds 2-4, imaged after the first oral reading had put the thermometer under the tongue. Both papers analysed round 1 only (decision table). The UCI copy is not used: its `*_1` columns average each subject's rounds.
        - We drop the 17 subjects without a complete round-1 image (5 of them at or above 37.5 °C, 4 at or above 38 °C; decision table): their next complete image (round 2 or 3) was taken after the first oral reading, so they lack the image the prediction acts on. Left missing, the gap would mark a group that is 29% febrile against 10.6% elsewhere.
        - Target: `aveOralM`, the mean of two oral readings in monitor mode, the reference of both papers. We drop `aveOralF`, the same two readings in fast mode: a measurement of the target.
        - We keep `T_atm`, `Humidity`, `Distance` and `T_offset1`, which the v1 notebook dropped: the screening station records all four when it takes the image.
        - We convert `Time` to the decimal hour `TimeOfDay`, and drop `SubjectID` (the measurement date and a number) and `Date`.
        - We drop subjects 170208-03 and 180228-01, one measurement under two codes a year apart: their images and oral readings agree, while the date, ethnicity and room readings differ (decision table).
        - One `Distance` of 79.0, among 0.60-0.77 m that day, is in centimetres: we set 0.79 m.
        - IID over subjects: each row is a new person, in the file once, and the day's conditions (`T_atm`, `Humidity`, `Distance`, `T_offset1`) are recorded for every new person, so they are features, not a group to hold out. The source calibrated on a random 60% of the subjects. The measurement day carries a small part of the target and more of the calibration offset (decision table); `hidden_groups.py` finds no hit.
        - The split comparisons are evidence, not the reason (random forest, 10 x 3 folds unless stated): folds grouped by day score as random ones do (R^2 0.699 against 0.700). The set-up changed between the two study years (two locations; median distance 0.80 m in the first winter, 0.60 m in the second). In 6 expanding windows over the newest half of the days, training on all earlier subjects instead of a random set of the same size changes the RMSE by +0.5% to +6.7% across ridge, forest and LightGBM; the first window of the second year is 5-29% worse with a bias of +0.1 °C, and a first-year calibration over-predicts the second year by 0.06-0.09 °C.
        - Not trivial: a one-feature segmented calibration of `T_Max1` in the source's style (our 4-knot linear spline; Wang 2022 gives no knots) reaches RMSE 0.276 °C, an additive model of every numeric feature 0.264 °C, better on 29 of 30 splits.
        - Anomaly: `Age` has an overlapping bin 21-30 for 10 subjects, and `aveOralM` lies on a 0.05 °C grid shifted by -0.01 °C, which does not change the RMSE. Both kept.
        - Scope (SEL-15, amended 2026-10-21, Lennart): each column is a blackbody-compensated temperature at a named facial site, the camera is used as a thermometer, the target is the same physical quantity measured by mouth, and the release holds no images, so the readings are measurements, not image descriptors (SEL-13). satimage and wilt, where an imaging sensor's values serve to recognise what the image shows, are the counter-cases.
        - Split decision (2026-10-21, Lennart): IID, not temporal. The task learns a calibration, a function of the inputs that should be the same on two different days when the other inputs are the same, so we expect no real signal across time. The year-to-year shift measured above (a first-year calibration over-predicts the second year by 0.06-0.09 °C; past-only training costs +0.5% to +6.7% RMSE) is recorded, and a temporal variant stays a candidate (SPLIT-31).
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 1 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`); 1 hold a state outside the scale, placed by the
          curator's rule (missing when the column has no other missing value, else the lowest level; a state that is
          simply not on the scale, such as Other, is missing).
    """

    # Task
    target = "aveOralM"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="root-mean-square difference A_rms (with clinical bias and its SD)",
        reference="Wang et al. 2022, Sensors 22(1):215, Sec. 2.5-2.6 (PMC8749858)",
        definition=(
            "A_rms = sqrt(mean((T_oral_estimated - T_ref)^2)) in degrees C; the paper reports it and the "
            "clinical bias per T_ref interval (<37, 37-38, >38 C)."
        ),
    )

    # Splits
    splits_comment = """
        Default splits: repeated 3-fold cross-validation over the subjects, one row each. Wang et al. (2022, Sec. 2.5) calibrated on a random 60% of the subjects and tested on the other 40%, and note that a random split of one pool may bias the estimate upwards (Sec. 4.5). Subjects measured on the same day fall on both sides of a split: 94-99% of the test subjects of a fold share their day with a training subject. Each row is a new person, and the day's conditions are recorded as features for every person. The set-up changed between the two study years (two locations, the median distance from 0.80 to 0.60 m), and a first-year calibration over-predicts the second year by 0.06-0.09 °C. The curation notes compare this split with folds grouped by day, which score the same, and with a temporal split on the date. We keep IID (Lennart, 2026-10-21): the calibration is a function of the inputs that should not depend on the day, so we expect no real signal across time; the measured shift between the years is the cost, and a temporal variant stays a candidate.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # two title rows (the round of each block, the papers' symbols) sit above the column names
        return pd.read_csv(raw_dir / "FLIR_groups1and2.csv", header=2, encoding="utf-8-sig")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # round 1, the target and what a screening knows, in the file's column order; this drops `SubjectID`, rounds
        # 2-4, `aveOralF`, `Date` and the empty separator columns
        keep = [
            *ROUND_1,
            self.target,
            "Gender",
            "Age",
            "Ethnicity",
            "T_atm",
            "Humidity",
            "Distance",
            "Cosmetics",
            "Time",
        ]
        # one measurement stored under two subject codes whose date, ethnicity and room readings differ: drop both
        twins = raw["SubjectID"].isin(SAME_MEASUREMENT)
        assert twins.sum() == 2
        assert raw.loc[twins, list(ROUND_1)].diff().iloc[1].abs().max() < 0.0105
        # the 17 subjects without a complete round-1 image: their next image (round 2 or 3) was taken after the first
        # oral reading, so they lack the input the prediction acts on
        complete = raw[list(ROUND_1)].notna().all(axis=1)
        df = raw.loc[~twins & complete, keep].copy()
        # one distance recorded in centimetres (79.0; the subject's day has 0.60-0.77 m)
        df.loc[df["Distance"] > 10, "Distance"] = df["Distance"] / 100
        # the time of the measurement as the decimal hour
        df["Time"] = pd.to_timedelta(df["Time"]).dt.total_seconds() / 3600
        return df.rename(columns={"Time": "TimeOfDay"})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # Cosmetics is a 0/1 flag (CLEAN-14)
        return FeatureTypes(ordinal=ORDINAL_LEVELS, categorical=["Gender", "Age", "Ethnicity", "Cosmetics"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        clean = self._clean(raw)  # the shipped subjects and values, indexed like `raw`
        kept = raw.loc[clean.index]
        target = clean[self.target]
        febrile = target >= 37.5

        sites = {
            "canthiMax": "extended canthi, max",
            "T_Max": "whole face, max",
            "T_OR": "mouth, mean of the 4 warmest pixels",
            "T_OR_Max": "mouth, max",
            "T_FHC_Max": "forehead centre, max",
        }
        rounds = {}
        for name, site in sites.items():
            values = kept[[f"{name}{k}" for k in (1, 2, 3, 4)]]
            rounds[f"{name} ({site})"] = {
                "corr. round 1": values.iloc[:, 0].corr(target),
                "corr. round 2": values.iloc[:, 1].corr(target),
                "corr. round 3": values.iloc[:, 2].corr(target),
                "corr. round 4 (mouth open)": values.iloc[:, 3].corr(target),
                "corr. mean of rounds (UCI copy)": values.mean(axis=1).corr(target),
                "round 2 minus round 1 (°C)": (values.iloc[:, 1] - values.iloc[:, 0]).mean(),
                "round 4 minus round 1 (°C)": (values.iloc[:, 3] - values.iloc[:, 0]).mean(),
            }

        others = raw[~raw["SubjectID"].isin(SAME_MEASUREMENT)]
        cohort = (
            others[list(ROUND_1)]
            .notna()
            .all(axis=1)
            .map({True: "complete round-1 image (kept)", False: "incomplete round-1 image (dropped)"})
        )
        oral = others[self.target]
        retakes = pd.DataFrame(
            {
                "subjects": cohort.value_counts(),
                "oral temperature >= 37.5 °C": (oral >= 37.5).groupby(cohort).sum(),
                "oral temperature >= 38.0 °C": (oral >= 38).groupby(cohort).sum(),
                "share >= 37.5 °C": (oral >= 37.5).groupby(cohort).mean().round(3),
            }
        ).rename_axis("cohort")

        # the measurement day is the date part of the subject id (yymmdd-n)
        day = kept["SubjectID"].str.split("-").str[0]
        quantities = {
            "aveOralM (target)": target,
            "aveOralM >= 37.5 °C": febrile.astype(float),
            "aveOralM minus T_Max1 (calibration offset)": target - clean["T_Max1"],
            "T_atm": clean["T_atm"],
            "Humidity": clean["Humidity"],
            "Distance": clean["Distance"],
            "T_offset1": clean["T_offset1"],
        }
        days = pd.DataFrame({name: day_effect(values, day) for name, values in quantities.items()}).T.round(3)

        twins = raw[raw["SubjectID"].isin(SAME_MEASUREMENT)].set_index("SubjectID")
        fields = ["Date", "Time", "Ethnicity", "T_atm", "Humidity", "Gender", "Age", "Distance", "Cosmetics"]
        fields += ["aveOralM", "aveOralF", "T_offset1", "T_Max1", "canthiMax1", "T_OR1"]
        pair = twins[fields].astype(str).T
        rounds_1_3 = [c for r in (1, 2, 3) for c in image_columns(r)]
        largest = f"{twins[rounds_1_3].diff().iloc[1].abs().max():.2f}"
        pair.loc["largest difference of the 81 image values of rounds 1-3 (°C)"] = [largest, largest]
        return [
            Decision(
                "Round 1 of the FLIR camera, not the mean of the four rounds (the UCI copy)",
                "Both papers analysed the first round only; Zhou et al. (2020) did so to approximate a realistic "
                "screening. The first oral reading follows the round-1 image, so rounds 2-4 were imaged after the "
                "thermometer had been under the tongue, and the mouth reads warmer from round 2 on. The mean over the "
                "rounds, which the UCI copy ships as `*_1`, correlates more with the target partly for that reason "
                "and because round 4 images the open mouth. Shipped subjects; differences over the subjects with "
                "both rounds.",
                pd.DataFrame(rounds).T.round(3),
            ),
            Decision(
                "Subjects without a complete round-1 image are dropped",
                "Their next complete image comes from round 2 or 3, after the first oral reading had put the "
                "thermometer under the tongue, so they lack the image the prediction acts on. Left missing, the "
                "missing image would mark a group with a higher share of fever. Subjects of the file without the "
                "double-coded pair.",
                retakes,
            ),
            Decision(
                "IID over subjects; the measurement day is not held out",
                "154 days with 1-15 subjects (median 6). For each quantity, the share of its variance between the "
                "day means, the same share with shuffled days, the permutation p-value and the intraclass "
                "correlation. The day carries a small part of the target and more of the offset between the oral "
                "temperature and the face maximum, and the room readings identify it. Folds grouped by day score "
                "the same as random ones (curation comments).",
                days,
            ),
            Decision(
                "One measurement under two subject codes: both rows dropped",
                "The images of rounds 1-3 and the oral readings agree, while the date, the time, the ethnicity and "
                "the room readings differ, so neither code can be trusted with the measurement.",
                pair,
            ),
        ]
