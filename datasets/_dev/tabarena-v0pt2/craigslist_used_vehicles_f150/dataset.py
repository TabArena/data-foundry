"""Curated dataset definition for `craigslist_used_vehicles_f150` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from data_foundry.definition import (
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
# The columns read: the advert's fields, the url (for the listing id, the Craigslist site and the advert's title, which
# it carries as a slug) and the VIN (to find one truck listed several times). Never read: the posting text and its
# title column (phone numbers, names), the image links, the
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

# The advert's title, from the url's slug (/d/<slug>/<id>.html): a model-year token marks where it starts (a city
# prefix comes before it), and every number of 1,000 or more that is no model year and every "<n>k" goes (prices,
# down payments, mileages), so no title states a price
SLUG = r"/d/([^/]+)/\d+\.html"
MODEL_YEAR_TOKEN = re.compile(r"19[7-9]\d|20[0-2]\d")
THOUSANDS_TOKEN = re.compile(r"\d+k")
# The test windows: a truck seen in a window scrape keeps only its copies from its last window scrape on
WINDOW_CUTOFFS = ("2020-03-22", "2020-06-17", "2020-09-16", "2020-12-03", "2021-05-06")

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
            "one row per truck within a scrape; a truck seen again in a later test scrape keeps only its latest copy."
        ),
        predicted="The asking price in US dollars, from 1,000 to 150,000.",
        known=(
            "What the advert states: its title (numbers that could be a price removed), model year, mileage, the model "
            "string with trim and cab, condition, cylinders, "
            "fuel, title status, transmission, drive, size, body type, colour, whether an owner or a dealer sells it, "
            "the Craigslist site and its coordinates, and the scrape's date."
        ),
        split=(
            "Each test set is one later scrape, with all earlier scrapes for training: the next market the price guide "
            "meets after its refit."
        ),
        changes=(
            "We keep the Ford F-150 of a scraped table of all makes, one row per truck within a scrape, drop a "
            "relisted truck's earlier copies (no test truck in training), placeholder prices and the 2026 scrape, set "
            "values impossible for an F-150 missing, drop the posting text and take the seller type and the title, "
            "without its numbers, from the url."
        ),
        fit="approximate",
        fit_reason=(
            "The fields are what an advert shows and the test scrapes are later markets, but the target is the asking "
            "price (a gap for a buyer who wants the sale price) and the poster types the fields in. A relisted truck's "
            "earlier copies are removed, so its dealer's knowledge of the earlier price is not part of the task."
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
        - The F-150: manufacturer `ford` and a model string starting with "f150" or "f-150" (versions 1-3 hold the model in `make`). The model string ships as text: 491 to 950 spellings a scrape (3,309 in all) that hold the trim, cab, bed and drive; a price typed into it (13 rows, such as "$21995") is removed.
        - One row per truck within a scrape period: one row per VIN, then one row per model year, mileage, price and Craigslist site, and, where the mileage is no multiple of 1,000, one row per model year, mileage and price on any site: dealers post one truck on several sites, and among such groups that carry VINs, 99.8% of 11,280 carry one VIN. The cross-site step drops 3,481 rows (3.2%; 1.5% to 3.5% of each scrape, 9.5% of May 2021); the price's 10th, 50th and 90th percentiles move from 3,500, 14,995 and 33,995 to 3,500, 14,950 and 33,919 dollars. Round mileages also match by VIN (98.5% of 741 groups) but are left, 2,713 rows more. These copies never leave their scrape, so they put no test truck in training; the step keeps a test window from scoring one truck several times (up to 56).
        - No test truck in training: a truck relisted in a later scrape is linked by its VIN or by its title, model year and mileage (which agree with the VIN in 93% to 99.7% of the pairs where both carry one, and find about a third more relistings; only 44% of the rows carry a VIN), and when it appears in a test scrape, its copies in earlier scrapes are dropped: 7,843 rows (7.5%), 4,415 of them from the training-only scrapes (1.0% of Oct 2018 to 16.4% of Jan 2020) and 2,258, 192, 591 and 387 from the Mar 2020 to Dec 2020 windows (their trucks are tested again later); May 2021 stays whole. Before the drop 12.6%, 18.0%, 2.2%, 5.4% and 3.2% of the Mar 2020 to May 2021 test rows had their VIN in training; after it none has an earlier copy by either link. Left: a truck whose title or mileage changed and that carries no VIN (1.5% to 2.3% of a window's test rows share model year and odd mileage with a training row, a link that agrees with the VIN in only 61% to 96%). The price's 10th, 50th and 90th percentiles move from 3,500, 14,950 and 33,919 to 3,495, 14,499 and 33,950 dollars; untuned LightGBM's RMSLE rises by 0.3% to 6.3% per window (0.314 to 0.321 on average), the part the relistings made easy.
        - Title: `advert_title` is the advert's title from the url's slug (`/d/<slug>/<id>.html`, 99.9% of rows; never the posting text): from its first model-year token on (a city prefix comes before it), hyphens as spaces, every "<n>k" and every token holding a number of 1,000 or more that is no model year (1975 to the scrape's year + 1) removed, so no title states a price, a down payment or a mileage; `_clean` asserts it. It names the trim and cab that 59% of the model strings, a bare "f-150", leave out. On the shipped rows: 0 titles with 7 or more digits in a row, 42 whose model year equals the price (a 2000 truck at 2,000 dollars); 38,868 spellings; 133 missing. Untuned LightGBM with the title's words lowers RMSLE by 5.0% to 6.6% per window (0.321 to 0.302 on average; 0.314 before both changes).
        - Price: listings under 1,000 or over 150,000 dollars are dropped (0 and 1 mean "call for price"; 4-13% of a scrape's F-150 rows are under 1,000), and so are placeholder prices (one digit five times or more, such as 99999, or a sequence, 1234, 12345 or 123456; 52 rows) and down payments posted as the price (under 5,000 for a truck of 2015 or newer; 124 rows). Charm prices such as 9,999 (435 rows) or 8,888 are real asking prices and stay.
        - Impossible values are set missing, the row kept, one rule each: a mileage over 500,000; a model year before 1975 (the F-150's first) or after the scrape's year; front-wheel drive (no F-150 has it; 2,456 rows); cylinders other than 6 or 8 (218); size compact or sub-compact (191); fuel electric before model year 2022 (11); coordinates outside the US (53). A mileage under 100 on a truck at least two model years old is a placeholder (0, 1) and set missing too (483 rows). `cylinders` becomes a number ("other" missing); `condition` and `size` are ordered scales.
        - Seller: `seller` is owner or dealer, the Craigslist section the poster picked (`/cto/` or `/ctd/` in the url): 36,982 owners and 60,309 dealers. Dealers list comparable trucks (2013-2015, 60,000 to 120,000 miles) 95 to 2,195 dollars higher in every scrape (by the median).
        - Dropped: the posting text, its title column and image links (never read: 70-80% of the F-150 texts hold a phone number), the url, listing id and VIN (identifiers, used for the steps above; the url's slug ships as the title), `manufacturer` (constant), `county` (empty), `state` (absent in versions 1-3; the site and the coordinates carry it) and the site's name (spelled differently in versions 1-3): the site's subdomain in the url replaces it as `region`.
        - The target ships as the log of the price; the metric is RMSLE on the price in dollars.
        - Anomaly: the fields are typed in by the poster: `condition`, `cylinders`, `drive`, `size`, `type` and `paint_color` are 26-62% missing. The mileage is 32% missing in 2018 and 17-27% up to Dec 2020, then 1.7% in May 2021: Craigslist made it a required field around 30 November 2020 (version 8's weekly postings go from 14-16% missing to 4.5% that week), a change a model in use meets too.
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
        "splits_dimensions_off_protocol": (
            "Five windows against nine: every scrape whose training side keeps half the rows is a window; the 50% "
            "floor stops more (Jan 2020 trains on 41.1%)."
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
        Five test windows, each one scrape, each trained on every earlier scrape: May 2021 (versions 9 and 10, 12,008 trucks, 87.7% of the rows in training), Dec 2020 (8,244; 79.2%), Sep 2020 (5,814; 73.2%), Jun 2020 (9,823; 63.1%) and Mar 2020 (10,829; 52.0%), with no test truck in training (a relisted truck's earlier copies are dropped). The horizon is one scrape (uploads 5 to 21 weeks apart; the scraper ran "every few months"): a pricing model refit on the listings so far meets the next market. No gap for the label: the price arrives with the advert. The scrape schedule leaves postings unseen before each window, by listing id about 7, 3, 16, 7.5 and 15 weeks before the Mar 2020 to May 2021 windows.
        Every scrape whose training side keeps half the rows is a window; the older scrapes (Oct 2018, Oct 2019, Dec 2019, Jan 2020) train on 0% to 41.1% and stay training data. The Mar 2020 window clears the 50% floor only with version 1 in training (42.4% without it); version 1's order is measured from listing ids, only its date is inferred. Five windows against the nine an IID split of 97,291 trucks would get (SPLIT-15): the 50% floor stops more. The windows are named by upload; their postings are, by listing id, about Jan to mid-Feb 2020 (Mar 2020, before COVID-19), Mar to Apr 2020 (Jun 2020, the pandemic's start), Aug to early Sep 2020, 28 Oct to 3 Dec 2020 and mid-Mar to 5 May 2021, when used-truck asking prices rose (the median of comparable trucks, 2013-2015 with 60,000 to 120,000 miles, from about 21,000 dollars in Jun 2020 to about 26,000).
        The 2026 scrape (version 11) is not a window: five years after the others, with trucks of model years the training data never shows.
        Not declared: a seller who also knows the rest of the scrape being priced. Training on the earlier scrapes plus four fifths of the test scrape (5 random folds) scores lower than this split, by 3.2%, 2.5%, 12.3%, 2.7% and 6.6% in the Mar 2020 to May 2021 windows (untuned LightGBM, RMSLE 0.296 against 0.314 on average, measured 2026-11-25 before the relisting drop and the title), mostly the market's move within one scrape; it puts training rows beside test rows of the same period and no longer tests a model meeting a later market.
    """
    temporal = Temporal(
        on="scrape_date",
        splits=TemporalSplits(window=1, unit="unique", cutoffs=WINDOW_CUTOFFS),
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
        df["advert_title"] = [
            _title(slug, year)
            for slug, year in zip(df["url"].str.extract(SLUG, expand=False), df["scrape_date"].dt.year, strict=True)
        ]
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
        _assert_no_price_in_title(df)
        # No test truck in training: a truck (one VIN, or one title, model year and mileage) seen in a window scrape
        # keeps only its rows from its last window scrape; its earlier copies go
        vin = df["vin"].str.upper().str.strip()
        title_truck = df["advert_title"] + "|" + df["year"].astype(str) + "|" + df["odometer"].astype(str)
        title_truck = title_truck.where(df[["advert_title", "year", "odometer"]].notna().all(axis=1))
        truck = _trucks(df.index, [vin, title_truck])
        window = df["scrape_date"].where(df["scrape_date"] >= pd.Timestamp(min(WINDOW_CUTOFFS)))
        df = df[~(df["scrape_date"] < window.groupby(truck).transform("max"))]
        df["price"] = np.log(df["price"])
        return drop_columns(
            df, ["version", "url", "id", "listing", "vin", "make", "manufacturer", "city", "county", "state"]
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["seller", "fuel", "title_status", "transmission", "drive", "type", "paint_color", "region"],
            string=["model", "advert_title"],
            ordinal={"condition": CONDITION, "size": SIZE},
        )


def _title(slug: object, scrape_year: int) -> str | float:
    """The advert's title from the url's slug: from the first model year on, without numbers that could be a price."""
    if not isinstance(slug, str):
        return np.nan
    tokens = slug.lower().split("-")
    start = next((i for i, t in enumerate(tokens) if MODEL_YEAR_TOKEN.fullmatch(t)), 0)
    kept = [t for t in tokens[start:] if not _price_like(t, scrape_year)]
    return " ".join(kept) or np.nan


def _price_like(token: str, scrape_year: int) -> bool:
    """A "<n>k", or a token holding a number of 1,000 or more, unless the token is a model year."""
    if THOUSANDS_TOKEN.fullmatch(token):
        return True
    if token.isdigit() and FIRST_F150_YEAR <= int(token) <= scrape_year + 1:
        return False
    return any(int(run) >= 1000 for run in re.findall(r"\d+", token))


def _assert_no_price_in_title(df: pd.DataFrame) -> None:
    """No shipped title holds a number of 1,000 or more that is no model year, or a "<n>k"."""
    tokens = df["advert_title"].str.split(" ").explode().dropna()
    scrape_year = df["scrape_date"].dt.year.reindex(tokens.index)
    number = pd.to_numeric(tokens.where(tokens.str.fullmatch(r"\d+")), errors="coerce")
    model_year = number.between(FIRST_F150_YEAR, scrape_year + 1)
    big = tokens.str.findall(r"\d+").map(lambda runs: any(int(r) >= 1000 for r in runs))
    assert not (big & ~model_year).any(), "a title holds a number of 1,000 or more that is no model year"
    assert not tokens.str.fullmatch(r"\d+k").any(), "a title holds a '<n>k'"


def _trucks(index: pd.Index, keys: list[pd.Series]) -> pd.Series:
    """One id per truck: the rows connected by any of the keys (missing keys link nothing)."""
    truck = pd.Series(np.arange(len(index)), index=index)
    while True:
        before = truck.copy()
        for key in keys:
            linked = key.notna()
            truck[linked] = truck[linked].groupby(key[linked]).transform("min")
        if truck.equals(before):
            return truck
