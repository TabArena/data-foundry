"""Curated dataset definition for `fiat_500` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_foundry.definition import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    TaskSummary,
    TimeBasis,
)

# one car: the trim, engine power, age and mileage of a listing (the owner count differs between dealers)
CAR_KEY = ["model", "engine_power", "age_in_days", "km"]
# the group: a car whose trim two dealers entered differently is still one car
GROUP_KEY = ["engine_power", "age_in_days", "km"]


class Fiat500(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="At what price is a used Fiat 500 listed?",
        use_case=(
            "For example, a seller in Italy sets the asking price of a used Fiat 500, or a buyer checks whether a "
            "listing is overpriced, by comparison with current listings."
        ),
        row=(
            "One used Fiat 500 listed on the Italian site automobile.it (1,420 cars from 1,538 listings, uploaded to "
            "Kaggle in 2020; the date of the crawl is not stated)."
        ),
        predicted="The listed price, from 2,500 to 11,100; the currency is not stated.",
        known=(
            "The trim (lounge, pop or sport), engine power, age in days, mileage, number of previous owners, and the "
            "location as latitude and longitude."
        ),
        split=(
            "Random cars of the same crawl, standing for new listings in the same market, grouped by car: a car "
            "whose trim two dealers entered differently stays on one side."
        ),
        changes=(
            "We keep one row per car: 118 listings repeat the trim, engine power, age and mileage of another, the same "
            "car scraped twice or listed at several places."
        ),
        fit="direct",
        fit_reason=(
            "The features are what a listing shows, and a held-out listing is a car to price. The target is the "
            "asking price, not the sale price, and the listings come from one crawl."
        ),
    )

    # Dataset
    unique_name = "fiat_500"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/paolocons/another-fiat-500-dataset-1538-rows",
            license="CC0: Public Domain",
            year="2020",
            bibtex=r"""
                @misc{paolocons2020fiat,
                  author       = {Kaggle User Paolocons},
                  title        = {Another Dataset on Used Fiat 500 (1538 Rows)},
                  year         = {2020},
                  howpublished = {\url{https://www.kaggle.com/datasets/paolocons/another-fiat-500-dataset-1538-rows}},
                  note         = {Kaggle dataset},
                }
            """,
        ),
    )
    download_description = """
        kaggle datasets download paolocons/another-fiat-500-dataset-1538-rows -p local-data-warehouse/fiat_500/ && unzip local-data-warehouse/fiat_500/another-fiat-500-dataset-1538-rows.zip -d local-data-warehouse/fiat_500/ && rm local-data-warehouse/fiat_500/another-fiat-500-dataset-1538-rows.zip
    """
    curation_comments = """
        We start with automobile_dot_it_used_fiat_500_in_Italy_dataset_filtered.csv from Kaggle.

        - One row is one used Fiat 500 listed for sale in Italy, from "a query done on an website specialized in used cars" (data card); the file name names automobile.it. The target is the listed price.
        - Currency: not stated.
        - Crawl date: not stated. The file was uploaded on 2020-04-07, and age_in_days counts "from the time the dataset has been created" (data card).
        - Filter: not stated. The file name ends in "_filtered", but neither the data card nor the author's notebooks say what was removed.
        - We keep one row per car, its first listing (1,420 rows): 118 rows repeat the model, engine power, age and mileage of another (Lennart, 2026-10-14; the owner count left the key on 2026-11-26, Andrej). 18 are exact copies, most 12-14 rows after the first (the crawler saw the listing on two result pages), and one car with an odd mileage such as 9,248 km appears at up to 9 places a median 396 km apart, mostly at one price. The owner count is no part of the key: the uploader's second file of the same crawl (Kaggle, "Small dataset about used Fiat 500 sold in Italy") holds 41 of these listings and gives another owner count for 25 of them, so 8 cars stayed twice under a key with it.
        - The copies are not chance: with mileages shuffled among cars of the same trim, power and half-year of age (one row per key, 1,000 draws), distinct cars share trim, power, month and an odd mileage 1.3 times per draw against 82 repeats in the file, and a round mileage 10.2 times against 36, so about 10 of the round-mileage merges are likely different cars (under 1% of the rows). Price before and after: mean 8,576 over all listings, 8,498 kept; median 9,000 and 8,900.
        - Mileage 56,779 km: kept as recorded (2026-11-26, Andrej: "a valid pattern in real data and not a leak"). Twelve listings at seven places give exactly this mileage for cars of 1.2 to 12.8 years, all kept; it likely stands for a reading the advert did not give.
        - Partial order, left unordered (2026-11-01, CLEAN-14): `model`: pop is the base trim; lounge and sport are both
          above it but not ranked against each other.
        - Split by car (2026-11-26, Andrej): a random split that keeps every car on one side. `car_id` numbers the rows of equal engine power, age and mileage (1,406 cars); it is no model input. After the one-row-per-car key 14 cars still have two rows, because two dealers entered another trim: a car of 701 days and 39,162 km is listed as pop and as sport at the same two places at the same prices. The other 13 pairs are 3 with an odd mileage (one at 56,779 km) and 10 with a round one, which may be different cars and cost nothing on one side. Under random 3-fold splits 1.3% of the test rows had such a twin in training.
    """
    split_leaf = "L-FILL.unit"
    time_basis = TimeBasis(
        "RetrospectiveFillIn",
        """
        one crawl of listings (published on Kaggle in 2020; the crawl date is not stated),
        whose prices the use case fills in for the same market. It cannot test a later market.
        """,
    )

    # Task
    target = "price"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "Kaggle dataset without a competition or paper; the data card says only 'to train myself and test regression "
            "algorithms', no metric named"
        ),
    )
    grouping = Grouping(
        on="car_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a car: the listings that agree in engine power, age in days and mileage (1,406 cars from the 1,420 rows; 14 with two rows, whose trim two dealers entered differently). The use case prices a car newly listed, so a test car is new to the model with all its listings and cannot be priced off its own listing at another dealer. Each row is one prediction, made from its listing.
        """,
    )

    # Splits
    splits_comment = """
        Random splits grouped by car: every listing of a car stays on one side, so a model prices cars it has not seen. The cars are one crawl, so the split fills in prices of the same market and does not test a later one.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/automobile_dot_it_used_fiat_500_in_Italy_dataset_filtered.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # One row per car: the same model, power, age and mileage again is the same car listed again; dealers
        # disagree on the owner count, so it is no part of the key
        df = raw.drop_duplicates(subset=CAR_KEY, keep="first").copy()
        # a car whose trim two dealers entered differently keeps two rows: group them so both stay on one side
        df["car_id"] = df.groupby(GROUP_KEY, sort=False).ngroup().map("car_{:04d}".format)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "model",
                "car_id",
            ],
        )
