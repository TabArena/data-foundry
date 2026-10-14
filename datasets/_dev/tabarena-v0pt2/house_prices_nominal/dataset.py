"""Curated dataset definition for `house_prices_nominal` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
    object_columns,
)

# The data end in July 2010 with 8 sales (101-122 in July 2006-2009): the month was cut by the extract.
FIRST_INCOMPLETE_MONTH = 201007

# De Cock (2011, p. 4): the houses over 4,000 sq ft of living area are the five unusual sales of the file.
OUTLIER_LIVING_AREA = 4000

# The documentation's labels of the dwelling-type codes (DataDocumentation.txt, "MS SubClass").
MS_SUBCLASS_LABELS = {
    "020": "1-STORY 1946 & NEWER ALL STYLES",
    "030": "1-STORY 1945 & OLDER",
    "040": "1-STORY W/FINISHED ATTIC ALL AGES",
    "045": "1-1/2 STORY - UNFINISHED ALL AGES",
    "050": "1-1/2 STORY FINISHED ALL AGES",
    "060": "2-STORY 1946 & NEWER",
    "070": "2-STORY 1945 & OLDER",
    "075": "2-1/2 STORY ALL AGES",
    "080": "SPLIT OR MULTI-LEVEL",
    "085": "SPLIT FOYER",
    "090": "DUPLEX - ALL STYLES AND AGES",
    "120": "1-STORY PUD (Planned Unit Development) - 1946 & NEWER",
    "150": "1-1/2 STORY PUD - ALL AGES",
    "160": "2-STORY PUD - 1946 & NEWER",
    "180": "PUD - MULTILEVEL - INCL SPLIT LEV/FOYER",
    "190": "2 FAMILY CONVERSION - ALL STYLES AND AGES",
}

# Columns whose "NA" is a documented level ("NA No Basement", ...), the label we write for it, and the column that
# says whether the item exists (None: the column alone says it).
ABSENT_LEVELS = {
    "Alley": ("No alley access", None),
    "Bsmt Qual": ("No basement", "Bsmt Qual"),
    "Bsmt Cond": ("No basement", "Bsmt Qual"),
    "Bsmt Exposure": ("No basement", "Bsmt Qual"),
    "BsmtFin Type 1": ("No basement", "Bsmt Qual"),
    "BsmtFin Type 2": ("No basement", "Bsmt Qual"),
    "Fireplace Qu": ("No fireplace", None),
    "Garage Type": ("No garage", "Garage Type"),
    "Garage Finish": ("No garage", "Garage Type"),
    "Garage Qual": ("No garage", "Garage Type"),
    "Garage Cond": ("No garage", "Garage Type"),
    "Pool QC": ("No pool", None),
    "Fence": ("No fence", None),
    "Misc Feature": ("None", None),
}


class HousePricesNominal(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What price will a house in Ames, Iowa sell for?",
        use_case=(
            "For example, a lender or a valuation service estimates the sale price of a house from the assessor's "
            "record, with a model refit every two months on the latest sales."
        ),
        row=(
            "One sale of residential property in Ames, Iowa, January 2006 to June 2010, from the city assessor's "
            "office (2,919 sales)."
        ),
        predicted="The sale price in US dollars, on a log scale.",
        known=(
            "The assessor's record of the property (neighbourhood, lot, building type, areas, rooms, quality and "
            "condition grades, year built and remodelled, basement, garage) and the sale's month, type and condition."
        ),
        split=(
            "Each test window is two calendar months, 13 windows from May-June 2008 to May-June 2010; training is "
            "every earlier sale."
        ),
        changes=(
            "We use De Cock's full file instead of the Kaggle competition's random half, split by sale month instead "
            "of at random, and drop his three partial sales of very large new houses."
        ),
        fit="direct",
        fit_reason=(
            "The record describes the house at the sale and the windows follow time, as for a model in use. De Cock "
            "kept only the latest sale of a home sold twice, so the older months miss about 100 sales."
        ),
    )

    # Dataset
    unique_name = "house_prices_nominal"
    year = "2011"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://doi.org/10.1080/10691898.2011.11889627"
    license = (
        "JSE data policy: free to use in teaching; use in papers, books or other published material needs the "
        "consent of the contributing author (https://jse.amstat.org/jse_users.htm)"
    )
    data_tags = ("Spatial",)
    download_description = """
        We download the text version of the data file published with De Cock (2011): AmesHousing.txt, tab-separated,
        2,930 rows and 82 columns (sha256 6cfe6cb525ba437de428653a1040e2aed7d696640bf75203786a6d7a0e67cfcc). Its
        documentation is https://jse.amstat.org/v19n3/decock/DataDocumentation.txt.

        mkdir -p local-data-warehouse/house_prices_nominal
        wget -P local-data-warehouse/house_prices_nominal https://jse.amstat.org/v19n3/decock/AmesHousing.txt

        The record's links, the Kaggle competition house-prices-advanced-regression-techniques and OpenML 42165 (its
        train.csv), hold 1,460 of these sales with prices; see curation_comments.
    """
    bibtex = """
        @article{decock2011ames,
          author = {De Cock, Dean},
          title = {Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project},
          journal = {Journal of Statistics Education},
          volume = {19},
          number = {3},
          year = {2011},
          doi = {10.1080/10691898.2011.11889627}
        }
    """
    curation_comments = """
        We start with AmesHousing.txt, the data file of De Cock (2011): 2,930 sales of residential property in Ames, Iowa, January 2006 to July 2010, from the Ames City Assessor's Office.

        - Prediction point: a house sells, and a valuation model refit every two months on all earlier sales predicts its price from the assessor's record of the property and the sale's type and condition.
        - Source: we use this file rather than the record's Kaggle competition (OpenML 42165), whose 1,460 labelled rows it holds: twice the labelled rows, values as published.
        - Anomaly: De Cock kept only the latest sale of a home sold more than once (p. 4), so the older months miss about 100 sales.
        - We drop the 8 sales of July 2010: the extract cut the month (decision table).
        - We drop `Order` (the file's row number) and `PID` (the parcel number, unique per row).
        - `Yr Sold` and `Mo Sold` become `Month Sold`, the month of the sale and the time column (the file gives no day).
        - In 14 columns "NA" is a documented level for an absent item ("NA No Basement", ...). We write it out ("No basement", ...); empty fields are the missing values. Where the item exists (two houses with a detached garage), "NA" is missing.
        - `MS SubClass` codes ("020", ...) become the documentation's labels. We strip the trailing blank of `Sale Type` "WD ".
        - `Garage Yr Blt` = 2207 (a house built in 2006 and sold new in 2007) is a typo; we set it to missing.
        - The 23 nominal and 21 text-coded ordinal variables are categorical with the source's codes, as in OpenML's house_prices_nominal; the rest is numeric. Total and part areas are kept as published.
        - The target is the natural log of `SalePrice`, renamed to `log_SalePrice`; RMSE on it is the competition's metric.
        - We drop De Cock's three "true outliers" (p. 4), partial sales of new houses over 4,000 sq ft, and keep his two other houses over 4,000 sq ft (decision table). The three would only train, yet without them the task probe's linear model goes from RMSE 0.133 to 0.124.
        - The records describe the house at the sale: no house built two or more years before its sale has a remodel year after it.
        - Anomaly: `Year Remod/Add` starts at 1950: 337 of the 629 houses built before 1950 show 1950, where the documentation gives the construction year for no remodel. Kept as recorded.
        - Note: allocation sales ("Alloca") and adjoining-land purchases ("AdjLand") come mostly in blocks of neighbouring parcels sold in one month, so a block shares a window; kept, with `Sale Condition` as a feature.
        - No duplicate rows. Two pairs of neighbouring parcels share every feature and sold in one month at different prices; kept.
        - Note: the record's `Trivial` marker does not hold: `Overall Qual` alone reaches R² 0.682 and De Cock's two-variable model 0.766, against 0.912 for LightGBM.
    """

    # Task
    target = "log_SalePrice"
    problem_type = "regression"

    # Splits: two-month calendar windows down to half of the rows for training (13 windows of 46-191 sales).
    temporal = Temporal(on="Month Sold", splits=TemporalSplits(window=2, unit="months", min_train_fraction=0.5))
    splits_comment = """
        A price model refit every two months predicts the sales of the next two months: 13 test windows of two calendar months, from May-June 2010 back to May-June 2008, newest first, each trained on all earlier sales. The windows stop where the training side would fall below half of the rows (a March-April 2008 window would train on 47% of them). An IID task of this size would get 10 x 3 splits; monthly windows would hold 19-112 sales, so we use two months (46-191 sales per window). A price is known once the sale is recorded, so each window trains on every earlier month without a gap. A model used earlier, at the purchase agreement one or two months before the sale, would need a gap of that length; over the 13 windows it changes LightGBM's RMSE by +0.0006 (SE 0.0010) for one month and +0.0026 (SE 0.0013) for two.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # "NA" is a documented level in 14 columns and empty fields are missing, so only "" is read as missing. The
        # parcel number and the dwelling-type code are codes: read as text to keep the leading zeros.
        return pd.read_csv(
            raw_dir / "AmesHousing.txt",
            sep="\t",
            keep_default_na=False,
            na_values=[""],
            dtype={"PID": str, "MS SubClass": str},
        )

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # The extract cut July 2010 (8 sales).
        month = df["Yr Sold"] * 100 + df["Mo Sold"]
        df = df[month < FIRST_INCOMPLETE_MONTH]
        # De Cock's "true outliers" (p. 4): partial sales of new houses over 4,000 sq ft at $28-$40 per sq ft. The two
        # other houses over 4,000 sq ft are market sales and stay.
        outliers = (df["Gr Liv Area"] > OUTLIER_LIVING_AREA) & (df["Sale Condition"] == "Partial")
        assert outliers.sum() == 3, "expected De Cock's three partial-sale outliers"
        df = df[~outliers]
        # The time column: the month of the sale (the file gives no day).
        df["Month Sold"] = (df["Yr Sold"] * 100 + df["Mo Sold"]).astype(str)
        # Absent items: write out the documented "NA" level; where the item exists, "NA" is a missing value. The
        # anchors are read before any column is rewritten.
        anchors = {col: df[col] == "NA" for col in ("Bsmt Qual", "Garage Type")}
        for col, (label, anchor) in ABSENT_LEVELS.items():
            is_na = df[col] == "NA"
            absent = anchors[anchor] if anchor is not None else is_na
            df[col] = df[col].mask(is_na & absent, label).mask(is_na & ~absent)
        assert not any((df[c] == "NA").any() for c in object_columns(df)), "an undocumented NA level is left"
        # Dwelling-type codes to the documentation's labels.
        assert df["MS SubClass"].isin(list(MS_SUBCLASS_LABELS)).all(), "an undocumented MS SubClass code"
        df["MS SubClass"] = df["MS SubClass"].map(MS_SUBCLASS_LABELS)
        df["Sale Type"] = df["Sale Type"].str.strip()
        # A typo: a garage built in 2207 (house built 2006, sold new in 2007).
        typo = df["Garage Yr Blt"] > df["Yr Sold"].max()
        assert typo.sum() == 1, "expected one garage year after the data end"
        df.loc[typo, "Garage Yr Blt"] = np.nan
        # Target: the log of the sale price, renamed in place.
        df = df.rename(columns={"SalePrice": "log_SalePrice"})
        df["log_SalePrice"] = np.log(df["log_SalePrice"])
        return drop_columns(df, ["Order", "PID", "Yr Sold", "Mo Sold"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The non-numeric columns are the 23 nominal and 21 text-coded ordinal variables of the documentation (text
        # in the cleaned frame, categories in the final one).
        return FeatureTypes(
            categorical=[c for c in df.columns if c != "Month Sold" and not pd.api.types.is_numeric_dtype(df[c])],
            datetime={"Month Sold": "%Y%m"},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        july = raw[raw["Mo Sold"] == 7].groupby("Yr Sold").size().rename("sales in July")

        windows = []
        for months in (1, 2, 3):
            splits = TemporalSplits(window=months, unit="months", min_train_fraction=0.5).splits(df, "Month Sold")
            sizes = pd.Series([len(test) for folds in splits.values() for _, test in folds.values()])
            windows.append(
                {
                    "window (months)": months,
                    "windows": len(sizes),
                    "fewest test rows": int(sizes.min()),
                    "median test rows": int(sizes.median()),
                    "most test rows": int(sizes.max()),
                }
            )

        large = raw.loc[
            raw["Gr Liv Area"] > OUTLIER_LIVING_AREA,
            ["Gr Liv Area", "Neighborhood", "Yr Sold", "Mo Sold", "Sale Condition", "SalePrice"],
        ].sort_values(["Yr Sold", "Mo Sold"], kind="stable")
        large["price per sq ft"] = (large["SalePrice"] / large["Gr Liv Area"]).round(1)
        large["kept"] = large["Sale Condition"] != "Partial"
        partial = raw[raw["Sale Condition"] == "Partial"]
        partial_median = (partial["SalePrice"] / partial["Gr Liv Area"]).median()
        return [
            Decision(
                "Sales of July 2010 dropped: the extract cut the month",
                "The file ends in July 2010 with 8 sales, against 101-122 in July of every earlier year.",
                july,
            ),
            Decision(
                "Two-month test windows",
                "The convention asks for as many windows as an IID task gets splits (30), at least half of the rows "
                "for training and about 50 test rows per window. Monthly windows hold as few as 19 sales in winter; "
                "two-month windows hold at least 46.",
                pd.DataFrame(windows).set_index("window (months)"),
            ),
            Decision(
                "The 3 partial sales over 4,000 sq ft dropped, the 2 market sales kept",
                'De Cock (p. 4) names the five houses over 4,000 sq ft: three are "true outliers (Partial Sales that '
                'likely don\'t represent actual market values)" and two are "very large houses priced relatively '
                f'appropriately". The three sold at $28-$40 per sq ft, against a median of ${partial_median:.0f} for '
                "partial sales; the record describes the finished house, the price does not. All five sold before the "
                "oldest test window, so they would only train.",
                large.reset_index(drop=True),
            ),
        ]
