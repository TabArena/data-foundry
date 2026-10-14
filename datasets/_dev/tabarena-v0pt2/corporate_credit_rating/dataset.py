"""Curated dataset definition for `corporate_credit_rating` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, TaskSummary, drop_columns

# The class of each letter grade in the file. CCC, CC and C form one class, as in the rating table the uploader
# follows (notebook cell 15, from Investopedia: "CCC/CC/C ... Highest Risk"); AAA (7 rows) is dropped, as the uploader
# did. Defaults are dropped as well: S&P's "D" and Moody's "C" (the same table: "In Default"), see `_rating_class`.
RATING_CLASSES = {
    "AA": "AA",
    "A": "A",
    "BBB": "BBB",
    "BB": "BB",
    "B": "B",
    "CCC": "CCC/CC/C",
    "CC": "CCC/CC/C",
    "C": "CCC/CC/C",
}
MOODYS = "Moody's Investors Service"


def _rating_class(raw: pd.DataFrame) -> pd.Series:
    """The class of every row of the raw file; missing for the rows we drop (AAA, S&P's "D", Moody's "C")."""
    moodys_default = (raw["Rating"] == "C") & (raw["Rating Agency Name"] == MOODYS)
    return raw["Rating"].map(RATING_CLASSES).where(~moodys_default)


class CorporateCreditRating(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Which letter grade would a rating agency give this company, judging from its financial statements?"),
        use_case=(
            "An analyst estimates the grade an agency would give a company that has no rating of its own (a shadow "
            "rating), from its financial statements and sector (the uploader's question)."
        ),
        row=(
            "One credit rating of a US company by one of five agencies, 2005-2016, with the company's financial "
            "ratios of that fiscal year (2,020 ratings of 592 companies, at most one per company and year)."
        ),
        predicted=("The letter grade, one of six classes from AA to a merged CCC/CC/C; BBB is the most common (33%)."),
        known=(
            "25 financial ratios (liquidity, profitability, debt, cash flow, per-share values), the sector, the "
            "agency and the rating date."
        ),
        split=(
            "Whole companies are held out, so the test data stands for companies whose ratings the model has not seen."
        ),
        changes=(
            "We split by company instead of at random, as a rated company's current grade is public and repeats in "
            "72% of its next ratings. We merge CCC, CC and C and drop the 7 AAA ratings and the two defaults."
        ),
        fit="direct",
        fit_reason=(
            "Statements and sector are what an analyst has for an unrated company, and held-out companies match that."
            " Each row's agency and date are an arbitrary pick among the company's ratings of that year, and "
            "companies delisted before June 2020 are missing."
        ),
    )

    # Dataset
    unique_name = "corporate_credit_rating"
    year = "2020"
    domain = "finance"
    source = "GitHub"  # the uploader's repository held the file 17 days before his Kaggle upload
    source_url = "https://github.com/Agewerc/ML-Finance"
    license = "CC BY 4.0"
    download_description = """
        We download Alan Gewerc's Kaggle dataset (one version, file of 2020-07-24, CC BY 4.0 on the data card). He
        first published the same file as data/corporate_rating.csv in his GitHub repository (commit 83411e2 of
        2020-07-07), next to the script that built it (generateCreditRatingDataset.py) and its inputs; OpenML 43344 is
        a re-upload.
        corporate_rating.csv: sha256 ba6bdd88a63996949edbb88cf9f1dc52af68a84f4590d067acdcdfe3515b7409

        mkdir -p local-data-warehouse/corporate_credit_rating && cd local-data-warehouse/corporate_credit_rating
        kaggle datasets download agewerc/corporate-credit-rating
        unzip corporate-credit-rating.zip && rm corporate-credit-rating.zip

        Pinned alternative (byte-identical):
        wget https://raw.githubusercontent.com/Agewerc/ML-Finance/83411e245eab6b4a92dc57bbc207defd41abccfd/data/corporate_rating.csv
    """
    bibtex = r"""
        @misc{gewerc2020corporate,
          author = {Gewerc, Alan},
          title = {Corporate Credit Rating: Credit Ratings of Big {US} Firms and their Financials},
          year = {2020},
          howpublished = {\url{https://www.kaggle.com/datasets/agewerc/corporate-credit-rating}},
          note = {Kaggle dataset; ratings from the opendatasoft credit ratings history, financial ratios from
            Financial Modeling Prep; built with https://github.com/Agewerc/ML-Finance}
        }
    """
    curation_comments = """
        We start with corporate_rating.csv from Alan Gewerc's Kaggle dataset: 2,029 credit ratings of 593 US companies,
        given by five agencies from 2005 to 2016, each with 25 annual financial ratios, the sector and the rating date.

        - Prediction point: from a company's financial statements for a fiscal year and its sector, an analyst estimates
          the letter grade a given agency would give a company without a rating of its own (a shadow rating, the
          uploader's question). The ratios are of the previous calendar year for a rating from January to June and of
          the same year for one from July to December (last bullet).
        - Grouped by company (Symbol), not temporal as the record's tag says: a rated company's current rating is
          public, so a model from financials alone serves companies without a rating. On the quarterly windows of a
          first version, 86.6% of the test ratings were of a company with a training row, and carrying its latest letter
          forward beat a random forest (log-loss skill 0.39 against 0.31; decision table).
        - Target: the letter grade. CCC, CC and C form one class "CCC/CC/C", as in the rating table the uploader follows
          (notebook cell 15). We drop the 7 AAA rows and the two defaults, S&P's "D" and Moody's "C"; the uploader
          dropped AAA and D too (decision table), but we do not merge into his four risk tiers.
        - We drop Name (one to one with Symbol); Symbol is the group column. The rating agency and the rating date
          (datetime) stay features: both are known when a rating is estimated, and the agencies' levels differ.
        - Anomaly: the build script keeps, per company and fiscal year, the first rating in the file order of the
          ratings history, so a row's agency and date are an arbitrary pick among the company's ratings of that year;
          Moody's Aa3, Ba3, B3 and Caa3 actions never entered the file.
        - Anomaly: 171 rows carry one of several letter grades the agency gave the company's debt on that day. We keep
          them as published (random forest log-loss skill 0.157 with these rows, 0.152 without).
        - Anomaly: the agencies cover different years, so the class shares move with the mix (decision table).
        - Anomaly: the companies are those listed in June 2020; companies delisted by then, often after a default, have
          no row.
        - Anomaly: some ratios hold impossible or extreme values, and some zeros and ones stand for items the statements
          did not report. We keep them as reported: new rows record them alike.
        - Note: ebitPerRevenue equals pretaxProfitMargin in 90.8% of the rows, and companyEquityMultiplier equals
          debtEquityRatio + 1 in 89.6%; we keep all four.
        - Note: no duplicate rows; a company has at most one row per fiscal year.
        - Note: ratings from July to December come with statements published after the rating, but these tell no more
          about it than the previous year's (log loss -0.018 with the previous statements, 95% CI -0.046 to +0.009). We
          keep all rows.
    """

    # Task
    target = "Rating"
    problem_type = "multiclass_classification"

    # Splits: grouped by company (shadow rating of a company without a rating).
    grouping = Grouping(
        on="Symbol",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a company (its ticker, Symbol); its rows are ratings of different fiscal years, at most one per
            fiscal year. The use case is a shadow rating: estimating the letter grade an agency would give a company
            from its financial statements, for a company without a rating of its own. The uploader frames the task this
            way ("Is it possible to predict what credit profile a company will receive from a rating agency based on
            its financial indicators?", notebook cell 47) and fits his models on the sector and the ratios alone. A rated
            company's current rating is public and repeats in 72% of its next ratings, so holding out whole companies
            tests the model on companies whose ratings it has not seen. Each rating is one prediction, made from its own
            row.
        """,
    )
    splits_comment = """
        Grouped 3-fold cross-validation by company (Symbol), 10 repeats: every rating of a test company is unseen in
        training. The uploader's notebook split the ratings at random (80/20, cell 49), which puts other fiscal years of
        the same company in training.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "corporate_rating.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Letter grades to the six classes; AAA and the two defaults are dropped (see RATING_CLASSES).
        df["Rating"] = _rating_class(df)
        df = df[df["Rating"].notna()]
        # The company's name; its ticker (Symbol, one to one) stays as the group column.
        return drop_columns(df, ["Name"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["Rating Agency Name", "Sector", "Symbol"],
            datetime={"Date": "%m/%d/%Y"},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        grades = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "CC", "C", "D"]
        classes = _rating_class(raw).fillna("dropped")
        mapping = pd.crosstab(raw["Rating"], classes).reindex(grades)
        date = pd.to_datetime(raw["Date"], format="%m/%d/%Y")
        agencies = pd.crosstab(date.dt.year.rename("year"), raw["Rating Agency Name"])
        # Ratings per company and how often a rating repeats the company's previous one (the shipped rows).
        kept = raw.assign(date=date, rating_class=_rating_class(raw)).dropna(subset=["rating_class"])
        kept = kept.sort_values(["Symbol", "date"], kind="stable")
        previous = kept.groupby("Symbol")["rating_class"].shift()
        with_previous = previous.notna()
        persistence = pd.Series(
            {
                "companies": kept["Symbol"].nunique(),
                "ratings": len(kept),
                "companies with 2 or more ratings": int((kept.groupby("Symbol").size() >= 2).sum()),
                "ratings with an earlier rating of the company": int(with_previous.sum()),
                "of these, the same class as that earlier rating": (
                    f"{(kept['rating_class'] == previous)[with_previous].mean():.1%}"
                ),
            },
            name="value",
        )
        return [
            Decision(
                "Letter grades as classes, CCC/CC/C merged, AAA and defaults dropped",
                "The agencies' letter categories, with the three lowest merged as in the uploader's rating table. "
                "AAA (7 rows) and the defaults (S&P's D, Moody's C; 2 rows) are too few; the uploader dropped AAA "
                "and D too.",
                mapping,
            ),
            Decision(
                "Grouped by company, not temporal",
                "Most companies have several ratings and a rating mostly repeats the company's previous one, so on a "
                "temporal split the models mainly recognise known companies. A model from financials alone serves "
                "companies without a rating: whole companies are held out.",
                persistence,
            ),
            Decision(
                "Agencies cover different years",
                "The ratings history holds different years for each agency (rows of the raw file per rating year), "
                "so the agency mix and with it the class shares change over time; the agency is a feature.",
                agencies,
            ),
        ]
