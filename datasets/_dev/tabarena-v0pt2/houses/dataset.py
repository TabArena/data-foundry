"""Curated dataset definition for `houses` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class Houses(AbstractCuratedDataset):
    # Dataset
    unique_name = "houses"
    year = "1990"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://lib.stat.cmu.edu/datasets/"
    license = "Public"
    data_tags = ("Spatial",)
    download_description = """
        We download the houses.zip from the lib.stat.cmu.edu repository and preprocess cadata.txt (strip the 27-line header text, remove leading whitespace, add a column header row).

        mkdir -p local-data-warehouse/houses/ && wget -q -P /tmp https://lib.stat.cmu.edu/datasets/houses.zip && unzip -o /tmp/houses.zip -d /tmp && { echo "MedianHouseValue  MedianIncome  HousingMedianAge  TotalRooms  TotalBedrooms  Population  Households  Latitude  Longitude"; sed -n '28,$p' /tmp/cadata.txt | sed 's/^  //'; } > local-data-warehouse/houses/cadata_manual.txt && rm /tmp/houses.zip /tmp/cadata.txt
    """
    bibtex = r"""
        @article{pace1997sparse,
          title={Sparse spatial autoregressions},
          author={Pace, R Kelley and Barry, Ronald},
          journal={Statistics \\& Probability Letters},
          volume={33},
          number={3},
          pages={291--297},
          year={1997},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - The data contains rows whose values were capped artificially at a price of 500001. This creates a censored target, punishing model that learn to extrapolate from the data. We remove rows with this censored value in the target variable to obtain a more realistic task.
        - We kept the latitude and longitude features as they are.
        - We log scaled the target variable (with base e) as intended by the original task.
        - Anomaly: As always, we randomly shuffle the data before uploading. If one does not randomly shuffle the data, there would be a distribution shift from the longitude and latitude based on the original order of data samples.
    """

    # Task
    target = "LnMedianHouseValue"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/cadata_manual.txt", index_col=False, sep="  ")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Fix lat/longitude whitespace error from original data
        df[["Latitude", "Longitude"]] = df["Latitude"].str.split(" ", expand=True)
        df[["Latitude", "Longitude"]] = df[["Latitude", "Longitude"]].astype(float)
        df = df[df["MedianHouseValue"] < 500001].reset_index(drop=True)
        target_feature = "LnMedianHouseValue"
        # Transform to log space as defined by original task
        df[target_feature] = np.log(df["MedianHouseValue"])
        df = df.drop(columns=["MedianHouseValue"])
        return df
