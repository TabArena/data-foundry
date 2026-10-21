"""Curated dataset definition for `melbourne_housing_market` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

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

# Attributes the uploader scraped from realestate.com.au after the sale (forum thread 53664, step 4). The coordinates
# come from the same lookup (4,760 of the 4,915 sales without these attributes also lack them); they stay for every
# row, as a location does not change.
SCRAPED_ATTRIBUTES = ["Bedroom2", "Bathroom", "Car", "Landsize", "BuildingArea", "YearBuilt"]

# The uploader looked the attributes up for all earlier sales at once, by 10 April 2017 (thread 30748: on 28 March
# "It may be difficult", on 10 April "I've added some more info to the dataset including landsize, bedroom, bathroom,
# carspace"); the sales from the sheet of 22 April 2017 on were looked up by the weekly runs. The six attributes of
# the sales before this lookup are blanked (LEAK-7, LEAK-10).
BATCH_LOOKUP = pd.Timestamp("2017-04-10")

# The uploader's suburb lookups (forum thread 53664, step 5): one value per suburb. Two rows lack them (the "Fawkner
# Lot" row and one Footscray row) and get their suburb's values.
SUBURB_LOOKUPS = ["Postcode", "CouncilArea", "Regionname", "Propertycount"]
ROWS_WITHOUT_LOOKUP = 2

# Building areas that cannot be: below 10 m², above 1,000 m² where the area also exceeds the lot or 200 m² per room,
# and a house's area equal to its land size (the lot copied into the field).
MIN_BUILDING_AREA = 10
MAX_BUILDING_AREA = 1000
MAX_AREA_PER_ROOM = 200

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
    task_summary = TaskSummary(
        question="Before the auction, at what price will a Melbourne property sell, for a property that sells?",
        use_case=(
            "Before the auction of a Melbourne property, a price model fitted on all earlier sales estimates the "
            "price it sells for, for example for a buyer or an agent setting expectations. The task covers the "
            "properties that sell: a property passed in at auction has no sale price."
        ),
        row=(
            "One sale of a property listed for auction in Melbourne, January 2016 to March 2018, from the weekly "
            "result sheets of Domain.com.au (21,266 sales)."
        ),
        predicted="The sale price, as the natural log of Australian dollars.",
        known=(
            "The address, suburb, postcode, council area, region, distance to the centre and the suburb's number of "
            "properties; the property type, rooms, agent and auction date; and, from a lookup on realestate.com.au "
            "made after the sale, the coordinates and six attributes (bedrooms, bathrooms, car spaces, land and "
            "building size, year built), blank for the sales before April 2017, looked up months later."
        ),
        split=(
            "Nine test windows of three consecutive weekly sheets, from August 2017 to March 2018; each trains on all"
            " earlier sales and predicts up to 7 calendar weeks ahead."
        ),
        changes=(
            "We drop results without a sale price (passed in, vendor bid) and the auction outcome, known only after "
            "the auction, blank the attributes looked up months after the sale, and test on later weekly sheets "
            "instead of random sales."
        ),
        fit="direct",
        fit_reason=(
            "The listing and the earlier sales are what a price model has before the auction, the rows are the "
            "properties that sell, as the use case names, and later sheets stand for the coming auctions. The "
            "scraped attributes were looked up days or weeks after the sale (the weekly runs); those of the earlier "
            "sales, looked up months later, are blanked."
        ),
    )

    # Dataset
    unique_name = "melbourne_housing_market"
    year = "2018"  # the snapshot we pin (version 27); the source grew with each version from 2017 to 2018
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/anthonypino/melbourne-housing-market"
    license = "CC BY-NC-SA 4.0"
    data_tags = ("Spatial",)
    download_description = """
        We download version 27 of the Kaggle dataset anthonypino/melbourne-housing-market (2018-10-14, the current
        one; the md5s below identify its files). It holds two
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

        - Prediction point: before the auction, for a property that sells. A price model fitted on all earlier sales predicts the sale price from the listing and the auction date; a property passed in has no sale price and is not in the task.
        - Version: the dataset's other file, MELBOURNE_HOUSE_PRICES_LESS.csv (read only for the decision tables), holds more results but not the scraped attributes. We use the full file for them: the RMSE in log price is 0.182 with them, 0.200 without them and 0.206 with the other file's columns only (LightGBM with fixed parameters on the shipped windows, 3 seeds; worse in 9 of 9 windows; measured before the blanking of the April 2017 lookup, which adds 0.001).
        - Coverage: before 27 May 2017 the full file holds only the inner suburbs (decision table); all test windows lie later. We keep the earlier rows: training only on the sales from 27 May 2017 raises the RMSE from 0.182 to 0.185.
        - We keep the results with a sale price (S, SP, SA) and drop the passed-in (PI) and vendor-bid (VB) results, whose price is the highest or the vendor's bid (data card; decision table). We then drop Method, as the result of the auction is known only after it.
        - The 787 results dated 6 January 2018 are the sheet of 16 December 2017, read again in the holiday break (decision table); we date them 16 December 2017.
        - Repeated reports within 60 days: a sale reported again at the same price keeps its first report, and an address reported at two prices loses both reports. Addresses sold twice 63-679 days apart stay, as the earlier sale is history under the temporal split.
        - Attributes looked up after the sale (LEAK-7, LEAK-10; Lennart, 2026-10-21): the six attributes from realestate.com.au (Bedroom2, Bathroom, Car, Landsize, BuildingArea, YearBuilt) and the coordinates were looked up after the sale (forum thread 53664, step 4). The sales up to the sheet of 8 April 2017 were looked up at once, by 10 April 2017 (thread 30748: "It may be difficult" on 28 March, "I've added some more info to the dataset including landsize, bedroom, bathroom, carspace" on 10 April), up to 15 months after the sale; from the sheet of 22 April 2017 on, the uploader's weekly runs looked them up. We blank the six attributes of the 7,578 sales before 10 April 2017 (6,065 had them), so a missing value follows the date, not a change to the house. Bedroom2 equals Rooms in 84-88% of the sales of each month from April to September 2016, against 99.2-100% of each month from November 2016 on and 98.9-100% of each test window; the September 2017 snapshot holds the same values for the 2,728 test rows up to 23 September 2017. Blanking raises the RMSE by 0.0011 to 0.0016 over 3 seeds (mean 0.1813 to 0.1826, 6-7 of 9 windows worse; LightGBM with fixed parameters). A sale with a construction year after its sale year (a later building; six sales of 2016) also loses the six. The test rows keep the values of the weekly runs, recorded days or weeks after the sale; only Bedroom2 is checked against a value from the sale. The coordinates stay for every row, as a location does not change.
        - Impossible values to missing: YearBuilt before 1835, the founding of Melbourne, and BuildingArea, Bathroom and Bedroom2 of 0. Landsize 0 stays, as most of these rows are units without land of their own.
        - BuildingArea to missing where it cannot be (86 of 8,285 values): below 10 square metres (47), above 1,000 where it also exceeds the lot or 200 per room (7), and a house's area equal to its land size (32). Anomaly: 45 values of 10-29 may be in squares (9.29 square metres, an Australian unit); circumstantial, kept.
        - One Distance per suburb: the uploader's suburb table changed with the sheet of 27 May 2017 (140 of the 142 suburbs in both periods get a new value, Airport West 13.5 to 10.4 km), so each suburb gets the later value, the one every test window uses. The two rows without a suburb lookup (the "Fawkner Lot" row and one Footscray row) get their suburb's postcode, council area, region and property count.
        - Anomaly: 11 sheet dates (1,907 sales) are not a Saturday: nine lie 1-3 days after one, two are Thursdays (28 January and 4 February 2016); the other file has the same dates. Kept, as the windows count sheets, not days.
        - Spelling variants of a suburb or agency get the file's most frequent spelling.
        - Renamed: SellerG to Agent, Lattitude and Longtitude to Latitude and Longitude. The Type codes become the data card's words (house, unit, townhouse). Postcode is a category, Address text and Date a date. The target is log_price, the natural log of the price in Australian dollars.
        - Note: melbourne_housing_snapshot is a September 2017 subset of this file.
    """

    # Task
    target = "log_price"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "Kaggle dataset without a task or metric; regression fallback rmse (on the log target, close to RMSLE)."
        ),
    )

    # Splits: 9 windows of 3 weekly result sheets (the 3 x 3 an IID task of this size would get).
    temporal = Temporal(
        on="Date",
        splits=TemporalSplits(window=3, unit="unique", n_windows=9, min_train_fraction=0.5),
        horizon=3,
        horizon_unit="weeks",
    )
    splits_comment = """
        Before the auction, a price model fitted once per window on all earlier sales predicts the sales of the next three weekly result sheets: 9 test windows of 3 consecutive auction dates of the file (one weekly sheet each), from 3-17 March 2018 back to 12-26 August 2017, newest first. Each window trains on all earlier sales (55-95% of the rows), without a gap: a price is published in the sheet of its week. The horizon is three sheets, up to 7 calendar weeks: the file lacks the sheets of 10 June, 5 August and 2 December 2017 and 13 January 2018, so a window can span 4 calendar weeks, and the window of 20 January to 3 February 2018 trains on sales up to 16 December 2017. An IID task of this size would get 3 x 3 splits. Calendar windows do not fit the file: it has no sheet between 16 December 2017 and 20 January 2018 and 18 sales on 20 and 27 January 2018, so a monthly window would test January 2018 on 18 sales and a four-week one on 9. Three sheets put them in a window of 93 sales (20 January to 3 February 2018); the other windows hold 868-1,550. Recording delay (SPLIT-10; measured 2026-10-21 as house_prices_nominal did): the newest sheets are not short. Every weekly sheet of the full file from August 2017 to 17 March 2018 holds as many sales as the same sheet of the companion file, read up to October 2018 (558 of 558 on 17 March 2018), so no sale reached a sheet after it was first read. The three sheets of March 2018 hold 1,121 sales, against 1,174 in the same three sheets of 2017 (companion file, all suburbs), and the newest window's mean residual log price is +0.009 (one LightGBM fit per window), inside the range of the other windows (-0.013 to +0.022). No gap.
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
        # One Distance per suburb: the table the file uses from 27 May 2017, in every test window.
        later_table = df[df["Date"] >= FULL_COVERAGE_FROM].groupby("Suburb")["Distance"].first()
        df["Distance"] = df["Suburb"].map(later_table)
        assert df["Distance"].notna().all(), "every suburb has a Distance from 27 May 2017 on"
        # The two rows without a suburb lookup get their suburb's values.
        without_lookup = df[SUBURB_LOOKUPS].isna().any(axis=1)
        assert without_lookup.sum() == ROWS_WITHOUT_LOOKUP, "expected the Fawkner Lot and the Footscray row"
        for col in SUBURB_LOOKUPS:
            df[col] = df[col].fillna(df.groupby("Suburb")[col].transform("first"))
        # The scraped attributes of the sales looked up in the batch of April 2017, months after the sale, and of a
        # building finished after the sale (a later building).
        looked_up_late = (df["Date"] < BATCH_LOOKUP) | (df["YearBuilt"] > df["Date"].dt.year)
        df.loc[looked_up_late, SCRAPED_ATTRIBUTES] = np.nan
        # Impossible values that stand for missing ones.
        df.loc[df["YearBuilt"] < FOUNDING_YEAR, "YearBuilt"] = np.nan
        for col in ("BuildingArea", "Bathroom", "Bedroom2"):
            df.loc[df[col] == 0, col] = np.nan
        area = df["BuildingArea"]
        too_large = (area > MAX_BUILDING_AREA) & ((area > df["Landsize"]) | (area / df["Rooms"] > MAX_AREA_PER_ROOM))
        lot_copied = (df["Type"] == "h") & (area == df["Landsize"])
        df.loc[(area < MIN_BUILDING_AREA) | too_large | lot_copied, "BuildingArea"] = np.nan
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
