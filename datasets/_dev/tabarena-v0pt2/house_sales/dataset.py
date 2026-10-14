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
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

SALES_FILE = "kc_house_data.csv"
CHANGE_LOG_ZIP = "Change History Detail.zip"
BUILDINGS_ZIP = "Residential Building.zip"
CHANGES_FILE = "house_sales_changes.csv"  # prepared: the change log of the file's parcels, for the attributes below
BATHS_FILE = "house_sales_bath_counts.csv"  # prepared: today's bathroom counts of building 1 of the file's parcels

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
}
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
            out[[*CHANGED_COLUMNS.values(), "bathrooms"]].fillna(-1).to_numpy()
            != sales.reset_index(drop=True)[[*CHANGED_COLUMNS.values(), "bathrooms"]].fillna(-1).to_numpy()
        )
        .any(axis=1)
        .sum()
    )
    return out, stats


class HouseSales(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What price will a house in King County, Washington, sell for?",
        use_case=(
            "An automated valuation model, as lenders or property sites run, estimates a house's price on the day it "
            "sells from the county assessor's record and its location, trained on all earlier sales."
        ),
        row=(
            "One sale of a house in King County, Washington (the Seattle area), May 2014 to April 2015 (20,967 sales)."
        ),
        predicted="The sale price, on a log scale; prices range from $75,000 to $7.7 million.",
        known=(
            "The sale date, the location (coordinates and ZIP code) and the assessor's record of the house on the "
            "sale day: living, basement and lot area, bedrooms, bathrooms, floors, year built and renovated, grade "
            "and condition. A view index, waterfront and the neighbours' areas are as of July 2015."
        ),
        split=(
            "Each test window is three weeks of sales, nine windows from late October 2014 to April 2015, newest "
            "first; training is all earlier sales."
        ),
        changes=(
            "The file holds the assessor's record of July 2015, after every sale; we rebuild each house as of its "
            "sale day from the county's change log. We drop May 2015, which the extract cut short, and split by sale "
            "date."
        ),
        fit="direct",
        fit_reason=(
            "The features describe the house as it was sold, and the windows follow a model refit every three weeks. "
            "A few values (view, waterfront, neighbours' areas) are still from July 2015, and the 1,225 sales the "
            "county flags as changed since the sale stay as noise."
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
        https://github.com/learnml/machine-learning-specialization holds the same table).

        We download kc_house_data.csv from Kaggle (21,613 rows; md5 b1e7bdf4f3e61792c0979a5697dc7145) and two extracts of the King County Department of Assessments (https://info.kingcounty.gov/assessor/DataDownload/default.aspx): the change log of the property records (1.8 GB) and the residential building file. The county updates both every week; the definition reads the changes of 2014 and later for the file's parcels, and today's bathroom counts only where no later change records them.

        mkdir -p local-data-warehouse/house_sales
        kaggle datasets download harlfoxem/housesalesprediction -p local-data-warehouse/house_sales
        unzip local-data-warehouse/house_sales/housesalesprediction.zip -d local-data-warehouse/house_sales
        rm local-data-warehouse/house_sales/housesalesprediction.zip
        wget -O "local-data-warehouse/house_sales/Change History Detail.zip" "https://aqua.kingcounty.gov/extranet/assessor/Change%20History%20Detail.zip"
        wget -O "local-data-warehouse/house_sales/Residential Building.zip" "https://aqua.kingcounty.gov/extranet/assessor/Residential%20Building.zip"

        The first build filters the change log to house_sales_changes.csv and house_sales_bath_counts.csv in the same folder.
    """
    bibtex = r"""
        @misc{harlfoxem2016housesales,
          author = {harlfoxem},
          title = {House Sales in King County, USA},
          year = {2016},
          howpublished = {\url{https://www.kaggle.com/datasets/harlfoxem/housesalesprediction}},
          note = {Kaggle dataset; first distributed as kc\_house\_data with the University of Washington's Machine Learning Specialization on Coursera (2015)}
        }
    """
    curation_comments = """
        We start with kc_house_data.csv from Kaggle: 21,613 sales of houses in King County, Washington, dated 2014-05-02 to 2015-05-27. Two extracts of the King County Department of Assessments give the house as it stood at each sale.

        - Prediction point: a house sells, and we predict its price from the assessor's record on the day of the sale and its location, with a model trained on all earlier sales (an automated valuation model).
        - The file's house features are the assessor's record as of 18-19 July 2015, after every kept sale (decision table). For 2,151 of the 20,967 kept rows the record changed between the sale and then, mostly upward, and untuned LightGBM scores better on these rows with the file's values (RMSE 0.156 against 0.208 with the record at the sale). These values are recorded after the outcome, so we rebuild each row as of its sale day.
        - The rebuild (`_as_of_sale`): each of `grade`, `condition`, `sqft_living`, `sqft_basement`, `bedrooms`, `floors`, `yr_built`, `yr_renovated` and `sqft_lot` whose attribute changed after the sale day and before 18 July 2015 takes the old value of its first such change. `bathrooms` (full, three-quarter and half baths) is rebuilt from the three counts where their history gives the file's value, and kept for the 5 rows where it does not. `sqft_above` is `sqft_living` minus `sqft_basement`, as in every row of the file. `_prepare_raw_files` cuts the two extracts down to the file's parcels.
        - We leave `view`, `waterfront` (the file's 0-4 view index is not a county attribute), `sqft_living15`, `sqft_lot15` (the neighbours' areas in July 2015) and the 10 values whose old value is blank as in the file.
        - Anomaly: the record at the sale describes what was sold, so `yr_built` is rebuilt for 24 rows, mostly teardowns, and 6 houses under construction carry a placeholder living area of 8 to 200 sq ft. We keep the 1,225 rows the county flags with sale warning 26, "IMP. CHARACTERISTICS CHANGED SINCE SALE", as noise.
        - We drop the 646 sales of May 2015 (3.0%): the sales list was extracted in mid-May 2015, so the month is incomplete, and its quickly recorded sales are cheaper (decision table).
        - We keep the repeated sales of one house (159 houses sold twice and one three times): under the temporal split the earlier sale is in the past, and LightGBM predicts resales worse than the other test rows (RMSE 0.36 against 0.17).
        - We drop `id`, the parcel number. `_load_raw` reads it and `zipcode` as text to keep the leading zeros.
        - `yr_renovated` = 0 (GeoDa: "'0' if never renovated") and 0 bedrooms or 0 bathrooms at the sale are unrecorded values; we set them to missing.
        - Target: `log_price`, the log of the sale price ($75,000 to $7.7M).
        - `zipcode` is categorical, and `date` (the sale date) is a datetime and the time column.
        - No duplicate rows. 9 pairs of different parcels share every feature (townhouses built together), one of them sold on the same day at two prices (the conflicting duplicate the checks report); we keep them.
    """

    # Task
    target = "log_price"
    problem_type = "regression"

    # Splits
    temporal = Temporal(on="date", splits=TemporalSplits(window=3, unit="weeks", n_windows=9, min_train_fraction=0.5))
    splits_comment = """
        A price model refit every three weeks predicts the sales of the next three weeks: 9 test windows of 21 days, from 10-30 April 2015 back to 24 October-13 November 2014, newest first, each trained on all earlier sales. Nine windows are the 3 x 3 splits an IID task of this size gets; they hold 659 to 1,565 sales each, and the oldest trains on 54% of the rows. Calendar months (a monthly refit) would give 6 windows of 978 to 2,231 sales.
    """

    prepared_raw_files = (CHANGES_FILE, BATHS_FILE)

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

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        # The parcel number and the ZIP code are codes: read them as text to keep the leading zeros.
        sales = pd.read_csv(raw_dir / SALES_FILE, dtype={"id": str, "zipcode": str})
        changes = pd.read_csv(
            raw_dir / CHANGES_FILE,
            dtype={"id": str, "record": str, "attribute": str, "value": str},
            keep_default_na=False,
        )
        bath_counts = pd.read_csv(raw_dir / BATHS_FILE, dtype={"id": str})
        return {"sales": sales, "changes": changes, "bath_counts": bath_counts}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # The sales of May 2015 are incomplete (the sales list was extracted mid-month); dates read YYYYMMDDT000000.
        df = raw["sales"][raw["sales"]["date"] < FIRST_INCOMPLETE_MONTH]
        # The house features as the assessor's record stood on the day of each sale (see `_as_of_sale`).
        df, _ = _as_of_sale(df, _parse_changes(raw["changes"]), raw["bath_counts"])
        # Proxy missing values: 0 bedrooms or bathrooms are unrecorded; a renovation year of 0 means none recorded.
        for col in ("bedrooms", "bathrooms", "yr_renovated"):
            df[col] = df[col].replace({0: np.nan})
        # Target: the log of the sale price, renamed in place.
        df = df.rename(columns={"price": "log_price"})
        df["log_price"] = np.log(df["log_price"])
        return drop_columns(df, ["id"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["zipcode"],
            datetime={"date": "%Y%m%dT%H%M%S"},
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        sales = raw["sales"]
        changes = _parse_changes(raw["changes"])
        kept = sales[sales["date"] < FIRST_INCOMPLETE_MONTH].reset_index(drop=True)
        rebuilt, stats = _as_of_sale(kept, changes, raw["bath_counts"])

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
        columns = [*CHANGED_COLUMNS.values(), "bathrooms", "sqft_above"]
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
