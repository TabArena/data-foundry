"""Curated dataset definition for `diamonds` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, Source, TaskSummary

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "cut": ["Fair", "Good", "Very Good", "Premium", "Ideal"],
    "color": ["J", "I", "H", "G", "F", "E", "D"],
    "clarity": ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"],
}

# The columns a stone's listings share (review issue 1): its two price lists write length and width in swapped order
# and grade the cut each its own way, so those columns differ between the listings of one stone.
STONE_KEY = ["carat", "color", "clarity", "depth", "table", "z"]


class Diamonds(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is the price of a diamond with these grading characteristics?",
        use_case=(
            "For example, an online diamond seller prices a newly listed stone from its grading (weight, cut, colour,"
            " clarity, proportions), in line with the rest of its catalogue."
        ),
        row=(
            "One listing of a diamond with its asking price, from the diamonds data of the ggplot2 R package: 53,940 "
            "listings of 43,000 stones that Hadley Wickham scraped from the search site diamondse.info in February "
            "2007 (his post to R-help, April 2023); 40% of the rows are one of two or more listings of the same "
            "stone, in two price lists."
        ),
        predicted="The price in US dollars, shipped on a log scale for modelling; scored by RMSLE on the dollar price.",
        known=(
            "Weight in carats, cut quality, colour grade, clarity grade, total depth and table width in percent, and "
            "length, width and depth in millimetres."
        ),
        split=(
            "Whole stones are held out, every listing of a stone on one side, so the test data stands for stones not "
            "yet priced, against the same day's price lists."
        ),
        fit="direct",
        fit_reason=(
            "The features are the grading a seller has before pricing a stone, and held-out stones of the one "
            "scrape (diamondse.info, February 2007) match pricing new stock against the day's price lists; a stone's "
            "other listing, which gives its price, is never on the other side. The sellers behind the two price "
            "lists are not stated."
        ),
        changes=(
            "We added a stone id, the stone's grading in the six columns its listings share (weight, colour, "
            "clarity, depth and table in percent, height), and split by it; it is no model input."
        ),
    )

    # Dataset
    unique_name = "diamonds"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://github.com/tidyverse/ggplot2/blob/main/data-raw/diamonds.csv",
            license="MIT License",
            year="2007",
            bibtex="""
                @incollection{wickham2016data,
                  title={Data analysis},
                  author={Wickham, Hadley},
                  booktitle={ggplot2: Elegant graphics for data analysis},
                  pages={189--201},
                  year={2016},
                  publisher={Springer}
                }
            """,
        ),
    )
    data_tags = ("Retrospective",)
    download_description = """
        We download the CSV directly from the ggplot2 GitHub repository.

        mkdir -p local-data-warehouse/diamonds/ && wget -O local-data-warehouse/diamonds/original_diamonds.csv https://raw.githubusercontent.com/tidyverse/ggplot2/main/data-raw/diamonds.csv
    """
    curation_comments = """
        - The price ships on a log scale (log of US dollars), the scale a practitioner models a price on, and is scored
          by RMSLE on the dollar price after the inverse (`target_transform="log"`; Lennart, 2026-10-21): a price's
          error matters relative to the price.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 3 columns are ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`).
        - Time basis: Retrospective: one scrape of the search site diamondse.info in February 2007 (Wickham, R-help,
          April 2023); each row a listing's grading and its asking price at that moment; the use case prices a stone
          against the same day's price list. Not tested: prices after 2007.
        - Split by stone (2026-11-12, Andrej, review issue 1 B): 21,493 rows (40%) share carat, colour, clarity,
          depth, table and z (height) with another row, mostly in pairs whose length and width are swapped: one stone
          in two price lists of the scrape. In 98% of the 9,747 swapped pairs the dearer price is the cheaper one
          times one of eight fixed factors set by the price band, exact to the dollar, so under random folds the 27%
          of test rows whose stone's other listing sat in training could be priced by lookup. `stone_id` (the six
          columns' group number: 43,000 stones of 1 to 6 rows) is the group and no model input. Both listings stay,
          since they carry two prices of two lists (fiat_500 keeps one row per car, whose copies share a price). The
          146 exact copies (features and price) fall into one stone each. Untuned LightGBM, 3 x 3 folds, RMSLE:
          random 0.0853, by stone 0.0860.
    """

    # Task
    target = "price"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason=(
            "A teaching dataset of the ggplot2 package defines no task or score; for a price the error that matters "
            "is relative to the price (a $500 miss means more on a $1,000 stone than on a $15,000 one), so RMSLE."
        ),
        target_transform="log",
    )
    grouping = Grouping(
        on="stone_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a stone: the rows that agree in carat, colour, clarity, depth, table and height (z), the grading two listings of one stone share (43,000 stones; 32,447 listed once, 10,296 twice, 257 three to six times). The two listings of a stone come from two price lists of the same scrape: one writes the larger diameter first and grades the cut its own way, and its price is the other's times a fixed factor of the price band. The use case prices a stone newly listed, whose other listing a seller does not have, so the test stones are new to the model with all their listings. Each row is one prediction, made from its listing's grading.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the stone: every listing of a stone stays on one side, so a model prices stones it has not seen and cannot read a price off the stone's other listing. Stones of the same carat, colour and clarity that differ in depth, table or height are different stones and can be on both sides.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/original_diamonds.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df[self.task_metadata.target_column_name] = np.log(df[self.task_metadata.target_column_name])
        # a stone is listed up to six times (mostly twice, in two price lists): its listings share these six columns
        df["stone_id"] = df.groupby(STONE_KEY, sort=False).ngroup().map("stone_{:05d}".format)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "cut",
                "color",
                "clarity",
                "stone_id",
            ],
        )
