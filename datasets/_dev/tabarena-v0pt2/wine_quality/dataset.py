"""Curated dataset definition for `wine_quality` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, Temporal, TemporalSplits


class WineQuality(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("What quality score would expert tasters give a Vinho Verde wine, judging from its lab analysis?"),
        use_case=(
            "A wine certification body or producer estimates the tasting panel's score from routine lab tests, to "
            "support the tasters' evaluation (Cortez et al. 2009)."
        ),
        row=(
            "One red or white Vinho Verde wine sample from the Portuguese certification body, May 2004 to February "
            "2007 (5,271 samples)."
        ),
        predicted="The median of at least three expert scores, on a scale of 0 to 10.",
        known=(
            "Eleven lab measurements (fixed and volatile acidity, citric acid, residual sugar, chlorides, free and "
            "total sulphur dioxide, density, pH, sulphates, alcohol) and the wine's colour."
        ),
        split=(
            "Nine windows of 295 wines over the newest half of the file order, each trained on all earlier wines, so "
            "the test data stands for wines graded later. The release has no dates: the file order is taken as the "
            "order of entry, a judgement call from the data, not documented by the source."
        ),
        changes=(
            "We drop 1,177 exact repeated rows (18%), most likely repeated records from the export, and 49 rows that "
            "repeat another wine with one or two lab values re-entered, so each wine counts once. We add each row's position in its colour file as the time order of the split, not "
            "as a model input."
        ),
        fit="direct",
        fit_reason=(
            "The lab values are measured as part of certification alongside the tasting, and windows of later wines "
            "match scoring new wines of the same process; the time order is inferred from the file, not dated."
        ),
    )

    # Dataset
    unique_name = "wine_quality"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C56S3T",
            license="CC BY 4.0",
            year="2009",
            bibtex=r"""
                @article{cortez2009modeling,
                  title={Modeling wine preferences by data mining from physicochemical properties},
                  author={Cortez, Paulo and Cerdeira, Ant{\'o}nio and Almeida, Fernando and Matos, Telmo and Reis, Jos{\'e}},
                  journal={Decision support systems},
                  volume={47},
                  number={4},
                  pages={547--553},
                  year={2009},
                  publisher={Elsevier}
                }
            """,
        ),
    )
    download_description = """
        Download from UCI and uzip data to a predefined folder.
        mkdir -p local-data-warehouse/wine_quality/ && wget -P local-data-warehouse/wine_quality/ https://archive.ics.uci.edu/static/public/186/wine+quality.zip && unzip local-data-warehouse/wine_quality/wine+quality.zip -d local-data-warehouse/wine_quality/ && rm local-data-warehouse/wine_quality/wine+quality.zip
    """
    curation_comments = """
        - We combine the original datasets for red and white wine into a single dataset with an additional column indicating the type of wine (red or white).
        - We treat the task as a regression problem, following the original work and because the target is the median wine quality (of at least 3 evaluations by experts).
        - We drop exact duplicate rows (1,177 of 6,497, 18%): identical in all 11 physicochemical values, the colour and the median score; no identical feature vector carries two different scores. The paper builds "a distinct wine sample (with all tests) per row" (Cortez et al. 2009, Sec. 2.1), so the copies are most likely repeated records from exporting the certification system's per-test entries, and under a random split they put a row's twin in train. Grouping identical rows would only reproduce this deduplication.
        - We also drop 49 near-copies (2026-11-13, Andrej, review issue 1, B): pairs of one colour that agree on 10 of
          the 11 lab values (47 pairs) or 9 (2 pairs), keeping the first in file order (41 white, 8 red rows leave;
          5,271 wines). They are double entries, not retests: 1 value differs (fixed acidity, alcohol, residual sugar
          or total sulphur dioxide only), against 3 to 6 in the 115 pairs analysed twice that we keep; the grade agrees
          in 49 of 49 pairs, against 76% in the retests; alcohol differs by exactly 1/60 or 1/30 (9.2333 against 9.25),
          arithmetic rather than measurement; and the rows sit 1 to 17 rows apart like the exact copies. The grade
          shares move by at most 0.04 points (mean 5.796 to 5.794). `file_position` is computed before the drop, so
          positions are those of the raw file.
        - Density is recorded with 5 decimals in 2,443 rows and 4 or fewer in 2,877; the 5-decimal rows grade about
          0.1 higher in both colours (red 5.68 against 5.57, white 5.90 against 5.81), a recording batch (an
          instrument or a period; the source does not say), kept as published (2026-11-13, Andrej, review issue 2,
          B). A model reads it only through an engineered count of decimals; the fifth decimal (0.00001) is far below
          the spread between wines (about 0.003).
        - Split by file position, a judgement call (2026-11-13, Andrej, review issue 3, B). The release dates the wines
          only as May 2004 to February 2007 and keeps no sample number, so `file_position` (a row's share of its
          own colour file, 0 first, 1 last) stands in for time; it is no date, and putting both colours on one axis
          assumes both were entered at a steady pace over the same period. Readings of the file order weighed:
          order of entry in the certification body's iLab system; a producer's request entered together within it;
          sorted by producer; sorted by a file column; sorted by a dropped attribute (grape, brand); shuffled. The
          data leave only the first two. No column is sorted, and neighbouring rows are alike (grade runs, position
          explains up to 31% of a column's variance), which rules out a shuffle and a sort by column. Both colour
          files write density with 5 decimals in the same stretches (a burst at 12-20% of each file, almost none at
          33-46%, about 82% from 46% on), a change in the lab's recording that a sort by producer would scatter.
          Both drift alike (mean grade per tenth of each file r = 0.78 between the colours, at most 0.48 for any
          shifted pairing), with a wave of 36-46% of each file, about a year if the 33 months are spread evenly.
          Repeated rows sit within 17 rows of their copy (240 of 240 red, 925 of 937 white). On the same test wines
          at equal training size (untuned LightGBM, MAE), training on random wines scores 0.528, on wines before and
          after the window 0.535, on earlier wines only 0.546: earlier wines predict worse than wines from both sides,
          as drift in time does, while under a sort by producer both sides would be equally new. CVRVV sample numbers
          or dates that show another order (a sort by producer, say) would overturn the split.
        - `file_position` is no model input (`Temporal(..., feature=False)`): it is a row's place in an exported
          file, which the certification body does not hold when it grades a wine.
    """

    # Task
    target = "median_wine_quality"
    problem_type = "regression"
    metric = Metric.source(
        "mae",
        original="MAD (mean absolute deviation), with REC accuracy at tolerance T=0.25/0.5/1.0 and Kappa",
        reference="Cortez et al. 2009, Decision Support Systems 47(4):547-553",
        definition="Mean absolute error of the predicted median quality grade",
    )
    # Splits
    splits_comment = """
        Nine test windows of 295 wines over the newest half by file position, each trained on every earlier wine (2,616
        to 4,976 wines, 50% to 94% of the rows); a window stands for the next wines the certification body grades. The release has no
        date: the file order is taken as the order of entry, inferred from the data and not documented, so the split
        is a judgement call (the curation notes give the readings weighed and the evidence). `file_position` is a
        row's share of its colour file, no date, and assumes both files were entered at a steady pace. No gap: the
        grade is given at the tasting that dates the row.
    """
    temporal = Temporal(
        on="file_position",
        splits=TemporalSplits(window=295, unit="rows", n_windows=9),
        feature=False,  # a row's place in an exported file, not held by the grader (2026-11-13, Andrej)
    )
    accepted_check_warnings = {
        "task_target_low_cardinality": "The target is the median of at least three expert grades on a 0-10 scale "
        "(7 values occur); the paper models it as regression (Cortez et al. 2009, Sec. 2.2).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df_red = pd.read_csv(raw_dir / "winequality-red.csv", sep=";")
        df_white = pd.read_csv(raw_dir / "winequality-white.csv", sep=";")
        return {"df_red": df_red, "df_white": df_white}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df_red, df_white = raw["df_red"], raw["df_white"]
        df_red["wine_color"] = "red"
        df_white["wine_color"] = "white"
        # Time order of the split: a row's share of its own colour file (0 first, 1 last), the inferred entry order
        for part in (df_red, df_white):
            part["file_position"] = np.arange(len(part)) / len(part)
        df = pd.concat([df_white, df_red], ignore_index=True)
        df.columns = df.columns.str.replace(" ", "_")
        target_feature = "median_wine_quality"
        df = df.rename(columns={"quality": target_feature})
        # Exact copies (all 11 lab values, colour and the median score): the paper builds "a distinct wine sample
        # (with all tests) per row" (Cortez et al. 2009, Sec. 2.1), so a repeated row adds no information
        # (keep first: the earlier entry of a copy)
        df = df[~df.duplicated(subset=[c for c in df.columns if c != "file_position"])].reset_index(drop=True)
        # Near-copies (2026-11-13, Andrej, review issue 1, B): two rows of one colour that agree on at least 9 of the
        # 11 lab values are one wine entered twice with a value re-entered (49 pairs, same grade in all 49); keep the
        # first in file order. file_position was set above, so positions stay those of the raw file.
        lab = [c for c in df.columns if c not in ("wine_color", target_feature, "file_position")]
        later = set()
        for _, colour_rows in df.groupby("wine_color"):
            ordered = colour_rows.sort_values("file_position", kind="stable")
            idx, values = ordered.index.to_numpy(), ordered[lab].to_numpy()
            for a in range(len(idx) - 1):
                n_equal = (values[a + 1 :] == values[a]).sum(axis=1)
                later.update(idx[a + 1 + np.flatnonzero(n_equal >= len(lab) - 2)])
        df = df.drop(index=sorted(later)).reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "wine_color",
            ],
        )
