"""Curated dataset definition for `predict_students_dropout_and_academic_success` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    Splits,
    TaskSummary,
    Temporal,
    drop_columns,
)

# Scores and ratings with no words per level: numbers, as the source ships them (CLEAN-14).
SCORES = ["Application_order"]

# The enrolment year from Portugal's national figures (INE, via PORDATA, the source's macro data): each year has one
# (unemployment %, inflation %, GDP growth %) triple, and every student carries the triple of the year they enrolled.
YEAR_OF_UNEMPLOYMENT = {
    7.6: 2008,
    9.4: 2009,
    10.8: 2010,
    12.7: 2011,
    15.5: 2012,
    16.2: 2013,
    13.9: 2014,
    12.4: 2015,
    11.1: 2016,
    8.9: 2017,
}
# The normal length of a course in years: "3 years, except Nursing which has 4 years" (Realinho et al. 2022, Sec. 3.1);
# the label is the status at its end.
NORMAL_LENGTH = {"Nursing": 4}
DEFAULT_LENGTH = 3
# One test window per enrolment cohort, newest first.
TEST_COHORTS = (2017, 2016, 2015, 2014)


class PredictStudentsDropoutAndAcademicSuccess(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a student drop out, still be enrolled, or graduate by the end of the normal length of the course?"
        ),
        use_case=(
            "A higher-education institution identifies students at risk of dropping out or failing, early in their "
            "studies, to offer them support (the source's aim); as the data holds first-year results, the prediction "
            "point is the end of the first year."
        ),
        row=(
            "One student of 17 undergraduate degrees at one Portuguese higher-education institution (4,424 students);"
            " enrolment years 2008 to 2017, recovered from the national figures each student carries."
        ),
        predicted=(
            "The student's status at the end of the normal length of the course: graduated (49.93%), dropped out "
            "(32.12%) or still enrolled (17.95%)."
        ),
        known=(
            "Background at enrolment (course, day or evening classes, application route and choice rank, previous "
            "schooling and grades, age, nationality, parents' education and jobs, scholarship, special needs), "
            "national unemployment, inflation and GDP, and the units taken, passed and grades of the first two "
            "semesters."
        ),
        split=(
            "Four enrolment cohorts, 2014 to 2017, each scored at the end of its first year; training is the students "
            "whose course had reached its normal end by then (three years, four for Nursing)."
        ),
        changes=(
            "We drop the fee and debt status, which the source does not date and which look read at the file's "
            "extract, years after many students left, and recover each student's enrolment year from the national "
            "figures to split by cohort."
        ),
        fit="approximate",
        fit_reason=("When the scholarship status was recorded is not stated, so it may be read after the first year."),
    )

    # Dataset
    unique_name = "predict_students_dropout_and_academic_success"
    domain = "education"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5MC89",
            license="CC BY 4.0",
            year="2021",
            bibtex=r"""
                @inproceedings{martins2021early,
                  title={Early prediction of student’s performance in higher education: A case study},
                  author={Martins, M{\'o}nica V and Tolledo, Daniel and Machado, Jorge and Baptista, Lu{\'\i}s MT and Realinho, Valentim},
                  booktitle={Trends and Applications in Information Systems and Technologies: Volume 1 9},
                  pages={166--175},
                  year={2021},
                  organization={Springer}
                }
            """,
        ),
    )
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/predict_students_dropout_and_academic_success/ && wget -P local-data-warehouse/predict_students_dropout_and_academic_success/ https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip && unzip local-data-warehouse/predict_students_dropout_and_academic_success/predict+students+dropout+and+academic+success.zip -d local-data-warehouse/predict_students_dropout_and_academic_success/  && rm local-data-warehouse/predict_students_dropout_and_academic_success/predict+students+dropout+and+academic+success.zip
    """
    curation_comments = """
        - We renamed the target variable and fixed some typos in the feature names.
        - We reversed the ordinal encoding of all categorical features.
        - We removed whitespaces and special characters from the feature names.
        - Partial order, left unordered (2026-11-01, CLEAN-14): `Previous_qualification`, `Mothers_qualification` and
          `Fathers_qualification` lie on the Portuguese education ladder, but the pre- and post-Bologna degrees are ties
          and the old-system courses sit beside the year levels, so there is no single line.
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 1 scores with no words per level are
          numbers (`SCORES`): `Application_order`.
        - Enrolment year (2026-11-12, Andrej): the file has no year column, but unemployment, inflation and GDP take
          ten value triples, each Portugal's published figures of one year (INE, via PORDATA, the source's macro
          data), so `enrolment_year` (2008 to 2017) is mapped from `Unemployment_rate` and checked against the other
          two. It is the time column of the splits; it adds no information the triple does not already give.
        - We drop `Tuition_fees_up_to_date` and `Debtor` (2026-11-12, Andrej, review issue 1 B): the source gives no
          recording date (the data paper lists them as socioeconomic data from the student-records file), arrears
          cannot exist at enrolment, and the pattern fits one status read at the file's extract. 86.6% of the 528
          students behind on fees dropped out, against 24.7% of the others (debtors: 62.0% of 503, against 28.3%);
          students still enrolled are behind on fees at 0.8% in the 2008-2011 cohorts and 15% in 2015-2017 (debtors
          5% and 25%), while graduates are behind at about 1.2% in every era. A previous degree does not explain the
          debt: debtors are 10% to 11% among holders of another degree and 8% among first-time students. With both,
          log loss was 0.587 (untuned LightGBM, the random folds of 2026-11-06), without them 0.633.
        - `Scholarship_holder` (2026-11-12, Andrej): no recording date, like the fee and debt status; kept, unlike
          them, as a scholarship can exist by the end of the first year and the data shows no sign of a later read
          (holders drop out at 12% against 39%; without it log loss rises by 0.004, untuned LightGBM, shipped random
          folds of 2026-11-06).
    """

    # Task
    target = "AcademicOutcome"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason="UCI page and the data paper define no task metric; the first-publication case study compares classifiers on several scores (likely F1 given the class imbalance) without a declared task metric. Not verified in full text."
    )

    # Splits: one window per cohort, scored when the cohort ends its first year; training holds only the students whose
    # outcome is known by then, so the gap differs by course length (see `splits_comment`).
    temporal = Temporal(on="enrolment_year", horizon=1, horizon_unit="years", gap=1, gap_unit="years")
    splits_comment = """
        Four test windows, one enrolment cohort each, newest first (2017, 2016, 2015, 2014; 368, 414, 445 and 390
        students). A window's model is fitted when its cohort ends its first year. The label is the status at the end of the
        course's normal length (three years, four for Nursing; Realinho et al. 2022, Sec. 3.1), so training holds only
        the students whose normal end came before that: for a three-year course the cohorts up to two years older
        (a gap of one cohort), for Nursing up to three years older (a gap of two). The training sides hold 54% to 80%
        of the 4,424 students. Measured 2026-11-11 (untuned LightGBM, log loss): 0.740 (2017), 0.791, 0.694, 0.706
        (2014), +0.02 to +0.14 above training on as many students drawn from all cohorts; the random split this
        replaces flattered log loss by that much.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        data = pd.read_csv(raw_dir / "data.csv", sep=";")
        return data

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        data = raw
        target_feature = "AcademicOutcome"
        data = data.rename(
            columns={
                "Target": target_feature,
                "Daytime/evening attendance	": "Daytime/evening attendance",
            }
        )
        maps = {
            "International": {1: "yes", 0: "no"},
            "Marital status": {
                1: "single",
                2: "married",
                3: "widower",
                4: "divorced",
                5: "facto union",
                6: "legally separated",
            },
            "Application mode": {
                1: "1st phase - general contingent",
                2: "Ordinance No. 612/93",
                5: "1st phase - special contingent (Azores Island)",
                7: "Holders of other higher courses",
                10: "Ordinance No. 854-B/99",
                15: "International student (bachelor)",
                16: "1st phase - special contingent (Madeira Island)",
                17: "2nd phase - general contingent",
                18: "3rd phase - general contingent",
                26: "Ordinance No. 533-A/99, item b2) (Different Plan)",
                27: "Ordinance No. 533-A/99, item b3 (Other Institution)",
                39: "Over 23 years old",
                42: "Transfer",
                43: "Change of course",
                44: "Technological specialization diploma holders",
                51: "Change of institution/course",
                53: "Short cycle diploma holders",
                57: "Change of institution/course (International)",
            },
            "Course": {
                33: "Biofuel Production Technologies",
                171: "Animation and Multimedia Design",
                8014: "Social Service (evening attendance)",
                9003: "Agronomy",
                9070: "Communication Design",
                9085: "Veterinary Nursing",
                9119: "Informatics Engineering",
                9130: "Equinculture",
                9147: "Management",
                9238: "Social Service",
                9254: "Tourism",
                9500: "Nursing",
                9556: "Oral Hygiene",
                9670: "Advertising and Marketing Management",
                9773: "Journalism and Communication",
                9853: "Basic Education",
                9991: "Management (evening attendance)",
            },
            "Daytime/evening attendance": {1: "daytime", 0: "evening"},
            "Previous qualification": {
                1: "Secondary education",
                2: "Higher education - bachelor's degree",
                3: "Higher education - degree",
                4: "Higher education - master's",
                5: "Higher education - doctorate",
                6: "Frequency of higher education",
                9: "12th year of schooling - not completed",
                10: "11th year of schooling - not completed",
                12: "Other - 11th year of schooling",
                14: "10th year of schooling",
                15: "10th year of schooling - not completed",
                19: "Basic education 3rd cycle (9th/10th/11th year) or equiv.",
                38: "Basic education 2nd cycle (6th/7th/8th year) or equiv.",
                39: "Technological specialization course",
                40: "Higher education - degree (1st cycle)",
                42: "Professional higher technical course",
                43: "Higher education - master (2nd cycle)",
            },
            "Nacionality": {
                1: "Portuguese",
                2: "German",
                6: "Spanish",
                11: "Italian",
                13: "Dutch",
                14: "English",
                17: "Lithuanian",
                21: "Angolan",
                22: "Cape Verdean",
                24: "Guinean",
                25: "Mozambican",
                26: "Santomean",
                32: "Turkish",
                41: "Brazilian",
                62: "Romanian",
                100: "Moldova (Republic of)",
                101: "Mexican",
                103: "Ukrainian",
                105: "Russian",
                108: "Cuban",
                109: "Colombian",
            },
            "Mother's qualification": {
                1: "Secondary Education - 12th Year of Schooling or Eq.",
                2: "Higher Education - Bachelor's Degree",
                3: "Higher Education - Degree",
                4: "Higher Education - Master's",
                5: "Higher Education - Doctorate",
                6: "Frequency of Higher Education",
                9: "12th Year of Schooling - Not Completed",
                10: "11th Year of Schooling - Not Completed",
                11: "7th Year (Old)",
                12: "Other - 11th Year of Schooling",
                14: "10th Year of Schooling",
                18: "General commerce course",
                19: "Basic Education 3rd Cycle",
                22: "Technical-professional course",
                26: "7th year of schooling",
                27: "2nd cycle of the general high school course",
                29: "9th Year of Schooling - Not Completed",
                30: "8th year of schooling",
                34: "Unknown",
                35: "Can't read or write",
                36: "Can read without having a 4th year of schooling",
                37: "Basic education 1st cycle (4th/5th year) or equiv.",
                38: "Basic Education 2nd Cycle",
                39: "Technological specialization course",
                40: "Higher education - degree (1st cycle)",
                41: "Specialized higher studies course",
                42: "Professional higher technical course",
                43: "Higher Education - Master (2nd cycle)",
                44: "Higher Education - Doctorate (3rd cycle)",
            },
            "Father's qualification": {
                1: "Secondary Education - 12th Year of Schooling or Eq.",
                2: "Higher Education - Bachelor's Degree",
                3: "Higher Education - Degree",
                4: "Higher Education - Master's",
                5: "Higher Education - Doctorate",
                6: "Frequency of Higher Education",
                9: "12th Year of Schooling - Not Completed",
                10: "11th Year of Schooling - Not Completed",
                11: "7th Year (Old)",
                12: "Other - 11th Year of Schooling",
                13: "2nd year complementary high school course",
                14: "10th Year of Schooling",
                18: "General commerce course",
                19: "Basic Education 3rd Cycle",
                20: "Complementary High School Course",
                22: "Technical-professional course",
                25: "Complementary High School Course - not concluded",
                26: "7th year of schooling",
                27: "2nd cycle of the general high school course",
                29: "9th Year of Schooling - Not Completed",
                30: "8th year of schooling",
                31: "General Course of Administration and Commerce",
                33: "Supplementary Accounting and Administration",
                34: "Unknown",
                35: "Can't read or write",
                36: "Can read without having a 4th year of schooling",
                37: "Basic education 1st cycle",
                38: "Basic Education 2nd Cycle",
                39: "Technological specialization course",
                40: "Higher education - degree (1st cycle)",
                41: "Specialized higher studies course",
                42: "Professional higher technical course",
                43: "Higher Education - Master (2nd cycle)",
                44: "Higher Education - Doctorate (3rd cycle)",
            },
            "Mother's occupation": {
                0: "Student",
                1: "Representatives of Legislative/Executive Bodies",
                2: "Specialists in Intellectual/Scientific Activities",
                3: "Intermediate Level Technicians and Professions",
                4: "Administrative staff",
                5: "Personal Services, Security and Safety Workers and Sellers",
                6: "Farmers and Skilled Workers",
                7: "Skilled Workers in Industry/Construction/Craftsmen",
                8: "Installation and Machine Operators",
                9: "Unskilled Workers",
                10: "Armed Forces Professions",
                90: "Other Situation",
                99: "(blank)",
                122: "Health professionals",
                123: "Teachers",
                125: "ICT Specialists",
                131: "Intermediate science and engineering technicians",
                132: "Health technicians",
                134: "Legal/social/cultural technicians",
                141: "Office workers",
                143: "Finance/statistics workers",
                144: "Other administrative support",
                151: "Personal service workers",
                152: "Sellers",
                153: "Personal care workers",
                171: "Skilled construction workers",
                173: "Printing/jewelers/artisans",
                175: "Food/woodworking workers",
                191: "Cleaning workers",
                192: "Unskilled agriculture workers",
                193: "Unskilled construction workers",
                194: "Meal preparation assistants",
            },
            "Father's occupation": {
                0: "Student",
                1: "Representatives of Legislative/Executive Bodies",
                2: "Specialists in Intellectual/Scientific Activities",
                3: "Intermediate Level Technicians and Professions",
                4: "Administrative staff",
                5: "Personal Services, Security and Safety Workers and Sellers",
                6: "Farmers and Skilled Workers",
                7: "Skilled Workers in Industry/Construction/Craftsmen",
                8: "Installation and Machine Operators",
                9: "Unskilled Workers",
                10: "Armed Forces Professions",
                90: "Other Situation",
                99: "(blank)",
                101: "Armed Forces Officers",
                102: "Armed Forces Sergeants",
                103: "Other Armed Forces personnel",
                112: "Directors of administrative services",
                114: "Hotel/catering services directors",
                121: "Physical sciences/engineering specialists",
                122: "Health professionals",
                123: "Teachers",
                124: "Finance/administration specialists",
                131: "Intermediate science technicians",
                132: "Health technicians",
                134: "Legal/social/cultural technicians",
                135: "ICT technicians",
                141: "Office workers",
                143: "Finance/statistics workers",
                144: "Other administrative support",
                151: "Personal service workers",
                152: "Sellers",
                153: "Personal care workers",
                154: "Security personnel",
                161: "Market-oriented farmers",
                163: "Subsistence farmers",
                171: "Skilled construction workers",
                172: "Metal workers",
                174: "Electricians",
                175: "Food/craft workers",
                181: "Machine operators",
                182: "Assembly workers",
                183: "Vehicle drivers",
                192: "Unskilled agriculture workers",
                193: "Unskilled construction workers",
                194: "Meal preparation assistants",
                195: "Street vendors",
            },
            "Displaced": {1: "yes", 0: "no"},
            "Educational special needs": {1: "yes", 0: "no"},
            "Gender": {1: "male", 0: "female"},
            "Scholarship holder": {1: "yes", 0: "no"},
        }
        for column, mapping in maps.items():
            data[column] = data[column].map(mapping)
        # More renaming
        data = data.rename(columns={"Nacionality": "Nationality"})
        data.columns = [
            c.replace(" ", "_").replace(")", "").replace("(", "").replace("'", "").replace("/", "")
            for c in data.columns
        ]
        df = data
        # the fee and debt status have no recording date and look read at the extract (curation notes)
        df = drop_columns(df, ["Debtor", "Tuition_fees_up_to_date"])
        # scores with no words per level are numbers (CLEAN-14)
        df[SCORES] = df[SCORES].astype("object").apply(pd.to_numeric)
        # the enrolment year from the national figures (YEAR_OF_UNEMPLOYMENT, curation notes)
        df["enrolment_year"] = df["Unemployment_rate"].round(1).map(YEAR_OF_UNEMPLOYMENT)
        assert df["enrolment_year"].notna().all(), "an unemployment rate matches no year"
        assert df.groupby("enrolment_year")[["Inflation_rate", "GDP"]].nunique().eq(1).all().all(), (
            "inflation or GDP disagree within a year"
        )
        df["enrolment_year"] = df["enrolment_year"].astype("int64")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Marital_status",
                "Application_mode",
                "Course",
                "Daytimeevening_attendance",
                "Previous_qualification",
                "Nationality",
                "Mothers_qualification",
                "Fathers_qualification",
                "Mothers_occupation",
                "Fathers_occupation",
                "Displaced",
                "Educational_special_needs",
                "Gender",
                "Scholarship_holder",
                "International",
            ],
        )

    def _make_splits(self, df: pd.DataFrame) -> Splits:
        """One window per cohort in `TEST_COHORTS`; train is every student whose course's normal end came before the
        cohort's first year ended (enrolment year + normal length <= test cohort + 1).
        """
        year = df["enrolment_year"].to_numpy()
        length = df["Course"].astype(str).map(NORMAL_LENGTH).fillna(DEFAULT_LENGTH).to_numpy()
        positions = np.arange(len(df))
        splits: Splits = {}
        for i, cohort in enumerate(TEST_COHORTS):
            train = positions[year + length <= cohort + 1]
            test = positions[year == cohort]
            assert len(train) >= 0.5 * len(df), f"the {cohort} window trains on under half of the students"
            splits[i] = {0: (train.tolist(), test.tolist())}
        return splits
