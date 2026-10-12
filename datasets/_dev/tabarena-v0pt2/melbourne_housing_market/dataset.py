"""Curated dataset definition for `melbourne_housing_market` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Temporal, TemporalSplits, drop_columns

FULL_FILE = "Melbourne_housing_FULL.csv"
LESS_FILE = "MELBOURNE_HOUSE_PRICES_LESS.csv"

# Results with a sale price: sold, sold prior to the auction, sold after the auction (data card). The price of a
# passed-in (PI) or vendor-bid (VB) result is the highest or the vendor's bid, not a sale.
SALE_METHODS = ("S", "SP", "SA")

# The weekly results sheet of 16 December 2017 was downloaded again on 23 and 30 December, 6 and 8 January: the
# companion file holds the same 787 rows on each of these dates, the full file once, dated 6 January 2018.
COPIED_SHEET = {"6/01/2018": "16/12/2017"}
COPIED_SHEET_ROWS = 787

# A second report of the same address within this many days is the same sale reported again (the repeats with the
# same price lie 0-35 days apart, the resales kept 63-679 days).
REPORT_DAYS = 60

# Spelling variants of one suburb or agency (the lower-case suburbs occur once each; "Fawkner Lot" is "Fawkner" in
# the companion file; agency names that differ only in case or punctuation), mapped to the spelling the file uses most.
SUBURB_SPELLING = {"croydon": "Croydon", "viewbank": "Viewbank", "Fawkner Lot": "Fawkner"}
AGENT_SPELLING = {
    "CASTRAN": "Castran",
    "Obrien": "O'Brien",
    "OBrien": "O'Brien",
    "M.J": "MJ",
    "Re": "RE",
    "VICProp": "VICPROP",
    "Vicprop": "VICPROP",
}

# The property types as words (data card: "h - house,cottage,villa, semi,terrace; u - unit, duplex; t - townhouse").
TYPE_LABELS = {"h": "house", "u": "unit", "t": "townhouse"}

# Attributes the uploader scraped from realestate.com.au after the sale (forum thread 53664, step 4).
SCRAPED_ATTRIBUTES = ["Bedroom2", "Bathroom", "Car", "Landsize", "BuildingArea", "YearBuilt"]

# Melbourne was founded in 1835: an earlier construction year is a data error.
FOUNDING_YEAR = 1835

# The full file holds every result of the weekly sheets from this sheet on, before it only the inner suburbs.
FULL_COVERAGE_FROM = pd.Timestamp("2017-05-27")

# Distance bands (km from the CBD) for the coverage table.
DISTANCE_BANDS = ["0-5", "5-10", "10-15", "15-20", "20-25", "over 25"]

# The columns that identify a result in both files (the companion file lacks the scraped attributes).
RESULT_COLUMNS = ["Suburb", "Address", "Rooms", "Type", "Price", "Method", "SellerG"]


def _sales(full: pd.DataFrame) -> pd.DataFrame:
    """The sales of the full file with a price, the copied sheet dated back, the date parsed."""
    df = full.copy()
    copied = df["Date"].isin(list(COPIED_SHEET))
    assert copied.sum() == COPIED_SHEET_ROWS, "expected the 787 rows of the copied sheet"
    df["Date"] = pd.to_datetime(df["Date"].replace(COPIED_SHEET), format="%d/%m/%Y")
    return df[df["Method"].isin(SALE_METHODS) & df["Price"].notna()]


def _repeated_reports(df: pd.DataFrame) -> pd.DataFrame:
    """Flags for the sales an address reports twice within :data:`REPORT_DAYS` (``df`` sorted by date).

    ``again``: the later report of one sale (same price); ``conflict``: both reports of an address whose two reports
    give different prices.
    """
    address = df["Suburb"].str.lower() + "|" + df["Address"].str.lower()
    by_address = df.groupby(address, sort=False)
    days_since = (df["Date"] - by_address["Date"].shift()).dt.days
    days_until = (by_address["Date"].shift(-1) - df["Date"]).dt.days
    again = (days_since < REPORT_DAYS) & (df["Price"] == by_address["Price"].shift())
    conflict = ((days_since < REPORT_DAYS) & (df["Price"] != by_address["Price"].shift())) | (
        (days_until < REPORT_DAYS) & (df["Price"] != by_address["Price"].shift(-1))
    )
    return pd.DataFrame({"again": again, "conflict": conflict})


def _result_key(df: pd.DataFrame, columns: list[str]) -> pd.Series:
    """One text key per row from ``columns`` (a missing value written as "nan" under pandas 2 and 3)."""
    return df[columns].astype("string").fillna("nan").agg("|".join, axis=1)


class MelbourneHousingMarket(AbstractCuratedDataset):
    # Dataset
    unique_name = "melbourne_housing_market"
    year = "2018"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/anthonypino/melbourne-housing-market"
    license = "CC BY-NC-SA 4.0"
    data_tags = ("Spatial",)
    download_description = """
        We download the Kaggle dataset anthonypino/melbourne-housing-market (last updated 2018-10-14). It holds two
        files: Melbourne_housing_FULL.csv (34,857 rows, 21 columns; md5 06cc531612b8261e0c594c5085e3dc30), which the
        definition uses, and MELBOURNE_HOUSE_PRICES_LESS.csv (63,023 rows, 13 columns; md5
        cc467c28044d01770d8784cf287d1b6e), read only for the evidence of two cleaning steps.

        mkdir -p local-data-warehouse/melbourne_housing_market
        kaggle datasets download anthonypino/melbourne-housing-market -p local-data-warehouse/melbourne_housing_market
        unzip local-data-warehouse/melbourne_housing_market/melbourne-housing-market.zip -d local-data-warehouse/melbourne_housing_market
        rm local-data-warehouse/melbourne_housing_market/melbourne-housing-market.zip
    """
    bibtex = r"""
        @misc{pino2018melbourne,
          author = {Tony Pino},
          title = {Melbourne Housing Market},
          year = {2018},
          howpublished = {\url{https://www.kaggle.com/datasets/anthonypino/melbourne-housing-market}},
          note = {Kaggle dataset; weekly auction results of Domain.com.au, January 2016 to October 2018}
        }
    """
    curation_comments = """
        We start with Melbourne_housing_FULL.csv of the Kaggle dataset anthonypino/melbourne-housing-market: results of properties scheduled for auction in Melbourne (January 2016 to March 2018) from the weekly result sheets of Domain.com.au, with attributes scraped from realestate.com.au.

        - Prediction point: a property is listed for auction, and a price model refit on all earlier sales predicts its sale price from the listing and the auction date.
        - Version: the dataset's other file, MELBOURNE_HOUSE_PRICES_LESS.csv (read only for the decision tables), holds more results but not the scraped attributes. We use the full file for them: the RMSE in log price is 0.183 with them and 0.211 with the other file's columns only (LightGBM with fixed parameters on the shipped windows).
        - Coverage: before 27 May 2017 the full file holds only the inner suburbs (decision table); all test windows lie later. We keep the earlier rows: training only on the sales from 27 May 2017 raises the RMSE from 0.183 to 0.188.
        - We keep the results with a sale price (S, SP, SA) and drop the passed-in (PI) and vendor-bid (VB) results, whose price is the highest or the vendor's bid (data card; decision table). We then drop Method, as the result of the auction is known only after it.
        - The 787 results dated 6 January 2018 are the sheet of 16 December 2017, read again in the holiday break (decision table); we date them 16 December 2017.
        - Repeated reports within 60 days: a sale reported again at the same price keeps its first report, and an address reported at two prices loses both reports. Addresses sold twice 63-679 days apart stay, as the earlier sale is history under the temporal split.
        - The scraped attributes were taken after the sale: six sales of 2016 show a construction year of 2017 or 2018, so we set all six scraped attributes of these rows to missing. Other late lookups stay: blanking the scraped values of the 495 sales of 2016 whose Bedroom2 differs from the sheet's Rooms changes the RMSE by +0.0004.
        - Impossible values to missing: YearBuilt before 1835, the founding of Melbourne, and BuildingArea, Bathroom and Bedroom2 of 0. Landsize 0 stays, as most of these rows are units without land of their own.
        - Anomaly: 92 sales give a BuildingArea of 1-29 square metres; kept.
        - Anomaly: the uploader's processing changed with the sheet of 27 May 2017, and Distance differs before and after for 140 of the 142 suburbs in both periods. Kept: setting each suburb's Distance to its later value changes the RMSE by -0.0004.
        - Spelling variants of a suburb or agency get the file's most frequent spelling.
        - Renamed: SellerG to Agent, Lattitude and Longtitude to Latitude and Longitude. The Type codes become the data card's words (house, unit, townhouse). Postcode is a category, Address text and Date a date. The target is log_price, the natural log of the price in Australian dollars.
        - Note: melbourne_housing_snapshot is a September 2017 subset of this file.
    """

    # Task
    target = "log_price"
    problem_type = "regression"

    # Splits: 9 windows of 3 weekly result sheets (the 3 x 3 an IID task of this size would get).
    temporal = Temporal(
        on="Date",
        splits=TemporalSplits(window=3, unit="unique", n_windows=9, min_train_fraction=0.5),
        horizon=3,
        horizon_unit="weeks",
    )
    splits_comment = """
        A price model refit after every three weekly result sheets predicts the sales of the next three: 9 test windows of 3 consecutive auction dates of the file (one weekly sheet each), from 3-17 March 2018 back to 12-26 August 2017, newest first. Each window trains on all earlier sales (55-95% of the rows), without a gap: a price is published in the sheet of its week. An IID task of this size would get 3 x 3 splits. Calendar windows do not fit the file: it has no sheet between 16 December 2017 and 20 January 2018 and 18 sales on 20 and 27 January 2018, so a monthly window would test January 2018 on 18 sales and a four-week one on 9. Three sheets put them in a window of 93 sales (20 January to 3 February 2018); the other windows hold 868-1,550.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {"full": pd.read_csv(raw_dir / FULL_FILE), "less": pd.read_csv(raw_dir / LESS_FILE)}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # Sales with a price; the copied sheet of 16 December 2017 gets its own date back.
        df = _sales(raw["full"]).sort_values("Date", kind="stable")
        # Spelling variants of one suburb or agency.
        df["Suburb"] = df["Suburb"].replace(SUBURB_SPELLING)
        df["SellerG"] = df["SellerG"].replace(AGENT_SPELLING)
        # A sale reported twice: keep the first report; drop both reports when their prices differ.
        flags = _repeated_reports(df)
        df = df[~(flags["again"] | flags["conflict"])]
        # The scraped attributes of a building finished after the sale describe a later building.
        later_building = df["YearBuilt"] > df["Date"].dt.year
        df.loc[later_building, SCRAPED_ATTRIBUTES] = np.nan
        # Impossible values that stand for missing ones.
        df.loc[df["YearBuilt"] < FOUNDING_YEAR, "YearBuilt"] = np.nan
        for col in ("BuildingArea", "Bathroom", "Bedroom2"):
            df.loc[df[col] == 0, col] = np.nan
        # Readable names and labels.
        df["Type"] = df["Type"].map(TYPE_LABELS)
        df["Postcode"] = df["Postcode"].astype("Int64").astype("string")
        df = df.rename(
            columns={"SellerG": "Agent", "Lattitude": "Latitude", "Longtitude": "Longitude", "Price": "log_price"}
        )
        # Target: the log of the sale price in Australian dollars.
        df["log_price"] = np.log(df["log_price"])
        # The result of the auction is known only after it.
        return drop_columns(df, ["Method"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["Suburb", "Type", "Agent", "Postcode", "CouncilArea", "Regionname"],
            string=["Address"],
            datetime=["Date"],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        full, less = raw["full"], raw["less"]

        # 1. The auction results and their prices.
        methods = full.groupby("Method").agg(rows=("Price", "size"), with_price=("Price", "count"))
        methods["kept"] = methods.index.isin(SALE_METHODS)

        # 2. The sheet of 16 December 2017 in the companion file, and its copy in the full file.
        sheet = set(_result_key(less[less["Date"] == "16/12/2017"], RESULT_COLUMNS))
        dates = ["9/12/2017", "16/12/2017", "23/12/2017", "30/12/2017", "6/01/2018", "8/01/2018", "20/01/2018"]
        copies = pd.DataFrame(
            {
                "rows in the less file": [int((less["Date"] == d).sum()) for d in dates],
                "of them rows of the 16 December sheet": [
                    int(_result_key(less[less["Date"] == d], RESULT_COLUMNS).isin(sheet).sum()) for d in dates
                ],
                "rows in the full file": [int((full["Date"] == d).sum()) for d in dates],
            },
            index=pd.Index(dates, name="date"),
        )

        # 3. The share of the companion file's results that the full file holds, by distance and period (the sheets
        # the full file has).
        where = ["Suburb", "Address", "Date"]
        held = _result_key(less, where).isin(set(_result_key(full, where)))
        less_date = pd.to_datetime(less["Date"], format="%d/%m/%Y")
        sheets = less["Date"].isin(set(full["Date"])) & (
            less_date <= pd.to_datetime(full["Date"], format="%d/%m/%Y").max()
        )
        period = pd.Series(
            np.where(less_date < FULL_COVERAGE_FROM, "before 27 May 2017", "from 27 May 2017"), index=less.index
        )
        band = pd.cut(less["Distance"], [0, 5, 10, 15, 20, 25, 100], labels=DISTANCE_BANDS)
        coverage = (
            held[sheets]
            .groupby([band[sheets].rename("km from the CBD"), period[sheets].rename("period")], observed=True)
            .mean()
            .unstack("period")
            .round(3)
        )

        # 4. Sales reported twice.
        sales = _sales(full).sort_values("Date", kind="stable")
        sales["Suburb"] = sales["Suburb"].replace(SUBURB_SPELLING)
        flags = _repeated_reports(sales)
        address = df["Suburb"].str.lower() + "|" + df["Address"].str.lower()
        reports = pd.Series(
            {
                "sales with a price": len(sales),
                "later report of one sale (dropped)": int(flags["again"].sum()),
                "reports of one address with two prices (dropped)": int(flags["conflict"].sum()),
                "addresses sold twice 63 days or more apart (kept)": int((address.value_counts() > 1).sum()),
            },
            name="rows",
        )

        # 5. Window layouts: test rows per window and the smallest training share.
        layouts = {
            "3 weekly sheets (shipped)": TemporalSplits(window=3, unit="unique", n_windows=9, min_train_fraction=0.5),
            "4 weekly sheets": TemporalSplits(window=4, unit="unique", n_windows=9, min_train_fraction=0.5),
            "4 calendar weeks": TemporalSplits(window=4, unit="weeks", n_windows=9, min_train_fraction=0.5),
            "1 calendar month": TemporalSplits(window=1, unit="months", n_windows=9, min_train_fraction=0.5),
        }
        windows = {}
        for name, layout in layouts.items():
            splits = layout.splits(df, self.temporal.on)
            test = [len(te) for folds in splits.values() for _, te in folds.values()]
            train = [len(tr) / len(df) for folds in splits.values() for tr, _ in folds.values()]
            windows[name] = {
                "windows": len(test),
                "fewest test rows": min(test),
                "most test rows": max(test),
                "smallest training share": round(min(train), 3),
            }

        return [
            Decision(
                "Sale prices only: passed-in and vendor-bid results dropped",
                "The price of a passed-in (PI) or vendor-bid (VB) result is the highest or the vendor's bid. A model "
                "of the sale price fitted on each window's training side (LightGBM) puts PI prices a median 4.3% and "
                "VB prices 6.6% below its prediction, the sales 0.1% above.",
                methods,
            ),
            Decision(
                "The results dated 6 January 2018 are the sheet of 16 December 2017",
                "The companion file holds the same 787 rows on 16, 23 and 30 December 2017 and on 6 and 8 January "
                "2018: one sheet read again in each week of the holiday break. We date them 16 December.",
                copies,
            ),
            Decision(
                "Before 27 May 2017 the file holds the inner suburbs only",
                "Share of the companion file's results that the full file holds. All test windows lie after 27 May "
                "2017, when the full file starts to hold every result of a sheet.",
                coverage,
            ),
            Decision(
                "One row per sale",
                "A sale reported again within 60 days keeps its first report; two reports of one address with "
                "different prices are both dropped; resales 63-679 days apart stay.",
                reports,
            ),
            Decision(
                "Test windows of three weekly sheets",
                "The file has no sheet between 16 December 2017 and 20 January 2018 and 18 sales in January 2018: "
                "calendar windows leave a window of 9-18 sales, four sheets per window leave 2 of 9 windows below "
                "half of the rows for training.",
                pd.DataFrame(windows).T,
            ),
        ]
