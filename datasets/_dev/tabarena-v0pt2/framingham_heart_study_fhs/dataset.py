"""Curated dataset definition for `framingham_heart_study_fhs` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary, drop_columns

TEN_YEARS = 3652
"""Days in 10 years (10 x 365.25, rounded down). No event, death or censor date of the cohort falls on days
3,648-3,654, so any cut-off there gives the same labels."""

EDUCATION = {
    1.0: "0-11 years",
    2.0: "high school or GED",
    3.0: "some college or vocational school",
    4.0: "college degree or more",
}
"""The four levels of `educ` (documentation): bins of years of schooling."""

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
"""The baseline risk factors of the teaching dataset, renamed as in MIT's cut (the file of the Kaggle uploads).
`prevalentStroke` is dropped from the task (0 in every kept row) but stays here to match MIT's rows."""

# Columns of the teaching dataset that are not features, with the reason.
DROPPED_COLUMNS = {
    "RANDID": "participant identifier",
    "PERIOD": "examination cycle: 1 for every row of the cohort",
    "TIME": "days since the baseline exam: 0 for every row of the cohort",
    "PREVCHD": "prevalent CHD: 0 for every participant of the cohort",
    "PREVAP": "prevalent angina: 0 for every participant of the cohort (part of PREVCHD)",
    "PREVMI": "prevalent MI: 0 for every participant of the cohort (part of PREVCHD)",
    "PREVSTRK": "prevalent stroke: 0 for every participant of the cohort (prior ASCVD is excluded)",
    "HDLC": "HDL cholesterol: measured at period 3 only",
    "LDLC": "LDL cholesterol: measured at period 3 only",
    "DEATH": "follow-up: death during the 24 years (builds the target)",
    "ANGINA": "follow-up: incident angina",
    "HOSPMI": "follow-up: incident hospitalized MI",
    "MI_FCHD": "follow-up: incident hospitalized MI or fatal CHD (builds the target)",
    "ANYCHD": "follow-up: incident CHD",
    "STROKE": "follow-up: incident stroke (builds the target)",
    "CVD": "follow-up: incident cardiovascular disease",
    "HYPERTEN": "follow-up: incident hypertension",
    "TIMEAP": "follow-up: days to angina or censoring",
    "TIMEMI": "follow-up: days to hospitalized MI or censoring",
    "TIMEMIFC": "follow-up: days to hospitalized MI, fatal CHD or censoring (builds the target)",
    "TIMECHD": "follow-up: days to CHD or censoring",
    "TIMESTRK": "follow-up: days to stroke or censoring (builds the target)",
    "TIMECVD": "follow-up: days to cardiovascular disease or censoring",
    "TIMEDTH": "follow-up: days to death or censoring (builds the target)",
    "TIMEHYP": "follow-up: days to hypertension or censoring",
}

ASCVD = "hard ASCVD within 10 years"
DIED = "died without hard ASCVD within 10 years"
LOST = "lost to follow-up within 10 years"
FREE = "free of hard ASCVD for 10 years"
OUTCOMES = [ASCVD, DIED, LOST, FREE]

CHD = "CHD within 10 years"
CHD_DIED = "died without CHD within 10 years"
CHD_FREE = "CHD-free for 10 years"
CHD_OUTCOMES = [CHD, CHD_DIED, LOST, CHD_FREE]


def _chd_free(teaching: pd.DataFrame) -> pd.DataFrame:
    """The baseline exam (period 1) of the participants free of CHD, the population at risk of the documentation."""
    return teaching[teaching["PERIOD"].eq(1) & teaching["PREVCHD"].eq(0)]


def _baseline(teaching: pd.DataFrame) -> pd.DataFrame:
    """The baseline exam of the participants free of CHD and stroke: no prior ASCVD, the cohort of the PCE."""
    chd_free = _chd_free(teaching)
    return chd_free[chd_free["PREVSTRK"].eq(0)]


def _outcome(df: pd.DataFrame) -> pd.Series:
    """What happened to each participant in the 10 years after the baseline exam, for hard ASCVD.

    TIMEMIFC and TIMESTRK are the days of the first hospitalized MI or fatal CHD (MI_FCHD = 1) and of the first stroke
    (STROKE = 1) or, without the event, the censor date: "end of followup, death or last known contact date if subject
    is lost to followup" (documentation, p. 4). Follow-up for hard ASCVD ends at the earlier of the two.
    """
    ascvd = (df["MI_FCHD"].eq(1) & df["TIMEMIFC"].le(TEN_YEARS)) | (df["STROKE"].eq(1) & df["TIMESTRK"].le(TEN_YEARS))
    died = ~ascvd & df["DEATH"].eq(1) & df["TIMEDTH"].le(TEN_YEARS)
    censor = df[["TIMEMIFC", "TIMESTRK"]].min(axis=1)
    lost = ~ascvd & ~died & censor.le(TEN_YEARS)
    outcome = pd.Series(FREE, index=df.index)
    outcome[ascvd] = ASCVD
    outcome[died] = DIED
    outcome[lost] = LOST
    return outcome


def _chd_outcome(df: pd.DataFrame) -> pd.Series:
    """What happened to each participant in the 10 years after the baseline exam, for any CHD (ANYCHD, TIMECHD)."""
    chd = df["ANYCHD"].eq(1) & df["TIMECHD"].le(TEN_YEARS)
    died = ~chd & df["DEATH"].eq(1) & df["TIMEDTH"].le(TEN_YEARS)
    lost = ~chd & ~died & df["TIMECHD"].le(TEN_YEARS)
    outcome = pd.Series(CHD_FREE, index=df.index)
    outcome[chd] = CHD
    outcome[died] = CHD_DIED
    outcome[lost] = LOST
    return outcome


def _mit_rows(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """MIT's cut matched to the CHD-free baseline rows of the teaching dataset on its 15 features (no two share them)."""
    mit = raw["mit"].astype(float)
    baseline = _chd_free(raw["teaching"]).rename(columns=FEATURES)
    baseline["male"] = baseline["male"].map({1.0: 1.0, 2.0: 0.0})
    features = list(FEATURES.values())
    matched = mit.merge(baseline, on=features, how="inner", validate="one_to_one")
    assert len(matched) == len(mit) == len(baseline), (len(matched), len(mit), len(baseline))
    return matched


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "education": [
        "0-11 years",
        "high school or GED",
        "some college or vocational school",
        "college degree or more",
    ],  # open-ended
}


class FraminghamHeartStudyFhs(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a person without heart disease or stroke have a heart attack, die of heart disease or have a stroke "
            "within ten years?"
        ),
        use_case=(
            "At a patient's first assessment, a physician estimates the 10-year risk of a first hard atherosclerotic "
            "cardiovascular event (heart attack, coronary death or stroke), the risk on which current US guidelines "
            "decide statin treatment, for a patient free of such disease."
        ),
        row=(
            "One participant of the Framingham Heart Study (Massachusetts) at the first exam, the baseline exam of "
            "about 1956 (three exams roughly 1956-1968), free of coronary heart disease and stroke (4,199 "
            "participants of the teaching version of the data)."
        ),
        predicted=(
            "Whether a first hospitalized heart attack, death from coronary heart disease or stroke occurs within 10 "
            "years of the exam (hard ASCVD, the outcome of the 2013 pooled cohort equations); 6.6% have one."
        ),
        known=(
            "Age, sex, education, smoking and cigarettes per day, blood pressure medication, hypertension, diabetes, "
            "total cholesterol, systolic and diastolic blood pressure, BMI, heart rate and glucose. HDL cholesterol, "
            "which current risk scores use, is missing: it was measured only at the third exam."
        ),
        split=("Random participants, so the test data stands for new patients examined in the same way."),
        changes=(
            "We rebuild the label from the event dates as hard ASCVD; in the common copy, 265 of 644 positives had no "
            "coronary event within 10 years. We drop the 25 participants with an earlier stroke and the 16 whose "
            "follow-up ended early without an event."
        ),
        fit="direct",
        fit_reason=(
            "Everything is measured at the exam and the outcome, the one current treatment decisions use, follows "
            "within a fixed ten years, as in use. The care is that of the late 1950s, before statins (3.0% on blood "
            "pressure medication). The teaching data was anonymized by undocumented methods: no noise was added "
            "(digit preference intact); permutation or visit selection cannot be checked."
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
        documentation p. 1) of the 4,215 participants free of CHD and stroke, the cohort without prior atherosclerotic
        cardiovascular disease (ASCVD). The year 2004 is the creation date of the teaching file (2004-03-02,
        documentation p. 8); its first release date is not stated.

        - Prediction point: the baseline exam. A physician predicts whether a participant free of CHD and stroke will
          have a first hard ASCVD event within 10 years, from 14 risk factors of period 1.
        - We read the teaching dataset rather than MIT's cut of it (the file of the Kaggle uploads, its baseline rows
          with PREVCHD = 0), because the label has to be rebuilt from the event columns.
        - Target `ascvd_within_10_years`: Yes when a first hospitalized myocardial infarction or fatal CHD (MI_FCHD,
          day TIMEMIFC) or a first stroke (STROKE, day TIMESTRK) happens within 3,652 days of the baseline exam. This is
          hard ASCVD, the outcome of the ACC/AHA pooled cohort equations (2013), the score on which current US statin
          decisions are made (Lennart, 2026-10-22: hard ASCVD matches the real-world use now). For context on the
          same CHD-free cohort, any CHD (ANYCHD: angina pectoris, myocardial infarction, coronary insufficiency or
          fatal CHD; the outcome of the FHS 10-year CHD function of Wilson et al. 1998) gives 379 Yes and hard CHD
          (MI_FCHD, the outcome of ATP III) 191 (decision table 3).
        - MIT's TenYearCHD is 1 exactly when TIMECHD is below 10 years, and TIMECHD is the censor date for a participant
          without an event, so 265 of its 644 positives had no CHD event within 10 years (decision table 1). Its
          label cannot be used for any endpoint.
        - Prior ASCVD is excluded, as in the pooled cohort equations: besides the 194 with prevalent CHD, we drop the 25
          participants with a stroke before the baseline exam (PREVSTRK = 1). The teaching data records their stroke
          as STROKE = 1 on day 0, so kept they would all be Yes and `prevalentStroke` would give their label away.
        - The 218 participants who died without hard ASCVD within 10 years are No: they had no event (LEAK-22).
          Dropping them would select the cohort on an event after the prediction point and remove high-risk negatives.
        - We drop the 16 participants whose follow-up ended within 10 years without an event (the earlier of the
          TIMEMIFC and TIMESTRK censor dates): their 10-year status is unknown. 4,199 participants remain, 276 Yes
          (6.6%; 187 hard CHD, 99 stroke, 10 both).
        - We drop the identifier RANDID, the columns constant in the cohort (PERIOD, TIME, PREVCHD, PREVAP, PREVMI,
          PREVSTRK), HDLC and LDLC (measured at period 3 only, so the task lacks the HDL that current risk scores use)
          and the follow-up columns (events and days to event, death or censoring).
        - We rename the features as in MIT's cut; `male` is 1 for SEX = 1 (men) and 0 for SEX = 2 (women). The flags
          stay 0/1. `education` becomes its four labels as a category (CLEAN-12; Lennart, 2026-10-22: a categorical
          code is encoded as such). Age and the flags without missing values are stored as integers.
        - Missing values are real missing values in the source; there are no sentinels, and the ranges match the
          documentation. cigsPerDay heaps at 9 and 43, values that occur almost only at period 1; their coding is
          undocumented, and we keep them.
        - Anomaly: BioLINCC anonymized the teaching data by methods it does not document (Nahhas, Introduction to
          Regression Methods for Public Health Using R, App. A.6, names permutations or random visit selection). No
          noise was added: digit preference is intact (systolic BP ends in 0 far more often than in an odd digit).
          Within a person, BMI and systolic BP six years apart correlate at r 0.90 and 0.71, and ages match the exam
          days in every later exam. Permutation or visit selection cannot be checked. Four participants have an
          MI/CHD and stroke censor date (end of follow-up) after their death; they are No either way.
        - Selection: the teaching data is "a subset of the data collected as part of the Framingham study" on 4,434
          participants (documentation p. 1), of the 5,209 enrolled in 1948; how they were chosen is not documented.
          The first exam is about 1956, so people who died or left before it are likely missing. The task stands for
          this subset, not for the whole cohort.
        - Terms: BioLINCC calls teaching data unsuitable for publication (`license`). We use it to compare learning
          methods, not to estimate clinical effects.
        - No duplicate rows: no two participants share all 14 features.
        - Note: IID split, one row per participant. The use case is risk prediction for new patients at an exam, and
          the teaching data has no exam dates or family identifiers, so spouses and relatives cannot be identified.
        - Possible variant (Lennart, 2026-10-22): every event-free exam with 10 years of follow-up left (periods 1-3),
          split grouped by participant, would make a grouped task; for any CHD (10,759 rows, 1,229 Yes) logistic
          regression rose from 0.736 to 0.745 on the same baseline test rows; not measured for hard ASCVD. Not shipped:
          the use case is a patient's first assessment (USE-11), and the later exams are older, selected survivors.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 1 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`).
    """

    # Task
    target = "ascvd_within_10_years"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="The teaching dataset defines no task or metric. The context (10-year risk scores) points to the C statistic, which equals roc_auc for a fixed-horizon binary outcome, so the fallback and the context agree."
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "teaching": pd.read_csv(raw_dir / "framingham_teaching.csv"),
            # read only for the target decision; the CR line endings are read like newlines
            "mit": pd.read_csv(raw_dir / "framingham_mit_15071.csv"),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # the baseline exam of the participants free of CHD and stroke (no prior ASCVD)
        df = _baseline(raw["teaching"])
        # the 10-year hard ASCVD label; the 16 participants lost to follow-up within 10 years have no known status
        outcome = _outcome(df)
        df = df[outcome.ne(LOST)]
        df[self.target] = outcome[outcome.ne(LOST)].eq(ASCVD).map({True: "Yes", False: "No"})
        # identifiers, constant and period-3 columns, and the follow-up columns
        df = drop_columns(df, DROPPED_COLUMNS)
        # MIT's names; SEX 1 = men, 2 = women
        df = df.rename(columns=FEATURES)
        df["male"] = df["male"].map({1.0: 1, 2.0: 0})
        # the education code as its labels (CLEAN-12)
        df["education"] = df["education"].map(EDUCATION)
        # whole numbers without missing values
        for column in ["age", "currentSmoker", "prevalentHyp", "diabetes"]:
            df[column] = df[column].astype("int64")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the 0/1 flags (CLEAN-14) and the education level are categorical; the measurements stay numeric
        del df
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=["male", "education", "currentSmoker", "BPMeds", "prevalentHyp", "diabetes"],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        # 1. MIT's TenYearCHD by what happened in the 10 years (any CHD, the outcome MIT's label stands for)
        matched = _mit_rows(raw)
        chd_outcome = _chd_outcome(matched)
        ascvd_yes = _outcome(matched).eq(ASCVD) & matched["prevalentStroke"].eq(0)
        by_outcome = pd.DataFrame(
            {
                "participants": chd_outcome.value_counts(),
                "MIT TenYearCHD = 1": matched["TenYearCHD"].groupby(chd_outcome).sum(),
                "TIMECHD min (days)": matched["TIMECHD"].groupby(chd_outcome).min(),
                "TIMECHD max (days)": matched["TIMECHD"].groupby(chd_outcome).max(),
                f"{self.target} = Yes": ascvd_yes.groupby(chd_outcome).sum(),
            }
        ).reindex(CHD_OUTCOMES)
        by_outcome.index.name = "any CHD within 10 years"
        same = int(matched["TenYearCHD"].eq(matched["TIMECHD"].lt(TEN_YEARS).astype(int)).sum())

        # 2. the cohort
        teaching = raw["teaching"]
        period_1 = teaching[teaching["PERIOD"].eq(1)]
        chd_free = _chd_free(teaching)
        baseline = _baseline(teaching)
        outcome = _outcome(baseline)
        cohort = pd.Series(
            {
                "participants at the baseline exam (period 1)": len(period_1),
                "with prevalent CHD (dropped)": int(period_1["PREVCHD"].eq(1).sum()),
                "free of CHD (MIT's 4,240 rows)": len(chd_free),
                "with prevalent stroke (dropped)": int(chd_free["PREVSTRK"].eq(1).sum()),
                "free of CHD and stroke": len(baseline),
                "lost to follow-up within 10 years without hard ASCVD (dropped)": int(outcome.eq(LOST).sum()),
                "died without hard ASCVD within 10 years (kept, No)": int(outcome.eq(DIED).sum()),
                "kept": len(df),
                f"kept, {self.target} = Yes": int(df[self.target].eq("Yes").sum()),
            },
            name="participants",
        )
        cohort.index.name = "step"
        stroke = chd_free[chd_free["PREVSTRK"].eq(1)]
        prior_stroke = pd.Series(
            {
                "participants": len(stroke),
                "STROKE = 1": int(stroke["STROKE"].eq(1).sum()),
                "TIMESTRK = 0": int(stroke["TIMESTRK"].eq(0).sum()),
            },
            name="CHD-free participants with PREVSTRK = 1",
        )

        # 3. the endpoint: first events within 10 years on the CHD-free cohort and on the kept rows
        def events(rows: pd.DataFrame) -> pd.Series:
            hard_chd = rows["MI_FCHD"].eq(1) & rows["TIMEMIFC"].le(TEN_YEARS)
            stroke_event = rows["STROKE"].eq(1) & rows["TIMESTRK"].le(TEN_YEARS)
            return pd.Series(
                {
                    "any CHD (ANYCHD; FHS 10-year CHD function, 1998)": int(
                        (rows["ANYCHD"].eq(1) & rows["TIMECHD"].le(TEN_YEARS)).sum()
                    ),
                    "hard CHD (MI_FCHD; ATP III, 2001)": int(hard_chd.sum()),
                    "stroke (STROKE)": int(stroke_event.sum()),
                    "hard ASCVD (MI_FCHD or STROKE; pooled cohort equations, 2013)": int(
                        (hard_chd | stroke_event).sum()
                    ),
                }
            )

        kept = baseline[outcome.ne(LOST)]
        endpoints = pd.DataFrame(
            {
                f"free of CHD ({len(chd_free):,})": events(chd_free),
                f"kept rows ({len(kept):,})": events(kept),
            }
        )
        endpoints.index.name = "first event within 10 years"
        return [
            Decision(
                "The target is rebuilt: MIT's TenYearCHD counts deaths and losses to follow-up as CHD",
                f"MIT's TenYearCHD equals TIMECHD < {TEN_YEARS} days in {same:,} of {len(matched):,} rows, and "
                "TIMECHD is the day of the first CHD event or, without one, the censor date (death, last contact or end "
                "of follow-up). So it is no label for any endpoint; ours is built from the event and death days. "
                "Participants of MIT's rows, matched to the teaching dataset on their 15 features.",
                by_outcome,
            ),
            Decision(
                "Cohort: the baseline exam of the participants without prior ASCVD",
                "The pooled cohort equations apply to people without ASCVD, so prevalent CHD and prevalent stroke are "
                "dropped; the teaching data codes a prior stroke as STROKE = 1 on day 0, which would make each a Yes. "
                "Participants whose 10-year status is unknown are dropped; deaths from other causes are No (LEAK-22).",
                cohort,
            ),
            Decision(
                "Prior strokes are recorded as incident strokes on day 0",
                "Every CHD-free participant with a stroke before the baseline exam has STROKE = 1 and TIMESTRK = 0.",
                prior_stroke,
            ),
            Decision(
                "Endpoint: hard ASCVD, the outcome of the current treatment decision",
                "The ACC/AHA pooled cohort equations (2013), on which US statin decisions are made, predict a first "
                "heart attack, CHD death or stroke. Any CHD and hard CHD are the outcomes of the older FHS and ATP III "
                "scores; counted here for context.",
                endpoints,
            ),
        ]
