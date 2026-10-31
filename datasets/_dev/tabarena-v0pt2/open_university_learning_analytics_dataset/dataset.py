"""Curated dataset definition for `open_university_learning_analytics_dataset` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    SplitPlan,
    TaskSummary,
    drop_columns,
)

PREDICTION_DAY = 60
"""The day of the module-presentation (0 = its official start) at whose start the model predicts."""

MARKING_DAYS = 14
"""Days after the later of cut-off and submission until a TMA's score is known (assumed from the OU's ten working
days; the data holds no return date)."""

KEY = ["code_module", "code_presentation", "id_student"]
"""One registration: a student on one module-presentation (the source's own key)."""

CATEGORICAL = [
    "module_presentation",
    "code_module",
    "presentation_start",
    "gender",
    "region",
    "highest_education",
    "imd_band",
    "age_band",
    "disability",
]


def _assessment_features(raw: dict[str, pd.DataFrame], day: int) -> tuple[pd.DataFrame, pd.Series]:
    """Per registration: the TMAs and CMAs due before `day`, the submissions made before it, the scores known on it.

    Returns the per-registration features and, per module-presentation, the number of assessments due before `day`.
    """
    assessments = raw["assessments"]
    assessments = assessments[assessments["assessment_type"] != "Exam"]
    results = raw["student_assessment"].merge(assessments, on="id_assessment", how="inner", validate="many_to_one")
    results["days_early"] = results["date"] - results["date_submitted"]

    due = assessments[assessments["date"] < day].groupby(["code_module", "code_presentation"]).size()
    submitted = results[(results["is_banked"] == 0) & (results["date"] < day) & (results["date_submitted"] < day)]
    # a CMA is marked by computer when submitted; a TMA is returned within ten working days of its cut-off (or of a
    # late submission); a banked result comes from an earlier presentation and is known from the start
    marked_on = np.where(
        results["assessment_type"] == "TMA",
        np.maximum(results["date"], results["date_submitted"]) + MARKING_DAYS,
        results["date_submitted"],
    )
    # a TMA of weight 0 does not count toward the result and is not graded (BBB 2014J marks its first TMA 1 or 100),
    # so its mark is no score; the weight-0 CMAs of FFF are graded quizzes and stay
    graded = (results["assessment_type"] == "CMA") | (results["weight"] > 0)
    known = results[((results["is_banked"] == 1) | (marked_on < day)) & graded]
    features = pd.concat(
        [
            submitted.groupby(KEY).size().rename("assessments_submitted"),
            submitted.groupby(KEY)["days_early"].mean().rename("days_early_mean"),
            known.groupby(KEY)["score"].agg(score_mean="mean", score_min="min"),
            results[results["is_banked"] == 1].groupby(KEY).size().rename("assessments_banked"),
        ],
        axis=1,
    )
    return features, due.rename("assessments_due")


def _click_features(raw: dict[str, pd.DataFrame], day: int) -> pd.DataFrame:
    """Per registration: the VLE clicks of the days before `day` (the log starts 8 to 25 days before the start)."""
    clicks = raw["student_vle"]
    clicks = clicks[clicks["date"] < day].merge(
        raw["vle"][["id_site", "activity_type"]], on="id_site", how="left", validate="many_to_one"
    )
    since_start = clicks[clicks["date"] >= 0]
    per_type = since_start.groupby([*KEY, "activity_type"])["sum_click"].sum().unstack("activity_type", fill_value=0)
    per_type.columns = [f"clicks_{activity_type}" for activity_type in per_type.columns]
    return pd.concat(
        [
            clicks[clicks["date"] < 0].groupby(KEY)["sum_click"].sum().rename("clicks_before_start"),
            per_type,
            since_start.groupby(KEY)["date"].nunique().rename("active_days"),
            since_start[since_start["date"] >= day - 14].groupby(KEY)["sum_click"].sum().rename("clicks_last_14_days"),
            (day - clicks.groupby(KEY)["date"].max()).rename("days_since_last_click"),
        ],
        axis=1,
    )


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "highest_education": [
        "No Formal quals",
        "Lower Than A Level",
        "A Level or Equivalent",
        "HE Qualification",
        "Post Graduate Qualification",
    ],
    "imd_band": ["0-10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-70%", "70-80%", "80-90%", "90-100%"],
    "age_band": ["0-35", "35-55", "55<="],  # open-ended
}


class OpenUniversityLearningAnalyticsDataset(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("On day 60 of an online course, will a student finish with distinction, pass, fail or withdraw?"),
        use_case=(
            "On day 60 of a running module presentation, the Open University looks for students at risk, for example "
            "to offer tutor support, with a model trained on earlier presentations of the same module."
        ),
        row=(
            "One student's registration on one of 22 presentations of 7 modules of the UK Open University, 2013-2014,"
            " still active on day 60 (26,395 registrations)."
        ),
        predicted="The final result of the registration: distinction, pass, fail or withdrawn.",
        known=(
            "The module and its start month, the student's profile (sex, region, prior education, deprivation band of "
            "the area, age band, disability), the earlier attempts at the module, the credits the student is "
            "studying, the registration date, the assessment results and submission timing known by day 60, and the "
            "daily activity in the online learning environment before day 60."
        ),
        split=(
            "Whole presentations are held out in three folds, so the test data stands for a presentation the model "
            "has not seen; training can include later and concurrent presentations, but not the test students' own "
            "concurrent or later registrations."
        ),
        changes=(
            "We fix day 60 as the prediction point, build the features from what is known by then (no marks of "
            "ungraded assignments), drop the registrations that ended before day 60, and hold "
            "out whole presentations."
        ),
        fit="approximate",
        fit_reason=(
            "Deployment trains on earlier presentations only, but four start dates do not allow a split by time, so "
            "training also holds later and concurrent ones: 67% of training rows come from presentations still "
            "running on the test presentation's day 60. Training leaves out the test students' own concurrent and "
            "later registrations; 4.9% of test rows share a student with training through earlier registrations, "
            "which deployment also knows."
        ),
    )

    # Dataset
    unique_name = "open_university_learning_analytics_dataset"
    year = "2015"
    domain = "education"
    source = "Other"
    source_url = "https://research.stem.open.ac.uk/ouanalyse/open-dataset-more/"  # the OU's page, first release 2015
    license = "CC BY 4.0"
    data_tags = ("Spatial", "ForcedGroupedFromTemporal")
    download_description = """
        The OU first published the release on its own page in 2015 (see below). We download it (anonymisedData.zip)
        from the authors' figshare deposit, the data citation of Kuzilek et al. (2017):

        mkdir -p local-data-warehouse/open_university_learning_analytics_dataset
        cd local-data-warehouse/open_university_learning_analytics_dataset
        wget -O anonymisedData.zip https://ndownloader.figshare.com/files/8606371
        echo "7412686fd77cf0e0ee1e8c3e9b354308  anonymisedData.zip" | md5sum -c -
        unzip anonymisedData.zip && rm anonymisedData.zip

        This gives the seven tables assessments.csv, courses.csv, studentAssessment.csv, studentInfo.csv,
        studentRegistration.csv, studentVle.csv and vle.csv (464 MB). The OU's own page
        (https://research.stem.open.ac.uk/ouanalyse/open-dataset-more/, formerly
        https://analyse.kmi.open.ac.uk/open_dataset) shows a download button without a link, and its old file URL
        (http://schools.stem.open.ac.uk/cdn/files/anonymisedData.zip) returns 404 (both 2026-10-06). The UCI copy
        (https://archive.ics.uci.edu/static/public/349/open+university+learning+analytics+dataset.zip) holds the
        same tables with empty values written as "?": its files equal these once "?" is replaced by "" and these
        files' CRLF line ends by LF.
    """
    bibtex = """
        @article{kuzilek2017oulad,
          author = {Kuzilek, Jakub and Hlosta, Martin and Zdrahal, Zdenek},
          title = {Open University Learning Analytics dataset},
          journal = {Scientific Data},
          volume = {4},
          pages = {170171},
          year = {2017},
          doi = {10.1038/sdata.2017.171}
        }
    """
    curation_comments = """
        We start with the seven tables of the Open University Learning Analytics Dataset (OULAD): studentInfo.csv, one row per registration of a student on a module-presentation (32,593 rows; 22 presentations of 7 modules in 2013 and 2014), joined with the registration dates, the assessment results and the daily VLE click log.

        - Prediction point: the start of day 60 of the module-presentation (day 0 is its official start), when the OU looks for students at risk in a running presentation. Day 60 is our choice, made for the use case: by then the first assessment marks are back; it was not picked by comparing scores at other days. The target is final_result (Distinction, Pass, Fail, Withdrawn), the "final course results" the dataset paper names.
        - Cohort: the registrations active on day 60 (decision table). We drop the 6,190 that ended before day 60, whose result is already decided (6,182 Withdrawn and 8 Fail), and the 8 made after day 60. The 42 that withdrew on day 60 itself stay, as the features stop at day 59.
        - Assessments (TMAs and CMAs, not the final exam): assessments_due, assessments_submitted and days_early_mean use the cut-offs and submissions before day 60. score_mean and score_min use the scores known on day 60: a CMA's from its submission, a TMA's 14 days after the later of its cut-off and its submission, and a banked result from the start. The 14 days are an assumption from the OU Tutor Support Statement ("ten working days"); the data holds no return date, and with holidays ten working days take longer than 14 calendar days, so the delay may err toward a leak (skill 0.132 with it, 0.158 without, one grouped repeat). Weight-0 TMAs are left out of the scores (BBB 2014J, below); FFF's weight-0 CMAs are graded quizzes (mean mark 86) and stay. assessments_banked counts banked results.
        - studied_credits: "the modules the student is currently studying" (dataset paper), with no date. It is equal across a student's concurrent registrations, withdrawn ones included, which fits a total taken at registration; kept.
        - VLE: clicks_before_start (from the log's first day, 8 to 25 days before the start, to day -1), clicks per activity type, active_days and clicks_last_14_days on days 0-59, and days_since_last_click (missing without a click); nothing from day 60 on enters. Counts without a record are 0.
        - We drop id_student (an identifier, used first by the train filter below), date_unregistration (in the cohort the withdrawal date, after day 60) and code_presentation, whose year names the presentation (the start month stays as presentation_start). module_presentation_length (courses.csv) differs only between the years of a module and start month, so it also names the presentation and is not joined.
        - imd_band: we write the band "10-20" as "10-20%", like the other nine.
        - Categorical: module_presentation, code_module, presentation_start and the six profile columns (gender to disability).
        - Split: grouped by module_presentation (Grouping definition). Deployment would train on earlier presentations, but four start dates cannot give three temporal windows with half of the rows before each (decision table), so whole presentations are held out instead; 67% of a fold's training rows (averaged over test rows) come from presentations still running on the test presentation's day 60. Tagged ForcedGroupedFromTemporal (SPLIT-8, Lennart, 2026-10-21): on the one valid temporal window (test 2014J, 66.5% of the rows before it) untuned LightGBM has log loss 1.205 grouped against 1.185 temporal, and random forest, LightGBM and logistic regression rank the same under both splits (measured before the train filter and the weight-0 change, review panel 2026-10-20), so the grouped split costs about 0.02 log loss against real use.
        - Train filter (_make_splits): students recur, so 12.9% of a grouped test fold's rows have the same student on the train side. Shared students link all 22 presentations, so no grouping separates them. From each fold's train side we drop the registrations of its test students that started on or after the student's first test presentation (concurrent or later ones, which deployment would not know): 577-901 rows per split, 3.2-5.7% of the train side. What stays: 4.9% of test rows share a student with training only through earlier registrations, which deployment also knows. Before the filter these rows cost +0.002 to +0.005 log loss over all test rows, which is not distinguishable from removing as many random rows.
        - Anomaly: BBB 2014J changed its design. Its first TMA has weight 0 and is marked 1 or 100 (1,739 of 1,776 marks; the other BBB presentations weight and grade it). An OU analyst knows the weights and computes scores over graded assessments, so score_mean and score_min leave weight-0 TMAs out: 1,655 rows lose that mark (1,652 of BBB 2014J), and BBB 2014J has no known score on day 60. On the 9 splits, untuned LightGBM reaches log-loss skill 0.167 (standard deviation over the splits 0.015; 0.04 on BBB 2014J) and random forest 0.158 (-0.23 on BBB 2014J). With these marks in, LightGBM reached 0.141 (0.052; -0.42 on BBB 2014J) and random forest 0.168, so the change favours no model family.
        - Anomaly: 93 Withdrawn registrations (0.35% of rows, all in 2014J presentations) have no date_unregistration and stay in the cohort. 84 of them have no click on days 46-59, against 22% of the withdrawals that have a date, and 19 never clicked, so most likely withdrew before day 60. We keep them: the date would be inferred from the label and the activity, and a filter on Withdrawn alone selects on the target. 45 registrations have no date_registration (7 in the cohort, kept missing).
        - Duplicates: one pair of rows shares all features but not the result (Fail and Withdrawn); we keep both as two real registrations.
        - Spread (TP-3): untuned model families score alike on the 9 splits (log-loss skill 0.173 random forest, 0.170 LightGBM, 0.162 logistic regression; the lead of 0.011 is within twice its paired standard error of 0.009). Kept pending tuned results (Lennart, 2026-10-22): re-check with the first tuned run.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 3 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`).
    """

    # Task
    target = "final_result"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The source is a data descriptor (OU Analyse open dataset) with no prediction task or metric; our day-60 "
            "four-class task is our construction."
        )
    )
    grouping = Grouping(
        on="module_presentation",
        labels="per_sample",
        prediction_unit="row",
        context="all_rows",
        definition="""
            One group is a module-presentation (module_presentation, e.g. "BBB 2014J"): one run of a module, starting in February (B) or October (J) of 2013 or 2014; 22 runs of 7 modules. A model is used during a running presentation, whose results are not known yet, and is trained on other presentations of the same module. The OULAD page advises analysing the B and J presentations separately, each informed by the previous one of its kind: "for some presentations the corresponding previous B/J presentation do not exist and therefore the J presentation must be used to inform the B presentation or vice versa. In the dataset this is the case of CCC, EEE and GGG modules" (OULAD page, courses.csv). That advice points to earlier presentations; the test presentations are new to the model, and each registration in them is one prediction. On day 60 every registration of the running presentation is known with its day-60 features (OU Analyse scores all students of a presentation each week), so a model may use the presentation's other rows, for example to compare a student's activity with the cohort's. The split is less strict than deployment: the train side also holds later presentations and the concurrent ones of other modules (but not the test students' own concurrent or later registrations), because a temporal split by start date cannot give three windows with half of the data for training (four start dates).
        """,
    )
    splits_comment = """
        Grouped 3-fold cross-validation over the 22 module-presentations with 3 repeats (the recommended split for
        this size): each test fold holds six to nine presentations that the model has not seen. It stands
        in for the temporal split of deployment (train on earlier presentations of a module), which four start dates
        cannot give with three windows and half of the data for training. Each train side leaves out the
        registrations of that fold's test students that started on or after their first test presentation (577-901
        rows per split).
    """
    accepted_check_warnings = {
        "groups_test_groups_few": "The 22 module-presentations are all the presentations the source has (6-9 per test "
        "fold), and holding out whole presentations is the use case. Each fold still scores 7,694-10,563 registrations "
        "one by one (smallest class: 874 rows), and the signal across presentations is real: on unseen presentations "
        "logistic regression, random forest, LightGBM and kNN reach macro ROC AUC 0.753, 0.753, 0.753 and 0.642 "
        "(group_probes.py, 2026-10-20), and untuned LightGBM's log-loss skill varies little over the 9 splits "
        "(0.167, standard deviation 0.015).",
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "info": pd.read_csv(raw_dir / "studentInfo.csv"),
            "registration": pd.read_csv(raw_dir / "studentRegistration.csv"),
            "assessments": pd.read_csv(raw_dir / "assessments.csv"),
            "student_assessment": pd.read_csv(raw_dir / "studentAssessment.csv"),
            "vle": pd.read_csv(raw_dir / "vle.csv"),
            "student_vle": pd.read_csv(
                raw_dir / "studentVle.csv",
                dtype={"id_student": "int32", "id_site": "int32", "date": "int16", "sum_click": "int32"},
            ),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        day = PREDICTION_DAY
        df = raw["info"].merge(raw["registration"], on=KEY, how="left", validate="one_to_one")

        # the registrations active on the prediction day
        ended = df["date_unregistration"] < day
        not_yet = df["date_registration"] > day
        df = df.loc[~ended & ~not_yet].copy()

        df["presentation_start"] = df["code_presentation"].str[-1].map({"B": "February", "J": "October"})
        df["module_presentation"] = df["code_module"] + " " + df["code_presentation"]
        df["imd_band"] = df["imd_band"].replace({"10-20": "10-20%"})

        assessment, due = _assessment_features(raw, day)
        df = df.merge(due, left_on=["code_module", "code_presentation"], right_index=True, how="left")
        df = df.merge(assessment, left_on=KEY, right_index=True, how="left")
        clicks = _click_features(raw, day)
        df = df.merge(clicks, left_on=KEY, right_index=True, how="left")

        counts = ["assessments_due", "assessments_submitted", "assessments_banked"]
        counts += [c for c in clicks.columns if c != "days_since_last_click"]
        df[counts] = df[counts].fillna(0).astype("int64")
        # id_student stays until the split step, which uses it to filter the train side (_make_splits)
        return drop_columns(df, ["code_presentation", "date_unregistration"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(ordinal=ORDINAL_LEVELS, categorical=CATEGORICAL)

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # the grouped 3x3 cross-validation, then each train side loses the registrations of that fold's test students
        # that started on or after the student's first test presentation (concurrent or later: deployment would not
        # know them); earlier registrations stay, as deployment knows them
        student = df["id_student"].to_numpy()
        period = df["module_presentation"].astype(str).str.split(" ").str[1].to_numpy()  # "2013B" < ... < "2014J"
        splits = {}
        for repeat, folds in self._cross_validation(df).items():
            splits[repeat] = {}
            for fold, (train_rows, test) in folds.items():
                first_test = pd.Series(period[test]).groupby(student[test]).min()
                train = np.asarray(train_rows)
                first = pd.Series(student[train]).map(first_test)
                drop = (first.notna() & (pd.Series(period[train]) >= first.fillna("~"))).to_numpy()
                splits[repeat][fold] = (train[~drop].tolist(), list(test))
        return SplitPlan(splits=splits, df=df.drop(columns=["id_student"]))

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        start = df["module_presentation"].astype(str).str.split(" ").str[1]
        by_start = (
            pd.DataFrame({"start": start, "module_presentation": df["module_presentation"].astype(str)})
            .groupby("start")
            .agg(presentations=("module_presentation", "nunique"), rows=("module_presentation", "size"))
        )
        by_start["share of rows"] = (by_start["rows"] / by_start["rows"].sum()).round(3)
        by_start["share of rows before it"] = (by_start["rows"].cumsum().shift(fill_value=0) / len(df)).round(3)

        registrations = raw["info"].merge(raw["registration"], on=KEY, how="left", validate="one_to_one")
        status = np.select(
            [
                registrations["date_unregistration"] < PREDICTION_DAY,
                registrations["date_registration"] > PREDICTION_DAY,
            ],
            [f"ended before day {PREDICTION_DAY} (dropped)", f"registered after day {PREDICTION_DAY} (dropped)"],
            default=f"active on day {PREDICTION_DAY} (kept)",
        )
        cohort = pd.crosstab(pd.Series(status, name="registration"), registrations["final_result"], margins=True)
        return [
            Decision(
                "Grouped by module-presentation, not temporal by start date",
                "Deployment trains on earlier presentations of a module, but the data has four start dates: only the "
                "newest (2014J) has half of the rows before it, so a temporal split cannot give three windows. Whole "
                "presentations are held out instead.",
                by_start,
            ),
            Decision(
                f"Cohort: the registrations active on day {PREDICTION_DAY}",
                "A registration that ended before the prediction day already has its result (Withdrawn, or Fail for 8); "
                "one made after it does not exist yet.",
                cohort,
            ),
        ]
