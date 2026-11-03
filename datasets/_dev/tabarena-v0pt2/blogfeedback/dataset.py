"""Curated dataset definition for `blogfeedback` (data-foundry v2). Evidence: README.md."""

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
)

TARGET = "comments_next_24h"  # 281, the comments in the 24 hours after the base time; shipped as its log1p
# The UCI attribute list (the dataset page): 51-55 count comments, 56-60 the same for trackbacks ("links").
COUNTS = (
    "comments_total",  # 51: comments before the base time
    "comments_last_24h",  # 52: in the 24 hours before the base time
    "comments_24h_to_48h_before",  # 53: between 48 and 24 hours before the base time
    "comments_first_24h",  # 54: in the first 24 hours after publication, before the base time
    "comments_change_24h",  # 55: 52 minus 53
    "links_total",
    "links_last_24h",
    "links_24h_to_48h_before",
    "links_first_24h",
    "links_change_24h",
)
STATS = ("mean", "std", "min", "max", "median")
# 1-50: the five statistics of each of 51-60 over the blog's rows, in this order (a1-a5 are those of a51; checked on
# the data: the published values equal these statistics over the training file, standard deviation with ddof=0).
AGGREGATES = tuple(f"blog_{count}_{stat}" for count in COUNTS for stat in STATS)
# 63-262: presence flags of the 200 words Buza ranked by the gap in comments between posts with and without them
# (chapter, footnote 1); the words are not named.
WORDS = tuple(f"word_{i:03d}" for i in range(1, 201))
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
BASE_WEEKDAY = tuple(f"base_{d}" for d in WEEKDAYS)  # 263-269 (checked: Monday first, against the test file dates)
PUB_WEEKDAY = tuple(f"pub_{d}" for d in WEEKDAYS)  # 270-276
COLUMNS = (
    *AGGREGATES,
    *COUNTS,
    "hours_since_publication",  # 61
    "post_length",  # 62
    *WORDS,
    *BASE_WEEKDAY,
    *PUB_WEEKDAY,
    "parent_posts",  # 277: posts this post replies to by trackback
    "parent_comments_min",  # 278-280: comments those parents received
    "parent_comments_max",
    "parent_comments_mean",
    TARGET,
)
# Constant in every row: the blogs' minimum of three counts is 0 for every blog, and `parent_comments_min` is a broken
# source column: 0 wherever there is a parent, even in the 249 one-parent rows whose max and mean are above 0 (missing
# without a parent, step 5).
CONSTANT = (
    "blog_comments_24h_to_48h_before_min",
    "blog_links_last_24h_min",
    "blog_links_24h_to_48h_before_min",
    "parent_comments_min",
)
# Copies of another column in every row: two blog minimums (of the total and of the first 24 hours), and 22 word flags
# equal to word_003, set only in the 4 training rows of one post that has all 200 words.
COPIES = (
    "blog_comments_first_24h_min",
    "blog_links_first_24h_min",
    *(f"word_{i:03d}" for i in (11, 14, 18, 19, 32, 35, 68, 70, 87, 94, 99, 104, 107, 110, 117, 128, 136, 138, 150)),
    *(f"word_{i:03d}" for i in (174, 181, 188)),
)
TEST_START = pd.Timestamp("2012-01-31")  # day 1 of the test period is 1 February 2012
N_FOLDS = 5  # out-of-fold blog statistics for the training rows
FOLD_SEED = 42


def blog_statistics(counts: np.ndarray, blog: np.ndarray, fold: np.ndarray | None = None) -> np.ndarray:
    """The 50 blog statistics of each row, from the count columns of the blog's other rows.

    Args:
        counts: The 10 count columns (51-60), one row per post and base time.
        blog: The blog of each row.
        fold: The fold of each row. None: statistics over all rows of the blog, as the source computed them; else
            over the blog's rows in the other folds (NaN when there are none).

    Returns:
        An array of shape (rows, 50), the statistics of each count column in the order of ``AGGREGATES``, rounded to
        float32 like the published values.
    """
    out = np.full((len(counts), len(AGGREGATES)), np.nan)
    fold = np.zeros(len(counts), dtype=int) if fold is None else fold
    all_rows = fold.max() == 0
    _, blog_ids = np.unique(blog, return_inverse=True)
    order = np.argsort(blog_ids, kind="stable")
    starts = np.flatnonzero(np.r_[True, np.diff(blog_ids[order]) != 0])
    for rows in np.split(order, starts[1:]):
        for k in np.unique(fold[rows]):
            target = rows[fold[rows] == k]
            others = counts[rows] if all_rows else counts[rows[fold[rows] != k]]
            if len(others) == 0:
                continue
            stats = np.stack(
                [others.mean(0), others.std(0), others.min(0), others.max(0), np.median(others, 0)], axis=1
            )
            out[target] = stats.reshape(-1)
    return out.astype(np.float32).astype(np.float64)


def post_folds(df: pd.DataFrame) -> np.ndarray:
    """A fold per post: the blog (its published statistics), the text and the publication weekday identify a post."""
    key = pd.util.hash_pandas_object(df[[*AGGREGATES, "post_length", *WORDS, *PUB_WEEKDAY]], index=False)
    _, post_ids = np.unique(key.to_numpy(), return_inverse=True)
    fold_of_post = np.random.default_rng(FOLD_SEED).permutation(post_ids.max() + 1) % N_FOLDS
    return fold_of_post[post_ids]


class Blogfeedback(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How many comments will a post on a Hungarian blog receive in the next 24 hours, given its comments and "
            "trackbacks so far?"
        ),
        use_case=(
            "A social-media monitoring service decides each morning which of the blog posts published in the last 72 "
            "hours its analysts follow, from the comments each is expected to draw over the next day. The source is "
            "such a service: Buza's prototype with Capgemini Magyarország for companies that 'might have to react "
            "quickly' to news about them (chapter, abstract and Sec. 1)."
        ),
        row=(
            "One post at one daily base time, at most 72 hours after it was published, on one of at least 554 "
            "Hungarian blogs (the crawl covered 'roughly 1200 sources', chapter Sec. 5.1): the training crawl of "
            "2010-2011 and the 60 test days of February and March 2012. Most posts appear at three base times."
        ),
        predicted=(
            "The number of comments the post receives in the 24 hours after the base time, shipped on a log scale; "
            "65% of the training rows and 70% of the test rows get none. Scored per test day by how many of the "
            "day's 10 most-commented posts the predicted top 10 holds."
        ),
        known=(
            "The post's comments and trackbacks before the base time, its age and length, which of 178 words it "
            "contains (from the 200 Buza chose because posts with and without them differ most in comments), the "
            "weekdays of publication and base time, the comments of the posts it replies to, and statistics of the "
            "blog's posts in the training crawl."
        ),
        split=(
            "The test data is the newest 54 of the 60 days of February and March 2012, in nine windows of 6 days; each "
            "window trains on the 2010-2011 crawl and the test days before it."
        ),
        changes=(
            "For the training rows we recompute the blog statistics from the blog's other posts, since as published "
            "they include the post's own later comment counts. We drop copies of a post at the same base time, and a "
            "post length of 0 (no text extracted) becomes missing."
        ),
        fit="approximate",
        fit_reason=(
            "The source names the actor and moment, the features count what was known at the base time, and the "
            "test days follow the training crawl. One gap: the crawl is undated, so the training rows' blog "
            "statistics come from the blog's other posts, earlier and later, while the test rows' come from the past. "
            "Kept with a note: the word flags Buza chose by their link to the comments."
        ),
    )

    # Dataset
    unique_name = "blogfeedback"
    year = "2012"
    domain = "technology & internet"
    source = "Other"  # Buza's release of 2012, named in the chapter (Sec. 5.1); UCI 304 (2014) has the same bytes
    source_url = "http://www.cs.bme.hu/~buza/blogdata.zip"
    license = "CC BY 4.0"  # stated on UCI 304, the copy we download; the 2012 readme states none
    data_tags = ("Anonymized",)
    download_description = """
        We download UCI's copy (dataset 304, 2014); its 61 CSV files are byte-identical to Buza's release of 2012 (http://www.cs.bme.hu/~buza/blogdata.zip, files dated 2012-07-24).
        wget https://archive.ics.uci.edu/static/public/304/blogfeedback.zip   # DOI 10.24432/C58S3F
        mkdir -p local-data-warehouse/blogfeedback && unzip blogfeedback.zip -d local-data-warehouse/blogfeedback
        rm blogfeedback.zip
        # blogData_train.csv and the 60 files blogData_test-2012.MM.DD.HH_00.csv, no header, 281 columns.
        # The zip of 2014-05-29 had sha256 1ba74e5ad920f7cd037502b2968581cc695146a226a73eff52fe8ad875ed4bcf on 2026-11-01.
    """
    bibtex = r"""
        @incollection{buza2014feedback,
          author = {Buza, Krisztian},
          title = {Feedback Prediction for Blogs},
          booktitle = {Data Analysis, Machine Learning and Knowledge Discovery},
          publisher = {Springer},
          year = {2014},
          pages = {145--152},
          doi = {10.1007/978-3-319-01595-8\_16},
          note = {Author's copy: \url{http://www.cs.bme.hu/~buza/pdfs/gfkl2012_blogs.pdf}}
        }
        @misc{buza2012blogdata,
          author = {Buza, Krisztian},
          title = {{BlogFeedback} data},
          year = {2012},
          howpublished = {\url{http://www.cs.bme.hu/~buza/blogdata.zip}},
          note = {Re-released as UCI Machine Learning Repository dataset 304 (2014), doi:10.24432/C58S3F}
        }
    """
    curation_comments = """
        We start with blogData_train.csv and the 60 daily test files of UCI 304, byte-identical to Buza's 2012 release (blogdata.zip, chapter Sec. 5.1): posts of at least 554 Hungarian blogs (the chapter crawled "roughly 1200 sources").

        - Prediction point: the daily base time, at most 72 hours after publication (UCI: "we calculate all the features of the selected blog posts from the information that was available at the basetime"). The target, the comments in the next 24 hours, ships as log1p (CLEAN-16); 65% of training and 70% of test rows are observed zeros.
        - Leak, fixed (LEAK-10, CLEAN-7): as published, a training row's 50 blog statistics cover every row of its blog in the training file, the post's own later rows included (`blog_statistics(..., None)` gives them back, decision 1). We recompute them over the blog's rows in the other 4 of 5 folds of whole posts (`post_folds`); 250 rows of blogs in one fold get missing values. The test rows keep the published values, statistics over the training rows only (LEAK-29).
        - Known blog (USE-10): 713 test rows (10.1%) carry the all-zero vector, and 24.8% of them had comments before the base time, against none of the training rows with that vector as published: probably blogs without training rows (0 here, missing on the training side). Predictions stay calibrated on them (predicted and observed shares with a comment within 0.015 per window).
        - Not removed: the recomputed statistics include the blog's later posts and, in small blogs, still move a little with the row's own outcome (Spearman -0.23 within blogs of 2-5 posts), so tuning on training rows is slightly optimistic (the statistics add 0.061 to R^2 on log1p in post-grouped folds of the crawl, 0.043 on test), and the out-of-fold maximum is below the full-crawl value the test rows carry in 22% of training rows. Untuned LightGBM, 3 windows x 2 seeds: RMSLE 0.620 with the published, 0.622 with the recomputed, 0.659 without statistics.
        - Note: the parents' comments are counts at each base time: with an unchanged set of parents they only rise between a post's base times (96 and 97 rises in 1,587 pairs) and fall only when the set shrinks (702 of 731 changes). The chapter (Sec. 4.2) does not say when they were counted.
        - Potential leak, kept on purpose: the word flags are "the 200 most discriminative words" (chapter, footnote 1), ranked by the gap in comments between posts with and without them, on posts the chapter does not name, possibly the test days. They add nothing: RMSLE 0.622 with and 0.620 without, Hits@10 6.61 with and 6.74 without (3 windows x 2 seeds); in the chapter's Table 1 they lower Hits@10 for 6 of 7 models. Kept while the curator decides; revisit if Buza's word list or documents become known.
        - Copies (LEAK-19, decision 2): 3,194 exact copies in the training file and 588 within a test day are dropped after the statistics, one kept; the 17 copies across test days (distinct posts), 13 text-less training pairs the recomputation makes identical and 410 text-less rows whose features recur with another target stay.
        - CLEAN-10: `post_length` 0 (23% of training and 20% of test rows, never with a word) is a text-extraction gap: 100 blogs without text in any row hold 90% of them. It becomes missing, as do the parents' comments without a parent (a stored 0).
        - CLEAN-5: dropped 4 constant columns (three blog minimums; `parent_comments_min`, a broken source column) and 24 copies (two blog minimums; 22 word flags equal to `word_003`). The weekday blocks become `basetime_weekday` and `publication_weekday` (CLEAN-13; Monday first, checked against the file dates); the 0/1 word flags are categorical (CLEAN-14).
        - `basetime_day` is the time column and a feature: the test file's day (1 = 1 February 2012), 0 for the undated training crawl. It is also the metric's group, a test day (MET-2 does not cover the time column used as the metric's group; Andrej, 2026-11-02).
        - Metric (MET-1; MET-7, the source fixes k = 10 a day): Buza's Hits@10 per test day, as `mean_group_top_k_overlap` with k = 10 and the day as the group (CC 2026-11-02, Andrej); the score is Hits@10 / 10, and the target's log1p does not change a ranking. It replaces the RMSLE stand-in of the review panel, which pooled rows across days (Kendall tau 0.61-0.88 per window against Hits@10), and RMSE on the count, which follows a few viral posts (the top 1% of test rows hold 66-93% of its squared error) and rated a sort by the last day's comments (5.6 hits a day) below the training mean (0.9). Each window has 6 test days, each with at least 10 posts that get comments.
        - TP-10, untuned LightGBM, seed 0: RMSLE 0.622 against 0.756 for the best per-post rule (last-24-hour comments times a factor fitted on the training side), and 0.94 more of each day's top 10 than a sort by last-24-hour comments (paired SE 0.25-0.27 per window); better in 3 of 3 windows on both. Leg 2: `comments_24h_to_48h_before` and `comments_change_24h` are the source's window counts over a life of at most 72 hours, summaries of the series up to the prediction point (g_research_crypto_forecasting, rain_in_australia).
    """

    # Task
    target = "log1p_comments_next_24h"
    problem_type = "regression"
    metric = Metric.source(
        "mean_group_top_k_overlap",
        original=(
            "Hits@10 per test day: of the 10 posts predicted to draw the most comments in the next 24 hours, how many "
            "are among the day's 10 most-commented, averaged over the test days (chapter Sec. 5.1, p. 5; Table 1 "
            "reports AUC@10, a ROC AUC with the day's true top 10 as positives, beside it). The metric is Hits@10 / "
            "10, the share of the day's true top 10 found; ties at the 10th place count by their expected share"
        ),
        reference="http://www.cs.bme.hu/~buza/pdfs/gfkl2012_blogs.pdf",
        params={"k": 10},
        inputs={"group": "basetime_day"},
        target_transform="log1p",
    )
    splits_comment = """
        UCI ships a temporally disjoint split: an undated training crawl with base times in 2010-2011 and 60 daily test files of February and March 2012 (UCI: use "the provided, temporally disjoint train and test splits"); the source trains once on the crawl and predicts all 60 test days (chapter Sec. 5.1). We keep it and cut the newest 54 test days into nine windows of 6 days, newest first, as many windows as SPLIT-15 gives a task of this size (Andrej, 2026-11-03: "With the given sample size we would prioritize 9 folds"); each trains on the training crawl and every earlier test day, and test days 1 to 6 (1 to 6 February) are only ever training rows. A row's label is known 24 hours after its base time, at the next day's base time, so no gap is needed. Each window is a model refit up to 6 days earlier, a service that retrains weekly; the source refits once for 60 days. The crawl is a single time value, so only the 7,036 rows of the test days can be test rows (about 700 per window); for the same reason the training history cannot be trimmed to a recent stretch (SPLIT-20). Under Hits@10 a 6-day window measures a difference between two models with a standard error of about 0.48 hits a day (0.26 for 20 days), so the nine windows are read together. The measurements in the curation notes were taken on the earlier three windows of 20 days (days 41-60, 21-40 and 1-20).
    """
    temporal = Temporal(
        on="basetime_day",
        splits=TemporalSplits(window=6, unit="unique", n_windows=9),
        horizon=6,
        horizon_unit="days",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        files = [raw_dir / "blogData_train.csv", *sorted(raw_dir.glob("blogData_test-*.csv"))]
        parts = []
        for path in files:
            part = pd.read_csv(path, header=None, names=list(COLUMNS), dtype=np.float64)
            parts.append(pd.concat([part, pd.Series(path.name, index=part.index, name="file")], axis=1))
        return pd.concat(parts, ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. The day of the base time from the test file's name; 0 for the training crawl (no dates published).
        date = df["file"].str.extract(r"test-(\d{4}\.\d\d\.\d\d)", expand=False)
        day = (pd.to_datetime(date, format="%Y.%m.%d") - TEST_START).dt.days
        df["basetime_day"] = day.fillna(0).astype(int)
        train = df["basetime_day"].eq(0).to_numpy()
        # 2. Exact copies of a post at the same base time (LEAK-19), within the training file and within a test day,
        #    found on the published columns (3,194 and 588 rows); dropped after step 3, which counts them as the
        #    source did.
        copy = df.duplicated(subset=[*COLUMNS, "basetime_day"]).to_numpy()
        # 3. Out-of-fold blog statistics for the training rows (LEAK-10): 5 folds of whole posts, each row from the
        #    blog's rows in the other folds, over the training file with its copies. `blog_statistics(..., None)`
        #    gives the published values back (99.6% of the cells within 1e-5, the rest float32 rounding of the
        #    source's standard deviation), the decision table compares them.
        tr = df.loc[train]
        blog = pd.util.hash_pandas_object(tr[list(AGGREGATES)], index=False).to_numpy()
        df.loc[train, list(AGGREGATES)] = blog_statistics(tr[list(COUNTS)].to_numpy(), blog, post_folds(tr))
        df = df.loc[~copy]
        # 4. The weekday blocks (one flag per row) as categories (CLEAN-12, CLEAN-13).
        for name, block in (("basetime_weekday", BASE_WEEKDAY), ("publication_weekday", PUB_WEEKDAY)):
            assert df[list(block)].sum(axis=1).eq(1).all(), f"{name}: not one flag per row"
            df[name] = np.array(WEEKDAYS)[df[list(block)].to_numpy().argmax(1)]
        # 5. Stored zeros that are not measurements (CLEAN-10): without a parent post the parents' comment statistics, and
        #    a post length of 0, a text-extraction gap per blog (after step 3, whose post key reads the raw length).
        no_parent = df["parent_posts"].eq(0)
        df.loc[no_parent, ["parent_comments_min", "parent_comments_max", "parent_comments_mean"]] = np.nan
        df.loc[df["post_length"].eq(0), "post_length"] = np.nan
        df[list(WORDS)] = df[list(WORDS)].astype(int)
        # 6. Constant columns and copies of another column (CLEAN-5).
        out = df.drop(columns=[*BASE_WEEKDAY, *PUB_WEEKDAY, "file", *CONSTANT, *COPIES, TARGET])
        # 7. The target on the log scale (CLEAN-16); the metric ranks each day's posts, which the log does not change.
        return pd.concat([out, np.log1p(df[TARGET]).rename(self.target)], axis=1)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["basetime_weekday", "publication_weekday", *(w for w in WORDS if w in df)])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        is_train = raw["file"].eq("blogData_train.csv").to_numpy()
        tr, te = raw.loc[is_train], raw.loc[~is_train]
        counts = list(COUNTS)
        blog_tr = pd.util.hash_pandas_object(tr[list(AGGREGATES)], index=False).to_numpy()
        in_sample = blog_statistics(tr[counts].to_numpy(), blog_tr, None)
        oof = blog_statistics(tr[counts].to_numpy(), blog_tr, post_folds(tr))
        # the test rows' statistics against the same statistics over the blog's training rows and over the test files
        both = pd.concat([tr, te])
        blog_both = pd.util.hash_pandas_object(both[list(AGGREGATES)], index=False).to_numpy()
        part = np.r_[np.zeros(len(tr), int), np.ones(len(te), int)]  # the test rows from the training rows only
        over_train = blog_statistics(both[counts].to_numpy(), blog_both, part)[len(tr) :]
        blog_te = pd.util.hash_pandas_object(te[list(AGGREGATES)], index=False).to_numpy()
        over_test = blog_statistics(te[counts].to_numpy(), blog_te, None)

        def share(a: np.ndarray, b: np.ndarray) -> float:
            return round(float(np.all(np.isclose(a, b, rtol=1e-3, atol=1e-3), axis=1).mean()), 4)

        published_tr, published_te = tr[list(AGGREGATES)].to_numpy(), te[list(AGGREGATES)].to_numpy()
        table = pd.DataFrame(
            {
                "rows": ["training file", "training file", "test files", "test files"],
                "published statistics equal to": [
                    "the blog's statistics over all its training rows",
                    "the out-of-fold statistics we ship",
                    "the blog's statistics over its training rows",
                    "the blog's statistics over its test rows",
                ],
                "share of rows (all 50 within 0.1%)": [
                    share(published_tr, in_sample),
                    share(published_tr, oof),
                    share(published_te, over_train),
                    share(published_te, over_test),
                ],
            }
        )
        # copies of a post at the same base time, and feature vectors with more than one target
        copies = raw.duplicated(subset=[*COLUMNS, "file"])
        features = [c for c in COLUMNS if c != TARGET]
        vectors = raw.loc[~copies & is_train].groupby(features, sort=False)[TARGET].nunique()
        dups = pd.DataFrame(
            {
                "part": ["training file", "test files (within a day)", "test files (across days, kept)"],
                "rows": [int(is_train.sum()), int((~is_train).sum()), int((~is_train).sum())],
                "exact copies": [
                    int((copies & is_train).sum()),
                    int((copies & ~is_train).sum()),
                    int((raw.loc[~is_train].duplicated(subset=COLUMNS) & ~copies[~is_train]).sum()),
                ],
                "copies without text": [
                    int((copies & is_train & raw["post_length"].eq(0)).sum()),
                    int((copies & ~is_train & raw["post_length"].eq(0)).sum()),
                    None,
                ],
            }
        )
        dups["feature vectors with 2+ targets (after dropping copies)"] = [int((vectors > 1).sum()), None, None]
        return [
            Decision(
                title="The blog statistics of the training rows are recomputed out of fold",
                why=(
                    "As published, a training row's 50 blog statistics are computed over every row of its blog in the "
                    "training file, the same post at later base times included, so they hold the row's own target. "
                    "The test rows' statistics are history from the training file. We recompute the training rows' "
                    "statistics from the blog's posts in the other 4 of 5 folds of whole posts."
                ),
                evidence=table,
            ),
            Decision(
                title="Exact copies of a post at the same base time are dropped",
                why=(
                    "A copy repeats a post at the same base time with the same label (most training copies sit next "
                    "to the original in the file): one is kept (LEAK-19). Feature vectors with two targets are posts "
                    "without text that the features cannot tell apart; they stay."
                ),
                evidence=dups,
            ),
        ]
