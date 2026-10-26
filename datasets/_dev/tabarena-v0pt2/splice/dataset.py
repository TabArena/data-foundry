"""Curated dataset definition for `splice` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class Splice(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is the middle of this 60-base stretch of DNA a splice junction, and of which kind?",
        use_case=(
            "For example, a gene-annotation tool scans a primate DNA sequence and marks where exons and introns meet,"
            " to predict how a gene's RNA is spliced."
        ),
        row=("One 60-nucleotide window of primate DNA around a candidate site (3,190 windows, UCI 1992)."),
        predicted=("The site type: exon-to-intron junction (24%), intron-to-exon junction (24%), or neither (52%)."),
        known=(
            "The base at each of the 60 positions, 30 on each side of the site: A, C, G, T or a code for an ambiguous"
            " base."
        ),
        split="Random windows, so the test data stands for other windows of the same collection.",
        fit="approximate",
        fit_reason=(
            "The windows are a curated set in which about half are junctions, a share set by how the examples were "
            "chosen rather than by how often junctions occur along a gene."
        ),
    )

    # Dataset
    unique_name = "splice"
    year = "1992"
    domain = "biology & life sciences"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5M888"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/splice/ && wget -P local-data-warehouse/splice/ https://archive.ics.uci.edu/static/public/69/molecular+biology+splice+junction+gene+sequences.zip && unzip local-data-warehouse/splice/molecular+biology+splice+junction+gene+sequences.zip -d local-data-warehouse/splice/
    """
    bibtex = """
        @article{towell1994knowledge,
          title={Knowledge-based artificial neural networks},
          author={Towell, Geoffrey G and Shavlik, Jude W},
          journal={Artificial intelligence},
          volume={70},
          number={1-2},
          pages={119--165},
          year={1994},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - We tabularized the fixed-size DNA sequences from the original dataset based on the nucleotide position.
        - We removed the instance ID.
    """

    # Task
    target = "SiteType"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason="Towell, Shavlik & Noordewier 1990-1994 report test error rates of KBANN (per class too), a habit without costs between the three site types. Original rejected: error rate. log_loss is the multiclass fallback.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/splice.data", index_col=False, header=None)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Strip tab-like whitespaces from original data
        df = df.map(lambda x: x.strip())
        df = df.drop(columns=[1])  # Drop instance ID
        target_feature = "SiteType"
        split_data = df[2].apply(lambda x: pd.Series(list(x)))
        # Generate new column names from -30 to +30 excluding 0
        split_data.columns = [f"position_{i}" for i in range(-30, 31) if i != 0]
        split_data[target_feature] = df[0]
        df = split_data
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[c for c in df.columns if c.startswith("position_")])
