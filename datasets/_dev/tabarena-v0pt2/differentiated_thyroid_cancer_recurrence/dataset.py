"""Curated dataset definition for `differentiated_thyroid_cancer_recurrence` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns


class DifferentiatedThyroidCancerRecurrence(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a patient's thyroid cancer come back after surgery?",
        use_case=(
            "After thyroid surgery, at the initial staging visit, the endocrinologist estimates the risk of recurrence"
            " to decide on radioiodine therapy, the target level of thyroid-stimulating hormone and the initial "
            "follow-up schedule."
        ),
        row=(
            "One patient with well-differentiated thyroid cancer after thyroid removal in Hamadan, Iran (383 "
            "patients); the source states at least 10 years of follow-up."
        ),
        predicted=(
            "Whether the cancer recurred during follow-up (28% did); the label seems to count persistent disease as "
            "well."
        ),
        known=(
            "Age, sex, smoking, thyroid function, examination findings, swollen lymph nodes, the tumour's pathology "
            "and focality, its T, N and M stage and overall stage, and the initial risk class of the American Thyroid"
            " Association."
        ),
        split="Random patients, so the test data stands for new patients of the same clinic.",
        changes=(
            "We drop the response to therapy, assessed in the first two years of follow-up and partly the outcome "
            "itself, and an undefined, undated radiotherapy column."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs are those of the initial staging, but the label is not verified: recurrence seems to include "
            "persistent disease, and the stated follow-up (at least 10 years) conflicts with the cohort period "
            "(2008-2023). A few distant metastases found after staging are kept as a potential leak, and one clinic's "
            "patients make a small task."
        ),
    )

    # Dataset
    unique_name = "differentiated_thyroid_cancer_recurrence"
    year = "2023"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5632J"
    license = "CC BY 4.0"
    download_description = """
        We download the data from UCI (dataset 915, donated by the authors; the zip holds one file, Thyroid_Diff.csv,
        sha256 a2c65f7c8fa0e78a65aa4946961aafd45218c92760d10375fe2c778045c97b44). OpenML 46605 is a 2025 re-upload
        of the same 383 rows.

        mkdir -p local-data-warehouse/differentiated_thyroid_cancer_recurrence && wget -P local-data-warehouse/differentiated_thyroid_cancer_recurrence/ https://archive.ics.uci.edu/static/public/915/differentiated+thyroid+cancer+recurrence.zip && unzip local-data-warehouse/differentiated_thyroid_cancer_recurrence/differentiated+thyroid+cancer+recurrence.zip -d local-data-warehouse/differentiated_thyroid_cancer_recurrence/
    """
    bibtex = """
        @article{borzooei2024machine,
          title={Machine learning for risk stratification of thyroid cancer patients: a 15-year cohort study},
          author={Borzooei, Shiva and Briganti, Giovanni and Golparian, Mitra and Lechien, Jerome R and Tarokhian, Aidin},
          journal={European Archives of Oto-Rhino-Laryngology},
          volume={281},
          number={4},
          pages={2095--2104},
          year={2024},
          publisher={Springer},
          doi={10.1007/s00405-023-08299-w}
        }
    """
    curation_comments = """
        We start with Thyroid_Diff.csv from UCI: 383 patients with well-differentiated thyroid cancer followed after thyroidectomy in Hamadan, Iran; the source states at least 10 years of follow-up.

        - Prediction point: after initial therapy, at the initial staging, when the ATA risk of recurrence is assigned. The model predicts recurrence during follow-up; the 14 kept features describe the patient and the tumour at diagnosis and surgery.
        - We drop `Response`, the response to therapy. It is assessed during the first 2 years of follow-up (Tuttle et al. 2010), after the prediction point, and its structural incomplete category, "persistent or newly identified loco-regional or distant metastases" (ATA 2015), is the outcome itself (decision table).
        - We drop `Hx Radiothreapy` ("Yes" for 7 patients). No source defines or dates it, and 6 of the 7 are ATA high-risk men with advanced disease who all recurred, which fits radiotherapy given after the prediction point (decision table).
        - We rename the pathology value "Hurthel cell" to "Hurthle cell" (source typo).
        - `Age` is numeric and every other feature categorical.
        - Note: no source gives the meaning of `Hx Smoking`; it is probably former smoking, since 37 current smokers have `Hx Smoking` = No.
        - Duplicates: we keep the 26 rows (6.8%) that copy another row. The file's 383 rows are the paper's 383 patients, so the copies are distinct patients with the same coarse record: women with an ATA low-risk tumour who did not recur, 44 of the 48 rows in duplicate groups in the five most common profiles. Permuting `Age` within ATA risk and sex gives about as many by chance (23.2 duplicate feature vectors against 27). One profile of three patients carries both labels; we keep all three, as different patients with the same coarse record whose outcomes differ, a label ambiguity the task has (LEAK-20).
        - IID split over patients.
        - Anomaly: `Stage` differs from the AJCC 8th edition stage computed from `Age`, `T`, `N` and `M` in 12 of 383 rows. We keep it as recorded.
        - Potential leak, kept on purpose: 2 of the 18 patients with M1 are ATA intermediate risk, although distant metastases are ATA high risk, so their metastases may have been found after the initial staging. Dropping `M` and `Stage` changes the ROC AUC by +0.001. `M` stays, unlike the radiotherapy column: it is a defined staging field and only 2 of its 18 M1 values are doubtful, while the radiotherapy column has no definition or date and 6 of its 7 positives look like treatment of advanced disease. Revisit when the paper's variable definitions are read.
        - Potential leak, kept on purpose: `Risk` was probably assigned from the records with the follow-up known. A crude ATA rule from `T`, `N`, `M` and `Adenopathy` agrees with it in 337 of 383 rows, and the discordant rows are not pushed toward the outcome (33% and 24% recurred, against 28% where the rule agrees); `Risk` adds at most 0.010 ROC AUC over the other columns. It stays as the clinician's own estimate, which the model refines.
        - Note: the label seems to count persistent disease as recurrence; the paper is behind a paywall. Recurrence is 4.8%, 62.7% and 100% in ATA low, intermediate and high risk, against about 3%, 21% and 68% of persistent or recurrent structural disease in Tuttle et al. 2010, and all 18 patients with M1 recurred. The task is valid either way, as the ATA initial risk estimates "the risk of persistent/recurrent disease" (ATA 2015).
        - Note: all 34 patients with ATA high risk or M1 recurred; if the label counts persistent disease, they may have the outcome at staging, a cohort question (LEAK-36). On 20 x 3 stratified folds, logistic regression gives ROC AUC 0.928 on all test rows and 0.901 without the High/M1 test rows (`Risk` alone 0.896 and 0.850). Leaving out as many other positives that the model ranks highest also gives 0.901, so the drop shows how hard the remaining rows are, not a leak. We keep the rows until the paper's cohort is known.
        - Note: the source states at least 10 years of follow-up, but the cohort paper gives the period January 2008 to December 2023 (Khazaei et al. 2024), so the labels of the later patients may be censored. Without dates this cannot be tested.
        - Note: the record's `Trivial` marker came from the paper's ROC AUC 0.984-0.997 on all features combined. Here the ATA risk alone gives 0.896 on the 60 shipped splits; a random forest beats it on 59 of 60 (mean gain 0.032), unscaled logistic regression on 59 and untuned CatBoost on 60, and standardised logistic regression on 52.
    """

    # Task
    target = "Recurred"
    problem_type = "binary_classification"
    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Kept on purpose: the 383 rows are the paper's 383 patients, and the 26 copies (22 profiles) are women with "
            "an ATA low-risk tumour who did not recur, 44 of the 48 rows in duplicate groups in the five most common "
            "profiles of 14 coarse clinical fields. Permuting age within risk and sex gives 23 duplicate feature vectors "
            "by chance (95% range 16-30) against 27 observed, and leaving the copied test rows out lowers the ROC AUC "
            "by 0.002-0.008 on the 60 shipped splits."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Thyroid_Diff.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # typo in the source
        df["Pathology"] = df["Pathology"].replace({"Hurthel cell": "Hurthle cell"})
        # the response to therapy is assessed during the first 2 years of follow-up, after the prediction point, and
        # its structural incomplete category is persistent or new metastatic disease, the outcome itself; no source
        # defines or dates the radiotherapy column, and its "Yes" rows look like treatment of advanced disease
        df = drop_columns(df, ["Response", "Hx Radiothreapy"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[c for c in df.columns if c not in ("Age", self.target)])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        recurred = raw["Recurred"].eq("Yes")
        by_response = recurred.groupby(raw["Response"]).agg(patients="size", recurred="sum")
        by_response["share_recurred"] = (by_response["recurred"] / by_response["patients"]).round(3)

        radiotherapy = raw.groupby("Hx Radiothreapy").agg(
            patients=("Recurred", "size"),
            recurred=("Recurred", lambda s: int(s.eq("Yes").sum())),
            ata_high_risk=("Risk", lambda s: int(s.eq("High").sum())),
            distant_metastases=("M", lambda s: int(s.eq("M1").sum())),
            men=("Gender", lambda s: int(s.eq("M").sum())),
            median_age=("Age", "median"),
        )

        copies = df.duplicated(keep=False)
        features = [c for c in df.columns if c != self.target]
        duplicates = pd.Series(
            {
                "rows": len(df),
                "exact duplicate rows in the raw file (Response included)": int(raw.duplicated().sum()),
                "exact duplicate rows of the curated frame (copies beyond the first)": int(df.duplicated().sum()),
                "rows in these duplicate groups": int(copies.sum()),
                "of these labelled recurred": int(df.loc[copies, self.target].eq("Yes").sum()),
                "of these ATA low risk": int(df.loc[copies, "Risk"].eq("Low").sum()),
                "rows whose features occur with both labels": int(
                    df.groupby(features, observed=True)[self.target].transform("nunique").gt(1).sum()
                ),
            },
            name="count",
        )
        return [
            Decision(
                "Response to therapy dropped",
                "It is assessed during the first 2 years of follow-up, after the initial staging at which the task "
                "predicts, and a structural incomplete response is persistent or new metastatic disease, the outcome "
                "itself (ATA 2015, [B29]).",
                by_response,
            ),
            Decision(
                "Radiotherapy column (Hx Radiothreapy) dropped",
                "No source defines or dates it, and 6 of its 7 'Yes' rows are high-risk men with advanced disease who "
                "all recurred, so it may record treatment given after the prediction point; it adds nothing to the "
                "other columns.",
                radiotherapy,
            ),
            Decision(
                "Duplicate rows kept",
                "The 383 rows are the paper's 383 patients; the copies are women with a low-risk tumour who did not "
                "recur, 44 of the 48 rows in duplicate groups in the five most common profiles of 14 coarse fields. "
                "The one profile with both labels is a label ambiguity the task has (LEAK-20).",
                duplicates,
            ),
        ]
