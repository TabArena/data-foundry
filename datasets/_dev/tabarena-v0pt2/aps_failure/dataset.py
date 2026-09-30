"""Curated dataset definition for `aps_failure` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class ApsFailure(AbstractCuratedDataset):
    # Dataset
    unique_name = "aps_failure"
    year = "2016"
    domain = "industry & manufacturing"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5V60Q"
    license = "CC BY 4.0"
    data_tags = ("ForcedIIDFromTemporal", "Anonymized")
    download_description = """
        mkdir -p local-data-warehouse/aps_failure && wget -P local-data-warehouse/aps_failure/ https://archive.ics.uci.edu/static/public/414/ida2016challenge.zip && unzip local-data-warehouse/aps_failure/ida2016challenge.zip -d local-data-warehouse/aps_failure/ && rm local-data-warehouse/aps_failure/ida2016challenge.zip
    """
    bibtex = r"""
        @misc{ida2016challenge,
          author       = {{IDA2016Challenge}},
          title        = {IDA2016Challenge [Dataset]},
          year         = {2016},
          howpublished = {\url{https://doi.org/10.24432/C5V60Q}},
          note         = {UCI Machine Learning Repository},
        }
    """
    curation_comments = """
        - We combined the original training and testing data into a single dataset.
        - We renamed the target feature to "AirPressureSystemFailure".
        - We converted "na" strings to real NaN/missing values, making the data numeric.
        - Anomaly: we cannot determine the data types of the features.
        - Anomaly: some features are bins of histograms (see original data description).
        - Anomaly: the original task used a cost matrix for evaluation.
    """

    # Task
    target = "AirPressureSystemFailure"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # remove the leading text before the header form both the training and test data.
        df = pd.concat(
            [
                pd.read_csv(f"{raw_dir}/to_uci/aps_failure_training_set.csv", skiprows=20, na_values="na"),
                pd.read_csv(f"{raw_dir}/to_uci/aps_failure_test_set.csv", skiprows=20, na_values="na"),
            ]
        )
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df.rename(columns={"class": "AirPressureSystemFailure"}, inplace=True)
        return df
