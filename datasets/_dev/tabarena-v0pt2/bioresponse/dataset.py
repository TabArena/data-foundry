"""Curated dataset definition for `bioresponse` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Metric, Source, TaskSummary


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
        fit="approximate",
        fit_reason=(
            "The source names neither the response nor its assay, so what a positive means cannot be checked; without "
            "structures the split cannot hold out a chemical series, so scores may be higher than on a new series."
        ),
    )

    # Dataset
    unique_name = "bioresponse"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/c/bioresponse",
            license="Public Domain",
            year="2012",
            bibtex="""
                @misc{bioresponse2012hamner,
                    author = {Ben Hamner and dcthompson and Jorg},
                    title = {Predicting a Biological Response},
                    year = {2012},
                    howpublished = {https://kaggle.com/competitions/bioresponse},
                    note = {Kaggle}
                }
            """,
        ),
    )
    data_tags = ("Anonymized", "Timeless")
    download_description = """
        We download the data from Kaggle and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/bioresponse && cd local-data-warehouse/bioresponse && kaggle competitions download -c bioresponse && unzip bioresponse.zip && rm bioresponse.zip
    """
    curation_comments = """
        - We changed the name of the target and mapped it to yes/no
        - Anomaly: Only train data is used, since test data is empty for target
        - Potential leak, kept on purpose: the 941 non-binary descriptors are min-max scaled over Kaggle's train and test molecules (each is exactly 0 and 1 over the 6,252 of both files, only 609 of them over the 3,751 rows we ship), so the scaling includes our test folds; no unscaled descriptors are published. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if raw descriptors appear.
        - Time basis: Timeless: the response is a property of the molecule and every descriptor is computed from its
          structure, so nothing in a row arrives later. Boehringer Ingelheim tested the molecules over an unstated
          period and published no date, structure or compound id, so no forward split is possible; the label drifts only
          weakly along the file order (positive share 0.57-0.59 in the first deciles against 0.50-0.51 in the last,
          Spearman -0.04) and the order is not known to follow the assays. Not tested: a new chemical series, as close
          analogues cannot be grouped (nearest-neighbour label agreement 92% in the closest tenth of distances against
          64% in the farthest).
        - Entity leakage, not recoverable (Andrej, 2026-11-11): no two molecules share all 1,776 descriptors and the
          nearest pair differs in 16, so no copy is dropped; close analogues of one series share the label
          (nearest-neighbour agreement 92% in the closest tenth of distances against 64% in the farthest) and cross the
          random split, as no structure or compound id is published to group them. The random split stays: Kaggle's
          own test set looks like a random draw (a model tells its 2,501 molecules from the 3,751 training molecules at
          ROC AUC 0.485, against 0.484-0.497 for a random third of train; nearest-training distances match), and
          scoring new analogues of series already in testing is the lead-optimisation use case the competition framed.
    """

    # Task
    target = "MoleculeElicitsResponse"
    problem_type = "binary_classification"
    metric = Metric.source(
        "log_loss",
        original="Log Loss",
        reference="https://www.kaggle.com/c/bioresponse (Evaluation; Kaggle API evaluationMetric 'Log Loss', per the record's 2026-10-21 assessment)",
        definition="mean binary cross-entropy of the predicted probability that the molecule elicits a response",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.rename(columns={"Activity": "MoleculeElicitsResponse"})
        df["MoleculeElicitsResponse"] = df["MoleculeElicitsResponse"].map({0: "No", 1: "Yes"})
        return df
