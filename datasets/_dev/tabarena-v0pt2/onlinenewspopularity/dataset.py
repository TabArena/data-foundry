"""Curated dataset definition for `onlinenewspopularity` (data-foundry v2). Evidence: README.md."""

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
    drop_columns,
)

# The URL path holds the publication date: http://mashable.com/YYYY/MM/DD/<slug>/
URL_PATTERN = r"^http://mashable\.com/(\d{4})/(\d{2})/(\d{2})/([^/]+)/$"
# The crawl date of the release (UCI: "Acquisition date: January 8, 2015"), from which `timedelta` counts back.
ACQUISITION_DATE = "2015-01-08"
CHANNEL_FLAGS = {
    "data_channel_is_lifestyle": "lifestyle",
    "data_channel_is_entertainment": "entertainment",
    "data_channel_is_bus": "business",
    "data_channel_is_socmed": "social_media",
    "data_channel_is_tech": "tech",
    "data_channel_is_world": "world",
}
WEEKDAY_FLAGS = [
    "weekday_is_monday",
    "weekday_is_tuesday",
    "weekday_is_wednesday",
    "weekday_is_thursday",
    "weekday_is_friday",
    "weekday_is_saturday",
    "weekday_is_sunday",
    "is_weekend",
]
KEYWORD_SHARES = [
    "kw_min_min",
    "kw_max_min",
    "kw_avg_min",
    "kw_min_max",
    "kw_max_max",
    "kw_avg_max",
    "kw_min_avg",
    "kw_max_avg",
    "kw_avg_avg",
]
SELF_REFERENCE_SHARES = ["self_reference_min_shares", "self_reference_max_shares", "self_reference_avg_sharess"]
POSITIVE_POLARITY = ["avg_positive_polarity", "min_positive_polarity", "max_positive_polarity"]
NEGATIVE_POLARITY = ["avg_negative_polarity", "min_negative_polarity", "max_negative_polarity"]
# Statistics of the article body, undefined for a body without words.
BODY_STATISTICS = [
    "n_unique_tokens",
    "n_non_stop_unique_tokens",
    "average_token_length",
    "global_subjectivity",
    "global_sentiment_polarity",
    "global_rate_positive_words",
    "global_rate_negative_words",
    "rate_positive_words",
    "rate_negative_words",
    *POSITIVE_POLARITY,
    *NEGATIVE_POLARITY,
]
LDA_TOPICS = ["LDA_00", "LDA_01", "LDA_02", "LDA_03", "LDA_04"]
# The one share count in the release that is not a whole number (a parsing artefact).
FRACTIONAL_SHARES = 1.59


def _url_dates(urls: pd.Series) -> pd.Series:
    """The publication date in each article URL, as ``YYYY-MM-DD`` text."""
    parts = urls.str.extract(URL_PATTERN)
    if parts.isna().any().any():
        raise ValueError("A URL does not follow http://mashable.com/YYYY/MM/DD/<slug>/.")
    return parts[0] + "-" + parts[1] + "-" + parts[2]


def _channels(df: pd.DataFrame) -> np.ndarray:
    """The data channel from its one-hot block; an article with no flag set is "other"."""
    flags = df[list(CHANNEL_FLAGS)]
    if (flags.sum(axis=1) > 1).any():
        raise ValueError("An article has more than one data channel flag.")
    return np.select([flags[c] == 1 for c in CHANNEL_FLAGS], list(CHANNEL_FLAGS.values()), "other")


class Onlinenewspopularity(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How often will a Mashable article be shared?",
        use_case=(
            "Before publishing, a news editor estimates an article's shares and tries changes to the article and its "
            "publication day, as the source's decision-support system does (Fernandes et al. 2015)."
        ),
        row=("One article published on Mashable from 7 January 2013 to 27 December 2014 (39,643 articles)."),
        predicted=(
            "The number of shares at the crawl of 8 January 2015, on a log scale; the source's popular/unpopular task"
            " cuts this count at 1,400."
        ),
        known=(
            "Statistics of the text and page (word counts, title length, links, images, videos, sentiment, "
            "subjectivity, keywords), the channel (business, tech and others), the earlier Mashable articles it links "
            "to or shares keywords with and their shares at the crawl of 8 January 2015, and the publication date."
        ),
        split=(
            "Each test window is two weeks of articles (24 August to 27 December 2014); training is every article "
            "published at least a week before, as for a model refit every two weeks."
        ),
        changes=(
            "We take the publication date from the URL and drop the weekday flags and the age column, which follow a "
            "later date for 24% of the articles, and the topic scores, fitted on all texts including the test ones."
        ),
        fit="direct",
        fit_reason=(
            "Articles are scored before publication on later windows, as in the source's system. Two potential leaks "
            "are kept and noted, which do not make the fit approximate (USE-8 as amended 2026-10-21): the keyword "
            "and link statistics use other articles' shares at the crawl, and for 80% of the test rows the keyword "
            "statistics include same-day articles published later (R² 0.158 with both, 0.135 and 0.143 without each)."
        ),
    )

    # Dataset
    unique_name = "onlinenewspopularity"
    year = "2015"
    domain = "technology & internet"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5NS3V"
    license = "CC BY 4.0"
    download_description = """
        mkdir -p local-data-warehouse/onlinenewspopularity
        wget -P local-data-warehouse/onlinenewspopularity https://archive.ics.uci.edu/static/public/332/online+news+popularity.zip
        unzip local-data-warehouse/onlinenewspopularity/online+news+popularity.zip -d local-data-warehouse/onlinenewspopularity

        The zip (7,476,401 bytes, sha256 dba2ae526f62ccef6f2f8efb53b0268319f4d0d2719bb98d88958cfe31d58a22, files
        dated 2015-05-31) holds OnlineNewsPopularity/OnlineNewsPopularity.csv and OnlineNewsPopularity.names; the
        definition reads the CSV. UCI states the license (CC BY 4.0) on the dataset page; the articles themselves
        belong to Mashable, so the release holds statistics of each article and its URL, not its text.
    """
    bibtex = r"""
        @inproceedings{fernandes2015proactive,
          author = {Fernandes, Kelwin and Vinagre, Pedro and Cortez, Paulo},
          title = {A Proactive Intelligent Decision Support System for Predicting the Popularity of Online News},
          booktitle = {Progress in Artificial Intelligence. 17th Portuguese Conference on Artificial Intelligence, EPIA 2015},
          series = {Lecture Notes in Computer Science},
          volume = {9273},
          pages = {535--546},
          publisher = {Springer},
          year = {2015},
          doi = {10.1007/978-3-319-23485-4_53}
        }
    """
    curation_comments = """
        We start with OnlineNewsPopularity.csv from the UCI repository (dataset 332): Mashable articles published from 2013-01-07 to 2014-12-27, with 58 features extracted from each article's HTML and its shares at the crawl of 2015-01-08 (Fernandes et al. 2015). The R^2 values below are LightGBM on our 9 windows, averaged over 3 seeds.

        - Prediction point: before publication. The source's system "analyzes articles prior to their publication" (abstract) and suggests changes to the article and its publication day; the earlier Mashable articles are known, with their shares at the crawl of 2015-01-08 (see the potential leaks below).
        - Target: `log_shares`, the natural log of the shares at the crawl. The source's binary task (popular above 1,400 shares) is a cut of this count.
        - Time: the publication date comes from the URL, which Mashable's archived pages confirm; the URL is dropped.
        - We drop `timedelta` and the seven weekday flags with `is_weekend`. They follow the authors' date, 1 to 5 days after the URL date for 24% of the articles, which is not known before publication and goes with the outcome (decision table).
        - The six `data_channel_is_*` flags become one categorical `data_channel`, `other` when no flag is set.
        - We drop one article whose text processing failed (counts in its rate columns, zero topic and sentiment values).
        - Proxy missing values, set to missing: statistics of words, links or earlier articles that do not exist (no body words, no positive or negative words, a self-reference maximum of 0, the first day's keywords) and negative keyword statistics (-1 and averages that include it). The share count 1.59, the only one that is not a whole number (`kw_max_min` 111 rows, `self_reference_min_shares` 10, `self_reference_max_shares` 3; 120 rows), is set to missing with the averages that include it.
        - We drop `n_non_stop_words`, which only repeats `n_tokens_content` > 0 (1 with body words, 0 without), and `rate_negative_words`, which is 1 - `rate_positive_words` in every row where both are defined.
        - We drop the five LDA topic columns: the paper applied LDA "to all Mashable texts" (Sec. 2.1), test windows included, and without the texts it cannot be refitted per window (decision table).
        - Potential leak, kept on purpose: the keyword and self-reference statistics hold other articles' share counts at the crawl of 2015-01-08, not at publication. They include the counts of articles from the gap week and from earlier in the same test window (at least 0.9% and 0.4% of the test rows), whose shares an editor would have seen younger. Masking the 2,907 cells traced to an article less than 8 days older than the row changes R^2 by -0.0004, less than the spread over seeds (0.002). Without the keyword columns R^2 falls from 0.158 to 0.135, without the self-reference columns to 0.143. Revisit if a source with counts at publication appears.
        - Potential leak, kept on purpose: the keyword statistics summarize the articles with an earlier authors' date, so for the shifted rows (80% of the test rows, 6,627 of 8,289; the three newest windows entirely) they include articles of the same day published hours later. These bring no measurable gain: the keyword columns lower the squared error by 0.0187 for shifted and 0.0264 for unshifted test articles (difference -0.008, standard error 0.008). The self-reference statistics come from the page's links at the crawl, so a link added after publication can point to a newer article; such links are rare (4 of 895 traceable articles link to an article 1 to 2 days newer, about what chance gives). The page counts (`num_hrefs`, `num_imgs` and the rest) are read at the crawl too.
        - We keep the newest articles. The paper discarded articles less than three weeks old, but the shares of the 481 articles from 2014-12-18 on show no deficit (decision table).
        - No duplicate rows; the URLs are unique.
        - Text: the release holds statistics of the text only; a TF-IDF encoding of the URL slug does not help (R^2 0.152 with it).
    """

    # Task
    target = "log_shares"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "The paper scores a binary task (shares >= 1,400 threshold) with accuracy/F1/AUC; we ship a regression on "
            "log shares, so the original target is not ours; rmse on the log target is the regression fallback."
        )
    )

    # Splits: nine two-week windows, the size of the paper's rolling test sets, with a one-week gap.
    temporal = Temporal(
        on="publication_date",
        splits=TemporalSplits(window=2, unit="weeks", n_windows=9, gap=1),
    )
    splits_comment = """
        Expanding-window temporal splits: 9 test windows of two calendar weeks (Sunday to Saturday), from 2014-08-24 to 2014-12-27, newest first, with 769 to 1,001 articles each; train is every article published at least one week before the window starts (30,967 to 38,385 articles, 78% of the data or more). A model is refit every two weeks and predicts the articles of the next two weeks before they are published, as in the paper's rolling windows of L = 1,000 predictions (Sec. 3.1, p. 7; 1,000 articles are two to three weeks of Mashable's output). The one-week gap keeps the training labels to shares that had settled at the cutoff (the paper: the shares of some articles younger than 4 days had not, Sec. 2.1, p. 3). The labels are the counts at the 2015-01-08 crawl for train and test alike, so the gap stands in for the settling time only. The paper trains on a sliding window of W = 10,000 articles; we expand the train side, which keeps a full season before the first window and scores no lower (R^2 0.158 expanding, 0.146 sliding). Nine windows are the 3 x 3 splits an IID task of this size would get.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # The header and the values carry a space after every comma.
        return pd.read_csv(raw_dir / "OnlineNewsPopularity" / "OnlineNewsPopularity.csv", skipinitialspace=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # One article is a processing failure (counts instead of rates, no topic or sentiment values): drop it.
        df = raw[raw["n_unique_tokens"] <= 1]
        # The publication date from the URL; `timedelta` and the weekday flags follow another, later date.
        df["publication_date"] = _url_dates(df["url"])
        df["data_channel"] = _channels(df)

        # Proxy missing values: statistics of words, links or earlier articles that do not exist.
        df.loc[df["n_tokens_content"] == 0, BODY_STATISTICS] = np.nan
        df.loc[df["global_rate_positive_words"] == 0, POSITIVE_POLARITY] = np.nan
        df.loc[df["global_rate_negative_words"] == 0, NEGATIVE_POLARITY] = np.nan
        no_polar_words = (df["rate_positive_words"] == 0) & (df["rate_negative_words"] == 0)
        df.loc[no_polar_words, ["rate_positive_words", "rate_negative_words"]] = np.nan
        # The share count 1.59 is not a whole number: missing, with the averages that include it.
        kw_fraction = df["kw_max_min"] == FRACTIONAL_SHARES
        df.loc[kw_fraction, ["kw_max_min", "kw_avg_min"]] = np.nan
        self_min = df["self_reference_min_shares"] == FRACTIONAL_SHARES
        self_max = df["self_reference_max_shares"] == FRACTIONAL_SHARES
        df.loc[self_min, "self_reference_min_shares"] = np.nan
        df.loc[self_max, "self_reference_max_shares"] = np.nan
        df.loc[self_min | self_max, "self_reference_avg_sharess"] = np.nan
        # No linked Mashable article with a known share count (real counts are at least 1).
        df.loc[df["self_reference_max_shares"] == 0, SELF_REFERENCE_SHARES] = np.nan
        # No earlier article with the keywords (the first day); negative values (-1, and averages that include it).
        df.loc[df["kw_max_max"] == 0, KEYWORD_SHARES] = np.nan
        df[KEYWORD_SHARES] = df[KEYWORD_SHARES].mask(df[KEYWORD_SHARES] < 0)

        # Target: the log of the shares (1 to 843,300).
        df["log_shares"] = np.log(df["shares"])
        return drop_columns(
            df,
            [
                "url",
                "timedelta",
                "shares",
                "n_non_stop_words",
                "rate_negative_words",
                *CHANNEL_FLAGS,
                *WEEKDAY_FLAGS,
                *LDA_TOPICS,
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["data_channel"], datetime={"publication_date": "%Y-%m-%d"})

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        url_date = pd.to_datetime(_url_dates(raw["url"]))
        flag_date = pd.Timestamp(ACQUISITION_DATE) - pd.to_timedelta(raw["timedelta"], unit="D")
        shift = (flag_date - url_date).dt.days.rename("days the authors' date falls after the URL date")
        log_shares = np.log(raw["shares"])
        relative = log_shares - log_shares.groupby(url_date).transform("mean")
        early = url_date < "2014-04-01"
        shifts = shift.value_counts().sort_index(kind="stable")
        by_shift = pd.DataFrame(
            {
                "articles": shifts,
                "mean log shares relative to the same URL date": relative.groupby(shift).mean().round(3),
                "standard error": relative.groupby(shift).sem().round(3),
                "articles before April 2014": shift[early].value_counts().reindex(shifts.index, fill_value=0),
                "their mean": relative[early]
                .groupby(shift[early])
                .mean()
                .reindex(shifts.index)
                .map(lambda v: "" if pd.isna(v) else f"{v:.3f}"),
            }
        )

        channel = pd.Series(_channels(raw), index=raw.index, name="data_channel")
        topics = raw[LDA_TOPICS].groupby([channel, url_date.dt.year.rename("year")]).mean().round(2)

        week = url_date.dt.to_period("W").astype(str).rename("week")
        weekly = (
            raw["shares"]
            .groupby(week)
            .agg(articles="size", median_shares="median", share_at_least_1400=lambda s: round((s >= 1400).mean(), 2))
        )
        return [
            Decision(
                "Publication date from the URL; `timedelta` and the weekday flags dropped",
                "The weekday flags follow 2015-01-08 minus `timedelta`, a date 1 to 5 days after the URL date for 24% "
                "of the articles (all of December 2014), while Mashable's pages carry the URL date. Within a "
                "publication date, the shifted articles have more shares, and the shifted date is not known before "
                "publication.",
                by_shift,
            ),
            Decision(
                "LDA topic columns dropped: one topic model, fitted on all texts",
                "Every channel loads on the same topics in both years, so there is one topic model, and the paper says "
                "it was fitted on all Mashable texts (Sec. 2.1, p. 4), the test windows' texts included. The columns "
                "cannot be refitted per window and carry no measurable signal (R^2 0.158 with and without them).",
                topics,
            ),
            Decision(
                "The newest articles kept: their shares had settled",
                "The paper dropped articles under three weeks old, but the release keeps them; the last weeks show no "
                "deficit of shares against the weeks before.",
                weekly.tail(9),
            ),
        ]
