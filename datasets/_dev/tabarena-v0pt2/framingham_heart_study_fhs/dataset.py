"""Curated dataset definition for `framingham_heart_study_fhs` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

TEN_YEARS = 3652
"""Days in 10 years (10 x 365.25, rounded down). No event, death or censor date of the cohort falls on days
3,648-3,654, so any cut-off there gives the same labels."""

FEATURES = {
    "SEX": "male",
    "AGE": "age",
    "educ": "education",
    "CURSMOKE": "currentSmoker",
    "CIGPDAY": "cigsPerDay",
    "BPMEDS": "BPMeds",
    "PREVSTRK": "prevalentStroke",
    "PREVHYP": "prevalentHyp",
    "DIABETES": "diabetes",
    "TOTCHOL": "totChol",
    "SYSBP": "sysBP",
    "DIABP": "diaBP",
    "BMI": "BMI",
    "HEARTRTE": "heartRate",
    "GLUCOSE": "glucose",
}
"""The baseline risk factors of the teaching dataset, renamed as in MIT's cut (the file of the Kaggle uploads)."""

# Columns of the teaching dataset that are not features, with the reason.
DROPPED_COLUMNS = {
    "RANDID": "participant identifier",
    "PERIOD": "examination cycle: 1 for every row of the cohort",
    "TIME": "days since the baseline exam: 0 for every row of the cohort",
    "PREVCHD": "prevalent CHD: 0 for every participant of the cohort",
    "PREVAP": "prevalent angina: 0 for every participant of the cohort (part of PREVCHD)",
    "PREVMI": "prevalent MI: 0 for every participant of the cohort (part of PREVCHD)",
    "HDLC": "HDL cholesterol: measured at period 3 only",
    "LDLC": "LDL cholesterol: measured at period 3 only",
    "DEATH": "follow-up: death during the 24 years (builds the target)",
    "ANGINA": "follow-up: incident angina",
    "HOSPMI": "follow-up: incident hospitalized MI",
    "MI_FCHD": "follow-up: incident hospitalized MI or fatal CHD",
    "ANYCHD": "follow-up: incident CHD (builds the target)",
    "STROKE": "follow-up: incident stroke",
    "CVD": "follow-up: incident cardiovascular disease",
    "HYPERTEN": "follow-up: incident hypertension",
    "TIMEAP": "follow-up: days to angina or censoring",
    "TIMEMI": "follow-up: days to hospitalized MI or censoring",
    "TIMEMIFC": "follow-up: days to hospitalized MI, fatal CHD or censoring",
    "TIMECHD": "follow-up: days to CHD or censoring (builds the target)",
    "TIMESTRK": "follow-up: days to stroke or censoring",
    "TIMECVD": "follow-up: days to cardiovascular disease or censoring",
    "TIMEDTH": "follow-up: days to death or censoring (builds the target)",
    "TIMEHYP": "follow-up: days to hypertension or censoring",
}

CHD = "CHD within 10 years"
DIED = "died without CHD within 10 years"
LOST = "lost to follow-up within 10 years"
FREE = "CHD-free for 10 years"
OUTCOMES = [CHD, DIED, LOST, FREE]


def _baseline(teaching: pd.DataFrame) -> pd.DataFrame:
    """The baseline exam (period 1) of the participants free of CHD, the population at risk of the documentation."""
    return teaching[teaching["PERIOD"].eq(1) & teaching["PREVCHD"].eq(0)]


def _outcome(df: pd.DataFrame) -> pd.Series:
    """What happened to each participant in the 10 years after the baseline exam.

    TIMECHD is the day of the first CHD event (ANYCHD = 1) or, without an event, the censor date: "end of followup,
    death or last known contact date if subject is lost to followup" (documentation, p. 4).
    """
    chd = df["ANYCHD"].eq(1) & df["TIMECHD"].le(TEN_YEARS)
    died = ~chd & df["DEATH"].eq(1) & df["TIMEDTH"].le(TEN_YEARS)
    lost = ~chd & ~died & df["TIMECHD"].le(TEN_YEARS)
    outcome = pd.Series(FREE, index=df.index)
    outcome[chd] = CHD
    outcome[died] = DIED
    outcome[lost] = LOST
    return outcome


def _mit_rows(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """MIT's cut matched to the baseline rows of the teaching dataset on its 15 features (no two rows share them)."""
    mit = raw["mit"].astype(float)
    baseline = _baseline(raw["teaching"]).rename(columns=FEATURES)
    baseline["male"] = baseline["male"].map({1.0: 1.0, 2.0: 0.0})
    features = list(FEATURES.values())
    matched = mit.merge(baseline, on=features, how="inner", validate="one_to_one")
    assert len(matched) == len(mit) == len(baseline), (len(matched), len(mit), len(baseline))
    return matched


class FraminghamHeartStudyFhs(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Will a person without coronary heart disease have a first coronary event within ten years?"),
        use_case=(
            "At a patient's first assessment, a physician estimates the 10-year risk of a first coronary heart "
            "disease event for a patient free of it, to decide on prevention, for example blood pressure or "
            "cholesterol treatment."
        ),
        row=(
            "One participant of the Framingham Heart Study (Massachusetts) at the first exam, the baseline exam of "
            "about 1956 (three exams roughly 1956-1968), free of coronary heart disease (4,224 participants of the "
            "teaching version of the data)."
        ),
        predicted=(
            "Whether a first coronary heart disease event (angina, heart attack, coronary insufficiency or death from"
            " it) occurs within 10 years of the exam; 9.0% have one."
        ),
        known=(
            "Age, sex, education, smoking and cigarettes per day, blood pressure medication, earlier stroke, "
            "hypertension, diabetes, total cholesterol, systolic and diastolic blood pressure, BMI, heart rate and "
            "glucose. HDL cholesterol, which current risk scores use, is missing: it was measured only at the third "
            "exam."
        ),
        split=("Random participants, so the test data stands for new patients examined in the same way."),
        changes=(
            "We rebuild the label from the event dates; in the common copy, 265 of 644 positives had no coronary "
            "event within 10 years. We drop the 16 participants whose follow-up ended early without an event."
        ),
        fit="direct",
        fit_reason=(
            "Everything is measured at the exam and the outcome follows within a fixed ten years, as in use. The "
            "care is that of the late 1950s, before statins (3.0% on blood pressure medication). The teaching data "
            "was anonymized by undocumented methods: no noise was added (digit preference intact); permutation or "
            "visit selection cannot be checked."
        ),
    )

    # Dataset
    unique_name = "framingham_heart_study_fhs"
    year = "2004"
    domain = "medical & healthcare"
    source = "GOV Website"
    source_url = "https://biolincc.nhlbi.nih.gov/teaching/"
    license = (
        "NHLBI BioLINCC teaching dataset, free on request; BioLINCC: 'teaching datasets are completely unsuitable "
        "for publication purposes since specific statistical measures were used to create anonymous versions'. "
        "Redistributed 'with permission from the National Heart, Lung, and Blood Institute' in the R package "
        "riskCommunicator (GPL-3)"
    )
    download_description = r"""
        The Framingham Heart Study teaching dataset of NHLBI BioLINCC (https://biolincc.nhlbi.nih.gov/teaching/) is sent
        on request. The R package riskCommunicator redistributes it with NHLBI's permission as its data set
        `framingham` (11,627 rows x 39 columns); data/framingham.rda is the same file in versions 0.1.0, 1.0.0 and 1.0.1
        (sha256 8fdd578ae462f823bf737f451d8a98227c35cb2dbd6390cf2df3b3fa97050f56). It matches every count and mean of
        the BioLINCC documentation we compared (period-1 participants, prevalent CHD, events and deaths by sex). We
        export it to CSV with pyreadr; in R, write.csv(framingham, "framingham_teaching.csv", row.names = FALSE) gives
        the same values. The Kaggle upload shreyjain601/framingham-heart-study ("Framingham Dataset.csv") is reported
        to hold the same 453,453 values in the same order; not re-checked.

        mkdir -p local-data-warehouse/framingham_heart_study_fhs && cd local-data-warehouse/framingham_heart_study_fhs
        wget https://cran.r-project.org/src/contrib/Archive/riskCommunicator/riskCommunicator_1.0.0.tar.gz
        tar xzf riskCommunicator_1.0.0.tar.gz riskCommunicator/data/framingham.rda
        uvx --from pyreadr==0.5.7 --with pandas==3.0.6 python -c "import pyreadr; pyreadr.read_r('riskCommunicator/data/framingham.rda')['framingham'].to_csv('framingham_teaching.csv', index=False)"
        rm -r riskCommunicator riskCommunicator_1.0.0.tar.gz
        sha256sum framingham_teaching.csv
        # 0ab97721ec4757fe107bf6ce7f9ea51b8dd9999c57f461dda73e345000f7ed62

        MIT's cut, the file of the Kaggle uploads in the curation record, is read only for the evidence of the target
        decision (MIT OpenCourseWare, 15.071 The Analytics Edge, Spring 2017; byte-identical to Kaggle
        aasheesh200/framingham-heart-study-dataset).

        wget -O framingham_mit_15071.csv https://ocw.mit.edu/courses/15-071-the-analytics-edge-spring-2017/5d689a024551e672313f7fd7eb1bee8d_framingham.csv
        sha256sum framingham_mit_15071.csv
        # 2c0e57dc0361b420becf1facec0a054af06c420eae0ae2faf0fdc8591fadb018
    """
    bibtex = r"""
        @misc{nhlbi2004framingham,
          author = {{National Heart, Lung, and Blood Institute}},
          title = {Framingham Heart Study Longitudinal Data Documentation (Teaching Dataset)},
          year = {2004},
          howpublished = {\url{https://biolincc.nhlbi.nih.gov/teaching/}},
          note = {BioLINCC teaching dataset; documentation version 2021a,
            \url{https://biolincc.nhlbi.nih.gov/media/teachingstudies/FHS_Teaching_Longitudinal_Data_Documentation_2021a.pdf}}
        }
        @manual{grembi2022riskcommunicator,
          author = {Grembi, Jessica},
          title = {{riskCommunicator}: G-Computation to Estimate Interpretable Epidemiological Effects},
          year = {2022},
          note = {R package version 1.0.0; data set framingham},
          doi = {10.32614/CRAN.package.riskCommunicator}
        }
        @misc{bertsimas2017analyticsedge,
          author = {Bertsimas, Dimitris},
          title = {15.071 The Analytics Edge, Spring 2017},
          year = {2017},
          howpublished = {Massachusetts Institute of Technology: MIT OpenCourseWare,
            \url{https://ocw.mit.edu/courses/15-071-the-analytics-edge-spring-2017/}},
          note = {Unit 3, The Framingham Heart Study: the cut of the Kaggle uploads}
        }
    """
    curation_comments = """
        We start with the Framingham Heart Study teaching dataset of NHLBI BioLINCC, as redistributed in the R package
        riskCommunicator. We keep the baseline exam (period 1, about 1956; the three exams ran roughly 1956-1968,
        documentation p. 1) of the 4,240 participants free of CHD, the population at risk of the documentation (p. 5).
        The year 2004 is the creation date of the teaching file (2004-03-02, documentation p. 8); its first release
        date is not stated.

        - Prediction point: the baseline exam. A physician predicts whether a participant free of coronary heart disease
          will have a first CHD event within 10 years, from the 15 risk factors of period 1.
        - We read the teaching dataset rather than MIT's cut of it (the file of the Kaggle uploads, its baseline rows
          with PREVCHD = 0), because the label has to be rebuilt from the event columns.
        - Target `chd_within_10_years`: Yes when the first CHD event (ANYCHD: angina pectoris, myocardial infarction,
          coronary insufficiency or fatal CHD) happens within 3,652 days of the baseline exam. MIT's TenYearCHD is 1
          exactly when TIMECHD is below 10 years, and TIMECHD is the censor date for a participant without an event,
          so 265 of its 644 positives had no CHD event within 10 years (decision table). ANYCHD is the outcome of
          the FHS 10-year CHD risk function
          (https://www.framinghamheartstudy.org/fhs-risk-functions/coronary-heart-disease-10-year-risk/, based on
          Wilson et al. 1998: "Outcome Coronary Heart Disease", "Hard CHD events exclude angina pectoris"). Hard CHD
          (MI_FCHD), the outcome of the FHS hard-CHD function, would give 191 Yes.
        - The 251 participants who died without CHD within 10 years are No: they had no CHD event. Dropping them would
          select the cohort on an event after the prediction point and remove high-risk negatives.
        - We drop the 16 participants whose CHD follow-up ended within 10 years without an event: their 10-year status
          is unknown. 4,224 participants remain, 379 Yes (9.0%).
        - We drop the identifier RANDID, the columns constant in the cohort (PERIOD, TIME, PREVCHD, PREVAP, PREVMI),
          HDLC and LDLC (measured at period 3 only, so the task lacks the HDL that current risk scores use) and the
          follow-up columns (events and days to event, death or censoring).
        - We rename the features as in MIT's cut; `male` is 1 for SEX = 1 (men) and 0 for SEX = 2 (women). The flags
          stay 0/1 and education stays numeric, as it is ordered. Age and the flags without missing values are stored
          as integers.
        - Missing values are real missing values in the source; there are no sentinels, and the ranges match the
          documentation. cigsPerDay heaps at 9 and 43, values that occur almost only at period 1; their coding is
          undocumented, and we keep them.
        - Anomaly: BioLINCC anonymized the teaching data by methods it does not document (Nahhas, Introduction to
          Regression Methods for Public Health Using R, App. A.6, names permutations or random visit selection). No
          noise was added: digit preference is intact (systolic BP ends in 0 far more often than in an odd digit).
          Within a person, BMI and systolic BP six years apart correlate at r 0.90 and 0.71, and ages match the exam
          days in every later exam. Permutation or visit selection cannot be checked. Three participants have a CHD
          censor date after their death; they are No either way.
        - Selection: the teaching data is "a subset of the data collected as part of the Framingham study" on 4,434
          participants (documentation p. 1), of the 5,209 enrolled in 1948; how they were chosen is not documented.
          The first exam is about 1956, so people who died or left before it are likely missing. The task stands for
          this subset, not for the whole cohort.
        - Terms: BioLINCC calls teaching data unsuitable for publication (`license`). We use it to compare learning
          methods, not to estimate clinical effects.
        - No duplicate rows: no two participants share all 15 features.
        - Note: IID split, one row per participant. The use case is risk prediction for new patients at an exam, and
          the teaching data has no exam dates or family identifiers, so spouses and relatives cannot be identified.
    """

    # Task
    target = "chd_within_10_years"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "teaching": pd.read_csv(raw_dir / "framingham_teaching.csv"),
            # read only for the target decision; the CR line endings are read like newlines
            "mit": pd.read_csv(raw_dir / "framingham_mit_15071.csv"),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # the baseline exam of the participants free of CHD
        df = _baseline(raw["teaching"])
        # the 10-year CHD label; the 16 participants lost to follow-up within 10 years have no known status
        outcome = _outcome(df)
        df = df[outcome.ne(LOST)]
        df[self.target] = outcome[outcome.ne(LOST)].eq(CHD).map({True: "Yes", False: "No"})
        # identifiers, constant and period-3 columns, and the follow-up columns
        df = drop_columns(df, DROPPED_COLUMNS)
        # MIT's names; SEX 1 = men, 2 = women
        df = df.rename(columns=FEATURES)
        df["male"] = df["male"].map({1.0: 1, 2.0: 0})
        # whole numbers without missing values
        for column in ["age", "currentSmoker", "prevalentStroke", "prevalentHyp", "diabetes"]:
            df[column] = df[column].astype("int64")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the 0/1 flags are categorical (CLEAN-14); the ordered education level and the measurements stay numeric
        del df
        return FeatureTypes(
            categorical=["male", "currentSmoker", "BPMeds", "prevalentStroke", "prevalentHyp", "diabetes"],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        # 1. MIT's TenYearCHD by what happened in the 10 years
        matched = _mit_rows(raw)
        outcome = _outcome(matched)
        by_outcome = pd.DataFrame(
            {
                "participants": outcome.value_counts(),
                "MIT TenYearCHD = 1": matched["TenYearCHD"].groupby(outcome).sum(),
                "TIMECHD min (days)": matched["TIMECHD"].groupby(outcome).min(),
                "TIMECHD max (days)": matched["TIMECHD"].groupby(outcome).max(),
                "chd_within_10_years": pd.Series({CHD: "Yes", DIED: "No", LOST: "dropped", FREE: "No"}),
            }
        ).reindex(OUTCOMES)
        by_outcome.index.name = "outcome within 10 years"
        same = int(matched["TenYearCHD"].eq(matched["TIMECHD"].lt(TEN_YEARS).astype(int)).sum())

        # 2. the cohort
        teaching = raw["teaching"]
        period_1 = teaching[teaching["PERIOD"].eq(1)]
        cohort = pd.Series(
            {
                "participants at the baseline exam (period 1)": len(period_1),
                "with prevalent CHD (dropped)": int(period_1["PREVCHD"].eq(1).sum()),
                "free of CHD (MIT's 4,240 rows)": len(_baseline(teaching)),
                "lost to follow-up within 10 years without CHD (dropped)": int(outcome.eq(LOST).sum()),
                "kept": len(df),
                "kept, chd_within_10_years = Yes": int(df[self.target].eq("Yes").sum()),
            },
            name="participants",
        )
        cohort.index.name = "step"
        return [
            Decision(
                "The target is rebuilt: MIT's TenYearCHD counts deaths and losses to follow-up as CHD",
                f"MIT's TenYearCHD equals TIMECHD < {TEN_YEARS} days in {same:,} of {len(matched):,} rows, and "
                "TIMECHD is the day of the first CHD event or, without one, the censor date (death, last contact or end "
                "of follow-up). Our label is a first CHD event (ANYCHD = 1) within 10 years. Participants of MIT's rows, "
                "matched to the teaching dataset on their 15 features.",
                by_outcome,
            ),
            Decision(
                "Cohort: the baseline exam of the participants free of CHD",
                "The population at risk of the documentation (period 1, PREVCHD = 0), without the participants whose "
                "10-year status is unknown.",
                cohort,
            ),
        ]
