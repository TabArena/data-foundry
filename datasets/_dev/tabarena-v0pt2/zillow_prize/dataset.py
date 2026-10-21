"""Curated dataset definition for `zillow_prize` (data-foundry v2). Evidence: README.md."""

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
)


def sales_files() -> dict[str, str]:
    """The sales file of each year (one row per sale with its logerror), as downloaded.

    A function, not a constant: whether `_prepare_raw_files` runs again is decided by a hash of that method and the
    functions it calls, and module constants are not part of the hash.
    """
    return {"2016": "train_2016_v2.csv.zip", "2017": "train_2017.csv.zip"}


LAST_COMPLETE_MONTH = "2017-08-01"
"""Sales on or after this date are dropped: Zillow's 2017 release covers August and September 2017 only in part."""

DELINQUENCY_SNAPSHOT_MONTH = "2016-09-01"
"""Both property files hold one tax-delinquency snapshot of about this month; for earlier sales it is blanked."""

QUALITY_2017_TO_2016 = {1: 10, 2: 10, 3: 7, 4: 7, 5: 7, 6: 7, 7: 4, 8: 4, 9: 1, 10: 10, 11: 10, 12: 12}
"""`buildingqualitytypeid` of properties_2017 on the scale of properties_2016, read off the parcels in both files."""

PRESENCE_FLAGS = (
    "hashottuborspa",
    "fireplaceflag",
    "taxdelinquencyflag",
    "poolcnt",
    "pooltypeid10",
    "pooltypeid2",
    "pooltypeid7",
    "decktypeid",
    "storytypeid",
)
"""Columns that hold one value or nothing (True, "Y", 1, 66 or 7): only their presence carries information."""

CODE_COLUMNS = (
    "fips",
    "airconditioningtypeid",
    "architecturalstyletypeid",
    "buildingclasstypeid",
    "heatingorsystemtypeid",
    "propertylandusetypeid",
    "typeconstructiontypeid",
    "regionidcity",
    "regionidneighborhood",
    "regionidzip",
)
"""Numeric codes of a fixed set (counties, regions, the type ids of the data dictionary): categories."""


class ZillowPrize(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("How far will Zillow's automated home value estimate be from the price a home sells for this month?"),
        use_case=(
            "Before a month starts, Zillow predicts for each home how far its value estimate (the Zestimate) will "
            "miss the sale price, to improve the estimate (Kaggle Zillow Prize, round 1)."
        ),
        row=(
            "One home sale in Los Angeles, Orange or Ventura county, California, January 2016 to July 2017 (153,108 "
            "sales)."
        ),
        predicted=(
            "The log of the Zestimate minus the log of the sale price, as Zillow records it; near zero for most "
            "sales, with 2.1% beyond 0.4 either way, mostly data errors."
        ),
        known=(
            "The sale month and the home's facts from the county property file of the sale's year: location (county, "
            "city, ZIP code, neighbourhood, coordinates), size, rooms, building type, quality and age, lot, pool, "
            "garage, assessed tax values, and tax delinquency for the sales from September 2016 on."
        ),
        split=(
            "Each test window is one month of sales (nine windows, November 2016 to July 2017, newest first); "
            "training is every sale before the preceding month, since Zillow receives sales with a delay."
        ),
        changes=(
            "Each sale takes the property file of its own year, so a 2016 sale never sees the 2017 file; both files "
            "were extracted after some of their sales, so a few home facts may postdate the sale. We blank the tax "
            "delinquency for sales before September 2016 (it was looked up later), drop August and September 2017, "
            "which Zillow released only in part, and split by sale month."
        ),
        fit="approximate",
        fit_reason=(
            "Zillow predicted from much more than the public files: the Zestimate itself, the listing data and the "
            "last sale price were never released, so the inputs are only the county facts. The property files were "
            "extracted after some of their sales, so a few facts may postdate the sale (edits measured for 1-4% of "
            "parcels)."
        ),
    )

    # Dataset
    unique_name = "zillow_prize"
    year = "2017"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/zillow-prize-1"
    license = "Kaggle Competition Rules (data for use in the competition only; no redistribution)"
    data_tags = ("Spatial",)
    download_description = """
        We download the sales and property files of round 1 from Kaggle (the competition rules must be accepted on
        the competition page first). sample_submission.csv is not needed. We keep the zip files as downloaded;
        `_prepare_raw_files` writes the property rows of the sold parcels to two parquet files next to them.

        mkdir -p local-data-warehouse/zillow_prize && cd local-data-warehouse/zillow_prize
        for f in train_2016_v2.csv train_2017.csv properties_2016.csv properties_2017.csv zillow_data_dictionary.xlsx; do
            kaggle competitions download -c zillow-prize-1 -f $f -p .
        done

        Files (md5): train_2016_v2.csv.zip (83d97a3af6718cd3d0047bb9cef5f366), train_2017.csv.zip
        (6b3aa0924226a13b5e50efb7632825b9), properties_2016.csv.zip (9d31981b1921c82c4e413463b89b2d46),
        properties_2017.csv.zip (971daab9c17f95208fb7556ede1b06e3), zillow_data_dictionary.xlsx
        (ee71063852e0a724e2eef1bc86981206; read by no code, it documents the columns).
    """
    bibtex = r"""
        @misc{Zillow2017ZillowPrize,
          author = {{Zillow}},
          title  = {Zillow Prize: Zillow's Home Value Prediction (Zestimate)},
          year   = {2017},
          howpublished = {\url{https://www.kaggle.com/competitions/zillow-prize-1}},
          note   = {Kaggle competition, round 1}
        }
    """
    curation_comments = """
        We start with train_2016_v2.csv and train_2017.csv (home sales in Los Angeles, Orange and Ventura counties) and properties_2016.csv and properties_2017.csv (one row per parcel) from round 1 of the Kaggle competition Zillow Prize.

        - Prediction point: the first day of the sale month, since Zillow pairs each sale with the Zestimate of that day (FAQ). `transaction_month` replaces `transactiondate`.
        - Target: `logerror` = log(Zestimate) - log(SalePrice), rounded to 4 decimals, as in train_2016_v2 and the Evaluation page. The competition scored MAE, which we declare (task_probes.md, rule 6, TP-6).
        - Extreme values, kept: 2.1% of the rows have an absolute logerror above 0.4 and hold 74% of the squared error (decision table). Zillow traces them mostly to data errors such as miskeyed prices; the competition's test kept them.
        - Small signal (task probes no_signal, drift_baseline, unstable), kept: untuned LightGBM with an absolute-error loss (100 trees, row and column subsampling 0.8) beats the train mean in 8 or 9 of the 9 windows, depending on the seed (R^2 about 0.001 to 0.012); squared-error fits do not (3 or 4 of 9). A constant train median loses to the mean in 9 of 9, so the gain comes from the features (task_probes.md, rule 2). Tuned results are pending.
        - Each sale gets its parcel's row from the property file of its year, which keeps the 2016 sale reassessments of properties_2017 out of the 2016 rows. Neither file predates its sales: properties_2016 is a snapshot of about September 2016 and properties_2017 was released in October 2017. Building facts differ between the files for 1.4-2.3% of the parcels sold January to May 2016 (about 1.1% for later 2016 sales) and for 3.2-3.7% of the parcels sold only in 2017, flat by sale month in 2017; the share of 2017 parcels whose tax value moved shows no jump at the sale (0.204-0.217 in every month). So the facts kept are almost always the ones on file before the sale (as in melbourne_housing_market).
        - We drop the sales of August and September 2017 (14,737 rows): Zillow's 2017 release covers them only in part and calls them "a biased sample" (decision table).
        - Note: after 15 October 2016 train_2016_v2 holds only part of the sales (the rest were the public leaderboard), so the November and December 2016 test windows hold 1,826 and 1,739 sales, about 18% of a usual month, and are noisier. The share looks random (absolute logerror above 0.4: 2.2% after, 2.0% before), so we keep them.
        - We drop the 24 sales of 2017 whose parcel has no home facts in properties_2017, as Zillow did for 2016 (discussion 34667).
        - We drop the 19 sales within 31 days of a sale of the same parcel, as the competition does (Data page); other repeat sales stay.
        - `buildingqualitytypeid` (lower is better) is on another scale in properties_2017, where each code comes from one 2016 code (decision table; a crosstab of the data, Zillow publishes no conversion); we map the 2017 values onto the 2016 scale, which holds 8 values (1, 4, 6, 7, 8, 10, 11, 12; 6, 8 and 11 on 8 rows). It stays numeric (ordinal).
        - Each column of `PRESENCE_FLAGS` holds one value or nothing and becomes a boolean (`taxdelinquencyflag` 1 or 0, see below).
        - `taxdelinquencyyear`: the two-digit years (3 to 15, and 99) become four-digit years.
        - `taxdelinquencyflag` and `taxdelinquencyyear` are one snapshot of about August-September 2016 in both files, taken after the sale for the sales of January to August 2016 (1.5% flagged, against 3.1-4.7% per month from September 2016; a sale clears the arrears). Both are missing for the sales before September 2016 (72,157 training rows; the flag is 1 or 0 elsewhere); every test row keeps them, since the snapshot predates every test window. Blanking, keeping and dropping them give the same L1 LightGBM skill within the seed spread (R^2 0.0053-0.0057, 9 windows, 3 seeds, two configs).
        - Zero means "not recorded" and becomes missing in `roomcnt` in every county (all of Los Angeles, 44% of Orange; those homes have a median of 3 bedrooms), in `bathroomcnt` (its zeros lack the counts derived from it), in `bedroomcnt` where the bathrooms are also 0 (large homes, no studios) and in `garagetotalsqft` where `garagecarcnt` is 1 or more (14,981 rows, about 30% of the Orange and Ventura garages).
        - The spa and hot-tub flags (`hashottuborspa`, `pooltypeid10`) are recorded for about half as many parcels in properties_2017 as in properties_2016 (2.2-3.1% of the 2016 sales against 1.5-2.3% of the 2017 sales for `hashottuborspa`); a recording change we keep, since no source says which file is right.
        - Near copies, kept since they differ on some rows: `calculatedbathnbr` equals `bathroomcnt` on 99.98% of the rows, `finishedsquarefeet50` equals `finishedfloor1squarefeet` on 99.5%, `censustractandblock` equals `rawcensustractandblock` on its leading digits on 98.9%.
        - We drop `parcelid` (an identifier), `regionidcounty` (a recoding of `fips`), `assessmentyear` (the sale year minus one, constant within each property file) and `transactiondate`.
        - `CODE_COLUMNS` (fips, the region ids and the type ids of the data dictionary), `propertycountylandusecode` and `propertyzoningdesc` are categories; the census tract-and-block numbers stay numeric: each is a county, tract and block code, so its order follows geography, and it has about 55,000 values.
        - Duplicate rows, kept: 7 rows repeat another row exactly and 39 more repeat another row's features with another logerror. They are separate sales of separate parcels, such as units of one building.
    """

    # Task
    target = "logerror"
    problem_type = "regression"
    metric = "mae"  # the competition's metric

    # Splits: monthly windows, train ending one month before each window.
    splits_comment = """
        Zillow asks for one prediction per home and month, made before the month starts (round 1 scored the sales of October to December 2017 with the data released on 2 October). We simulate a model refit every month that predicts the sales of the next month: 9 monthly test windows (the number of splits an IID task of this size gets), from July 2017 back to November 2016, newest first. Train is every sale before the month that precedes the window (a gap of one month): Zillow receives the sales from the county recorders with a delay, and its 2017 release lacked part of the two newest months. The oldest window trains on 53% of the rows.
    """
    temporal = Temporal(
        on="transaction_month",
        splits=TemporalSplits(window=1, unit="months", n_windows=9, gap=1),
    )
    accepted_check_warnings = {
        "meta_time_horizon_mismatch": "`transaction_month` holds the first day of the sale month (the prediction "
        "point), so each one-month test window holds a single date and its span reads as 1 day; the windows are "
        "calendar months.",
    }

    # The property files have 2,985,217 rows each; `_prepare_raw_files` keeps the rows of the parcels sold in
    # 2016 or 2017 once, and `_load_raw` starts from them.
    prepared_raw_files = ("properties_2016_sold.parquet", "properties_2017_sold.parquet")

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # The text columns, read as text so that codes such as `0100` keep their leading zeros (listed here, not as a
        # module constant, so that the hash of this method covers them).
        text_columns = (
            "hashottuborspa",
            "fireplaceflag",
            "taxdelinquencyflag",
            "propertycountylandusecode",
            "propertyzoningdesc",
        )
        sold = pd.concat([pd.read_csv(raw_dir / name, usecols=["parcelid"]) for name in sales_files().values()])
        for year in sales_files():
            properties = pd.read_csv(
                raw_dir / f"properties_{year}.csv.zip", dtype=dict.fromkeys(text_columns, str), low_memory=False
            )
            properties = properties[properties["parcelid"].isin(sold["parcelid"])]
            properties.to_parquet(raw_dir / f"properties_{year}_sold.parquet", index=False)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        raw = {}
        for year, name in sales_files().items():
            raw[f"sales_{year}"] = pd.read_csv(raw_dir / name, dtype={"transactiondate": str})
            raw[f"properties_{year}"] = pd.read_parquet(raw_dir / f"properties_{year}_sold.parquet")
        return raw

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. Each sale gets its parcel's row from the property file of its year (one row per parcel in each file).
        df = pd.concat(
            [
                raw[f"sales_{year}"].merge(raw[f"properties_{year}"], on="parcelid", how="left", validate="many_to_one")
                for year in sales_files()
            ],
            ignore_index=True,
        )
        date = pd.to_datetime(df["transactiondate"], format="%Y-%m-%d")
        sold_2017 = date.dt.year == 2017

        # 2. August and September 2017 are only partly covered.
        keep = date < LAST_COMPLETE_MONTH
        # 3. Sales of parcels without home facts in their property file (only the parcelid).
        facts = [c for c in raw["properties_2017"].columns if c != "parcelid"]
        keep &= df[facts].notna().any(axis=1)
        df, date, sold_2017 = df[keep], date[keep], sold_2017[keep]

        # 4. A sale within 31 days of the parcel's previous sale: the competition keeps the first one.
        order = pd.DataFrame({"parcelid": df["parcelid"], "date": date}).sort_values(
            ["parcelid", "date"], kind="stable"
        )
        days_since_previous = order.groupby("parcelid")["date"].diff().dt.days.reindex(df.index)
        keep = ~(days_since_previous <= 31)
        df, sold_2017 = df[keep], sold_2017[keep]

        # 5. The prediction point is the first day of the sale month.
        df["transaction_month"] = df["transactiondate"].str.slice(0, 7) + "-01"

        # 6. One value or nothing: presence flags.
        for column in PRESENCE_FLAGS:
            assert df[column].nunique() == 1, column  # a presence flag only when the column has a single value
            df[column] = df[column].notna()

        # 7. The 2017 quality codes on the 2016 scale; two-digit delinquency years as years.
        quality = df["buildingqualitytypeid"]
        df["buildingqualitytypeid"] = quality.where(~sold_2017, quality.map(QUALITY_2017_TO_2016))
        assert df["buildingqualitytypeid"].isna().sum() == quality.isna().sum()  # every 2017 code is mapped
        delinquency = df["taxdelinquencyyear"]
        df["taxdelinquencyyear"] = delinquency + np.where(delinquency > 50, 1900, 2000)
        # The delinquency snapshot was taken after the sales before September 2016 (a sale clears the arrears): unknown.
        before_snapshot = df["transaction_month"] < DELINQUENCY_SNAPSHOT_MONTH
        # The flag becomes 1.0 / 0.0 with missing values (a boolean column cannot hold them for every model).
        df["taxdelinquencyflag"] = df["taxdelinquencyflag"].astype(float).mask(before_snapshot)
        df["taxdelinquencyyear"] = df["taxdelinquencyyear"].mask(before_snapshot)
        # Zero as "not recorded": room counts in every county; no bathrooms only where the counts derived from them
        # (calculatedbathnbr, fullbathcnt) are missing; no bedrooms together with no bathrooms (large homes); no garage
        # area for a garage with cars.
        df["bedroomcnt"] = df["bedroomcnt"].mask((df["bedroomcnt"] == 0) & (df["bathroomcnt"] == 0))
        for column in ("roomcnt", "bathroomcnt"):
            df[column] = df[column].mask(df[column] == 0)
        df["garagetotalsqft"] = df["garagetotalsqft"].mask((df["garagetotalsqft"] == 0) & (df["garagecarcnt"] > 0))

        # 8. The target with the 4 decimals of the source.
        df["logerror"] = df["logerror"].round(4)

        # 9. Codes stored as floats: whole numbers, so their categories read "6037", not "6037.0".
        for column in CODE_COLUMNS:
            df[column] = df[column].astype("Int64")

        return drop_columns(df, ["parcelid", "transactiondate", "regionidcounty", "assessmentyear"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[*CODE_COLUMNS, "propertycountylandusecode", "propertyzoningdesc"],
            datetime={"transaction_month": "%Y-%m-%d"},
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        sales = pd.concat([raw[f"sales_{year}"] for year in sales_files()], ignore_index=True)
        month = sales["transactiondate"].str.slice(0, 7)
        by_month = (
            sales.assign(month=month, above_1=sales["logerror"].abs() > 1)
            .groupby("month")
            .agg(sales=("logerror", "size"), mean_logerror=("logerror", "mean"), share_above_1=("above_1", "mean"))
            .loc[lambda t: t.index >= "2017-01"]
            .round(4)
        )

        codes = {
            year: raw[f"properties_{year}"].set_index("parcelid")["buildingqualitytypeid"].astype("Int64")
            for year in sales_files()
        }
        quality = pd.crosstab(
            codes["2016"].rename("code in properties_2016"), codes["2017"].rename("code in properties_2017")
        )

        error = df["logerror"] - df["logerror"].mean()
        bands = pd.cut(df["logerror"].abs(), [0, 0.1, 0.4, 1, 2, np.inf], include_lowest=True)
        outliers = pd.DataFrame(
            {
                "share of rows": bands.value_counts(normalize=True, sort=False),
                "share of squared error": (error**2).groupby(bands, observed=False).sum() / (error**2).sum(),
                "share of absolute error": error.abs().groupby(bands, observed=False).sum() / error.abs().sum(),
            }
        ).round(4)
        outliers.index = outliers.index.astype(str).rename("absolute logerror")

        return [
            Decision(
                "August and September 2017 dropped",
                "Zillow's 2017 release covers these months only in part and calls them a biased sample; they hold "
                "about twice the share of extreme errors of January to July 2017.",
                by_month,
            ),
            Decision(
                "buildingqualitytypeid of 2017 mapped onto the 2016 scale",
                "The same parcel has another code in properties_2017; each 2017 code comes from one 2016 code "
                "(parcels sold in 2016 or 2017 with a value in both files).",
                quality,
            ),
            Decision(
                "Extreme logerror values kept",
                "Rows with an absolute logerror above 1 are few but hold half of the squared error around the mean, "
                "so they would weigh heavily in RMSE; the competition scored MAE on all sales, the metric we declare.",
                outliers,
            ),
        ]
