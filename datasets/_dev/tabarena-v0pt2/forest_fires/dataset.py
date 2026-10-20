"""Curated dataset definition for `forest_fires` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, TaskSummary, anonymize_ids

DAILY_FWI_CODES = ["FFMC", "DMC", "DC", "ISI"]
"""The fire weather index values the park's station computes once a day; equal values mark the same day."""


class ForestFires(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How large an area will a forest fire burn?",
        use_case=(
            "When a fire breaks out in the Montesinho natural park, the fire service estimates from the weather how "
            "large it will grow, to decide where to send air tankers and ground crews (the paper's stated use)."
        ),
        row=("One forest fire in the Montesinho natural park in northeast Portugal, 2000-2003 (517 fires)."),
        predicted="The burned area in hectares, on a log scale; 48% of the fires burned 0 ha.",
        known=(
            "The fire's square on a grid map of the park, the month and weekday, four components of the Canadian fire"
            " weather index, and the temperature, humidity, wind and rain."
        ),
        split=(
            "Whole fire days are held out (fires sharing the day's fire weather index values), so the test data stands"
            " for fires on days the model has not seen; the year is not in the data."
        ),
        fit="approximate",
        fit_reason=(
            "The days are reconstructed from the daily fire weather index values, since the data has no date, and "
            "test days come from the same years rather than later ones. Under this split the models do not beat the "
            "training mean."
        ),
    )

    # Dataset
    unique_name = "forest_fires"
    year = "2008"
    domain = "environmental science & climate"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5D88D"
    license = "CC BY 4.0"
    data_tags = ("Spatial",)
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/162/forest+fires.zip && unzip forest+fires.zip && rm forest+fires.zip forestfires.names
        mkdir -p local-data-warehouse/forest_fires && mv forestfires.csv local-data-warehouse/forest_fires/
    """
    bibtex = r"""
        @article{cortez2007data,
          title={A data mining approach to predict forest fires using meteorological data},
          author={Cortez, Paulo and Morais, An{\'\i}bal de Jesus Raimundo},
          year={2007},
          publisher={Associa{\c{c}}{\~a}o Portuguesa para a Intelig{\^e}ncia Artificial (APPIA)}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - The original paper used random 10-fold cross-validation. The data does not contain dates, only month and weekday over four years (January 2000 to December 2003, Cortez and Morais 2007, Sec. 2), so a split by time is impossible. A split by day is possible, and we use it (see below), which marks the task as Non-IID, so there is no ForcedIIDFromTemporal tag. The task in the paper was also about feature selection (so scientific discovery).
        - Day-grouped splits (2026-10-19), not random ones. FFMC, DMC, DC and ISI are the station's daily values of the Canadian Fire Weather Index (moisture codes of the fine fuel, the duff layer and deep drought, each carried over from the previous day, and the spread index computed from FFMC and the day's wind), so fires with the same four values burned on the same day: 517 fires on 227 days, the largest 10 fires, 402 fires sharing their day. Within a day the four values never differ, while temperature, humidity and wind differ on 95-96% of the days with several fires and the map square on 81-86%, so these are separate fires with their own readings. 9 of the 227 days carry two weekdays and 2 of them two months (entry errors or codes carried over); grouping on the codes keeps them together. On random splits TabPFN-3.5 beats the training mean (R^2 0.012, above all 200 shuffles of the labels, p = 0.005), on day-grouped splits it does not (R^2 -0.002 on 60 splits; on 12 of them +0.001, p = 0.16 against 200 shuffles on the same splits): the signal came from fires of the same day on both sides of the split. The use case sizes a fire from that day's weather, and no fire of that day is in the training data. Evidence: `~/claude_jobs/forest_fires_review/`, curation record (Andrej, 2026-10-19).
        - The source itself finds no method better than the mean on RMSE: "The best RMSE was attained by the naive mean predictor" (UCI notes on Cortez and Morais 2007); the paper's best model wins on the mean absolute deviation by predicting small fires better.
        - We log1p scale the target as suggest by the authors.
        - The data contains naturally occurring duplicates.
    """

    # Task
    target = "area"
    problem_type = "regression"
    grouping = Grouping(
        on="fire_day",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a day: the fires with the same daily fire weather index values (FFMC, DMC, DC, ISI), which the park's weather station computes once a day (Cortez and Morais 2007, Sec. 2). The data has no date, so the day is reconstructed from these values. The use case is sizing a new fire from that day's weather to send crews, and no fire of the same day is known then, so whole days are held out; the paper split fires at random. Each fire is one prediction, made from its own row.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on fire_day: all fires of one day (same daily fire weather index values) stay on one side, so a model predicts fires on days it has not seen. Days of the same season can be on both sides. The paper uses random 10-fold cross-validation.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "forestfires.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df["area"] = np.log1p(df["area"])
        # The split groups: one day per combination of the station's daily fire weather index values
        day = df[DAILY_FWI_CODES].astype(str).agg("|".join, axis=1)
        df["fire_day"] = anonymize_ids(day)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "fire_day",
                "month",
                "day",
            ],
        )
