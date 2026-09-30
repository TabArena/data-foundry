"""Curated dataset definition for `diamonds` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class Diamonds(AbstractCuratedDataset):
    # Dataset
    unique_name = "diamonds"
    year = "2015"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://github.com/tidyverse/ggplot2/blob/main/data-raw/diamonds.csv"
    license = "MIT License"
    download_description = """
        We download the CSV directly from the ggplot2 GitHub repository.

        mkdir -p local-data-warehouse/diamonds/ && wget -O local-data-warehouse/diamonds/original_diamonds.csv https://raw.githubusercontent.com/tidyverse/ggplot2/main/data-raw/diamonds.csv
    """
    bibtex = """
        @incollection{wickham2016data,
          title={Data analysis},
          author={Wickham, Hadley},
          booktitle={ggplot2: Elegant graphics for data analysis},
          pages={189--201},
          year={2016},
          publisher={Springer}
        }
    """
    curation_comments = """
        - Unlike TabArena, we log scale the target as it is a price and hence log scaling is generally recommended.
    """

    # Task
    target = "price"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/original_diamonds.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df[self.task_metadata.target_column_name] = np.log(df[self.task_metadata.target_column_name])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "cut",
                "color",
                "clarity",
            ],
        )
