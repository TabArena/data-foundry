"""Curated dataset definition for `wine_quality` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class WineQuality(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("What quality score would expert tasters give a Vinho Verde wine, judging from its lab analysis?"),
        use_case=(
            "A wine certification body or producer estimates the tasting panel's score from routine lab tests, to "
            "support the tasters' evaluation (Cortez et al. 2009)."
        ),
        row=(
            "One red or white Vinho Verde wine sample from the Portuguese certification body, May 2004 to February "
            "2007 (5,320 samples)."
        ),
        predicted="The median of at least three expert scores, on a scale of 0 to 10.",
        known=(
            "Eleven lab measurements (fixed and volatile acidity, citric acid, residual sugar, chlorides, free and "
            "total sulphur dioxide, density, pH, sulphates, alcohol) and the wine's colour."
        ),
        split=("Random wine samples, so the test data stands for new samples of the same region and years."),
        changes=(
            "We drop 1,177 exact repeated rows (18%), most likely repeated records from the export, which put a row's"
            " twin in training."
        ),
        fit="direct",
        fit_reason=(
            "The lab values are measured as part of certification alongside the tasting, and random samples of the "
            "same years match scoring new wines of the same process."
        ),
    )

    # Dataset
    unique_name = "wine_quality"
    year = "2009"
    domain = "chemistry & material science"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C56S3T"
    license = "CC BY 4.0"
    download_description = """
        Download from UCI and uzip data to a predefined folder.
        mkdir -p local-data-warehouse/wine_quality/ && wget -P local-data-warehouse/wine_quality/ https://archive.ics.uci.edu/static/public/186/wine+quality.zip && unzip local-data-warehouse/wine_quality/wine+quality.zip -d local-data-warehouse/wine_quality/ && rm local-data-warehouse/wine_quality/wine+quality.zip
    """
    bibtex = r"""
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
    """
    curation_comments = """
        - We combine the original datasets for red and white wine into a single dataset with an additional column indicating the type of wine (red or white).
        - We treat the task as a regression problem, following the original work and because the target is the median wine quality (of at least 3 evaluations by experts).
        - We drop exact duplicate rows (1,177 of 6,497, 18%): identical in all 11 physicochemical values, the colour and the median score; no identical feature vector carries two different scores. The paper builds "a distinct wine sample (with all tests) per row" (Cortez et al. 2009, Sec. 2.1), so the copies are most likely repeated records from exporting the certification system's per-test entries, and under a random split they put a row's twin in train. We keep the IID split: grouping identical rows would only reproduce this deduplication.
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
        df = pd.concat([df_white, df_red], ignore_index=True)
        df.columns = df.columns.str.replace(" ", "_")
        target_feature = "median_wine_quality"
        df = df.rename(columns={"quality": target_feature})
        # Exact copies (all 11 lab values, colour and the median score): the paper builds "a distinct wine sample
        # (with all tests) per row" (Cortez et al. 2009, Sec. 2.1), so a repeated row adds no information
        df = df[~df.duplicated()].reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "wine_color",
            ],
        )
