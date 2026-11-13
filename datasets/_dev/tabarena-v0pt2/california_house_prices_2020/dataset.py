"""Curated dataset definition for `california_house_prices_2020` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, Temporal, TemporalSplits

# Entries of one sale scraped twice: the same address, ZIP code and sold price, with the same year built (51 pairs, a
# median 61 Kaggle IDs apart) or, where one copy lacks the year, the same living area (6 pairs; issue 6 of the v0.2
# review). One of the 6 older copies would leave anyway with the listings that predate their last sale.
SAME_SALE_ROWS = 57


def _same_sale(a: pd.Series, b: pd.Series) -> bool:
    """Whether two entries of one address, ZIP code and sold price are one sale scraped twice.

    They are when the year built is the same (both may be missing), or missing in one copy with the same living area.
    """
    ya, yb = a["Year built"], b["Year built"]
    if (pd.isna(ya) and pd.isna(yb)) or ya == yb:
        return True
    if pd.isna(ya) or pd.isna(yb):
        la, lb = a["Total interior livable area"], b["Total interior livable area"]
        return bool(la == lb or (pd.isna(la) and pd.isna(lb)))
    return False


# One sale scraped under two spellings of its address ("SPACE 34" / "SPC 34"): the same description, sold price, ZIP
# code, living area and year built within 600 Kaggle IDs (the review counted 500 steps of the shipped order;
# the widest pair, "1754 Lebec Oaks Rd" and "1754 Lebec Rd", is 517 IDs apart; issue 4 of the v0.2 review).
RESPELLED_SALE_ROWS = 54
RESPELLED_MAX_ID_SPAN = 600

# One transaction booked on several homes: the same sold price on two or more addresses of one street and ZIP code,
# each sold for more than 1.5 times its list price (issue 1 of the v0.2 review).
BUILDING_PRICE_ROWS = 14
BUILDING_PRICE_MIN_RATIO = 1.5


def _street(address: object) -> str:
    """The street of an address, without house number and unit: "321 S Elm Dr #3" -> "s elm dr"."""
    a = str(address).lower()
    a = re.sub(r"\s*(?:#|unit|apt|ste|suite|spc|space|bldg)\s*\S*$", "", a)
    a = re.sub(r"^[\d\-&/ .]+(?:1/2)?\s*", "", a)
    return a.strip()


# Scores and ratings with no words per level: numbers, as the source ships them (CLEAN-14).
SCORES = ["Elementary School Score", "Middle School Score", "High School Score"]


class CaliforniaHousePrices2020(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What price will a California home sell for, given its listing?",
        use_case=(
            "For example, when a home is listed, a buyer, an agent or a valuation website estimates the price it will"
            " sell for, to set or judge an offer."
        ),
        row=(
            "One sale of a home in California around 2020, as scraped from Zillow; Arizona homes, second copies of "
            "one sale, one price booked on several homes and homes whose listing predates their last sale are dropped."
        ),
        predicted="The sale price in US dollars, on a log scale.",
        known=(
            "The listing (list price, listing date, description), the home's facts (type, year built, size, lot, "
            "rooms, heating, cooling, parking, appliances), its previous sale, tax assessment, address, region, and "
            "nearby schools with ratings and distances. The sale order (`time_index`) orders the split but is no model "
            "input."
        ),
        split=(
            "Three test sets, each a sixth of the sales in sale order (the newest half of the sales), with all "
            "earlier sales for training. The order comes from the Kaggle row ID, as the data has no sale dates."
        ),
        changes=(
            'We drop 5,413 listings whose description states the sold price, one written after the sale ("closed '
            'escrow"), 2,480 whose listing describes an earlier sale, 111 second copies of a sale scraped twice (57 '
            "under one address, 54 under another spelling), and 14 sales that carry one price booked on several "
            "homes, and order and split the sales by the Kaggle ID, which follows the sale order."
        ),
        fit="approximate",
        fit_reason=(
            "The time axis is the order of the Kaggle IDs, checked on Redfin for some homes rather than given, and "
            "each test set is a count of sales rather than a calendar period. The listing facts are known before the "
            "sale."
        ),
    )

    # Dataset
    unique_name = "california_house_prices_2020"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/california-house-prices/data?select=train.csv",
            license="Custom Kaggle Competition Rules",
            year="2021",
            bibtex=r"""
                @misc{d2lcourse2021california_house_prices,
                  author       = {d2lcourse},
                  title        = {California House Prices},
                  year         = {2021},
                  howpublished = {\url{https://kaggle.com/competitions/california-house-prices}},
                  note         = {Kaggle}
                }
            """,
        ),
    )
    data_tags = ("Spatial",)
    download_description = """
        We utilize the train.csv from the Kaggle competition. We use the following commands to download and organize the data:

        kaggle competitions download -c california-house-prices -f train.csv && unzip train.csv.zip train.csv && rm train.csv.zip
        mkdir -p local-data-warehouse/california_house_prices_2020 && mv train.csv local-data-warehouse/california_house_prices_2020
    """
    curation_comments = """
        We follow some common preprocessing steps from Kaggle and enhance features as much as possible.

        We found out that the data was web scraped from a real-estate website and that the houses are ordered by the time they were sold such that a house with a higher ID was sold later. We confirmed this by looking at the history of various houses on redfin.com that we found in the dataset and checking their order in the ID with the time they were sold. Houses with a higher ID were sold later.

        - We log scale the target variable (log1p); the metric is the competition's RMSLE on the price, computed after the inverse (`target_transform="log1p"`).
        - We do not have the exact dates but we know a higher ID means a later sale. We name the ID column accordingly to "time_index" and use it to order and split the rows. The data agree: sorted by ID, the latest listing date per ID decile rises from 2020-03-02 to 2020-12-30. We split on this sale order, not on "Listed On": a house is listed before it is sold, so a listing-date split could train on a house that sells after the test period starts.
        - `time_index` orders and splits the rows and is no model input (`Temporal(..., feature=False)`): it arrives with the target (2026-11-12, Andrej). A home is predicted at its listing, and the sale's place in the sale order is the listing plus the time on market, known only once the home sells; the listing date (`Listed On`) stays a feature.
        - The descriptions did contain the last sold price with a standard phrase such as "This home last sold for $X in January 2020. The Zestimate for this house is $Y The Rent Zestimate for this home is $Z/mo.". In these cases $X is identical to the target variable. Given such a drastic data leakage, we remove all rows (5413) that contain this phrase in the description to ensure they are not different in other ways too.
        - The website is Zillow, not Redfin as first assumed (2026-11-11): 5,314 descriptions carry Zillow's generated text for off-market homes ("The Zestimate for this house is $Y"), some "Note: This property is not currently for sale or for rent on Zillow.", and the column names are Zillow's fact labels ("Total interior livable area", "Appliances included", "Laundry features"); Redfin appears only in agents' own words (6 descriptions). The Kaggle host does not name the website. The sale order was checked on redfin.com, which shows the same sale histories.
        - The one description written after the sale (Andrej, 2026-11-10 and 2026-11-11; LEAK-10): we drop the sale whose description says "Property has closed escrow for $1,500,000". Twelve more descriptions give a dollar amount within 0.5% of the sold price that is not the list price, but they are asking prices a buyer reads at the listing (a price cut, "buy it now", a probate auction's minimum overbid) or loose bounds ("under $500K"), and stay: a price known before the sale is a feature, and dropping a row because its text is close to its own label selects rows by the label. "sold for" is no rule: its 39 other descriptions speak of neighbours, earlier sales or "sold for land value".
        - Note, sometime descriptions are missing and we intend that models/pipelines need to be able to handle this.
        - When investigating the "Lot" column we found many cases where the lot size (given in sq ft) is incorrect compared to the official lot size on the internet. The parser seems to have had an issue because the website often incorrectly showed the sq ft but gave the unit as acres. We found cases that were wrong by checking the acres size of the houses and anything with more than 2000 acres was investigated and subsequently corrected.
        - We parsed the bedrooms with a proxy following Kaggle and added an additional column containing only the semi-free text descriptions of the bedrooms.
        - We fix the parser errors for two cases for total interior livable area that were clear outliers based on the real data on redfin.
        - Garage and total space were in most cases the same values parsed from different fields. We keep Garage space and add an 'Extra Space' column that is the difference between total and garage space as an additional feature. This results in some cases with negative extra space that are most likely parser errors. We set them to nan. Note, we observed that that garage space number is in many cases a parsing error and does not reflect the real garage count.
        - The data has a lot of spatial features that are already semi-resolved to distances. This could be further enhanced using the address information. We leave it to the pipeline to handle this, if at all.
        - The dataset contains many text-like many categorical that are also high-cardinality, so perfect string data.
        - We drop all entries from the State of Arizona (AZ) as they are only a small fraction (n=431 after our preprocessing). The dataset is specified to be for California house prices.
        - We treat ZIP codes as strings. But we add a new categorical features that puts zip code in to approximate relevant buckets of regions.
        - We fixed one entry that had a negative value for garage space, likely due to a typo. This error still exists on the website.
        - We drop the 2,480 homes (6.0%) whose last sale is on or after their listing date: the listing describes an earlier sale, and 125 of them give the price we predict as the last sale price. They were 5-6% of each test window but about half its squared error (LightGBM RMSE 0.196 with them, 0.140 without). Listings older than 6 months before the sale stay (Lennart, 2026-10-14).
        - After all the above preprocessing, 63 homes appear more than once (same address, ZIP code and year built; 130 rows). 51 pairs give the same sold price a median 61 Kaggle IDs apart: one sale scraped twice, of which we keep the newest entry. The other 28 rows are sales at another price (a resale, or another unit at an address without a unit number) and stay, as an earlier sale is history under the temporal split (Lennart, 2026-10-21: "we want to keep real repeats, as houses can be sold several times"). A missing year built counts as a match where the living area agrees (Andrej, 2026-11-12): 6 more pairs share the address, ZIP code, sold price and living area while one copy lacks the year (four units of 555 Fulton St, San Francisco, 750 Van Ness Ave #706 and 242 Robles Way), and we keep the newest entry of each; the older Robles Way copy, a 2018 listing, would leave anyway as a listing that predates its last sale, so the final data loses 5 sales, each of which was scored twice (both copies in one test window).
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 3 scores with no words per level are
          numbers (`SCORES`): `Elementary School Score`, `Middle School Score`, `High School Score`.
        - One sale scraped under two spellings of its address (Andrej, 2026-11-11): 54 pairs share the description (over 50 characters), sold price, ZIP code, living area and year built while the address is spelled two ways ("270 Hames Rd SPACE 34" and "SPC 34", "1922-1924 Warren St" and "1922 Warren St", "1754 Lebec Oaks Rd" and "1754 Lebec Rd"), within 600 Kaggle IDs; we keep the newest entry, as for a sale scraped twice under one spelling. Four groups more than 1,000 IDs apart stay: separate units of one development at one price (900 S Dwight Ave).
        - One transaction booked on several homes (Andrej, 2026-11-11; USE-5, CLEAN-11): we drop the 14 sales that share one sold price with another address of the same street and ZIP code, each sold for more than 1.5 times its list price, such as eight condos of 321 and 327 S Elm Dr, Beverly Hills, each listed at $1.9-3.9M and each "sold" for $35.8M: a building's price, not a home's. Eight of them carried 36% of the newest window's squared error. The other sales far from their list price (271 under half or over twice it) stay, as nothing shows they are errors.
    """

    # Task
    target = "Sold Price"
    problem_type = "regression"
    metric = Metric.source(
        "rmsle",
        original="RMSLE (root mean squared logarithmic error)",
        reference="https://www.kaggle.com/competitions/california-house-prices (Evaluation; Kaggle API, per the record's 2026-10-21 assessment)",
        definition="RMSLE on the raw Sold Price, computed after the inverse of the shipped log1p(Sold Price)",
        target_transform="log1p",
    )

    # Splits
    splits_comment = """
        Three test windows in sale order, each a sixth of the sales (6,497 rows), cut from the newest half; each trains on all earlier sales (50%, 67% and 83% of the rows), so no window trains on less than half of the data (SPLIT-14). Each window is a separate repeat with one fold. We simulate deploying a model at one point in the sale order for the next stretch of sales. As the time_index gives the order but no dates, the windows are counts of sales, not calendar periods. The earlier layout (each window a quarter of the rows) trained the oldest window on 25% of the rows, below SPLIT-14's floor (2026-10-21).
        The windows are cut in sale order, the time the label arrives, while a home is predicted at its listing: a test
        home listed before its window began meets training sales that closed after its listing (80-96% of each
        window's test homes; a gap of a third or a whole window at equal training size changes the RMSLE by -0.001 to
        +0.005, in no consistent direction, 2026-11-11). A home enters the data only once sold, so a cut on the listing
        date would make the newest listings the fast sellers.
    """
    temporal = Temporal(
        on="time_index",
        splits=TemporalSplits(window=None, unit="rows", n_windows=3, min_train_fraction=0.5),
        horizon=6497,
        horizon_unit="steps",
        feature=False,  # the sale order arrives with the target: no model input (2026-11-12, Andrej)
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.rename(
            columns={
                "Id": "time_index",
            }
        )
        # Remove rows with target leakage in description
        leak_mask = ~df["Summary"].isna() & (df["Summary"].str.contains("last sold for"))
        df = df[~leak_mask]
        # ... and the one description written after the sale, "Property has closed escrow for $1,500,000" (Andrej,
        # 2026-11-10 and 2026-11-11; LEAK-10). Other dollar amounts near the sold price are asking prices or bounds a
        # buyer reads at the listing, and stay.
        closed = df["Summary"].fillna("").str.contains("closed escrow", case=False)
        assert closed.sum() == 1, "expected one description written after the sale"
        df = df[~closed]
        # Set wrongly parsed years to NaN
        df.loc[df["Year built"].isin([0, 19, 9999, 1471, 2281]), "Year built"] = np.nan
        # Fix wrong lot sizes
        #   - found by: wrong_lot_size_mask = (df["Lot"]/43560) > 2000
        for time_index, correct_size in [
            (1701, 6660),
            (5198, 5500),
            (11205, 5768),
            (16036, 4200),
            (17241, 7650),
            (19469, 60984),
            (23605, 7700),
            (23807, 35283.6),
            (30942, 4500),
            (31871, 6500),
            (34622, 6403),
            (39769, 2584),
            (43009, 7546),
            # still says acres
            (13280, 5804),
            (46033, 6216),
        ]:
            df.loc[df["time_index"] == time_index, "Lot"] = correct_size
        assert ((df["Lot"] / 43560) > 2000).sum() == 0, "There are still wrong lot sizes > 2000 acres"
        # Parse the year (a float with missing values) to a date here; `_feature_types` cannot express this
        c = "Year built"  # special case
        nan_mask = df[c].isna()
        df.loc[nan_mask, c] = df.loc[~df[c].isna(), c].iloc[0]
        df[c] = pd.to_datetime(df[c].astype(int).astype(str), errors="raise")
        df.loc[nan_mask, c] = pd.NaT
        # Extra FE for Bedrooms
        bedroom_description_mask = pd.to_numeric(df["Bedrooms"], errors="coerce").isna()
        df["Bedrooms_description"] = df["Bedrooms"]
        df.loc[(~bedroom_description_mask) | (df["Bedrooms"].isna()), "Bedrooms_description"] = np.nan

        # Compute a proxy for bedrooms from the description
        # https://www.kaggle.com/code/wuwawa/automl-using-h2o
        def bedroom_proxy(x):
            if not pd.isna(x) and not x.isdigit():
                temp = x.split(",")
                n = len(x.split(","))
                if "Walk-in Closet" in temp:
                    n -= 1
                if "Reverse Floor Plan" in temp:
                    n -= 1
                if n <= 0:
                    n = np.nan
                return n
            return x

        df["Bedrooms"] = df["Bedrooms"].astype(object)  # pandas 3 reads text as `str`, which takes no numbers
        df.loc[bedroom_description_mask, "Bedrooms"] = df.loc[bedroom_description_mask, "Bedrooms"].apply(bedroom_proxy)
        df["Bedrooms"] = pd.to_numeric(df["Bedrooms"], errors="coerce")
        # Fix wrong sqft parsing outliers
        for time_index, correct_size in [
            (43911, 702),
            (26533, 700),
        ]:
            df.loc[df["time_index"] == time_index, "Total interior livable area"] = correct_size
        # Add extra space and remove total space duplicates
        df.loc[df["time_index"] == 41450, "Garage spaces"] = 5  # fix data error
        df["Extra Space"] = df["Total spaces"] - df["Garage spaces"]
        df.loc[df["Extra Space"] < 0, "Extra Space"] = np.nan
        df = df.drop(columns=["Total spaces"])
        # Drop entries from AZ state
        df = df[df["State"] != "AZ"]
        df = df.drop(columns=["State"])

        # Zip code buckets for CA
        def zip_buckets(x):
            if pd.isna(x):
                return np.nan

            x = int(x)

            if x < 91911:
                return "Southern California / LA Area"

            if x < 93000:
                return "San Diego Area"
            if x < 94000:
                return "Central California"
            if x < 95200:
                return "San Francisco Bay Area"
            if x < 97000:
                return "Northern California"

            raise ValueError(f"Unexpected zip code: {x}")

        df["Zip Region"] = df["Zip"].apply(zip_buckets)
        # One sale scraped twice (same address, ZIP code and sold price, and the same year built or, where one copy
        # lacks it, the same living area; Andrej, 2026-11-12): keep the newest entry. Repeated sales of a home at
        # another price stay, as an earlier sale is history under the temporal split.
        df = df.sort_values("time_index", kind="stable").reset_index(drop=True)
        sale_key = ["Address", "Zip", "Sold Price"]
        same_sale = []
        for _, g in df[df.duplicated(sale_key, keep=False)].groupby(sale_key, sort=False):
            for a, i in enumerate(g.index[:-1]):
                if any(_same_sale(g.loc[i], g.loc[j]) for j in g.index[a + 1 :]):
                    same_sale.append(i)
        assert len(same_sale) == SAME_SALE_ROWS, f"expected {SAME_SALE_ROWS} sales scraped twice, got {len(same_sale)}"
        df = df.drop(index=same_sale).reset_index(drop=True)
        # Drop homes whose listing predates their last sale: it describes an earlier sale (see curation_comments)
        df = df[~(pd.to_datetime(df["Last Sold On"]) >= pd.to_datetime(df["Listed On"]))]
        # One sale scraped under two spellings of its address: the same description (over 50 characters), sold
        # price, ZIP code, living area and year built on two or more addresses within 600 Kaggle IDs; keep the newest
        # entry (Andrej, 2026-11-11)
        key = ["Summary", "Sold Price", "Zip", "Total interior livable area", "Year built"]
        cand = df[df["Summary"].fillna("").str.len() > 50]
        respelled = []
        for _, g in cand.fillna({"Total interior livable area": -1}).groupby(key, dropna=False):
            if (
                len(g) > 1
                and g["Address"].nunique() > 1
                and g["time_index"].max() - g["time_index"].min() <= RESPELLED_MAX_ID_SPAN
            ):
                respelled += list(g.sort_values("time_index", kind="stable").index[:-1])
        assert len(respelled) == RESPELLED_SALE_ROWS, (
            f"expected {RESPELLED_SALE_ROWS} respelled sales, got {len(respelled)}"
        )
        df = df.drop(index=respelled)
        # Drop one transaction booked on several homes: the same sold price on two or more addresses of one street and
        # ZIP code, each sold for more than 1.5 times its list price (Andrej, 2026-11-11; USE-5, CLEAN-11)
        street = df["Address"].map(_street)
        building = []
        for _, g in df.assign(street=street).groupby(["Sold Price", "Zip", "street"]):
            if g["Address"].nunique() > 1 and (g["Sold Price"] > BUILDING_PRICE_MIN_RATIO * g["Listed Price"]).all():
                building += list(g.index)
        assert len(building) == BUILDING_PRICE_ROWS, (
            f"expected {BUILDING_PRICE_ROWS} building-price sales, got {len(building)}"
        )
        df = df.drop(index=building)
        # Log scale target as it is exp distributed
        df[self.task_metadata.target_column_name] = np.log1p(df[self.task_metadata.target_column_name])
        # Rest time_index (to avoid gaps from dropping rows)
        df = df.drop(columns=["time_index"]).reset_index().rename(columns={"index": "time_index"})
        # scores with no words per level are numbers (CLEAN-14)
        df[SCORES] = df[SCORES].astype("object").apply(pd.to_numeric)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["Zip Region"],
            string=[
                "Summary",
                "Type",
                "Heating",
                "Cooling",
                "Parking",
                "Region",
                "Elementary School",
                "Middle School",
                "High School",
                "Flooring",
                "Heating features",
                "Cooling features",
                "Appliances included",
                "Laundry features",
                "Parking features",
                "City",
                "Address",
                "Zip",  # an integer in the source, so the string has no ".0"
                "Bedrooms_description",
            ],
            # "Year built" is parsed in `_clean`
            datetime={"Year built": None, "Listed On": "%Y-%m-%d", "Last Sold On": "%Y-%m-%d"},
        )
