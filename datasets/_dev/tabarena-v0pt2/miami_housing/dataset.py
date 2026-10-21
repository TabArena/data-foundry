"""Curated dataset definition for `miami_housing` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class MiamiHousing(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What price will a single-family home in Miami sell for?",
        use_case=(
            "For example, a property appraiser or a lender estimates the market value of a home from its property "
            "record and location, using the sales of the same year."
        ),
        row="One single-family home sold in Miami in 2016 (13,776 after removing repeated parcels).",
        predicted="The sale price in US dollars, on a log scale.",
        known=(
            "Latitude and longitude, land and living area, the value of special features such as pools, the age and "
            "structure quality, the month of sale, airplane noise above a threshold, and distances to the ocean, "
            "water, rail line, highway, the city centre and the nearest sub-centre."
        ),
        split="Random homes, so the test data stands for other homes sold in the same year.",
        fit="direct",
        fit_reason=(
            "The features are property records and location facts known before a sale, and other homes of the same "
            "year match valuing unsold homes as of that year. The source paper studies price drivers rather than "
            "prediction."
        ),
    )

    # Dataset
    unique_name = "miami_housing"
    year = "2021"  # data from 2016, curated in 2021
    domain = "finance"
    source = "OpenML"
    source_url = "https://www.openml.org/d/43093"
    license = "CC BY-NC-SA"
    data_tags = ("Spatial",)
    download_description = """
        wget https://www.openml.org/data/download/22047757/miami2016.arff && mkdir -p local-data-warehouse/miami_housing && mv miami2016.arff local-data-warehouse/miami_housing/
    """
    bibtex = """
        @misc{mayer2021structured,
          title={Structured Additive Regression and Tree Boosting},
          author={Mayer, Michael and Bourassa, Steven C and Hoesli, Martin and Scognamiglio, Donato},
          year={2021},
          howpublished={SSRN preprint, \\url{https://doi.org/10.2139/ssrn.3924412}},
          note={Cited by the data's first upload, OpenML 43093}
        }
        @article{bourassa2021big,
          title={Big data, accessibility and urban house prices},
          author={Bourassa, Steven C and Hoesli, Martin and Merlin, Louis and Renne, John},
          journal={Urban Studies},
          volume={58},
          number={15},
          pages={3176--3195},
          year={2021},
          publisher={SAGE Publications Sage UK: London, England}
        }
    """
    curation_comments = """
        - We log scale the target.
        - We drop duplicated homes (non-unique identifiers and location) (~1% of the data).
        - We drop the ID column "PARCELNO".
        - Anomaly: while the original paper describes data with 57k samples, we only have 13k on OpenML or Kaggle.
        - The file first appeared on OpenML (43093, uploaded 2021-09-24, creator Steven C. Bourassa, citing Mayer et
          al. 2021). Kaggle deepcontractor/miami-housing-dataset copies its description and names openml.org as its
          source, and OpenML 44983 (2022) copies Kaggle.
    """

    # Task
    target = "SALE_PRC"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "Mayer et al. 2021 (SSRN) could not be read; the abstract names only 'predictive performance'. rmse on "
            "the log sale price is the regression fallback."
        )
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(f"{raw_dir}/miami2016.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop_duplicates(subset=["PARCELNO"])
        df = df.drop(columns=["PARCELNO"])
        df[self.task_metadata.target_column_name] = np.log(df[self.task_metadata.target_column_name])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "avno60plus",
            ],
        )
