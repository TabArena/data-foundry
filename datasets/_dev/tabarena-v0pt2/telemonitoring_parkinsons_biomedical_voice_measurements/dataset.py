"""Curated dataset definition for `telemonitoring_parkinsons_biomedical_voice_measurements` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping

THREE_MONTH_VISIT_DAY = 91
"""Day of the 3-month clinic assessment for a subject whose interpolated UPDRS shows no bend (median of the others)."""


def _three_month_day(days: np.ndarray, values: np.ndarray) -> float:
    """Day of the 3-month assessment: where a continuous two-piece linear fit of the daily UPDRS bends.

    The fit is a least-squares search over knots on a 0.25-day grid. When it is not at least 10 times better than a
    straight line, the subject shows no bend (its 3-month score lies on the line) and the protocol's day is used.
    """
    best_knot, best_sse = THREE_MONTH_VISIT_DAY, np.inf
    for knot in np.arange(days[1], days[-2] + 0.25, 0.25):
        design = np.column_stack([np.ones_like(days), days, np.clip(days - knot, 0, None)])
        coef, *_ = np.linalg.lstsq(design, values, rcond=None)
        sse = float(((design @ coef - values) ** 2).sum())
        if sse < best_sse:
            best_knot, best_sse = float(knot), sse
    line_sse = float(((np.polyval(np.polyfit(days, values, 1), days) - values) ** 2).sum())
    return best_knot if line_sse >= 10 * best_sse else float(THREE_MONTH_VISIT_DAY)


class TelemonitoringParkinsonsBiomedicalVoiceMeasurements(AbstractCuratedDataset):
    # Dataset
    unique_name = "telemonitoring_parkinsons_biomedical_voice_measurements"
    year = "2009"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5ZS3N"
    license = "CC BY 4.0"
    data_tags = ("Non-IID", "Grouped", "WrongDomain")
    download_description = """
        We get the 2009 data from the UCI repository.

        wget "https://archive.ics.uci.edu/static/public/189/parkinsons+telemonitoring.zip" -O parkinsons_telemonitoring.zip && unzip parkinsons_telemonitoring.zip parkinsons_updrs.data && rm parkinsons_telemonitoring.zip && mkdir -p local-data-warehouse/telemonitoring_parkinsons_biomedical_voice_measurements && mv parkinsons_updrs.data local-data-warehouse/telemonitoring_parkinsons_biomedical_voice_measurements/
    """
    bibtex = """
        @article{tsanas2010accurate,
          title={Accurate telemonitoring of {Parkinson's} disease progression by noninvasive speech tests},
          author={Tsanas, Athanasios and Little, Max A. and McSharry, Patrick E. and Ramig, Lorraine O.},
          journal={IEEE Transactions on Biomedical Engineering},
          volume={57},
          number={4},
          pages={884--893},
          year={2010},
          doi={10.1109/TBME.2009.2036000}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        We aim to simulate the task of predicting the UPDRS score of Parkinson's patients based on their voice measurements over time. This represents the task of only getting the voice measurements to judge the UPDRS. We assume we have no measurement of a patient to make this call. Thus, we have a grouped data task, where we have to holdout entire patients over time. We thus test for one patients multiple time points and repeated measurements at once.

        - We use total_UPDRS as target. The clinicians assessed UPDRS at baseline, 3 and 6 months; every weekly test day in between got a linearly interpolated score (UCI: "Clinician's total UPDRS score, linearly interpolated"; Tsanas et al. 2010: "piecewise linear interpolation was used"), so most labels are estimates that know the next assessment. We keep the three test days nearest real assessments, each with all its phonations (about six per day, the same label up to 0.005): the first test day (median day 7 after recruitment), the test day nearest the 3-month assessment and the last test day (median day 178). The 3-month assessment is where a subject's interpolated score bends: a continuous two-piece linear fit puts it at a median of day 91 (77 to 115), and the kept test day lies within 5 days before to 8 days after it. Subjects 14 and 30 show no bend (the fit is no better than a straight line), so we take the test day nearest day 91, the 3-month visit. Until 2026-10 we kept the last session before day 130 (median day 126, a label interpolated a median 35 days after the assessment), matched exact test times (so only part of a day's phonations) and took the first and last rows in file order, which are not the earliest and latest for 2 and 3 subjects.
        - We have several measurements per day for each patient when they were measured. We have some edge cases with negative test time as they got measured before the study started.
    """

    # Task
    target = "total_UPDRS"
    problem_type = "regression"
    grouping = Grouping(
        on="subject#",
        labels="per_sample",
        time_on="test_time",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a subject of a six-month trial of at-home voice recordings (42 subjects); its rows are the phonations of the kept test days, about six per day. UPDRS was assessed in the clinic at baseline, 3 and 6 months and interpolated for the weekly test days (Tsanas et al. 2010), so each phonation is one prediction of its test day's UPDRS, made from that phonation alone. Tsanas et al. split the phonations at random and track enrolled patients; holding out whole subjects is stricter and predicts for a subject not seen in training.
        """,
    )

    # Splits
    splits_comment = """
        We create a default group-label-per-sample split. We thus simulate the use case that someone fits a model and deploys it to predict the UPDRS score of a new patient based on their voice measurements for some time, ignoring the trajectory of the patient itself. We thus have to hold out entire patients and test for one patients multiple time points and repeated measurements at once.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "parkinsons_updrs.data")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(
            columns=[
                "motor_UPDRS",
            ]
        )
        # cast here: the groupby and the sort below run on the categorical subject ids
        df["subject#"] = df["subject#"].astype("category")

        def select_rows(x):
            # The clinicians assessed UPDRS at baseline, 3 and 6 months; the weekly test days in between got a linearly
            # interpolated score. Keep the three test days nearest the assessments: the first, the one nearest the
            # 3-month assessment and the last, each with all its phonations.
            x = x.sort_values("test_time", kind="stable")
            day = np.floor(x["test_time"])
            per_day = x.groupby(day)["total_UPDRS"].mean()
            days = per_day.index.to_numpy(dtype=float)
            middle = days[np.argmin(np.abs(days - _three_month_day(days, per_day.to_numpy())))]
            return x[day.isin([days[0], middle, days[-1]])]

        df = df.groupby("subject#", group_keys=False).apply(select_rows).reset_index(drop=True)
        df = (
            df.sample(frac=1, random_state=42)
            .sort_values(by=["subject#", "test_time"], kind="stable")
            .reset_index(drop=True)
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["sex", "subject#"])


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
