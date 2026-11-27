"""Curated dataset definition for `bcsc_risk_estimation` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
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

# The BCSC codebook ("Risk Estimation Dataset Documentation", Barlow, August 2006): the columns of risk.txt, which the
# one-exam-per-woman file risk_rand.txt shares (the same 16 whitespace-separated columns and codes).
COLUMNS = [
    "menopaus",
    "agegrp",
    "density",
    "race",
    "hispanic",
    "bmi",
    "agefirst",
    "nrelbc",
    "brstproc",
    "lastmamm",
    "surgmeno",
    "hrt",
    "invasive",
    "cancer",
    "training",
    "count",
]
RENAME = {
    "menopaus": "menopausal_status",
    "agegrp": "age_group",
    "density": "birads_breast_density",
    "race": "race",
    "hispanic": "hispanic",
    "bmi": "bmi_group",
    "agefirst": "age_at_first_birth",
    "nrelbc": "first_degree_relatives_with_breast_cancer",
    "brstproc": "prior_breast_procedure",
    "lastmamm": "last_mammogram_result",
    "surgmeno": "surgical_menopause",
    "hrt": "current_hormone_therapy",
    "cancer": TARGET,
}
# 9 means unknown in every coded column except the age group, where it is the band 75-79 (codebook); density 9
# also covers "different measurement system", surgical menopause and hormone therapy 9 also "not menopausal".
UNKNOWN = 9

# The codebook's words for its codes (CLEAN-12).
CODE_LABELS = {
    "menopausal_status": {"0": "premenopausal", "1": "postmenopausal or age 55 or older"},
    "age_group": {
        "1": "35-39",
        "2": "40-44",
        "3": "45-49",
        "4": "50-54",
        "5": "55-59",
        "6": "60-64",
        "7": "65-69",
        "8": "70-74",
        "9": "75-79",
        "10": "80-84",
    },
    "birads_breast_density": {
        "1": "almost entirely fatty",
        "2": "scattered fibroglandular densities",
        "3": "heterogeneously dense",
        "4": "extremely dense",
    },
    "race": {"1": "white", "2": "Asian or Pacific Islander", "3": "black", "4": "Native American", "5": "other or mixed"},
    "hispanic": {"0": "no", "1": "yes"},
    "bmi_group": {"1": "10-24.99", "2": "25-29.99", "3": "30-34.99", "4": "35 or more"},
    "age_at_first_birth": {"0": "under 30", "1": "30 or older", "2": "nulliparous"},
    "first_degree_relatives_with_breast_cancer": {"0": "0", "1": "1 (or positive, number unknown)", "2": "2 or more"},
    "prior_breast_procedure": {"0": "no", "1": "yes"},
    "last_mammogram_result": {"0": "negative", "1": "false positive"},
    "surgical_menopause": {"0": "natural", "1": "surgical"},
    "current_hormone_therapy": {"0": "no", "1": "yes"},
}
# The ordinal scales, lowest level first, from the codebook.
ORDINAL_LEVELS = {
    "age_group": list(CODE_LABELS["age_group"].values()),
    "birads_breast_density": list(CODE_LABELS["birads_breast_density"].values()),
    "bmi_group": list(CODE_LABELS["bmi_group"].values()),
    "first_degree_relatives_with_breast_cancer": ["0", "1 (or positive, number unknown)", "2 or more"],
}
CATEGORICAL = [c for c in CODE_LABELS if c not in ORDINAL_LEVELS]


class BcscRiskEstimation(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a woman who comes for a screening mammogram be diagnosed with breast cancer within a year, judged "
            "from her risk factors and her breast density, before the radiologist assesses the mammogram?"
        ),
        use_case=(
            "At a woman's screening visit, the screening programmes of the Breast Cancer Surveillance Consortium "
            "estimate the short-term breast cancer risk of their later women from self-reported risk factors, her "
            "breast density and the result of her last mammogram, to tailor screening and prevention (the source's "
            "published risk model)."
        ),
        row=(
            "One screening mammogram of a woman aged 35 to 84 in the US Breast Cancer Surveillance Consortium, 1996 "
            "to 2002, with a mammogram in the five years before: each of 1,007,660 women once."
        ),
        predicted=(
            "Whether breast cancer (in situ or invasive) is diagnosed within one year after the exam; 0.73% of the "
            "women."
        ),
        known=(
            "Age group, menopause and how it came about, race and ethnicity, BMI group, age at first birth, the "
            "number of first-degree relatives with breast cancer, an earlier breast procedure, the result of the "
            "last mammogram, current hormone therapy, and the breast density the radiologist records from this "
            "mammogram; not the radiologist's assessment of it."
        ),
        split="Random folds over the women: every row is a different woman.",
        changes=(
            "We expand the source's aggregated cells by their count, drop `invasive` (part of the target) and the "
            "source's `training` flag (a prescribed random split), and set the code for unknown to missing, except "
            "in the age group, where it is the band 75-79; premenopausal women get a level \"not menopausal\" in "
            "surgical menopause and hormone therapy."
        ),
        fit="approximate",
        fit_reason=(
            "The rows, features and label are those of the source's published risk model (Barlow et al. 2006). Two "
            "gaps: the one-year label, mostly this screen's own detections, stands in for the longer invasive risk "
            "that prevention decides on; and density read from this mammogram stands in for the prior exam's."
        ),
    )

    # Dataset
    unique_name = "bcsc_risk_estimation"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="GOV Website",
            url="https://www.bcsc-research.org/index.php/datasets/rfdataset",
            license=(
                "BCSC data terms: download after registration; citing Barlow et al. 2006 and the BCSC web site is "
                "required; no licence named and no teaching-only clause"
            ),
            year="2006",
            bibtex="""
                @article{barlow2006bcscrisk,
                  author = {Barlow, William E. and White, Emily and Ballard-Barbash, Rachel and Vacek, Pamela M. and
                    Titus-Ernstoff, Linda and Carney, Patricia A. and Tice, Jeffrey A. and Buist, Diana S. M. and
                    Geller, Berta M. and Rosenberg, Robert and Yankaskas, Bonnie C. and Kerlikowske, Karla},
                  title = {Prospective Breast Cancer Risk Prediction Model for Women Undergoing Screening Mammography},
                  journal = {Journal of the National Cancer Institute},
                  volume = {98},
                  number = {17},
                  pages = {1204--1214},
                  year = {2006},
                  doi = {10.1093/jnci/djj331},
                  note = {Data collection and sharing was supported by the National Cancer Institute-funded Breast Cancer
                    Surveillance Consortium (HHSN261201100031C). You can learn more about the BCSC at:
                    \\url{http://www.bcsc-research.org/}.}
                }
            """,
        ),
    )
    download_description = """
        The Breast Cancer Surveillance Consortium distributes the Risk Estimation Dataset after a registration form
        (name, institution, e-mail, captcha) at https://www.bcsc-research.org/index.php/datasets/rfdataset; the page
        that follows the form links both versions as zips:

        - risk_dataset.zip (sha256 f2460ad6ec5b0d765bd4a7b1ec61053cb0657bf1bafa88f40c558d44d89f2e12): `risk.txt`
          (dated 2011-03-17, 280,660 cells, 2,392,998 exams, several per woman; sha256
          256c5710a3b8971fcea952df5bf65edd376bdce4d26375600a3799eec1a938a9);
        - risk_dataset_v2.zip (sha256 7a34f0a282aa3bdaab1f9c54b3ff6c2f8a78015cd7ad3439409e170432821e0a):
          `risk_rand.txt` (dated 2019-01-07, 181,903 cells, 1,007,660 exams, one per woman; sha256
          821b1a1c748cc0935af3e4f6fa392b784fb6527cedb58e91687a91bd10538481), the file we use.

        Both are whitespace-separated with CRLF line ends:

        mkdir -p local-data-warehouse/bcsc_risk_estimation
        unzip -o <risk_dataset_v2.zip> -d local-data-warehouse/bcsc_risk_estimation
        unzip -o <risk_dataset.zip> -d local-data-warehouse/bcsc_risk_estimation   # only for the version comparison
    """
    curation_comments = """
        We start with the BCSC Risk Estimation Dataset, the data of the BCSC's published risk model (Barlow et al. 2006): screening mammograms of 1996-2002 from women aged 35-84 without earlier breast cancer and with a mammogram in the five years before, linked to cancer registries and pathology. The file is aggregated: one row per combination of risk factors and outcome, with a `count`.

        - Prediction point: the woman comes for a screening mammogram; the intake answers, the result of her last mammogram and the breast density the radiologist records from this mammogram are known; the radiologist's assessment of this mammogram is not in the data ("The index mammogram's assessment is not included"). This is the step before `breast_cancer_prediction`, where the read is a feature.
        - Target: `cancer` (invasive or DCIS within one year after the exam), the paper's outcome. `invasive` is a part of it and goes.
        - Version: the one-exam-per-woman file (`risk_rand.txt`, added in August 2012; "All population and other characteristics remain the same"), 1,007,660 women, 7,319 cancers (0.73%). The page does not say how the exam was chosen (the name suggests at random). The all-exams file (`risk.txt`, 2,392,998 exams, 11,638 cancers, 0.49%, the paper's data) has no woman id in its cells, so random folds would put one woman's exams on both sides; it is not used. The cancer share is higher with one exam per woman because women with a cancer leave follow-up at the diagnosis and so contribute fewer exams.
        - `training` (a "75% random sample" for the paper's development, 25% validation; 75.0% in this file too, assignment not described for it) goes: we declare our own folds.
        - Unknown (code 9) becomes missing in every coded column except the age group, where 9 is the band 75-79 (56,233 women, 1.15% cancers) and no code means unknown. Density 9 also covers "different measurement system"; surgical menopause and hormone therapy 9 is "unknown or not menopausal": it holds all 280,205 premenopausal women, which `menopausal_status` tells apart.
        - Density is the radiologist's reading of this mammogram ("judged by the radiologist from the screening mammogram"), recorded before the exam's assessment, which the source leaves out; the BCSC risk calculator takes it as an input. It is worth 0.016 ROC AUC (untuned LightGBM 0.653 with it, 0.638 without). Women with an unknown density or last mammogram result have a 1.2-1.4 times higher cancer share within an age band, a fact fixed at the visit.
        - Surgical menopause and hormone therapy: code 9 becomes "not menopausal" for the 280,205 premenopausal women and stays missing for the others (CLEAN-12). The relatives level 1 also holds a positive family history with the number unknown (codebook), and says so.
        - Metric: ROC AUC is the paper's c statistic, but its 0.631 and 0.624 are per menopausal group; logistic regression gives 0.62-0.63 per group here and 0.649 pooled. AUC does not score calibration, which a clinical user of absolute risk needs.
        - Codes carry the codebook's words (CLEAN-12); age group, density, BMI group and the number of relatives are ordered (CLEAN-14).
        - Repeated feature vectors: every row of a cell is a copy of the others (181,903 cells for 1,007,660 women), as the twelve features are coarse categories; they are different women with independent outcomes.
        - Size: 3 folds give 671,773 training and 335,887 test rows, under the collection's 1M / 500k row budget, so the dataset ships whole (no `_1m` version).
    """
    split_leaf = "L-FORCED.random"
    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "The source ships aggregated cells of twelve coarse categories, expanded by their count: every row of a "
            "cell is a different woman with the same profile (181,903 cells for 1,007,660 women), and their outcomes "
            "are independent, so a copy in train tells nothing about the test woman beyond her profile."
        ),
        "dataset_pure_feature_value": (
            "Premenopausal women, ages 35-44, almost entirely fatty breasts and Native American women are low-risk "
            "groups known at the visit, before the outcome; at a 99.3% base rate of no cancer their 99.6-99.7% are "
            "ordinary category effects (the paper's risk factors), not a leak."
        ),
    }
    time_basis = TimeBasis(
        "ForcedIIDFromTemporal",
        """
        the screening exams were collected from 1996 to 2002, and the file carries no
        dates ("do not include any dates"), so the time is lost. A dated release would test exams later than those
        used for training.
        """,
    )

    # Task
    target = TARGET
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="concordance (c) statistic of the logistic risk models",
        reference="Barlow et al. 2006, J Natl Cancer Inst 98(17):1204-1214",
        definition="Area under the ROC curve of the predicted probability of breast cancer within one year",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "risk_rand.txt", sep=r"\s+", header=None, names=COLUMNS)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # one row per exam: the cells repeated by their count
        df = raw.loc[raw.index.repeat(raw["count"])].reset_index(drop=True)
        df = drop_columns(df, ["count", "training", "invasive"])
        df = df.rename(columns=RENAME)
        coded = [c for c in CODE_LABELS if c != "age_group"]  # age 9 is the band 75-79
        df[coded] = df[coded].replace(UNKNOWN, np.nan)
        df[TARGET] = df[TARGET].map({0: "No", 1: "Yes"})
        df = decode(df, CODE_LABELS)
        # code 9 of these two holds "unknown or not menopausal": premenopausal women get a level of their own (CLEAN-12)
        premenopausal = df["menopausal_status"].eq("premenopausal")
        for col in ["surgical_menopause", "current_hormone_therapy"]:
            df[col] = df[col].astype(object).mask(premenopausal & df[col].isna(), "not menopausal")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(ordinal=ORDINAL_LEVELS, categorical=CATEGORICAL)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        cells = raw.groupby("cancer")["count"].agg(cells="size", exams="sum")
        return [
            Decision(
                "The aggregated cells are expanded by their count",
                "The source ships one row per combination of risk factors and outcome with a `count`, which 'must be "
                "used to obtain correct estimates'. Cells and exams by outcome.",
                cells,
            ),
        ]
