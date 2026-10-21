"""Curated dataset definition for `bioresponse` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class Bioresponse(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a molecule produce the biological response that the company's assay measures?",
        use_case=(
            "For example, a medicinal chemist at Boehringer Ingelheim screens candidate molecules on properties "
            "computed from their structure and decides which to synthesize and test in the lab."
        ),
        row=("One molecule tested by Boehringer Ingelheim (3,751 molecules, released for a 2012 Kaggle competition)."),
        predicted=(
            "Whether the molecule elicited the response (54% did); the source names neither the response nor the assay."
        ),
        known=(
            "1,776 numbers computed from the molecule's structure (descriptors of size, shape, elemental make-up and "
            "the like), already normalised and with hidden names."
        ),
        split=(
            "Random molecules, so the test data stands for new candidates; close analogues of a test molecule can be "
            "in training, as no structure is given to group them."
        ),
        fit="direct",
        fit_reason=(
            "The descriptors come from the structure alone, which is all a chemist has before synthesis. Without "
            "structures the split cannot keep a chemical series together, so scores may be higher than on a truly new"
            " series."
        ),
    )

    # Dataset
    unique_name = "bioresponse"
    year = "2012"
    domain = "chemistry & material science"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/c/bioresponse"
    license = "Public Domain"
    download_description = """
        We download the data from Kaggle and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/bioresponse && cd local-data-warehouse/bioresponse && kaggle competitions download -c bioresponse && unzip bioresponse.zip && rm bioresponse.zip
    """
    bibtex = """
        @misc{bioresponse2012hamner,
            author = {Ben Hamner and dcthompson and Jorg},
            title = {Predicting a Biological Response},
            year = {2012},
            howpublished = {https://kaggle.com/competitions/bioresponse},
            note = {Kaggle}
        }
    """
    curation_comments = """
        - We changed the name of the target and mapped it to yes/no
        - Anomaly: Only train data is used, since test data is empty for target
        - Potential leak, kept on purpose: the 941 non-binary descriptors are min-max scaled over Kaggle's train and test molecules (each is exactly 0 and 1 over the 6,252 of both files, only 609 of them over the 3,751 rows we ship), so the scaling includes our test folds; no unscaled descriptors are published. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if raw descriptors appear.
        - Metric: the competition scored log loss (Kaggle's evaluation metric for bioresponse), which we declare (TP-6).
    """

    # Task
    target = "MoleculeElicitsResponse"
    problem_type = "binary_classification"
    metric = "log_loss"  # the competition's metric

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.rename(columns={"Activity": "MoleculeElicitsResponse"})
        df["MoleculeElicitsResponse"] = df["MoleculeElicitsResponse"].map({0: "No", 1: "Yes"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # 0/1 flags (features holding only 0 and 1, plus missing values) are categorical (CLEAN-14)
        flags = [
            c
            for c in df.columns.drop(self.target)
            if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() == 2 and df[c].dropna().isin([0, 1]).all()
        ]
        return FeatureTypes(categorical=flags)
