"""Curated dataset definition for `mutual_funds_india` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class MutualFundsIndia(AbstractCuratedDataset):
    # Dataset
    unique_name = "mutual_funds_india"
    year = "2023"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/ravibarnawal/mutual-funds-india-detailed"
    license = "CC0: Public Domain"
    download_description = """
        kaggle datasets download ravibarnawal/mutual-funds-india-detailed --unzip && mkdir -p local-data-warehouse/mutual_funds_india && mv comprehensive_mutual_funds_data.csv local-data-warehouse/mutual_funds_india/
    """
    bibtex = r"""
        @misc{Barnawal2022MutualFundsIndiaDetailed,
          author = {Ravi Barnawal},
          title  = {Mutual Funds India Detailed},
          year   = {2022},
          howpublished = {\url{https://www.kaggle.com/datasets/ravibarnawal/mutual-funds-india-detailed}},
          note   = {Kaggle dataset}
        }
    """
    curation_comments = """
        We start with the data from Kaggle.

        - We aim to predict the return over 3 years and drop all samples that do not have data for 3 year return.
        - We drop potentially leaking columns about returns (alpha, beta, sd, sharpe, sortino).
        - We drop "rating". The data is one snapshot (scraped April 2023), so the target is the trailing 3-year return at that date. The rating comes from portals such as Value Research (uploader on Kaggle), whose star rating ranks funds within their category on risk-adjusted return, weighting the 5-year score 60% and the 3-year score 40% (https://www.valueresearchonline.com/fund-rating-methodology/). It is therefore computed partly from the target, like sharpe and alpha. In the data, the median within-category rank of returns_3yr rises from 0.18 at 1 star to 0.89 at 5 stars. Dropping it lowers R^2 from 0.811 to 0.783.
    """

    # Task
    target = "returns_3yr"
    problem_type = "regression"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "comprehensive_mutual_funds_data.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(columns=["alpha", "beta", "sd", "sharpe", "sortino", "returns_5yr", "returns_1yr", "rating"])
        df = df[df["returns_3yr"].notna()]
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "sub_category",
                "category",
            ],
            string=[
                "scheme_name",
                "amc_name",
                "fund_manager",
            ],
        )
