"""Curated dataset definition for `breast_cancer_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from data_foundry.definition import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    TimeBasis,
    decode,
    drop_columns,
)

TARGET = "cancer_within_one_year"

# The BCSC codebook ("Digital Mammography Dataset Documentation"): source name -> our name.
RENAME = {
    "age_c": "age",
    "assess_c": "birads_assessment",
    "cancer_c": TARGET,
    "compfilm_c": "comparison_mammogram_available",
    "density_c": "birads_breast_density",
    "famhx_c": "family_history_breast_cancer",
    "hrt_c": "current_hormone_therapy",
    "prvmam_c": "prior_mammogram",
    "biophx_c": "prior_breast_biopsy",
    "mammtype": "mammogram_type",
    "CaTypeO": "cancer_type",
    "bmi_c": "bmi",
    "ptid": "patient_id",
}
ASSESSMENT = {  # the codebook's labels with the BI-RADS category number, as radiology reports name them
    0: "0: Needs additional imaging",
    1: "1: Negative",
    2: "2: Benign finding(s)",
    3: "3: Probably benign",
    4: "4: Suspicious abnormality",
    5: "5: Highly suggestive of malignancy",
}
YES_NO_MISSING = [  # 0 = no, 1 = yes, 9 = missing
    "comparison_mammogram_available",
    "family_history_breast_cancer",
    "current_hormone_therapy",
    "prior_mammogram",
    "prior_breast_biopsy",
]


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "birads_breast_density": [
        "almost entirely fatty",
        "scattered fibroglandular densities",
        "heterogeneously dense",
        "extremely dense",
    ],
}


# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "birads_breast_density": {
        "1": "almost entirely fatty",
        "2": "scattered fibroglandular densities",
        "3": "heterogeneously dense",
        "4": "extremely dense",
    },
}


class BreastCancerPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a woman who comes for a screening mammogram be diagnosed with breast cancer within a year, judged "
            "from her risk factors and her breast density, before the radiologist assesses the mammogram?"
        ),
        use_case=(
            "At a woman's screening visit, a screening programme of the Breast Cancer Surveillance Consortium "
            "estimates her short-term breast cancer risk from her risk factors and her breast density, to tailor "
            "screening and prevention."
        ),
        row=(
            "One screening mammogram of a woman aged 60 to 89 in the US Breast Cancer Surveillance Consortium, 2005 "
            "to 2008: each of 36,714 women once, with her earliest exam in the sample."
        ),
        predicted=(
            "Whether breast cancer (in situ or invasive) is diagnosed within one year after the exam; 0.65% of the "
            "women."
        ),
        known=(
            "Age, BMI, family history, earlier biopsy and mammogram, hormone therapy, whether an earlier mammogram "
            "was at hand for comparison, film or digital imaging, and the breast density the radiologist records from "
            "this mammogram; not the radiologist's assessment of it."
        ),
        split=(
            "Random folds over the women: every row is a different woman, so the test data stands for other women's "
            "exams."
        ),
        changes=(
            "We drop the cancer type, which is recorded at diagnosis and encodes the label, and the radiologist's "
            "assessment, the follow-up decision through which most cancers are found; we keep one exam per woman, "
            "her earliest (3,133 women have 2 to 4)."
        ),
        fit="approximate",
        fit_reason=(
            "The task of the BCSC's risk models, before the read. Two gaps: the one-year label, mostly this screen's "
            "own detections, stands in for the longer invasive risk that prevention decides on; and density read "
            "from this mammogram stands in for the prior exam's."
        ),
    )

    # Dataset
    unique_name = "breast_cancer_prediction"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="GOV Website",
            url="https://www.bcsc-research.org/index.php/datasets/mammography_dataset",
            license="BCSC data terms: download after registration, citation of the BCSC required, 'recommended for use as a "
            "teaching tool only; they should not be used to conduct primary research'; no licence named "
            "(the Kaggle mirror states CC0-1.0)",
            year="2014",
            bibtex="""
                @misc{bcsc2014digitalmammography,
                  author = {{Breast Cancer Surveillance Consortium}},
                  title = {Digital Mammography Dataset},
                  year = {2014},
                  howpublished = {\\url{https://www.bcsc-research.org/index.php/datasets/mammography_dataset}},
                  note = {The Breast Cancer Surveillance Consortium and its data collection and sharing activities are funded
                    by the National Cancer Institute (P01CA154292). Downloaded 10/07/2026 from the Breast Cancer Surveillance
                    Consortium Web site - \\url{http://www.bcsc-research.org/}. Data collection and sharing was supported by
                    the National Cancer Institute-funded Breast Cancer Surveillance Consortium (HHSN261201100031C)}
                }
            """,
        ),
    )
    download_description = """
        The Breast Cancer Surveillance Consortium distributes the BCSC Digital Mammography Dataset after a
        registration form (name, institution, e-mail, captcha) at
        https://www.bcsc-research.org/index.php/datasets/mammography_dataset (until 2016 at breastscreening.cancer.gov,
        behind a password). The download page that follows the form links a zip
        (sha256 182efaa16c8cbf7498ade7d8c3fc88532d0558be195c7b9be164238129d3f072) that holds one file, `dataset.csv`
        (dated 2014-06-04, 40,000 rows, sha256 5f7378e765aeabad4fbdb2224167ff90729d8b0349af9858bd7d2fcdcedb8c90,
        CRLF line ends). We store it as `mammography.csv`:

        mkdir -p local-data-warehouse/breast_cancer_prediction
        unzip -p <the downloaded zip> dataset.csv > local-data-warehouse/breast_cancer_prediction/mammography.csv

        A byte-identical copy (same sha256) is on GitHub, pinned to a commit, for a download without the form:

        wget -O local-data-warehouse/breast_cancer_prediction/mammography.csv https://raw.githubusercontent.com/lintai666/mammography/2f35ca3b97871743112ebc07097ea9f0d19c45da/mammography.csv

        The Kaggle and OpenML copies (kaggle datasets download haithemhermessi/breast-cancer-screening-data-set;
        OpenML 43687, via a JohnSnowLabs re-upload) hold the same rows with decoded labels and without the two exact
        duplicate rows: after `_clean`'s duplicate drop, all 39,998 rows match.
    """
    curation_comments = """
        We start with the BCSC Digital Mammography Dataset (`mammography.csv`, 40,000 rows) from the Breast Cancer Surveillance Consortium: a random sample of 20,000 digital and 20,000 film screening mammograms of women aged 60-89, January 2005 to December 2008.

        - Prediction point: the woman comes for her screening mammogram; the intake answers, the exam facts and the breast density the radiologist records from this mammogram are known; the radiologist's assessment of it is not (review issue 2, B, Andrej 2026-11-27). This is the task of the BCSC's risk models (Barlow et al. 2006), the same question as `bcsc_risk_estimation` on other exams (2005-2008 against 1996-2002), other inputs and a far smaller sample. The source's own example question (a model 'using patient characteristics and mammography assessment') is a teaching exercise on the read's accuracy.
        - Target: `cancer_c` as `cancer_within_one_year` (Yes / No), a breast cancer diagnosis (DCIS or invasive) within one year after the exam: 239 cancers in 36,714 women (0.65%). We drop `CaTypeO` (cancer type), which is recorded at the diagnosis and encodes the label (8 = no cancer).
        - The BI-RADS assessment is dropped: it is the follow-up decision (0 more imaging, 4-5 biopsy, 1-2 routine screening), and the cancers are found through it, so as a feature it made the score the read's accuracy (ROC AUC 0.914 alone, 0.93 with the models). Women read 0, 4 or 5 (8%) hold 87% of the cancers.
        - Without the assessment the signal is modest: logistic regression ROC AUC 0.606, LightGBM 0.563 (one exam per woman, 3 x 3 folds, 2026-11-27; the untuned task probe: linear 0.580, ahead of the dummy on every split, LightGBM and random forest 0.544); the BCSC's published risk model reaches a c statistic of 0.62-0.63 on 2.4M exams.
        - `birads_breast_density` 1-4 stays numeric, since the order is the meaning (1 almost entirely fatty, 4 extremely dense).
        - The codebook's 9 = missing in the five yes/no answers and -99 = missing in `bmi` become NaN. `mammogram_type` 1 and 2 become film and digital. `RENAME` maps the codebook names to ours.
        - One exam per woman, her earliest in the sample (lowest age; two age ties keep the file's order), so the folds are IID (Lennart, 2026-10-15): 3,133 of the 36,714 women contribute 2-4 exams, and the use case is one woman's screening read. The 20 women with cancer and several exams are positive only on their last exam, so 20 of the 259 cancers go. Untuned LightGBM scores alike either way (ROC AUC 0.928 earliest exam, 0.923 latest, 0.925 all exams grouped by woman). The file's two exact copies go with it.
        - Duplicates: repeated feature vectors (52.2% of the rows, the `dataset_duplicate_rows` warning) stay: the features are coarse, and these are different women with the same profile (49.6% of the test rows have a copy in train), whose outcomes are independent.
        - Anomaly: the BCSC recommends the data "for use as a teaching tool only; they should not be used to conduct primary research". We use it to compare learning methods, not to estimate clinical effects.
        - Ordinal scales (2026-10-30, the curator's decisions of 2026-10-31 and 2026-11-01, CLEAN-14): 2 columns are ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); 1 of them decoded from the source's codes
          into its words (`CODE_LABELS`, 2026-11-01); 1 hold a state outside the scale, placed by the curator's rule
          (missing when the column has no other missing value, else the lowest level; a state that is simply not on the
          scale, such as Other, is missing); codes that mean unknown are missing (CLEAN-10).
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 1 ordered codes carry their codebook's
          words (`CODE_LABELS`), in the same order.
    """
    split_leaf = "L-FORCED.random"
    time_basis = TimeBasis(
        "ForcedIIDFromTemporal",
        """
        the screening exams were collected over time, and the file carries no exam
        date, so the time is lost. A dated release would test exams later than those used for training. Not taken as
        stationary (Andrej, 2026-11-18): The main feature is a reading that technology and BI-RADS coding changed;
        changed coding is a fact against.
        """,
    )

    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Each row is a different woman (one exam per woman); the nine features are coarse (age in years, BI-RADS "
            "categories, yes/no answers), so many women share a profile; their outcomes are independent, so a copy "
            "in train tells nothing about the test woman beyond her profile."
        ),
    }

    # Task
    target = TARGET
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="The BCSC page poses the question (predict any cancer from patient characteristics and the mammography assessment) but names no metric; it suggests the data for 'statistical methods for binary outcomes'.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "mammography.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.rename(columns=RENAME)
        # One exam per woman, her earliest in the sample (lowest age; ties keep the file's order): the use case is a
        # woman's screening read, and 91.5% of the women have one exam. This also drops the file's two exact copies.
        df = df.sort_values(["patient_id", "age"], kind="stable").drop_duplicates("patient_id", keep="first")
        df = drop_columns(df, ["patient_id"])
        # cancer type is recorded at the diagnosis: 8 = no cancer, so it encodes the label
        df = drop_columns(df, ["cancer_type"])
        df[TARGET] = df[TARGET].map({0: "No", 1: "Yes"})
        # the radiologist's assessment is the follow-up decision, and most cancers are found through it (review
        # issue 2, B, Andrej 2026-11-27): the task is the risk before it
        df = drop_columns(df, ["birads_assessment"])
        df["mammogram_type"] = df["mammogram_type"].map({1: "film", 2: "digital"})
        # codebook sentinels: 9 = missing for the yes/no answers, -99 for BMI
        df[YES_NO_MISSING] = df[YES_NO_MISSING].replace(9, np.nan)
        df["bmi"] = df["bmi"].replace(-99, np.nan)
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # 0/1 flags are categorical (CLEAN-14)
        flags = [
            "comparison_mammogram_available",
            "current_hormone_therapy",
            "prior_breast_biopsy",
            "prior_mammogram",
            "family_history_breast_cancer",
        ]
        return FeatureTypes(ordinal=ORDINAL_LEVELS, categorical=["mammogram_type", *flags])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        women = raw.rename(columns=RENAME).sort_values(["patient_id", "age"], kind="stable")
        women = women.drop_duplicates("patient_id", keep="first")
        by_assessment = (
            women.assign(birads_assessment=women["birads_assessment"].map(ASSESSMENT))
            .groupby("birads_assessment")[TARGET]
            .agg(women="size", cancers="sum")
            .assign(share_of_cancers=lambda t: (t["cancers"] / t["cancers"].sum()).round(3))
            .reindex(list(ASSESSMENT.values()))  # BI-RADS 0 to 5
        )
        exams = raw.rename(columns=RENAME).drop_duplicates()
        exams["cancer"] = exams[TARGET].eq(1)
        exams["earliest"] = exams["age"].eq(exams.groupby("patient_id")["age"].transform("min"))
        by_count = (
            exams.groupby("patient_id")
            .agg(
                exams=("cancer", "size"),
                cancers=("cancer", "sum"),
                cancer_on_earliest=("cancer", lambda c: bool(c[exams.loc[c.index, "earliest"]].any())),
            )
            .groupby("exams")
            .agg(
                women=("cancers", "size"),
                women_with_cancer=("cancers", lambda c: int((c > 0).sum())),
                cancer_on_the_earliest_exam=("cancer_on_earliest", "sum"),
            )
        )
        return [
            Decision(
                "The radiologist's assessment is dropped",
                "It is the follow-up decision: 0 sends a woman to more imaging, 4-5 to a biopsy, 1-2 back to routine "
                "screening, and the cancers are found through it (assessments 0, 4 and 5 hold most of them). As a "
                "feature it made the task the read's own accuracy (ROC AUC 0.91 alone); the task is the risk before "
                "it (review issue 2, B). Women by the dropped assessment, one exam each.",
                by_assessment,
            ),
            Decision(
                "One exam per woman, her earliest",
                "Some women contribute several exams. Each woman counts once, with her earliest exam in the sample, "
                "so the folds are IID; the women with cancer and several exams are positive only on their last exam, "
                "so their cancers are not in the data. Women by number of exams in the file.",
                by_count,
            ),
        ]
