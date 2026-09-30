"""Curated dataset definition for `splice` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class Splice(AbstractCuratedDataset):
    # Dataset
    unique_name = "splice"
    year = "1991"
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
        cat_features = [f"position_{i}" for i in range(-30, 31) if i != 0] + [target_feature]
        df[cat_features] = df[cat_features].astype("category")
        return df
