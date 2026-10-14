"""Curated dataset definition for `bioresponse` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


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
    domain = "biology & life sciences"
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
    """

    # Task
    target = "MoleculeElicitsResponse"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.rename(columns={"Activity": "MoleculeElicitsResponse"})
        df["MoleculeElicitsResponse"] = df["MoleculeElicitsResponse"].map({0: "No", 1: "Yes"})
        return df
