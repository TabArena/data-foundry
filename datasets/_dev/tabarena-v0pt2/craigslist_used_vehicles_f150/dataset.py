"""Curated dataset definition for `craigslist_used_vehicles_f150` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

# One Kaggle version per scrape, dated by its upload, not by when its listings were posted: each scrape holds about five
# weeks of postings, which end at the upload in versions 8 and 10 (measured from `posting_date`) and, by listing id,
# 5 to 10 weeks before it in versions 2 to 6. Version 1 is an older scrape re-uploaded in 2019: Craigslist issues
# listing ids in posting order, and all of version 1's ids lie about 277 million ids (over a year of postings) before
# version 2's, so its order is measured and its date inferred: the first upload of the dataset, 2018-10-10. Versions 9 and 10, two weeks apart and sharing 27% of their listings, are one
# scrape period, dated by version 10. Version 11 (2026) is read but not used.
SCRAPE_DATES = {
    1: "2018-10-10",
    2: "2019-10-14",
    3: "2019-12-02",
    4: "2020-01-07",
    5: "2020-03-22",
    6: "2020-06-17",
    7: "2020-09-16",
    8: "2020-12-03",
    9: "2021-05-06",
    10: "2021-05-06",
}
VERSIONS = (*SCRAPE_DATES, 11)
# The columns read: the advert's fields, the url (for the listing id and the Craigslist site) and the VIN (to find one
# truck listed several times). Never read: the posting text and title (phone numbers, names), the image links, the
# posting date (two of the nine periods) and the fields only the 2026 scrape has.
READ = {
    "id", "url", "city", "region", "state", "county", "price", "year", "manufacturer", "make", "model", "condition",
    "cylinders", "fuel", "odometer", "title_status", "transmission", "vin", "drive", "size", "type", "paint_color",
    "lat", "long",
}  # fmt: skip
FORD_FILE = "ford_listings.parquet"

MIN_PRICE, MAX_PRICE = 1_000, 150_000  # below: 0, 1 and other placeholders; above: typing errors (up to 1.1e16)
MAX_ODOMETER = 500_000  # miles; higher readings are typing errors and become missing
FIRST_F150_YEAR = 1975  # the model year the F-150 was introduced
# Prices that are no asking price: one digit repeated five times or more (11111, 99999), a sequence (1234, 12345,
# 123456), or a down payment posted as the price (under 5,000 for a truck of 2015 or newer). Charm prices such as
# 9,999 or 8,888 are real asking prices and stay.
PLACEHOLDER_PRICE = r"(\d)\1{4,}|1234|12345|123456"
DOWN_PAYMENT_PRICE, DOWN_PAYMENT_YEAR = 5_000, 2015
# Values impossible for an F-150 become missing (the row stays): it is never front-wheel drive, has 6 or 8 cylinders,
# is no compact car, had no electric version before model year 2022, and a US Craigslist site lies in the US.
F150_CYLINDERS = (6, 8)
FIRST_ELECTRIC_YEAR = 2022
US_LAT, US_LONG = (17.0, 72.0), (-180.0, -64.0)  # Puerto Rico and Hawaii to Alaska
# A mileage under 100 on a truck at least two model years old is a placeholder (0, 1), not a reading
PLACEHOLDER_ODOMETER, PLACEHOLDER_ODOMETER_AGE = 100, 2

CONDITION = ["salvage", "fair", "good", "excellent", "like new", "new"]
SIZE = ["mid-size", "full-size"]  # sub-compact and compact are impossible for an F-150


class CraigslistUsedVehiclesF150(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="At what price is a used Ford F-150 listed on Craigslist?",
        use_case=(
            "The source names none; ours: a price guide refit once per scrape on every earlier scrape prices the next "
            "scrape's F-150 listings, for a seller or dealer setting an asking price or a buyer or marketplace judging one."
        ),
        row=(
            "One F-150 listing in one of nine nationwide scrapes of Craigslist's US car adverts (2018 to May 2021), "
            "one row per truck and scrape."
        ),
        predicted="The asking price in US dollars, from 1,000 to 150,000.",
        known=(
            "What the advert states: model year, mileage, the model string with trim and cab, condition, cylinders, "
            "fuel, title status, transmission, drive, size, body type, colour, whether an owner or a dealer sells it, "
            "the Craigslist site and its coordinates, and the scrape's date."
        ),
        split=(
            "Each test set is one later scrape, with all earlier scrapes for training: the next market the price guide "
            "meets after its refit."
        ),
        changes=(
            "We keep the Ford F-150 of a scraped table of all makes, one row per truck within a scrape (also across "
            "sites), drop placeholder prices (0, 1, 12345, 99999, down payments) and the 2026 scrape, set values "
            "impossible for an F-150 missing, drop the posting text and keep the seller type from the url."
        ),
        fit="approximate",
        fit_reason=(
            "The fields are what an advert shows and the test scrapes are later markets, but the target is the asking "
            "price (a gap for a buyer who wants the sale price), the poster types the fields in, and the title is not "
            "shipped. Kept on purpose, not a gap: a relisted truck trains with its earlier price, as its dealer knows."
        ),
    )

    # Dataset
    unique_name = "craigslist_used_vehicles_f150"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data",
            license="CC0: Public Domain",
            year="2018",
            bibtex=r"""
                @misc{reese2018craigslist,
                  author       = {Austin Reese},
                  title        = {Used Cars Dataset (Craigslist Cars+Trucks Data)},
                  year         = {2018},
                  howpublished = {\url{https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data}},
                  note         = {Kaggle dataset, versions 1 to 11},
                }
            """,
            files=("v*/craigslist-carstrucks-data.zip",),
        ),
    )
    data_tags = ("Spatial",)
    download_description = """
        One folder per Kaggle version (each version is one scrape; the zips stay zipped):

        for N in 1 2 3 4 5 6 7 8 9 10 11; do kaggle datasets download austinreese/craigslist-carstrucks-data/$N -p local-data-warehouse/craigslist_used_vehicles_f150/v$N; done

        The definition reads the zips once and writes their Ford rows, without the posting text, to ford_listings.parquet.
    """
    curation_comments = """
        We start with the eleven Kaggle versions of austinreese/craigslist-carstrucks-data (one CSV each, every US car listing on Craigslist at the scrape) and keep the Ford F-150.

        - Prediction point: when the advert is written, so every field the advert shows is known; the price arrives with it, so the split needs no gap.
        - Versions and dates: each version is one scrape, dated by its upload, not by its postings: a scrape holds about five weeks of postings, which end at the upload in versions 8 and 10 (their `posting_date`) and, by listing id, 5 to 10 weeks before it in versions 2 to 6. Version 1 (uploaded 2019-10-08) is an older scrape: Craigslist issues listing ids in posting order (they follow the posting date of versions 8, 10 and 11 with a correlation of 0.99998), and all of version 1's ids lie about 277 million ids, over a year of postings, before version 2's, so it is dated 2018-10-10, the dataset's first upload: its order is measured, its date inferred (`Time: Inferred` for that period; it is training data only, and the split uses only the order). Versions 9 and 10 (2021-04-20 and 2021-05-06) share 26-27% of their listing ids and form one period (dated 2021-05-06; a listing in both kept once, from version 10); no other pair of versions shares more than 27 ids. Version 11 (2026-11-05) is left out: five years after the others, with columns of its own.
        - US sites only: version 1 also holds Canadian and Mexican Craigslist sites (437 F-150 rows on craigslist.ca, prices in Canadian dollars, and 46 on craigslist.com.mx), which are dropped.
        - The F-150: manufacturer `ford` and a model string starting with "f150" or "f-150" (versions 1-3 hold the model in `make`). The model string ships as text: 600 to 1,000 spellings a scrape (3,343 in all) that hold the trim, cab, bed and drive; a price typed into it (13 rows, such as "$21995") is removed.
        - One row per truck within a scrape period: one row per VIN, then one row per model year, mileage, price and Craigslist site, and, where the mileage is no multiple of 1,000, one row per model year, mileage and price on any site: dealers post one truck on several sites, and among such groups that carry VINs, 99.8% of 11,280 carry one VIN. The cross-site step drops 3,481 rows (3.2%; 1.5% to 3.5% of each scrape, 9.5% of May 2021); the price's 10th, 50th and 90th percentiles move from 3,500, 14,995 and 33,995 to 3,500, 14,950 and 33,919 dollars. Round mileages also match by VIN (98.5% of 741 groups) but are left, 2,713 rows more.
        - Price: listings under 1,000 or over 150,000 dollars are dropped (0 and 1 mean "call for price"; 4-13% of a scrape's F-150 rows are under 1,000), and so are placeholder prices (one digit five times or more, such as 99999, or a sequence, 1234, 12345 or 123456; 52 rows) and down payments posted as the price (under 5,000 for a truck of 2015 or newer; 124 rows). Charm prices such as 9,999 (435 rows) or 8,888 are real asking prices and stay.
        - Impossible values are set missing, the row kept, one rule each: a mileage over 500,000; a model year before 1975 (the F-150's first) or after the scrape's year; front-wheel drive (no F-150 has it; 2,456 rows); cylinders other than 6 or 8 (218); size compact or sub-compact (191); fuel electric before model year 2022 (11); coordinates outside the US (53). A mileage under 100 on a truck at least two model years old is a placeholder (0, 1) and set missing too (483 rows). `cylinders` becomes a number ("other" missing); `condition` and `size` are ordered scales.
        - Seller: `seller` is owner or dealer, the Craigslist section the poster picked (`/cto/` or `/ctd/` in the url): 37,839 owners and 67,295 dealers. Dealers list comparable trucks 500 to 2,200 dollars higher in every scrape.
        - Dropped: the posting text, title and image links (never read: 70-80% of the F-150 texts hold a phone number), the url, listing id and VIN (identifiers, used for the steps above; the advert's title, which the url carries as a slug, is not shipped), `manufacturer` (constant), `county` (empty), `state` (absent in versions 1-3; the site and the coordinates carry it) and the site's name (spelled differently in versions 1-3): the site's subdomain in the url replaces it as `region`.
        - The target ships as the log of the price; the metric is RMSLE on the price in dollars.
        - Potential leak, kept on purpose: a truck relisted in a later scrape (its VIN seen before; 8,634 rows, 8.2%) is in training with its earlier price when it is tested: 12.6%, 18.0%, 2.2%, 5.4% and 3.2% of the Mar 2020 to May 2021 windows, at the same price in 4.0%, 7.6%, 0.8%, 1.9% and 1.1%. No listing id appears in two periods, so each is a new advert (at a new price in 61.6% of cases), a repost the use case meets: a dealer knows the earlier price of a truck it posts again. Dropping the linked ones moves the RMSE by -1.6% to +1.9%; only 46.5% of the rows carry a VIN, so the rest cannot be linked.
        - Anomaly: the fields are typed in by the poster: `condition`, `cylinders`, `drive`, `size`, `type` and `paint_color` are 23-66% missing. The mileage is 32% missing in 2018 and 17-23% up to Dec 2020, then 1.7% in May 2021: Craigslist made it a required field around 30 November 2020 (version 8's weekly postings go from 14-16% missing to 4.5% that week), a change a model in use meets too.
    """
    split_leaf = "L-ORDER.windows"
    accepted_check_warnings = {
        "dataset_missing_value_label": (
            "`title_status` 'missing' is Craigslist's own option, a truck without a title document: a real state, not a "
            "missing value."
        ),
        "dataset_conflicting_duplicate_rows": (
            "93.6% of 1,708 same-year, same-mileage, different-price groups share a VIN: one truck at two prices "
            "within one scrape. A scrape is never cut by the split, so they stay together."
        ),
        "task_time_on_few_unique": "Nine scrape periods, one date each, by design: the scrape is the time step.",
        "splits_below_target": (
            "Five windows against nine: every scrape whose training side keeps half the rows is a window; the 50% "
            "floor stops more (Jan 2020 trains on 40.3%)."
        ),
    }

    # Task
    target = "price"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason=(
            "A scraped Kaggle dataset without a task, leaderboard or paper: the data card, the scraper's GitHub README "
            "and a web search name no metric. For an asking price the error that matters is relative to the price, "
            "so RMSLE on the price in dollars."
        ),
        target_transform="log",
    )

    # Splits
    splits_comment = """
        Five test windows, each one scrape, each trained on every earlier scrape: May 2021 (versions 9 and 10, 12,008 trucks, 88.6% of the rows in training), Dec 2020 (8,631; 80.4%), Sep 2020 (6,405; 74.3%), Jun 2020 (10,015; 64.8%) and Mar 2020 (13,087; 52.3%). The horizon is one scrape (uploads 5 to 21 weeks apart; the scraper ran "every few months"): a pricing model refit on the listings so far meets the next market. No gap for the label: the price arrives with the advert. The scrape schedule leaves postings unseen before each window, by listing id about 7, 3, 16, 7.5 and 15 weeks before the Mar 2020 to May 2021 windows.
        Every scrape whose training side keeps half the rows is a window; the older scrapes (Oct 2018, Oct 2019, Dec 2019, Jan 2020) train on 0% to 40.3% and stay training data. The Mar 2020 window clears the 50% floor only with version 1 in training (43.5% without it); version 1's order is measured from listing ids, only its date is inferred. Five windows against the nine an IID split of 105,134 trucks would get (SPLIT-15): the 50% floor stops more. The windows are named by upload; their postings are, by listing id, about Jan to mid-Feb 2020 (Mar 2020, before COVID-19), Mar to Apr 2020 (Jun 2020, the pandemic's start), Aug to early Sep 2020, 28 Oct to 3 Dec 2020 and mid-Mar to 5 May 2021, when used-truck asking prices rose (the median of comparable trucks, 2013-2015 with 60,000 to 120,000 miles, from about 21,000 dollars in Jun 2020 to about 26,000).
        The 2026 scrape (version 11) is not a window: five years after the others, with trucks of model years the training data never shows.
        Not declared: a seller who also knows the rest of the scrape being priced. Training on the earlier scrapes plus four fifths of the test scrape (5 random folds) scores lower than this split, by 3.2%, 2.5%, 12.3%, 2.7% and 6.6% in the Mar 2020 to May 2021 windows (untuned LightGBM, RMSLE 0.296 against 0.314 on average, measured 2026-11-25), mostly the market's move within one scrape; it puts training rows beside test rows of the same period and no longer tests a model meeting a later market.
    """
    temporal = Temporal(
        on="scrape_date",
        splits=TemporalSplits(
            window=1, unit="unique", cutoffs=("2020-03-22", "2020-06-17", "2020-09-16", "2020-12-03", "2021-05-06")
        ),
        horizon=1,
        horizon_unit="steps",
    )

    prepared_raw_files = (FORD_FILE,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        frames = []
        for n in VERSIONS:
            with zipfile.ZipFile(raw_dir / f"v{n}" / "craigslist-carstrucks-data.zip") as archive:
                name = next(m for m in archive.namelist() if m.endswith(".csv"))
                with archive.open(name) as fh:
                    header = pd.read_csv(fh, nrows=0).columns
                with archive.open(name) as fh:
                    part = pd.read_csv(fh, usecols=[c for c in header if c.lower() in READ], dtype=str)
            part.columns = [c.lower() for c in part.columns]
            part = part[part["manufacturer"].fillna("").str.lower() == "ford"]
            part.insert(0, "version", n)
            frames.append(part)
        pd.concat(frames, ignore_index=True).to_parquet(raw_dir / FORD_FILE, index=False)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / FORD_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # Versions 1-3 hold the model in `make`; the Craigslist site is the url's subdomain in every version
        df["model"] = df["model"].where(df["model"].notna(), df["make"]).str.lower().str.strip()
        df["region"] = df["url"].str.extract(r"^https?://([a-z0-9]+)\.craigslist\.org", expand=False)
        df["listing"] = df["url"].str.extract(r"/(\d+)\.html", expand=False)
        # Owner or dealer: the Craigslist section the poster picked, /cto/ (by owner) or /ctd/ (by dealer)
        df["seller"] = df["url"].str.extract(r"/ct([od])/", expand=False).map({"o": "owner", "d": "dealer"})
        # US sites only: version 1 also holds Canadian sites (craigslist.ca, prices in Canadian dollars)
        df = df[df["region"].notna()]
        assert df["listing"].notna().all(), "every url names a listing"
        # The Ford F-150 of the 2018-2021 scrapes
        df = df[df["model"].fillna("").str.match(r"f-?150(?!\d)") & df["version"].isin(list(SCRAPE_DATES))].copy()
        df["scrape_date"] = pd.to_datetime(df["version"].map(SCRAPE_DATES))
        # Versions 9 and 10 are one period: a listing in both is kept once, from version 10
        df = df.sort_values("version", kind="stable")
        df = df[~df.duplicated(["scrape_date", "listing"], keep="last")]
        # Numbers; impossible values missing
        for c in ["price", "year", "odometer", "lat", "long"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df.loc[df["odometer"] > MAX_ODOMETER, "odometer"] = np.nan
        df.loc[(df["year"] < FIRST_F150_YEAR) | (df["year"] > df["scrape_date"].dt.year + 1), "year"] = np.nan
        df["cylinders"] = pd.to_numeric(df["cylinders"].str.extract(r"^(\d+) cylinders$", expand=False))
        # Asking prices only: no placeholders, typing errors or down payments
        df = df[df["price"].between(MIN_PRICE, MAX_PRICE)]
        price = df["price"].astype("int64").astype(str)
        placeholder = price.str.fullmatch(PLACEHOLDER_PRICE) | (
            (df["price"] < DOWN_PAYMENT_PRICE) & (df["year"] >= DOWN_PAYMENT_YEAR)
        )
        df = df[~placeholder]
        # One row per truck within a scrape period: per VIN, then per year, mileage, price and site, and, for a mileage
        # that is no multiple of 1,000, per year, mileage and price on any site (dealers post one truck on several
        # sites; 99.8% of such groups that carry VINs carry one VIN)
        vin = df["vin"].str.upper().str.strip()
        df = df[vin.isna() | ~pd.DataFrame({"t": df["scrape_date"], "v": vin}).duplicated(keep="last")]
        truck = ["scrape_date", "year", "odometer", "price"]
        df = df.drop_duplicates([*truck, "region"], keep="last")
        odd_mileage = df["odometer"].notna() & (df["odometer"] % 1000 != 0)
        df = df[~(odd_mileage & df.duplicated(truck, keep="last"))].copy()
        # Values impossible for an F-150, and placeholder mileages, become missing
        df.loc[df["drive"] == "fwd", "drive"] = np.nan
        df.loc[~df["cylinders"].isin(F150_CYLINDERS), "cylinders"] = np.nan
        df.loc[df["size"].isin(["sub-compact", "compact"]), "size"] = np.nan
        df.loc[(df["fuel"] == "electric") & (df["year"] < FIRST_ELECTRIC_YEAR), "fuel"] = np.nan
        outside_us = ~(df["lat"].between(*US_LAT) & df["long"].between(*US_LONG))
        df.loc[outside_us, ["lat", "long"]] = np.nan
        old = df["year"] <= df["scrape_date"].dt.year - PLACEHOLDER_ODOMETER_AGE
        df.loc[old & (df["odometer"] < PLACEHOLDER_ODOMETER), "odometer"] = np.nan
        # A price typed into the model string (12 rows) is removed
        df["model"] = df["model"].str.replace(r"\$[\d,.]+", "", regex=True).str.strip()
        df["price"] = np.log(df["price"])
        return drop_columns(
            df, ["version", "url", "id", "listing", "vin", "make", "manufacturer", "city", "county", "state"]
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["seller", "fuel", "title_status", "transmission", "drive", "type", "paint_color", "region"],
            string=["model"],
            ordinal={"condition": CONDITION, "size": SIZE},
        )
