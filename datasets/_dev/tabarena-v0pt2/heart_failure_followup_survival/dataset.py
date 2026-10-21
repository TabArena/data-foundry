"""Curated dataset definition for `heart_failure_followup_survival` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

HORIZON = 60  # days of follow-up; a death on day 60 or earlier counts
# Values the source filled in where a lab value was missing: the column mean of CPK and platelets, and for serum
# creatinine the mean of the patient's own outcome group (Ahmad et al. 2017, Table 1: 1.18 survivors, 1.83 deaths)
FILLED = {"creatinine_phosphokinase": 582.0, "platelets": 263358.03, "serum_creatinine": (1.18, 1.83)}


def _filled(raw: pd.DataFrame) -> dict[str, pd.Series]:
    """Per column, the rows whose value was filled in by the source."""
    return {col: raw[col].round(2).isin(np.atleast_1d(value)) for col, value in FILLED.items()}


def _cohort(raw: pd.DataFrame) -> pd.DataFrame:
    """Per patient: death within the horizon, and follow-up long enough to know the patient was alive at its end."""
    event = raw["DEATH_EVENT"].eq(1) & raw["time"].le(HORIZON)
    followed = raw["time"].ge(HORIZON) & ~event
    return pd.DataFrame({"event": event, "followed": followed})


class HeartFailureFollowupSurvival(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a patient with heart failure die within 60 days?",
        use_case=(
            "For example, a cardiologist estimates a heart-failure patient's risk of dying in the next two months "
            "from routine findings and blood tests, to decide on closer follow-up or treatment."
        ),
        row=(
            "One patient with heart failure, aged 40 or older, at the Faisalabad Institute of Cardiology or the "
            "Allied Hospital in Faisalabad, Pakistan, April-December 2015 (291 of the 299 patients)."
        ),
        predicted="Whether the patient died within 60 days of the start of follow-up: 54 of 291 did (19%).",
        known=(
            "Age, sex, smoking, anaemia, diabetes, high blood pressure, the heart's ejection fraction, and blood "
            "values (creatinine phosphokinase, platelets, serum creatinine, serum sodium). The first three are missing "
            "where the source filled in a mean."
        ),
        split=("Random patients, so the test data stands for new patients of the same hospitals and year."),
        changes=(
            "The source is a survival study with a follow-up of 4 to 285 days that differs by patient. We turn it "
            "into a 60-day outcome: we drop the 8 survivors followed less than 60 days, and the follow-up time and "
            "status. We set 91 lab values that the source filled in back to missing; the creatinine ones had been "
            "filled with the mean of the patient's own outcome group."
        ),
        fit="approximate",
        fit_reason=(
            "The outcome, a fixed horizon and the findings match the decision, but heart-failure mortality is usually "
            "judged at 30 days or 1 year; here 30 days leaves 35 deaths, and 90 days would drop 45 survivors. Where "
            "follow-up starts and when the measurements were taken is not stated."
        ),
    )

    # Dataset
    unique_name = "heart_failure_followup_survival"
    year = "2017"
    domain = "medical & healthcare"
    source = "Other"  # S1 Data of Ahmad et al. 2017 (PLoS ONE); UCI 519 is the 2020 re-upload
    source_url = "https://doi.org/10.1371/journal.pone.0181001"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/519/heart+failure+clinical+records.zip && unzip heart+failure+clinical+records.zip && rm heart+failure+clinical+records.zip && mkdir -p local-data-warehouse/heart_failure_followup_survival && mv heart_failure_clinical_records_dataset.csv local-data-warehouse/heart_failure_followup_survival/
    """
    bibtex = """
        @article{ahmad2017survival,
          title={Survival analysis of heart failure patients: A case study},
          author={Ahmad, Tanvir and Munir, Assia and Bhatti, Sajjad Haider and Aftab, Muhammad and Raza, Muhammad Ali},
          journal={PLOS ONE},
          volume={12},
          number={7},
          pages={e0181001},
          year={2017},
          publisher={Public Library of Science},
          doi={10.1371/journal.pone.0181001}
        }
    """
    curation_comments = """
        We start with the UCI copy (519) of the S1 data of Ahmad et al. 2017 (PLoS ONE 12:e0181001); the two files hold the same rows. UCI names Chicco & Jurman 2020 (BMC Med Inform Decis Mak 20:16) as its introductory paper, a later re-analysis.

        - The source is a survival study: `time` is the follow-up in days (4-285), ending at death or censoring, and DEATH_EVENT says which. The label is death within 60 days (day 60 or earlier) against being alive at day 60. Until 2026-10-21 the label was death at any time during follow-up, so a survivor followed 12 days counted the same as one followed 285 days; a Kaplan-Meier estimate puts about 31 deaths within 285 days among those 203 survivors.
        - We drop the 8 survivors followed less than 60 days, whose 60-day status is unknown. If follow-up ended on one date for all (the censored times fit mid-January 2016), these are patients admitted late, and the late admissions who died early stay in; a Kaplan-Meier estimate puts that at about 1 death.
        - 60 days keeps all but 8 patients. 30 days, the usual short-term horizon in heart failure, leaves 35 deaths; 90 days would drop 45 survivors.
        - We drop `time` and DEATH_EVENT, which define the label.
        - The source filled in missing lab values without saying so (neither Ahmad et al. 2017 nor Chicco & Jurman 2020 mentions missing data). We set them back to missing: creatinine phosphokinase 582 (the column mean, 47 rows), platelets 263358.03 (the column mean, 25 rows), and serum creatinine 1.18 (11 rows, all survivors) and 1.83 (8 rows, all deaths). The creatinine values are the survivor and death means in Ahmad et al. Table 1, so they were filled from the outcome; apart from one 0.75 they are the only creatinine values with two decimals.
        - Anaemia among deaths: 46 in the file, 54 in Ahmad et al. Table 1; we keep the file's values.
        - We keep the other features as they are. The study that introduced the dataset also curated a subset of features. We leave it to the pipeline to select the relevant features for the task.
    """

    # Task
    target = "death_within_60_days"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "heart_failure_clinical_records_dataset.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # filled-in lab values back to missing; the creatinine ones were filled from the outcome
        for col, filled in _filled(df).items():
            df[col] = df[col].astype(float).mask(filled)
        cohort = _cohort(df)
        # survivors followed less than 60 days have no 60-day status
        keep = cohort["event"] | cohort["followed"]
        df = df.loc[keep]
        df["death_within_60_days"] = cohort.loc[keep, "event"].astype(int)
        # follow-up time and status define the label
        df = drop_columns(df, ["time", "DEATH_EVENT"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "anaemia",
                "diabetes",
                "high_blood_pressure",
                "sex",
                "smoking",
            ],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        cohort = _cohort(raw)
        status = raw["DEATH_EVENT"].map({1: "died", 0: "censored"})
        outcome = pd.Series("survivor followed < 60 days (dropped)", index=raw.index)
        outcome.loc[cohort["followed"]] = "alive at day 60"
        outcome.loc[cohort["event"]] = "died within 60 days"
        horizon = pd.crosstab(outcome.rename("60-day label"), status.rename("source status"), margins=True)
        filled = pd.DataFrame(
            [
                {
                    "column": col,
                    "filled value": FILLED[col],
                    "rows": int(mask.sum()),
                    "died (source)": int(raw.loc[mask, "DEATH_EVENT"].sum()),
                    "censored (source)": int((raw.loc[mask, "DEATH_EVENT"] == 0).sum()),
                }
                for col, mask in _filled(raw).items()
            ]
        )
        return [
            Decision(
                title="Death within 60 days, not death at any time during follow-up",
                why=(
                    "Follow-up runs 4 to 285 days and differs by patient, so 'survived' often meant 'not followed "
                    "long enough'. A fixed horizon gives every kept patient a known label."
                ),
                evidence=horizon,
            ),
            Decision(
                title="Filled-in lab values set back to missing",
                why=(
                    "The source filled missing values with a mean without saying so; for serum creatinine it used the "
                    "mean of the patient's own outcome group (1.18 survivors, 1.83 deaths), which leaks the label."
                ),
                evidence=filled,
            ),
        ]
