"""Curated dataset definition for `breast_cancer_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, drop_columns

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


class BreastCancerPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "breast_cancer_prediction"
    year = "2014"
    domain = "medical & healthcare"
    source = "GOV Website"
    source_url = "https://www.bcsc-research.org/index.php/datasets/mammography_dataset"
    license = (
        "BCSC data terms: download after registration, citation of the BCSC required, 'recommended for use as a "
        "teaching tool only; they should not be used to conduct primary research'; no licence named "
        "(the Kaggle mirror states CC0-1.0)"
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
    bibtex = """
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
    """
    curation_comments = """
        We start with the BCSC Digital Mammography Dataset (`mammography.csv`, 40,000 rows) from the Breast Cancer Surveillance Consortium: a random sample of 20,000 digital and 20,000 film screening mammograms of women aged 60-89, January 2005 to December 2008.

        - Prediction point: the screening mammogram has just been read, so the radiologist's BI-RADS assessment and density, the intake answers and the exam facts are known. This is the source's own question (BCSC exam question 4): a model "to predict occurrence of any cancer using patient characteristics and mammography assessment".
        - Target: `cancer_c` as `cancer_within_one_year` (Yes / No), a breast cancer diagnosis (DCIS or invasive) within one year after the exam: 259 cancers in 39,998 exams (0.65%). We drop `CaTypeO` (cancer type), which is recorded at the diagnosis and encodes the label (8 = no cancer).
        - The BI-RADS assessment stays a feature: the radiologist gives it at the exam, and the source's question uses it as a predictor. It is categorical because assessment 0 (needs additional imaging) is a positive screen; its values are the codebook's labels prefixed with the BI-RADS number ("4: Suspicious abnormality").
        - The assessment carries most of the signal (task probe flag `one_feature`, decision table): alone it reaches ROC AUC 0.907. We keep it as the core of the task, and the task is not `Trivial`: regularised LightGBM, CatBoost and a random forest beat it on 9 of 9 splits, by 0.019-0.023 (task_probes.md, rule 4).
        - `birads_breast_density` 1-4 stays numeric, since the order is the meaning (1 almost entirely fatty, 4 extremely dense).
        - The codebook's 9 = missing in the five yes/no answers and -99 = missing in `bmi` become NaN. `mammogram_type` 1 and 2 become film and digital. `RENAME` maps the codebook names to ours.
        - Duplicates: we drop the second of two exact copies, the woman's id included (`ptid` 19408 and 34035), as the Kaggle and OpenML copies did. The other repeated feature vectors (52.8% of the exams) stay: the features are coarse, and these are different women with the same profile.
        - Grouped by woman (`patient_id`, the BCSC's `ptid`): 3,133 of the 36,714 women contribute 2-4 exams. Rows are no closer to their own woman than chance (`groups_not_clustered`), so the use case decides: the model is used for other women (Grouping definition). Each label belongs to its exam: the 20 women with cancer and several exams have only their last exam positive.
        - Anomaly: the BCSC recommends the data "for use as a teaching tool only; they should not be used to conduct primary research". We use it to compare learning methods, not to estimate clinical effects.
    """

    accepted_check_warnings = {
        "dataset_pure_feature_value": (
            "BI-RADS 1 (Negative: 26,031 exams, 20 cancers), BI-RADS 2 (Benign finding(s): 10,717, 12) and density 1 "
            "(almost entirely fatty: 5,429) are the low-risk results of the screening read, given at the exam before "
            "the outcome; at a 99.35% base rate of no cancer they are ordinary category effects, not a leak."
        ),
        "groups_labels_constant": (
            "Labels are per exam by construction (a cancer diagnosis within one year of that exam). The 20 women with "
            "two labels are the 20 women with cancer and several exams, each with only her last exam positive; the "
            "other 3,113 women with several exams had no cancer."
        ),
    }

    # Task
    target = TARGET
    problem_type = "binary_classification"
    grouping = Grouping(
        on="patient_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a woman, identified by the BCSC's patient study id (`ptid`). The source says "Some women contribute multiple examinations to the data" and offers the data for "statistical methods for binary outcomes or correlated data" (BCSC, Digital Mammography Dataset page); its exam question adds that women "are recommended to undergo mammography screening annually or biennially, so some women have multiple mammograms included in the data set". 3,133 of the 36,714 women have 2-4 exams. The 40,000 exams are a random sample of the BCSC's screening mammograms, so a model built on them is used for the exams of other women: the test women are new. Each exam is one prediction, made from that exam alone.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "mammography.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.rename(columns=RENAME)
        # two exact copies, the woman's id included; the Kaggle and OpenML copies drop them too
        df = df.drop_duplicates(keep="first")
        # cancer type is recorded at the diagnosis: 8 = no cancer, so it encodes the label
        df = drop_columns(df, ["cancer_type"])
        df[TARGET] = df[TARGET].map({0: "No", 1: "Yes"})
        df["birads_assessment"] = df["birads_assessment"].map(ASSESSMENT)
        df["mammogram_type"] = df["mammogram_type"].map({1: "film", 2: "digital"})
        # codebook sentinels: 9 = missing for the yes/no answers, -99 for BMI
        df[YES_NO_MISSING] = df[YES_NO_MISSING].replace(9, np.nan)
        df["bmi"] = df["bmi"].replace(-99, np.nan)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["birads_assessment", "mammogram_type"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del raw
        by_assessment = (
            df.groupby("birads_assessment", observed=True)[TARGET]
            .agg(exams="size", cancers=lambda s: int((s == "Yes").sum()))
            .assign(cancer_rate=lambda t: (t["cancers"] / t["exams"]).round(4))
            .reindex(list(ASSESSMENT.values()))  # BI-RADS 0 to 5
        )
        exams = df.groupby("patient_id").size()
        cancers = df[TARGET].eq("Yes").groupby(df["patient_id"]).sum()
        by_count = (
            pd.DataFrame({"exams": exams, "cancers": cancers})
            .groupby("exams")
            .agg(women=("cancers", "size"), women_with_cancer=("cancers", lambda s: int((s > 0).sum())))
        )
        return [
            Decision(
                "The radiologist's assessment is a feature and carries most of the signal",
                "It is given at the exam, and the source asks for a model 'using patient characteristics and "
                "mammography assessment'. Assessments 0, 4 and 5 are the positive screens (recall).",
                by_assessment,
            ),
            Decision(
                "Grouped by woman",
                "Some women contribute several exams; the model is used for women outside the sample, and each "
                "woman with cancer has one positive exam, her last.",
                by_count,
            ),
        ]
