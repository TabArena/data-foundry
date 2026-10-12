"""Curated dataset definition for `corporate_credit_rating_cat_data_set_ratings_raitings` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, drop_columns

RATIOS = {
    "COMMEQTA": "common_equity_to_total_assets",
    "LLPLOANS": "loan_loss_provision_to_total_loans",
    "COSTTOINCOME": "operating_costs_to_operating_income",
    "ROE": "return_on_equity",
    "LIQASSTA": "liquid_assets_to_total_assets",
    "SIZE": "log_total_assets",
}
"""The book's ratio columns and the names we give them, after the definitions on the book's data page."""


class CorporateCreditRatingCatDataSetRatingsRaitings(AbstractCuratedDataset):
    # Dataset
    unique_name = "corporate_credit_rating_cat_data_set_ratings_raitings"
    year = "2016"
    domain = "finance"
    source = "Other"
    source_url = "http://www.creditriskanalytics.net/datasets-private2.html"
    license = (
        "Use only in conjunction with the Credit Risk Analytics textbooks; commercial use prohibited (the agreement "
        "on the book's download form, http://www.creditriskanalytics.net/datasets.html). The site's terms add: "
        '"You must not: Republish material from Credit Risk Analytics ... Redistribute content from Credit Risk '
        'Analytics" (http://www.creditriskanalytics.net/terms.html)'
    )
    download_description = """
        We download ratings.csv from the data page of the book "Credit Risk Analytics" (Baesens, Roesch and Scheule,
        Wiley 2016). The book's site asks for a name and an agreement on http://www.creditriskanalytics.net/datasets.html
        before it shows the data page; the file link itself needs no login. The page also offers the same 197 rows as
        ratings.sas7bdat (identical values). Copies of the same ratings.csv sit on GitHub (for example in
        dpicone1/Credit-Risk-Anaytics-The-R-Companion, same sha256).

        mkdir -p local-data-warehouse/corporate_credit_rating_cat_data_set_ratings_raitings
        wget -O local-data-warehouse/corporate_credit_rating_cat_data_set_ratings_raitings/ratings.csv http://www.creditriskanalytics.net/uploads/1/9/5/1/19511601/ratings.csv

        sha256 of ratings.csv: 7cabb6bbad6eecba5af853f878f465298815affcbcc866b094c524799f06cfcc

        Not OpenML 46372 (the record's first link, 5,000 rows, uploaded 2024 from a Medium article's GitHub
        repository Polanitz/Multiclass-Classification-for-Corporate-Credit-Ratings): its rows are generated from these
        197 (see curation_comments).
    """
    bibtex = r"""
        @book{baesens2016credit,
          title={Credit Risk Analytics: Measurement Techniques, Applications, and Examples in {SAS}},
          author={Baesens, Bart and R{\"o}sch, Daniel and Scheule, Harald},
          publisher={John Wiley \& Sons},
          address={Hoboken, NJ},
          year={2016},
          isbn={978-1-119-14398-7},
          doi={10.1002/9781119449560}
        }
    """
    curation_comments = """
        We start with ratings.csv from the data page of the book Credit Risk Analytics (Baesens, Roesch and Scheule 2016): 197 rated institutions, one row each, with an anonymised id (`spid`), the rating "numerically encoded (1 = AAA, etc.)" and six financial ratios.

        - Prediction point: an institution whose financial statements are known but whose agency rating is not; we map it to the agency's scale from the six ratios, as the R Companion's code for chapter 8 ("Low Default Portfolios") does with an ordered logit. The data page names no agency, years or country, so how the statement date relates to the rating date is unknown.
        - Not OpenML 46372 (the record's first link): its 5,000 rows are generated from these 197, each value drawn uniformly between the minimum and maximum of the book's rows with the same rating (all 30,000 values lie inside those ranges; none is a book row).
        - Target: `rating_notch`, the book's rating code from 1 (AAA) to 10, as regression with RMSE. The R Companion's chapter 8 code scores the model by the notch difference between the actual and the predicted rating, so the order and the distance carry the task; as 10 classes, three codes would hold 3-5 rows (decision table).
        - We drop `spid`, an anonymised id with no documented meaning. Its values sit in two ranges, and a flag for the range lifts ridge R^2 from 0.286 to 0.299; we drop it anyway, since no source says what the ranges are.
        - The six ratios are renamed after the data page's definitions (`RATIOS`).
        - No missing values and no duplicate rows. Negative loan-loss provisions (released provisions) and negative returns on equity (loss years) are real values.
        - Anomaly: the file is two blocks of 98 and 99 rows, each sorted by rating, with no institution in both. A random forest cannot tell the blocks apart (ROC AUC 0.52), so we read them as two halves of one cross-section; the base class shuffles the rows.
        - Anomaly: one institution (code 8) has `log_total_assets` 10.59, against 15.33 for the next smallest. We keep it: ridge fits it, and read as a unit slip it would fit worse.
        - Note: we read the codes as notches (AAA to BBB-). As letter grades, the 57 institutions with codes 7-10 would be rated CCC or worse, while codes 7, 8 and 9 have median ROE of 11%, 8% and 10%. The data page gives only "1 = AAA", so this reading is not verified.
        - Note: the rated entities are banks, although the data page says "corporate ratings": loan-loss provisions to loans and liquid assets to total assets are bank ratios.
        - Note: the closest tenth of the test rows shares its nearest training row's code in 25.5% of cases, against 22.4% for all rows, so there are no clusters of near-copies, the artefact for which the same book's HMEQ data was retired.
    """

    # Task
    target = "rating_notch"
    problem_type = "regression"
    accepted_check_warnings = {
        "task_target_low_cardinality": (
            "The target is a rating code on a 10-notch scale (1 = AAA). The R Companion's chapter 8 code (a reader's "
            "transcription; the book text was not read) scores the ordinal rating model by the notch difference "
            "between the actual and the predicted rating, so regression keeps the order and the distance (as "
            "wine_quality does for its 0-10 grade); as 10 classes, three codes would hold 3-5 rows."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "ratings.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # `spid` is an anonymised id, one per institution, with no documented meaning.
        df = drop_columns(raw, ["spid"])
        # The rating code (1 = AAA, one notch per step) is the regression target; the ratios get readable names.
        return df.rename(columns={"rating": self.target, **RATIOS})

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        by_rating = raw.groupby("rating")
        table = pd.DataFrame(
            {
                "rows": by_rating.size(),
                "median log_total_assets": by_rating["SIZE"].median().round(2),
                "median common_equity_to_total_assets": by_rating["COMMEQTA"].median().round(3),
                "median liquid_assets_to_total_assets": by_rating["LIQASSTA"].median().round(3),
                "median loan_loss_provision_to_total_loans": by_rating["LLPLOANS"].median().round(4),
                "median return_on_equity": by_rating["ROE"].median().round(3),
            }
        )
        table.index.name = "rating code (1 = AAA)"
        return [
            Decision(
                "The rating code is a regression target, not 10 classes",
                "The R Companion's chapter 8 code (a reader's transcription) scores the rating model by the notch "
                "difference between the actual and the predicted rating, and the ratios move with the code as a "
                "1 = AAA scale should (Spearman with the code: log_total_assets -0.50, liquid assets -0.39, equity "
                "+0.26, loan-loss provisions +0.20, return on equity -0.17, costs to income +0.10). As classes, "
                "codes 1, 2 and 10 would hold 3, 5 and 4 institutions.",
                table,
            )
        ]
