"""Curated dataset definition for `jm1` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import openml
from data_foundry.v2 import AbstractCuratedDataset

if TYPE_CHECKING:
    import pandas as pd


class Jm1(AbstractCuratedDataset):
    # Dataset
    unique_name = "jm1"
    year = "2004"
    domain = "technology & internet"
    source = "OpenML"
    source_url = "https://www.openml.org/d/1053"
    license = "Public Domain"
    download_description = """
        We download the data from OpenML inside the notebook.
    """
    bibtex = """
        @inproceedings{menzies2004good,
          title={How good is your blind spot sampling policy},
          author={Menzies, Tim and Di Stefano, Justin S},
          booktitle={Eighth IEEE International Symposium on High Assurance Systems Engineering, 2004. Proceedings.},
          pages={129--138},
          year={2004},
          organization={IEEE}
        }
    """
    curation_comments = """
        - We selected this dataset as representative of a set of predictive modeling tasks of software engineering (other examples of such tasks are available on OpenML under the names mozilla4, pc1, pc2, pc3, mc1, kc1, kc2). This dataset was selected as it has the largest sample size.
    """

    # Task
    target = "defects"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = openml.datasets.get_dataset(1053).get_data()[0]
        return df
