"""Curated dataset definition for `house_sales` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import zipfile
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

SALES_FILE = "kc_house_data.csv"
CHANGE_LOG_ZIP = "Change History Detail.zip"
BUILDINGS_ZIP = "Residential Building.zip"
SALES_ZIP = "Real Property Sales.zip"
CHANGES_FILE = "house_sales_changes.csv"  # prepared: the change log of the file's parcels, for the attributes below
BATHS_FILE = "house_sales_bath_counts.csv"  # prepared: today's bathroom counts of building 1 of the file's parcels
WARNINGS_FILE = "house_sales_sale_warnings.csv"  # prepared: the county's sale warnings of the file's parcels, 2014-15

# The sales of May 2015 are incomplete: the sales list was extracted in mid-May 2015.
FIRST_INCOMPLETE_MONTH = "20150501"
# The house features are the assessor's record as of 18-19 July 2015 (a weekend): they hold the changes dated up to
# 17 July 2015 and none dated from 20 July on.
SNAPSHOT = pd.Timestamp("2015-07-18")
# (record, attribute) of the change log -> the column of the file it sets
CHANGED_COLUMNS = {
    ("Bldg 1", "BldgGrade"): "grade",
    ("Bldg 1", "Condition"): "condition",
    ("Bldg 1", "SqFtTotLiving"): "sqft_living",
    ("Bldg 1", "SqFtFinBasement"): "sqft_basement",
    ("Bldg 1", "Bedrooms"): "bedrooms",
    ("Bldg 1", "Stories"): "floors",
    ("Bldg 1", "YrBuilt"): "yr_built",
    ("Bldg 1", "YrRenovated"): "yr_renovated",
    ("Land", "SqFtLot"): "sqft_lot",
    ("LandFootage", "SqFtLot"): "sqft_lot",  # the lot size changes are logged under this record
}
REBUILT_COLUMNS = list(dict.fromkeys(CHANGED_COLUMNS.values()))
# The county's sale warnings (lookup type 7 of EXTR_LookUp) that mark a sale as not at market value
NON_MARKET_WARNINGS = {
    "15": "no market exposure",
    "46": "non-representative sale",
    "60": "short sale",
    "51": "related party, friend, or neighbor",
    "23": "forced sale",
    "13": "bankruptcy - receiver or trustee",
}
# Living areas under this many sq ft with bedrooms recorded are placeholders of houses under construction
MIN_LIVING_AREA = 250
# `bathrooms` counts a full bath as 1, a three-quarter bath as 0.75 and a half bath as 0.5
BATH_WEIGHTS = {"BathFullCount": 1.0, "Bath3qtrCount": 0.75, "BathHalfCount": 0.5}
CONDITION = {"Poor": 1, "Fair": 2, "Average": 3, "Good": 4, "Very Good": 5}
# a blank value means none for these attributes, and an unknown value for the others
BLANK_IS_ZERO = ("SqFtFinBasement", "YrRenovated", *BATH_WEIGHTS)


def _parse_values(attribute: pd.Series, value: pd.Series) -> pd.Series:
    """The change log's text values in the file's units: grade "7  Average" -> 7, condition "Good" -> 4, numbers."""
    out = pd.to_numeric(value, errors="coerce").astype(float)
    grade = (attribute == "BldgGrade").to_numpy()
    out[grade] = pd.to_numeric(value[grade].str.extract(r"^(\d+)", expand=False), errors="coerce").to_numpy()
    condition = (attribute == "Condition").to_numpy()
    out[condition] = value[condition].map(CONDITION).astype(float).to_numpy()
    out[(attribute.isin(BLANK_IS_ZERO) & (value == "")).to_numpy()] = 0.0
    return out


def _parse_changes(changes: pd.DataFrame) -> pd.DataFrame:
    """The prepared change log with its update time parsed and its old values in the file's units (`old`)."""
    return changes.assign(
        updated=pd.to_datetime(changes["updated"], format="%Y-%m-%d %H:%M"),
        old=_parse_values(changes["attribute"], changes["value"]),
    )


def _first_changes(changes: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    """The earliest change per group of ``keys`` (by update time, then event)."""
    order = changes.sort_values([*keys, "updated", "event"], kind="stable")
    return order.groupby(keys, sort=False).head(1)


def _sale_codes(sales: pd.DataFrame, warnings: pd.DataFrame) -> pd.Series:
    """The county's sale warning codes of each sale (a set; empty when unflagged or unmatched).

    A sale matches the county's sales on parcel, deed date and price; a sale with several matching county records takes
    the codes of all of them.
    """
    keys = pd.DataFrame(
        {"row": np.arange(len(sales)), "id": sales["id"].to_numpy(), "date": sales["date"].str[:8].to_numpy()}
    )
    keys["price"] = sales["price"].round().astype("int64").to_numpy()
    matched = keys.merge(warnings, on=["id", "date", "price"])
    codes = matched.groupby("row")["warning"].agg(lambda w: set(" ".join(w).split()))
    return codes.reindex(np.arange(len(sales))).apply(lambda c: c if isinstance(c, set) else set())


def _market_sales(sales: pd.DataFrame, warnings: pd.DataFrame) -> pd.DataFrame:
    """The sales without a county warning that marks them as not at market value (`NON_MARKET_WARNINGS`)."""
    non_market = _sale_codes(sales, warnings).apply(lambda c: bool(c & set(NON_MARKET_WARNINGS))).to_numpy()
    return sales[~non_market]


def _as_of_sale(sales: pd.DataFrame, changes: pd.DataFrame, bath_counts: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Rebuild the house features as the assessor's record stood on each sale's day.

    A change between the sale and the snapshot means that the file shows a value the record did not hold at the sale:
    the old value of the first such change is the value at the sale. Returns the frame and counts for the comments.
    """
    out = sales.reset_index(drop=True)
    sale_day = pd.to_datetime(out["date"].str[:8], format="%Y%m%d")
    rows = pd.DataFrame({"row": np.arange(len(out)), "id": out["id"].to_numpy(), "sale": sale_day.to_numpy()})
    post = changes.merge(rows, on="id")
    post = post[(post["updated"].dt.normalize() > post["sale"]) & (post["updated"] < SNAPSHOT)]
    first = _first_changes(post, ["row", "record", "attribute"])
    stats: dict = {"blank": 0}

    for (record, attribute), column in CHANGED_COLUMNS.items():
        hit = first[(first["record"] == record) & (first["attribute"] == attribute)]
        stats["blank"] += int(hit["old"].isna().sum())
        hit = hit[hit["old"].notna()]  # an unknown old value leaves the file's value
        dtype = out[column].dtype
        values = out[column].to_numpy(dtype=float, copy=True)
        values[hit["row"].to_numpy()] = hit["old"].to_numpy()
        out[column] = values.astype(dtype) if dtype == np.int64 else values

    # bathrooms: each count at the snapshot is the old value of its first change on or after the snapshot, else
    # today's count; a count changed after the sale held the old value of its first such change at the sale
    baths = changes[(changes["record"] == "Bldg 1") & changes["attribute"].isin(list(BATH_WEIGHTS))]
    later = _first_changes(baths[baths["updated"] >= SNAPSHOT], ["id", "attribute"])
    today = bath_counts.melt(id_vars="id", value_vars=list(BATH_WEIGHTS), var_name="attribute", value_name="count")
    counts = today.merge(later[["id", "attribute", "old"]], on=["id", "attribute"], how="outer")
    counts["count"] = counts["old"].where(counts["old"].notna(), counts["count"])
    at_snapshot = counts.pivot(index="id", columns="attribute", values="count").reindex(columns=list(BATH_WEIGHTS))
    # the counts at the snapshot must give the file's `bathrooms`, else the record's history is not complete
    file_baths = (at_snapshot * pd.Series(BATH_WEIGHTS)).sum(axis=1, min_count=len(BATH_WEIGHTS))
    at_sale = first[(first["record"] == "Bldg 1") & first["attribute"].isin(list(BATH_WEIGHTS))]
    snapshot_counts = counts[["id", "attribute", "count"]].rename(columns={"count": "snapshot"})
    at_sale = at_sale.merge(snapshot_counts, on=["id", "attribute"], how="left")
    term = (at_sale["old"] - at_sale["snapshot"]) * at_sale["attribute"].map(BATH_WEIGHTS)
    delta = term.groupby(at_sale["row"]).sum()
    delta[term.isna().groupby(at_sale["row"]).any()] = np.nan
    positions = delta.index.to_numpy()
    reliable = np.isclose(
        file_baths.reindex(out["id"].to_numpy()[positions]).to_numpy(), out["bathrooms"].to_numpy()[positions]
    )
    reliable &= delta.notna().to_numpy()
    stats["baths_rebuilt"] = int(reliable.sum())
    stats["baths_kept"] = int((~reliable).sum())
    bathrooms = out["bathrooms"].to_numpy().copy()
    bathrooms[positions[reliable]] += delta.to_numpy()[reliable]
    out["bathrooms"] = bathrooms

    # the area above ground is the living area without the finished basement, as in every row of the file
    out["sqft_above"] = out["sqft_living"] - out["sqft_basement"]
    stats["rows"] = int(
        (
            out[[*REBUILT_COLUMNS, "bathrooms"]].fillna(-1).to_numpy()
            != sales.reset_index(drop=True)[[*REBUILT_COLUMNS, "bathrooms"]].fillna(-1).to_numpy()
        )
        .any(axis=1)
        .sum()
    )
    return out, stats


class HouseSales(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What price will a house in King County, Washington, sell for?",
        use_case=(
            "The county assessor's mass appraisal, or an automated valuation model that works from public records, "
            "estimates the price a house sells for from the assessor's record of the house on the sale day and its "
            "location, before the sale is recorded, trained on the sales recorded earlier."
        ),
        row=(
            "One market sale of a house in King County, Washington (the Seattle area), May 2014 to April 2015 "
            "(19,906 sales)."
        ),
        predicted="The sale price, on a log scale; prices range from $75,000 to $7.7 million.",
        known=(
            "The sale date, the location (coordinates and ZIP code) and the assessor's record of the house on the "
            "sale day: living, basement and lot area, bedrooms, bathrooms, floors, year built and renovated, grade "
            "and condition. A view index, waterfront and the neighbours' areas are as of July 2015. The assessed "
            "value and the house's previous sale price are not included."
        ),
        split=(
            "Each test window is three weeks of sales, nine windows from late October 2014 to April 2015, newest "
            "first; training is all sales up to a week before the window."
        ),
        changes=(
            "The file holds the assessor's record of July 2015, after every sale; we rebuild each house as of its "
            "sale day from the county's change log. We drop the 1,061 sales the county flags as not at market value "
            "(such as short sales and sales between relatives) and May 2015, which the extract cut short, and split "
            "by sale date with a one-week gap for the recording of a sale."
        ),
        fit="direct",
        fit_reason=(
            "The features are the assessor's record on the sale day, which a mass appraisal works from. A small "
            "remnant from July 2015 stays: view, waterfront and the neighbours' areas changed after the sale for "
            "about 145 rows (masking them: RMSE 0.2147 against 0.2132), and the 1,073 sales the county flags as "
            "changed since the sale stay as noise."
        ),
    )

    # Dataset
    unique_name = "house_sales"
    year = "2015"
    domain = "business & marketing"
    source = "GOV Website"  # King County's recorded sales; the file is a course cut of them, downloaded from Kaggle
    source_url = "https://info.kingcounty.gov/assessor/DataDownload/default.aspx"
    license = "CC0 1.0 Public Domain"
    data_tags = ("Spatial",)
    download_description = """
        kc_house_data.csv is a cut of the sales and property records of the King County Department of Assessments
        (21,386 of its 21,613 rows match a recorded sale on parcel, date and price), first distributed with the
        University of Washington's Machine Learning Specialization on Coursera (2015; course-2/kc_house_data.gl.zip in
        https://github.com/learnml/machine-learning-specialization is dated 2015-11-06; its contents not checked).

        We download kc_house_data.csv from Kaggle (21,613 rows; md5 b1e7bdf4f3e61792c0979a5697dc7145) and three extracts of the King County Department of Assessments (https://info.kingcounty.gov/assessor/DataDownload/default.aspx): the change log of the property records (1.8 GB), the residential building file and the real property sales (150 MB). The county updates them every week; the definition reads the changes of 2014 and later for the file's parcels, today's bathroom counts only where no later change records them, and the 2014-2015 sales of the file's parcels (parcel, deed date, price and sale warnings; no names).

        mkdir -p local-data-warehouse/house_sales
        kaggle datasets download harlfoxem/housesalesprediction -p local-data-warehouse/house_sales
        unzip local-data-warehouse/house_sales/housesalesprediction.zip -d local-data-warehouse/house_sales
        rm local-data-warehouse/house_sales/housesalesprediction.zip
        wget -O "local-data-warehouse/house_sales/Change History Detail.zip" "https://aqua.kingcounty.gov/extranet/assessor/Change%20History%20Detail.zip"
        wget -O "local-data-warehouse/house_sales/Residential Building.zip" "https://aqua.kingcounty.gov/extranet/assessor/Residential%20Building.zip"
        wget -O "local-data-warehouse/house_sales/Real Property Sales.zip" "https://aqua.kingcounty.gov/extranet/assessor/Real%20Property%20Sales.zip"

        The first build filters the extracts to three files in the same folder. With the downloads of 2026-10-07 (change log, building file) and 2026-10-19 (sales) their md5 are: house_sales_changes.csv 06491065b3ddbc8b0d9d20fb82444cad, house_sales_bath_counts.csv dc04ef1d66b0f1374a5b541bfb76c9ea, house_sales_sale_warnings.csv 06e45bc786381590dfcf24822e1ce221. A different md5 after a new download means the county changed its 2014-2015 records.
    """
    bibtex = r"""
        @misc{fox2015kchousedata,
          author = {Fox, Emily and Guestrin, Carlos},
          title = {kc\_house\_data: House sales in King County, Washington},
          year = {2015},
          howpublished = {Machine Learning Specialization, University of Washington, Coursera; \url{https://www.coursera.org/specializations/machine-learning}},
          note = {Re-uploaded to Kaggle in 2016 as harlfoxem/housesalesprediction}
        }
        @misc{kingcounty2015assessor,
          author = {{King County Department of Assessments}},
          title = {Assessor data download: real property sales, residential building and change history extracts},
          year = {2015},
          howpublished = {\url{https://info.kingcounty.gov/assessor/DataDownload/default.aspx}}
        }
    """
    curation_comments = """
        We start with kc_house_data.csv from Kaggle: 21,613 sales of houses in King County, Washington, dated 2014-05-02 to 2015-05-27. Three extracts of the King County Department of Assessments give the house as it stood at each sale and the county's flags on each sale.

        - Prediction point: a house sells, and the assessor's mass appraisal or a public-record valuation model estimates its price from the assessor's record on the sale day and its location, trained on the sales recorded earlier. The assessed value and the previous sale price are not in the file.
        - We drop the 1,061 sales (5.1%) whose county record carries a warning for a sale not at market value: 15 no market exposure, 46 non-representative, 60 short sale, 51 related party, 23 forced sale, 13 bankruptcy (`_market_sales`, decision table). Sales are matched on parcel, deed date and price (20,742 of the 20,967 sales before May 2015; the other 225 stay). These sales sat 0.14 to 0.23 below an untuned LightGBM on the log scale; teardowns (10) and segregations (29) did not (-0.02 and +0.05), so they stay.
        - The file's house features are the assessor's record as of 18-19 July 2015, after every kept sale (decision table). For 2,188 of the 19,906 kept rows the record changed between the sale and then, mostly upward, and untuned LightGBM scored better on the changed rows with the file's values (RMSE 0.156 against 0.208 with the record at the sale, 9 windows, measured before the non-market filter). These values are recorded after the outcome, so we rebuild each row as of its sale day.
        - The rebuild (`_as_of_sale`): each of `grade`, `condition`, `sqft_living`, `sqft_basement`, `bedrooms`, `floors`, `yr_built`, `yr_renovated` and `sqft_lot` (logged under the `Land` and `LandFootage` records) whose attribute changed after the sale day and before 18 July 2015 takes the old value of its first such change. `bathrooms` (full, three-quarter and half baths) is rebuilt from the three counts where their history gives the file's value, and kept for the 5 rows where it does not. `sqft_above` is `sqft_living` minus `sqft_basement` (the finished basement), as in every row of the file. `_prepare_raw_files` cuts the extracts down to the file's parcels.
        - Potential leak, kept on purpose: `view` (the file's 0-4 index, not a county attribute), `waterfront`, `sqft_living15` and `sqft_lot15` (the neighbours' areas) are as of July 2015. About 145 rows had a view or waterfront rating changed after the sale (39 gained a view); masking their `view` gives RMSE 0.2147 against 0.2132 kept, and dropping the neighbours' areas changes the changed rows by 0.004. Blanking them would make the missing value mark a change after the sale, so they stay, as do the 11 values whose old value is blank, the 5 bathroom rows and about 24 rows whose building record was entered in full after the sale. Revisit if a county view rating history becomes usable.
        - The 1,073 kept sales the county flags with warning 26, "IMP. CHARACTERISTICS CHANGED SINCE SALE", stay as noise: 944 of them are not rebuilt because their changes come after July 2015, and they sell below the model (-0.12), so the file holds the record at the sale.
        - Anomaly: the record at the sale describes what was sold, so `yr_built` is rebuilt for 22 rows, mostly teardowns. 5 houses under construction carry a placeholder living area of 8 to 200 sq ft with bedrooms recorded; we set their `sqft_living` and `sqft_above` to missing and keep the rows (the 290 sq ft house without bedrooms stays).
        - We drop the 646 sales of May 2015 (3.0%): the bulk of the sales list stops on 15 May 2015 (5 sales recorded up to 2 June), so the month is incomplete, and its quickly recorded sales are cheaper (decision table).
        - We keep the repeated sales of one house (120 houses sold twice): under the temporal split the earlier sale is in the past, and LightGBM predicted resales worse than the other test rows (RMSE 0.27 against 0.17, measured before the non-market filter).
        - We drop `id`, the parcel number. `_load_raw` reads it and `zipcode` as text to keep the leading zeros.
        - `yr_renovated` = 0 means never renovated (GeoDa: "'0' if never renovated"); we set it to missing, so missing means "never renovated". 0 bedrooms or 0 bathrooms at the sale are unrecorded values; we set them to missing.
        - Target: `log_price`, the log of the sale price ($75,000 to $7.7M).
        - `zipcode` is categorical, and `date` (the sale date) is a datetime and the time column.
        - No duplicate rows. Different parcels can share every feature but the date and the price (townhouses built together); one pair also shares the date and was sold at two prices (the conflicting duplicate the checks report); we keep them.
    """

    # Task
    target = "log_price"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason="Neither the King County assessor extracts nor the Kaggle dataset card define a task metric (the Coursera course that first distributed kc_house_data used RSS/RMSE on the raw price as a teaching exercise, not a benchmark definition). For a sale price the error that matters is relative to the price (prices range from $75,000 to $7.7 million), so RMSLE on the price.",
        target_transform="log",
    )

    # Splits
    temporal = Temporal(
        on="date", splits=TemporalSplits(window=3, unit="weeks", n_windows=9, min_train_fraction=0.5, gap=1)
    )
    splits_comment = """
        9 test windows of three weeks (21 days), from 10-30 April 2015 back to 24 October-13 November 2014, newest first, each trained on the sales up to one week before the window. The gap is the delay before a sale is recorded and a refit can learn its price: from the deed date to the recording date the delay has a median of 6 days, and 91% of sales are recorded within 14 days. The window length follows the window count, not a refit cadence the source states: nine windows are the 3 x 3 splits an IID task of this size gets; they hold 617 to 1,458 sales each, and the oldest trains on 52% of the rows. Calendar months (a monthly refit) would give 6 windows of 911 to 2,084 sales. With one year of data the windows cover late October to April only, and the training history is under one year.
    """

    prepared_raw_files = (CHANGES_FILE, BATHS_FILE, WARNINGS_FILE)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        ids = set(pd.read_csv(raw_dir / SALES_FILE, usecols=["id"], dtype=str)["id"])
        attributes = {attribute for _, attribute in CHANGED_COLUMNS} | set(BATH_WEIGHTS)
        records = {record for record, _ in CHANGED_COLUMNS}
        columns = ["Major", "Minor", "EventId", "Id", "Attribute", "AttributeValue", "UpdateDate"]
        parts = []
        with zipfile.ZipFile(raw_dir / CHANGE_LOG_ZIP) as archive:
            (member,) = [name for name in archive.namelist() if name.lower().endswith(".csv")]
            with archive.open(member) as handle:
                reader = pd.read_csv(
                    handle, dtype=str, keep_default_na=False, encoding="latin-1", usecols=columns, chunksize=1_000_000
                )
                for block in reader:
                    rows = block[
                        block["Attribute"].str.strip().isin(attributes) & block["Id"].str.strip().isin(records)
                    ]
                    rows = rows.apply(lambda s: s.str.strip())
                    parcel = rows["Major"].str.zfill(6) + rows["Minor"].str.zfill(4)
                    year = rows["UpdateDate"].str.split().str[2]
                    parts.append(rows[parcel.isin(ids) & (year >= "2014")].assign(id=parcel))
        log = pd.concat(parts, ignore_index=True)
        updated = pd.to_datetime(log["UpdateDate"].str.split().str.join(" "), format="%b %d %Y %I:%M%p")
        log = pd.DataFrame(
            {
                "id": log["id"],
                "record": log["Id"],
                "attribute": log["Attribute"],
                "value": log["AttributeValue"],
                "updated": updated.dt.strftime("%Y-%m-%d %H:%M"),
                "event": log["EventId"].astype("int64"),
            }
        )
        log = log.sort_values(["id", "record", "attribute", "updated", "event"], kind="stable")
        log.to_csv(raw_dir / CHANGES_FILE, index=False)

        with zipfile.ZipFile(raw_dir / BUILDINGS_ZIP) as archive, archive.open("EXTR_ResBldg.csv") as handle:
            buildings = pd.read_csv(
                handle,
                dtype=str,
                keep_default_na=False,
                encoding="latin-1",
                usecols=["Major", "Minor", "BldgNbr", *BATH_WEIGHTS],
            ).apply(lambda s: s.str.strip())
        buildings["id"] = buildings["Major"].str.zfill(6) + buildings["Minor"].str.zfill(4)
        buildings = buildings[buildings["id"].isin(ids) & (buildings["BldgNbr"] == "1")]
        buildings = buildings.drop_duplicates("id")[["id", *BATH_WEIGHTS]].sort_values("id", kind="stable")
        buildings.to_csv(raw_dir / BATHS_FILE, index=False)

        # the county's sales of the file's parcels in 2014-2015: parcel, deed date, price and sale warnings only
        with zipfile.ZipFile(raw_dir / SALES_ZIP) as archive, archive.open("EXTR_RPSale.csv") as handle:
            county = pd.read_csv(
                handle,
                dtype=str,
                keep_default_na=False,
                encoding="latin-1",
                usecols=["Major", "Minor", "DocumentDate", "SalePrice", "SaleWarning"],
            ).apply(lambda s: s.str.strip())
        county["id"] = county["Major"].str.zfill(6) + county["Minor"].str.zfill(4)
        county = county[county["id"].isin(ids) & county["DocumentDate"].str[-4:].isin(["2014", "2015"])]
        deed = pd.to_datetime(county["DocumentDate"], format="%m/%d/%Y")
        warnings = pd.DataFrame(
            {
                "id": county["id"],
                "date": deed.dt.strftime("%Y%m%d"),
                "price": county["SalePrice"].astype("int64"),
                "warning": county["SaleWarning"],
            }
        )
        warnings = warnings.sort_values(["id", "date", "price", "warning"], kind="stable")
        warnings.to_csv(raw_dir / WARNINGS_FILE, index=False)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        # The parcel number and the ZIP code are codes: read them as text to keep the leading zeros.
        sales = pd.read_csv(raw_dir / SALES_FILE, dtype={"id": str, "zipcode": str})
        changes = pd.read_csv(
            raw_dir / CHANGES_FILE,
            dtype={"id": str, "record": str, "attribute": str, "value": str},
            keep_default_na=False,
        )
        bath_counts = pd.read_csv(raw_dir / BATHS_FILE, dtype={"id": str})
        warnings = pd.read_csv(
            raw_dir / WARNINGS_FILE, dtype={"id": str, "date": str, "warning": str}, keep_default_na=False
        )
        return {"sales": sales, "changes": changes, "bath_counts": bath_counts, "warnings": warnings}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # The sales of May 2015 are incomplete (the sales list was extracted mid-month); dates read YYYYMMDDT000000.
        df = raw["sales"][raw["sales"]["date"] < FIRST_INCOMPLETE_MONTH]
        # The target is a market price: drop the sales the county flags as not at market value.
        df = _market_sales(df, raw["warnings"])
        # The house features as the assessor's record stood on the day of each sale (see `_as_of_sale`).
        df, _ = _as_of_sale(df, _parse_changes(raw["changes"]), raw["bath_counts"])
        # Proxy missing values: 0 bedrooms or bathrooms are unrecorded; a renovation year of 0 means never renovated.
        for col in ("bedrooms", "bathrooms", "yr_renovated"):
            df[col] = df[col].replace({0: np.nan})
        # A living area of a few sq ft with bedrooms recorded is the placeholder of a house under construction.
        placeholder = (df["sqft_living"] < MIN_LIVING_AREA) & df["bedrooms"].notna()
        df[["sqft_living", "sqft_above"]] = df[["sqft_living", "sqft_above"]].astype(float).mask(placeholder)
        # Target: the log of the sale price, renamed in place.
        df = df.rename(columns={"price": "log_price"})
        df["log_price"] = np.log(df["log_price"])
        return drop_columns(df, ["id"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["zipcode", "waterfront"],  # waterfront is a 0/1 flag (CLEAN-14)
            datetime={"date": "%Y%m%dT%H%M%S"},
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        sales = raw["sales"]
        changes = _parse_changes(raw["changes"])
        before_may = sales[sales["date"] < FIRST_INCOMPLETE_MONTH].reset_index(drop=True)
        kept = _market_sales(before_may, raw["warnings"]).reset_index(drop=True)
        rebuilt, stats = _as_of_sale(kept, changes, raw["bath_counts"])

        # 0. the sales per county warning: dropped when the warning marks a sale not at market value
        codes = _sale_codes(before_may, raw["warnings"])
        flagged = pd.Series([c for row in codes for c in row]).value_counts()
        dropped = codes.apply(lambda c: bool(c & set(NON_MARKET_WARNINGS)))
        per_code = pd.DataFrame(
            {
                "sales": flagged,
                "dropped": flagged.index.isin(list(NON_MARKET_WARNINGS)),
            }
        ).rename_axis("county sale warning")
        per_code = per_code.sort_values("sales", ascending=False, kind="stable")

        # 1. the file's features are the record of mid-July 2015: changes dated before then are in the file (their
        # old value differs from it), changes dated after are not (their old value is the file's value)
        house = sales.drop_duplicates("id").set_index("id")
        building = changes[(changes["record"] == "Bldg 1") & changes["attribute"].isin([a for _, a in CHANGED_COLUMNS])]
        building = building[(building["updated"] >= "2015-06-22") & (building["updated"] < "2015-08-17")]
        column = building["attribute"].map({a: c for (_, a), c in CHANGED_COLUMNS.items()})
        in_file = [house.at[i, c] if i in house.index else np.nan for i, c in zip(building["id"], column)]
        week = building["updated"].dt.to_period("W-SUN").astype(str)
        snapshot = (
            pd.DataFrame({"week of the change": week, "equal": building["old"].to_numpy() == np.asarray(in_file)})
            .groupby("week of the change")["equal"]
            .agg(changes="size", share_old_value_equals_file="mean")
            .round(3)
        )

        # 2. the values rebuilt as of the sale, by column
        columns = [*REBUILT_COLUMNS, "bathrooms", "sqft_above"]
        file_values = kept[columns].astype(float)
        sale_values = rebuilt[columns].astype(float)
        differs = file_values.fillna(-1) != sale_values.fillna(-1)
        revised = pd.DataFrame(
            {
                "rows rebuilt": differs.sum(),
                "file higher": (file_values > sale_values).sum(),
                "file lower": (file_values < sale_values).sum(),
            }
        )

        # 3. the sales of May 2015
        date = pd.to_datetime(sales["date"], format="%Y%m%dT%H%M%S")
        month = date.dt.to_period("M").astype(str)
        per_month = month.value_counts().sort_index(kind="stable").rename("sales in the Kaggle file")
        may = date[month == "2015-05"]
        per_week = ((may.dt.day - 1) // 7).value_counts().sort_index(kind="stable")
        weeks = {0: "May 1-7", 1: "May 8-14", 2: "May 15-21", 3: "May 22-28"}

        # 4. resales per test window: the test rows whose house sold before the window
        kept_date = pd.to_datetime(kept["date"], format="%Y%m%dT%H%M%S")
        windows = self.temporal.splits.splits(df, self.temporal.on)
        resales = {}
        for _, folds in sorted(windows.items()):
            test = df[self.temporal.on].iloc[folds[0][1]]
            start, end = test.min(), test.max()
            in_window = (kept_date >= start) & (kept_date <= end)
            earlier = set(kept.loc[kept_date < start, "id"])
            resales[f"{start.date()} to {end.date()}"] = {
                "test rows": int(in_window.sum()),
                "resales of a house sold before": int(kept.loc[in_window, "id"].isin(earlier).sum()),
            }
        return [
            Decision(
                "Sales the county flags as not at market value dropped",
                f"We match each sale to the county's sales on parcel, deed date and price and drop the "
                f"{int(dropped.sum()):,} sales with a warning for a sale not at market value ("
                + ", ".join(f"{k} {v}" for k, v in NON_MARKET_WARNINGS.items())
                + "). The other warnings stay: a teardown (10) or a segregation (29) is sold at a market price for "
                "the land or the changed lot, and 26 is the county's note that the house changed after the sale.",
                per_code,
            ),
            Decision(
                "House features rebuilt as of each sale from the assessor's change log",
                f"The file shows each house as the assessor recorded it in mid-July 2015, after every sale. For "
                f"{stats['rows']:,} rows the record changed between the sale and then; we use the record as it stood "
                f"on the day of the sale. Bathrooms are rebuilt for {stats['baths_rebuilt']:,} rows and left as in "
                f"the file for {stats['baths_kept']:,}, whose later bathroom history does not add up to the file.",
                revised,
            ),
            Decision(
                "The file's house features are the assessor's record as of 18-19 July 2015",
                "Changes of building 1 dated up to 17 July 2015 are in the file (their old value differs from it); "
                "changes dated from 20 July 2015 on are not (their old value is the file's value).",
                snapshot,
            ),
            Decision(
                "Sales of May 2015 dropped: the sales list was extracted mid-month",
                "The month holds 646 sales against 978-2,231 in the others, nearly all from its first two weeks ("
                + ", ".join(f"{weeks[k]}: {v}" for k, v in per_week.items())
                + "). In the assessor's sales records, 24% of the month's sales of the kind the table holds made it "
                "in, against 80-89% in every earlier month, and the quickly recorded sales that did are cheaper.",
                per_month,
            ),
            Decision(
                "Repeated sales of one house kept",
                "A new sale can be the resale of a known house, and under the temporal split a resale's earlier sale "
                "is history.",
                pd.DataFrame(resales).T.rename_axis("test window"),
            ),
        ]
