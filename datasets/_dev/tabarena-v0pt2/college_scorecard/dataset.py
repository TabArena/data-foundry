"""Curated dataset definition for `college_scorecard` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

RAW_ZIP = "College_Scorecard_Raw_Data_06102026.zip"
FIRST_COHORT = 2001  # first fall with admissions and test scores (documentation p. 12)
LAST_COHORT = 2018  # newest cohort with a published completion rate (MERGED2024_25_PP.csv)
YEARS_TO_RATE = 6  # a four-year cohort's 150% completion rate is in the file six years after entry
MIN_COHORT_SIZE = 30  # the threshold below which the Scorecard suppresses its pooled rates (documentation p. 25)
NEW_SAT_COHORT = 2017  # the first entering cohort reported on the redesigned SAT scale (the file of 2017-18)
# The College Board's new-to-old SAT concordance (Concordance Tables, May 9, 2016): Table 3 for the math section,
# Table 2 for the total score (old scale: critical reading plus math), in 10-point steps.
SAT_TABLES = "sat_concordance.csv"
SAT_COLUMNS = {"SATMT25": "math", "SATMT75": "math", "SAT_AVG": "total"}

PCIP = [
    f"PCIP{code:02d}"
    for code in (1, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 19, 22, 23, 24, 25, 26, 27, 29, 30, 31, 38, 39, 40, 41, 42,
                 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 54)
]  # fmt: skip
# race and ethnicity shares: the categories IPEDS uses from 2008-09 on, and the older ones they replace
NEW_RACE = ["UGDS_WHITE", "UGDS_BLACK", "UGDS_HISP", "UGDS_ASIAN", "UGDS_AIAN", "UGDS_NHPI", "UGDS_2MOR"]
OLD_RACE = {
    "UGDS_WHITE": "UGDS_WHITENH",
    "UGDS_BLACK": "UGDS_BLACKNH",
    "UGDS_HISP": "UGDS_HISPOLD",
    "UGDS_ASIAN": "UGDS_API",  # Asian/Pacific Islander: holds the later UGDS_NHPI share too
    "UGDS_AIAN": "UGDS_AIANOLD",
}
FEATURES = [
    # the institution in the entry year
    "STABBR", "REGION", "CONTROL", "PREDDEG", "HIGHDEG", "MAIN", "NUMBRANCH", "OPEFLAG", "DISTANCEONLY",
    # admissions of the entering class (fall of the entry year); the SAT reading percentiles are left out (the
    # redesigned section of 2017 on has no concordance to the old one)
    "OPENADMP", "ADMCON7", "ADM_RATE", "ADM_RATE_ALL", "ACTCM25", "ACTCM75", "ACTEN25", "ACTEN75", "ACTMT25",
    "ACTMT75", *SAT_COLUMNS,
    # enrollment and its composition (fall of the entry year)
    "UGDS", "GRADS", "UGDS_WOMEN", *NEW_RACE, "UGDS_NRA", "UGDS_UNKN", *OLD_RACE.values(), "PPTUG_EF", "UG25ABV",
    # aid, prices, finances and faculty
    "PCTPELL", "FTFTPCTPELL", "PCTFLOAN", "FTFTPCTFLOAN", "COSTT4_A", "TUITIONFEE_IN", "TUITIONFEE_OUT", "NPT4_PUB",
    "NPT4_PRIV", "TUITFTE", "INEXPFTE", "ENDOWBEGIN", "AVGFACSAL", "PFTFAC", "STUFACR",
    # program mix: share of awards by 2-digit CIP family (the academic year before)
    *PCIP,
    # the latest published first-year retention rate (the cohort one year older, back in the entry fall)
    "RET_FT4",
]  # fmt: skip
OUTCOME = ["C150_4", "D150_4"]  # completion rate within 150% of normal time and its adjusted cohort count
LATEST_RATE = "C150_4_LATEST"  # C150_4 of the entry-year file: the cohort six years older, the newest rate published

# value labels from the data dictionary (CollegeScorecardDataDictionary.xlsx, sheet Institution_Data_Dictionary)
LABELS = {
    "CONTROL": {1: "Public", 2: "Private nonprofit", 3: "Private for-profit"},
    "PREDDEG": {
        0: "Not classified",
        1: "Predominantly certificate-degree granting",
        2: "Predominantly associate's-degree granting",
        3: "Predominantly bachelor's-degree granting",
        4: "Entirely graduate-degree granting",
    },
    "HIGHDEG": {
        0: "Non-degree-granting",
        1: "Certificate degree",
        2: "Associate degree",
        3: "Bachelor's degree",
        4: "Graduate degree",
    },
    "REGION": {
        0: "U.S. Service Schools",
        1: "New England (CT, ME, MA, NH, RI, VT)",
        2: "Mid East (DE, DC, MD, NJ, NY, PA)",
        3: "Great Lakes (IL, IN, MI, OH, WI)",
        4: "Plains (IA, KS, MN, MO, NE, ND, SD)",
        5: "Southeast (AL, AR, FL, GA, KY, LA, MS, NC, SC, TN, VA, WV)",
        6: "Southwest (AZ, NM, OK, TX)",
        7: "Rocky Mountains (CO, ID, MT, UT, WY)",
        8: "Far West (AK, CA, HI, NV, OR, WA)",
        9: "Outlying Areas (AS, FM, GU, MH, MP, PR, PW, VI)",
    },
    "OPEFLAG": {
        1: "Participates in Title IV federal financial aid programs",
        2: "Branch campus of a main campus that participates in Title IV",
        3: "Deferment only - limited participation",
        5: "Not currently participating in Title IV, has an OPE ID number",
        6: "Not currently participating in Title IV, does not have OPE ID number",
        7: "Stopped participating during the collection year",
        8: "New participants (became eligible during the collection year)",
        19: "Not eligible",
    },
    "OPENADMP": {1: "Yes", 2: "No", 3: "Does not enroll first-time students"},
    "ADMCON7": {
        1: "Required",
        2: "Recommended",
        3: "Neither required nor recommended",
        4: "Do not know",
        5: "Considered but not required",
    },
}
TO_MISSING = {"ADMCON7": (-1, -2)}  # IPEDS: -1 not reported, -2 not applicable (open admission, until fall 2013)


def cohort_rows(raw: pd.DataFrame) -> pd.DataFrame:
    """One row per four-year institution and entering cohort: the entry-year file joined with its completion rate.

    The features come from the file of the entry year (its C150_4, the rate of the cohort six years older, becomes
    C150_4_LATEST), the target C150_4 and D150_4 from the file six years later (the cohort map gives C150_4 in
    MERGED_2024-25 as the fall 2018 cohort). Keeps UNITID for the decisions.
    """
    entry = raw[(raw["ICLEVEL"] == 1) & raw["file_year"].between(FIRST_COHORT, LAST_COHORT)]
    entry = entry.drop(columns=["ICLEVEL", "D150_4"]).rename(
        columns={"file_year": "cohort_year", "C150_4": LATEST_RATE}
    )
    outcome = raw.loc[raw["C150_4"].notna(), ["UNITID", "file_year", *OUTCOME]]
    outcome = outcome.assign(cohort_year=outcome["file_year"] - YEARS_TO_RATE).drop(columns="file_year")
    return entry.merge(outcome, on=["UNITID", "cohort_year"], how="inner", validate="one_to_one")


def to_labels(series: pd.Series, labels: dict, missing: tuple = ()) -> pd.Series:
    """Map codes to the dictionary's labels; codes in ``missing`` become NA, any other unknown code fails."""
    unknown = set(series.dropna().unique()) - set(labels) - set(missing)
    if unknown:
        msg = f"{series.name}: codes {sorted(unknown)} are not in the data dictionary."
        raise ValueError(msg)
    return series.map(labels)


class CollegeScorecard(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What share of the students entering a US four-year college this fall will graduate within six years?"
        ),
        use_case=(
            "For example, when a new class enters, a state agency, an accreditor or the college itself estimates its "
            "six-year completion rate from the college's published data, to plan support or review colleges likely to"
            " fall short."
        ),
        row=(
            "One four-year US institution and the first-time, full-time class that entered it in one fall, 2001 to "
            "2018, with at least 30 students (34,431 rows, U.S. Department of Education's College Scorecard)."
        ),
        predicted=(
            "The share of the class that completes within 150% of normal time (six years for a four-year degree), "
            "published six years after entry; a rate from 0 to 1."
        ),
        known=(
            "The college's figures in the Scorecard file of the entry year: type, control, state and region, degrees,"
            " admission rate, ACT and SAT scores, cost and net price, aid and loan shares, enrollment by race and field of"
            " study, spending and faculty, and its latest published completion and retention rates of older classes."
        ),
        split=(
            "Each of four test windows is one entering class (2015 to 2018, newest first); training is every class "
            "that entered at least six years before, whose rate was published by then. About 92% of the test colleges"
            " also appear in training with older classes."
        ),
        changes=(
            "We rebuilt the task from the Department of Education's files: features from the entry year, the rate "
            "from six years later, and a five-year gap before each test class. The TableShift copy binarises the rate"
            " and takes features from the year it is reported. SAT scores from 2017 on, on the redesigned test, are"
            " put back on the old scale with the College Board's tables."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is published in the entry year and the rate follows six years later, as in "
            "use; each test class comes after every class with a published rate. State and region carry their newest "
            "value in old files, a small exception."
        ),
    )

    # Dataset
    unique_name = "college_scorecard"
    year = "2026"
    domain = "education"
    source = "GOV Website"
    source_url = "https://collegescorecard.ed.gov/data/"
    license = "CC BY (data.gov catalog entry of the U.S. Department of Education)"
    data_tags = ("Spatial",)
    download_description = """
        College Scorecard "All Data Files" release of June 10, 2026 (U.S. Department of Education). The official link
        on https://collegescorecard.ed.gov/data/ is
        https://ed-public-download.scorecard.network/downloads/College_Scorecard_Raw_Data_06102026.zip; it answered
        HTTP 403 (CloudFront) from our servers on 2026-10-06, so we take the Internet Archive copy of the same file.
        Its MD5 equals the ETag of the original (38f26ca8776518f77836ddfa1e219de8).

        mkdir -p local-data-warehouse/college_scorecard
        wget -O local-data-warehouse/college_scorecard/College_Scorecard_Raw_Data_06102026.zip \\
          "https://web.archive.org/web/20260822105756id_/https://ed-public-download.scorecard.network/downloads/College_Scorecard_Raw_Data_06102026.zip"
        md5sum local-data-warehouse/college_scorecard/College_Scorecard_Raw_Data_06102026.zip

        `sat_concordance.csv` next to this file holds Table 2 (total score) and Table 3 (math section) of the College
        Board's "Concordance Tables" for converting new SAT scores to old ones (released May 9, 2016):
        https://satsuite.collegeboard.org/media/pdf/higher-ed-brief-sat-concordance.pdf

        The zip (470 MB) stays packed; `_load_raw` reads the 30 files MERGED1996_97_PP.csv to MERGED2025_26_PP.csv
        from it. Which year each column of each file covers is in the data dictionary of this release (sheet
        Institution_Cohort_Map; README "Released June 10, 2026") and in the technical documentation (version September
        2025, the pages cited in the curation notes), pinned as Internet Archive snapshots:
        https://web.archive.org/web/20260830015514/https://collegescorecard.ed.gov/files/CollegeScorecardDataDictionary.xlsx
        https://web.archive.org/web/20260630125853/https://collegescorecard.ed.gov/files/InstitutionDataDocumentation.pdf
    """
    bibtex = r"""
        @misc{usdoe2026collegescorecard,
            author       = {{U.S. Department of Education}},
            title        = {{College Scorecard}: All Data Files (Institution-Level Data, 1996-97 to 2025-26)},
            year         = {2026},
            month        = jun,
            note         = {Data release of June 10, 2026},
            howpublished = {\url{https://collegescorecard.ed.gov/data/}}
        }
    """
    curation_comments = """
        We start with the files MERGED1996_97_PP.csv to MERGED2025_26_PP.csv of the College Scorecard release of June 10, 2026 (U.S. Department of Education).

        - Prediction point: the fall a first-time, full-time cohort enters a four-year institution. A model sees that year's Scorecard file, including the institution's latest published outcomes, and predicts the share of the cohort that completes within 150% of normal time, published six files later (Institution_Cohort_Map).
        - One row per institution and entering cohort of fall 2001-2018 (the first test scores and the last completion rates): the features of a four-year institution (ICLEVEL = 1) from the entry-year file, and as target `completion_rate_150pct` the C150_4 of the file six years later, joined on UNITID. The entry file's own C150_4, the rate of the cohort six years older, becomes C150_4_LATEST.
        - We keep cohorts of at least 30 students (D150_4), the size below which the Scorecard suppresses its pooled rates (documentation p. 25).
        - Features: close to TableShift's list. We drop columns the release fills from its newest file or one fixed year (LOCALE, CCBASIC, CCSIZSET, ACCREDAGENCY, HBCU, SCH_DEG), which would show old cohorts later information, series that end before the newest test cohort (the NSLDS student profile, the census shares, the writing scores) and mostly blank ones, and add per-year columns such as PREDDEG, C150_4_LATEST and RET_FT4. UG25ABV stays, though IPEDS collects it for odd falls only.
        - SAT: from the 2017 cohort on the Scorecard reports the redesigned test, unlike every training cohort (median change within an institution from 2016 to 2017: +30 SATMT25, +70 SAT_AVG, against at most 7 between any two other years up to 2018). We put SATMT25, SATMT75 and SAT_AVG of those cohorts back on the old scale with the College Board's concordance tables (May 2016; linear between their 10-point steps), after which the median 2016-2017 change is 0 and -5 (Lennart, 2026-10-16). Untuned LightGBM R² on the 2018 and 2017 windows: 0.783 and 0.802 as published, 0.798 and 0.808 converted, 0.796 and 0.809 without SAT; the ACT columns cover most of the same institutions. SATVR25/75 stay out: the new reading-and-writing section has no table to the old critical reading section.
        - The institution's own history stays: C150_4_LATEST and RET_FT4 are published in the entry-year file, and an entity's own history is legitimate under a temporal split. The latest rate carried forward scores R² 0.734 on the 2018 window (decision table), untuned LightGBM on all features 0.797.
        - Codes become the data dictionary's labels. ADMCON7's -1 (not reported) and -2 (not applicable, the open-admission institutions up to 2013, blank from 2014 on) become missing.
        - Race and ethnicity shares: in the 2008-09 and 2009-10 files an institution reports in the old IPEDS categories, the new ones or both, with 0.0 in the set it does not use. Each share becomes the sum of its new and old category, and UGDS_NHPI and UGDS_2MOR are missing where only the old set was used.
        - We drop the identifier UNITID, ICLEVEL (constant after the filter) and D150_4 (from the outcome file). STABBR and REGION stay, though old files hold their newest value.
        - Split: temporal by entering cohort with a label gap (splits comment), not grouped by institution, since a model is used on the next cohorts of institutions it has seen (decision table).
        - Anomaly: completion rates of 0 (24 institution-cohorts) and 1 (14), and ACT 25th percentiles below 10 (56 rows), kept as reported.
        - Note: we keep the rate as a regression target; TableShift binarizes it at 0.5.
    """

    # Task
    target = "completion_rate_150pct"
    problem_type = "regression"

    # Splits
    splits_comment = """
        Expanding-window temporal splits by entering cohort: 4 test windows of one cohort each (the falls of 2018, 2017, 2016 and 2015), newest first. Train is every cohort that entered at least six years before the test cohort (a gap of five cohort years): a cohort's 150% completion rate is published six Scorecard files after it entered, in the file that also publishes the entry data of the cohort being predicted, so the five cohorts in between have no label yet at the prediction point. The windows roll back from the newest cohort while train keeps at least half of the 18 cohorts, which allows 4 windows instead of the 9 an IID task of this size would get. The cohorts of 2013 and 2014 are in no split: they sit in the gap of every window and before the oldest test window. Without the gap, untuned LightGBM reaches R² 0.86 instead of 0.81 (mean of the 4 windows): training on cohorts whose rate is not yet published overstates the scores.
    """
    temporal = Temporal(
        on="cohort_year",
        splits=TemporalSplits(window=1, unit="unique", n_windows=9, gap=YEARS_TO_RATE - 1, min_train_fraction=0.5),
        horizon=1,
        horizon_unit="years",
        gap=YEARS_TO_RATE - 1,
        gap_unit="years",
    )
    accepted_check_warnings = {
        "splits_rows_unused": "By design: the cohorts of 2013 and 2014 (3,676 rows) lie in the five-year label gap of "
        "every window (the newest window trains on 2001-2012) and before the oldest test window (2015, the last one "
        "whose train side keeps half of the cohorts).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = ["UNITID", "ICLEVEL", *FEATURES, *OUTCOME]
        frames, years = [], []
        with zipfile.ZipFile(raw_dir / RAW_ZIP) as archive:
            names = sorted(n for n in archive.namelist() if re.fullmatch(r"[^/]+/MERGED\d{4}_\d{2}_PP\.csv", n))
            for name in names:
                with archive.open(name) as file:
                    frames.append(pd.read_csv(file, usecols=columns, na_values=["NULL", "PrivacySuppressed"]))
                years.append(int(re.search(r"MERGED(\d{4})_", name).group(1)))
        # the file's academic year (MERGED2018_19_PP.csv: 2018) as the first column; copy() joins the column blocks
        raw = pd.concat(frames, keys=years, names=["file_year", None]).copy()
        return raw.reset_index(level="file_year").reset_index(drop=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. Features of the entry year joined with the cohort's completion rate six files later.
        df = cohort_rows(raw)
        # 2. Cohorts of at least 30 students (the threshold the Scorecard applies to its pooled rates).
        df = df[df["D150_4"] >= MIN_COHORT_SIZE]
        # 3. SAT scores from the 2017 cohort on are on the redesigned scale: back to the old one, which every training
        #    cohort has, with the College Board's concordance tables (linear between their 10-point steps).
        tables = pd.read_csv(self.folder / SAT_TABLES)
        redesigned = df["cohort_year"] >= NEW_SAT_COHORT
        for column, table in SAT_COLUMNS.items():
            points = tables[tables["table"] == table]
            df.loc[redesigned, column] = np.interp(df.loc[redesigned, column], points["new_sat"], points["old_sat"])
        # 4. Race and ethnicity shares. Before 2008 only the old categories exist; in the 2008-09 and 2009-10 files an
        #    institution reports in the old categories, the new ones, or partly in both (the shares of both sets with
        #    UGDS_NRA and UGDS_UNKN add up to 1), with 0.0 in the set it does not use. Each share becomes the sum of
        #    its new and old category; NHPI and 2MOR (new categories only) are missing where only old ones are used.
        old_columns = list(OLD_RACE.values())
        old_only = df[old_columns].fillna(0).sum(axis=1).gt(0) & df[NEW_RACE].fillna(0).sum(axis=1).eq(0)
        for new, old in OLD_RACE.items():
            df[new] = df[[new, old]].sum(axis=1, min_count=1)
        df.loc[old_only, ["UGDS_NHPI", "UGDS_2MOR"]] = np.nan
        df = drop_columns(df, old_columns)
        # 5. Codes to labels; ADMCON7's -1 (not reported) and -2 (not applicable) become missing.
        for column, labels in LABELS.items():
            df[column] = to_labels(df[column], labels, missing=TO_MISSING.get(column, ()))
        # 6. Target, and the identifier and the cohort count (from the outcome file) out.
        df = df.rename(columns={"C150_4": self.target})
        return drop_columns(df, ["UNITID", "D150_4"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # MAIN and DISTANCEONLY are 0/1 flags (CLEAN-14)
        return FeatureTypes(categorical=["STABBR", *LABELS, "MAIN", "DISTANCEONLY"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        rows = cohort_rows(raw)
        rows = rows[rows["D150_4"] >= MIN_COHORT_SIZE]
        time = df[self.temporal.on]
        seen, carried = [], []
        for folds in self.temporal.splits.splits(df, self.temporal.on).values():
            train, test = folds[0]
            cohort, last_train = int(time.iloc[test].max()), int(time.iloc[train].max())
            group = rows[rows["cohort_year"] == cohort]
            train_ids = set(rows.loc[rows["cohort_year"] <= last_train, "UNITID"])
            seen.append(
                {
                    "test cohort": cohort,
                    "train cohorts": f"{int(time.iloc[train].min())}-{last_train}",
                    "test rows": len(group),
                    "test institutions with a train cohort": f"{group['UNITID'].isin(train_ids).mean():.1%}",
                }
            )
            # carry-forward: the latest published rate through a line fit on the train side (train mean if missing)
            fit, held = df.iloc[train], df.iloc[test]
            known = fit[LATEST_RATE].notna()
            slope, intercept = np.polyfit(fit.loc[known, LATEST_RATE], fit.loc[known, self.target], 1)
            guess = (intercept + slope * held[LATEST_RATE]).fillna(fit[self.target].mean())
            residual = ((held[self.target] - guess) ** 2).sum()
            total = ((held[self.target] - held[self.target].mean()) ** 2).sum()
            carried.append(
                {
                    "test cohort": cohort,
                    "with a published rate": f"{held[LATEST_RATE].notna().mean():.1%}",
                    "R² of the carried-forward rate": round(1 - residual / total, 3),
                }
            )
        return [
            Decision(
                "Temporal split by entering cohort, not grouped by institution",
                "A model is used on the next entering cohorts of institutions it has seen; train holds every cohort "
                "whose completion rate was published when the test cohort entered (six or more years older).",
                pd.DataFrame(seen),
            ),
            Decision(
                "The institution's latest published completion and retention rates are features",
                "Both are published in the entry-year file, so a user has them at the prediction point. The latest "
                "completion rate, carried forward through a line fit on the train side, is the baseline to beat "
                "(table); untuned LightGBM on all features beats it on every window.",
                pd.DataFrame(carried),
            ),
        ]
