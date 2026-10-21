"""Curated dataset definition for `perth_house_prices` (data-foundry v2). Evidence: README.md."""

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
)

RAW_FILE = "all_perth_310121.csv"
COORDINATE_COLUMNS = ["LATITUDE", "LONGITUDE", "NEAREST_SCH_DIST"]  # the school distance is computed from them
# Opening month of the stations opened since 1988 (Joondalup line Dec 1992, extended to Currambine Aug 1993, Clarkson
# Oct 2004, Greenwood Jan 2005, Butler Sep 2014; Thornlie Aug 2005; Mandurah line Dec 2007). The file names the
# nearest station at the scrape, so a sale before the opening names a station that did not exist.
STATION_OPENED = {
    **dict.fromkeys(
        ["Joondalup", "Edgewater", "Whitfords", "Warwick", "Stirling", "Glendalough", "Leederville"], "1992-12"
    ),
    "Currambine": "1993-08",
    "Clarkson": "2004-10",
    "Greenwood": "2005-01",
    "Thornlie": "2005-08",
    "Butler": "2014-09",
    **dict.fromkeys(
        [
            "Esplanade",
            "Canning Bridge",
            "Bull Creek",
            "Murdoch",
            "Cockburn Central",
            "Kwinana",
            "Wellard",
            "Rockingham",
            "Warnbro",
            "Mandurah",
        ],
        "2007-12",
    ),
}
SCHOOL_OPENED = {"JOSEPH BANKS SECONDARY COLLEGE": "2015-01"}  # the one school in the file known to open after 1988


class PerthHousePrices(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What price will a house in Perth sell for this month?",
        use_case=(
            "A valuation model, refit at the start of each month on all earlier sales, estimates the price of a house"
            " sold that month, for example for a lender or an agent."
        ),
        row=(
            "One house sale in Perth, Western Australia, from a property website scraped in January 2021; each "
            "property's latest sale only, dated by month from 1988 to 2020 (33,090 sales)."
        ),
        predicted=(
            "The sale price in Australian dollars, as its natural logarithm; the data is truncated at $2.44M "
            "(dearer sales are absent)."
        ),
        known=(
            "The sale month, address and location, the site's record of the house (rooms, garage, land and floor "
            "area, build year) as of the January 2021 scrape, the nearest station and school as of the scrape "
            "(blank before they opened) with their distances, and that school's rank of 2019 or later."
        ),
        split=(
            "Each test window is one month of April to December 2020, trained on all earlier sales, as for a model "
            "refit at the start of each month."
        ),
        changes=(
            "We drop 563 sales dated before the house was built (land or off-the-plan sales), blank the station or "
            "school for the sales before it opened, and set impossible floor areas and bathroom counts to missing."
        ),
        fit="approximate",
        fit_reason=(
            "Each month is predicted from earlier sales only, from a house's record and location. Two gaps remain: "
            "the data is truncated at $2.44M (dearer sales are absent), and the house attributes are the site's "
            "record of January 2021 rather than at the sale."
        ),
    )

    # Dataset
    unique_name = "perth_house_prices"
    year = "2021"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/datasets/syuzai/perth-house-prices"
    license = "CC BY-NC-SA 4.0"
    data_tags = ("Spatial",)
    download_description = """
        We download all_perth_310121.csv from Kaggle (33,656 rows, 19 columns; sha256
        e9f334588eaaa6d4a82b89900dd7bd2abfe7644fd9ee9acb238d022eec4f9aff). The dataset has one version (created
        2021-01-31); the API does not serve it by version number. OpenML 43822 holds the same table.

        mkdir -p local-data-warehouse/perth_house_prices
        kaggle datasets download syuzai/perth-house-prices -p local-data-warehouse/perth_house_prices
        unzip local-data-warehouse/perth_house_prices/perth-house-prices.zip -d local-data-warehouse/perth_house_prices
        rm local-data-warehouse/perth_house_prices/perth-house-prices.zip
    """
    bibtex = r"""
        @misc{syuzai2021perth,
          author = {syuzai},
          title = {Perth House Prices},
          year = {2021},
          howpublished = {\url{https://www.kaggle.com/datasets/syuzai/perth-house-prices}},
          note = {Kaggle dataset, scraped from http://house.speakingsame.com/}
        }
    """
    curation_comments = """
        We start with all_perth_310121.csv from the Kaggle dataset syuzai/perth-house-prices: 33,656 sales in 321 suburbs of Perth, dated by month from April 1988 to December 2020, scraped from house.speakingsame.com.

        - Prediction point: a property sells, and a valuation model refit monthly on all earlier sales predicts its price from the listing, the address and the location.
        - Temporal split on `DATE_SOLD`: 9 monthly test windows, April to December 2020 (splits comment).
        - `DATE_SOLD` is the sale month ("09-2018", a trailing carriage return stripped), parsed to the first day of the month; it is the time column and a feature.
        - The target is the natural log of `PRICE`, renamed to `log_PRICE`.
        - Sampling: a property appears only with its latest sale before the scrape, and each suburb holds only its newest sales, so the older years are thin (decision table).
        - Anomaly: the data is truncated at $2,440,000: one sale sits at that price and none above it, although the site lists dearer sales, so the dearer sales are absent (not set to the ceiling). The task is the price of a sale up to $2.44M, and the dearest suburbs keep only their cheaper sales (decision table).
        - We drop the 563 sales (1988-2016) dated before the year the house was built: a land or off-the-plan sale is not the sale of the house the valuation prices, and the row's attributes describe a house built 1-23 years later; LightGBM prices them 0.1-0.5 log units too high, by setup (decision table). All are training rows. The 140 sales in the build year stay as the boundary case (a sale just before or after completion), although 9-13% of them are priced more than 0.5 log units too high.
        - We drop 3 copies of sales geocoded to several address points (identical except the coordinates and the school distance); two pairs that differ in the address and its coordinates stay.
        - Missing values: "NULL" and empty fields are read as missing, and we set the proxies `LAND_AREA` 999999 and `GARAGE` 99 to missing. `GARAGE` has no 0, so a missing value may also mean no car space.
        - Impossible values to missing, rows kept: `FLOOR_AREA` of 1-40 m² for a house of 2 or more bedrooms (19 rows), and `BATHROOMS` more than 2 above `BEDROOMS` (2 rows: 16 bathrooms in 95 m², 7 bathrooms with 1 bedroom). Unusual values stay: whole-complex land areas of strata units and garages of 13-50 car spaces.
        - Anomaly: no house has a build year after 2017, so newer houses lack `BUILD_YEAR` (missing in 9.5% of all rows).
        - Anomaly: the house attributes are the site's record at the scrape. Before the test period they did not change: bedrooms or bathrooms differ from the sold listings of heptix/perth-property-prices in 0.7% of the shared 2007-2016 sales (2.8% in 2017-2018). In the test period the record is often older than the sale, not newer (27.0% of the shared 2020 sales differ, mostly with fewer rooms), which adds noise to the test windows but no post-sale value.
        - Station and school as of the scrape: we blank `NEAREST_STN` and `NEAREST_STN_DIST` for the 147 sales (1988-2014) before their station opened (the opening months of 22 stations), and `NEAREST_SCH`, `NEAREST_SCH_DIST` and `NEAREST_SCH_RANK` for the 58 sales (1990-2014) that name Joseph Banks Secondary College, opened in 2015; all are training rows.
        - Potential leak, kept on purpose: `NEAREST_SCH_RANK` is one ranking per school, of 2019 or later (the 2015 school is ranked), so for most rows it postdates the sale and for the test rows its year is unknown and may follow the sale; the effect is nil (mean RMSE 0.1623 without it against 0.1622, one seed, 9 windows). Schools opened since 1988 other than Joseph Banks were not checked. Revisit if the ranking year is found. `NEAREST_SCH_RANK` is missing for unranked schools.
        - `NEAREST_STN` `Vic` names two stations 14 km apart; we split it by longitude into Victoria Street (Mosman Park, west of 115.8° E, 98 rows) and Victoria Park (198 rows).
        - `ADDRESS` stays as text (string), as in melbourne_housing_market: unit numbers and lettered lots are the only trace of the property type the upload dropped (decision table).
        - Categorical: `SUBURB`, `POSTCODE`, `NEAREST_STN` and `NEAREST_SCH`.
        - Note: we keep the 52 sales since 2012 below $120,000, probably transfers of a share or not at market: the file has no sale type to mark them, and a price floor of our own would filter on the target (as house_sales and house_prices_nominal).
        - Note: December 2020 is short (0.71 of November's sales, 0.83-1.04 in 2013-2019; some sales were not yet on the site), but its prices are in line, so it stays the newest test window (decision table).
        - Licence: CC BY-NC-SA 4.0 (Kaggle data card); the terms of the scraped site are not stated.
    """

    # Task
    target = "log_PRICE"
    problem_type = "regression"
    metric = Metric.fallback(
        reason="Kaggle dataset (scraped listings), no task or metric defined by the source; regression default rmse on the log target."
    )

    # Splits: 9 monthly windows (the 3 x 3 an IID task of this size would get), April to December 2020.
    temporal = Temporal(on="DATE_SOLD", splits=TemporalSplits(window=1, unit="months", n_windows=9))
    splits_comment = """
        A price model refit at the start of every month predicts that month's sales: 9 test windows of one calendar month, December 2020 back to April 2020, newest first, each trained on all earlier sales (88-99% of the rows). The source dates sales by month only. An IID task of this size would get 3 x 3 splits; the windows hold 284-628 sales. No gap: many sales reach the site within days (an archived page of 14 April 2021 lists four sales of April 2021 among the 10 newest of Mount Lawley), and a month after its end December 2020 held about 80% of its usual share of November's count. At the source's month resolution the smallest gap drops the whole previous month, more than the delay.
    """
    accepted_check_warnings = {
        "meta_time_horizon_mismatch": "`DATE_SOLD` holds the first day of the sale month (the source gives no day), "
        "so each one-month test window holds a single date and its span reads as 1 day; the windows are calendar "
        "months (as zillow_prize).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # Missing values are "NULL" (GARAGE, BUILD_YEAR) or empty (NEAREST_SCH_RANK); no other token means missing.
        return pd.read_csv(raw_dir / RAW_FILE, keep_default_na=False, na_values=["NULL", ""])

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # The month of the sale, "09-2018" followed by a carriage return in the file.
        df["DATE_SOLD"] = df["DATE_SOLD"].str.strip()
        sold = pd.to_datetime(df["DATE_SOLD"], format="%m-%Y")
        # Sales dated before the year the house was built: the row describes a house built after the sale.
        df = df[~(df["BUILD_YEAR"] > sold.dt.year)]
        # One sale geocoded to several address points: rows identical except the coordinates.
        df = df[~df.duplicated(subset=[c for c in df.columns if c not in COORDINATE_COLUMNS], keep="first")]
        # Proxy missing values.
        df["LAND_AREA"] = df["LAND_AREA"].mask(df["LAND_AREA"] == 999999)
        df["GARAGE"] = df["GARAGE"].mask(df["GARAGE"] == 99)
        # Impossible values: a house of 2+ bedrooms on 1-40 m2, more bathrooms than bedrooms + 2 (16 in 95 m2).
        df["FLOOR_AREA"] = df["FLOOR_AREA"].mask((df["FLOOR_AREA"] <= 40) & (df["BEDROOMS"] >= 2))
        df["BATHROOMS"] = df["BATHROOMS"].mask(df["BATHROOMS"] > df["BEDROOMS"] + 2)
        # Station and school as of the scrape: blank them for a sale before they opened.
        sold = pd.to_datetime(df["DATE_SOLD"], format="%m-%Y")
        station_opened = pd.to_datetime(
            df["NEAREST_STN"].map({f"{name} Station": month for name, month in STATION_OPENED.items()})
        )
        df.loc[sold < station_opened, ["NEAREST_STN", "NEAREST_STN_DIST"]] = np.nan
        school_opened = pd.to_datetime(df["NEAREST_SCH"].map(SCHOOL_OPENED))
        df.loc[sold < school_opened, ["NEAREST_SCH", "NEAREST_SCH_DIST", "NEAREST_SCH_RANK"]] = np.nan
        # `Vic` names Victoria Street (Mosman Park, west) and Victoria Park, 14 km apart.
        is_vic = df["NEAREST_STN"] == "Vic"
        df.loc[is_vic, "NEAREST_STN"] = np.where(
            df.loc[is_vic, "LONGITUDE"] < 115.8, "Victoria Street Station", "Victoria Park Station"
        )
        # Target: the log of the sale price, renamed in place.
        df = df.rename(columns={"PRICE": "log_PRICE"})
        df["log_PRICE"] = np.log(df["log_PRICE"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["SUBURB", "POSTCODE", "NEAREST_STN", "NEAREST_SCH"],
            string=["ADDRESS"],
            datetime={"DATE_SOLD": "%m-%Y"},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        sold = pd.to_datetime(raw["DATE_SOLD"].str.strip(), format="%m-%Y")

        # Sales dated before the build year, by how many years the house was built after the sale.
        gap = raw["BUILD_YEAR"] - sold.dt.year
        spans = {"1 year": (1, 1), "2 years": (2, 2), "3-5 years": (3, 5), "over 5 years": (6, 1000)}
        before_build = pd.DataFrame(
            {
                "sales": {k: int(gap.between(lo, hi).sum()) for k, (lo, hi) in spans.items()},
                "sold in": {
                    k: f"{sold[gap.between(lo, hi)].dt.year.min()}-{sold[gap.between(lo, hi)].dt.year.max()}"
                    for k, (lo, hi) in spans.items()
                },
            }
        )
        before_build.index.name = "built after the sale by"

        # The newest sales of each suburb: when a suburb's rows start, by how many rows it has (the raw file).
        per_suburb = sold.groupby(raw["SUBURB"]).agg(["size", "min"])
        per_suburb["rows in the file"] = pd.cut(
            per_suburb["size"], bins=[0, 50, 100, 150, 250], labels=["1-50", "51-100", "101-150", "151-231"]
        )
        coverage = per_suburb.groupby("rows in the file", observed=True).agg(
            suburbs=("size", "size"),
            **{
                "median first sale": ("min", lambda s: s.median().strftime("%Y-%m")),
                "latest first sale": ("min", lambda s: s.max().strftime("%Y-%m")),
            },
        )

        # Sales per month at the end of the year (the curated frame): December 2020 is short.
        counts = df["DATE_SOLD"].dt.to_period("M").value_counts()
        end_of_year = pd.DataFrame(
            {
                month: {year: int(counts.get(pd.Period(f"{year}-{number}", "M"), 0)) for year in range(2013, 2021)}
                for month, number in (("October", 10), ("November", 11), ("December", 12))
            }
        )
        end_of_year.index.name = "year"
        end_of_year["December / November"] = (end_of_year["December"] / end_of_year["November"]).round(2)

        # The address carries the property type the upload dropped (the curated frame).
        address_text = df["ADDRESS"].astype(str)
        kind = pd.Series(
            np.select(
                [address_text.str.contains("/"), address_text.str.match(r"^\d+[A-Za-z]\b")],
                ["unit number (10/23 ...)", "lettered lot (12A ...)"],
                default="plain street number",
            ),
            index=df.index,
            name="address",
        )
        address = (
            df.assign(PRICE=np.exp(df["log_PRICE"]).round(-2))
            .groupby(kind)[["PRICE", "LAND_AREA", "FLOOR_AREA", "BEDROOMS"]]
            .median()
        )
        address.columns = [f"median {c}" for c in address.columns]
        address.insert(0, "sales", kind.value_counts())
        address = address.loc[["plain street number", "lettered lot (12A ...)", "unit number (10/23 ...)"]]

        # The top of the target (the curated frame): the yearly maximum stops at $2.40-2.44M.
        price = np.exp(df["log_PRICE"]).round(-2)
        year = df["DATE_SOLD"].dt.year
        recent = year >= 2011
        cap = pd.DataFrame(
            {
                "sales": year[recent].value_counts().sort_index(kind="stable"),
                "maximum price": price[recent].groupby(year[recent]).max().astype(int),
                "sales at $2M or more": (price[recent] >= 2_000_000).groupby(year[recent]).sum().astype(int),
            }
        )
        cap.index.name = "year"

        # Sales before their station or school opened (the raw file, after the build-year drop).
        kept = raw[~(gap > 0)]
        kept_sold = sold[~(gap > 0)]
        rows = {}
        for column, opened_map in (("NEAREST_STN", STATION_OPENED), ("NEAREST_SCH", SCHOOL_OPENED)):
            keys = {f"{k} Station": v for k, v in opened_map.items()} if column == "NEAREST_STN" else opened_map
            before = kept_sold < pd.to_datetime(kept[column].map(keys))
            for name, n in kept.loc[before, column].value_counts().items():
                years = kept_sold[before & (kept[column] == name)].dt.year
                rows[name] = {"opened": keys[name], "sales before": int(n), "sold in": f"{years.min()}-{years.max()}"}
        anachronisms = pd.DataFrame(rows).T
        anachronisms.index.name = "station or school"

        return [
            Decision(
                "No sale above $2,440,000: a truncated target, kept and documented",
                "The upload stops at $2,440,000 in every year, with one sale at that price, although the site lists "
                "dearer sales (17 McNeil Street, Peppermint Grove, $5,200,000 in June 2013): the dearer sales are "
                "absent, not set to the ceiling. Nothing in the source gives them back, so the task is the price of "
                "a sale up to $2.44M.",
                cap,
            ),
            Decision(
                "Sales dated before the build year dropped",
                "563 sales describe a house built 1 to 23 years after the sale: a land or off-the-plan sale, not the "
                "sale of the house the valuation prices. LightGBM prices them 0.1-0.5 log units too high on average, "
                "by setup. All are older than the test windows; the 140 sales in the build year stay.",
                before_build,
            ),
            Decision(
                "Station and school blanked for sales before they opened",
                "The nearest station and school are as of the scrape; a sale before the opening names one that did "
                "not exist, so its name and distance (and the school's rank) are set to missing.",
                anachronisms,
            ),
            Decision(
                "Each suburb holds its newest sales only",
                "Busy suburbs start in 2018-2020, quiet ones reach back decades, so old training years are thin; "
                "the test windows (April-December 2020) hold the newest sales of every suburb.",
                coverage,
            ),
            Decision(
                "December 2020 kept as the newest window",
                "December 2020 holds fewer sales than usual relative to November (sales not yet on the site at "
                "the scrape), but its prices relative to each suburb's median are in line with the months before.",
                end_of_year,
            ),
            Decision(
                "ADDRESS kept as text",
                "Unit numbers and lettered lots mark strata units and subdivided blocks, the property type the "
                "upload dropped.",
                address,
            ),
        ]
