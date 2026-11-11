"""Curated dataset definition for `miami_housing` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, Temporal, TemporalSplits

# Scores and ratings with no words per level: numbers, as the source ships them (CLEAN-14).
SCORES = ["structure_quality"]


class MiamiHousing(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What price will a single-family home in Miami sell for?",
        use_case=(
            "For example, a lender or a valuation site, refitting its model every month on all earlier sales, "
            "prices the homes sold in the next month from their property record and location."
        ),
        row="One sale of a single-family home in Miami in 2016 (13,932 sales; 152 homes sold more than once).",
        predicted="The sale price in US dollars, on a log scale.",
        known=(
            "Latitude and longitude, land and living area, the value of special features such as pools, the age and "
            "structure quality, the month of sale, airplane noise above a threshold, and distances to the ocean, "
            "water, rail line, highway, the city centre and the nearest sub-centre."
        ),
        split=(
            "By month of sale: five test months, August to December 2016, each trained on all earlier months (58% "
            "to 92% of the sales)."
        ),
        fit="direct",
        fit_reason=(
            "The features are property records and location facts known before a sale, and each test month is "
            "predicted from earlier sales only, as a model in use prices later sales. The data cover one year, so "
            "the training history is under a year. The source paper studies price drivers rather than prediction."
        ),
    )

    # Dataset
    unique_name = "miami_housing"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="OpenML",
            url="https://www.openml.org/d/43093",
            license="CC BY-NC-SA",
            year="2021",  # data from 2016, curated in 2021
            bibtex="""
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
            """,
        ),
    )
    data_tags = ("Spatial",)
    download_description = """
        wget https://www.openml.org/data/download/22047757/miami2016.arff && mkdir -p local-data-warehouse/miami_housing && mv miami2016.arff local-data-warehouse/miami_housing/
    """
    curation_comments = """
        - We log scale the target.
        - We keep the repeated sales of one home (156 sales of 152 homes; 2026-11-11, Andrej): under the split by
          month the earlier sale is history. There are no exact copies to drop. Six pairs repeat the price in another
          month (possibly one sale recorded twice); they stay. Nine homes sold two or three times within one month
          at different prices share every feature (the conflicting duplicates the checks report); they stay.
        - We drop the ID column "PARCELNO".
        - `sale_month` (2016-MM-01), built from `month_sold`, is the time column; `month_sold` stays a feature (`sale_month` is a feature too, as a date).
        - Anomaly: while the original paper describes data with 57k samples, we only have 13k on OpenML or Kaggle.
        - The file first appeared on OpenML (43093, uploaded 2021-09-24, creator Steven C. Bourassa, citing Mayer et
          al. 2021). Kaggle deepcontractor/miami-housing-dataset copies its description and names openml.org as its
          source, and OpenML 44983 (2022) copies Kaggle.
        - `structure_quality` ("quality of the structure", OpenML 43093, codes 1-5 without labels) is an ordered
          category in the order of its codes (2026-10-31, CLEAN-14; the curator's marks: the order comes from the
          context and logic, not from the target, so the high prices of the 16 homes rated 3 do not move it).
        - Cycle (2026-11-01, CLEAN-14, Lennart's rule): `month_sold` (1-12) stays a number. A weekday or a month is a
          position in a continuous cycle (weekday 1.5 is Monday noon), and the source ships it as a number; named
          weekdays and months are ordered categories instead.
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 1 scores with no words per level are
          numbers (`SCORES`): `structure_quality`.
    """

    # Task
    target = "SALE_PRC"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason="Mayer et al. 2021 (SSRN) could not be read; the abstract names only 'predictive performance'. For a sale price the error that matters is relative to the price, so RMSLE on the price.",
        target_transform="log",
    )

    # Splits: five calendar months, August to December 2016, each trained on all earlier months.
    temporal = Temporal(
        on="sale_month",
        splits=TemporalSplits(window=1, unit="months", n_windows=5, min_train_fraction=0.5),
    )
    splits_comment = """
        A price model refit every month predicts the next month's sales: five test windows of one calendar month,
        December back to August 2016, newest first, each trained on all earlier months (92%, 83%, 76%, 67% and 58%
        of the 13,932 sales; 1,057 to 1,275 test sales). No gap: sales are dated by month, longer than the delay from a
        sale to its record (SPLIT-10). The data hold one year, so training history is under a year. The earlier random
        split (3 x 3 folds) read the task as an appraiser valuing the year's homes from the same year's sales; it was
        replaced so that this dated house-sale table follows the regime of the others (2026-11-11, Andrej). At equal
        training size, training on earlier months only cost +0.001 RMSLE against sales from all other months
        (untuned LightGBM 0.147 against 0.146; ridge 0.268 against 0.267; 2026-11-06).
    """
    accepted_check_warnings = {
        "meta_time_horizon_mismatch": "`sale_month` holds the first day of the sale month (the source gives no day), "
        "so each one-month test window holds a single date and its span reads as 1 day; the windows are calendar "
        "months (as perth_house_prices and zillow_prize).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(f"{raw_dir}/miami2016.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # repeated sales of a home stay (history under the split by month); only exact copies would go (none)
        df = df.drop_duplicates()
        df = df.drop(columns=["PARCELNO"])
        # the time column: the month of the sale (the file gives no day)
        df["sale_month"] = pd.to_datetime({"year": 2016, "month": df["month_sold"].astype(int), "day": 1})
        df[self.task_metadata.target_column_name] = np.log(df[self.task_metadata.target_column_name])
        # scores with no words per level are numbers (CLEAN-14)
        df[SCORES] = df[SCORES].astype("object").apply(pd.to_numeric)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "avno60plus",
            ],
        )
