"""Curated dataset definition for `houses` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


class Houses(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("What is the typical house value in a California neighbourhood, judging from its census figures?"),
        use_case=(
            "For example, a lender or housing agency estimates the median home value of a neighbourhood from its "
            "income, housing stock, population and location, where no value is recorded."
        ),
        row=(
            "One California block group, a compact neighbourhood of the 1990 census (19,675 block groups, Pace and "
            "Barry 1997)."
        ),
        predicted="The block group's median house value, on a logarithmic scale as in the source.",
        known=(
            "The median income, the median age of the houses, the totals of rooms, bedrooms, people and households, "
            "and the block group's latitude and longitude."
        ),
        split="Random block groups across the state; neighbouring block groups can be in training.",
        changes=(
            "We drop the block groups whose value sits at the cap of 500,001 dollars, a censored value, so the most "
            "expensive neighbourhoods are not in the data."
        ),
        fit="approximate",
        fit_reason=(
            "The value and the features come from the same census, which reports the value for every block group, so "
            "the task stands in for valuing areas where no value is known. Dropping the capped rows leaves out the "
            "most expensive areas, which such a use would meet."
        ),
    )

    # Dataset
    unique_name = "houses"
    year = "1999"
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
